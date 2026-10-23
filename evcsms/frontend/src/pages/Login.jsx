import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Zap, Mail, Lock, ArrowRight, Shield, UserCheck, AlertCircle } from 'lucide-react';
import { TeslaBackground } from '../components/TeslaBackground';

export const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const from = location.state?.from?.pathname || '/dashboard';

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSubmitting(true);
    try {
      const user = await login(email, password);
      if (user.role === 'ADMIN') {
        navigate('/admin');
      } else {
        navigate(from);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Invalid email or password. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  const fillDemoOwner = () => {
    setEmail('owner@evcsms.com');
    setPassword('ownerpassword123');
    setError('');
  };

  const fillDemoAdmin = () => {
    setEmail('admin@evcsms.com');
    setPassword('adminpassword123');
    setError('');
  };

  return (
    <div className="min-h-screen bg-navy-950 flex flex-col justify-center py-12 sm:px-6 lg:px-8 relative overflow-hidden">
      <TeslaBackground />
      {/* Background ambient decorative glows */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none"></div>
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none"></div>

      <div className="sm:mx-auto sm:w-full sm:max-w-md relative z-10 text-center">
        <div className="flex justify-center mb-4">
          <img
            src="/logo-dark.svg"
            alt="EVCSMS Logo"
            className="h-14 w-auto object-contain drop-shadow-[0_4px_20px_rgba(16,185,129,0.35)]"
          />
        </div>
        <h2 className="text-center text-2xl font-extrabold text-white tracking-tight">
          Sign In to Your Account
        </h2>
        <p className="mt-1 text-center text-xs text-slate-400">
          Smart Grid Electric Vehicle Charging Network
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md relative z-10 px-4 sm:px-0">
        <div className="glass-panel py-8 px-6 sm:px-10 rounded-3xl shadow-2xl border border-navy-700">
          {error && (
            <div className="mb-6 p-3.5 rounded-xl bg-red-500/10 border border-red-500/30 flex items-start gap-3">
              <AlertCircle className="w-5 h-5 text-red-400 shrink-0 mt-0.5" />
              <p className="text-sm text-red-300">{error}</p>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                Email Address
              </label>
              <div className="relative rounded-xl shadow-sm">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                  <Mail className="h-4 w-4 text-slate-400" />
                </div>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="name@example.com"
                  className="block w-full pl-10 pr-4 py-2.5 bg-navy-900 border border-navy-700 rounded-xl text-white placeholder-slate-500 text-sm focus:outline-none focus:ring-2 focus:ring-evgreen-500 focus:border-transparent transition-all"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                Password
              </label>
              <div className="relative rounded-xl shadow-sm">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                  <Lock className="h-4 w-4 text-slate-400" />
                </div>
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="block w-full pl-10 pr-4 py-2.5 bg-navy-900 border border-navy-700 rounded-xl text-white placeholder-slate-500 text-sm focus:outline-none focus:ring-2 focus:ring-evgreen-500 focus:border-transparent transition-all"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={submitting}
              className="w-full py-3 px-4 rounded-xl bg-gradient-to-r from-evgreen-500 to-emerald-600 hover:from-evgreen-400 hover:to-emerald-500 text-navy-950 font-bold text-sm shadow-glow-green flex items-center justify-center gap-2 transition-all transform active:scale-95 disabled:opacity-50"
            >
              {submitting ? 'Authenticating...' : 'Sign In'}
              <ArrowRight className="w-4 h-4" />
            </button>
          </form>

          {/* Quick Demo Autofill Helpers */}
          <div className="mt-6 pt-6 border-t border-navy-800">
            <span className="block text-center text-xs text-slate-400 font-medium mb-3">
              Quick 1-Click Demo Logins:
            </span>
            <div className="grid grid-cols-2 gap-2.5">
              <button
                type="button"
                onClick={fillDemoOwner}
                className="p-2.5 bg-navy-800/80 hover:bg-navy-800 border border-navy-700 rounded-xl text-left transition-colors flex items-center gap-2"
              >
                <div className="w-7 h-7 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center shrink-0">
                  <UserCheck className="w-4 h-4" />
                </div>
                <div>
                  <span className="block text-xs font-semibold text-white">EV Owner</span>
                  <span className="block text-[10px] text-slate-400">Rahul Sharma</span>
                </div>
              </button>

              <button
                type="button"
                onClick={fillDemoAdmin}
                className="p-2.5 bg-navy-800/80 hover:bg-navy-800 border border-navy-700 rounded-xl text-left transition-colors flex items-center gap-2"
              >
                <div className="w-7 h-7 rounded-lg bg-amber-500/20 text-amber-400 flex items-center justify-center shrink-0">
                  <Shield className="w-4 h-4" />
                </div>
                <div>
                  <span className="block text-xs font-semibold text-white">Station Admin</span>
                  <span className="block text-[10px] text-slate-400">Priya Deshmukh</span>
                </div>
              </button>
            </div>
          </div>

          <div className="mt-6 text-center">
            <p className="text-xs text-slate-400">
              New EV Owner?{' '}
              <Link to="/register" className="text-evgreen-400 hover:text-evgreen-300 font-semibold underline underline-offset-4">
                Create an account
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
