import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { NotificationProvider } from './context/NotificationContext';
import { ProtectedRoute } from './components/ProtectedRoute';
import { Navbar } from './components/Navbar';

// Pages
import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { Dashboard } from './pages/Dashboard';
import { StationsSearch } from './pages/StationsSearch';
import { StationDetail } from './pages/StationDetail';
import { Bookings } from './pages/Bookings';
import { ActiveSession } from './pages/ActiveSession';
import { Payments } from './pages/Payments';
import { Vehicles } from './pages/Vehicles';
import { AdminDashboard } from './pages/AdminDashboard';
import { TeslaBackground } from './components/TeslaBackground';

const AppLayout = ({ children }) => {
  return (
    <div className="min-h-screen flex flex-col bg-navy-950 text-slate-100 font-sans relative overflow-x-hidden">
      <TeslaBackground />
      <Navbar />
      <main className="relative z-10 flex-1 pb-16">{children}</main>
      <footer className="relative z-10 glass-nav py-6 border-t border-navy-800 text-center text-xs text-slate-500">
        EVCSMS &copy; 2026 • EV Charging Station Management System • Object-Oriented Software Design
      </footer>
    </div>
  );
};

export const App = () => {
  return (
    <AuthProvider>
      <NotificationProvider>
        <Router>
          <Routes>
            {/* Public routes */}
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />

            {/* Protected EV Owner & Common routes */}
            <Route
              path="/dashboard"
              element={
                <ProtectedRoute>
                  <AppLayout>
                    <Dashboard />
                  </AppLayout>
                </ProtectedRoute>
              }
            />

            <Route
              path="/stations"
              element={
                <ProtectedRoute>
                  <AppLayout>
                    <StationsSearch />
                  </AppLayout>
                </ProtectedRoute>
              }
            />

            <Route
              path="/stations/:id"
              element={
                <ProtectedRoute>
                  <AppLayout>
                    <StationDetail />
                  </AppLayout>
                </ProtectedRoute>
              }
            />

            <Route
              path="/bookings"
              element={
                <ProtectedRoute>
                  <AppLayout>
                    <Bookings />
                  </AppLayout>
                </ProtectedRoute>
              }
            />

            <Route
              path="/session/active"
              element={
                <ProtectedRoute>
                  <AppLayout>
                    <ActiveSession />
                  </AppLayout>
                </ProtectedRoute>
              }
            />

            <Route
              path="/payments"
              element={
                <ProtectedRoute>
                  <AppLayout>
                    <Payments />
                  </AppLayout>
                </ProtectedRoute>
              }
            />

            <Route
              path="/vehicles"
              element={
                <ProtectedRoute>
                  <AppLayout>
                    <Vehicles />
                  </AppLayout>
                </ProtectedRoute>
              }
            />

            {/* Admin only route */}
            <Route
              path="/admin"
              element={
                <ProtectedRoute requiredRole="ADMIN">
                  <AppLayout>
                    <AdminDashboard />
                  </AppLayout>
                </ProtectedRoute>
              }
            />

            {/* Fallback */}
            <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </Routes>
        </Router>
      </NotificationProvider>
    </AuthProvider>
  );
};

export default App;
