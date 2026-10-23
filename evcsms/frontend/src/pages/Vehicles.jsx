import React, { useState, useEffect } from 'react';
import apiClient from '../api/client';
import {
  Car,
  Battery,
  Zap,
  Plus,
  Trash2,
  CheckCircle2,
  AlertCircle,
  X,
} from 'lucide-react';

export const Vehicles = () => {
  const [vehicles, setVehicles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [regNo, setRegNo] = useState('');
  const [batteryCapacity, setBatteryCapacity] = useState('40.5');
  const [connectorType, setConnectorType] = useState('CCS2');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  const fetchVehicles = async () => {
    try {
      const res = await apiClient.get('/vehicles/my');
      setVehicles(res.data);
    } catch (err) {
      console.error("Failed to load vehicles", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchVehicles();
  }, []);

  const handleAddVehicle = async (e) => {
    e.preventDefault();
    setError('');
    setSubmitting(true);
    try {
      await apiClient.post('/vehicles', {
        reg_no: regNo,
        battery_capacity: parseFloat(batteryCapacity),
        connector_type: connectorType,
      });
      setModalOpen(false);
      setRegNo('');
      fetchVehicles();
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to register vehicle.");
    } finally {
      setSubmitting(false);
    }
  };

  const handleDeleteVehicle = async (id) => {
    if (!window.confirm("Remove this vehicle from your account?")) return;
    try {
      await apiClient.delete(`/vehicles/${id}`);
      fetchVehicles();
    } catch (err) {
      alert("Failed to remove vehicle.");
    }
  };

  const quickPresets = [
    { name: 'Tata Nexon EV', capacity: 40.5, connector: 'CCS2' },
    { name: 'MG ZS EV', capacity: 50.3, connector: 'CCS2' },
    { name: 'Hyundai Ioniq 5', capacity: 72.6, connector: 'CCS2' },
    { name: 'Mahindra XUV400', capacity: 39.4, connector: 'CCS2' },
    { name: 'Nissan Leaf (Import)', capacity: 40.0, connector: 'CHAdeMO' },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-white flex items-center gap-2">
            <Car className="w-6 h-6 text-evcyan-400" /> My Electric Vehicles
          </h1>
          <p className="text-slate-400 text-xs mt-1">
            Registered EVs are checked against charger connector standards during booking to prevent incompatibility.
          </p>
        </div>

        <button
          onClick={() => {
            setModalOpen(true);
            setError('');
          }}
          className="py-2.5 px-4 rounded-xl bg-gradient-to-r from-evgreen-500 to-emerald-600 hover:from-evgreen-400 text-navy-950 font-bold text-xs shadow-glow-green flex items-center gap-2 self-start sm:self-auto"
        >
          <Plus className="w-4 h-4" /> Add New Vehicle
        </button>
      </div>

      {/* Vehicle Cards Grid */}
      {loading ? (
        <div className="glass-panel p-12 rounded-3xl text-center text-slate-400 text-sm">
          Loading vehicles...
        </div>
      ) : vehicles.length === 0 ? (
        <div className="glass-panel p-12 rounded-3xl text-center space-y-4">
          <Car className="w-12 h-12 mx-auto text-slate-500" />
          <h3 className="text-lg font-bold text-white">No Vehicles Registered</h3>
          <p className="text-xs text-slate-400 max-w-sm mx-auto">
            Add your electric vehicle to check automatic port compatibility when reserving charging slots.
          </p>
          <button
            onClick={() => setModalOpen(true)}
            className="py-2 px-4 rounded-xl bg-navy-800 text-evgreen-400 border border-evgreen-500/30 font-semibold text-xs"
          >
            + Register EV Now
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {vehicles.map((v) => (
            <div
              key={v.id}
              className="glass-panel p-6 rounded-3xl border border-navy-700 hover:border-navy-600 transition-all flex flex-col justify-between"
            >
              <div>
                <div className="flex items-start justify-between">
                  <div>
                    <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Electric Vehicle</span>
                    <h3 className="text-xl font-black text-white tracking-wide mt-0.5">{v.reg_no}</h3>
                  </div>

                  <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-cyan-500/20 text-cyan-400 border border-cyan-500/30">
                    {v.connector_type}
                  </span>
                </div>

                <div className="mt-6 p-4 rounded-2xl bg-navy-900 border border-navy-800 text-xs space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-slate-400 flex items-center gap-1.5">
                      <Battery className="w-4 h-4 text-emerald-400" /> Battery Capacity:
                    </span>
                    <strong className="text-white font-bold">{v.battery_capacity} kWh</strong>
                  </div>

                  <div className="flex items-center justify-between">
                    <span className="text-slate-400 flex items-center gap-1.5">
                      <Zap className="w-4 h-4 text-evcyan-400" /> Compatible Ports:
                    </span>
                    <strong className="text-slate-200">{v.connector_type} (AC / DC)</strong>
                  </div>
                </div>
              </div>

              <div className="mt-6 pt-4 border-t border-navy-800 flex justify-end">
                <button
                  onClick={() => handleDeleteVehicle(v.id)}
                  className="py-1.5 px-3 rounded-lg text-xs text-red-400 hover:bg-red-500/10 font-semibold flex items-center gap-1 transition-colors"
                >
                  <Trash2 className="w-3.5 h-3.5" /> Remove
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Add Vehicle Modal */}
      {modalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-navy-950/80 backdrop-blur-md animate-in fade-in">
          <div className="glass-panel w-full max-w-lg p-6 sm:p-8 rounded-3xl border border-navy-700 shadow-2xl relative">
            <button
              onClick={() => setModalOpen(false)}
              className="absolute top-5 right-5 text-slate-400 hover:text-white"
            >
              <X className="w-5 h-5" />
            </button>

            <h3 className="text-xl font-bold text-white mb-1">Register Electric Vehicle</h3>
            <p className="text-xs text-slate-400 mb-6">
              Connector specifications ensure accurate compatibility matching at charging hubs.
            </p>

            {error && (
              <div className="mb-4 p-3 rounded-xl bg-red-500/10 border border-red-500/30 flex items-start gap-2.5 text-xs text-red-300">
                <AlertCircle className="w-4 h-4 text-red-400 shrink-0 mt-0.5" />
                <span>{error}</span>
              </div>
            )}

            {/* Quick model preset chips */}
            <div className="mb-5">
              <span className="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-2">
                Quick Model Presets
              </span>
              <div className="flex flex-wrap gap-2">
                {quickPresets.map((p) => (
                  <button
                    type="button"
                    key={p.name}
                    onClick={() => {
                      setBatteryCapacity(p.capacity.toString());
                      setConnectorType(p.connector);
                    }}
                    className="py-1 px-2.5 rounded-lg bg-navy-900 hover:bg-navy-800 text-[11px] text-slate-300 border border-navy-700 transition-colors"
                  >
                    {p.name}
                  </button>
                ))}
              </div>
            </div>

            <form onSubmit={handleAddVehicle} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">
                  Registration Number
                </label>
                <input
                  type="text"
                  required
                  value={regNo}
                  onChange={(e) => setRegNo(e.target.value.toUpperCase())}
                  placeholder="e.g. MH-12-EV-2024"
                  className="w-full py-2.5 px-3 bg-navy-900 border border-navy-700 rounded-xl text-white text-xs focus:ring-2 focus:ring-evgreen-500 tracking-wider font-semibold"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">
                    Battery Capacity (kWh)
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    required
                    value={batteryCapacity}
                    onChange={(e) => setBatteryCapacity(e.target.value)}
                    placeholder="e.g. 40.5"
                    className="w-full py-2.5 px-3 bg-navy-900 border border-navy-700 rounded-xl text-white text-xs focus:ring-2 focus:ring-evgreen-500"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">
                    Connector Standard
                  </label>
                  <select
                    value={connectorType}
                    onChange={(e) => setConnectorType(e.target.value)}
                    className="w-full py-2.5 px-3 bg-navy-900 border border-navy-700 rounded-xl text-white text-xs focus:ring-2 focus:ring-evgreen-500"
                  >
                    <option value="CCS2">CCS2 (Standard in India)</option>
                    <option value="Type 2">Type 2 (AC Slow / Fast)</option>
                    <option value="CHAdeMO">CHAdeMO (DC Japanese standard)</option>
                    <option value="GB/T">GB/T</option>
                  </select>
                </div>
              </div>

              <button
                type="submit"
                disabled={submitting}
                className="w-full mt-2 py-3 px-4 rounded-xl bg-gradient-to-r from-evgreen-500 to-emerald-600 hover:from-evgreen-400 text-navy-950 font-bold text-xs shadow-glow-green flex items-center justify-center gap-2 transition-transform transform active:scale-95 disabled:opacity-50"
              >
                {submitting ? 'Registering...' : 'Save EV Vehicle'}
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
