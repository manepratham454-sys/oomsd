import React, { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useNotifications } from '../context/NotificationContext';
import {
  Zap,
  MapPin,
  Calendar,
  Activity,
  Car,
  CreditCard,
  ShieldCheck,
  Bell,
  LogOut,
  User as UserIcon,
  Menu,
  X,
  CheckCircle2,
} from 'lucide-react';

export const Navbar = () => {
  const { user, logout, role } = useAuth();
  const { notifications, unreadCount, markAsRead, markAllAsRead } = useNotifications();
  const location = useLocation();
  const navigate = useNavigate();

  const [notifOpen, setNotifOpen] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navLinks = [
    { name: 'Dashboard', path: '/dashboard', icon: Zap },
    { name: 'Stations', path: '/stations', icon: MapPin },
    { name: 'My Bookings', path: '/bookings', icon: Calendar },
    { name: 'Charging', path: '/session/active', icon: Activity },
    { name: 'Vehicles', path: '/vehicles', icon: Car },
    { name: 'Payments', path: '/payments', icon: CreditCard },
  ];

  if (role === 'ADMIN') {
    navLinks.push({ name: 'Admin Hub', path: '/admin', icon: ShieldCheck });
  }

  const isActive = (path) => location.pathname === path;

  return (
    <nav className="glass-nav sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/dashboard" className="flex items-center gap-3 group">
            <img
              src="/logo-dark.svg"
              alt="EVCSMS Logo"
              className="h-10 w-auto object-contain transition-transform duration-300 group-hover:scale-105"
            />
            <span className="hidden lg:inline-block text-[10px] font-bold uppercase px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
              OOSMD
            </span>
          </Link>

          {/* Desktop Nav Links */}
          <div className="hidden md:flex items-center gap-1">
            {navLinks.map((link) => {
              const Icon = link.icon;
              const active = isActive(link.path);
              return (
                <Link
                  key={link.path}
                  to={link.path}
                  className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                    active
                      ? 'bg-navy-800 text-evgreen-400 border border-evgreen-500/30 shadow-sm'
                      : 'text-slate-300 hover:text-white hover:bg-navy-850'
                  }`}
                >
                  <Icon className={`w-4 h-4 ${active ? 'text-evgreen-400' : 'text-slate-400'}`} />
                  {link.name}
                </Link>
              );
            })}
          </div>

          {/* Right Controls: Notifications & User Menu */}
          <div className="hidden md:flex items-center gap-4">
            {/* Notification Dropdown Trigger */}
            <div className="relative">
              <button
                onClick={() => setNotifOpen(!notifOpen)}
                className="relative p-2 rounded-lg text-slate-300 hover:text-white hover:bg-navy-800 transition-colors"
                title="Notifications"
              >
                <Bell className="w-5 h-5" />
                {unreadCount > 0 && (
                  <span className="absolute top-1 right-1 w-4 h-4 bg-emerald-500 text-navy-950 text-[10px] font-bold rounded-full flex items-center justify-center animate-pulse">
                    {unreadCount > 9 ? '9+' : unreadCount}
                  </span>
                )}
              </button>

              {/* Notification Popover */}
              {notifOpen && (
                <div className="absolute right-0 mt-2 w-80 sm:w-96 glass-panel rounded-xl shadow-2xl p-4 border border-navy-700 animate-in fade-in zoom-in-95 duration-150 z-50">
                  <div className="flex items-center justify-between pb-3 border-b border-navy-700">
                    <div className="flex items-center gap-2">
                      <Bell className="w-4 h-4 text-evgreen-400" />
                      <span className="font-semibold text-white text-sm">Notifications</span>
                    </div>
                    {unreadCount > 0 && (
                      <button
                        onClick={markAllAsRead}
                        className="text-xs text-evgreen-400 hover:text-evgreen-300 transition-colors"
                      >
                        Mark all read
                      </button>
                    )}
                  </div>

                  <div className="max-h-72 overflow-y-auto divide-y divide-navy-800/80 my-2">
                    {notifications.length === 0 ? (
                      <div className="text-center py-6 text-slate-400 text-sm">
                        No notifications yet
                      </div>
                    ) : (
                      notifications.slice(0, 15).map((n) => (
                        <div
                          key={n.id}
                          onClick={() => !n.is_read && markAsRead(n.id)}
                          className={`py-2.5 px-2 rounded-lg text-xs cursor-pointer transition-colors ${
                            n.is_read ? 'opacity-60 hover:bg-navy-800/40' : 'bg-navy-800/80 hover:bg-navy-800'
                          }`}
                        >
                          <div className="flex items-start justify-between gap-2">
                            <span className="font-medium text-slate-200">{n.message}</span>
                            {!n.is_read && (
                              <span className="w-2 h-2 rounded-full bg-evgreen-400 mt-1 shrink-0"></span>
                            )}
                          </div>
                          <span className="text-[10px] text-slate-400 mt-1 block">
                            {new Date(n.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })} • {new Date(n.timestamp).toLocaleDateString()}
                          </span>
                        </div>
                      ))
                    )}
                  </div>
                </div>
              )}
            </div>

            {/* User Profile & Role */}
            <div className="flex items-center gap-3 pl-2 border-l border-navy-700">
              <div className="flex flex-col text-right">
                <span className="text-xs font-semibold text-white truncate max-w-[120px]">{user?.name}</span>
                <span className={`text-[10px] font-bold uppercase tracking-wider ${role === 'ADMIN' ? 'text-amber-400' : 'text-evgreen-400'}`}>
                  {role === 'ADMIN' ? 'Station Admin' : 'EV Owner'}
                </span>
              </div>

              <button
                onClick={handleLogout}
                className="p-2 text-slate-400 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-colors"
                title="Log Out"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Mobile menu button */}
          <div className="flex md:hidden items-center gap-2">
            <button
              onClick={() => setNotifOpen(!notifOpen)}
              className="relative p-2 text-slate-300"
            >
              <Bell className="w-5 h-5" />
              {unreadCount > 0 && (
                <span className="absolute top-1 right-1 w-3.5 h-3.5 bg-emerald-500 text-navy-950 text-[9px] font-bold rounded-full flex items-center justify-center">
                  {unreadCount}
                </span>
              )}
            </button>
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 text-slate-300 hover:text-white"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden glass-panel border-b border-navy-800 px-4 pt-2 pb-4 space-y-1">
          {navLinks.map((link) => {
            const Icon = link.icon;
            const active = isActive(link.path);
            return (
              <Link
                key={link.path}
                to={link.path}
                onClick={() => setMobileMenuOpen(false)}
                className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium ${
                  active ? 'bg-navy-800 text-evgreen-400' : 'text-slate-300 hover:bg-navy-900'
                }`}
              >
                <Icon className="w-4 h-4" />
                {link.name}
              </Link>
            );
          })}
          <div className="pt-3 border-t border-navy-800 flex items-center justify-between">
            <span className="text-xs text-slate-400">{user?.name} ({role})</span>
            <button
              onClick={handleLogout}
              className="flex items-center gap-1.5 text-xs text-red-400 hover:text-red-300"
            >
              <LogOut className="w-4 h-4" /> Log out
            </button>
          </div>
        </div>
      )}
    </nav>
  );
};
