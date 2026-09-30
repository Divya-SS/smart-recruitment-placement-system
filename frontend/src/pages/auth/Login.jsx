import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { useToast } from '../../context/ToastContext';
import { LogIn, Shield, Briefcase, Lock, Mail, Sparkles } from 'lucide-react';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const { addToast } = useToast();
  const navigate = useNavigate();

  const handleLoginWithCredentials = async (emailToUse, passwordToUse) => {
    setLoading(true);
    try {
      await login(emailToUse.trim().toLowerCase(), passwordToUse);
      addToast('Signed in successfully', 'success');
      navigate('/dashboard');
    } catch (err) {
      addToast(err.response?.data?.message || 'Invalid email or password', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!email.trim() || !password) {
      addToast('Please enter both email and password', 'error');
      return;
    }
    await handleLoginWithCredentials(email, password);
  };

  const handleQuickLogin = (demoEmail, demoPass) => {
    setEmail(demoEmail);
    setPassword(demoPass);
    handleLoginWithCredentials(demoEmail, demoPass);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 p-4 relative overflow-hidden">
      {/* Decorative Glows */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-brand-500/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />

      <div className="w-full max-w-md bg-white rounded-3xl shadow-2xl p-8 border border-slate-100 relative z-10">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-gradient-to-tr from-brand-600 to-indigo-600 text-white shadow-xl shadow-brand-500/30 font-black text-2xl mb-4">
            SR
          </div>
          <h2 className="text-2xl font-black text-slate-900 tracking-tight">Welcome Back</h2>
          <p className="text-sm text-slate-500 mt-1">Smart Recruitment & Placement System</p>
        </div>

        {/* Quick Demo Credentials */}
        <div className="mb-6 bg-slate-50 border border-slate-200/80 rounded-2xl p-4">
          <div className="flex items-center gap-1.5 text-xs font-bold text-slate-600 uppercase tracking-wide mb-2.5">
            <Sparkles className="w-3.5 h-3.5 text-amber-500" />
            <span>1-Click Instant Login</span>
          </div>
          <div className="grid grid-cols-2 gap-2">
            <button
              type="button"
              onClick={() => handleQuickLogin('admin@recruitment.com', 'Admin@123')}
              className="flex flex-col items-center justify-center p-2.5 bg-white hover:bg-slate-100 border border-slate-200 rounded-xl text-xs font-semibold text-slate-800 shadow-sm transition group"
            >
              <div className="flex items-center gap-1.5 text-indigo-600 font-bold mb-0.5">
                <Shield className="w-3.5 h-3.5" />
                <span>Admin</span>
              </div>
              <span className="text-[10px] text-slate-400 font-normal">admin@recruitment.com</span>
            </button>
            <button
              type="button"
              onClick={() => handleQuickLogin('recruiter@recruitment.com', 'Recruiter@123')}
              className="flex flex-col items-center justify-center p-2.5 bg-white hover:bg-slate-100 border border-slate-200 rounded-xl text-xs font-semibold text-slate-800 shadow-sm transition group"
            >
              <div className="flex items-center gap-1.5 text-teal-600 font-bold mb-0.5">
                <Briefcase className="w-3.5 h-3.5" />
                <span>Recruiter</span>
              </div>
              <span className="text-[10px] text-slate-400 font-normal">recruiter@recruitment.com</span>
            </button>
          </div>
          <p className="text-[11px] text-slate-400 text-center mt-2.5">
            Password: <code className="bg-slate-200 px-1 py-0.5 rounded text-slate-700 font-mono">Admin@123</code> / <code className="bg-slate-200 px-1 py-0.5 rounded text-slate-700 font-mono">Recruiter@123</code>
          </p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
              Email Address
            </label>
            <div className="relative">
              <Mail className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 transform -translate-y-1/2" />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="e.g. admin@recruitment.com"
                className="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500 transition"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
              Password
            </label>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 transform -translate-y-1/2" />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500 transition"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full mt-2 py-3 bg-gradient-to-r from-brand-600 to-indigo-600 hover:from-brand-700 hover:to-indigo-700 text-white font-bold rounded-xl shadow-lg shadow-brand-500/25 transition duration-200 flex items-center justify-center gap-2 disabled:opacity-50"
          >
            {loading ? (
              <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
            ) : (
              <>
                <LogIn className="w-4 h-4" />
                <span>Sign In to Dashboard</span>
              </>
            )}
          </button>
        </form>
      </div>
    </div>
  );
}
