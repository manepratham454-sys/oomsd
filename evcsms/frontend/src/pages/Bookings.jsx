import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import apiClient from '../api/client';
import { useNotifications } from '../context/NotificationContext';
import {
  Calendar,
  Clock,
  MapPin,
  Zap,
  CheckCircle2,
  XCircle,
  AlertTriangle,
  ArrowUpRight,
  Trash2,
} from 'lucide-react';

export const Bookings = () => {
  const navigate = useNavigate();
  const { fetchNotifications } = useNotifications();

  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [cancellingId, setCancellingId] = useState(null);
  const [feedbackMsg, setFeedbackMsg] = useState({ text: '', type: '' });

  const fetchBookings = async () => {
    try {
      const res = await apiClient.get('/bookings/my');
      setBookings(res.data);
    } catch (err) {
      console.error("Failed to fetch bookings", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBookings();
  }, []);

  const handleCancelBooking = async (id) => {
    if (!window.confirm(`Are you sure you want to cancel booking #${id}?`)) return;
    setCancellingId(id);
    try {
      await apiClient.delete(`/bookings/${id}`);
      setFeedbackMsg({ text: `Booking #${id} has been cancelled and charger released.`, type: 'success' });
      await fetchBookings();
      fetchNotifications();
    } catch (err) {
      setFeedbackMsg({ text: err.response?.data?.detail || 'Failed to cancel booking.', type: 'error' });
    } finally {
      setCancellingId(null);
    }
  };

  const activeBookings = bookings.filter((b) => b.status === 'Confirmed' || b.status === 'Pending');
  const pastBookings = bookings.filter((b) => b.status !== 'Confirmed' && b.status !== 'Pending');

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-white flex items-center gap-2">
            <Calendar className="w-6 h-6 text-evgreen-400" /> My Charging Reservations
          </h1>
          <p className="text-slate-400 text-xs mt-1">
            Track upcoming slots, manage reservations, and initiate live charging sessions.
          </p>
        </div>

        <button
          onClick={() => navigate('/stations')}
          className="py-2.5 px-4 rounded-xl bg-gradient-to-r from-evgreen-500 to-emerald-600 hover:from-evgreen-400 text-navy-950 font-bold text-xs shadow-glow-green self-start sm:self-auto"
        >
          + Book New Slot
        </button>
      </div>

      {feedbackMsg.text && (
        <div
          className={`p-4 rounded-2xl text-xs font-semibold flex items-center justify-between ${
            feedbackMsg.type === 'success'
              ? 'bg-emerald-500/10 border border-emerald-500/30 text-emerald-300'
              : 'bg-red-500/10 border border-red-500/30 text-red-300'
          }`}
        >
          <span>{feedbackMsg.text}</span>
          <button onClick={() => setFeedbackMsg({ text: '', type: '' })} className="text-slate-400 hover:text-white">
            Dismiss
          </button>
        </div>
      )}

      {/* Active / Upcoming Bookings */}
      <div className="space-y-4">
        <h2 className="text-lg font-bold text-white flex items-center gap-2">
          <Clock className="w-4 h-4 text-evgreen-400" /> Active & Upcoming Reservations ({activeBookings.length})
        </h2>

        {loading ? (
          <div className="glass-panel p-8 rounded-2xl text-center text-slate-400 text-sm">
            Loading reservations...
          </div>
        ) : activeBookings.length === 0 ? (
          <div className="glass-panel p-8 rounded-2xl text-center text-slate-400 text-sm">
            No active reservations found. Search stations to reserve a slot.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {activeBookings.map((b) => (
              <div
                key={b.id}
                className="glass-panel p-6 rounded-2xl border border-navy-700 hover:border-navy-600 transition-all flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-start justify-between">
                    <div>
                      <span className="text-[11px] font-semibold text-slate-400">Reservation #{b.id}</span>
                      <h3 className="text-base font-bold text-white">{b.station_name || 'Station'}</h3>
                      <p className="text-xs text-slate-400">{b.station_city}</p>
                    </div>

                    <span className="text-[10px] font-bold px-2.5 py-1 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/40">
                      {b.status}
                    </span>
                  </div>

                  <div className="mt-4 p-3 rounded-xl bg-navy-900 border border-navy-800 text-xs space-y-1.5">
                    <div className="flex justify-between">
                      <span className="text-slate-400">Time Window:</span>
                      <strong className="text-slate-200">
                        {new Date(b.start_time).toLocaleDateString()} • {new Date(b.start_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })} - {new Date(b.end_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </strong>
                    </div>

                    <div className="flex justify-between">
                      <span className="text-slate-400">Charger:</span>
                      <strong className="text-evcyan-400">Port #{b.charger_id} ({b.charger_type} - {b.connector_type})</strong>
                    </div>

                    {b.vehicle_reg_no && (
                      <div className="flex justify-between">
                        <span className="text-slate-400">Vehicle:</span>
                        <strong className="text-slate-300">{b.vehicle_reg_no}</strong>
                      </div>
                    )}
                  </div>
                </div>

                <div className="mt-5 flex items-center gap-3">
                  <button
                    onClick={() => navigate('/session/active', { state: { bookingId: b.id } })}
                    className="flex-1 py-2 px-3 rounded-xl bg-gradient-to-r from-evgreen-500 to-emerald-600 hover:from-evgreen-400 text-navy-950 font-bold text-xs flex items-center justify-center gap-1.5 shadow-glow-green transition-transform active:scale-95"
                  >
                    <Zap className="w-3.5 h-3.5" /> Start Charging <ArrowUpRight className="w-3.5 h-3.5" />
                  </button>

                  <button
                    onClick={() => handleCancelBooking(b.id)}
                    disabled={cancellingId === b.id}
                    className="py-2 px-3 rounded-xl bg-navy-900 hover:bg-red-500/10 text-slate-400 hover:text-red-400 border border-navy-700 hover:border-red-500/30 text-xs font-semibold flex items-center gap-1 transition-colors"
                  >
                    <Trash2 className="w-3.5 h-3.5" /> Cancel
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Booking History */}
      {pastBookings.length > 0 && (
        <div className="space-y-4 pt-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-slate-400" /> Reservation History ({pastBookings.length})
          </h2>

          <div className="glass-panel rounded-2xl border border-navy-700 overflow-hidden">
            <div className="divide-y divide-navy-800 text-xs">
              {pastBookings.map((b) => (
                <div key={b.id} className="p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-white">{b.station_name}</span>
                      <span className="text-slate-400">• Charger #{b.charger_id}</span>
                      <span
                        className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                          b.status === 'Completed'
                            ? 'bg-blue-500/20 text-blue-400'
                            : b.status === 'Expired'
                            ? 'bg-amber-500/20 text-amber-400'
                            : 'bg-red-500/20 text-red-400'
                        }`}
                      >
                        {b.status}
                      </span>
                    </div>
                    <span className="text-[11px] text-slate-400 mt-1 block">
                      {new Date(b.start_time).toLocaleDateString()} ({new Date(b.start_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })})
                    </span>
                  </div>

                  {b.session_id && (
                    <button
                      onClick={() => navigate('/payments')}
                      className="py-1 px-3 bg-navy-800 hover:bg-navy-700 text-slate-300 text-xs rounded-lg self-start sm:self-auto"
                    >
                      View Invoice
                    </button>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
