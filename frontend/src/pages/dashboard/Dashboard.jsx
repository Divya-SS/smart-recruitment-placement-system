import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import StatusBadge from '../../components/common/StatusBadge';
import {
  Users,
  Briefcase,
  Building2,
  CalendarCheck,
  CheckCircle2,
  Sparkles,
  ArrowRight,
  TrendingUp,
  Clock,
  Video,
} from 'lucide-react';

export default function Dashboard() {
  const { user } = useAuth();
  const [metrics, setMetrics] = useState(null);
  const [pipeline, setPipeline] = useState([]);
  const [recentInterviews, setRecentInterviews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [mRes, pRes, iRes] = await Promise.all([
          api.get('/dashboard/metrics'),
          api.get('/dashboard/pipeline'),
          api.get('/dashboard/recent-interviews'),
        ]);
        setMetrics(mRes.data.data);
        setPipeline(pRes.data.data);
        setRecentInterviews(iRes.data.data);
      } catch (err) {
        console.error('Failed to load dashboard data', err);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboardData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="w-10 h-10 border-4 border-brand-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  const statCards = [
    {
      title: 'Total Candidates',
      value: metrics?.total_candidates || 0,
      icon: Users,
      color: 'from-blue-500 to-indigo-600',
      shadow: 'shadow-blue-500/20',
      link: '/candidates',
    },
    {
      title: 'Active Jobs',
      value: metrics?.active_jobs || 0,
      icon: Briefcase,
      color: 'from-emerald-500 to-teal-600',
      shadow: 'shadow-emerald-500/20',
      link: '/jobs',
    },
    {
      title: 'Client Companies',
      value: metrics?.total_companies || 0,
      icon: Building2,
      color: 'from-violet-500 to-purple-600',
      shadow: 'shadow-violet-500/20',
      link: '/companies',
    },
    {
      title: 'Interviews Scheduled',
      value: metrics?.interviews_scheduled || 0,
      icon: CalendarCheck,
      color: 'from-amber-500 to-orange-600',
      shadow: 'shadow-amber-500/20',
      link: '/interviews',
    },
    {
      title: 'Successful Placements',
      value: metrics?.placed_candidates || 0,
      icon: CheckCircle2,
      color: 'from-rose-500 to-pink-600',
      shadow: 'shadow-rose-500/20',
      link: '/applications',
    },
  ];

  return (
    <div className="space-y-8">
      {/* Welcome Hero Banner */}
      <div className="bg-gradient-to-r from-brand-600 via-indigo-600 to-purple-700 rounded-3xl p-8 text-white shadow-xl shadow-brand-500/10 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div>
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/20 backdrop-blur-md text-xs font-bold uppercase tracking-wider text-white mb-3">
            <Sparkles className="w-3.5 h-3.5 text-amber-300" /> Recruitment Intelligence
          </span>
          <h2 className="text-3xl font-black tracking-tight">
            Hello, {user?.full_name?.split(' ')[0] || 'User'}!
          </h2>
          <p className="text-indigo-100 text-sm mt-1 max-w-xl">
            Candidate skill matching algorithm and recruitment pipeline overview are updated and ready.
          </p>
        </div>

        <Link
          to="/matching"
          className="flex items-center gap-2 px-5 py-3 bg-white text-brand-700 hover:bg-indigo-50 font-bold rounded-2xl shadow-lg transition duration-200 text-sm flex-shrink-0"
        >
          <Sparkles className="w-4 h-4 text-brand-600" />
          <span>Launch Match Engine</span>
          <ArrowRight className="w-4 h-4" />
        </Link>
      </div>

      {/* KPI Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-5">
        {statCards.map((card, idx) => {
          const Icon = card.icon;
          return (
            <Link
              key={idx}
              to={card.link}
              className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm hover:shadow-md transition-all group flex flex-col justify-between"
            >
              <div className="flex items-center justify-between mb-4">
                <span className="text-xs font-bold text-slate-500 uppercase tracking-wide">
                  {card.title}
                </span>
                <div
                  className={`w-10 h-10 rounded-xl bg-gradient-to-tr ${card.color} ${card.shadow} flex items-center justify-center text-white shadow-md group-hover:scale-105 transition-transform`}
                >
                  <Icon className="w-5 h-5" />
                </div>
              </div>
              <div className="flex items-baseline justify-between">
                <span className="text-2xl font-black text-slate-900">{card.value}</span>
                <span className="text-xs font-semibold text-brand-600 group-hover:translate-x-0.5 transition-transform flex items-center gap-0.5">
                  View <ArrowRight className="w-3 h-3" />
                </span>
              </div>
            </Link>
          );
        })}
      </div>

      {/* Pipeline Funnel & Upcoming Interviews Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Recruitment Pipeline Stages */}
        <div className="lg:col-span-2 bg-white p-6 rounded-3xl border border-slate-200/80 shadow-sm">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-2.5">
              <TrendingUp className="w-5 h-5 text-brand-600" />
              <h3 className="text-lg font-bold text-slate-800">Recruitment Pipeline Funnel</h3>
            </div>
            <Link
              to="/applications"
              className="text-xs font-bold text-brand-600 hover:text-brand-700 flex items-center gap-1"
            >
              Full Pipeline <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="space-y-4">
            {pipeline.map((stage) => {
              const maxCount = Math.max(...pipeline.map((p) => p.count), 1);
              const percentage = Math.round((stage.count / maxCount) * 100);

              return (
                <div key={stage.stage} className="space-y-1.5">
                  <div className="flex justify-between items-center text-xs">
                    <span className="font-semibold text-slate-700">{stage.label}</span>
                    <span className="font-bold text-slate-900 bg-slate-100 px-2 py-0.5 rounded-md">
                      {stage.count} candidates
                    </span>
                  </div>
                  <div className="w-full h-3 bg-slate-100 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-brand-500 to-indigo-600 rounded-full transition-all duration-700"
                      style={{ width: `${Math.max(percentage, stage.count > 0 ? 8 : 2)}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Scheduled Interviews Feed */}
        <div className="bg-white p-6 rounded-3xl border border-slate-200/80 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center gap-2.5">
                <Clock className="w-5 h-5 text-amber-500" />
                <h3 className="text-lg font-bold text-slate-800">Upcoming Interviews</h3>
              </div>
              <Link
                to="/interviews"
                className="text-xs font-bold text-brand-600 hover:text-brand-700 flex items-center gap-1"
              >
                All <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>

            <div className="space-y-3.5">
              {recentInterviews.length === 0 ? (
                <p className="text-sm text-slate-400 text-center py-8">No interviews scheduled yet</p>
              ) : (
                recentInterviews.map((inv) => (
                  <div
                    key={inv.id}
                    className="p-3.5 bg-slate-50 border border-slate-200/70 rounded-2xl hover:bg-slate-100/70 transition"
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div>
                        <h4 className="text-xs font-bold text-slate-900">{inv.candidate_name}</h4>
                        <p className="text-[11px] text-slate-500">{inv.job_title}</p>
                      </div>
                      <StatusBadge status={inv.status} />
                    </div>
                    <div className="mt-2.5 flex items-center justify-between text-[11px] text-slate-500 pt-2 border-t border-slate-200/60">
                      <span className="font-medium">
                        {new Date(inv.scheduled_at).toLocaleDateString()} at{' '}
                        {new Date(inv.scheduled_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </span>
                      {inv.meeting_link_or_venue && (
                        <a
                          href={inv.meeting_link_or_venue}
                          target="_blank"
                          rel="noreferrer"
                          className="text-brand-600 hover:underline flex items-center gap-1 font-semibold"
                        >
                          <Video className="w-3 h-3" /> Join
                        </a>
                      )}
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

          <Link
            to="/interviews"
            className="mt-6 w-full py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-xl text-center transition block"
          >
            Manage All Interview Rounds
          </Link>
        </div>
      </div>
    </div>
  );
}
