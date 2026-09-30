import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import api from '../../services/api';
import { useToast } from '../../context/ToastContext';
import MatchProgressBar from '../../components/common/MatchProgressBar';
import StatusBadge from '../../components/common/StatusBadge';
import {
  Sparkles,
  Briefcase,
  Users,
  CheckCircle2,
  XCircle,
  Clock,
  MapPin,
  Building2,
  UserCheck,
  ArrowRight,
  TrendingUp,
} from 'lucide-react';

export default function CandidateMatching() {
  const [searchParams] = useSearchParams();
  const initialJobId = searchParams.get('job_id') || '';
  const { addToast } = useToast();

  const [jobs, setJobs] = useState([]);
  const [selectedJobId, setSelectedJobId] = useState(initialJobId);
  const [matchData, setMatchData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [applyingId, setApplyingId] = useState(null);

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const res = await api.get('/jobs?status=OPEN');
        const jobList = res.data.data.items || [];
        setJobs(jobList);
        if (!selectedJobId && jobList.length > 0) {
          setSelectedJobId(jobList[0].id.toString());
        }
      } catch (err) {
        console.error(err);
      }
    };
    fetchJobs();
  }, []);

  useEffect(() => {
    if (!selectedJobId) return;

    const runMatchingEngine = async () => {
      setLoading(true);
      try {
        const res = await api.get(`/matching/job/${selectedJobId}`);
        setMatchData(res.data.data);
      } catch (err) {
        addToast('Failed to calculate candidate matches', 'error');
      } finally {
        setLoading(false);
      }
    };
    runMatchingEngine();
  }, [selectedJobId]);

  const handleApplyCandidate = async (candidateId) => {
    setApplyingId(candidateId);
    try {
      await api.post('/applications', {
        candidate_id: candidateId,
        job_id: parseInt(selectedJobId),
        notes: 'Shortlisted directly via Intelligent Match Engine',
      });
      addToast('Candidate added to job pipeline!', 'success');
      // Refresh matching to show updated application status
      const res = await api.get(`/matching/job/${selectedJobId}`);
      setMatchData(res.data.data);
    } catch (err) {
      addToast(err.response?.data?.message || 'Failed to map candidate', 'error');
    } finally {
      setApplyingId(null);
    }
  };

  const selectedJob = jobs.find((j) => j.id.toString() === selectedJobId.toString());

  return (
    <div className="space-y-8">
      {/* Engine Hero Header */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 rounded-3xl p-8 text-white border border-slate-800 shadow-xl relative overflow-hidden">
        <div className="absolute right-0 top-0 w-96 h-96 bg-brand-500/10 rounded-full blur-3xl pointer-events-none" />

        <div className="relative z-10">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-400/20 text-amber-300 border border-amber-400/30 text-xs font-bold uppercase tracking-wider mb-3">
            <Sparkles className="w-3.5 h-3.5 text-amber-400" /> Multi-Factor Match Algorithm
          </div>
          <h2 className="text-3xl font-black tracking-tight">Smart Candidate Match Engine</h2>
          <p className="text-slate-300 text-sm mt-1 max-w-2xl">
            Automated rule-based screening engine evaluating skill overlap, experience depth, and location compatibility.
          </p>

          {/* Job Selection Dropdown in Hero */}
          <div className="mt-6 flex flex-col sm:flex-row sm:items-center gap-3">
            <label className="text-xs font-bold text-slate-400 uppercase tracking-wider">
              Select Job Requisition:
            </label>
            <select
              value={selectedJobId}
              onChange={(e) => setSelectedJobId(e.target.value)}
              className="px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-xl text-xs font-semibold text-white focus:outline-none focus:ring-2 focus:ring-brand-500 max-w-md shadow-inner"
            >
              {jobs.map((j) => (
                <option key={j.id} value={j.id}>
                  {j.title} ({j.company_name} • {j.location})
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Selected Job Spec Card */}
      {selectedJob && (
        <div className="bg-white p-6 rounded-3xl border border-slate-200/80 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="space-y-2">
            <div className="flex items-center gap-2.5">
              <span className="text-xs font-bold text-brand-600 bg-brand-50 px-2.5 py-0.5 rounded-lg border border-brand-200/60">
                Target Requisition
              </span>
              <h3 className="text-xl font-black text-slate-900">{selectedJob.title}</h3>
            </div>
            <p className="text-xs text-slate-500 line-clamp-1">{selectedJob.description}</p>
            <div className="flex flex-wrap items-center gap-4 text-xs text-slate-600 pt-1">
              <span className="flex items-center gap-1 font-semibold text-slate-800">
                <Building2 className="w-3.5 h-3.5 text-slate-400" /> {selectedJob.company_name}
              </span>
              <span className="flex items-center gap-1">
                <MapPin className="w-3.5 h-3.5 text-slate-400" /> {selectedJob.location}
              </span>
              <span className="flex items-center gap-1">
                <Clock className="w-3.5 h-3.5 text-slate-400" /> Min {selectedJob.min_experience_years} yrs exp
              </span>
            </div>
          </div>

          <div className="bg-slate-50 p-4 rounded-2xl border border-slate-200/70 text-right flex-shrink-0">
            <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-1">
              Candidates Evaluated
            </p>
            <span className="text-2xl font-black text-slate-900">
              {matchData?.candidates_evaluated || 0}
            </span>
          </div>
        </div>
      )}

      {/* Matching Results Feed */}
      {loading ? (
        <div className="flex items-center justify-center py-24">
          <div className="flex flex-col items-center gap-3">
            <div className="w-10 h-10 border-4 border-brand-500 border-t-transparent rounded-full animate-spin" />
            <p className="text-sm font-semibold text-slate-600">Running compatibility matrix...</p>
          </div>
        </div>
      ) : !matchData || matchData.matches.length === 0 ? (
        <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center">
          <p className="text-slate-500 text-sm">No candidate matches found.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {matchData.matches.map((item, index) => {
            const { candidate, match } = item;
            const isApplied = !!candidate.application_status;

            return (
              <div
                key={candidate.id}
                className="bg-white rounded-3xl border border-slate-200/80 p-6 shadow-sm hover:shadow-md transition flex flex-col lg:flex-row lg:items-center justify-between gap-6"
              >
                {/* Left: Candidate Info & Rank */}
                <div className="flex items-start gap-4 flex-1">
                  <div className="w-10 h-10 rounded-2xl bg-slate-900 text-white flex items-center justify-center font-black text-sm shadow-md flex-shrink-0">
                    #{index + 1}
                  </div>

                  <div className="space-y-2 flex-1">
                    <div className="flex flex-wrap items-center gap-2">
                      <h4 className="text-base font-bold text-slate-900">{candidate.full_name}</h4>
                      <StatusBadge status={candidate.status} />
                      {match.is_recommended && (
                        <span className="px-2.5 py-0.5 bg-emerald-50 text-emerald-700 border border-emerald-200 rounded-full text-[11px] font-bold flex items-center gap-1">
                          <CheckCircle2 className="w-3 h-3 text-emerald-600" /> Recommended Fit
                        </span>
                      )}
                    </div>

                    <div className="flex flex-wrap items-center gap-3 text-xs text-slate-500">
                      <span className="flex items-center gap-1">
                        <MapPin className="w-3.5 h-3.5 text-slate-400" /> {candidate.location}
                      </span>
                      <span className="flex items-center gap-1 font-semibold text-slate-800">
                        <Clock className="w-3.5 h-3.5 text-slate-400" /> {candidate.experience_years} yrs exp
                      </span>
                      <span className="text-slate-400">•</span>
                      <span>{candidate.highest_qualification}</span>
                    </div>

                    {/* Breakdown Chips */}
                    <div className="space-y-2 pt-2">
                      {/* Matched Skills */}
                      <div className="flex flex-wrap items-center gap-1.5 text-xs">
                        <span className="text-[11px] font-bold text-emerald-700 flex items-center gap-1 mr-1">
                          <CheckCircle2 className="w-3 h-3 text-emerald-600" /> Matched Skills:
                        </span>
                        {match.matched_skills.length > 0 ? (
                          match.matched_skills.map((s, idx) => (
                            <span
                              key={idx}
                              className="px-2 py-0.5 bg-emerald-50 text-emerald-800 border border-emerald-200/80 rounded-md text-[11px] font-semibold"
                            >
                              {s}
                            </span>
                          ))
                        ) : (
                          <span className="text-[11px] text-slate-400 italic">None</span>
                        )}
                      </div>

                      {/* Missing Skills */}
                      {match.missing_skills.length > 0 && (
                        <div className="flex flex-wrap items-center gap-1.5 text-xs">
                          <span className="text-[11px] font-bold text-rose-600 flex items-center gap-1 mr-1">
                            <XCircle className="w-3 h-3 text-rose-500" /> Missing Skills:
                          </span>
                          {match.missing_skills.map((s, idx) => (
                            <span
                              key={idx}
                              className="px-2 py-0.5 bg-rose-50 text-rose-700 border border-rose-200/80 rounded-md text-[11px] font-semibold"
                            >
                              {s}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                </div>

                {/* Right: Score Gauge & Shortlist Button */}
                <div className="lg:w-72 flex flex-col justify-between gap-4 pt-4 lg:pt-0 lg:border-l lg:border-slate-100 lg:pl-6">
                  <div>
                    <MatchProgressBar score={match.total_match_score} size="lg" />
                    <div className="grid grid-cols-3 gap-1 text-[10px] text-slate-400 text-center mt-2">
                      <div>
                        <p className="font-bold text-slate-700">{match.skill_match_percentage}%</p>
                        <span>Skills (65%)</span>
                      </div>
                      <div>
                        <p className="font-bold text-slate-700">{match.experience_score}%</p>
                        <span>Exp (25%)</span>
                      </div>
                      <div>
                        <p className="font-bold text-slate-700">{match.location_score}%</p>
                        <span>Loc (10%)</span>
                      </div>
                    </div>
                  </div>

                  {isApplied ? (
                    <div className="flex items-center justify-center gap-2 py-2 px-3 bg-slate-100 text-slate-700 rounded-xl text-xs font-bold">
                      <UserCheck className="w-4 h-4 text-emerald-600" />
                      <span>Pipeline: {candidate.application_status}</span>
                    </div>
                  ) : (
                    <button
                      onClick={() => handleApplyCandidate(candidate.id)}
                      disabled={applyingId === candidate.id}
                      className="w-full py-2.5 bg-gradient-to-r from-brand-600 to-indigo-600 hover:from-brand-700 hover:to-indigo-700 text-white font-bold text-xs rounded-xl shadow-md shadow-brand-500/20 transition flex items-center justify-center gap-2"
                    >
                      {applyingId === candidate.id ? (
                        <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                      ) : (
                        <>
                          <Sparkles className="w-3.5 h-3.5" />
                          <span>Shortlist to Job Pipeline</span>
                        </>
                      )}
                    </button>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
