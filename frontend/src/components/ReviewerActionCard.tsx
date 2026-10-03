import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { CheckCircle2, Flag, UserCheck, AlertCircle } from 'lucide-react';

interface ReviewerActionCardProps {
  investigationId: string;
  currentVerdict?: string | null;
  currentComment?: string | null;
  reviewedBy?: string | null;
  reviewedAt?: string | null;
  onSetVerdict: (verdict: 'approved' | 'flagged', comment: string) => Promise<void>;
}

export const ReviewerActionCard: React.FC<ReviewerActionCardProps> = ({
  investigationId,
  currentVerdict,
  currentComment,
  reviewedBy,
  reviewedAt,
  onSetVerdict,
}) => {
  const { role } = useAuth();
  const [comment, setComment] = useState(currentComment || '');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  const canReview = role === 'reviewer' || role === 'admin';

  const handleAction = async (verdict: 'approved' | 'flagged') => {
    setError(null);
    setSuccessMsg(null);
    if (verdict === 'flagged' && !comment.trim()) {
      setError('A substantive review comment is strictly required when flagging an inference.');
      return;
    }

    setSubmitting(true);
    try {
      await onSetVerdict(verdict, comment.trim());
      setSuccessMsg(`Investigation marked as ${verdict.toUpperCase()}.`);
    } catch (err: any) {
      setError(err.message || 'Failed to submit reviewer verdict');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div
      className="card"
      style={{
        marginTop: '1.5rem',
        border: currentVerdict === 'approved' ? '1px solid #10B981' : currentVerdict === 'flagged' ? '1px solid #EF4444' : '1px solid var(--border-subtle)',
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
          <UserCheck size={18} color="#38BDF8" />
          <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#FFFFFF' }}>
            Reviewer Attestation & Independent Quality Gate
          </h3>
        </div>

        {currentVerdict && (
          <span className={`badge ${currentVerdict === 'approved' ? 'badge-fact' : 'badge-conflict'}`}>
            VERDICT: {currentVerdict.toUpperCase()}
          </span>
        )}
      </div>

      {reviewedBy && (
        <div style={{ fontSize: '0.78rem', color: 'var(--text-dim)', marginBottom: '1rem' }}>
          Last attested by <strong style={{ color: 'var(--text-muted)' }}>{reviewedBy}</strong> on{' '}
          {reviewedAt ? new Date(reviewedAt).toLocaleString() : 'N/A'}
        </div>
      )}

      {error && (
        <div
          style={{
            background: 'rgba(239, 68, 68, 0.15)',
            border: '1px solid rgba(239, 68, 68, 0.3)',
            borderRadius: '0.4rem',
            padding: '0.5rem 0.75rem',
            fontSize: '0.78rem',
            color: '#FCA5A5',
            marginBottom: '1rem',
          }}
        >
          {error}
        </div>
      )}

      {successMsg && (
        <div
          style={{
            background: 'rgba(16, 185, 129, 0.15)',
            border: '1px solid rgba(16, 185, 129, 0.3)',
            borderRadius: '0.4rem',
            padding: '0.5rem 0.75rem',
            fontSize: '0.78rem',
            color: '#A7F3D0',
            marginBottom: '1rem',
          }}
        >
          {successMsg}
        </div>
      )}

      {canReview ? (
        <div>
          <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.4rem' }}>
            Reviewer Remarks / Forensic Critique (Required if Flagging):
          </label>
          <textarea
            className="input-field"
            rows={3}
            placeholder="e.g. 'Evidence supports sequence, but note lack of process export event' or 'Flagged because 60s time gap is too large without intermediary staging logs'..."
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            disabled={submitting}
            style={{ marginBottom: '1rem', resize: 'vertical' }}
          />

          <div style={{ display: 'flex', gap: '0.75rem' }}>
            <button
              type="button"
              className="btn btn-success"
              onClick={() => handleAction('approved')}
              disabled={submitting}
            >
              <CheckCircle2 size={16} /> Approve Reconstruction
            </button>
            <button
              type="button"
              className="btn btn-danger"
              onClick={() => handleAction('flagged')}
              disabled={submitting}
            >
              <Flag size={16} /> Flag Inference as Uncertain
            </button>
          </div>
        </div>
      ) : (
        <div style={{ fontSize: '0.8rem', color: 'var(--text-dim)', fontStyle: 'italic' }}>
          *Your current role is '{role}'. Only users with Reviewer or Admin credentials may submit official verdicts on reconstructions.
        </div>
      )}
    </div>
  );
};
