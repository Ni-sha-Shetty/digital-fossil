import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { CollectorStatus } from '../types';
import { Radio, Play, Square, ShieldCheck, Folder } from 'lucide-react';

export const CollectorControl: React.FC = () => {
  const [status, setStatus] = useState<CollectorStatus | null>(null);
  const [dirInput, setDirInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState<string | null>(null);

  const fetchStatus = async () => {
    try {
      const data = await api.getCollectorStatus();
      setStatus(data);
      if (!dirInput) {
        setDirInput(data.monitored_directory);
      }
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 3000);
    return () => clearInterval(interval);
  }, []);

  const handleStart = async () => {
    setLoading(true);
    setMsg(null);
    try {
      const res = await api.startCollector(dirInput);
      setMsg(res.message);
      await fetchStatus();
    } catch (err: any) {
      setMsg(`Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleStop = async () => {
    setLoading(true);
    setMsg(null);
    try {
      const res = await api.stopCollector();
      setMsg(res.message);
      await fetchStatus();
    } catch (err: any) {
      setMsg(`Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
          <Radio size={18} color={status?.is_running ? '#10B981' : '#94A3B8'} />
          <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#FFFFFF' }}>
            Explicit Test Directory Monitor (Watchdog Engine)
          </h3>
        </div>

        <span className={`badge ${status?.is_running ? 'badge-fact' : 'badge-baseline'}`}>
          {status?.is_running ? 'ACTIVE MONITORING' : 'IDLE / STOPPED'}
        </span>
      </div>

      {/* Mandatory Privacy Scope Notice */}
      <div
        style={{
          background: 'rgba(16, 185, 129, 0.08)',
          border: '1px solid rgba(16, 185, 129, 0.25)',
          borderRadius: '0.5rem',
          padding: '0.75rem 1rem',
          marginBottom: '1rem',
          fontSize: '0.78rem',
          color: '#A7F3D0',
          display: 'flex',
          alignItems: 'center',
          gap: '0.6rem',
        }}
      >
        <ShieldCheck size={18} color="#34D399" />
        <span>
          <strong>Strict Privacy Boundary:</strong> Monitoring is strictly limited to the explicitly selected user directory. Captures safe metadata only (file actions, timestamps, extensions, sizes). System surveillance, keystrokes, and credential collection are strictly prohibited.
        </span>
      </div>

      <div style={{ marginBottom: '1rem' }}>
        <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.4rem' }}>
          Target Test Directory Path:
        </label>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <input
            type="text"
            className="input-field font-mono"
            value={dirInput}
            onChange={(e) => setDirInput(e.target.value)}
            disabled={status?.is_running}
            style={{ fontSize: '0.8rem' }}
          />
          {!status?.is_running ? (
            <button className="btn btn-primary" onClick={handleStart} disabled={loading}>
              <Play size={15} /> Start Collector
            </button>
          ) : (
            <button className="btn btn-danger" onClick={handleStop} disabled={loading}>
              <Square size={15} /> Stop Collector
            </button>
          )}
        </div>
      </div>

      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: 'var(--text-dim)' }}>
        <span>Events Captured This Session: <strong style={{ color: '#38BDF8' }}>{status?.events_captured || 0}</strong></span>
        {msg && <span style={{ color: '#FDE047' }}>{msg}</span>}
      </div>
    </div>
  );
};
