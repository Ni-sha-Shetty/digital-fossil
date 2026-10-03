import React from 'react';
import { useAuth } from '../context/AuthContext';
import { UserRole } from '../types';
import { Shield, Activity, UserCheck, Settings, LogOut, Cpu, Compass } from 'lucide-react';

interface NavbarProps {
  currentTab: string;
  setCurrentTab: (tab: string) => void;
}

export const Navbar: React.FC<NavbarProps> = ({ currentTab, setCurrentTab }) => {
  const { user, role, logout, quickDemoLogin } = useAuth();

  const getRoleBadgeClass = (r?: UserRole | null) => {
    switch (r) {
      case 'investigator':
        return 'badge-fact';
      case 'reviewer':
        return 'badge-inference';
      case 'admin':
        return 'badge-hypothesis';
      default:
        return 'badge-baseline';
    }
  };

  return (
    <header
      style={{
        background: 'rgba(14, 22, 38, 0.85)',
        backdropFilter: 'blur(12px)',
        borderBottom: '1px solid var(--border-subtle)',
        position: 'sticky',
        top: 0,
        zIndex: 100,
        padding: '0.75rem 1.5rem',
      }}
    >
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          maxWidth: '1600px',
          margin: '0 auto',
        }}
      >
        {/* Brand */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
          <div
            style={{
              width: '38px',
              height: '38px',
              borderRadius: '8px',
              background: 'linear-gradient(135deg, #0EA5E9, #6366F1)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: '0 0 15px rgba(56, 189, 248, 0.4)',
            }}
          >
            <Compass size={22} color="#FFFFFF" />
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <span style={{ fontWeight: 800, fontSize: '1.15rem', letterSpacing: '-0.02em', color: '#FFFFFF' }}>
                DIGITAL FOSSIL
              </span>
              <span style={{ fontSize: '0.65rem', background: 'rgba(56, 189, 248, 0.15)', color: '#38BDF8', padding: '0.15rem 0.45rem', borderRadius: '4px', fontWeight: 700 }}>
                v1.0 RESEARCH
              </span>
            </div>
            <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>
              Explainable Digital Activity Reconstruction Engine
            </div>
          </div>
        </div>

        {/* Center Nav tabs */}
        <nav style={{ display: 'flex', gap: '0.4rem', background: 'rgba(8, 12, 20, 0.6)', padding: '0.3rem', borderRadius: '0.6rem', border: '1px solid var(--border-subtle)' }}>
          {role === 'investigator' && (
            <>
              <button
                className={`btn btn-sm ${currentTab === 'investigations' ? 'btn-primary' : 'btn-secondary'}`}
                onClick={() => setCurrentTab('investigations')}
              >
                <Activity size={14} /> Investigations
              </button>
              <button
                className={`btn btn-sm ${currentTab === 'ml_metrics' ? 'btn-primary' : 'btn-secondary'}`}
                onClick={() => setCurrentTab('ml_metrics')}
              >
                <Cpu size={14} /> ML Explainability
              </button>
            </>
          )}

          {role === 'reviewer' && (
            <>
              <button
                className={`btn btn-sm ${currentTab === 'reviewer_queue' ? 'btn-primary' : 'btn-secondary'}`}
                onClick={() => setCurrentTab('reviewer_queue')}
              >
                <UserCheck size={14} /> Review Queue
              </button>
              <button
                className={`btn btn-sm ${currentTab === 'investigations' ? 'btn-primary' : 'btn-secondary'}`}
                onClick={() => setCurrentTab('investigations')}
              >
                <Activity size={14} /> All Investigations
              </button>
            </>
          )}

          {role === 'admin' && (
            <>
              <button
                className={`btn btn-sm ${currentTab === 'admin' ? 'btn-primary' : 'btn-secondary'}`}
                onClick={() => setCurrentTab('admin')}
              >
                <Settings size={14} /> System Administration
              </button>
              <button
                className={`btn btn-sm ${currentTab === 'investigations' ? 'btn-primary' : 'btn-secondary'}`}
                onClick={() => setCurrentTab('investigations')}
              >
                <Activity size={14} /> Investigations
              </button>
              <button
                className={`btn btn-sm ${currentTab === 'ml_metrics' ? 'btn-primary' : 'btn-secondary'}`}
                onClick={() => setCurrentTab('ml_metrics')}
              >
                <Cpu size={14} /> ML Models
              </button>
            </>
          )}
        </nav>

        {/* Right side: Role Switcher & User Profile */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          {/* Quick Role Switcher for Hackathon Demonstration */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', background: 'var(--bg-card)', padding: '0.25rem 0.5rem', borderRadius: '6px', border: '1px solid var(--border-subtle)' }}>
            <span style={{ fontSize: '0.7rem', color: 'var(--text-dim)', fontWeight: 600 }}>SWITCH ROLE:</span>
            {(['investigator', 'reviewer', 'admin'] as UserRole[]).map((r) => (
              <button
                key={r}
                onClick={() => {
                  quickDemoLogin(r);
                  if (r === 'admin') setCurrentTab('admin');
                  else if (r === 'reviewer') setCurrentTab('reviewer_queue');
                  else setCurrentTab('investigations');
                }}
                style={{
                  background: role === r ? 'rgba(56, 189, 248, 0.2)' : 'transparent',
                  color: role === r ? '#38BDF8' : 'var(--text-muted)',
                  border: role === r ? '1px solid rgba(56, 189, 248, 0.4)' : '1px solid transparent',
                  padding: '0.15rem 0.45rem',
                  borderRadius: '4px',
                  fontSize: '0.7rem',
                  fontWeight: 700,
                  cursor: 'pointer',
                  textTransform: 'uppercase',
                }}
              >
                {r}
              </button>
            ))}
          </div>

          {/* Current Active Role Badge */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <span className={`badge ${getRoleBadgeClass(role)}`}>
              <Shield size={12} /> {role}
            </span>
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end' }}>
              <span style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-main)' }}>
                {user?.full_name}
              </span>
              <span style={{ fontSize: '0.68rem', color: 'var(--text-dim)', fontFamily: 'var(--font-mono)' }}>
                {user?.email}
              </span>
            </div>
            <button
              onClick={logout}
              title="Sign Out"
              style={{
                background: 'rgba(239, 68, 68, 0.12)',
                border: '1px solid rgba(239, 68, 68, 0.25)',
                color: '#F87171',
                borderRadius: '6px',
                padding: '0.4rem',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
              }}
            >
              <LogOut size={15} />
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};
