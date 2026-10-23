import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import apiClient from '../api/client';
import { useAuth } from '../context/AuthContext';
import {
  Zap,
  MapPin,
  Calendar,
  Activity,
  Car,
  CreditCard,
  ChevronRight,
  Clock,
  BatteryCharging,
  ArrowUpRight,
  Shield,
  Sparkles,
} from 'lucide-react';

export const Dashboard = () => {
  const { user, role } = useAuth();
  const navigate = useNavigate();

  const [activeSessions, setActiveSessions] = useState([]);
  const [recentBookings, setRecentBookings] = useState([]);
  const [vehicles, setVehicles] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [sessionsRes, bookingsRes, vehiclesRes] = await Promise.all([
          apiClient.get('/sessions/my/active'),
          apiClient.get('/bookings/my'),
          apiClient.get('/vehicles/my'),
        ]);
        setActiveSessions(sessionsRes.data);
        setRecentBookings(bookingsRes.data.slice(0, 4));
        setVehicles(vehiclesRes.data);
      } catch (err) {
        console.error("Dashboard data fetch failed", err);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const activeSession = activeSessions.length > 0 ? activeSessions[0] : null;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Welcome & Role Banner */}
      <div className="relative overflow-hidden rounded-3xl p-8 glass-panel border border-navy-700">
        <div className="absolute -right-10 -bottom-10 w-64 h-64 bg-evgreen-500/10 rounded-full blur-3xl pointer-events-none"></div>
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 relative z-10">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-400 text-xs font-semibold mb-3 border border-emerald-500/30">
              <Sparkles className="w-3.5 h-3.5" /> High-Speed Green Charging Network
            </div>
            <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
              Welcome back, <span className="bg-gradient-to-r from-white via-slate-100 to-evgreen-400 bg-clip-text text-transparent">{user?.name}</span>
            </h1>
            <p className="text-slate-400 text-sm mt-1 max-w-xl">
              Monitor active charging cycles, reserve high-speed DC Fast & AC slots across Pune and Mumbai, and manage your electric vehicles.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <Link
              to="/stations"
              className="py-3 px-5 rounded-xl bg-gradient-to-r from-evgreen-500 to-emerald-600 hover:from-evgreen-400 hover:to-emerald-500 text-navy-950 font-bold text-sm shadow-glow-green flex items-center gap-2 transition-transform transform active:scale-95"
            >
              <MapPin className="w-4 h-4" /> Find Nearest Station
            </Link>

            {role === 'ADMIN' && (
              <Link
                to="/admin"
                className="py-3 px-5 rounded-xl bg-navy-800 hover:bg-navy-700 text-amber-400 border border-amber-500/30 font-bold text-sm flex items-center gap-2 transition-colors"
              >
                <Shield className="w-4 h-4" /> Admin Hub
              </Link>
            )}
          </div>
        </div>
      </div>

      {/* Active Charging Session Banner (if in progress) */}
      {activeSession && (
        <div className="relative overflow-hidden rounded-3xl p-6 bg-gradient-to-r from-emerald-950/70 via-navy-900/90 to-cyan-950/70 border border-emerald-500/40 shadow-glow-green animate-energy-pulse">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-4">
              <div className="w-14 h-14 rounded-2xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center shrink-0">
                <BatteryCharging className="w-8 h-8 animate-bounce" />
              </div>
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-emerald-400">
                  Active Session In Progress
                </span>
                <h3 className="text-xl font-bold text-white">
                  {activeSession.station_name || 'EV Station'} • Charger #{activeSession.charger_id}
                </h3>
                <span className="text-xs text-slate-300">
                  {activeSession.power_kw} kW {activeSession.charger_type} • Started at {new Date(activeSession.start_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </span>
              </div>
            </div>

            <button
              onClick={() => navigate('/session/active')}
              className="py-2.5 px-6 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-navy-950 font-extrabold text-sm flex items-center gap-2 shadow-lg transition-transform transform active:scale-95"
            >
              Open Live Charging Console <ArrowUpRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}

      {/* Quick Stats Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="glass-panel p-5 rounded-2xl border border-navy-700">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-2">
            <span>My Bookings</span>
            <Calendar className="w-4 h-4 text-evgreen-400" />
          </div>
          <div className="text-2xl font-bold text-white">{recentBookings.length}</div>
          <span className="text-[11px] text-slate-400 mt-1 block">Scheduled reservations</span>
        </div>

        <div className="glass-panel p-5 rounded-2xl border border-navy-700">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-2">
            <span>Registered Vehicles</span>
            <Car className="w-4 h-4 text-evcyan-400" />
          </div>
          <div className="text-2xl font-bold text-white">{vehicles.length}</div>
          <span className="text-[11px] text-slate-400 mt-1 block">Compatible EV fleet</span>
        </div>

        <div className="glass-panel p-5 rounded-2xl border border-navy-700">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-2">
            <span>Active Sessions</span>
            <Activity className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-2xl font-bold text-white">{activeSessions.length}</div>
          <span className="text-[11px] text-slate-400 mt-1 block">Real-time telemetry</span>
        </div>

        <div className="glass-panel p-5 rounded-2xl border border-navy-700">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-2">
            <span>Network Tariff</span>
            <CreditCard className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold text-white">₹12 - ₹22</div>
          <span className="text-[11px] text-slate-400 mt-1 block">Per kWh delivered</span>
        </div>
      </div>

      {/* Two Column Layout: Recent Bookings & Registered Vehicles */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Bookings Section (2 Cols) */}
        <div className="lg:col-span-2 glass-panel p-6 rounded-3xl border border-navy-700 space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-navy-800">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <Calendar className="w-5 h-5 text-evgreen-400" /> Recent Bookings
            </h2>
            <Link to="/bookings" className="text-xs text-evgreen-400 hover:text-evgreen-300 font-medium flex items-center gap-1">
              View all <ChevronRight className="w-4 h-4" />
            </Link>
          </div>

          {recentBookings.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-slate-400 text-sm mb-4">No recent bookings scheduled yet.</p>
              <Link
                to="/stations"
                className="inline-flex items-center gap-2 py-2 px-4 rounded-xl bg-navy-800 text-evgreen-400 border border-evgreen-500/30 text-xs font-semibold hover:bg-navy-700 transition-colors"
              >
                Browse Stations & Book a Slot
              </Link>
            </div>
          ) : (
            <div className="space-y-3">
              {recentBookings.map((b) => (
                <div
                  key={b.id}
                  className="p-4 rounded-2xl bg-navy-900/80 border border-navy-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3 hover:border-navy-700 transition-colors"
                >
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-white text-sm">{b.station_name || 'Station'}</span>
                      <span className="text-xs text-slate-400">• Charger #{b.charger_id}</span>
                      <span
                        className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                          b.status === 'Confirmed'
                            ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                            : b.status === 'Completed'
                            ? 'bg-blue-500/20 text-blue-400'
                            : 'bg-slate-700 text-slate-300'
                        }`}
                      >
                        {b.status}
                      </span>
                    </div>

                    <div className="flex items-center gap-4 text-xs text-slate-400 mt-1">
                      <span className="flex items-center gap-1">
                        <Clock className="w-3.5 h-3.5 text-slate-500" />
                        {new Date(b.start_time).toLocaleDateString()} {new Date(b.start_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </span>
                      <span>Type: {b.charger_type} ({b.connector_type})</span>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    {b.status === 'Confirmed' && !b.session_id && (
                      <button
                        onClick={() => navigate('/session/active', { state: { bookingId: b.id } })}
                        className="py-1.5 px-3 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-navy-950 font-bold text-xs flex items-center gap-1 shadow-sm transition-colors"
                      >
                        Start Session <ArrowUpRight className="w-3 h-3" />
                      </button>
                    )}
                    <Link
                      to="/bookings"
                      className="py-1.5 px-3 rounded-lg bg-navy-800 hover:bg-navy-700 text-slate-300 text-xs font-medium transition-colors"
                    >
                      Details
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Vehicles Section (1 Col) */}
        <div className="glass-panel p-6 rounded-3xl border border-navy-700 space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-navy-800">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <Car className="w-5 h-5 text-evcyan-400" /> My Electric Vehicles
            </h2>
            <Link to="/vehicles" className="text-xs text-evcyan-400 hover:text-evcyan-300 font-medium flex items-center gap-1">
              Manage <ChevronRight className="w-4 h-4" />
            </Link>
          </div>

          {vehicles.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-slate-400 text-xs mb-3">No electric vehicles registered.</p>
              <Link
                to="/vehicles"
                className="py-1.5 px-3 rounded-lg bg-navy-800 text-evcyan-400 border border-evcyan-500/30 text-xs font-semibold"
              >
                + Add EV Vehicle
              </Link>
            </div>
          ) : (
            <div className="space-y-3">
              {vehicles.map((v) => (
                <div key={v.id} className="p-3.5 rounded-xl bg-navy-900/80 border border-navy-800">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-white text-sm tracking-wide">{v.reg_no}</span>
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-400 border border-cyan-500/30">
                      {v.connector_type}
                    </span>
                  </div>
                  <div className="text-xs text-slate-400 mt-1 flex items-center justify-between">
                    <span>Battery Capacity:</span>
                    <span className="font-semibold text-slate-200">{v.battery_capacity} kWh</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
