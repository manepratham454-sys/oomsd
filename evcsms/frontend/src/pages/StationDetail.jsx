import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import apiClient from '../api/client';
import { useAuth } from '../context/AuthContext';
import { useNotifications } from '../context/NotificationContext';
import {
  MapPin,
  Zap,
  Calendar,
  Clock,
  Car,
  CheckCircle2,
  AlertCircle,
  ArrowLeft,
  X,
  CreditCard,
  ShieldCheck,
  Power,
} from 'lucide-react';

export const StationDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const { fetchNotifications } = useNotifications();

  const [station, setStation] = useState(null);
  const [vehicles, setVehicles] = useState([]);
  const [loading, setLoading] = useState(true);

  // Booking Modal State
  const [bookingModalOpen, setBookingModalOpen] = useState(false);
  const [selectedCharger, setSelectedCharger] = useState(null);
  const [selectedVehicleId, setSelectedVehicleId] = useState('');
  const [startDate, setStartDate] = useState('');
  const [startTime, setStartTime] = useState('');
  const [endTime, setEndTime] = useState('');
  const [submittingBooking, setSubmittingBooking] = useState(false);
  const [bookingError, setBookingError] = useState('');
  const [bookingSuccess, setBookingSuccess] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [stationRes, vehiclesRes] = await Promise.all([
          apiClient.get(`/stations/${id}`),
          apiClient.get('/vehicles/my'),
        ]);
        setStation(stationRes.data);
        setVehicles(vehiclesRes.data);
        if (vehiclesRes.data.length > 0) {
          setSelectedVehicleId(vehiclesRes.data[0].id.toString());
        }
      } catch (err) {
        console.error("Failed to load station details", err);
      } finally {
        setLoading(false);
      }
    };

    // Pre-populate default times: start now + 10 mins, end start + 1 hour
    const now = new Date();
    now.setMinutes(now.getMinutes() + 10);
    const dateStr = now.toISOString().split('T')[0];
    const timeStr = now.toTimeString().split(' ')[0].slice(0, 5);

    const endObj = new Date(now.getTime() + 60 * 60 * 1000);
    const endTimeStr = endObj.toTimeString().split(' ')[0].slice(0, 5);

    setStartDate(dateStr);
    setStartTime(timeStr);
    setEndTime(endTimeStr);

    fetchData();
  }, [id]);

  const handleOpenBooking = (charger) => {
    setSelectedCharger(charger);
    setBookingError('');
    setBookingSuccess(null);
    setBookingModalOpen(true);
  };

  const handleCreateBooking = async (e) => {
    e.preventDefault();
    setBookingError('');
    setSubmittingBooking(true);

    try {
      const startDateTime = new Date(`${startDate}T${startTime}:00Z`).toISOString();
      const endDateTime = new Date(`${startDate}T${endTime}:00Z`).toISOString();

      const res = await apiClient.post('/bookings', {
        charger_id: selectedCharger.id,
        vehicle_id: selectedVehicleId ? parseInt(selectedVehicleId) : null,
        start_time: startDateTime,
        end_time: endDateTime,
      });

      setBookingSuccess(res.data);
      fetchNotifications(); // Refresh notifications immediately
    } catch (err) {
      setBookingError(err.response?.data?.detail || 'Booking failed. Please try a different slot.');
    } finally {
      setSubmittingBooking(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-16 text-center text-slate-400">
        Loading station telemetry...
      </div>
    );
  }

  if (!station) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-16 text-center text-red-400">
        Charging station not found.
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Back button */}
      <button
        onClick={() => navigate('/stations')}
        className="inline-flex items-center gap-2 text-xs font-semibold text-slate-400 hover:text-white transition-colors"
      >
        <ArrowLeft className="w-4 h-4" /> Back to Stations Search
      </button>

      {/* Station Overview Banner */}
      <div className="glass-panel p-8 rounded-3xl border border-navy-700 relative overflow-hidden">
        <div className="absolute right-0 top-0 w-96 h-96 bg-evgreen-500/10 rounded-full blur-3xl pointer-events-none"></div>
        <div className="flex flex-col md:flex-row md:items-start justify-between gap-6 relative z-10">
          <div>
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-400 text-xs font-bold mb-3 border border-emerald-500/30">
              <Zap className="w-3.5 h-3.5" /> High-Voltage EV Hub
            </div>
            <h1 className="text-3xl font-extrabold text-white">{station.name}</h1>
            <p className="text-sm text-slate-400 mt-1 flex items-center gap-1.5">
              <MapPin className="w-4 h-4 text-evgreen-400 shrink-0" />
              {station.address || `${station.city}, ${station.state}, ${station.country}`}
            </p>
          </div>

          <div className="flex items-center gap-4 bg-navy-900/90 p-4 rounded-2xl border border-navy-700/80">
            <div className="text-center px-3 border-r border-navy-700">
              <span className="block text-xs text-slate-400">Total Ports</span>
              <strong className="text-xl font-bold text-white">{station.chargers?.length || 0}</strong>
            </div>
            <div className="text-center px-3">
              <span className="block text-xs text-slate-400">Available</span>
              <strong className="text-xl font-bold text-emerald-400">
                {station.chargers?.filter((c) => c.status === 'Available').length || 0}
              </strong>
            </div>
          </div>
        </div>
      </div>

      {/* Chargers Grid */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-extrabold text-white flex items-center gap-2">
            <Power className="w-5 h-5 text-evgreen-400" /> Operational Chargers & Connectors
          </h2>
          <span className="text-xs text-slate-400">Live operational status</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {station.chargers?.map((charger) => {
            const isAvailable = charger.status === 'Available';
            const isBusy = charger.status === 'Busy';
            const isReserved = charger.status === 'Reserved';

            return (
              <div
                key={charger.id}
                className="glass-card p-6 rounded-2xl border border-navy-700 hover:border-navy-600 transition-all flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-start justify-between">
                    <div>
                      <span className="text-xs font-semibold text-slate-400">Port #{charger.id}</span>
                      <h3 className="text-lg font-bold text-white mt-0.5">{charger.type} Charger</h3>
                    </div>

                    <span
                      className={`text-xs font-bold px-2.5 py-1 rounded-full border ${
                        isAvailable
                          ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40'
                          : isBusy
                          ? 'bg-blue-500/20 text-blue-400 border-blue-500/40'
                          : isReserved
                          ? 'bg-amber-500/20 text-amber-400 border-amber-500/40'
                          : 'bg-red-500/20 text-red-400 border-red-500/40'
                      }`}
                    >
                      {charger.status}
                    </span>
                  </div>

                  <div className="mt-4 space-y-2 py-3 border-y border-navy-800 text-xs">
                    <div className="flex items-center justify-between">
                      <span className="text-slate-400">Connector Standard:</span>
                      <strong className="text-slate-200 bg-navy-800 px-2 py-0.5 rounded border border-navy-700">
                        {charger.connector_type}
                      </strong>
                    </div>

                    <div className="flex items-center justify-between">
                      <span className="text-slate-400">Output Power:</span>
                      <strong className="text-evcyan-400 font-bold">{charger.power_kw} kW</strong>
                    </div>

                    <div className="flex items-center justify-between">
                      <span className="text-slate-400">Tariff Rate:</span>
                      <strong className="text-emerald-400 font-bold">₹{charger.price_per_unit.toFixed(2)} / kWh</strong>
                    </div>
                  </div>
                </div>

                <div className="mt-5">
                  <button
                    onClick={() => handleOpenBooking(charger)}
                    disabled={!isAvailable}
                    className={`w-full py-2.5 px-4 rounded-xl text-xs font-bold flex items-center justify-center gap-2 transition-all ${
                      isAvailable
                        ? 'bg-gradient-to-r from-evgreen-500 to-emerald-600 hover:from-evgreen-400 hover:to-emerald-500 text-navy-950 shadow-glow-green cursor-pointer'
                        : 'bg-navy-800 text-slate-500 cursor-not-allowed border border-navy-700'
                    }`}
                  >
                    <Calendar className="w-4 h-4" />
                    {isAvailable ? 'Book Charging Slot' : `Unavailable (${charger.status})`}
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Booking Slot Modal */}
      {bookingModalOpen && selectedCharger && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-navy-950/80 backdrop-blur-md animate-in fade-in">
          <div className="glass-panel w-full max-w-lg p-6 sm:p-8 rounded-3xl border border-navy-700 shadow-2xl relative">
            <button
              onClick={() => setBookingModalOpen(false)}
              className="absolute top-5 right-5 text-slate-400 hover:text-white"
            >
              <X className="w-5 h-5" />
            </button>

            {bookingSuccess ? (
              <div className="text-center py-6 space-y-4">
                <div className="w-16 h-16 mx-auto rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center">
                  <CheckCircle2 className="w-10 h-10" />
                </div>
                <h3 className="text-2xl font-bold text-white">Booking Confirmed!</h3>
                <p className="text-xs text-slate-300 max-w-sm mx-auto">
                  Charger #{selectedCharger.id} has been reserved for your vehicle. A confirmation notification has been sent.
                </p>

                <div className="p-4 rounded-2xl bg-navy-900 border border-navy-700 text-left text-xs space-y-1.5">
                  <div className="flex justify-between">
                    <span className="text-slate-400">Booking ID:</span>
                    <strong className="text-white">#{bookingSuccess.id}</strong>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Station:</span>
                    <strong className="text-white">{station.name}</strong>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Reserved Slot:</span>
                    <strong className="text-emerald-400">
                      {new Date(bookingSuccess.start_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })} - {new Date(bookingSuccess.end_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </strong>
                  </div>
                </div>

                <div className="flex gap-3 pt-2">
                  <button
                    onClick={() => navigate('/bookings')}
                    className="flex-1 py-2.5 px-4 rounded-xl bg-navy-800 hover:bg-navy-700 text-slate-200 text-xs font-semibold"
                  >
                    View My Bookings
                  </button>
                  <button
                    onClick={() => navigate('/session/active', { state: { bookingId: bookingSuccess.id } })}
                    className="flex-1 py-2.5 px-4 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-navy-950 text-xs font-bold shadow-glow-green"
                  >
                    Start Session Now
                  </button>
                </div>
              </div>
            ) : (
              <div>
                <h3 className="text-xl font-bold text-white mb-1">
                  Reserve Charger #{selectedCharger.id}
                </h3>
                <p className="text-xs text-slate-400 mb-6">
                  {selectedCharger.type} ({selectedCharger.power_kw} kW) • {selectedCharger.connector_type} • ₹{selectedCharger.price_per_unit}/kWh
                </p>

                {bookingError && (
                  <div className="mb-4 p-3 rounded-xl bg-red-500/10 border border-red-500/30 flex items-start gap-2.5 text-xs text-red-300">
                    <AlertCircle className="w-4 h-4 text-red-400 shrink-0 mt-0.5" />
                    <span>{bookingError}</span>
                  </div>
                )}

                <form onSubmit={handleCreateBooking} className="space-y-4 text-left">
                  {/* Vehicle selection */}
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">
                      Select Vehicle (Connector Compatibility)
                    </label>
                    {vehicles.length === 0 ? (
                      <div className="p-3 bg-navy-900 border border-navy-700 rounded-xl text-xs text-amber-400">
                        No registered vehicles found. Please add a vehicle first or continue without assignment.
                      </div>
                    ) : (
                      <select
                        value={selectedVehicleId}
                        onChange={(e) => setSelectedVehicleId(e.target.value)}
                        className="w-full py-2.5 px-3 bg-navy-900 border border-navy-700 rounded-xl text-white text-xs focus:ring-2 focus:ring-evgreen-500"
                      >
                        {vehicles.map((v) => (
                          <option key={v.id} value={v.id}>
                            {v.reg_no} — {v.connector_type} ({v.battery_capacity} kWh)
                          </option>
                        ))}
                      </select>
                    )}
                  </div>

                  {/* Date Picker */}
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">
                      Booking Date
                    </label>
                    <input
                      type="date"
                      required
                      value={startDate}
                      onChange={(e) => setStartDate(e.target.value)}
                      className="w-full py-2.5 px-3 bg-navy-900 border border-navy-700 rounded-xl text-white text-xs focus:ring-2 focus:ring-evgreen-500"
                    />
                  </div>

                  {/* Time Window */}
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">
                        Start Time
                      </label>
                      <input
                        type="time"
                        required
                        value={startTime}
                        onChange={(e) => setStartTime(e.target.value)}
                        className="w-full py-2.5 px-3 bg-navy-900 border border-navy-700 rounded-xl text-white text-xs focus:ring-2 focus:ring-evgreen-500"
                      />
                    </div>

                    <div>
                      <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">
                        End Time
                      </label>
                      <input
                        type="time"
                        required
                        value={endTime}
                        onChange={(e) => setEndTime(e.target.value)}
                        className="w-full py-2.5 px-3 bg-navy-900 border border-navy-700 rounded-xl text-white text-xs focus:ring-2 focus:ring-evgreen-500"
                      />
                    </div>
                  </div>

                  <div className="p-3 bg-navy-900/60 border border-navy-800 rounded-xl text-xs text-slate-400">
                    * Booking flow automatically reserves the selected charger and verifies slot availability to prevent overlapping reservations.
                  </div>

                  <button
                    type="submit"
                    disabled={submittingBooking}
                    className="w-full py-3 px-4 rounded-xl bg-gradient-to-r from-evgreen-500 to-emerald-600 hover:from-evgreen-400 text-navy-950 font-bold text-xs shadow-glow-green flex items-center justify-center gap-2 transition-transform transform active:scale-95 disabled:opacity-50"
                  >
                    {submittingBooking ? 'Confirming Reservation...' : 'Confirm & Reserve Slot'}
                  </button>
                </form>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
