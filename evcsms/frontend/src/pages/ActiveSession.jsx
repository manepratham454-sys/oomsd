import React, { useState, useEffect, useRef } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import apiClient from '../api/client';
import { useNotifications } from '../context/NotificationContext';
import {
  Zap,
  Activity,
  BatteryCharging,
  Clock,
  CreditCard,
  StopCircle,
  Play,
  CheckCircle2,
  AlertCircle,
  ArrowRight,
  TrendingUp,
} from 'lucide-react';

export const ActiveSession = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { fetchNotifications } = useNotifications();

  // If navigated from a booking
  const passedBookingId = location.state?.bookingId;

  const [activeSession, setActiveSession] = useState(null);
  const [confirmedBookings, setConfirmedBookings] = useState([]);
  const [selectedBookingId, setSelectedBookingId] = useState(passedBookingId || '');
  const [loading, setLoading] = useState(true);
  const [actionError, setActionError] = useState('');
  const [sessionCompleted, setSessionCompleted] = useState(null);

  // Live simulation ticker states
  const [elapsedSeconds, setElapsedSeconds] = useState(0);
  const [liveKwh, setLiveKwh] = useState(0.0);
  const [liveCost, setLiveCost] = useState(0.0);
  const [batteryPercent, setBatteryPercent] = useState(32);
  const timerRef = useRef(null);

  // Load current active sessions or confirmed bookings
  const loadSessionState = async () => {
    try {
      const [sessionsRes, bookingsRes] = await Promise.all([
        apiClient.get('/sessions/my/active'),
        apiClient.get('/bookings/my'),
      ]);

      if (sessionsRes.data.length > 0) {
        const current = sessionsRes.data[0];
        setActiveSession(current);

        // Calculate initial elapsed time based on session start_time
        const startMs = new Date(current.start_time).getTime();
        const nowMs = Date.now();
        const diffSecs = Math.max(0, Math.floor((nowMs - startMs) / 1000));
        setElapsedSeconds(diffSecs);
      } else {
        setActiveSession(null);
      }

      const confirmed = bookingsRes.data.filter((b) => b.status === 'Confirmed');
      setConfirmedBookings(confirmed);
      if (!selectedBookingId && confirmed.length > 0) {
        setSelectedBookingId(confirmed[0].id.toString());
      }
    } catch (err) {
      console.error("Failed to load active session data", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSessionState();
  }, []);

  // Real-time ticking effect while session is active
  useEffect(() => {
    if (activeSession && activeSession.status === 'Active') {
      const powerKw = activeSession.power_kw || 50.0;
      const pricePerUnit = activeSession.price_per_unit || 15.0;

      timerRef.current = setInterval(() => {
        setElapsedSeconds((prev) => {
          const nextSecs = prev + 1;
          // Simulated units: (kW * hours)
          // For vivid presentation, accelerate time simulation by 60x so user sees numbers increment lively
          const simulatedHours = (nextSecs * 60) / 3600;
          const kwh = Math.round(powerKw * simulatedHours * 100) / 100;
          const cost = Math.round(kwh * pricePerUnit * 100) / 100;

          setLiveKwh(kwh);
          setLiveCost(cost);
          setBatteryPercent((b) => Math.min(95, 30 + Math.floor(kwh * 1.5)));
          return nextSecs;
        });
      }, 1000);
    } else {
      if (timerRef.current) clearInterval(timerRef.current);
    }

    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [activeSession]);

  const handleStartSession = async () => {
    if (!selectedBookingId) {
      setActionError("Please select a confirmed booking to start charging.");
      return;
    }
    setActionError('');
    try {
      const res = await apiClient.post('/sessions/start', {
        booking_id: parseInt(selectedBookingId),
      });
      setActiveSession(res.data);
      setSessionCompleted(null);
      setElapsedSeconds(0);
      setLiveKwh(0.1);
      fetchNotifications();
    } catch (err) {
      setActionError(err.response?.data?.detail || "Failed to start charging session.");
    }
  };

  const handleStopSession = async () => {
    if (!activeSession) return;
    if (!window.confirm("Are you sure you want to stop the charging session?")) return;
    setActionError('');
    try {
      // Pass the computed live units so user gets exact simulation result
      const res = await apiClient.post(`/sessions/${activeSession.id}/stop`, {
        custom_units: liveKwh > 0 ? liveKwh : 1.2,
      });
      setSessionCompleted(res.data);
      setActiveSession(null);
      if (timerRef.current) clearInterval(timerRef.current);
      fetchNotifications();
    } catch (err) {
      setActionError(err.response?.data?.detail || "Failed to stop charging session.");
    }
  };

  const formatTimer = (totalSeconds) => {
    const hours = Math.floor(totalSeconds / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-16 text-center text-slate-400">
        Connecting to charging telemetry stream...
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-white flex items-center gap-2">
            <Activity className="w-6 h-6 text-evgreen-400" /> Active Charging Telemetry
          </h1>
          <p className="text-slate-400 text-xs mt-1">
            Real-time energy flow simulation, battery status telemetry, and session billing calculations.
          </p>
        </div>
      </div>

      {actionError && (
        <div className="p-4 rounded-2xl bg-red-500/10 border border-red-500/30 flex items-start gap-3 text-xs text-red-300">
          <AlertCircle className="w-4 h-4 text-red-400 shrink-0 mt-0.5" />
          <span>{actionError}</span>
        </div>
      )}

      {/* Session Completed Prompt */}
      {sessionCompleted && (
        <div className="glass-panel p-8 rounded-3xl border border-emerald-500/40 shadow-glow-green text-center max-w-xl mx-auto space-y-4 animate-in fade-in">
          <div className="w-16 h-16 mx-auto rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center">
            <CheckCircle2 className="w-10 h-10" />
          </div>
          <h2 className="text-2xl font-bold text-white">Charging Session Completed!</h2>
          <p className="text-xs text-slate-300">
            Your vehicle has been successfully charged. Please proceed to payment to finalize the transaction.
          </p>

          <div className="p-4 rounded-2xl bg-navy-900 border border-navy-800 text-xs text-left space-y-2">
            <div className="flex justify-between">
              <span className="text-slate-400">Session ID:</span>
              <strong className="text-white">#{sessionCompleted.id}</strong>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Energy Delivered:</span>
              <strong className="text-evcyan-400 font-bold">{sessionCompleted.units_consumed} kWh</strong>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Total Billable Amount:</span>
              <strong className="text-emerald-400 text-sm font-bold">₹{sessionCompleted.total_cost.toFixed(2)}</strong>
            </div>
          </div>

          <button
            onClick={() => navigate('/payments', { state: { sessionId: sessionCompleted.id } })}
            className="w-full py-3 px-6 rounded-xl bg-gradient-to-r from-evgreen-500 to-emerald-600 hover:from-evgreen-400 text-navy-950 font-extrabold text-xs shadow-glow-green flex items-center justify-center gap-2 transition-transform transform active:scale-95"
          >
            <CreditCard className="w-4 h-4" /> Pay Now via UPI / Card / Wallet <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      )}

      {/* Active Session Console */}
      {activeSession ? (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Main Visualizer (7 Cols) */}
          <div className="lg:col-span-7 glass-panel p-8 rounded-3xl border border-navy-700 shadow-2xl relative overflow-hidden flex flex-col justify-between">
            <div className="flex items-center justify-between pb-4 border-b border-navy-800">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center animate-pulse">
                  <Zap className="w-6 h-6 fill-emerald-400" />
                </div>
                <div>
                  <h3 className="font-bold text-white text-base">Port #{activeSession.charger_id} • {activeSession.charger_type}</h3>
                  <span className="text-xs text-slate-400">{activeSession.station_name}</span>
                </div>
              </div>

              <span className="px-3 py-1 rounded-full text-xs font-extrabold bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 flex items-center gap-1.5 animate-pulse">
                <span className="w-2 h-2 rounded-full bg-emerald-400"></span> Live Dispensing
              </span>
            </div>

            {/* Simulated Animated Battery Flow */}
            <div className="my-8 flex flex-col items-center justify-center text-center">
              <div className="relative w-48 h-48 rounded-full border-4 border-navy-700 flex items-center justify-center shadow-glow-green">
                <div
                  className="absolute inset-0 rounded-full border-4 border-emerald-500 border-t-transparent animate-spin"
                  style={{ animationDuration: '3s' }}
                ></div>

                <div className="flex flex-col items-center z-10">
                  <BatteryCharging className="w-10 h-10 text-emerald-400 mb-1" />
                  <span className="text-3xl font-black text-white tracking-tight">{batteryPercent}%</span>
                  <span className="text-[10px] text-slate-400 font-semibold uppercase tracking-wider">State of Charge</span>
                </div>
              </div>

              <div className="mt-6 flex items-center gap-6 text-xs text-slate-300">
                <div>
                  <span className="block text-slate-500">Power Rate</span>
                  <strong className="text-white text-sm">{activeSession.power_kw} kW</strong>
                </div>
                <div className="h-6 w-px bg-navy-800"></div>
                <div>
                  <span className="block text-slate-500">Tariff</span>
                  <strong className="text-white text-sm">₹{activeSession.price_per_unit}/kWh</strong>
                </div>
                <div className="h-6 w-px bg-navy-800"></div>
                <div>
                  <span className="block text-slate-500">Vehicle</span>
                  <strong className="text-white text-sm">{activeSession.vehicle_reg_no || 'Assigned'}</strong>
                </div>
              </div>
            </div>

            {/* Stop Session Button */}
            <button
              onClick={handleStopSession}
              className="w-full py-3.5 px-4 rounded-xl bg-red-500 hover:bg-red-400 text-white font-extrabold text-sm shadow-lg flex items-center justify-center gap-2 transition-transform transform active:scale-95"
            >
              <StopCircle className="w-5 h-5" /> Stop Charging Session
            </button>
          </div>

          {/* Right Live Tickers (5 Cols) */}
          <div className="lg:col-span-5 space-y-4">
            {/* Ticker 1: Elapsed Duration */}
            <div className="glass-panel p-6 rounded-2xl border border-navy-700 flex items-center justify-between">
              <div>
                <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block">Session Duration</span>
                <span className="text-3xl font-extrabold text-white font-mono mt-1 block">
                  {formatTimer(elapsedSeconds)}
                </span>
                <span className="text-[10px] text-slate-500 mt-1 block">Real-time stopwatch</span>
              </div>
              <div className="w-12 h-12 rounded-xl bg-navy-800 text-evgreen-400 flex items-center justify-center">
                <Clock className="w-6 h-6" />
              </div>
            </div>

            {/* Ticker 2: Units Consumed (kWh) */}
            <div className="glass-panel p-6 rounded-2xl border border-navy-700 flex items-center justify-between">
              <div>
                <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block">Energy Dispensed</span>
                <span className="text-3xl font-extrabold text-evcyan-400 font-mono mt-1 block">
                  {liveKwh.toFixed(2)} <span className="text-base text-slate-400">kWh</span>
                </span>
                <span className="text-[10px] text-slate-500 mt-1 block">GRASP Information Expert metering</span>
              </div>
              <div className="w-12 h-12 rounded-xl bg-cyan-500/10 text-evcyan-400 flex items-center justify-center">
                <Zap className="w-6 h-6" />
              </div>
            </div>

            {/* Ticker 3: Live Billing Cost (INR) */}
            <div className="glass-panel p-6 rounded-2xl border border-navy-700 flex items-center justify-between">
              <div>
                <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block">Accumulated Cost</span>
                <span className="text-3xl font-extrabold text-emerald-400 font-mono mt-1 block">
                  ₹{liveCost.toFixed(2)}
                </span>
                <span className="text-[10px] text-slate-500 mt-1 block">Rate: ₹{activeSession.price_per_unit}/unit</span>
              </div>
              <div className="w-12 h-12 rounded-xl bg-emerald-500/10 text-emerald-400 flex items-center justify-center">
                <TrendingUp className="w-6 h-6" />
              </div>
            </div>
          </div>
        </div>
      ) : (
        /* If No Active Session: Start Session Picker */
        <div className="glass-panel p-8 rounded-3xl border border-navy-700 max-w-xl mx-auto space-y-6">
          <div className="text-center">
            <div className="w-14 h-14 mx-auto rounded-2xl bg-navy-800 text-evgreen-400 flex items-center justify-center mb-3">
              <Zap className="w-7 h-7" />
            </div>
            <h2 className="text-xl font-bold text-white">Start a Charging Session</h2>
            <p className="text-xs text-slate-400 mt-1">
              Select one of your confirmed reservations to plug in and start high-power energy delivery.
            </p>
          </div>

          {confirmedBookings.length === 0 ? (
            <div className="p-4 rounded-2xl bg-navy-900 border border-navy-800 text-center space-y-3">
              <p className="text-xs text-slate-400">
                You do not have any confirmed bookings at this time.
              </p>
              <button
                onClick={() => navigate('/stations')}
                className="py-2 px-4 rounded-xl bg-gradient-to-r from-evgreen-500 to-emerald-600 text-navy-950 font-bold text-xs"
              >
                Find Stations & Book
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                  Confirmed Reservation
                </label>
                <select
                  value={selectedBookingId}
                  onChange={(e) => setSelectedBookingId(e.target.value)}
                  className="w-full py-2.5 px-3 bg-navy-900 border border-navy-700 rounded-xl text-white text-xs focus:ring-2 focus:ring-evgreen-500"
                >
                  {confirmedBookings.map((b) => (
                    <option key={b.id} value={b.id}>
                      #{b.id} — {b.station_name} (Port #{b.charger_id} {b.charger_type})
                    </option>
                  ))}
                </select>
              </div>

              <button
                onClick={handleStartSession}
                className="w-full py-3 px-4 rounded-xl bg-gradient-to-r from-evgreen-500 to-emerald-600 hover:from-evgreen-400 text-navy-950 font-bold text-xs shadow-glow-green flex items-center justify-center gap-2 transition-transform transform active:scale-95"
              >
                <Play className="w-4 h-4 fill-navy-950" /> Initiate Charging Flow
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
