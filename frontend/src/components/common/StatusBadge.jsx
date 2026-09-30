import React from 'react';

const STATUS_CONFIGS = {
  // Application Statuses
  APPLIED: { bg: 'bg-blue-50', text: 'text-blue-700', border: 'border-blue-200', label: 'Applied' },
  SHORTLISTED: { bg: 'bg-purple-50', text: 'text-purple-700', border: 'border-purple-200', label: 'Shortlisted' },
  INTERVIEW_SCHEDULED: { bg: 'bg-amber-50', text: 'text-amber-700', border: 'border-amber-200', label: 'Interview Scheduled' },
  SELECTED: { bg: 'bg-emerald-50', text: 'text-emerald-700', border: 'border-emerald-200', label: 'Selected' },
  REJECTED: { bg: 'bg-rose-50', text: 'text-rose-700', border: 'border-rose-200', label: 'Rejected' },
  JOINED: { bg: 'bg-teal-50', text: 'text-teal-700', border: 'border-teal-200', label: 'Joined / Placed' },

  // Candidate Statuses
  AVAILABLE: { bg: 'bg-emerald-50', text: 'text-emerald-700', border: 'border-emerald-200', label: 'Available' },
  INTERVIEWING: { bg: 'bg-amber-50', text: 'text-amber-700', border: 'border-amber-200', label: 'Interviewing' },
  PLACED: { bg: 'bg-teal-50', text: 'text-teal-700', border: 'border-teal-200', label: 'Placed' },
  INACTIVE: { bg: 'bg-slate-100', text: 'text-slate-600', border: 'border-slate-200', label: 'Inactive' },

  // Job Statuses
  OPEN: { bg: 'bg-emerald-50', text: 'text-emerald-700', border: 'border-emerald-200', label: 'Active / Open' },
  ON_HOLD: { bg: 'bg-amber-50', text: 'text-amber-700', border: 'border-amber-200', label: 'On Hold' },
  CLOSED: { bg: 'bg-slate-100', text: 'text-slate-600', border: 'border-slate-200', label: 'Closed' },

  // Interview Statuses
  SCHEDULED: { bg: 'bg-blue-50', text: 'text-blue-700', border: 'border-blue-200', label: 'Scheduled' },
  COMPLETED: { bg: 'bg-emerald-50', text: 'text-emerald-700', border: 'border-emerald-200', label: 'Completed' },
  CANCELLED: { bg: 'bg-rose-50', text: 'text-rose-700', border: 'border-rose-200', label: 'Cancelled' },
  RESCHEDULED: { bg: 'bg-amber-50', text: 'text-amber-700', border: 'border-amber-200', label: 'Rescheduled' },

  // General Company Statuses
  ACTIVE: { bg: 'bg-emerald-50', text: 'text-emerald-700', border: 'border-emerald-200', label: 'Active' },
};

export default function StatusBadge({ status, className = '' }) {
  if (!status) return null;
  const config = STATUS_CONFIGS[status.toUpperCase()] || {
    bg: 'bg-slate-100',
    text: 'text-slate-700',
    border: 'border-slate-200',
    label: status,
  };

  return (
    <span
      className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold border ${config.bg} ${config.text} ${config.border} ${className}`}
    >
      <span className="w-1.5 h-1.5 rounded-full mr-1.5 bg-current opacity-80" />
      {config.label}
    </span>
  );
}
