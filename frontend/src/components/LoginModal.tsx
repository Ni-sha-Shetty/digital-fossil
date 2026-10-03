import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { UserRole } from '../types';
import { Compass, ShieldCheck, Lock, AlertTriangle, ArrowRight, User } from 'lucide-react';

export const LoginModal: React.FC = () => {
  const { login, quickDemoLogin, loading, error, clearError } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleManualSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password) return;
    try {
      await login(email, password);
    } catch {
      // error handled in context
    }
  };

  const handleQuickLogin = async (role: UserRole) => {
    clearError();
    await quickDemoLogin(role);
  };

  return (
    <div
      style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'radial-gradient(circle at 50% 20%, #172554 0%, #080C14 70%)',
        padding: '2rem 1rem',
      }}
    >
      <div
        style={{
          width: '100%',
          maxWidth: '520px',
          background: 'rgba(14, 22, 38, 0.95)',
          backdropFilter: 'blur(20px)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
          borderRadius: '1.25rem',
          padding: '2.5rem',
          boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.7)',
        }}
      >
        {/* Header Branding */}
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <div
            style={{
              width: '56px',
              height: '56px',
              borderRadius: '14px',
              background: 'linear-gradient(135deg, #0EA5E9, #6366F1)',
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: '0 0 30px rgba(56, 189, 248, 0.5)',
              marginBottom: '1rem',
            }}
          >
            <Compass size={32} color="#FFFFFF" />
          </div>
          <h1 style={{ fontSize: '1.85rem', fontWeight: 800, color: '#FFFFFF', letterSpacing: '-0.03em' }}>
            DIGITAL FOSSIL
          </h1>
          <p style={{ color: '#38BDF8', fontSize: '0.88rem', fontWeight: 600, marginTop: '0.25rem' }}>
            Explainable Digital Activity Reconstruction Engine
          </p>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.82rem', marginTop: '0.5rem', lineHeight: 1.4 }}>
            "Don't just show what happened. Reconstruct what likely happened — and prove why."
          </p>
        </div>

        {/* Core Epistemic Proposition Banner */}
        <div
          style={{
            background: 'rgba(16, 185, 129, 0.08)',
            border: '1px solid rgba(16, 185, 129, 0.25)',
            borderRadius: '0.75rem',
            padding: '0.75rem 1rem',
            marginBottom: '1.5rem',
            fontSize: '0.78rem',
            color: '#A7F3D0',
            lineHeight: 1.45,
          }}
        >
          <strong>Scientific Principle:</strong> Correlates digital artifacts into activity timelines while strictly separating confirmed facts, derived inferences, and testable hypotheses.
        </div>

        {error && (
          <div
            style={{
              background: 'rgba(239, 68, 68, 0.15)',
              border: '1px solid rgba(239, 68, 68, 0.4)',
              borderRadius: '0.5rem',
              padding: '0.65rem 0.9rem',
              marginBottom: '1.25rem',
              fontSize: '0.82rem',
              color: '#FCA5A5',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
            }}
          >
            <AlertTriangle size={16} />
            <span>{error}</span>
          </div>
        )}

        {/* 1-Click Demo Login Shortcuts */}
        <div style={{ marginBottom: '1.75rem' }}>
          <label style={{ display: 'block', fontSize: '0.75rem', fontWeight: 700, color: 'var(--text-dim)', marginBottom: '0.6rem', textTransform: 'uppercase' }}>
            Instant Demo Access (Click to Authenticate)
          </label>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '0.6rem' }}>
            <button
              type="button"
              className="btn btn-secondary"
              style={{ flexDirection: 'column', padding: '0.75rem 0.5rem', textAlign: 'center', border: '1px solid rgba(16, 185, 129, 0.4)' }}
              onClick={() => handleQuickLogin('investigator')}
              disabled={loading}
            >
              <span className="badge badge-fact" style={{ fontSize: '0.65rem', marginBottom: '0.2rem' }}>Investigator</span>
              <span style={{ fontSize: '0.75rem', color: '#FFFFFF', fontWeight: 600 }}>Alex Vance</span>
            </button>

            <button
              type="button"
              className="btn btn-secondary"
              style={{ flexDirection: 'column', padding: '0.75rem 0.5rem', textAlign: 'center', border: '1px solid rgba(56, 189, 248, 0.4)' }}
              onClick={() => handleQuickLogin('reviewer')}
              disabled={loading}
            >
              <span className="badge badge-inference" style={{ fontSize: '0.65rem', marginBottom: '0.2rem' }}>Reviewer</span>
              <span style={{ fontSize: '0.75rem', color: '#FFFFFF', fontWeight: 600 }}>Morgan Reed</span>
            </button>

            <button
              type="button"
              className="btn btn-secondary"
              style={{ flexDirection: 'column', padding: '0.75rem 0.5rem', textAlign: 'center', border: '1px solid rgba(192, 132, 252, 0.4)' }}
              onClick={() => handleQuickLogin('admin')}
              disabled={loading}
            >
              <span className="badge badge-hypothesis" style={{ fontSize: '0.65rem', marginBottom: '0.2rem' }}>Admin</span>
              <span style={{ fontSize: '0.75rem', color: '#FFFFFF', fontWeight: 600 }}>Jordan Croft</span>
            </button>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', margin: '1.25rem 0', gap: '0.75rem' }}>
          <div style={{ flex: 1, height: '1px', background: 'var(--border-subtle)' }} />
          <span style={{ fontSize: '0.75rem', color: 'var(--text-dim)', fontWeight: 600 }}>OR MANUAL CREDENTIALS</span>
          <div style={{ flex: 1, height: '1px', background: 'var(--border-subtle)' }} />
        </div>

        {/* Manual Login Form */}
        <form onSubmit={handleManualSubmit}>
          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.35rem' }}>
              Email Address
            </label>
            <div style={{ position: 'relative' }}>
              <input
                type="text"
                className="input-field"
                placeholder="investigator@digitalfossil.local"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
          </div>

          <div style={{ marginBottom: '1.5rem' }}>
            <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.35rem' }}>
              Password
            </label>
            <div style={{ position: 'relative' }}>
              <input
                type="password"
                className="input-field"
                placeholder="••••••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
          </div>

          <button
            type="submit"
            className="btn btn-primary"
            style={{ width: '100%', padding: '0.75rem' }}
            disabled={loading}
          >
            {loading ? 'Authenticating...' : 'Sign In to Investigation Workspace'} <ArrowRight size={16} />
          </button>
        </form>

        {/* Privacy Notice */}
        <div
          style={{
            marginTop: '2rem',
            paddingTop: '1.25rem',
            borderTop: '1px solid var(--border-subtle)',
            fontSize: '0.73rem',
            color: 'var(--text-dim)',
            lineHeight: 1.45,
            textAlign: 'center',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.4rem', color: 'var(--text-muted)', marginBottom: '0.3rem', fontWeight: 600 }}>
            <ShieldCheck size={14} color="#10B981" /> Defensive Research Privacy Notice
          </div>
          Local-first architecture. Monitoring is limited strictly to user-authorized test directories. No keystrokes, passwords, private contents, or covert background surveillance.
        </div>
      </div>
    </div>
  );
};
