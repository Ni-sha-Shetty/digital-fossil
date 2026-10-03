import React, { createContext, useContext, useState, useEffect } from 'react';
import { User, UserRole } from '../types';
import { api } from '../services/api';

interface AuthContextType {
  user: User | null;
  role: UserRole | null;
  token: string | null;
  isAuthenticated: boolean;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  quickDemoLogin: (role: UserRole) => Promise<void>;
  logout: () => void;
  error: string | null;
  clearError: () => void;
}

const DEMO_CREDENTIALS: Record<UserRole, { email: string; pass: string }> = {
  investigator: {
    email: 'investigator@digitalfossil.local',
    pass: 'investigator123',
  },
  reviewer: {
    email: 'reviewer@digitalfossil.local',
    pass: 'reviewer123',
  },
  admin: {
    email: 'admin@digitalfossil.local',
    pass: 'admin123',
  },
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(localStorage.getItem('df_token'));
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadUser() {
      if (token) {
        try {
          const profile = await api.getMe(token);
          setUser(profile);
        } catch (err) {
          console.warn('Session expired, clearing token');
          localStorage.removeItem('df_token');
          setToken(null);
          setUser(null);
        }
      }
      setLoading(false);
    }
    loadUser();
  }, [token]);

  const login = async (email: string, pass: string) => {
    setError(null);
    setLoading(true);
    try {
      const data = await api.login(email, pass);
      localStorage.setItem('df_token', data.access_token);
      setToken(data.access_token);
      const profile = await api.getMe(data.access_token);
      setUser(profile);
    } catch (err: any) {
      setError(err.message || 'Login failed');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const quickDemoLogin = async (targetRole: UserRole) => {
    const creds = DEMO_CREDENTIALS[targetRole];
    if (creds) {
      await login(creds.email, creds.pass);
    }
  };

  const logout = () => {
    localStorage.removeItem('df_token');
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        role: user?.role || null,
        token,
        isAuthenticated: !!user,
        loading,
        login,
        quickDemoLogin,
        logout,
        error,
        clearError: () => setError(null),
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within an AuthProvider');
  return ctx;
};
