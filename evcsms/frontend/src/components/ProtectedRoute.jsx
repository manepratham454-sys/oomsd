import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export const ProtectedRoute = ({ children, requiredRole }) => {
  const { user, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div className="min-h-screen bg-navy-950 flex items-center justify-center">
        <div className="flex flex-col items-center gap-3">
          <div className="w-10 h-10 border-4 border-evgreen-500 border-t-transparent rounded-full animate-spin"></div>
          <span className="text-slate-400 text-sm">Authenticating session...</span>
        </div>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  if (requiredRole && user.role !== requiredRole) {
    return (
      <div className="min-h-[80vh] flex items-center justify-center p-6">
        <div className="glass-panel p-8 rounded-2xl max-w-md text-center">
          <div className="w-16 h-16 mx-auto mb-4 bg-red-500/20 text-red-400 rounded-full flex items-center justify-center text-2xl font-bold">
            !
          </div>
          <h2 className="text-xl font-bold text-white mb-2">Access Restricted</h2>
          <p className="text-slate-400 text-sm mb-6">
            You require the <span className="text-evgreen-400 font-semibold">{requiredRole}</span> role to access this area.
          </p>
          <Navigate to="/dashboard" replace />
        </div>
      </div>
    );
  }

  return children;
};
