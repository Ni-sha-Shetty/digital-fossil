import React, { useState, useEffect } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import { LoginModal } from './components/LoginModal';
import { Navbar } from './components/Navbar';
import { InvestigatorView } from './views/InvestigatorView';
import { ReviewerView } from './views/ReviewerView';
import { AdminView } from './views/AdminView';
import { MLMetricsView } from './components/MLMetricsView';

const MainLayout: React.FC = () => {
  const { isAuthenticated, role, loading } = useAuth();
  const [currentTab, setCurrentTab] = useState<string>('investigations');

  useEffect(() => {
    if (role === 'admin') {
      setCurrentTab('admin');
    } else if (role === 'reviewer') {
      setCurrentTab('reviewer_queue');
    } else {
      setCurrentTab('investigations');
    }
  }, [role]);

  if (loading) {
    return (
      <div
        style={{
          minHeight: '100vh',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          background: 'var(--bg-app)',
          color: 'var(--text-muted)',
          fontSize: '0.9rem',
          fontWeight: 600,
        }}
      >
        Initializing Digital Fossil Engine...
      </div>
    );
  }

  if (!isAuthenticated) {
    return <LoginModal />;
  }

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', background: 'var(--bg-app)' }}>
      <Navbar currentTab={currentTab} setCurrentTab={setCurrentTab} />
      <main style={{ flex: 1, paddingBottom: '3rem' }}>
        {currentTab === 'investigations' && <InvestigatorView />}
        {currentTab === 'reviewer_queue' && <ReviewerView />}
        {currentTab === 'admin' && <AdminView />}
        {currentTab === 'ml_metrics' && <MLMetricsView />}
      </main>

      <footer
        style={{
          borderTop: '1px solid var(--border-subtle)',
          padding: '1.25rem',
          textAlign: 'center',
          fontSize: '0.75rem',
          color: 'var(--text-dim)',
          background: 'rgba(8, 12, 20, 0.95)',
        }}
      >
        <div style={{ maxWidth: '1200px', margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span>
            <strong>DIGITAL FOSSIL:</strong> Explainable Activity Reconstruction Platform • SQLite • scikit-learn • NetworkX • FastAPI • React
          </span>
          <span style={{ color: 'var(--text-muted)' }}>
            Strict epistemic separation: Fact ≠ Inference ≠ Hypothesis
          </span>
        </div>
      </footer>
    </div>
  );
};

export default function App() {
  return (
    <AuthProvider>
      <MainLayout />
    </AuthProvider>
  );
}
