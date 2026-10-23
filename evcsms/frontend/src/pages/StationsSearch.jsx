import React, { useState, useEffect, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import apiClient from '../api/client';
import { StationMap } from '../components/StationMap';
import {
  Search,
  MapPin,
  Zap,
  Filter,
  Navigation,
  Compass,
  ArrowRight,
  CheckCircle2,
  AlertTriangle,
  RotateCcw,
  Sparkles,
  SlidersHorizontal,
} from 'lucide-react';

export const StationsSearch = () => {
  const navigate = useNavigate();

  const [stations, setStations] = useState([]);
  const [selectedStation, setSelectedStation] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [cityFilter, setCityFilter] = useState('');
  const [typeFilter, setTypeFilter] = useState('');
  const [availableOnly, setAvailableOnly] = useState(false);
  const [userLocation, setUserLocation] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchStations = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (cityFilter) params.append('city', cityFilter);
      if (typeFilter) params.append('charger_type', typeFilter);
      if (availableOnly) params.append('available_only', 'true');
      if (userLocation) {
        params.append('lat', userLocation.lat);
        params.append('lng', userLocation.lng);
      }

      const res = await apiClient.get(`/stations?${params.toString()}`);
      setStations(res.data);
    } catch (err) {
      console.error("Failed to fetch stations", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStations();
  }, [cityFilter, typeFilter, availableOnly, userLocation]);

  // Client-side text filter by name, address, or connector
  const filteredStations = useMemo(() => {
    if (!searchQuery.trim()) return stations;
    const q = searchQuery.toLowerCase();
    return stations.filter(
      (s) =>
        s.name.toLowerCase().includes(q) ||
        s.address.toLowerCase().includes(q) ||
        s.city.toLowerCase().includes(q)
    );
  }, [stations, searchQuery]);

  const handleUseLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          setUserLocation({ lat: pos.coords.latitude, lng: pos.coords.longitude });
        },
        () => {
          // Fallback to Pune coordinates for demo
          setUserLocation({ lat: 18.5204, lng: 73.8567 });
        }
      );
    } else {
      setUserLocation({ lat: 18.5204, lng: 73.8567 });
    }
  };

  const resetAllFilters = () => {
    setCityFilter('');
    setTypeFilter('');
    setAvailableOnly(false);
    setUserLocation(null);
    setSearchQuery('');
    setSelectedStation(null);
  };

  const cities = useMemo(() => {
    return [
      { label: 'All Regions', value: '', count: stations.length },
      { label: 'Pune', value: 'Pune', count: stations.filter((s) => s.city === 'Pune').length },
      { label: 'Mumbai', value: 'Mumbai', count: stations.filter((s) => s.city === 'Mumbai').length },
      { label: 'Navi Mumbai', value: 'Navi Mumbai', count: stations.filter((s) => s.city === 'Navi Mumbai').length },
      { label: 'Thane', value: 'Thane', count: stations.filter((s) => s.city === 'Thane').length },
      { label: 'Expressway', value: 'Expressway', count: stations.filter((s) => s.city === 'Expressway').length },
      { label: 'Lonavala', value: 'Lonavala', count: stations.filter((s) => s.city === 'Lonavala').length },
    ];
  }, [stations]);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Header & Filter Controls Card */}
      <div className="relative overflow-hidden rounded-3xl bg-[#080e1d]/90 backdrop-blur-xl border border-navy-700/80 shadow-[0_16px_40px_rgba(0,0,0,0.6)] p-6 space-y-5">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/15 text-emerald-400 text-xs font-bold mb-2 border border-emerald-500/30">
              <Sparkles className="w-3.5 h-3.5" /> High-Voltage EV Supercharging Corridor
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight flex items-center gap-3">
              Charging Hub Network
              <span className="text-xs font-bold px-3 py-1 rounded-full bg-navy-800 text-slate-300 border border-navy-700">
                {filteredStations.length} Hubs Available
              </span>
            </h1>
            <p className="text-slate-400 text-xs sm:text-sm mt-1 max-w-2xl">
              Locate CCS2 DC Fast Chargers (up to 150 kW) and Type-2 AC standard charging stations across Pune, Mumbai, Navi Mumbai, and Thane.
            </p>
          </div>

          <div className="flex items-center gap-3 shrink-0">
            <button
              onClick={handleUseLocation}
              className={`py-2.5 px-4 rounded-xl text-xs font-bold flex items-center gap-2 transition-all ${
                userLocation
                  ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 shadow-glow-green'
                  : 'bg-navy-800 hover:bg-navy-700 text-slate-300 border border-navy-700'
              }`}
            >
              <Navigation className="w-4 h-4 text-evgreen-400" />
              {userLocation ? 'Location Active (Sorted by Distance)' : 'Use GPS Location'}
            </button>
          </div>
        </div>

        {/* Quick Search & Filter Chips Bar */}
        <div className="pt-2 border-t border-navy-800/80 space-y-3">
          <div className="grid grid-cols-1 md:grid-cols-12 gap-3 items-center">
            {/* Search Input (5 Cols) */}
            <div className="md:col-span-5 relative">
              <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                placeholder="Search hub by name, landmark, or street..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 bg-[#0b1325] border border-navy-700 rounded-xl text-white text-xs placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-evgreen-500 focus:border-transparent transition-all"
              />
            </div>

            {/* City Quick Filter Pills (5 Cols) */}
            <div className="md:col-span-5 flex items-center gap-1.5 overflow-x-auto pb-1 md:pb-0 scrollbar-none">
              {cities.map((c) => {
                const isActive = cityFilter === c.value;
                return (
                  <button
                    key={c.value}
                    onClick={() => {
                      setCityFilter(c.value);
                      setSelectedStation(null);
                    }}
                    className={`py-2 px-3 rounded-xl text-xs font-semibold shrink-0 transition-all ${
                      isActive
                        ? 'bg-gradient-to-r from-evgreen-500 to-emerald-600 text-navy-950 font-bold shadow-sm'
                        : 'bg-navy-900/90 text-slate-400 hover:text-white hover:bg-navy-800 border border-navy-800'
                    }`}
                  >
                    {c.label} ({c.count})
                  </button>
                );
              })}
            </div>

            {/* Reset Action (2 Cols) */}
            <div className="md:col-span-2 flex justify-end">
              <button
                onClick={resetAllFilters}
                className="w-full py-2 px-3 bg-navy-900 hover:bg-navy-800 text-slate-400 hover:text-white border border-navy-700 rounded-xl text-xs font-medium flex items-center justify-center gap-1.5 transition-colors"
              >
                <RotateCcw className="w-3.5 h-3.5" /> Reset
              </button>
            </div>
          </div>

          {/* Secondary Filter Row: Charger Type & Availability */}
          <div className="flex flex-wrap items-center gap-2 pt-1 text-xs">
            <span className="text-slate-500 text-[11px] font-bold uppercase tracking-wider flex items-center gap-1">
              <SlidersHorizontal className="w-3 h-3 text-slate-400" /> Filter:
            </span>

            <button
              onClick={() => setTypeFilter('')}
              className={`py-1.5 px-3 rounded-lg text-xs font-medium transition-colors ${
                typeFilter === ''
                  ? 'bg-navy-800 text-white border border-navy-600'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              All Types
            </button>

            <button
              onClick={() => setTypeFilter('DC Fast')}
              className={`py-1.5 px-3 rounded-lg text-xs font-medium flex items-center gap-1.5 transition-colors ${
                typeFilter === 'DC Fast'
                  ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 font-bold'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <Zap className="w-3.5 h-3.5 text-emerald-400" /> DC Ultra-Fast (60-150kW)
            </button>

            <button
              onClick={() => setTypeFilter('AC')}
              className={`py-1.5 px-3 rounded-lg text-xs font-medium transition-colors ${
                typeFilter === 'AC'
                  ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/40 font-bold'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              AC Standard (7.4-22kW)
            </button>

            <label className="ml-auto flex items-center gap-2 cursor-pointer text-slate-300 select-none py-1 px-2.5 rounded-lg bg-navy-900/60 border border-navy-800 hover:border-navy-700 transition-colors">
              <input
                type="checkbox"
                checked={availableOnly}
                onChange={(e) => setAvailableOnly(e.target.checked)}
                className="w-3.5 h-3.5 rounded text-emerald-500 bg-navy-800 border-navy-700 focus:ring-emerald-500"
              />
              <span className="text-xs font-semibold">Available Ports Only</span>
            </label>
          </div>
        </div>
      </div>

      {/* Main Grid: Interactive Map & Stations List Split View */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left: Opaque Interactive Map (7 Cols) */}
        <div className="lg:col-span-7 sticky top-20">
          <StationMap
            stations={filteredStations}
            selectedStation={selectedStation}
            onSelectStation={(s) => setSelectedStation(s)}
          />
        </div>

        {/* Right: Premium Station Cards List (5 Cols) */}
        <div className="lg:col-span-5 space-y-3.5 max-h-[560px] overflow-y-auto pr-1">
          {selectedStation && (
            <div className="flex items-center justify-between p-3 rounded-2xl bg-cyan-950/40 border border-cyan-500/30">
              <div className="flex items-center gap-2 text-xs text-cyan-300">
                <MapPin className="w-4 h-4 text-cyan-400" />
                <span className="font-semibold truncate max-w-[200px]">Focused: {selectedStation.name}</span>
              </div>
              <button
                onClick={() => setSelectedStation(null)}
                className="text-xs font-bold text-cyan-400 hover:text-white underline"
              >
                Show All ({filteredStations.length})
              </button>
            </div>
          )}

          {loading ? (
            <div className="p-12 rounded-3xl bg-[#080e1d]/90 border border-navy-800 text-center text-slate-400 text-sm flex flex-col items-center justify-center gap-3">
              <div className="w-8 h-8 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin"></div>
              <span>Synchronizing charging hub telemetry...</span>
            </div>
          ) : filteredStations.length === 0 ? (
            <div className="p-12 rounded-3xl bg-[#080e1d]/90 border border-navy-800 text-center text-slate-400 text-sm space-y-3">
              <AlertTriangle className="w-8 h-8 text-amber-400 mx-auto" />
              <p>No charging hubs match your filter criteria.</p>
              <button
                onClick={resetAllFilters}
                className="py-2 px-4 rounded-xl bg-navy-800 hover:bg-navy-700 text-xs font-bold text-white transition-colors"
              >
                Reset Search Filters
              </button>
            </div>
          ) : (
            filteredStations.map((st) => {
              const isSelected = selectedStation?.id === st.id;
              const hasAvailable = st.available_chargers > 0;
              return (
                <div
                  key={st.id}
                  onClick={() => setSelectedStation(st)}
                  className={`p-4 sm:p-5 rounded-2xl cursor-pointer transition-all duration-200 border ${
                    isSelected
                      ? 'bg-[#0f1b33] border-cyan-400 shadow-[0_0_24px_rgba(56,189,248,0.25)] scale-[1.01]'
                      : 'bg-[#090f1d]/90 hover:bg-[#0c1426] border-navy-800/80 hover:border-navy-700 shadow-lg'
                  }`}
                >
                  <div className="flex items-start justify-between gap-3">
                    <div className="min-w-0">
                      <div className="flex items-center gap-2">
                        <h3 className="font-bold text-white text-sm truncate">{st.name}</h3>
                      </div>
                      <p className="text-xs text-slate-400 mt-0.5 flex items-center gap-1.5">
                        <MapPin className="w-3.5 h-3.5 text-slate-500 shrink-0" />
                        <span>{st.city}, {st.state}</span>
                      </p>
                    </div>

                    <span
                      className={`shrink-0 inline-flex items-center gap-1.5 text-[11px] font-bold px-2.5 py-1 rounded-full border ${
                        hasAvailable
                          ? 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30'
                          : 'bg-amber-500/15 text-amber-400 border-amber-500/30'
                      }`}
                    >
                      <span className={`w-1.5 h-1.5 rounded-full ${hasAvailable ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400'}`}></span>
                      {hasAvailable
                        ? `${st.available_chargers} / ${st.total_chargers} Free`
                        : 'Fully Occupied'}
                    </span>
                  </div>

                  <p className="text-[11px] text-slate-400 mt-2 line-clamp-1">
                    {st.address}
                  </p>

                  <div className="flex items-center justify-between mt-3 pt-3 border-t border-navy-800/60 text-xs">
                    <div className="flex items-center gap-3">
                      <span className="text-slate-400">
                        Tariff: <strong className="text-emerald-400 font-bold">₹{st.min_price?.toFixed(2)}</strong>/kWh
                      </span>
                      {st.distance_km !== null && st.distance_km !== undefined && (
                        <span className="text-cyan-400 font-semibold flex items-center gap-1">
                          <Navigation className="w-3 h-3" /> {st.distance_km} km
                        </span>
                      )}
                    </div>

                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        navigate(`/stations/${st.id}`);
                      }}
                      className="py-1.5 px-3.5 bg-gradient-to-r from-evgreen-500 to-emerald-600 hover:from-evgreen-400 hover:to-emerald-500 text-navy-950 font-extrabold rounded-xl text-xs flex items-center gap-1.5 shadow-sm transition-transform active:scale-95"
                    >
                      Book Slot <ArrowRight className="w-3 h-3" />
                    </button>
                  </div>
                </div>
              );
            })
          )}
        </div>
      </div>
    </div>
  );
};
