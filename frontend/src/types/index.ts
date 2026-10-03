export type UserRole = 'investigator' | 'reviewer' | 'admin';

export interface User {
  id: number;
  email: string;
  full_name: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
}

export interface AuthToken {
  access_token: string;
  token_type: string;
  role: UserRole;
  email: string;
  full_name: string;
}

export interface ObservedFact {
  id: string;
  event_id: string;
  timestamp: string;
  statement: string;
  event_type: string;
  file_name: string;
  path: string;
  process_name: string | null;
  file_size: number;
}

export interface InferenceItem {
  id: string;
  statement: string;
  primary_file: string;
  related_file?: string | null;
  supporting_evidence_ids: string[];
  correlation_score: number;
  reasoning_factors: Record<string, any>;
  ml_probability?: number | null;
  status: string;
}

export interface HypothesisItem {
  id: string;
  hypothesis_text: string;
  supporting_evidence_ids: string[];
  contradicting_evidence_ids: string[];
  confidence: number;
  confidence_label: 'HIGH' | 'MEDIUM' | 'LOW';
  reasoning_summary: string;
  uncertainty_statement: string;
}

export interface MissingEvidenceItem {
  id: string;
  description: string;
  significance: string;
  expected_event_type?: string | null;
}

export interface ConflictingEvidenceItem {
  id: string;
  description: string;
  conflict_type: string;
  impact_on_confidence: string;
}

export interface GraphNode {
  id: string;
  label: string;
  type: string; // file, event, process, directory, session
  timestamp?: string | null;
  size?: number | null;
  is_anomaly?: boolean;
  metadata?: Record<string, any>;
}

export interface GraphEdge {
  source: string;
  target: string;
  label: string;
  relationship_type: string;
  score: number;
  evidence_ids: string[];
}

export interface GraphData {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

export interface NoteItem {
  id: number;
  investigation_id: string;
  author_email: string;
  author_role: string;
  content: string;
  created_at: string;
}

export interface InvestigationSummary {
  id: number;
  investigation_id: string;
  session_id: string;
  title: string;
  status: string;
  reviewer_verdict?: string | null;
  reviewer_comment?: string | null;
  reviewed_by?: string | null;
  reviewed_at?: string | null;
  overall_confidence: number;
  confidence_label: 'HIGH' | 'MEDIUM' | 'LOW';
  observed_facts_count: number;
  inferences_count: number;
  hypotheses_count: number;
  unknowns_count: number;
  summary: string;
  created_at: string;
  updated_at: string;
}

export interface InvestigationDetail extends InvestigationSummary {
  session_start: string;
  session_end: string;
  session_duration: number;
  is_anomaly: boolean;
  anomaly_score: number;
  observed_facts: ObservedFact[];
  inferences: InferenceItem[];
  hypotheses: HypothesisItem[];
  missing_evidence: MissingEvidenceItem[];
  conflicting_evidence: ConflictingEvidenceItem[];
  ai_explanation: string;
  graph: GraphData;
  notes: NoteItem[];
}

export interface EventItem {
  id: number;
  event_id: string;
  timestamp: string;
  event_type: string;
  path: string;
  file_name: string;
  extension: string;
  directory: string;
  file_size: number;
  source: string;
  process_name?: string | null;
  session_id?: string | null;
  created_at: string;
}

export interface SessionItem {
  id: number;
  session_id: string;
  start_time: string;
  end_time: string;
  duration_seconds: number;
  event_count: number;
  involved_files: string[];
  involved_directories: string[];
  detected_processes: string[];
  anomaly_score: number;
  is_anomaly: boolean;
  confidence_score: number;
  status: string;
  scenario_tag: string;
  created_at: string;
}

export interface SystemStats {
  total_events: number;
  total_sessions: number;
  total_investigations: number;
  anomalous_sessions: number;
  total_users: number;
  approved_investigations: number;
  flagged_investigations: number;
  collector_running: boolean;
  collector_directory: string;
  database_status: string;
  timestamp: string;
}

export interface ClassificationMetrics {
  model_name: string;
  accuracy: number;
  precision: number;
  recall: number;
  f1_score: number;
  confusion_matrix: number[][];
  feature_importances: Record<string, number>;
  sample_count: number;
}

export interface MLStatus {
  is_trained: boolean;
  models: ClassificationMetrics[];
  anomaly_detector_summary: Record<string, any>;
}

export interface CollectorStatus {
  is_running: boolean;
  monitored_directory: string;
  events_captured: number;
  privacy_notice: string;
  message: string;
}

export interface ThresholdConfig {
  session_threshold_sec: number;
  min_relationship_score: number;
  anomaly_threshold: number;
  updated_at: string;
  updated_by: string;
}

export interface AuditLogItem {
  id: number;
  timestamp: string;
  user_email: string;
  role: string;
  action: string;
  target: string;
  metadata: Record<string, any>;
}
