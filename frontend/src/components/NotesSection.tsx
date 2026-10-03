import React, { useState } from 'react';
import { NoteItem } from '../types';
import { useAuth } from '../context/AuthContext';
import { MessageSquare, Send, Shield } from 'lucide-react';

interface NotesSectionProps {
  investigationId: string;
  notes: NoteItem[];
  onAddNote: (content: string) => Promise<void>;
}

export const NotesSection: React.FC<NotesSectionProps> = ({
  investigationId,
  notes,
  onAddNote,
}) => {
  const { user } = useAuth();
  const [content, setContent] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!content.trim()) return;
    setSubmitting(true);
    try {
      await onAddNote(content.trim());
      setContent('');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="card" style={{ marginTop: '1.5rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '1rem' }}>
        <MessageSquare size={18} color="#38BDF8" />
        <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#FFFFFF' }}>
          Investigation Notes & Collaborative Audit Log ({notes.length})
        </h3>
      </div>

      {/* Notes List */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', marginBottom: '1.25rem' }}>
        {notes.length === 0 ? (
          <div style={{ fontSize: '0.8rem', color: 'var(--text-dim)', textAlign: 'center', padding: '1rem' }}>
            No investigation notes added yet.
          </div>
        ) : (
          notes.map((note) => (
            <div
              key={note.id}
              style={{
                background: 'rgba(255, 255, 255, 0.02)',
                border: '1px solid var(--border-subtle)',
                borderRadius: '0.5rem',
                padding: '0.75rem 1rem',
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.35rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <span className="badge badge-fact" style={{ fontSize: '0.65rem' }}>
                    {note.author_role.toUpperCase()}
                  </span>
                  <span style={{ fontSize: '0.78rem', color: '#FFFFFF', fontWeight: 600 }}>
                    {note.author_email}
                  </span>
                </div>
                <span className="font-mono" style={{ fontSize: '0.7rem', color: 'var(--text-dim)' }}>
                  {new Date(note.created_at).toLocaleString()}
                </span>
              </div>
              <div style={{ fontSize: '0.82rem', color: 'var(--text-main)', lineHeight: 1.4 }}>
                {note.content}
              </div>
            </div>
          ))
        )}
      </div>

      {/* Add Note Form */}
      <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '0.6rem' }}>
        <input
          type="text"
          className="input-field"
          placeholder="Add an investigative note or external corroboration..."
          value={content}
          onChange={(e) => setContent(e.target.value)}
          disabled={submitting}
        />
        <button type="submit" className="btn btn-primary" disabled={submitting || !content.trim()}>
          <Send size={15} /> Post
        </button>
      </form>
    </div>
  );
};
