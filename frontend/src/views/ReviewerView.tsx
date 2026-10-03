import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { InvestigationSummary, InvestigationDetail } from '../types';
import { FactInferenceQuadrant } from '../components/FactInferenceQuadrant';
import { ReviewerActionCard } from '../components/ReviewerActionCard';
import { ConfidenceMeter } from '../components/ConfidenceMeter';
import { AnomalyBadge } from '../components/AnomalyBadge';
import { UserCheck, FileDown, CheckCircle, Flag, Clock, Layers } from 'lucide-react';

export const ReviewerView: React.FC = () => {
  const [investigations, setInvestigations] = useState<InvestigationSummary[]>([]);
  const [selectedInvId, setSelectedInvId] = useState<string | null>(null);
  const [detail, setDetail] = useState<InvestigationDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [exportingPdf, setExportingPdf] = useState(false);

  const fetchQueue = async () => {
    try {
      const list = await api.getInvestigations();
      setInvestigations(list);
      if (!selectedInvId && list.length > 0) {
        setSelectedInvId(list[0].investigation_id);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchQueue();
  }, []);

  useEffect(() => {
    if (!selectedInvId) return;
    const loadDetail = async () => {
      try {
        const d = await api.getInvestigationDetail(selectedInvId);
        setDetail(d);
      } catch (e) {
        console.error(e);
      }
    };
    loadDetail();
  }, [selectedInvId]);

  const handleSetVerdict = async (verdict: 'approved' | 'flagged', comment: string) => {
    if (!selectedInvId) return;
    await api.setReviewerVerdict(selectedInvId, verdict, comment);
    // Refresh
    const updated = await api.getInvestigationDetail(selectedInvId);
    setDetail(updated);
    await fetchQueue();
  };

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

  if (loading) {
    return <div style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-muted)' }}>Loading Review Queue...</div>;
  }

  return (
    <div style={{ maxWidth: '1600px', margin: '0 auto', padding: '1.5rem' }}>
      {/* Header */}
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          background: 'linear-gradient(90deg, rgba(56, 189, 248, 0.15), rgba(14, 22, 38, 0.6))',
          border: '1px solid rgba(56, 189, 248, 0.3)',
          borderRadius: '0.75rem',
          padding: '1rem 1.5rem',
          marginBottom: '1.5rem',
        }}
      >
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span className="badge badge-inference">QUALITY GATE</span>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Reviewer Mode</span>
          </div>
          <h2 style={{ fontSize: '1.35rem', fontWeight: 800, color: '#FFFFFF', marginTop: '0.2rem' }}>
            Investigation Review & Attestation Queue
          </h2>
        </div>

        <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)', textAlign: 'right' }}>
          *Reviewers inspect evidence and approve/flag inferences without altering raw events.
        </div>
      </div>

      {/* Grid: Left Queue, Right Review Panel */}
      <div style={{ display: 'grid', gridTemplateColumns: '340px 1fr', gap: '1.5rem', alignItems: 'start' }}>
        {/* Left Queue */}
        <div className="card">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
            <UserCheck size={16} color="#38BDF8" />
            <h3 style={{ fontSize: '0.95rem', fontWeight: 700, color: '#FFFFFF' }}>Review Cases ({investigations.length})</h3>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', maxHeight: '720px', overflowY: 'auto' }}>
            {investigations.map((inv) => {
              const isSelected = selectedInvId === inv.investigation_id;
              const isApproved = inv.reviewer_verdict === 'approved';
              const isFlagged = inv.reviewer_verdict === 'flagged';

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
                    <span
                      className="badge"
                      style={{
                        background: isApproved ? 'rgba(16, 185, 129, 0.2)' : isFlagged ? 'rgba(239, 68, 68, 0.2)' : 'rgba(255, 255, 255, 0.08)',
                        color: isApproved ? '#34D399' : isFlagged ? '#F87171' : 'var(--text-muted)',
                        fontSize: '0.65rem',
                      }}
                    >
                      {isApproved ? 'APPROVED' : isFlagged ? 'FLAGGED' : 'PENDING'}
                    </span>
                  </div>

                  <div style={{ fontSize: '0.82rem', fontWeight: 600, color: '#FFFFFF', marginBottom: '0.35rem', lineHeight: 1.3 }}>
                    {inv.title}
                  </div>

                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.68rem', color: 'var(--text-dim)' }}>
                    <span>Confidence: {Math.round(inv.overall_confidence * 100)}%</span>
                    <span>{inv.observed_facts_count} Facts</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right Detail & Review Actions */}
        {detail ? (
          <div>
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
                  </div>
                  <h1 style={{ fontSize: '1.35rem', fontWeight: 800, color: '#FFFFFF' }}>{detail.title}</h1>
                </div>

                <button className="btn btn-secondary" onClick={handleExportPdf} disabled={exportingPdf}>
                  <FileDown size={16} /> Export PDF Report
                </button>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '1rem' }}>
                <ConfidenceMeter score={detail.overall_confidence} label={detail.confidence_label} />
                <AnomalyBadge isAnomaly={detail.is_anomaly} score={detail.anomaly_score} />
              </div>
            </div>

            {/* Reviewer Action Card (Primary focus for Reviewer Role) */}
            <ReviewerActionCard
              investigationId={detail.investigation_id}
              currentVerdict={detail.reviewer_verdict}
              currentComment={detail.reviewer_comment}
              reviewedBy={detail.reviewed_by}
              reviewedAt={detail.reviewed_at}
              onSetVerdict={handleSetVerdict}
            />

            {/* Facts and Inferences for Review Examination */}
            <FactInferenceQuadrant
              facts={detail.observed_facts}
              inferences={detail.inferences}
              hypotheses={detail.hypotheses}
              missingEvidence={detail.missing_evidence}
              conflictingEvidence={detail.conflicting_evidence}
            />
          </div>
        ) : (
          <div className="card" style={{ padding: '3rem', textAlign: 'center', color: 'var(--text-muted)' }}>
            Select an investigation case from the review queue.
          </div>
        )}
      </div>
    </div>
  );
};
