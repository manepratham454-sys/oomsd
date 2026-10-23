import React, { createContext, useContext, useState, useEffect } from 'react';
import apiClient from '../api/client';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('evcsms_token'));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initializeAuth = async () => {
      const storedToken = localStorage.getItem('evcsms_token');
      const storedUser = localStorage.getItem('evcsms_user');

      if (storedToken && storedUser) {
        try {
          setUser(JSON.parse(storedUser));
          setToken(storedToken);
          // Verify with /auth/me
          const res = await apiClient.get('/auth/me');
          setUser(res.data);
          localStorage.setItem('evcsms_user', JSON.stringify(res.data));
        } catch (err) {
          console.error("Token verification failed:", err);
          logout();
        }
      }
      setLoading(false);
    };

    initializeAuth();
  }, []);

  const login = async (email, password) => {
    const res = await apiClient.post('/auth/login', { email, password });
    const { access_token, role, user_id, name, email: userEmail } = res.data;

    const userData = { id: user_id, name, email: userEmail, role };
    setToken(access_token);
    setUser(userData);

    localStorage.setItem('evcsms_token', access_token);
    localStorage.setItem('evcsms_user', JSON.stringify(userData));
    return userData;
  };

  const register = async (name, email, password, phone_no, role = 'EV_OWNER') => {
    const res = await apiClient.post('/auth/register', {
      name,
      email,
      password,
      phone_no,
      role,
    });
    // Auto-login after registration
    return await login(email, password);
  };

  const logout = () => {
    localStorage.removeItem('evcsms_token');
    localStorage.removeItem('evcsms_user');
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, role: user?.role, login, register, logout, loading, isAuthenticated: !!user }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
