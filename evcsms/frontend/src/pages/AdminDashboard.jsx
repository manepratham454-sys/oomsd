import React, { useState, useEffect } from 'react';
import apiClient from '../api/client';
import {
  Shield,
  Zap,
  DollarSign,
  Activity,
  Layers,
  MapPin,
  TrendingUp,
  BarChart2,
  Plus,
  Edit2,
  Trash2,
  CheckCircle2,
  AlertCircle,
  X,
  Power,
} from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend,
  AreaChart,
  Area,
} from 'recharts';

export const AdminDashboard = () => {
  const [activeTab, setActiveTab] = useState('analytics'); // 'analytics' | 'stations' | 'chargers'
  const [summary, setSummary] = useState(null);
  const [usageData, setUsageData] = useState([]);
  const [revenueData, setRevenueData] = useState([]);
  const [utilizationData, setUtilizationData] = useState([]);
  const [stations, setStations] = useState([]);
  const [loading, setLoading] = useState(true);

  // Station Creation Modal
  const [stationModalOpen, setStationModalOpen] = useState(false);
  const [stationName, setStationName] = useState('');
  const [stationCity, setStationCity] = useState('');
  const [stationState, setStationState] = useState('Maharashtra');
  const [stationLat, setStationLat] = useState('18.5204');
  const [stationLng, setStationLng] = useState('73.8567');
  const [stationAddress, setStationAddress] = useState('');

  // Charger Creation Modal
  const [chargerModalOpen, setChargerModalOpen] = useState(false);
  const [targetStationId, setTargetStationId] = useState('');
  const [chargerType, setChargerType] = useState('DC Fast');
  const [connectorType, setConnectorType] = useState('CCS2');
  const [powerKw, setPowerKw] = useState('60');
  const [pricePerUnit, setPricePerUnit] = useState('18.50');

  // Feedback message
  const [statusMsg, setStatusMsg] = useState({ text: '', type: '' });

  const loadAllAdminData = async () => {
    try {
      const [sumRes, useRes, revRes, utiRes, stRes] = await Promise.all([
        apiClient.get('/admin/metrics/summary'),
        apiClient.get('/admin/reports/usage?days=7'),
        apiClient.get('/admin/reports/revenue?days=7'),
        apiClient.get('/admin/reports/utilization'),
        apiClient.get('/stations'),
      ]);

      setSummary(sumRes.data);
      setUsageData(useRes.data);
      setRevenueData(revRes.data);
      setUtilizationData(utiRes.data);
      setStations(stRes.data);
      if (stRes.data.length > 0 && !targetStationId) {
        setTargetStationId(stRes.data[0].id.toString());
      }
    } catch (err) {
      console.error("Admin dashboard fetch failed", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAllAdminData();
  }, []);

  const handleCreateStation = async (e) => {
    e.preventDefault();
    try {
      await apiClient.post('/stations', {
        name: stationName,
        city: stationCity,
        state: stationState,
        country: 'India',
        latitude: parseFloat(stationLat),
        longitude: parseFloat(stationLng),
        address: stationAddress,
      });
      setStationModalOpen(false);
      setStationName('');
      setStationCity('');
      setStationAddress('');
      setStatusMsg({ text: 'New station created successfully.', type: 'success' });
      loadAllAdminData();
    } catch (err) {
      setStatusMsg({ text: err.response?.data?.detail || 'Failed to create station.', type: 'error' });
    }
  };

  const handleAddCharger = async (e) => {
    e.preventDefault();
    try {
      await apiClient.post(`/stations/${targetStationId}/chargers`, {
        station_id: parseInt(targetStationId),
        type: chargerType,
        connector_type: connectorType,
        power_kw: parseFloat(powerKw),
        price_per_unit: parseFloat(pricePerUnit),
        status: 'Available',
      });
      setChargerModalOpen(false);
      setStatusMsg({ text: 'New charger port added.', type: 'success' });
      loadAllAdminData();
    } catch (err) {
      setStatusMsg({ text: err.response?.data?.detail || 'Failed to add charger.', type: 'error' });
    }
  };

  const handleUpdateChargerStatus = async (chargerId, newStatus) => {
    try {
      await apiClient.patch(`/chargers/${chargerId}/status`, { status: newStatus });
      setStatusMsg({ text: `Charger #${chargerId} status updated to ${newStatus}.`, type: 'success' });
      loadAllAdminData();
    } catch (err) {
      setStatusMsg({ text: 'Failed to update charger status.', type: 'error' });
    }
  };

  const handleUpdatePrice = async (chargerId, newPrice) => {
    const parsed = parseFloat(newPrice);
    if (isNaN(parsed) || parsed <= 0) return;
    try {
      await apiClient.patch(`/chargers/${chargerId}/pricing`, { price_per_unit: parsed });
      setStatusMsg({ text: `Charger #${chargerId} tariff updated to ₹${parsed}/kWh.`, type: 'success' });
      loadAllAdminData();
    } catch (err) {
      setStatusMsg({ text: 'Failed to update pricing.', type: 'error' });
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Admin Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-500/20 text-amber-400 text-xs font-bold mb-2 border border-amber-500/30">
            <Shield className="w-3.5 h-3.5" /> Station Operator Console
          </div>
          <h1 className="text-3xl font-extrabold text-white tracking-tight">Admin Management & Analytics Hub</h1>
          <p className="text-slate-400 text-xs mt-1">
            Configure stations, override charger statuses, set dynamic pricing tariffs, and view real-time energy & revenue reports.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setStationModalOpen(true)}
            className="py-2.5 px-4 rounded-xl bg-navy-800 hover:bg-navy-700 text-white border border-navy-700 font-bold text-xs flex items-center gap-1.5"
          >
            <Plus className="w-4 h-4 text-evgreen-400" /> New Station
          </button>
          <button
            onClick={() => setChargerModalOpen(true)}
            className="py-2.5 px-4 rounded-xl bg-gradient-to-r from-evgreen-500 to-emerald-600 hover:from-evgreen-400 text-navy-950 font-bold text-xs shadow-glow-green flex items-center gap-1.5"
          >
            <Plus className="w-4 h-4" /> New Charger
          </button>
        </div>
      </div>

      {statusMsg.text && (
        <div
          className={`p-4 rounded-2xl text-xs font-semibold flex items-center justify-between ${
            statusMsg.type === 'success'
              ? 'bg-emerald-500/10 border border-emerald-500/30 text-emerald-300'
              : 'bg-red-500/10 border border-red-500/30 text-red-300'
          }`}
        >
          <span>{statusMsg.text}</span>
          <button onClick={() => setStatusMsg({ text: '', type: '' })} className="text-slate-400 hover:text-white">
            Dismiss
          </button>
        </div>
      )}

      {/* Summary Metrics Cards */}
      {summary && (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          <div className="glass-panel p-4 rounded-2xl border border-navy-700">
            <span className="text-[11px] text-slate-400 block font-medium">Stations</span>
            <strong className="text-2xl font-black text-white">{summary.total_stations}</strong>
            <span className="text-[10px] text-slate-500 mt-1 block">Active Hubs</span>
          </div>

          <div className="glass-panel p-4 rounded-2xl border border-navy-700">
            <span className="text-[11px] text-slate-400 block font-medium">Total Chargers</span>
            <strong className="text-2xl font-black text-evcyan-400">{summary.total_chargers}</strong>
            <span className="text-[10px] text-slate-500 mt-1 block">AC / DC Fast</span>
          </div>

          <div className="glass-panel p-4 rounded-2xl border border-navy-700">
            <span className="text-[11px] text-slate-400 block font-medium">Active Sessions</span>
            <strong className="text-2xl font-black text-amber-400">{summary.active_sessions}</strong>
            <span className="text-[10px] text-slate-500 mt-1 block">Live Metering</span>
          </div>

          <div className="glass-panel p-4 rounded-2xl border border-navy-700">
            <span className="text-[11px] text-slate-400 block font-medium">Delivered Energy</span>
            <strong className="text-2xl font-black text-emerald-400">{summary.total_energy_delivered_kwh}</strong>
            <span className="text-[10px] text-slate-500 mt-1 block">kWh Dispensed</span>
          </div>

          <div className="glass-panel p-4 rounded-2xl border border-navy-700">
            <span className="text-[11px] text-slate-400 block font-medium">Total Revenue</span>
            <strong className="text-2xl font-black text-white">₹{summary.total_revenue_overall}</strong>
            <span className="text-[10px] text-slate-500 mt-1 block">Settled Payments</span>
          </div>

          <div className="glass-panel p-4 rounded-2xl border border-navy-700">
            <span className="text-[11px] text-slate-400 block font-medium">Registered Drivers</span>
            <strong className="text-2xl font-black text-slate-200">{summary.total_users}</strong>
            <span className="text-[10px] text-slate-500 mt-1 block">EV Owners</span>
          </div>
        </div>
      )}

      {/* Tabs Switcher */}
      <div className="flex border-b border-navy-800">
        <button
          onClick={() => setActiveTab('analytics')}
          className={`py-3 px-6 text-xs font-bold border-b-2 flex items-center gap-2 transition-colors ${
            activeTab === 'analytics'
              ? 'border-evgreen-500 text-evgreen-400'
              : 'border-transparent text-slate-400 hover:text-white'
          }`}
        >
          <BarChart2 className="w-4 h-4" /> Reports & Analytics (Recharts)
        </button>

        <button
          onClick={() => setActiveTab('stations')}
          className={`py-3 px-6 text-xs font-bold border-b-2 flex items-center gap-2 transition-colors ${
            activeTab === 'stations'
              ? 'border-evgreen-500 text-evgreen-400'
              : 'border-transparent text-slate-400 hover:text-white'
          }`}
        >
          <Layers className="w-4 h-4" /> Station & Charger Inventory
        </button>
      </div>

      {/* TAB 1: Analytics & Reports */}
      {activeTab === 'analytics' && (
        <div className="space-y-8">
          {/* Charts Row: Usage & Revenue */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Daily Usage Chart */}
            <div className="glass-panel p-6 rounded-3xl border border-navy-700">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-bold text-white flex items-center gap-2">
                  <Zap className="w-4 h-4 text-evcyan-400" /> Daily Energy Dispensed (kWh)
                </h3>
                <span className="text-[10px] text-slate-400">7-Day Window</span>
              </div>

              <div className="h-64 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={usageData.length > 0 ? usageData : [{ date: '2026-10-12', total_energy_kwh: 45 }, { date: '2026-10-13', total_energy_kwh: 28.5 }, { date: '2026-10-14', total_energy_kwh: 52 }]}>
                    <defs>
                      <linearGradient id="energyGrad" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#0ea5e9" stopOpacity={0.6}/>
                        <stop offset="95%" stopColor="#0ea5e9" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                    <XAxis dataKey="date" stroke="#64748b" fontSize={10} />
                    <YAxis stroke="#64748b" fontSize={10} unit=" kWh" />
                    <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '0.75rem', fontSize: '12px' }} />
                    <Area type="monotone" dataKey="total_energy_kwh" stroke="#0ea5e9" fillOpacity={1} fill="url(#energyGrad)" name="Energy Delivered (kWh)" />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Daily Revenue Chart */}
            <div className="glass-panel p-6 rounded-3xl border border-navy-700">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-bold text-white flex items-center gap-2">
                  <DollarSign className="w-4 h-4 text-emerald-400" /> Daily Revenue (₹)
                </h3>
                <span className="text-[10px] text-slate-400">7-Day Window</span>
              </div>

              <div className="h-64 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={revenueData.length > 0 ? revenueData : [{ date: '2026-10-12', total_revenue: 990 }, { date: '2026-10-13', total_revenue: 527.25 }, { date: '2026-10-14', total_revenue: 1200 }]}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                    <XAxis dataKey="date" stroke="#64748b" fontSize={10} />
                    <YAxis stroke="#64748b" fontSize={10} unit=" ₹" />
                    <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '0.75rem', fontSize: '12px' }} />
                    <Bar dataKey="total_revenue" fill="#10b981" radius={[6, 6, 0, 0]} name="Gross Revenue (INR)" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>

          {/* Station Charger Utilization Table */}
          <div className="glass-panel p-6 rounded-3xl border border-navy-700 space-y-4">
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-evgreen-400" /> Station Charger Utilization Rates
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {utilizationData.map((uti) => (
                <div key={uti.station_id} className="p-4 rounded-2xl bg-navy-900 border border-navy-800 space-y-3">
                  <div className="flex justify-between items-center">
                    <div>
                      <h4 className="font-bold text-white text-sm">{uti.station_name}</h4>
                      <span className="text-xs text-slate-400">{uti.city}</span>
                    </div>
                    <span className="text-base font-black text-emerald-400">{uti.utilization_rate_pct}% Utilization</span>
                  </div>

                  {/* Progress bar */}
                  <div className="w-full bg-navy-800 h-2.5 rounded-full overflow-hidden">
                    <div
                      className="bg-gradient-to-r from-evcyan-500 to-evgreen-500 h-full rounded-full transition-all duration-500"
                      style={{ width: `${Math.max(uti.utilization_rate_pct, 5)}%` }}
                    ></div>
                  </div>

                  <div className="grid grid-cols-3 gap-2 text-[11px] text-center pt-1">
                    <div className="p-2 rounded-lg bg-navy-950">
                      <span className="text-slate-400 block">Available</span>
                      <strong className="text-emerald-400 font-bold">{uti.available_chargers}</strong>
                    </div>
                    <div className="p-2 rounded-lg bg-navy-950">
                      <span className="text-slate-400 block">Busy</span>
                      <strong className="text-blue-400 font-bold">{uti.busy_chargers}</strong>
                    </div>
                    <div className="p-2 rounded-lg bg-navy-950">
                      <span className="text-slate-400 block">Reserved</span>
                      <strong className="text-amber-400 font-bold">{uti.reserved_chargers}</strong>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* TAB 2: Station & Charger Inventory */}
      {activeTab === 'stations' && (
        <div className="space-y-6">
          {stations.map((st) => (
            <div key={st.id} className="glass-panel p-6 rounded-3xl border border-navy-700 space-y-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-navy-800 gap-2">
                <div>
                  <h3 className="text-lg font-bold text-white">{st.name}</h3>
                  <span className="text-xs text-slate-400">{st.city}, {st.state} ({st.latitude}, {st.longitude})</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                    {st.chargers?.length || 0} Total Ports
                  </span>
                </div>
              </div>

              {/* Station Chargers Grid with Live Toggle Controls */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {st.chargers?.map((c) => (
                  <div key={c.id} className="p-4 rounded-2xl bg-navy-900 border border-navy-800 space-y-3">
                    <div className="flex justify-between items-start">
                      <div>
                        <span className="text-[10px] font-semibold text-slate-400">Port #{c.id}</span>
                        <h4 className="font-bold text-white text-sm">{c.type} ({c.power_kw} kW)</h4>
                        <span className="text-xs text-slate-400">{c.connector_type}</span>
                      </div>

                      {/* Status override select */}
                      <select
                        value={c.status}
                        onChange={(e) => handleUpdateChargerStatus(c.id, e.target.value)}
                        className={`text-xs font-bold py-1 px-2.5 rounded-lg border focus:outline-none ${
                          c.status === 'Available'
                            ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40'
                            : c.status === 'Busy'
                            ? 'bg-blue-500/20 text-blue-400 border-blue-500/40'
                            : c.status === 'Reserved'
                            ? 'bg-amber-500/20 text-amber-400 border-amber-500/40'
                            : 'bg-red-500/20 text-red-400 border-red-500/40'
                        }`}
                      >
                        <option value="Available" className="bg-navy-900 text-white">Available</option>
                        <option value="Busy" className="bg-navy-900 text-white">Busy</option>
                        <option value="Reserved" className="bg-navy-900 text-white">Reserved</option>
                        <option value="Offline" className="bg-navy-900 text-white">Offline</option>
                      </select>
                    </div>

                    {/* Tariff Edit Input */}
                    <div className="pt-2 border-t border-navy-800 flex items-center justify-between text-xs">
                      <span className="text-slate-400">Tariff (₹/kWh):</span>
                      <div className="flex items-center gap-1.5">
                        <input
                          type="number"
                          step="0.5"
                          defaultValue={c.price_per_unit}
                          onBlur={(e) => handleUpdatePrice(c.id, e.target.value)}
                          className="w-20 py-1 px-2 bg-navy-950 border border-navy-700 rounded-lg text-emerald-400 font-bold text-right"
                        />
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Modal: New Station */}
      {stationModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-navy-950/80 backdrop-blur-md animate-in fade-in">
          <div className="glass-panel w-full max-w-md p-6 sm:p-8 rounded-3xl border border-navy-700 shadow-2xl relative">
            <button onClick={() => setStationModalOpen(false)} className="absolute top-5 right-5 text-slate-400 hover:text-white">
              <X className="w-5 h-5" />
            </button>
            <h3 className="text-xl font-bold text-white mb-4">Add New Charging Station</h3>
            <form onSubmit={handleCreateStation} className="space-y-4 text-xs">
              <div>
                <label className="block text-slate-300 uppercase tracking-wider mb-1">Station Name</label>
                <input
                  type="text"
                  required
                  value={stationName}
                  onChange={(e) => setStationName(e.target.value)}
                  placeholder="e.g. Pune GreenCharge - Kothrud"
                  className="w-full py-2.5 px-3 bg-navy-900 border border-navy-700 rounded-xl text-white focus:ring-2 focus:ring-evgreen-500"
                />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-300 uppercase tracking-wider mb-1">City</label>
                  <input
                    type="text"
                    required
                    value={stationCity}
                    onChange={(e) => setStationCity(e.target.value)}
                    placeholder="e.g. Pune"
                    className="w-full py-2.5 px-3 bg-navy-900 border border-navy-700 rounded-xl text-white focus:ring-2 focus:ring-evgreen-500"
                  />
                </div>
                <div>
                  <label className="block text-slate-300 uppercase tracking-wider mb-1">State</label>
                  <input
                    type="text"
                    required
                    value={stationState}
                    onChange={(e) => setStationState(e.target.value)}
                    className="w-full py-2.5 px-3 bg-navy-900 border border-navy-700 rounded-xl text-white focus:ring-2 focus:ring-evgreen-500"
                  />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-300 uppercase tracking-wider mb-1">Latitude</label>
                  <input
                    type="text"
                    required
                    value={stationLat}
                    onChange={(e) => setStationLat(e.target.value)}
                    className="w-full py-2.5 px-3 bg-navy-900 border border-navy-700 rounded-xl text-white focus:ring-2 focus:ring-evgreen-500"
                  />
                </div>
                <div>
                  <label className="block text-slate-300 uppercase tracking-wider mb-1">Longitude</label>
                  <input
                    type="text"
                    required
                    value={stationLng}
                    onChange={(e) => setStationLng(e.target.value)}
                    className="w-full py-2.5 px-3 bg-navy-900 border border-navy-700 rounded-xl text-white focus:ring-2 focus:ring-evgreen-500"
                  />
                </div>
              </div>
              <div>
                <label className="block text-slate-300 uppercase tracking-wider mb-1">Full Street Address</label>
                <input
                  type="text"
                  value={stationAddress}
                  onChange={(e) => setStationAddress(e.target.value)}
                  placeholder="Street / IT Park address"
                  className="w-full py-2.5 px-3 bg-navy-900 border border-navy-700 rounded-xl text-white focus:ring-2 focus:ring-evgreen-500"
                />
              </div>
              <button
                type="submit"
                className="w-full py-3 rounded-xl bg-gradient-to-r from-evgreen-500 to-emerald-600 text-navy-950 font-bold shadow-glow-green mt-2"
              >
                Create Station
              </button>
            </form>
          </div>
        </div>
      )}

      {/* Modal: New Charger */}
      {chargerModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-navy-950/80 backdrop-blur-md animate-in fade-in">
          <div className="glass-panel w-full max-w-md p-6 sm:p-8 rounded-3xl border border-navy-700 shadow-2xl relative">
            <button onClick={() => setChargerModalOpen(false)} className="absolute top-5 right-5 text-slate-400 hover:text-white">
              <X className="w-5 h-5" />
            </button>
            <h3 className="text-xl font-bold text-white mb-4">Add Charger Port</h3>
            <form onSubmit={handleAddCharger} className="space-y-4 text-xs">
              <div>
                <label className="block text-slate-300 uppercase tracking-wider mb-1">Target Station</label>
                <select
                  value={targetStationId}
                  onChange={(e) => setTargetStationId(e.target.value)}
                  className="w-full py-2.5 px-3 bg-navy-900 border border-navy-700 rounded-xl text-white focus:ring-2 focus:ring-evgreen-500"
                >
                  {stations.map((st) => (
                    <option key={st.id} value={st.id}>{st.name} ({st.city})</option>
                  ))}
                </select>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-300 uppercase tracking-wider mb-1">Type</label>
                  <select
                    value={chargerType}
                    onChange={(e) => setChargerType(e.target.value)}
                    className="w-full py-2.5 px-3 bg-navy-900 border border-navy-700 rounded-xl text-white focus:ring-2 focus:ring-evgreen-500"
                  >
                    <option value="DC Fast">DC Fast</option>
                    <option value="AC">AC</option>
                  </select>
                </div>
                <div>
                  <label className="block text-slate-300 uppercase tracking-wider mb-1">Connector Standard</label>
                  <select
                    value={connectorType}
                    onChange={(e) => setConnectorType(e.target.value)}
                    className="w-full py-2.5 px-3 bg-navy-900 border border-navy-700 rounded-xl text-white focus:ring-2 focus:ring-evgreen-500"
                  >
                    <option value="CCS2">CCS2</option>
                    <option value="Type 2">Type 2</option>
                    <option value="CHAdeMO">CHAdeMO</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-300 uppercase tracking-wider mb-1">Power Output (kW)</label>
                  <input
                    type="number"
                    step="0.5"
                    required
                    value={powerKw}
                    onChange={(e) => setPowerKw(e.target.value)}
                    className="w-full py-2.5 px-3 bg-navy-900 border border-navy-700 rounded-xl text-white focus:ring-2 focus:ring-evgreen-500"
                  />
                </div>
                <div>
                  <label className="block text-slate-300 uppercase tracking-wider mb-1">Tariff (₹ / kWh)</label>
                  <input
                    type="number"
                    step="0.5"
                    required
                    value={pricePerUnit}
                    onChange={(e) => setPricePerUnit(e.target.value)}
                    className="w-full py-2.5 px-3 bg-navy-900 border border-navy-700 rounded-xl text-white focus:ring-2 focus:ring-evgreen-500"
                  />
                </div>
              </div>

              <button
                type="submit"
                className="w-full py-3 rounded-xl bg-gradient-to-r from-evgreen-500 to-emerald-600 text-navy-950 font-bold shadow-glow-green mt-2"
              >
                Add Charger to Station
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
