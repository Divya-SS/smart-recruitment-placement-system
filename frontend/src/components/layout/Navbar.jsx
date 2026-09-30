import React from 'react';
import { useAuth } from '../../context/AuthContext';
import { LogOut, User, ShieldCheck, Briefcase } from 'lucide-react';

export default function Navbar() {
  const { user, logout, isAdmin } = useAuth();

  return (
    <header className="h-16 bg-white border-b border-slate-200/80 px-6 flex items-center justify-between sticky top-0 z-30 shadow-sm">
      <div className="flex items-center gap-3">
        <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-brand-600 to-indigo-600 flex items-center justify-center shadow-md shadow-brand-500/20 text-white font-black text-lg">
          SR
        </div>
        <div>
          <h1 className="text-base font-bold text-slate-800 leading-tight">Smart Recruitment</h1>
          <p className="text-xs text-slate-400 font-medium hidden sm:block">Placement & Talent Acquisition System</p>
        </div>
      </div>

      <div className="flex items-center gap-4">
        <div className="flex items-center gap-3 pr-2 sm:border-r sm:border-slate-200">
          <div className="w-9 h-9 rounded-full bg-slate-100 flex items-center justify-center text-slate-600 border border-slate-200 font-semibold text-sm">
            {user?.full_name ? user.full_name.charAt(0) : 'U'}
          </div>
          <div className="hidden sm:block text-left">
            <p className="text-xs font-bold text-slate-800 leading-none">{user?.full_name || 'User'}</p>
            <div className="flex items-center gap-1 mt-0.5">
              {isAdmin ? (
                <span className="inline-flex items-center text-[10px] font-bold text-indigo-600 uppercase tracking-wide">
                  <ShieldCheck className="w-3 h-3 mr-0.5" /> Administrator
                </span>
              ) : (
                <span className="inline-flex items-center text-[10px] font-bold text-teal-600 uppercase tracking-wide">
                  <Briefcase className="w-3 h-3 mr-0.5" /> Recruiter
                </span>
              )}
            </div>
          </div>
        </div>

        <button
          onClick={logout}
          title="Sign Out"
          className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-rose-600 hover:text-rose-700 hover:bg-rose-50 rounded-lg transition"
        >
          <LogOut className="w-4 h-4" />
          <span className="hidden sm:inline">Logout</span>
        </button>
      </div>
    </header>
  );
}
