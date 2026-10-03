import React, { useState } from 'react';
import { ObservedFact } from '../types';
import { Clock, FileText, ArrowRight, Terminal, HardDrive, CheckCircle } from 'lucide-react';

interface TimelineViewProps {
  facts: ObservedFact[];
  onSelectEvent?: (eventId: string) => void;
}

export const TimelineView: React.FC<TimelineViewProps> = ({ facts, onSelectEvent }) => {
  const [selectedEventId, setSelectedEventId] = useState<string | null>(null);

  const getEventBadgeClass = (type: string) => {
    switch (type) {
      case 'FILE_CREATED':
        return 'badge-fact';
      case 'FILE_MODIFIED':
        return 'badge-inference';
      case 'FILE_MOVED':
      case 'FILE_RENAMED':
        return 'badge-hypothesis';
      case 'FILE_DELETED':
        return 'badge-conflict';
      case 'PROCESS_STARTED':
        return 'badge-anomaly';
      default:
        return 'badge-baseline';
    }
  };

  const getEventIcon = (type: string) => {
    if (type.includes('PROCESS')) return <Terminal size={14} />;
    if (type.includes('DELETED')) return <HardDrive size={14} />;
    return <FileText size={14} />;
  };

  const sorted = [...facts].sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime());

  return (
    <div className="card" style={{ marginTop: '1.5rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.25rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
          <Clock size={18} color="#38BDF8" />
          <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#FFFFFF' }}>
            Interactive Activity Timeline ({sorted.length} Events)
          </h3>
        </div>
        <span style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>
          Chronological sequence with inter-event time deltas
        </span>
      </div>

      <div style={{ position: 'relative', paddingLeft: '1.5rem' }}>
        {/* Vertical timeline spine */}
        <div
          style={{
            position: 'absolute',
            left: '7px',
            top: '8px',
            bottom: '8px',
            width: '2px',
            background: 'linear-gradient(to bottom, #38BDF8, #6366F1, #A855F7)',
          }}
        />

        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {sorted.map((fact, idx) => {
            const currentDate = new Date(fact.timestamp);
            let deltaSeconds = 0;
            if (idx > 0) {
              const prevDate = new Date(sorted[idx - 1].timestamp);
              deltaSeconds = Math.round((currentDate.getTime() - prevDate.getTime()) / 1000);
            }
            const isSelected = selectedEventId === fact.event_id;

            return (
              <div
                key={fact.id}
                onClick={() => {
                  setSelectedEventId(isSelected ? null : fact.event_id);
                  if (onSelectEvent) onSelectEvent(fact.event_id);
                }}
                style={{
                  position: 'relative',
                  cursor: 'pointer',
                  background: isSelected ? 'rgba(56, 189, 248, 0.08)' : 'rgba(255, 255, 255, 0.02)',
                  border: isSelected ? '1px solid #38BDF8' : '1px solid var(--border-subtle)',
                  borderRadius: '0.6rem',
                  padding: '0.75rem 1rem',
                  transition: 'all 0.2s ease',
                }}
              >
                {/* Node node dot on spine */}
                <div
                  style={{
                    position: 'absolute',
                    left: '-1.85rem',
                    top: '1rem',
                    width: '12px',
                    height: '12px',
                    borderRadius: '50%',
                    background: isSelected ? '#38BDF8' : '#1E293B',
                    border: '2px solid #38BDF8',
                    boxShadow: isSelected ? '0 0 10px #38BDF8' : 'none',
                  }}
                />

                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.35rem' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                    <span className={`badge ${getEventBadgeClass(fact.event_type)}`}>
                      {getEventIcon(fact.event_type)} {fact.event_type.replace('FILE_', '')}
                    </span>
                    <span className="font-mono" style={{ fontSize: '0.75rem', color: '#FFFFFF', fontWeight: 600 }}>
                      {fact.file_name}
                    </span>
                  </div>

                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                    {idx > 0 && (
                      <span
                        className="badge"
                        style={{
                          background: 'rgba(255, 255, 255, 0.06)',
                          color: 'var(--text-muted)',
                          fontSize: '0.68rem',
                          fontFamily: 'var(--font-mono)',
                        }}
                      >
                        +{deltaSeconds}s
                      </span>
                    )}
                    <span className="font-mono" style={{ fontSize: '0.72rem', color: 'var(--text-dim)' }}>
                      {currentDate.toISOString().replace('T', ' ').substring(11, 19)} UTC
                    </span>
                  </div>
                </div>

                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.3rem' }}>
                  {fact.statement}
                </div>

                <div style={{ display: 'flex', gap: '1rem', fontSize: '0.72rem', color: 'var(--text-dim)', fontFamily: 'var(--font-mono)' }}>
                  <span>Path: {fact.path}</span>
                  {fact.file_size > 0 && <span>Size: {fact.file_size.toLocaleString()} B</span>}
                  {fact.process_name && <span>Process: {fact.process_name}</span>}
                  <span style={{ color: '#38BDF8' }}>ID: {fact.event_id}</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
