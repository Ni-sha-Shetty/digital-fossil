import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { SystemStats, User, ThresholdConfig, AuditLogItem } from '../types';
import { CollectorControl } from './CollectorControl';
import {
  Settings,
  Users,
  Sliders,
  History,
  RotateCcw,
  CheckCircle2,
  HardDrive,
  Activity,
  AlertTriangle,
  UserPlus
} from 'lucide-react';

export const AdminDashboard: React.FC = () => {
  const [stats, setStats] = useState<SystemStats | null>(null);
  const [users, setUsers] = useState<User[]>([]);
  const [thresholds, setThresholds] = useState<ThresholdConfig | null>(null);
  const [auditLogs, setAuditLogs] = useState<AuditLogItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [savingThresholds, setSavingThresholds] = useState(false);
  const [resettingDemo, setResettingDemo] = useState(false);
  const [statusMsg, setStatusMsg] = useState<string | null>(null);

  // Form for threshold editing
  const [sessionTh, setSessionTh] = useState(120);
  const [minRel, setMinRel] = useState(0.35);
  const [anomTh, setAnomTh] = useState(0.10);

  // Form for user creation
  const [newEmail, setNewEmail] = useState('');
  const [newPass, setNewPass] = useState('');
  const [newName, setNewName] = useState('');
  const [newRole, setNewRole] = useState<'investigator' | 'reviewer' | 'admin'>('investigator');

  const loadData = async () => {
    try {
      const [sData, uData, tData, aData] = await Promise.all([
        api.getSystemStats(),
        api.getUsers(),
        api.getThresholds(),
        api.getAuditLogs({ limit: 50 }),
      ]);
      setStats(sData);
      setUsers(uData);
      setThresholds(tData);
      setSessionTh(tData.session_threshold_sec);
      setMinRel(tData.min_relationship_score);
      setAnomTh(tData.anomaly_threshold);
      setAuditLogs(aData.logs);
    } catch (e) {
      console.error('Failed to load admin data', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleSaveThresholds = async (e: React.FormEvent) => {
    e.preventDefault();
    setSavingThresholds(true);
    setStatusMsg(null);
    try {
      const updated = await api.updateThresholds({
        session_threshold_sec: sessionTh,
        min_relationship_score: minRel,
        anomaly_threshold: anomTh,
      });
      setThresholds(updated);
      setStatusMsg('Analysis thresholds updated successfully and logged in audit trail.');
      await loadData();
    } catch (err: any) {
      setStatusMsg(`Error: ${err.message}`);
    } finally {
      setSavingThresholds(false);
    }
  };

  const handleCreateUser = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.createUser({
        email: newEmail,
        password: newPass,
        full_name: newName,
        role: newRole,
      });
      setNewEmail('');
      setNewPass('');
      setNewName('');
      setStatusMsg('New system user created successfully.');
      await loadData();
    } catch (err: any) {
      setStatusMsg(`Error creating user: ${err.message}`);
    }
  };

  const handleResetDemoData = async () => {
    if (!window.confirm('Reset all demo investigations and reload standard benchmark scenarios?')) return;
    setResettingDemo(true);
    setStatusMsg(null);
    try {
      const res = await api.resetDemoData();
      setStatusMsg(res.message);
      await loadData();
    } catch (err: any) {
      setStatusMsg(`Error resetting demo data: ${err.message}`);
    } finally {
      setResettingDemo(false);
    }
  };

  if (loading) {
    return <div style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-muted)' }}>Loading Administration Panel...</div>;
  }

  return (
    <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '1.5rem' }}>
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem' }}>
        <div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: '#FFFFFF', display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <Settings size={24} color="#C084FC" /> System Administration & Governance
          </h2>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '0.2rem' }}>
            Telemetry thresholds, role authorization, watchdog folder monitoring, and immutable audit logs.
          </p>
        </div>

        <button
          className="btn btn-secondary"
          onClick={handleResetDemoData}
          disabled={resettingDemo}
          style={{ borderColor: 'rgba(239, 68, 68, 0.4)' }}
        >
          <RotateCcw size={15} color="#F87171" className={resettingDemo ? 'animate-spin' : ''} />
          {resettingDemo ? 'Re-seeding Scenarios...' : 'Reset Benchmark Datasets'}
        </button>
      </div>

      {statusMsg && (
        <div
          style={{
            background: 'rgba(56, 189, 248, 0.1)',
            border: '1px solid rgba(56, 189, 248, 0.3)',
            borderRadius: '0.5rem',
            padding: '0.75rem 1rem',
            fontSize: '0.82rem',
            color: '#38BDF8',
            marginBottom: '1.5rem',
          }}
        >
          {statusMsg}
        </div>
      )}

      {/* Top Stats Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1rem', marginBottom: '1.5rem' }}>
        <div className="card">
          <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)', marginBottom: '0.2rem' }}>TOTAL EVENTS STORED</div>
          <div style={{ fontSize: '1.6rem', fontWeight: 800, color: '#FFFFFF', fontFamily: 'var(--font-mono)' }}>
            {stats?.total_events}
          </div>
          <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginTop: '0.2rem' }}>Canonical events</div>
        </div>

        <div className="card">
          <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)', marginBottom: '0.2rem' }}>ACTIVE SESSIONS</div>
          <div style={{ fontSize: '1.6rem', fontWeight: 800, color: '#38BDF8', fontFamily: 'var(--font-mono)' }}>
            {stats?.total_sessions}
          </div>
          <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginTop: '0.2rem' }}>
            {stats?.anomalous_sessions} flagged as anomalous
          </div>
        </div>

        <div className="card">
          <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)', marginBottom: '0.2rem' }}>INVESTIGATIONS</div>
          <div style={{ fontSize: '1.6rem', fontWeight: 800, color: '#A855F7', fontFamily: 'var(--font-mono)' }}>
            {stats?.total_investigations}
          </div>
          <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginTop: '0.2rem' }}>
            {stats?.approved_investigations} approved / {stats?.flagged_investigations} flagged
          </div>
        </div>

        <div className="card">
          <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)', marginBottom: '0.2rem' }}>DATABASE HEALTH</div>
          <div style={{ fontSize: '1.2rem', fontWeight: 800, color: '#10B981', fontFamily: 'var(--font-mono)' }}>
            ONLINE
          </div>
          <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginTop: '0.2rem' }}>
            {stats?.database_status}
          </div>
        </div>
      </div>

      {/* Collector Widget */}
      <div style={{ marginBottom: '1.5rem' }}>
        <CollectorControl />
      </div>

      {/* Threshold Configuration & User Management Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '1.5rem', marginBottom: '1.5rem' }}>
        {/* Analysis Threshold Configuration */}
        <div className="card">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '1rem' }}>
            <Sliders size={18} color="#38BDF8" />
            <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#FFFFFF' }}>
              Dynamic Analysis Thresholds
            </h3>
          </div>

          <form onSubmit={handleSaveThresholds}>
            <div style={{ marginBottom: '1.25rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', marginBottom: '0.35rem' }}>
                <span style={{ color: 'var(--text-muted)' }}>Sessionization Gap Threshold:</span>
                <span className="font-mono" style={{ color: '#38BDF8', fontWeight: 700 }}>{sessionTh} seconds</span>
              </div>
              <input
                type="range"
                min="30"
                max="600"
                step="10"
                value={sessionTh}
                onChange={(e) => setSessionTh(parseInt(e.target.value))}
                style={{ width: '100%' }}
              />
              <span style={{ fontSize: '0.7rem', color: 'var(--text-dim)' }}>
                Maximum inter-event delay before splitting into new activity session (default: 120s / 2 min).
              </span>
            </div>

            <div style={{ marginBottom: '1.25rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', marginBottom: '0.35rem' }}>
                <span style={{ color: 'var(--text-muted)' }}>Minimum Relationship Score:</span>
                <span className="font-mono" style={{ color: '#38BDF8', fontWeight: 700 }}>{minRel.toFixed(2)}</span>
              </div>
              <input
                type="range"
                min="0.10"
                max="0.80"
                step="0.05"
                value={minRel}
                onChange={(e) => setMinRel(parseFloat(e.target.value))}
                style={{ width: '100%' }}
              />
              <span style={{ fontSize: '0.7rem', color: 'var(--text-dim)' }}>
                Minimum composite correlation to assert a relationship edge in knowledge graph.
              </span>
            </div>

            <div style={{ marginBottom: '1.5rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', marginBottom: '0.35rem' }}>
                <span style={{ color: 'var(--text-muted)' }}>Anomaly Contamination Rate:</span>
                <span className="font-mono" style={{ color: '#38BDF8', fontWeight: 700 }}>{(anomTh * 100).toFixed(0)}%</span>
              </div>
              <input
                type="range"
                min="0.02"
                max="0.30"
                step="0.01"
                value={anomTh}
                onChange={(e) => setAnomTh(parseFloat(e.target.value))}
                style={{ width: '100%' }}
              />
              <span style={{ fontSize: '0.7rem', color: 'var(--text-dim)' }}>
                Isolation Forest expected anomaly proportion in event distributions.
              </span>
            </div>

            <button type="submit" className="btn btn-primary" disabled={savingThresholds}>
              {savingThresholds ? 'Updating Thresholds...' : 'Save Configuration & Log Audit'}
            </button>
          </form>
        </div>

        {/* User Management */}
        <div className="card">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '1rem' }}>
            <Users size={18} color="#C084FC" />
            <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#FFFFFF' }}>
              User Authorization & Role Management
            </h3>
          </div>

          {/* User List */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', marginBottom: '1.25rem', maxHeight: '180px', overflowY: 'auto' }}>
            {users.map((u) => (
              <div
                key={u.id}
                style={{
                  background: 'rgba(255,255,255,0.02)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: '0.4rem',
                  padding: '0.5rem 0.75rem',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                }}
              >
                <div>
                  <div style={{ fontSize: '0.82rem', fontWeight: 600, color: '#FFFFFF' }}>{u.full_name}</div>
                  <div className="font-mono" style={{ fontSize: '0.7rem', color: 'var(--text-dim)' }}>{u.email}</div>
                </div>
                <span className={`badge ${u.role === 'admin' ? 'badge-hypothesis' : u.role === 'reviewer' ? 'badge-inference' : 'badge-fact'}`}>
                  {u.role.toUpperCase()}
                </span>
              </div>
            ))}
          </div>

          {/* Add User */}
          <form onSubmit={handleCreateUser} style={{ borderTop: '1px solid var(--border-subtle)', paddingTop: '1rem' }}>
            <div style={{ fontSize: '0.78rem', fontWeight: 700, color: 'var(--text-main)', marginBottom: '0.6rem' }}>
              Create New Operator:
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '0.5rem', marginBottom: '0.5rem' }}>
              <input
                type="text"
                className="input-field"
                placeholder="Full Name"
                value={newName}
                onChange={(e) => setNewName(e.target.value)}
                required
              />
              <input
                type="email"
                className="input-field"
                placeholder="Email Address"
                value={newEmail}
                onChange={(e) => setNewEmail(e.target.value)}
                required
              />
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '0.5rem', marginBottom: '0.75rem' }}>
              <input
                type="password"
                className="input-field"
                placeholder="Password"
                value={newPass}
                onChange={(e) => setNewPass(e.target.value)}
                required
              />
              <select
                className="input-field"
                value={newRole}
                onChange={(e: any) => setNewRole(e.target.value)}
              >
                <option value="investigator">Investigator</option>
                <option value="reviewer">Reviewer</option>
                <option value="admin">Administrator</option>
              </select>
            </div>
            <button type="submit" className="btn btn-secondary btn-sm">
              <UserPlus size={14} /> Provision Operator Account
            </button>
          </form>
        </div>
      </div>

      {/* Audit Log Table */}
      <div className="card">
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '1rem' }}>
          <History size={18} color="#F59E0B" />
          <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#FFFFFF' }}>
            System Audit Log & Traceability Records ({auditLogs.length})
          </h3>
        </div>

        <div style={{ overflowX: 'auto', maxHeight: '320px' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.78rem' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid var(--border-medium)', color: 'var(--text-dim)', fontSize: '0.72rem' }}>
                <th style={{ padding: '0.5rem 0.75rem' }}>TIMESTAMP (UTC)</th>
                <th style={{ padding: '0.5rem 0.75rem' }}>OPERATOR</th>
                <th style={{ padding: '0.5rem 0.75rem' }}>ROLE</th>
                <th style={{ padding: '0.5rem 0.75rem' }}>ACTION</th>
                <th style={{ padding: '0.5rem 0.75rem' }}>TARGET</th>
                <th style={{ padding: '0.5rem 0.75rem' }}>METADATA</th>
              </tr>
            </thead>
            <tbody>
              {auditLogs.map((log) => (
                <tr key={log.id} style={{ borderBottom: '1px solid var(--border-subtle)' }}>
                  <td className="font-mono" style={{ padding: '0.5rem 0.75rem', color: 'var(--text-dim)' }}>
                    {new Date(log.timestamp).toISOString().replace('T', ' ').substring(0, 19)}
                  </td>
                  <td style={{ padding: '0.5rem 0.75rem', color: '#FFFFFF' }}>
                    {log.user_email}
                  </td>
                  <td style={{ padding: '0.5rem 0.75rem' }}>
                    <span className="badge badge-baseline" style={{ fontSize: '0.65rem' }}>
                      {log.role}
                    </span>
                  </td>
                  <td style={{ padding: '0.5rem 0.75rem', fontWeight: 700, color: '#38BDF8' }}>
                    {log.action}
                  </td>
                  <td className="font-mono" style={{ padding: '0.5rem 0.75rem', color: 'var(--text-muted)' }}>
                    {log.target}
                  </td>
                  <td className="font-mono" style={{ padding: '0.5rem 0.75rem', color: 'var(--text-dim)', fontSize: '0.7rem' }}>
                    {JSON.stringify(log.metadata)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
