import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { InvestigationSummary, InvestigationDetail, EventItem } from '../types';
import { ConfidenceMeter } from '../components/ConfidenceMeter';
import { AnomalyBadge } from '../components/AnomalyBadge';
import { FactInferenceQuadrant } from '../components/FactInferenceQuadrant';
import { TimelineView } from '../components/TimelineView';
import { RelationshipGraph } from '../components/RelationshipGraph';
import { EvidenceTable } from '../components/EvidenceTable';
import { NotesSection } from '../components/NotesSection';
import {
  FileDown,
  Search,
  Filter,
  Activity,
  Bot,
  Layers,
  Clock,
  Network,
  Database,
  CheckCircle2,
  Sparkles
} from 'lucide-react';

export const InvestigatorView: React.FC = () => {
  const [investigations, setInvestigations] = useState<InvestigationSummary[]>([]);
  const [selectedInvId, setSelectedInvId] = useState<string | null>(null);
  const [detail, setDetail] = useState<InvestigationDetail | null>(null);
  const [rawEvents, setRawEvents] = useState<EventItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [loadingDetail, setLoadingDetail] = useState(false);
  const [exportingPdf, setExportingPdf] = useState(false);
  const [activeSection, setActiveSection] = useState<'quadrant' | 'timeline' | 'graph' | 'evidence' | 'ai'>('quadrant');

  // Filters
  const [search, setSearch] = useState('');
  const [confidenceFilter, setConfidenceFilter] = useState('');
  const [anomalyOnly, setAnomalyOnly] = useState(false);

  const fetchInvestigations = async () => {
    try {
      const list = await api.getInvestigations({
        search: search || undefined,
        confidence_filter: confidenceFilter || undefined,
        anomaly_only: anomalyOnly,
      });
      setInvestigations(list);
      if (!selectedInvId && list.length > 0) {
        // Automatically select the first (document workflow benchmark)
        setSelectedInvId(list[0].investigation_id);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchInvestigations();
  }, [search, confidenceFilter, anomalyOnly]);

  useEffect(() => {
    if (!selectedInvId) return;
    const loadDetail = async () => {
      setLoadingDetail(true);
      try {
        const invDetail = await api.getInvestigationDetail(selectedInvId);
        setDetail(invDetail);

        // Fetch session raw events for the ledger
        const evData = await api.getEvents({ session_id: invDetail.session_id, limit: 100 });
        setRawEvents(evData.events);
      } catch (e) {
        console.error(e);
      } finally {
        setLoadingDetail(false);
      }
    };
    loadDetail();
  }, [selectedInvId]);

  const handleExportPdf = async () => {
    if (!selectedInvId) return;
    setExportingPdf(true);
    try {
      const blob = await api.downloadReportPdf(selectedInvId);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `Digital_Fossil_Report_${selectedInvId}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (err: any) {
      alert(`Export error: ${err.message}`);
    } finally {
      setExportingPdf(false);
    }
  };

  const handleAddNote = async (content: string) => {
    if (!selectedInvId) return;
    const note = await api.addNote(selectedInvId, content);
    if (detail) {
      setDetail({ ...detail, notes: [...detail.notes, note] });
    }
  };

  return (
    <div style={{ maxWidth: '1600px', margin: '0 auto', padding: '1.5rem' }}>
      {/* Top Banner with Quick Demo Load */}
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          background: 'linear-gradient(90deg, rgba(37, 99, 235, 0.15), rgba(14, 22, 38, 0.6))',
          border: '1px solid var(--border-glow)',
          borderRadius: '0.75rem',
          padding: '1rem 1.5rem',
          marginBottom: '1.5rem',
        }}
      >
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span className="badge badge-fact">OPERATIONAL WORKSPACE</span>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Investigator Mode</span>
          </div>
          <h2 style={{ fontSize: '1.35rem', fontWeight: 800, color: '#FFFFFF', marginTop: '0.2rem' }}>
            Explainable Digital Activity Reconstruction
          </h2>
        </div>

        {/* 1-Click Load Demo Investigation */}
        <div style={{ display: 'flex', gap: '0.75rem' }}>
          <button
            className="btn btn-primary"
            onClick={() => {
              if (investigations.length > 0) {
                setSelectedInvId(investigations[0].investigation_id);
              }
            }}
          >
            <Sparkles size={16} /> Load Document Workflow Benchmark
          </button>
        </div>
      </div>

      {/* Main Grid: Left Investigation Selector, Right Detail View */}
      <div style={{ display: 'grid', gridTemplateColumns: '340px 1fr', gap: '1.5rem', alignItems: 'start' }}>
        {/* Left Column: Investigations List & Filters */}
        <div className="card">
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Activity size={16} color="#38BDF8" />
              <h3 style={{ fontSize: '0.95rem', fontWeight: 700, color: '#FFFFFF' }}>Active Cases ({investigations.length})</h3>
            </div>
          </div>

          {/* Search */}
          <div style={{ position: 'relative', marginBottom: '0.75rem' }}>
            <input
              type="text"
              className="input-field"
              placeholder="Search case titles or IDs..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              style={{ paddingLeft: '2rem', fontSize: '0.75rem' }}
            />
            <Search size={14} color="var(--text-dim)" style={{ position: 'absolute', left: '0.65rem', top: '0.7rem' }} />
          </div>

          {/* Filter options */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '0.5rem', marginBottom: '1rem' }}>
            <select
              className="input-field"
              value={confidenceFilter}
              onChange={(e) => setConfidenceFilter(e.target.value)}
              style={{ fontSize: '0.72rem' }}
            >
              <option value="">All Confidence</option>
              <option value="HIGH">High (&gt;= 75%)</option>
              <option value="MEDIUM">Medium</option>
              <option value="LOW">Low</option>
            </select>

            <button
              onClick={() => setAnomalyOnly(!anomalyOnly)}
              style={{
                background: anomalyOnly ? 'rgba(251, 146, 60, 0.2)' : 'var(--bg-card)',
                color: anomalyOnly ? '#FB923C' : 'var(--text-muted)',
                border: anomalyOnly ? '1px solid #FB923C' : '1px solid var(--border-subtle)',
                borderRadius: '0.5rem',
                fontSize: '0.72rem',
                fontWeight: 600,
                cursor: 'pointer',
              }}
            >
              Anomalies Only
            </button>
          </div>

          {/* List items */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', maxHeight: '680px', overflowY: 'auto' }}>
            {investigations.map((inv) => {
              const isSelected = selectedInvId === inv.investigation_id;
              const confColor = inv.confidence_label === 'HIGH' ? '#10B981' : inv.confidence_label === 'MEDIUM' ? '#F59E0B' : '#EF4444';

              return (
                <div
                  key={inv.id}
                  onClick={() => setSelectedInvId(inv.investigation_id)}
                  style={{
                    background: isSelected ? 'rgba(56, 189, 248, 0.12)' : 'rgba(255, 255, 255, 0.02)',
                    border: isSelected ? '1px solid #38BDF8' : '1px solid var(--border-subtle)',
                    borderRadius: '0.5rem',
                    padding: '0.75rem',
                    cursor: 'pointer',
                    transition: 'all 0.2s',
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.2rem' }}>
                    <span className="font-mono" style={{ fontSize: '0.72rem', color: '#38BDF8', fontWeight: 700 }}>
                      {inv.investigation_id}
                    </span>
                    <span style={{ fontSize: '0.68rem', fontWeight: 700, color: confColor }}>
                      {inv.confidence_label} ({Math.round(inv.overall_confidence * 100)}%)
                    </span>
                  </div>

                  <div style={{ fontSize: '0.82rem', fontWeight: 600, color: '#FFFFFF', marginBottom: '0.35rem', lineHeight: 1.3 }}>
                    {inv.title}
                  </div>

                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.68rem', color: 'var(--text-dim)' }}>
                    <span>{inv.observed_facts_count} Facts / {inv.inferences_count} Infs</span>
                    {inv.reviewer_verdict ? (
                      <span style={{ color: inv.reviewer_verdict === 'approved' ? '#34D399' : '#F87171' }}>
                        {inv.reviewer_verdict.toUpperCase()}
                      </span>
                    ) : (
                      <span>Pending Review</span>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right Column: Deep Investigation Workspace */}
        {loadingDetail ? (
          <div className="card" style={{ padding: '3rem', textAlign: 'center', color: 'var(--text-muted)' }}>
            Reconstructing activity and synthesizing multi-relational knowledge graph...
          </div>
        ) : detail ? (
          <div>
            {/* Investigation Header Card */}
            <div className="card" style={{ marginBottom: '1.25rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '0.3rem' }}>
                    <span className="font-mono" style={{ fontSize: '0.85rem', color: '#38BDF8', fontWeight: 700 }}>
                      {detail.investigation_id}
                    </span>
                    <span className="badge badge-baseline font-mono" style={{ fontSize: '0.7rem' }}>
                      Session: {detail.session_id}
                    </span>
                    <span className={`badge ${detail.reviewer_verdict === 'approved' ? 'badge-fact' : detail.reviewer_verdict === 'flagged' ? 'badge-conflict' : 'badge-baseline'}`}>
                      {detail.reviewer_verdict ? `REVIEW: ${detail.reviewer_verdict.toUpperCase()}` : 'PENDING REVIEW'}
                    </span>
                  </div>
                  <h1 style={{ fontSize: '1.4rem', fontWeight: 800, color: '#FFFFFF' }}>{detail.title}</h1>
                </div>

                {/* PDF Export Button */}
                <button
                  className="btn btn-secondary"
                  onClick={handleExportPdf}
                  disabled={exportingPdf}
                >
                  <FileDown size={16} />
                  {exportingPdf ? 'Compiling PDF...' : 'Export Forensic Report'}
                </button>
              </div>

              {/* Gauges & Badges Row */}
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '1rem', marginBottom: '1rem' }}>
                <ConfidenceMeter score={detail.overall_confidence} label={detail.confidence_label} />
                <AnomalyBadge isAnomaly={detail.is_anomaly} score={detail.anomaly_score} />
              </div>

              <div style={{ display: 'flex', gap: '1.5rem', fontSize: '0.75rem', color: 'var(--text-dim)', paddingTop: '0.6rem', borderTop: '1px solid var(--border-subtle)' }}>
                <span>Duration: <strong style={{ color: 'var(--text-muted)' }}>{detail.session_duration.toFixed(1)}s</strong></span>
                <span>Observed Facts: <strong style={{ color: '#10B981' }}>{detail.observed_facts_count}</strong></span>
                <span>Inferred Relationships: <strong style={{ color: '#38BDF8' }}>{detail.inferences_count}</strong></span>
                <span>Hypotheses Formulated: <strong style={{ color: '#C084FC' }}>{detail.hypotheses_count}</strong></span>
                <span>Identified Gaps: <strong style={{ color: '#FBBF24' }}>{detail.unknowns_count}</strong></span>
              </div>
            </div>

            {/* View Sub-Tabs */}
            <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1rem' }}>
              <button
                className={`btn btn-sm ${activeSection === 'quadrant' ? 'btn-primary' : 'btn-secondary'}`}
                onClick={() => setActiveSection('quadrant')}
              >
                <Layers size={14} /> Epistemic Separation (4 Tiers)
              </button>
              <button
                className={`btn btn-sm ${activeSection === 'timeline' ? 'btn-primary' : 'btn-secondary'}`}
                onClick={() => setActiveSection('timeline')}
              >
                <Clock size={14} /> Interactive Timeline
              </button>
              <button
                className={`btn btn-sm ${activeSection === 'graph' ? 'btn-primary' : 'btn-secondary'}`}
                onClick={() => setActiveSection('graph')}
              >
                <Network size={14} /> Relationship Graph
              </button>
              <button
                className={`btn btn-sm ${activeSection === 'ai' ? 'btn-primary' : 'btn-secondary'}`}
                onClick={() => setActiveSection('ai')}
              >
                <Bot size={14} /> AI Narrative & Evidence Package
              </button>
              <button
                className={`btn btn-sm ${activeSection === 'evidence' ? 'btn-primary' : 'btn-secondary'}`}
                onClick={() => setActiveSection('evidence')}
              >
                <Database size={14} /> Telemetry Ledger
              </button>
            </div>

            {/* Sub-tab views */}
            {activeSection === 'quadrant' && (
              <FactInferenceQuadrant
                facts={detail.observed_facts}
                inferences={detail.inferences}
                hypotheses={detail.hypotheses}
                missingEvidence={detail.missing_evidence}
                conflictingEvidence={detail.conflicting_evidence}
              />
            )}

            {activeSection === 'timeline' && (
              <TimelineView facts={detail.observed_facts} />
            )}

            {activeSection === 'graph' && (
              <RelationshipGraph graph={detail.graph} />
            )}

            {activeSection === 'evidence' && (
              <EvidenceTable events={rawEvents} />
            )}

            {activeSection === 'ai' && (
              <div className="card" style={{ marginTop: '1.5rem', borderLeft: '4px solid #38BDF8' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '1rem' }}>
                  <Bot size={18} color="#38BDF8" />
                  <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#FFFFFF' }}>
                    Explainable Forensic Synthesis & Structured Evidence Package
                  </h3>
                </div>
                <div style={{ whiteSpace: 'pre-wrap', fontSize: '0.85rem', color: 'var(--text-main)', lineHeight: 1.6, background: 'rgba(0,0,0,0.25)', padding: '1.25rem', borderRadius: '0.5rem', border: '1px solid var(--border-subtle)' }}>
                  {detail.ai_explanation}
                </div>
              </div>
            )}

            {/* Investigation Notes & Collaboration Section */}
            <NotesSection
              investigationId={detail.investigation_id}
              notes={detail.notes}
              onAddNote={handleAddNote}
            />
          </div>
        ) : (
          <div className="card" style={{ padding: '3rem', textAlign: 'center', color: 'var(--text-muted)' }}>
            Select an investigation case to inspect its evidence and reconstructed session.
          </div>
        )}
      </div>
    </div>
  );
};
