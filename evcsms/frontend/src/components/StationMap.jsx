import React, { useEffect, useRef, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import { Zap, MapPin, ExternalLink, Globe, Layers, Navigation, BatteryCharging } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const GOOGLE_MAPS_API_KEY = "AIzaSyCOf9eWKzgeqoBYRJ1uws3-1J1qoailI0c";

// Fix Leaflet's default marker icon paths in Vite bundles
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

// Sleek high-end EV charging station badge pin with real-time port count
const createCustomIcon = (availableCount, isSelected = false) => {
  const isAvailable = availableCount > 0;
  const primaryColor = isSelected ? '#38bdf8' : isAvailable ? '#10b981' : '#f59e0b';
  const glowColor = isSelected ? 'rgba(56, 189, 248, 0.7)' : isAvailable ? 'rgba(16, 185, 129, 0.6)' : 'rgba(245, 158, 11, 0.6)';

  return L.divIcon({
    className: 'custom-leaflet-marker',
    html: `
      <div style="position: relative; display: flex; flex-direction: column; align-items: center; cursor: pointer;">
        <div style="
          background: #090f1d;
          border: 2px solid ${primaryColor};
          width: ${isSelected ? '38px' : '34px'};
          height: ${isSelected ? '38px' : '34px'};
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          box-shadow: 0 0 16px ${glowColor}, 0 4px 8px rgba(0,0,0,0.7);
          transition: transform 0.2s ease;
        ">
          <svg xmlns="http://www.w3.org/2000/svg" width="${isSelected ? '20' : '17'}" height="${isSelected ? '20' : '17'}" viewBox="0 0 24 24" fill="${primaryColor}" stroke="${primaryColor}" stroke-width="1.5">
            <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
          </svg>
        </div>
        <div style="
          position: absolute;
          top: -6px;
          right: -6px;
          background: ${primaryColor};
          color: #060a14;
          font-family: system-ui, -apple-system, sans-serif;
          font-weight: 800;
          font-size: 10px;
          min-width: 17px;
          height: 17px;
          border-radius: 9px;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 0 4px;
          border: 1.5px solid #060a14;
        ">
          ${availableCount}
        </div>
        <div style="
          width: 0; 
          height: 0; 
          border-left: 5px solid transparent;
          border-right: 5px solid transparent;
          border-top: 6px solid ${primaryColor};
          margin-top: -1px;
        "></div>
      </div>
    `,
    iconSize: [40, 48],
    iconAnchor: [20, 44],
    popupAnchor: [0, -42],
  });
};

const ChangeMapView = ({ center, stations, selectedStation }) => {
  const map = useMap();
  useEffect(() => {
    if (selectedStation) {
      map.setView([selectedStation.latitude, selectedStation.longitude], 14, { animate: true });
    } else if (stations && stations.length > 1) {
      const bounds = L.latLngBounds(stations.map(s => [s.latitude, s.longitude]));
      map.fitBounds(bounds, { padding: [40, 40], maxZoom: 14 });
    } else if (center && center.length === 2 && !isNaN(center[0]) && !isNaN(center[1])) {
      map.setView(center, map.getZoom());
    }
  }, [center, stations, selectedStation, map]);
  return null;
};

// Sleek Dark Theme Style for Google Maps
const darkGoogleMapsStyle = [
  { elementType: "geometry", stylers: [{ color: "#0b1329" }] },
  { elementType: "labels.text.stroke", stylers: [{ color: "#0b1329" }] },
  { elementType: "labels.text.fill", stylers: [{ color: "#746855" }] },
  {
    featureType: "administrative.locality",
    elementType: "labels.text.fill",
    stylers: [{ color: "#38bdf8" }],
  },
  {
    featureType: "poi",
    elementType: "labels.text.fill",
    stylers: [{ color: "#10b981" }],
  },
  {
    featureType: "poi.park",
    elementType: "geometry",
    stylers: [{ color: "#0d2036" }],
  },
  {
    featureType: "road",
    elementType: "geometry",
    stylers: [{ color: "#1e293b" }],
  },
  {
    featureType: "road",
    elementType: "geometry.stroke",
    stylers: [{ color: "#111827" }],
  },
  {
    featureType: "road.highway",
    elementType: "geometry",
    stylers: [{ color: "#1e3a5f" }],
  },
  {
    featureType: "road.highway",
    elementType: "geometry.stroke",
    stylers: [{ color: "#0f172a" }],
  },
  {
    featureType: "water",
    elementType: "geometry",
    stylers: [{ color: "#050b14" }],
  },
  {
    featureType: "water",
    elementType: "labels.text.fill",
    stylers: [{ color: "#0284c7" }],
  },
];

export const StationMap = ({ stations = [], selectedStation = null, onSelectStation }) => {
  const navigate = useNavigate();
  // Default to Leaflet so maps render flawlessly without Google Maps key/billing popups, with instant toggle to Google Maps
  const [mapEngine, setMapEngine] = useState('leaflet'); // 'leaflet' | 'google'
  const [googleMapsLoaded, setGoogleMapsLoaded] = useState(false);
  const [googleMapsError, setGoogleMapsError] = useState(false);

  const googleMapRef = useRef(null);
  const mapInstanceRef = useRef(null);
  const markersRef = useRef([]);

  // Default coordinates: Central Maharashtra (Pune - Mumbai corridor)
  const defaultCenter = { lat: 18.85, lng: 73.35 };
  const centerLat = selectedStation ? selectedStation.latitude : stations.length > 0 ? stations[0].latitude : defaultCenter.lat;
  const centerLng = selectedStation ? selectedStation.longitude : stations.length > 0 ? stations[0].longitude : defaultCenter.lng;

  // Handle Google Maps auth failure globally
  useEffect(() => {
    window.gm_authFailure = () => {
      console.warn("Google Maps API authentication failed or key unactivated. Switching to Leaflet OSM.");
      setGoogleMapsError(true);
      setMapEngine('leaflet');
    };
  }, []);

  // Load Google Maps JavaScript API script
  useEffect(() => {
    if (window.google && window.google.maps) {
      setGoogleMapsLoaded(true);
      return;
    }

    const existingScript = document.getElementById('google-maps-script');
    if (!existingScript) {
      const script = document.createElement('script');
      script.id = 'google-maps-script';
      script.src = `https://maps.googleapis.com/maps/api/js?key=${GOOGLE_MAPS_API_KEY}&libraries=places`;
      script.async = true;
      script.defer = true;
      script.onload = () => setGoogleMapsLoaded(true);
      script.onerror = () => {
        console.warn("Google Maps script failed to load. Falling back to Leaflet.");
        setGoogleMapsError(true);
        setMapEngine('leaflet');
      };
      document.head.appendChild(script);
    } else {
      existingScript.addEventListener('load', () => setGoogleMapsLoaded(true));
    }
  }, []);

  // Initialize and update Google Map
  useEffect(() => {
    if (mapEngine !== 'google' || !googleMapsLoaded || !googleMapRef.current || !window.google) return;

    try {
      if (!mapInstanceRef.current) {
        mapInstanceRef.current = new window.google.maps.Map(googleMapRef.current, {
          center: { lat: centerLat, lng: centerLng },
          zoom: 9,
          styles: darkGoogleMapsStyle,
          disableDefaultUI: false,
          zoomControl: true,
          mapTypeControl: true,
          streetViewControl: false,
          fullscreenControl: true,
        });
      }

      // Auto-fit bounds or pan to selected station
      if (selectedStation) {
        mapInstanceRef.current.panTo({ lat: selectedStation.latitude, lng: selectedStation.longitude });
        mapInstanceRef.current.setZoom(14);
      } else if (stations.length > 1) {
        const bounds = new window.google.maps.LatLngBounds();
        stations.forEach((st) => bounds.extend(new window.google.maps.LatLng(st.latitude, st.longitude)));
        mapInstanceRef.current.fitBounds(bounds, { top: 50, right: 50, bottom: 50, left: 50 });
      } else if (stations.length === 1) {
        mapInstanceRef.current.panTo({ lat: stations[0].latitude, lng: stations[0].longitude });
        mapInstanceRef.current.setZoom(12);
      }

      // Clear old markers
      markersRef.current.forEach((m) => m.setMap(null));
      markersRef.current = [];

      // Add markers for stations
      stations.forEach((st) => {
        const isAvailable = st.available_chargers > 0;
        const markerColor = isAvailable ? "#10b981" : "#f59e0b";
        const isSelected = selectedStation?.id === st.id;

        const marker = new window.google.maps.Marker({
          position: { lat: st.latitude, lng: st.longitude },
          map: mapInstanceRef.current,
          title: st.name,
          icon: {
            path: window.google.maps.SymbolPath.CIRCLE,
            fillColor: markerColor,
            fillOpacity: 1,
            strokeColor: isSelected ? "#38bdf8" : "#ffffff",
            strokeWeight: isSelected ? 4 : 2,
            scale: isSelected ? 14 : 11,
          },
          zIndex: isSelected ? 999 : 1,
        });

        const infoWindow = new window.google.maps.InfoWindow({
          content: `
            <div style="color: #0f172a; font-family: sans-serif; min-width: 190px; padding: 4px;">
              <h4 style="font-weight: 700; margin: 0 0 4px 0; font-size: 13px;">${st.name}</h4>
              <p style="margin: 0 0 6px 0; font-size: 11px; color: #64748b;">${st.city}, ${st.state}</p>
              <div style="display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 4px;">
                <span>Available:</span>
                <strong style="color: #10b981;">${st.available_chargers} / ${st.total_chargers} Ports</strong>
              </div>
              <div style="display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 8px;">
                <span>Tariff from:</span>
                <strong>₹${st.min_price?.toFixed(2) || '15.00'}/kWh</strong>
              </div>
              <a href="/stations/${st.id}" style="display: block; text-align: center; background: #10b981; color: #0b1329; text-decoration: none; font-weight: 700; font-size: 11px; padding: 6px 10px; border-radius: 6px;">
                View Chargers & Book ⚡
              </a>
            </div>
          `,
        });

        marker.addListener('click', () => {
          if (onSelectStation) onSelectStation(st);
          infoWindow.open(mapInstanceRef.current, marker);
        });

        markersRef.current.push(marker);
      });
    } catch (e) {
      console.error("Google maps initialization error", e);
    }
  }, [mapEngine, googleMapsLoaded, stations, selectedStation, onSelectStation]);

  const leafletCenter = [centerLat, centerLng];

  return (
    <div className="relative w-full h-[560px] rounded-3xl overflow-hidden border border-navy-700/80 bg-[#090f1d] shadow-[0_20px_50px_rgba(0,0,0,0.8)]">
      {/* Map Switcher Header Bar */}
      <div className="absolute top-4 right-4 z-[1000] flex items-center gap-1.5 p-1.5 bg-[#060a14]/90 backdrop-blur-md rounded-2xl border border-navy-700/80 shadow-2xl">
        <button
          onClick={() => setMapEngine('leaflet')}
          className={`py-1.5 px-3.5 rounded-xl text-xs font-bold flex items-center gap-2 transition-all ${
            mapEngine === 'leaflet'
              ? 'bg-gradient-to-r from-evgreen-500 to-emerald-600 text-navy-950 shadow-glow-green'
              : 'text-slate-400 hover:text-white hover:bg-navy-800/60'
          }`}
        >
          <Layers className="w-3.5 h-3.5" /> High-Res Map
        </button>

        <button
          onClick={() => setMapEngine('google')}
          className={`py-1.5 px-3.5 rounded-xl text-xs font-bold flex items-center gap-2 transition-all ${
            mapEngine === 'google'
              ? 'bg-gradient-to-r from-evcyan-500 to-blue-600 text-white shadow-glow-cyan'
              : 'text-slate-400 hover:text-white hover:bg-navy-800/60'
          }`}
        >
          <Globe className="w-3.5 h-3.5" /> Google Satellite
        </button>
      </div>

      {/* Map Stats Quick HUD in Top-Left */}
      <div className="absolute top-4 left-4 z-[1000] hidden sm:flex items-center gap-2 py-1.5 px-3.5 bg-[#060a14]/85 backdrop-blur-md rounded-2xl border border-navy-700/80 shadow-lg text-xs font-medium text-slate-300">
        <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        <span>{stations.length} Active Hubs</span>
        <span className="text-navy-600">•</span>
        <span className="text-emerald-400 font-semibold">
          {stations.reduce((acc, s) => acc + (s.available_chargers || 0), 0)} Ports Ready
        </span>
      </div>

      {/* Render Google Maps Engine */}
      {mapEngine === 'google' && (
        <div className="w-full h-full relative bg-[#090f1d]">
          <div ref={googleMapRef} className="w-full h-full" />
          {!googleMapsLoaded && !googleMapsError && (
            <div className="absolute inset-0 bg-[#090f1d] flex flex-col items-center justify-center gap-3">
              <div className="w-9 h-9 border-3 border-evgreen-500 border-t-transparent rounded-full animate-spin"></div>
              <span className="text-xs text-slate-400 font-medium">Connecting Google Maps Telemetry...</span>
            </div>
          )}
        </div>
      )}

      {/* Render Leaflet OpenStreetMap Engine */}
      {mapEngine === 'leaflet' && (
        <div className="w-full h-full relative bg-[#090f1d]">
          <MapContainer
            center={leafletCenter}
            zoom={9}
            scrollWheelZoom={true}
            style={{ width: '100%', height: '100%', background: '#090f1d' }}
          >
            <ChangeMapView center={leafletCenter} stations={stations} selectedStation={selectedStation} />
            <TileLayer
              attribution='&copy; <a href="https://carto.com/">CartoDB</a>'
              url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"
            />

            {stations.map((station) => {
              const isSelected = selectedStation?.id === station.id;
              return (
                <Marker
                  key={station.id}
                  position={[station.latitude, station.longitude]}
                  icon={createCustomIcon(station.available_chargers, isSelected)}
                  eventHandlers={{
                    click: () => onSelectStation && onSelectStation(station),
                  }}
                >
                  <Popup className="custom-dark-popup">
                    <div style={{ color: '#0f172a', padding: '6px 2px', minWidth: '220px', fontFamily: 'Inter, sans-serif' }}>
                      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '4px' }}>
                        <span style={{ fontSize: '10px', fontWeight: '800', textTransform: 'uppercase', color: station.available_chargers > 0 ? '#059669' : '#d97706', letterSpacing: '0.05em' }}>
                          ● {station.available_chargers > 0 ? `${station.available_chargers} Available` : 'Full'}
                        </span>
                        <span style={{ fontSize: '11px', fontWeight: '700', color: '#0f172a' }}>
                          ₹{station.min_price?.toFixed(2) || '15.00'}/kWh
                        </span>
                      </div>
                      
                      <h4 style={{ fontWeight: '800', margin: '0 0 3px 0', fontSize: '14px', color: '#0b1329', lineHeight: '1.2' }}>
                        {station.name}
                      </h4>
                      <p style={{ margin: '0 0 10px 0', fontSize: '11px', color: '#64748b', lineHeight: '1.4' }}>
                        {station.address}
                      </p>

                      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '6px 8px', background: '#f1f5f9', borderRadius: '8px', marginBottom: '10px', fontSize: '11px' }}>
                        <span style={{ color: '#475569' }}>Total Chargers:</span>
                        <strong style={{ color: '#0f172a' }}>{station.total_chargers} Fast Ports</strong>
                      </div>

                      <button
                        onClick={() => navigate(`/stations/${station.id}`)}
                        style={{
                          width: '100%',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          gap: '6px',
                          background: '#10b981',
                          color: '#060a14',
                          border: 'none',
                          borderRadius: '8px',
                          padding: '8px 12px',
                          fontWeight: '800',
                          fontSize: '12px',
                          cursor: 'pointer',
                          boxShadow: '0 2px 8px rgba(16, 185, 129, 0.4)',
                        }}
                      >
                        ⚡ View Chargers & Book
                      </button>
                    </div>
                  </Popup>
                </Marker>
              );
            })}
          </MapContainer>
        </div>
      )}
    </div>
  );
};
