import React from 'react';
import { ShieldCheck, HelpCircle } from 'lucide-react';

interface ConfidenceMeterProps {
  score: number;
  label: 'HIGH' | 'MEDIUM' | 'LOW';
}

export const ConfidenceMeter: React.FC<ConfidenceMeterProps> = ({ score, label }) => {
  const percentage = Math.round(score * 100);

  const getColor = () => {
    if (label === 'HIGH') return '#10B981';
    if (label === 'MEDIUM') return '#F59E0B';
    return '#EF4444';
  };

  return (
    <div
      style={{
        background: 'rgba(255, 255, 255, 0.03)',
        border: '1px solid var(--border-subtle)',
        borderRadius: '0.65rem',
        padding: '0.85rem 1.15rem',
        display: 'flex',
        alignItems: 'center',
        gap: '1rem',
      }}
    >
      <div style={{ position: 'relative', width: '48px', height: '48px' }}>
        <svg width="48" height="48" viewBox="0 0 36 36">
          <path
            d="M18 2.0845
              a 15.9155 15.9155 0 0 1 0 31.831
              a 15.9155 15.9155 0 0 1 0 -31.831"
            fill="none"
            stroke="rgba(255, 255, 255, 0.1)"
            strokeWidth="3.5"
          />
          <path
            d="M18 2.0845
              a 15.9155 15.9155 0 0 1 0 31.831
              a 15.9155 15.9155 0 0 1 0 -31.831"
            fill="none"
            stroke={getColor()}
            strokeWidth="3.5"
            strokeDasharray={`${percentage}, 100`}
            strokeLinecap="round"
          />
        </svg>
        <div
          style={{
            position: 'absolute',
            inset: 0,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '0.75rem',
            fontWeight: 800,
            fontFamily: 'var(--font-mono)',
            color: '#FFFFFF',
          }}
        >
          {percentage}%
        </div>
      </div>

      <div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', marginBottom: '0.15rem' }}>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-dim)', fontWeight: 600 }}>EVIDENCE CONFIDENCE</span>
          <span
            className="badge"
            style={{
              background: `${getColor()}20`,
              color: getColor(),
              border: `1px solid ${getColor()}40`,
              fontSize: '0.65rem',
            }}
          >
            {label}
          </span>
        </div>
        <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', lineHeight: 1.3 }}>
          Calibrated metric accounting for temporal continuity, filename similarity, and missing telemetry penalties.
        </div>
      </div>
    </div>
  );
};
