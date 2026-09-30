import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import { useToast } from '../../context/ToastContext';
import StatusBadge from '../../components/common/StatusBadge';
import Modal from '../../components/common/Modal';
import {
  CalendarCheck,
  Plus,
  Video,
  MapPin,
  Clock,
  Star,
  MessageSquare,
  User,
  CheckCircle2,
  Trash2,
} from 'lucide-react';

export default function Interviews() {
  const { isAdmin } = useAuth();
  const { addToast } = useToast();
  const [interviews, setInterviews] = useState([]);
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);

  // Schedule Modal
  const [isScheduleOpen, setIsScheduleOpen] = useState(false);
  const [scheduleData, setScheduleData] = useState({
    application_id: '',
    interview_round: 'Technical Round 1',
    scheduled_at: '',
    mode: 'ONLINE',
    meeting_link_or_venue: '',
    interviewer_name: '',
    interviewer_email: '',
  });

  // Feedback Modal
  const [isFeedbackOpen, setIsFeedbackOpen] = useState(false);
  const [selectedInterview, setSelectedInterview] = useState(null);
  const [feedbackData, setFeedbackData] = useState({
    technical_rating: 5,
    communication_rating: 5,
    overall_rating: 5,
    comments: '',
    recommendation: 'HIRE',
  });

  const fetchInterviews = async () => {
    setLoading(true);
    try {
      const res = await api.get('/interviews');
      setInterviews(res.data.data.items || []);
    } catch (err) {
      addToast('Failed to load interviews', 'error');
    } finally {
      setLoading(false);
    }
  };

  const fetchApplications = async () => {
    try {
      const res = await api.get('/applications');
      setApplications(res.data.data.items || []);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchInterviews();
    fetchApplications();
  }, []);

  const handleOpenSchedule = () => {
    setScheduleData({
      application_id: applications.length > 0 ? applications[0].id : '',
      interview_round: 'Technical Round 1',
      scheduled_at: new Date(Date.now() + 86400000).toISOString().slice(0, 16),
      mode: 'ONLINE',
      meeting_link_or_venue: 'https://meet.google.com/xyz-demo',
      interviewer_name: '',
      interviewer_email: '',
    });
    setIsScheduleOpen(true);
  };

  const handleScheduleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/interviews', scheduleData);
      addToast('Interview scheduled successfully', 'success');
      setIsScheduleOpen(false);
      fetchInterviews();
    } catch (err) {
      addToast(err.response?.data?.message || 'Failed to schedule', 'error');
    }
  };

  const handleOpenFeedback = (inv) => {
    setSelectedInterview(inv);
    if (inv.feedback) {
      setFeedbackData({
        technical_rating: inv.feedback.technical_rating,
        communication_rating: inv.feedback.communication_rating,
        overall_rating: inv.feedback.overall_rating,
        comments: inv.feedback.comments || '',
        recommendation: inv.feedback.recommendation,
      });
    } else {
      setFeedbackData({
        technical_rating: 5,
        communication_rating: 5,
        overall_rating: 5,
        comments: '',
        recommendation: 'HIRE',
      });
    }
    setIsFeedbackOpen(true);
  };

  const handleFeedbackSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post(`/interviews/${selectedInterview.id}/feedback`, feedbackData);
      addToast('Evaluation feedback recorded successfully', 'success');
      setIsFeedbackOpen(false);
      fetchInterviews();
    } catch (err) {
      addToast(err.response?.data?.message || 'Failed to submit feedback', 'error');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this interview record?')) return;
    try {
      await api.delete(`/interviews/${id}`);
      addToast('Interview removed', 'success');
      fetchInterviews();
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
            <CalendarCheck className="w-7 h-7 text-brand-600" /> Interview Management & Feedback
          </h2>
          <p className="text-sm text-slate-500 mt-0.5">
            Coordinate interview rounds, video meeting links, and structured candidate evaluation scores.
          </p>
        </div>

        <button
          onClick={handleOpenSchedule}
          className="flex items-center gap-2 px-4 py-2.5 bg-brand-600 hover:bg-brand-700 text-white text-xs font-bold rounded-xl shadow-md shadow-brand-500/20 transition"
        >
          <Plus className="w-4 h-4" /> Schedule Interview Round
        </button>
      </div>

      {/* Interviews List */}
      {loading ? (
        <div className="flex items-center justify-center py-20">
          <div className="w-8 h-8 border-4 border-brand-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : interviews.length === 0 ? (
        <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center">
          <p className="text-slate-500 text-sm">No interviews scheduled yet.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {interviews.map((inv) => (
            <div
              key={inv.id}
              className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-sm hover:shadow-md transition flex flex-col justify-between"
            >
              <div>
                <div className="flex items-start justify-between gap-3 mb-2">
                  <div>
                    <span className="text-[11px] font-bold text-brand-600 uppercase tracking-wider">
                      {inv.interview_round}
                    </span>
                    <h3 className="text-lg font-bold text-slate-900 leading-tight mt-0.5">
                      {inv.candidate_name}
                    </h3>
                    <p className="text-xs text-slate-500 mt-0.5 font-medium">{inv.job_title}</p>
                  </div>
                  <StatusBadge status={inv.status} />
                </div>

                <div className="space-y-2 text-xs text-slate-600 my-4 bg-slate-50/70 p-3.5 rounded-xl border border-slate-100">
                  <div className="flex items-center gap-2">
                    <Clock className="w-4 h-4 text-slate-400 flex-shrink-0" />
                    <span>
                      {new Date(inv.scheduled_at).toLocaleDateString()} at{' '}
                      {new Date(inv.scheduled_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                  </div>

                  <div className="flex items-center gap-2">
                    <User className="w-4 h-4 text-slate-400 flex-shrink-0" />
                    <span>Interviewer: {inv.interviewer_name}</span>
                  </div>

                  {inv.meeting_link_or_venue && (
                    <div className="flex items-center gap-2 truncate">
                      <Video className="w-4 h-4 text-slate-400 flex-shrink-0" />
                      <a
                        href={inv.meeting_link_or_venue}
                        target="_blank"
                        rel="noreferrer"
                        className="text-brand-600 hover:underline truncate font-semibold"
                      >
                        {inv.meeting_link_or_venue}
                      </a>
                    </div>
                  )}
                </div>

                {/* Feedback Snapshot if available */}
                {inv.feedback ? (
                  <div className="p-3 bg-emerald-50/60 border border-emerald-200/60 rounded-xl mb-4 text-xs">
                    <div className="flex items-center justify-between mb-1">
                      <span className="font-bold text-emerald-900 flex items-center gap-1">
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" /> Recommendation:
                      </span>
                      <span className="font-black text-emerald-800 uppercase text-[11px]">
                        {inv.feedback.recommendation}
                      </span>
                    </div>
                    <div className="flex items-center gap-4 text-slate-600 text-[11px] my-1">
                      <span>Tech: <strong>{inv.feedback.technical_rating}/5</strong></span>
                      <span>Comm: <strong>{inv.feedback.communication_rating}/5</strong></span>
                      <span>Overall: <strong>{inv.feedback.overall_rating}/5</strong></span>
                    </div>
                    {inv.feedback.comments && (
                      <p className="text-slate-600 italic mt-1 line-clamp-2">"{inv.feedback.comments}"</p>
                    )}
                  </div>
                ) : null}
              </div>

              {/* Actions */}
              <div className="flex items-center justify-between pt-3 border-t border-slate-100">
                <button
                  onClick={() => handleOpenFeedback(inv)}
                  className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-100 hover:bg-brand-50 hover:text-brand-600 text-slate-700 text-xs font-bold rounded-xl transition"
                >
                  <Star className="w-3.5 h-3.5 text-amber-500" />
                  <span>{inv.feedback ? 'Update Evaluation' : 'Submit Feedback & Rating'}</span>
                </button>

                {isAdmin && (
                  <button
                    onClick={() => handleDelete(inv.id)}
                    className="p-1.5 text-slate-400 hover:text-rose-600 rounded-lg transition"
                    title="Delete"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Schedule Interview Modal */}
      <Modal
        isOpen={isScheduleOpen}
        onClose={() => setIsScheduleOpen(false)}
        title="Schedule Interview Round"
      >
        <form onSubmit={handleScheduleSubmit} className="space-y-4 text-xs">
          <div>
            <label className="block font-bold text-slate-700 mb-1">Application / Candidate *</label>
            <select
              required
              value={scheduleData.application_id}
              onChange={(e) => setScheduleData({ ...scheduleData, application_id: e.target.value })}
              className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none"
            >
              <option value="">Select Candidate Application</option>
              {applications.map((a) => (
                <option key={a.id} value={a.id}>
                  {a.candidate_name} → {a.job_title} ({a.company_name})
                </option>
              ))}
            </select>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block font-bold text-slate-700 mb-1">Round Name *</label>
              <input
                type="text"
                required
                value={scheduleData.interview_round}
                onChange={(e) => setScheduleData({ ...scheduleData, interview_round: e.target.value })}
                placeholder="e.g. Technical Round 1"
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none"
              />
            </div>
            <div>
              <label className="block font-bold text-slate-700 mb-1">Date & Time *</label>
              <input
                type="datetime-local"
                required
                value={scheduleData.scheduled_at}
                onChange={(e) => setScheduleData({ ...scheduleData, scheduled_at: e.target.value })}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block font-bold text-slate-700 mb-1">Interviewer Name *</label>
              <input
                type="text"
                required
                value={scheduleData.interviewer_name}
                onChange={(e) => setScheduleData({ ...scheduleData, interviewer_name: e.target.value })}
                placeholder="e.g. Lead Engineer"
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none"
              />
            </div>
            <div>
              <label className="block font-bold text-slate-700 mb-1">Interviewer Email</label>
              <input
                type="email"
                value={scheduleData.interviewer_email}
                onChange={(e) => setScheduleData({ ...scheduleData, interviewer_email: e.target.value })}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none"
              />
            </div>
          </div>

          <div>
            <label className="block font-bold text-slate-700 mb-1">Video Meeting Link / Venue</label>
            <input
              type="text"
              value={scheduleData.meeting_link_or_venue}
              onChange={(e) => setScheduleData({ ...scheduleData, meeting_link_or_venue: e.target.value })}
              placeholder="https://meet.google.com/xyz-link"
              className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none"
            />
          </div>

          <div className="flex justify-end gap-2 pt-4 border-t border-slate-100">
            <button
              type="button"
              onClick={() => setIsScheduleOpen(false)}
              className="px-4 py-2 bg-slate-100 text-slate-700 rounded-xl font-bold hover:bg-slate-200 transition"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-5 py-2 bg-brand-600 text-white rounded-xl font-bold hover:bg-brand-700 transition"
            >
              Confirm Schedule
            </button>
          </div>
        </form>
      </Modal>

      {/* Evaluation Feedback Modal */}
      <Modal
        isOpen={isFeedbackOpen}
        onClose={() => setIsFeedbackOpen(false)}
        title={`Evaluation Feedback: ${selectedInterview?.candidate_name}`}
      >
        <form onSubmit={handleFeedbackSubmit} className="space-y-4 text-xs">
          <div className="grid grid-cols-3 gap-3">
            <div>
              <label className="block font-bold text-slate-700 mb-1">Technical (1-5)</label>
              <select
                value={feedbackData.technical_rating}
                onChange={(e) => setFeedbackData({ ...feedbackData, technical_rating: parseInt(e.target.value) })}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none"
              >
                {[5, 4, 3, 2, 1].map((r) => (
                  <option key={r} value={r}>
                    {r} ★ {r === 5 ? '(Exceptional)' : r === 4 ? '(Good)' : r === 3 ? '(Average)' : '(Poor)'}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block font-bold text-slate-700 mb-1">Communication (1-5)</label>
              <select
                value={feedbackData.communication_rating}
                onChange={(e) => setFeedbackData({ ...feedbackData, communication_rating: parseInt(e.target.value) })}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none"
              >
                {[5, 4, 3, 2, 1].map((r) => (
                  <option key={r} value={r}>
                    {r} ★
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block font-bold text-slate-700 mb-1">Overall (1-5)</label>
              <select
                value={feedbackData.overall_rating}
                onChange={(e) => setFeedbackData({ ...feedbackData, overall_rating: parseInt(e.target.value) })}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none"
              >
                {[5, 4, 3, 2, 1].map((r) => (
                  <option key={r} value={r}>
                    {r} ★
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div>
            <label className="block font-bold text-slate-700 mb-1">Hiring Recommendation *</label>
            <select
              value={feedbackData.recommendation}
              onChange={(e) => setFeedbackData({ ...feedbackData, recommendation: e.target.value })}
              className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none font-bold"
            >
              <option value="STRONG_HIRE">STRONG HIRE (Candidate exceeds all standards)</option>
              <option value="HIRE">HIRE (Meets criteria)</option>
              <option value="HOLD">HOLD (Backup / Consider for other team)</option>
              <option value="NO_HIRE">NO HIRE (Does not meet minimum requirements)</option>
            </select>
          </div>

          <div>
            <label className="block font-bold text-slate-700 mb-1">Interviewer Notes & Evaluation Comments</label>
            <textarea
              rows="4"
              value={feedbackData.comments}
              onChange={(e) => setFeedbackData({ ...feedbackData, comments: e.target.value })}
              placeholder="Elaborate on candidate strengths, problem-solving ability, and architecture knowledge..."
              className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none"
            />
          </div>

          <div className="flex justify-end gap-2 pt-4 border-t border-slate-100">
            <button
              type="button"
              onClick={() => setIsFeedbackOpen(false)}
              className="px-4 py-2 bg-slate-100 text-slate-700 rounded-xl font-bold hover:bg-slate-200 transition"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-5 py-2 bg-brand-600 text-white rounded-xl font-bold hover:bg-brand-700 transition"
            >
              Save Feedback & Mark Completed
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
