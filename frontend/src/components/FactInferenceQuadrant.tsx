import React, { useState } from 'react';
import {
  ObservedFact,
  InferenceItem,
  HypothesisItem,
  MissingEvidenceItem,
  ConflictingEvidenceItem
} from '../types';
import { CheckCircle2, GitMerge, Lightbulb, HelpCircle, AlertTriangle, ChevronRight, ChevronDown, ShieldAlert } from 'lucide-react';

interface FactInferenceQuadrantProps {
  facts: ObservedFact[];
  inferences: InferenceItem[];
  hypotheses: HypothesisItem[];
  missingEvidence: MissingEvidenceItem[];
  conflictingEvidence: ConflictingEvidenceItem[];
  onSelectEvidence?: (evidenceId: string) => void;
}

export const FactInferenceQuadrant: React.FC<FactInferenceQuadrantProps> = ({
  facts,
  inferences,
  hypotheses,
  missingEvidence,
  conflictingEvidence,
  onSelectEvidence,
}) => {
  const [activeTab, setActiveTab] = useState<'all' | 'facts' | 'inferences' | 'hypotheses' | 'unknowns'>('all');
  const [expandedInferenceId, setExpandedInferenceId] = useState<string | null>(null);

  const toggleExpand = (id: string) => {
    setExpandedInferenceId(expandedInferenceId === id ? null : id);
  };

  return (
    <div style={{ marginTop: '1.5rem' }}>
      {/* Epistemic Navigation Filter Tabs */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          borderBottom: '1px solid var(--border-subtle)',
          paddingBottom: '0.75rem',
          marginBottom: '1.25rem',
        }}
      >
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <button
            className={`btn btn-sm ${activeTab === 'all' ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setActiveTab('all')}
          >
            All Epistemic Tiers
          </button>
          <button
            className={`btn btn-sm ${activeTab === 'facts' ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setActiveTab('facts')}
          >
            <span className="badge badge-fact" style={{ fontSize: '0.65rem' }}>{facts.length}</span> Observed Facts
          </button>
          <button
            className={`btn btn-sm ${activeTab === 'inferences' ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setActiveTab('inferences')}
          >
            <span className="badge badge-inference" style={{ fontSize: '0.65rem' }}>{inferences.length}</span> Inferences
          </button>
          <button
            className={`btn btn-sm ${activeTab === 'hypotheses' ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setActiveTab('hypotheses')}
          >
            <span className="badge badge-hypothesis" style={{ fontSize: '0.65rem' }}>{hypotheses.length}</span> Hypotheses
          </button>
          <button
            className={`btn btn-sm ${activeTab === 'unknowns' ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setActiveTab('unknowns')}
          >
            <span className="badge badge-unknown" style={{ fontSize: '0.65rem' }}>
              {missingEvidence.length + conflictingEvidence.length}
            </span> Unknowns & Gaps
          </button>
        </div>

        <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)', fontStyle: 'italic' }}>
          *Epistemic boundary: Inferences and hypotheses are never stated as verified facts.
        </div>
      </div>

      {/* Quadrant Grid */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: activeTab === 'all' ? 'repeat(2, 1fr)' : '1fr',
          gap: '1.25rem',
        }}
      >
        {/* 1. OBSERVED FACTS */}
        {(activeTab === 'all' || activeTab === 'facts') && (
          <div className="card" style={{ borderLeft: '4px solid var(--fact-color)' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <CheckCircle2 size={18} color="var(--fact-color)" />
                <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#FFFFFF' }}>OBSERVED FACTS</h3>
              </div>
              <span className="badge badge-fact">Direct Telemetry ({facts.length})</span>
            </div>
            <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '0.85rem' }}>
              Confirmed physical event logs recorded by OS or collectors. Immutable factual baseline.
            </p>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem', maxHeight: '420px', overflowY: 'auto', paddingRight: '0.3rem' }}>
              {facts.length === 0 ? (
                <div style={{ fontSize: '0.8rem', color: 'var(--text-dim)', textAlign: 'center', padding: '1rem' }}>
                  No event records observed.
                </div>
              ) : (
                facts.map((fact) => (
                  <div
                    key={fact.id}
                    style={{
                      background: 'rgba(255, 255, 255, 0.02)',
                      border: '1px solid var(--border-subtle)',
                      borderRadius: '0.5rem',
                      padding: '0.65rem 0.85rem',
                      fontSize: '0.82rem',
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.25rem' }}>
                      <span className="font-mono" style={{ fontSize: '0.72rem', color: 'var(--fact-color)', fontWeight: 700 }}>
                        {fact.id}
                      </span>
                      <span className="font-mono" style={{ fontSize: '0.7rem', color: 'var(--text-dim)' }}>
                        {new Date(fact.timestamp).toLocaleTimeString()}
                      </span>
                    </div>
                    <div style={{ color: 'var(--text-main)', lineHeight: 1.35 }}>
                      {fact.statement}
                    </div>
                    <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.4rem', fontSize: '0.7rem', color: 'var(--text-dim)' }}>
                      <span>Type: <strong style={{ color: 'var(--text-muted)' }}>{fact.event_type.replace('FILE_', '')}</strong></span>
                      {fact.process_name && <span>Process: <strong style={{ color: 'var(--text-muted)' }}>{fact.process_name}</strong></span>}
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        )}

        {/* 2. INFERENCES */}
        {(activeTab === 'all' || activeTab === 'inferences') && (
          <div className="card" style={{ borderLeft: '4px solid var(--inference-color)' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <GitMerge size={18} color="var(--inference-color)" />
                <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#FFFFFF' }}>INFERENCES</h3>
              </div>
              <span className="badge badge-inference">Derived Relations ({inferences.length})</span>
            </div>
            <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '0.85rem' }}>
              Probabilistic relationships synthesized across multiple observed records with transparent weights.
            </p>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem', maxHeight: '420px', overflowY: 'auto', paddingRight: '0.3rem' }}>
              {inferences.length === 0 ? (
                <div style={{ fontSize: '0.8rem', color: 'var(--text-dim)', textAlign: 'center', padding: '1rem' }}>
                  No correlated inferences meeting threshold.
                </div>
              ) : (
                inferences.map((inf) => {
                  const isExpanded = expandedInferenceId === inf.id;
                  return (
                    <div
                      key={inf.id}
                      style={{
                        background: 'rgba(255, 255, 255, 0.02)',
                        border: '1px solid var(--border-subtle)',
                        borderRadius: '0.5rem',
                        padding: '0.65rem 0.85rem',
                        fontSize: '0.82rem',
                      }}
                    >
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.25rem' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                          <span className="font-mono" style={{ fontSize: '0.72rem', color: 'var(--inference-color)', fontWeight: 700 }}>
                            {inf.id}
                          </span>
                          <span className="badge badge-inference" style={{ fontSize: '0.65rem' }}>
                            Score: {inf.correlation_score.toFixed(2)}
                          </span>
                        </div>
                        <button
                          onClick={() => toggleExpand(inf.id)}
                          style={{ background: 'transparent', border: 'none', color: 'var(--text-muted)', cursor: 'pointer', display: 'flex', alignItems: 'center', fontSize: '0.72rem' }}
                        >
                          {isExpanded ? <ChevronDown size={14} /> : <ChevronRight size={14} />} Factors
                        </button>
                      </div>

                      <div style={{ color: 'var(--text-main)', lineHeight: 1.35, marginBottom: '0.4rem' }}>
                        {inf.statement}
                      </div>

                      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.35rem', alignItems: 'center' }}>
                        <span style={{ fontSize: '0.7rem', color: 'var(--text-dim)' }}>Supporting Evidence:</span>
                        {inf.supporting_evidence_ids.map((evId) => (
                          <span
                            key={evId}
                            onClick={() => onSelectEvidence && onSelectEvidence(evId)}
                            className="font-mono"
                            style={{
                              fontSize: '0.68rem',
                              background: 'rgba(56, 189, 248, 0.1)',
                              color: '#38BDF8',
                              padding: '0.1rem 0.35rem',
                              borderRadius: '3px',
                              cursor: 'pointer',
                              border: '1px solid rgba(56, 189, 248, 0.25)',
                            }}
                          >
                            {evId}
                          </span>
                        ))}
                      </div>

                      {/* Factor Breakdown Accordion */}
                      {isExpanded && (
                        <div
                          style={{
                            marginTop: '0.65rem',
                            paddingTop: '0.65rem',
                            borderTop: '1px solid var(--border-subtle)',
                            fontSize: '0.72rem',
                            color: 'var(--text-muted)',
                            background: 'rgba(0, 0, 0, 0.2)',
                            borderRadius: '4px',
                            padding: '0.5rem',
                          }}
                        >
                          <div style={{ fontWeight: 700, color: 'var(--text-main)', marginBottom: '0.3rem' }}>
                            Scoring Factor Breakdown:
                          </div>
                          {Object.entries(inf.reasoning_factors).map(([factorName, details]: [string, any]) => (
                            <div key={factorName} style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.2rem' }}>
                              <span>• {factorName.replace('_', ' ')}:</span>
                              <span className="font-mono" style={{ color: '#38BDF8' }}>
                                Score {details.score} (weight {details.weight})
                              </span>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  );
                })
              )}
            </div>
          </div>
        )}

        {/* 3. HYPOTHESES */}
        {(activeTab === 'all' || activeTab === 'hypotheses') && (
          <div className="card" style={{ borderLeft: '4px solid var(--hypothesis-color)' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Lightbulb size={18} color="var(--hypothesis-color)" />
                <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#FFFFFF' }}>HYPOTHESES</h3>
              </div>
              <span className="badge badge-hypothesis">Explanatory Models ({hypotheses.length})</span>
            </div>
            <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '0.85rem' }}>
              High-level syntheses of operator intent. Accompanied by mandatory explicit uncertainty disclosures.
            </p>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', maxHeight: '420px', overflowY: 'auto' }}>
              {hypotheses.map((hyp) => (
                <div
                  key={hyp.id}
                  style={{
                    background: 'rgba(192, 132, 252, 0.04)',
                    border: '1px solid rgba(192, 132, 252, 0.2)',
                    borderRadius: '0.6rem',
                    padding: '0.85rem 1rem',
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.4rem' }}>
                    <span className="font-mono" style={{ fontSize: '0.75rem', color: 'var(--hypothesis-color)', fontWeight: 700 }}>
                      {hyp.id}
                    </span>
                    <span className="badge badge-hypothesis" style={{ fontSize: '0.68rem' }}>
                      Evidence Confidence: {Math.round(hyp.confidence * 100)}% ({hyp.confidence_label})
                    </span>
                  </div>

                  <div style={{ fontSize: '0.85rem', color: '#FFFFFF', fontWeight: 600, lineHeight: 1.4, marginBottom: '0.5rem' }}>
                    {hyp.hypothesis_text}
                  </div>

                  <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>
                    <strong>Reasoning:</strong> {hyp.reasoning_summary}
                  </div>

                  {/* Explicit Uncertainty Statement (MANDATORY REQUIREMENT) */}
                  <div
                    style={{
                      background: 'rgba(239, 68, 68, 0.1)',
                      border: '1px solid rgba(239, 68, 68, 0.25)',
                      borderRadius: '0.4rem',
                      padding: '0.5rem 0.75rem',
                      fontSize: '0.75rem',
                      color: '#FCA5A5',
                    }}
                  >
                    <strong>Explicit Uncertainty Statement:</strong> {hyp.uncertainty_statement}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* 4. UNKNOWNS & CONFLICTING EVIDENCE */}
        {(activeTab === 'all' || activeTab === 'unknowns') && (
          <div className="card" style={{ borderLeft: '4px solid var(--unknown-color)' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <HelpCircle size={18} color="var(--unknown-color)" />
                <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#FFFFFF' }}>UNKNOWN / INSUFFICIENT EVIDENCE</h3>
              </div>
              <span className="badge badge-unknown">
                Gaps & Conflicts ({missingEvidence.length + conflictingEvidence.length})
              </span>
            </div>
            <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '0.85rem' }}>
              Identified breaks in the forensic chain of custody and contradictory telemetry indicators.
            </p>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem', maxHeight: '420px', overflowY: 'auto' }}>
              {missingEvidence.length === 0 && conflictingEvidence.length === 0 ? (
                <div style={{ fontSize: '0.8rem', color: 'var(--text-dim)', textAlign: 'center', padding: '1rem' }}>
                  No critical evidentiary gaps or contradictions detected.
                </div>
              ) : (
                <>
                  {missingEvidence.map((m) => (
                    <div
                      key={m.id}
                      style={{
                        background: 'rgba(251, 191, 36, 0.05)',
                        border: '1px solid rgba(251, 191, 36, 0.25)',
                        borderRadius: '0.5rem',
                        padding: '0.65rem 0.85rem',
                        fontSize: '0.8rem',
                      }}
                    >
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', marginBottom: '0.2rem' }}>
                        <span className="badge badge-unknown" style={{ fontSize: '0.65rem' }}>MISSING TELEMETRY</span>
                        <span className="font-mono" style={{ fontSize: '0.72rem', color: 'var(--unknown-color)', fontWeight: 700 }}>
                          {m.id}
                        </span>
                      </div>
                      <div style={{ color: '#FEF08A', fontWeight: 600, marginBottom: '0.2rem' }}>
                        {m.description}
                      </div>
                      <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>
                        <strong>Significance:</strong> {m.significance}
                      </div>
                    </div>
                  ))}

                  {conflictingEvidence.map((c) => (
                    <div
                      key={c.id}
                      style={{
                        background: 'rgba(248, 113, 113, 0.08)',
                        border: '1px solid rgba(248, 113, 113, 0.3)',
                        borderRadius: '0.5rem',
                        padding: '0.65rem 0.85rem',
                        fontSize: '0.8rem',
                      }}
                    >
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', marginBottom: '0.2rem' }}>
                        <span className="badge badge-conflict" style={{ fontSize: '0.65rem' }}>
                          <ShieldAlert size={11} /> CONTRADICTORY EVIDENCE
                        </span>
                        <span className="font-mono" style={{ fontSize: '0.72rem', color: 'var(--conflict-color)', fontWeight: 700 }}>
                          {c.id}
                        </span>
                      </div>
                      <div style={{ color: '#FCA5A5', fontWeight: 600, marginBottom: '0.2rem' }}>
                        {c.description}
                      </div>
                      <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>
                        <strong>Forensic Impact:</strong> {c.impact_on_confidence}
                      </div>
                    </div>
                  ))}
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
