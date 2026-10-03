import React, { useState } from 'react';
import { EventItem } from '../types';
import { Search, Database, HardDrive, Terminal } from 'lucide-react';

interface EvidenceTableProps {
  events: EventItem[];
  highlightId?: string | null;
}

export const EvidenceTable: React.FC<EvidenceTableProps> = ({ events, highlightId }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [typeFilter, setTypeFilter] = useState('ALL');

  const filtered = events.filter((e) => {
    const matchesSearch =
      e.file_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      e.event_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
      e.path.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesType = typeFilter === 'ALL' || e.event_type === typeFilter;
    return matchesSearch && matchesType;
  });

  return (
    <div className="card" style={{ marginTop: '1.5rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
          <Database size={18} color="#38BDF8" />
          <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#FFFFFF' }}>
            Telemetry Evidence Ledger ({events.length} Records)
          </h3>
        </div>

        {/* Search and Filters */}
        <div style={{ display: 'flex', gap: '0.6rem' }}>
          <div style={{ position: 'relative', width: '220px' }}>
            <input
              type="text"
              className="input-field"
              placeholder="Search filename or ID..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={{ paddingLeft: '2rem', fontSize: '0.78rem' }}
            />
            <Search size={14} color="var(--text-dim)" style={{ position: 'absolute', left: '0.6rem', top: '0.65rem' }} />
          </div>

          <select
            className="input-field"
            value={typeFilter}
            onChange={(e) => setTypeFilter(e.target.value)}
            style={{ width: '150px', fontSize: '0.78rem' }}
          >
            <option value="ALL">All Event Types</option>
            <option value="FILE_CREATED">FILE_CREATED</option>
            <option value="FILE_MODIFIED">FILE_MODIFIED</option>
            <option value="FILE_MOVED">FILE_MOVED</option>
            <option value="FILE_RENAMED">FILE_RENAMED</option>
            <option value="FILE_DELETED">FILE_DELETED</option>
            <option value="PROCESS_STARTED">PROCESS_STARTED</option>
          </select>
        </div>
      </div>

      {/* Table */}
      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.8rem' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid var(--border-medium)', color: 'var(--text-dim)', fontSize: '0.72rem' }}>
              <th style={{ padding: '0.6rem 0.75rem' }}>EVIDENCE ID</th>
              <th style={{ padding: '0.6rem 0.75rem' }}>TIMESTAMP (UTC)</th>
              <th style={{ padding: '0.6rem 0.75rem' }}>TYPE</th>
              <th style={{ padding: '0.6rem 0.75rem' }}>FILE ARTIFACT</th>
              <th style={{ padding: '0.6rem 0.75rem' }}>DIRECTORY / PATH</th>
              <th style={{ padding: '0.6rem 0.75rem' }}>SIZE</th>
              <th style={{ padding: '0.6rem 0.75rem' }}>PROCESS</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((evt) => {
              const isHighlighted = highlightId === evt.event_id;
              return (
                <tr
                  key={evt.id}
                  style={{
                    borderBottom: '1px solid var(--border-subtle)',
                    background: isHighlighted ? 'rgba(56, 189, 248, 0.12)' : 'transparent',
                    transition: 'background 0.2s',
                  }}
                >
                  <td className="font-mono" style={{ padding: '0.6rem 0.75rem', color: '#38BDF8', fontWeight: 600 }}>
                    {evt.event_id}
                  </td>
                  <td className="font-mono" style={{ padding: '0.6rem 0.75rem', color: 'var(--text-muted)' }}>
                    {new Date(evt.timestamp).toISOString().replace('T', ' ').substring(11, 19)}
                  </td>
                  <td style={{ padding: '0.6rem 0.75rem' }}>
                    <span className="badge badge-baseline" style={{ fontSize: '0.65rem' }}>
                      {evt.event_type.replace('FILE_', '')}
                    </span>
                  </td>
                  <td style={{ padding: '0.6rem 0.75rem', color: '#FFFFFF', fontWeight: 600 }}>
                    {evt.file_name}
                  </td>
                  <td className="font-mono" style={{ padding: '0.6rem 0.75rem', color: 'var(--text-dim)', maxWidth: '280px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }} title={evt.path}>
                    {evt.path}
                  </td>
                  <td className="font-mono" style={{ padding: '0.6rem 0.75rem', color: 'var(--text-muted)' }}>
                    {evt.file_size > 0 ? `${evt.file_size.toLocaleString()} B` : '-'}
                  </td>
                  <td style={{ padding: '0.6rem 0.75rem', color: 'var(--text-muted)' }}>
                    {evt.process_name || '-'}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};
