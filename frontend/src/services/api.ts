import {
  AuthToken,
  User,
  InvestigationSummary,
  InvestigationDetail,
  EventItem,
  SessionItem,
  SystemStats,
  MLStatus,
  CollectorStatus,
  ThresholdConfig,
  AuditLogItem,
  NoteItem
} from '../types';

const API_BASE = '/api/v1';

function getHeaders(token?: string | null): HeadersInit {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };
  const activeToken = token || localStorage.getItem('df_token');
  if (activeToken) {
    headers['Authorization'] = `Bearer ${activeToken}`;
  }
  return headers;
}

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let errorDetail = `Request failed with status ${res.status}`;
    try {
      const data = await res.json();
      if (data.detail) {
        errorDetail = typeof data.detail === 'string' ? data.detail : JSON.stringify(data.detail);
      }
    } catch {
      // fallback
    }
    throw new Error(errorDetail);
  }
  return res.json();
}

export const api = {
  // Auth
  async login(email: string, password: string): Promise<AuthToken> {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    return handleResponse<AuthToken>(res);
  },

  async getMe(token?: string): Promise<User> {
    const res = await fetch(`${API_BASE}/auth/me`, {
      headers: getHeaders(token),
    });
    return handleResponse<User>(res);
  },

  // Investigations
  async getInvestigations(params?: {
    search?: string;
    status_filter?: string;
    confidence_filter?: string;
    anomaly_only?: boolean;
  }): Promise<InvestigationSummary[]> {
    const query = new URLSearchParams();
    if (params?.search) query.append('search', params.search);
    if (params?.status_filter) query.append('status_filter', params.status_filter);
    if (params?.confidence_filter) query.append('confidence_filter', params.confidence_filter);
    if (params?.anomaly_only) query.append('anomaly_only', 'true');

    const res = await fetch(`${API_BASE}/investigations?${query.toString()}`, {
      headers: getHeaders(),
    });
    return handleResponse<InvestigationSummary[]>(res);
  },

  async getInvestigationDetail(id: string): Promise<InvestigationDetail> {
    const res = await fetch(`${API_BASE}/investigations/${id}`, {
      headers: getHeaders(),
    });
    return handleResponse<InvestigationDetail>(res);
  },

  async addNote(investigationId: string, content: string): Promise<NoteItem> {
    const res = await fetch(`${API_BASE}/investigations/${investigationId}/notes`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ content }),
    });
    return handleResponse<NoteItem>(res);
  },

  async setReviewerVerdict(
    investigationId: string,
    verdict: 'approved' | 'flagged',
    comment: string
  ): Promise<any> {
    const res = await fetch(`${API_BASE}/investigations/${investigationId}/verdict`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ verdict, comment }),
    });
    return handleResponse<any>(res);
  },

  async downloadReportPdf(investigationId: string): Promise<Blob> {
    const token = localStorage.getItem('df_token');
    const res = await fetch(`${API_BASE}/reports/investigations/${investigationId}/pdf`, {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    });
    if (!res.ok) {
      throw new Error(`Failed to download report PDF (HTTP ${res.status})`);
    }
    return res.blob();
  },

  // Events & Sessions
  async getEvents(params?: {
    filename?: string;
    event_type?: string;
    session_id?: string;
    skip?: number;
    limit?: number;
  }): Promise<{ total: number; events: EventItem[] }> {
    const query = new URLSearchParams();
    if (params?.filename) query.append('filename', params.filename);
    if (params?.event_type) query.append('event_type', params.event_type);
    if (params?.session_id) query.append('session_id', params.session_id);
    if (params?.skip !== undefined) query.append('skip', String(params.skip));
    if (params?.limit !== undefined) query.append('limit', String(params.limit));

    const res = await fetch(`${API_BASE}/events?${query.toString()}`, {
      headers: getHeaders(),
    });
    return handleResponse<{ total: number; events: EventItem[] }>(res);
  },

  async getSessions(anomalyOnly = false): Promise<SessionItem[]> {
    const res = await fetch(`${API_BASE}/sessions?anomaly_only=${anomalyOnly}`, {
      headers: getHeaders(),
    });
    return handleResponse<SessionItem[]>(res);
  },

  // ML
  async getMLStatus(): Promise<MLStatus> {
    const res = await fetch(`${API_BASE}/ml/status`, {
      headers: getHeaders(),
    });
    return handleResponse<MLStatus>(res);
  },

  async retrainML(): Promise<any> {
    const res = await fetch(`${API_BASE}/ml/retrain`, {
      method: 'POST',
      headers: getHeaders(),
    });
    return handleResponse<any>(res);
  },

  // Collector
  async getCollectorStatus(): Promise<CollectorStatus> {
    const res = await fetch(`${API_BASE}/collector/status`, {
      headers: getHeaders(),
    });
    return handleResponse<CollectorStatus>(res);
  },

  async startCollector(directoryPath?: string): Promise<any> {
    const res = await fetch(`${API_BASE}/collector/start`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ directory_path: directoryPath || null }),
    });
    return handleResponse<any>(res);
  },

  async stopCollector(): Promise<any> {
    const res = await fetch(`${API_BASE}/collector/stop`, {
      method: 'POST',
      headers: getHeaders(),
    });
    return handleResponse<any>(res);
  },

  // Admin
  async getSystemStats(): Promise<SystemStats> {
    const res = await fetch(`${API_BASE}/admin/stats`, {
      headers: getHeaders(),
    });
    return handleResponse<SystemStats>(res);
  },

  async getUsers(): Promise<User[]> {
    const res = await fetch(`${API_BASE}/admin/users`, {
      headers: getHeaders(),
    });
    return handleResponse<User[]>(res);
  },

  async createUser(payload: {
    email: string;
    password: string;
    full_name: string;
    role: string;
  }): Promise<User> {
    const res = await fetch(`${API_BASE}/admin/users`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(payload),
    });
    return handleResponse<User>(res);
  },

  async getThresholds(): Promise<ThresholdConfig> {
    const res = await fetch(`${API_BASE}/admin/thresholds`, {
      headers: getHeaders(),
    });
    return handleResponse<ThresholdConfig>(res);
  },

  async updateThresholds(payload: {
    session_threshold_sec: number;
    min_relationship_score: number;
    anomaly_threshold: number;
  }): Promise<ThresholdConfig> {
    const res = await fetch(`${API_BASE}/admin/thresholds`, {
      method: 'PUT',
      headers: getHeaders(),
      body: JSON.stringify(payload),
    });
    return handleResponse<ThresholdConfig>(res);
  },

  async getAuditLogs(params?: {
    action?: string;
    user_email?: string;
    skip?: number;
    limit?: number;
  }): Promise<{
    total: number;
    logs: AuditLogItem[];
  }> {
    const query = new URLSearchParams();
    if (params?.action) query.append('action', params.action);
    if (params?.user_email) query.append('user_email', params.user_email);
    if (params?.skip !== undefined) query.append('skip', String(params.skip));
    if (params?.limit !== undefined) query.append('limit', String(params.limit));

    const res = await fetch(`${API_BASE}/admin/audit-logs?${query.toString()}`, {
      headers: getHeaders(),
    });
    return handleResponse<{ total: number; logs: AuditLogItem[] }>(res);
  },

  async resetDemoData(): Promise<any> {
    const res = await fetch(`${API_BASE}/admin/reset-demo`, {
      method: 'POST',
      headers: getHeaders(),
    });
    return handleResponse<any>(res);
  },
};
