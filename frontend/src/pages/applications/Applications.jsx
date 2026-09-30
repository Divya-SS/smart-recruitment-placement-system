import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import { useToast } from '../../context/ToastContext';
import StatusBadge from '../../components/common/StatusBadge';
import MatchProgressBar from '../../components/common/MatchProgressBar';
import {
  Layers,
  Search,
  Filter,
  ArrowRight,
  Briefcase,
  User,
  Clock,
  Trash2,
  CheckCircle,
} from 'lucide-react';

const PIPELINE_STAGES = [
  { id: 'APPLIED', label: 'Applied', color: 'border-blue-400' },
  { id: 'SHORTLISTED', label: 'Shortlisted', color: 'border-purple-400' },
  { id: 'INTERVIEW_SCHEDULED', label: 'Interview Scheduled', color: 'border-amber-400' },
  { id: 'SELECTED', label: 'Selected', color: 'border-emerald-400' },
  { id: 'JOINED', label: 'Joined / Placed', color: 'border-teal-500' },
  { id: 'REJECTED', label: 'Rejected', color: 'border-rose-400' },
];

export default function Applications() {
  const { isAdmin } = useAuth();
  const { addToast } = useToast();
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [viewMode, setViewMode] = useState('kanban'); // 'kanban' | 'table'

  const fetchApplications = async () => {
    setLoading(true);
    try {
      const params = {};
      if (search) params.search = search;
      const res = await api.get('/applications', { params });
      setApplications(res.data.data.items || []);
    } catch (err) {
      addToast('Failed to load applications', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchApplications();
  }, [search]);

  const handleUpdateStatus = async (appId, newStatus) => {
    try {
      await api.patch(`/applications/${appId}/status`, { status: newStatus });
      addToast(`Candidate moved to ${newStatus}`, 'success');
      fetchApplications();
    } catch (err) {
      addToast(err.response?.data?.message || 'Failed to update status', 'error');
    }
  };

  const handleDelete = async (appId) => {
    if (!window.confirm('Are you sure you want to remove this application?')) return;
    try {
      await api.delete(`/applications/${appId}`);
      addToast('Application removed', 'success');
      fetchApplications();
    } catch (err) {
      addToast(err.response?.data?.message || 'Delete failed', 'error');
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-black text-slate-900 tracking-tight flex items-center gap-2.5">
            <Layers className="w-7 h-7 text-brand-600" /> Candidate Placement Pipeline
          </h2>
          <p className="text-sm text-slate-500 mt-0.5">
            Track candidates through screening, interviews, selection, and final joining.
          </p>
        </div>

        {/* View Switcher */}
        <div className="flex items-center bg-white p-1 rounded-xl border border-slate-200 text-xs font-bold">
          <button
            onClick={() => setViewMode('kanban')}
            className={`px-3 py-1.5 rounded-lg transition ${
              viewMode === 'kanban' ? 'bg-brand-600 text-white shadow-sm' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Kanban Board
          </button>
          <button
            onClick={() => setViewMode('table')}
            className={`px-3 py-1.5 rounded-lg transition ${
              viewMode === 'table' ? 'bg-brand-600 text-white shadow-sm' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Table List
          </button>
        </div>
      </div>

      {/* Search */}
      <div className="bg-white p-4 rounded-2xl border border-slate-200/80 shadow-sm max-w-md">
        <div className="relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 transform -translate-y-1/2" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search by candidate name or job title..."
            className="w-full pl-10 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs focus:outline-none focus:ring-2 focus:ring-brand-500/20"
          />
        </div>
      </div>

      {/* Main View */}
      {loading ? (
        <div className="flex items-center justify-center py-20">
          <div className="w-8 h-8 border-4 border-brand-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : viewMode === 'kanban' ? (
        /* Kanban Columns */
        <div className="grid grid-cols-1 md:grid-cols-3 xl:grid-cols-6 gap-4 items-start">
          {PIPELINE_STAGES.map((col) => {
            const stageApps = applications.filter((a) => a.status === col.id);

            return (
              <div
                key={col.id}
                className="bg-slate-100/80 rounded-2xl p-3 border border-slate-200/80 flex flex-col min-h-[400px]"
              >
                {/* Column Header */}
                <div className="flex items-center justify-between pb-2 mb-3 border-b border-slate-200">
                  <span className="text-xs font-bold text-slate-800">{col.label}</span>
                  <span className="text-[11px] font-extrabold bg-white text-slate-700 px-2 py-0.5 rounded-md shadow-xs">
                    {stageApps.length}
                  </span>
                </div>

                {/* Cards */}
                <div className="space-y-3 flex-1 overflow-y-auto">
                  {stageApps.map((app) => (
                    <div
                      key={app.id}
                      className={`bg-white rounded-xl p-3.5 shadow-sm border border-slate-200/70 border-l-4 ${col.color} space-y-2 hover:shadow-md transition`}
                    >
                      <div>
                        <h4 className="text-xs font-bold text-slate-900 leading-snug">{app.candidate_name}</h4>
                        <p className="text-[11px] text-slate-500 line-clamp-1">{app.job_title}</p>
                      </div>

                      <MatchProgressBar score={app.match_score} size="sm" />

                      {/* Status Transition Select */}
                      <div className="pt-2 border-t border-slate-100 flex items-center justify-between">
                        <select
                          value={app.status}
                          onChange={(e) => handleUpdateStatus(app.id, e.target.value)}
                          className="text-[10px] font-bold bg-slate-50 border border-slate-200 rounded-lg px-2 py-1 focus:outline-none"
                        >
                          {PIPELINE_STAGES.map((s) => (
                            <option key={s.id} value={s.id}>
                              → {s.label}
                            </option>
                          ))}
                        </select>

                        {isAdmin && (
                          <button
                            onClick={() => handleDelete(app.id)}
                            className="text-slate-400 hover:text-rose-600 p-1"
                            title="Delete"
                          >
                            <Trash2 className="w-3.5 h-3.5" />
                          </button>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        /* Table View */
        <div className="bg-white rounded-2xl border border-slate-200/80 overflow-hidden shadow-sm">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 border-b border-slate-200/80 text-slate-600 font-bold uppercase tracking-wider text-[10px]">
              <tr>
                <th className="py-3.5 px-4">Candidate</th>
                <th className="py-3.5 px-4">Target Job</th>
                <th className="py-3.5 px-4">Match %</th>
                <th className="py-3.5 px-4">Current Stage</th>
                <th className="py-3.5 px-4">Advance Status</th>
                {isAdmin && <th className="py-3.5 px-4 text-right">Actions</th>}
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {applications.map((app) => (
                <tr key={app.id} className="hover:bg-slate-50/50 transition">
                  <td className="py-3.5 px-4">
                    <p className="font-bold text-slate-900">{app.candidate_name}</p>
                    <p className="text-[11px] text-slate-400">{app.candidate_email}</p>
                  </td>
                  <td className="py-3.5 px-4">
                    <p className="font-semibold text-slate-800">{app.job_title}</p>
                    <p className="text-[11px] text-slate-500">{app.company_name}</p>
                  </td>
                  <td className="py-3.5 px-4 w-40">
                    <MatchProgressBar score={app.match_score} size="sm" />
                  </td>
                  <td className="py-3.5 px-4">
                    <StatusBadge status={app.status} />
                  </td>
                  <td className="py-3.5 px-4">
                    <select
                      value={app.status}
                      onChange={(e) => handleUpdateStatus(app.id, e.target.value)}
                      className="text-xs font-semibold bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1.5 focus:outline-none"
                    >
                      {PIPELINE_STAGES.map((s) => (
                        <option key={s.id} value={s.id}>
                          {s.label}
                        </option>
                      ))}
                    </select>
                  </td>
                  {isAdmin && (
                    <td className="py-3.5 px-4 text-right">
                      <button
                        onClick={() => handleDelete(app.id)}
                        className="p-1.5 text-slate-400 hover:text-rose-600 rounded-lg"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </td>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
