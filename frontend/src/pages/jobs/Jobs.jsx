import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import { useToast } from '../../context/ToastContext';
import StatusBadge from '../../components/common/StatusBadge';
import Modal from '../../components/common/Modal';
import {
  Briefcase,
  Search,
  Plus,
  Building2,
  MapPin,
  Clock,
  Sparkles,
  Edit2,
  Trash2,
  DollarSign,
  Users,
} from 'lucide-react';

export default function Jobs() {
  const { isAdmin } = useAuth();
  const { addToast } = useToast();
  const [jobs, setJobs] = useState([]);
  const [companies, setCompanies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('');

  // Modal
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingJob, setEditingJob] = useState(null);
  const [formData, setFormData] = useState({
    company_id: '',
    title: '',
    description: '',
    min_experience_years: 0,
    max_experience_years: '',
    qualification_required: '',
    location: '',
    job_type: 'FULL_TIME',
    min_salary: '',
    max_salary: '',
    openings_count: 1,
    status: 'OPEN',
    skills: [],
  });
  const [skillInput, setSkillInput] = useState('');

  const fetchJobs = async () => {
    setLoading(true);
    try {
      const params = {};
      if (search) params.search = search;
      if (statusFilter) params.status = statusFilter;
      const res = await api.get('/jobs', { params });
      setJobs(res.data.data.items || []);
    } catch (err) {
      addToast('Failed to load jobs', 'error');
    } finally {
      setLoading(false);
    }
  };

  const fetchCompanies = async () => {
    try {
      const res = await api.get('/companies');
      setCompanies(res.data.data.items || []);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchJobs();
  }, [search, statusFilter]);

  useEffect(() => {
    fetchCompanies();
  }, []);

  const handleOpenAdd = () => {
    setEditingJob(null);
    setFormData({
      company_id: companies.length > 0 ? companies[0].id : '',
      title: '',
      description: '',
      min_experience_years: 0,
      max_experience_years: '',
      qualification_required: '',
      location: '',
      job_type: 'FULL_TIME',
      min_salary: '',
      max_salary: '',
      openings_count: 1,
      status: 'OPEN',
      skills: [],
    });
    setIsModalOpen(true);
  };

  const handleOpenEdit = (job) => {
    setEditingJob(job);
    setFormData({
      company_id: job.company_id,
      title: job.title,
      description: job.description || '',
      min_experience_years: job.min_experience_years,
      max_experience_years: job.max_experience_years || '',
      qualification_required: job.qualification_required || '',
      location: job.location,
      job_type: job.job_type,
      min_salary: job.min_salary || '',
      max_salary: job.max_salary || '',
      openings_count: job.openings_count,
      status: job.status,
      skills: job.skills.map((s) => ({ skill_name: s.skill_name, is_mandatory: s.is_mandatory })),
    });
    setIsModalOpen(true);
  };

  const handleAddSkill = (skillName) => {
    if (!skillName.trim()) return;
    if (formData.skills.some((s) => s.skill_name.toLowerCase() === skillName.toLowerCase())) return;
    setFormData((prev) => ({
      ...prev,
      skills: [...prev.skills, { skill_name: skillName.trim(), is_mandatory: true }],
    }));
    setSkillInput('');
  };

  const handleRemoveSkill = (index) => {
    setFormData((prev) => ({
      ...prev,
      skills: prev.skills.filter((_, i) => i !== index),
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingJob) {
        await api.put(`/jobs/${editingJob.id}`, formData);
        addToast('Job requisition updated successfully', 'success');
      } else {
        await api.post('/jobs', formData);
        addToast('Job requisition published successfully', 'success');
      }
      setIsModalOpen(false);
      fetchJobs();
    } catch (err) {
      addToast(err.response?.data?.message || 'Failed to save job', 'error');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this job posting?')) return;
    try {
      await api.delete(`/jobs/${id}`);
      addToast('Job removed', 'success');
      fetchJobs();
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
            <Briefcase className="w-7 h-7 text-brand-600" /> Active Job Openings
          </h2>
          <p className="text-sm text-slate-500 mt-0.5">
            Manage job descriptions, required skill taxonomy, and candidate matches.
          </p>
        </div>

        <button
          onClick={handleOpenAdd}
          className="flex items-center gap-2 px-4 py-2.5 bg-brand-600 hover:bg-brand-700 text-white text-xs font-bold rounded-xl shadow-md shadow-brand-500/20 transition"
        >
          <Plus className="w-4 h-4" /> Post New Job
        </button>
      </div>

      {/* Filters Bar */}
      <div className="bg-white p-4 rounded-2xl border border-slate-200/80 shadow-sm grid grid-cols-1 sm:grid-cols-2 gap-3 max-w-xl">
        <div className="relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 transform -translate-y-1/2" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search jobs by title, company, location..."
            className="w-full pl-10 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs focus:outline-none focus:ring-2 focus:ring-brand-500/20"
          />
        </div>

        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs focus:outline-none"
        >
          <option value="">All Job Statuses</option>
          <option value="OPEN">Open / Active</option>
          <option value="ON_HOLD">On Hold</option>
          <option value="CLOSED">Closed</option>
        </select>
      </div>

      {/* Jobs Grid */}
      {loading ? (
        <div className="flex items-center justify-center py-20">
          <div className="w-8 h-8 border-4 border-brand-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : jobs.length === 0 ? (
        <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center">
          <p className="text-slate-500 text-sm">No job openings found matching criteria.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {jobs.map((job) => (
            <div
              key={job.id}
              className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-sm hover:shadow-md transition flex flex-col justify-between"
            >
              <div>
                <div className="flex items-start justify-between gap-3 mb-2">
                  <div>
                    <h3 className="text-lg font-bold text-slate-900 leading-snug">{job.title}</h3>
                    <p className="text-xs font-semibold text-brand-600 flex items-center gap-1.5 mt-0.5">
                      <Building2 className="w-3.5 h-3.5" />
                      {job.company_name}
                    </p>
                  </div>
                  <StatusBadge status={job.status} />
                </div>

                <p className="text-xs text-slate-500 line-clamp-2 my-3">{job.description}</p>

                <div className="grid grid-cols-2 gap-2 text-xs text-slate-600 mb-4 bg-slate-50/70 p-3 rounded-xl border border-slate-100">
                  <span className="flex items-center gap-1.5">
                    <MapPin className="w-3.5 h-3.5 text-slate-400" /> {job.location}
                  </span>
                  <span className="flex items-center gap-1.5 font-semibold text-slate-800">
                    <Clock className="w-3.5 h-3.5 text-slate-400" /> Min {job.min_experience_years} yrs exp
                  </span>
                  <span className="flex items-center gap-1.5">
                    <Users className="w-3.5 h-3.5 text-slate-400" /> {job.openings_count} Openings
                  </span>
                  <span className="flex items-center gap-1.5 text-emerald-700 font-semibold">
                    <DollarSign className="w-3.5 h-3.5 text-emerald-500" />{' '}
                    {job.min_salary ? `$${job.min_salary.toLocaleString()} - $${job.max_salary?.toLocaleString()}` : 'Competitive'}
                  </span>
                </div>

                {/* Required Skills */}
                <div className="flex flex-wrap gap-1.5 mb-4">
                  {job.skills && job.skills.length > 0 ? (
                    job.skills.map((s, idx) => (
                      <span
                        key={idx}
                        className="px-2 py-0.5 bg-brand-50 text-brand-700 border border-brand-200/60 rounded-lg text-[11px] font-semibold"
                      >
                        {s.skill_name}
                      </span>
                    ))
                  ) : (
                    <span className="text-xs text-slate-400">No skill requirements specified</span>
                  )}
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex items-center justify-between pt-4 border-t border-slate-100">
                <Link
                  to={`/matching?job_id=${job.id}`}
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white font-bold text-xs rounded-xl shadow-sm transition"
                >
                  <Sparkles className="w-3.5 h-3.5" />
                  <span>Find Best Candidates</span>
                </Link>

                <div className="flex items-center gap-2">
                  <button
                    onClick={() => handleOpenEdit(job)}
                    className="p-1.5 text-slate-600 hover:text-brand-600 hover:bg-slate-100 rounded-lg transition"
                    title="Edit"
                  >
                    <Edit2 className="w-4 h-4" />
                  </button>
                  {isAdmin && (
                    <button
                      onClick={() => handleDelete(job.id)}
                      className="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition"
                      title="Delete"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Add / Edit Job Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title={editingJob ? 'Edit Job Requisition' : 'Create Job Opening'}
      >
        <form onSubmit={handleSubmit} className="space-y-4 text-xs">
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block font-bold text-slate-700 mb-1">Company Partner *</label>
              <select
                required
                value={formData.company_id}
                onChange={(e) => setFormData({ ...formData, company_id: e.target.value })}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none"
              >
                <option value="">Select Company</option>
                {companies.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.name}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="block font-bold text-slate-700 mb-1">Job Title *</label>
              <input
                type="text"
                required
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                placeholder="e.g. Senior Python / Flask Backend Engineer"
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500/20"
              />
            </div>
          </div>

          <div>
            <label className="block font-bold text-slate-700 mb-1">Job Description</label>
            <textarea
              rows="3"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              placeholder="Outline responsibilities and project scope..."
              className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500/20"
            />
          </div>

          <div className="grid grid-cols-3 gap-3">
            <div>
              <label className="block font-bold text-slate-700 mb-1">Location *</label>
              <input
                type="text"
                required
                value={formData.location}
                onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                placeholder="e.g. Remote, or Seattle, WA"
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none"
              />
            </div>
            <div>
              <label className="block font-bold text-slate-700 mb-1">Min Exp (Years)</label>
              <input
                type="number"
                step="0.5"
                min="0"
                value={formData.min_experience_years}
                onChange={(e) => setFormData({ ...formData, min_experience_years: parseFloat(e.target.value) || 0 })}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none"
              />
            </div>
            <div>
              <label className="block font-bold text-slate-700 mb-1">Openings Count</label>
              <input
                type="number"
                min="1"
                value={formData.openings_count}
                onChange={(e) => setFormData({ ...formData, openings_count: parseInt(e.target.value) || 1 })}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block font-bold text-slate-700 mb-1">Min Salary / CTC ($)</label>
              <input
                type="number"
                value={formData.min_salary}
                onChange={(e) => setFormData({ ...formData, min_salary: e.target.value })}
                placeholder="e.g. 100000"
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none"
              />
            </div>
            <div>
              <label className="block font-bold text-slate-700 mb-1">Max Salary / CTC ($)</label>
              <input
                type="number"
                value={formData.max_salary}
                onChange={(e) => setFormData({ ...formData, max_salary: e.target.value })}
                placeholder="e.g. 140000"
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none"
              />
            </div>
          </div>

          {/* Skill Requirements Tagging */}
          <div>
            <label className="block font-bold text-slate-700 mb-1">Required Skills for Matching Engine</label>
            <div className="flex gap-2 mb-2">
              <input
                type="text"
                value={skillInput}
                onChange={(e) => setSkillInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    e.preventDefault();
                    handleAddSkill(skillInput);
                  }
                }}
                placeholder="Type skill & press enter (e.g. Python, SQL, Docker)..."
                className="flex-1 px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500/20"
              />
              <button
                type="button"
                onClick={() => handleAddSkill(skillInput)}
                className="px-4 py-2 bg-slate-800 text-white rounded-xl font-bold"
              >
                Add Skill
              </button>
            </div>

            <div className="flex flex-wrap gap-1.5 p-3 bg-slate-50 rounded-xl border border-slate-200 min-h-[44px]">
              {formData.skills.map((s, idx) => (
                <span
                  key={idx}
                  className="inline-flex items-center gap-1.5 px-2.5 py-1 bg-brand-50 text-brand-700 border border-brand-200 rounded-lg text-xs font-semibold"
                >
                  {s.skill_name}
                  <button
                    type="button"
                    onClick={() => handleRemoveSkill(idx)}
                    className="text-brand-400 hover:text-brand-700"
                  >
                    ×
                  </button>
                </span>
              ))}
            </div>
          </div>

          <div className="flex justify-end gap-2 pt-4 border-t border-slate-100">
            <button
              type="button"
              onClick={() => setIsModalOpen(false)}
              className="px-4 py-2 bg-slate-100 text-slate-700 rounded-xl font-bold hover:bg-slate-200 transition"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-5 py-2 bg-brand-600 text-white rounded-xl font-bold hover:bg-brand-700 transition"
            >
              {editingJob ? 'Save Changes' : 'Publish Job'}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
