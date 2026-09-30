import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import { useToast } from '../../context/ToastContext';
import StatusBadge from '../../components/common/StatusBadge';
import Modal from '../../components/common/Modal';
import {
  Users,
  Search,
  Plus,
  Filter,
  MapPin,
  Briefcase,
  GraduationCap,
  Mail,
  Phone,
  Edit2,
  Trash2,
  Tag,
  Sparkles,
} from 'lucide-react';

export default function Candidates() {
  const { isAdmin } = useAuth();
  const { addToast } = useToast();
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [selectedSkill, setSelectedSkill] = useState('');
  const [selectedStatus, setSelectedStatus] = useState('');
  const [skillsCatalog, setSkillsCatalog] = useState([]);

  // Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingCandidate, setEditingCandidate] = useState(null);
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    location: '',
    experience_years: 0,
    highest_qualification: '',
    current_company: '',
    current_ctc: '',
    expected_ctc: '',
    status: 'AVAILABLE',
    skills: [],
  });
  const [skillInput, setSkillInput] = useState('');

  const fetchCandidates = async () => {
    setLoading(true);
    try {
      const params = {};
      if (search) params.search = search;
      if (selectedSkill) params.skill = selectedSkill;
      if (selectedStatus) params.status = selectedStatus;

      const res = await api.get('/candidates', { params });
      setCandidates(res.data.data.items || []);
    } catch (err) {
      addToast('Failed to load candidates', 'error');
    } finally {
      setLoading(false);
    }
  };

  const fetchSkills = async () => {
    try {
      const res = await api.get('/candidates/skills');
      setSkillsCatalog(res.data.data || []);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchCandidates();
  }, [search, selectedSkill, selectedStatus]);

  useEffect(() => {
    fetchSkills();
  }, []);

  const handleOpenAddModal = () => {
    setEditingCandidate(null);
    setFormData({
      first_name: '',
      last_name: '',
      email: '',
      phone: '',
      location: '',
      experience_years: 0,
      highest_qualification: '',
      current_company: '',
      current_ctc: '',
      expected_ctc: '',
      status: 'AVAILABLE',
      skills: [],
    });
    setIsModalOpen(true);
  };

  const handleOpenEditModal = (c) => {
    setEditingCandidate(c);
    setFormData({
      first_name: c.first_name,
      last_name: c.last_name,
      email: c.email,
      phone: c.phone,
      location: c.location,
      experience_years: c.experience_years,
      highest_qualification: c.highest_qualification,
      current_company: c.current_company || '',
      current_ctc: c.current_ctc || '',
      expected_ctc: c.expected_ctc || '',
      status: c.status,
      skills: c.skills.map((s) => ({ skill_name: s.skill_name, proficiency: s.proficiency })),
    });
    setIsModalOpen(true);
  };

  const handleAddSkillTag = (skillName) => {
    if (!skillName.trim()) return;
    if (formData.skills.some((s) => s.skill_name.toLowerCase() === skillName.toLowerCase())) return;
    setFormData((prev) => ({
      ...prev,
      skills: [...prev.skills, { skill_name: skillName.trim(), proficiency: 'INTERMEDIATE' }],
    }));
    setSkillInput('');
  };

  const handleRemoveSkillTag = (index) => {
    setFormData((prev) => ({
      ...prev,
      skills: prev.skills.filter((_, i) => i !== index),
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingCandidate) {
        await api.put(`/candidates/${editingCandidate.id}`, formData);
        addToast('Candidate profile updated successfully', 'success');
      } else {
        await api.post('/candidates', formData);
        addToast('Candidate registered successfully', 'success');
      }
      setIsModalOpen(false);
      fetchCandidates();
      fetchSkills();
    } catch (err) {
      addToast(err.response?.data?.message || 'Failed to save candidate', 'error');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this candidate?')) return;
    try {
      await api.delete(`/candidates/${id}`);
      addToast('Candidate removed', 'success');
      fetchCandidates();
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
            <Users className="w-7 h-7 text-brand-600" /> Candidate Talent Pool
          </h2>
          <p className="text-sm text-slate-500 mt-0.5">
            Discover, screen, and manage candidates with verified skill proficiencies.
          </p>
        </div>

        <button
          onClick={handleOpenAddModal}
          className="flex items-center gap-2 px-4 py-2.5 bg-brand-600 hover:bg-brand-700 text-white text-xs font-bold rounded-xl shadow-md shadow-brand-500/20 transition"
        >
          <Plus className="w-4 h-4" /> Add Candidate
        </button>
      </div>

      {/* Filters Bar */}
      <div className="bg-white p-4 rounded-2xl border border-slate-200/80 shadow-sm grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div className="relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 transform -translate-y-1/2" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search by name, email, qualification..."
            className="w-full pl-10 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs focus:outline-none focus:ring-2 focus:ring-brand-500/20"
          />
        </div>

        <select
          value={selectedSkill}
          onChange={(e) => setSelectedSkill(e.target.value)}
          className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs focus:outline-none"
        >
          <option value="">All Skills Taxonomy</option>
          {skillsCatalog.map((s) => (
            <option key={s.id} value={s.name}>
              {s.name} ({s.category})
            </option>
          ))}
        </select>

        <select
          value={selectedStatus}
          onChange={(e) => setSelectedStatus(e.target.value)}
          className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs focus:outline-none"
        >
          <option value="">All Availability Statuses</option>
          <option value="AVAILABLE">Available</option>
          <option value="INTERVIEWING">Interviewing</option>
          <option value="PLACED">Placed</option>
          <option value="INACTIVE">Inactive</option>
        </select>
      </div>

      {/* Candidates Table / Grid */}
      {loading ? (
        <div className="flex items-center justify-center py-20">
          <div className="w-8 h-8 border-4 border-brand-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : candidates.length === 0 ? (
        <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center">
          <p className="text-slate-500 text-sm">No candidates found matching criteria.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {candidates.map((cand) => (
            <div
              key={cand.id}
              className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-sm hover:shadow-md transition flex flex-col justify-between"
            >
              <div>
                <div className="flex items-start justify-between gap-3 mb-3">
                  <div>
                    <h3 className="text-base font-bold text-slate-900">{cand.full_name}</h3>
                    <p className="text-xs text-slate-500 flex items-center gap-1.5 mt-0.5">
                      <GraduationCap className="w-3.5 h-3.5 text-slate-400" />
                      {cand.highest_qualification}
                    </p>
                  </div>
                  <StatusBadge status={cand.status} />
                </div>

                <div className="grid grid-cols-2 gap-2 text-xs text-slate-600 mb-4 bg-slate-50/70 p-3 rounded-xl border border-slate-100">
                  <span className="flex items-center gap-1.5">
                    <MapPin className="w-3.5 h-3.5 text-slate-400" /> {cand.location}
                  </span>
                  <span className="flex items-center gap-1.5 font-semibold text-slate-800">
                    <Briefcase className="w-3.5 h-3.5 text-slate-400" /> {cand.experience_years} yrs exp
                  </span>
                  <span className="flex items-center gap-1.5 truncate">
                    <Mail className="w-3.5 h-3.5 text-slate-400" /> {cand.email}
                  </span>
                  <span className="flex items-center gap-1.5">
                    <Phone className="w-3.5 h-3.5 text-slate-400" /> {cand.phone}
                  </span>
                </div>

                {/* Skills Tags */}
                <div className="flex flex-wrap gap-1.5 mb-4">
                  {cand.skills && cand.skills.length > 0 ? (
                    cand.skills.map((s, idx) => (
                      <span
                        key={idx}
                        className="px-2 py-0.5 bg-indigo-50 text-indigo-700 border border-indigo-200/60 rounded-lg text-[11px] font-semibold"
                      >
                        {s.skill_name}
                      </span>
                    ))
                  ) : (
                    <span className="text-xs text-slate-400">No skills tagged</span>
                  )}
                </div>
              </div>

              {/* Actions */}
              <div className="flex items-center justify-between pt-3 border-t border-slate-100 text-xs">
                <span className="text-slate-400 text-[11px]">
                  ID: #{cand.id} • Registered {new Date(cand.created_at).toLocaleDateString()}
                </span>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => handleOpenEditModal(cand)}
                    className="p-1.5 text-slate-600 hover:text-brand-600 hover:bg-slate-100 rounded-lg transition"
                    title="Edit"
                  >
                    <Edit2 className="w-4 h-4" />
                  </button>
                  {isAdmin && (
                    <button
                      onClick={() => handleDelete(cand.id)}
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

      {/* Add / Edit Candidate Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title={editingCandidate ? 'Edit Candidate Profile' : 'Register New Candidate'}
      >
        <form onSubmit={handleSubmit} className="space-y-4 text-xs">
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block font-bold text-slate-700 mb-1">First Name *</label>
              <input
                type="text"
                required
                value={formData.first_name}
                onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500/20"
              />
            </div>
            <div>
              <label className="block font-bold text-slate-700 mb-1">Last Name *</label>
              <input
                type="text"
                required
                value={formData.last_name}
                onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500/20"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block font-bold text-slate-700 mb-1">Email Address *</label>
              <input
                type="email"
                required
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500/20"
              />
            </div>
            <div>
              <label className="block font-bold text-slate-700 mb-1">Phone Number *</label>
              <input
                type="text"
                required
                value={formData.phone}
                onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500/20"
              />
            </div>
          </div>

          <div className="grid grid-cols-3 gap-3">
            <div>
              <label className="block font-bold text-slate-700 mb-1">Location *</label>
              <input
                type="text"
                required
                value={formData.location}
                onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                placeholder="e.g. San Francisco, CA"
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500/20"
              />
            </div>
            <div>
              <label className="block font-bold text-slate-700 mb-1">Years of Experience</label>
              <input
                type="number"
                step="0.5"
                min="0"
                value={formData.experience_years}
                onChange={(e) => setFormData({ ...formData, experience_years: parseFloat(e.target.value) || 0 })}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500/20"
              />
            </div>
            <div>
              <label className="block font-bold text-slate-700 mb-1">Status</label>
              <select
                value={formData.status}
                onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none"
              >
                <option value="AVAILABLE">Available</option>
                <option value="INTERVIEWING">Interviewing</option>
                <option value="PLACED">Placed</option>
                <option value="INACTIVE">Inactive</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block font-bold text-slate-700 mb-1">Highest Qualification *</label>
            <input
              type="text"
              required
              value={formData.highest_qualification}
              onChange={(e) => setFormData({ ...formData, highest_qualification: e.target.value })}
              placeholder="e.g. B.Tech Computer Science"
              className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500/20"
            />
          </div>

          {/* Skill Tagging System */}
          <div>
            <label className="block font-bold text-slate-700 mb-1">Technical Skills</label>
            <div className="flex gap-2 mb-2">
              <input
                type="text"
                value={skillInput}
                onChange={(e) => setSkillInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    e.preventDefault();
                    handleAddSkillTag(skillInput);
                  }
                }}
                placeholder="Type skill & press enter (e.g. Python, React, SQL)..."
                className="flex-1 px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500/20"
              />
              <button
                type="button"
                onClick={() => handleAddSkillTag(skillInput)}
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
                    onClick={() => handleRemoveSkillTag(idx)}
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
              {editingCandidate ? 'Save Changes' : 'Register Candidate'}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
