import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { MLStatus, ClassificationMetrics } from '../types';
import { Cpu, RefreshCw, CheckCircle2, BarChart2, Zap, Sliders } from 'lucide-react';

export const MLMetricsView: React.FC = () => {
  const [mlStatus, setMlStatus] = useState<MLStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [retraining, setRetraining] = useState(false);

  // Sandbox inputs
  const [testTimeDiff, setTestTimeDiff] = useState(12.0);
  const [testNameSim, setTestNameSim] = useState(0.85);
  const [testSameDir, setTestSameDir] = useState(true);
  const [testSameExt, setTestSameExt] = useState(false);
  const [testSeqCompat, setTestSeqCompat] = useState(true);
  const [testSizeRatio, setTestSizeRatio] = useState(0.80);
  const [testResult, setTestResult] = useState<any>(null);

  const fetchStatus = async () => {
    try {
      const data = await api.getMLStatus();
      setMlStatus(data);
    } catch (err) {
      console.error('Failed to load ML metrics', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStatus();
  }, []);

  const handleRetrain = async () => {
    setRetraining(true);
    try {
      await api.retrainML();
      await fetchStatus();
    } finally {
      setRetraining(false);
    }
  };

  const handleTestPredict = async () => {
    try {
      const res = await fetch('/api/v1/ml/predict-pair', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('df_token')}`,
        },
        body: JSON.stringify({
          time_diff_sec: testTimeDiff,
          filename_sim: testNameSim,
          same_directory: testSameDir,
          same_extension: testSameExt,
          seq_compatible: testSeqCompat,
          size_ratio: testSizeRatio,
        }),
      });
      const data = await res.json();
      setTestResult(data);
    } catch (e) {
      console.error(e);
    }
  };

  if (loading) {
    return <div style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-muted)' }}>Loading ML Models...</div>;
  }

  return (
    <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '1.5rem' }}>
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem' }}>
        <div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: '#FFFFFF', display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <Cpu size={24} color="#38BDF8" /> Machine Learning & Statistical Anomaly Architecture
          </h2>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '0.2rem' }}>
            Genuine scikit-learn models: Supervised event-pair correlation & Unsupervised Isolation Forest session anomaly detection.
          </p>
        </div>

        <button
          className="btn btn-secondary"
          onClick={handleRetrain}
          disabled={retraining}
        >
          <RefreshCw size={15} className={retraining ? 'animate-spin' : ''} />
          {retraining ? 'Retraining...' : 'Retrain & Re-evaluate Baseline'}
        </button>
      </div>

      {/* Model Cards Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '1.5rem', marginBottom: '2rem' }}>
        {mlStatus?.models.map((model) => (
          <div key={model.model_name} className="card">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
              <div>
                <span className="badge badge-inference" style={{ fontSize: '0.68rem', marginBottom: '0.3rem' }}>
                  Supervised Binary Classifier
                </span>
                <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#FFFFFF' }}>{model.model_name}</h3>
                <div style={{ fontSize: '0.72rem', color: 'var(--text-dim)' }}>
                  Evaluated on {model.sample_count} hold-out synthetic test instances
                </div>
              </div>
              <span className="badge badge-fact">Trained & Validated</span>
            </div>

            {/* Metrics Grid */}
            <div
              style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(4, 1fr)',
                gap: '0.75rem',
                background: 'rgba(255, 255, 255, 0.02)',
                padding: '0.85rem',
                borderRadius: '0.5rem',
                marginBottom: '1rem',
                textAlign: 'center',
              }}
            >
              <div>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-dim)' }}>ACCURACY</div>
                <div style={{ fontSize: '1.2rem', fontWeight: 800, color: '#10B981', fontFamily: 'var(--font-mono)' }}>
                  {(model.accuracy * 100).toFixed(1)}%
                </div>
              </div>
              <div>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-dim)' }}>PRECISION</div>
                <div style={{ fontSize: '1.2rem', fontWeight: 800, color: '#38BDF8', fontFamily: 'var(--font-mono)' }}>
                  {(model.precision * 100).toFixed(1)}%
                </div>
              </div>
              <div>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-dim)' }}>RECALL</div>
                <div style={{ fontSize: '1.2rem', fontWeight: 800, color: '#A855F7', fontFamily: 'var(--font-mono)' }}>
                  {(model.recall * 100).toFixed(1)}%
                </div>
              </div>
              <div>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-dim)' }}>F1 SCORE</div>
                <div style={{ fontSize: '1.2rem', fontWeight: 800, color: '#F59E0B', fontFamily: 'var(--font-mono)' }}>
                  {(model.f1_score * 100).toFixed(1)}%
                </div>
              </div>
            </div>

            {/* Confusion Matrix */}
            <div style={{ marginBottom: '1rem' }}>
              <div style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--text-muted)', marginBottom: '0.5rem' }}>
                CONFUSION MATRIX (True Pos / True Neg)
              </div>
              <div
                style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(2, 1fr)',
                  gap: '0.4rem',
                  maxWidth: '240px',
                  fontFamily: 'var(--font-mono)',
                  fontSize: '0.8rem',
                }}
              >
                <div style={{ background: 'rgba(16, 185, 129, 0.1)', padding: '0.4rem', borderRadius: '4px', textAlign: 'center' }}>
                  TN: {model.confusion_matrix[0]?.[0]}
                </div>
                <div style={{ background: 'rgba(239, 68, 68, 0.1)', padding: '0.4rem', borderRadius: '4px', textAlign: 'center' }}>
                  FP: {model.confusion_matrix[0]?.[1]}
                </div>
                <div style={{ background: 'rgba(239, 68, 68, 0.1)', padding: '0.4rem', borderRadius: '4px', textAlign: 'center' }}>
                  FN: {model.confusion_matrix[1]?.[0]}
                </div>
                <div style={{ background: 'rgba(16, 185, 129, 0.1)', padding: '0.4rem', borderRadius: '4px', textAlign: 'center' }}>
                  TP: {model.confusion_matrix[1]?.[1]}
                </div>
              </div>
            </div>

            {/* Feature Importances / Coefficients */}
            <div>
              <div style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--text-muted)', marginBottom: '0.5rem' }}>
                FEATURE COEFFICIENTS / IMPORTANCE
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.35rem' }}>
                {Object.entries(model.feature_importances).map(([feat, val]) => (
                  <div key={feat} style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem' }}>
                    <span style={{ color: 'var(--text-muted)' }}>{feat}</span>
                    <span className="font-mono" style={{ color: '#38BDF8', fontWeight: 600 }}>
                      {typeof val === 'number' ? val.toFixed(4) : val}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Anomaly Detector Architecture Box */}
      <div className="card" style={{ marginBottom: '2rem', borderLeft: '4px solid #FB923C' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <span className="badge badge-anomaly">UNSUPERVISED ML</span>
            <h3 style={{ fontSize: '1.05rem', fontWeight: 700, color: '#FFFFFF' }}>
              Isolation Forest Anomaly Detection (scikit-learn)
            </h3>
          </div>
          <span className="badge badge-baseline">Contamination: 10%</span>
        </div>
        <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', lineHeight: 1.5, marginBottom: '0.75rem' }}>
          <strong>Philosophical Distinction:</strong> {mlStatus?.anomaly_detector_summary.note}
        </p>
        <div style={{ fontSize: '0.78rem', color: 'var(--text-dim)', background: 'rgba(0,0,0,0.2)', padding: '0.6rem', borderRadius: '6px' }}>
          Evaluates multi-dimensional activity vectors across duration, modification frequency, rename volume, deletions, average delta times, and unique directory counts to flag sessions departing significantly from standard operational cadences.
        </div>
      </div>

      {/* Interactive Feature Sandbox */}
      <div className="card">
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '1rem' }}>
          <Sliders size={18} color="#38BDF8" />
          <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#FFFFFF' }}>
            Interactive Pairwise Relationship Prediction Sandbox
          </h3>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1rem', marginBottom: '1rem' }}>
          <div>
            <label style={{ display: 'block', fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '0.3rem' }}>
              Time Difference (seconds): {testTimeDiff}s
            </label>
            <input
              type="range"
              min="0"
              max="180"
              step="1"
              value={testTimeDiff}
              onChange={(e) => setTestTimeDiff(parseFloat(e.target.value))}
              style={{ width: '100%' }}
            />
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '0.3rem' }}>
              Filename Similarity: {(testNameSim * 100).toFixed(0)}%
            </label>
            <input
              type="range"
              min="0"
              max="1"
              step="0.05"
              value={testNameSim}
              onChange={(e) => setTestNameSim(parseFloat(e.target.value))}
              style={{ width: '100%' }}
            />
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '0.3rem' }}>
              Size Ratio: {(testSizeRatio * 100).toFixed(0)}%
            </label>
            <input
              type="range"
              min="0"
              max="1"
              step="0.05"
              value={testSizeRatio}
              onChange={(e) => setTestSizeRatio(parseFloat(e.target.value))}
              style={{ width: '100%' }}
            />
          </div>
        </div>

        <div style={{ display: 'flex', gap: '1.5rem', marginBottom: '1.25rem', fontSize: '0.8rem', color: 'var(--text-main)' }}>
          <label style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', cursor: 'pointer' }}>
            <input
              type="checkbox"
              checked={testSameDir}
              onChange={(e) => setTestSameDir(e.target.checked)}
            />
            Same Directory
          </label>
          <label style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', cursor: 'pointer' }}>
            <input
              type="checkbox"
              checked={testSameExt}
              onChange={(e) => setTestSameExt(e.target.checked)}
            />
            Same Extension
          </label>
          <label style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', cursor: 'pointer' }}>
            <input
              type="checkbox"
              checked={testSeqCompat}
              onChange={(e) => setTestSeqCompat(e.target.checked)}
            />
            Compatible Lifecycle Sequence
          </label>
        </div>

        <button className="btn btn-primary" onClick={handleTestPredict}>
          <Zap size={16} /> Compute Real-Time Pairwise Inference
        </button>

        {testResult && (
          <div
            style={{
              marginTop: '1rem',
              padding: '0.85rem',
              background: 'rgba(56, 189, 248, 0.08)',
              border: '1px solid rgba(56, 189, 248, 0.3)',
              borderRadius: '0.5rem',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
            }}
          >
            <div>
              <div style={{ fontWeight: 700, color: '#FFFFFF', marginBottom: '0.2rem' }}>
                Classification: {testResult.is_related ? 'LIKELY RELATED EVENTS' : 'INDEPENDENT / UNRELATED'}
              </div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                Ensemble Probability: {(testResult.probability * 100).toFixed(1)}% | Logistic Regression: {(testResult.logistic_regression_prob * 100).toFixed(1)}% | Random Forest: {(testResult.random_forest_prob * 100).toFixed(1)}%
              </div>
            </div>
            <span className={`badge ${testResult.is_related ? 'badge-fact' : 'badge-baseline'}`}>
              {(testResult.probability * 100).toFixed(1)}% PROBABILITY
            </span>
          </div>
        )}
      </div>
    </div>
  );
};
