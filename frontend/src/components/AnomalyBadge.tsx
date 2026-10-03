import React from 'react';
import { AlertCircle, CheckCircle, HelpCircle } from 'lucide-react';

interface AnomalyBadgeProps {
  isAnomaly: boolean;
  score: number;
}

export const AnomalyBadge: React.FC<AnomalyBadgeProps> = ({ isAnomaly, score }) => {
  return (
    <div
      style={{
        background: 'rgba(255, 255, 255, 0.03)',
        border: '1px solid var(--border-subtle)',
        borderRadius: '0.65rem',
        padding: '0.85rem 1.15rem',
        display: 'flex',
        alignItems: 'center',
        gap: '0.85rem',
      }}
    >
      <div
        style={{
          width: '36px',
          height: '36px',
          borderRadius: '50%',
          background: isAnomaly ? 'rgba(249, 115, 22, 0.15)' : 'rgba(16, 185, 129, 0.15)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: isAnomaly ? '#FB923C' : '#34D399',
        }}
      >
        {isAnomaly ? <AlertCircle size={20} /> : <CheckCircle size={20} />}
      </div>

      <div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.15rem' }}>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-dim)', fontWeight: 600 }}>BEHAVIORAL CADENCE</span>
          <span className={`badge ${isAnomaly ? 'badge-anomaly' : 'badge-baseline'}`} style={{ fontSize: '0.65rem' }}>
            {isAnomaly ? `ANOMALOUS (${(score * 100).toFixed(0)}%)` : `BASELINE (${(score * 100).toFixed(0)}%)`}
          </span>
        </div>
        <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', lineHeight: 1.3 }}>
          {isAnomaly
            ? 'Activity diverges from learned operating baseline. (Note: Anomaly denotes statistical novelty, not confirmed malice).'
            : 'Activity frequency, volume, and lifecycle transitions conform with baseline patterns.'}
        </div>
      </div>
    </div>
  );
};
