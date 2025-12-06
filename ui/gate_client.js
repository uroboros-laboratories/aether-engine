const DEFAULT_BASE_URL = (() => {
  if (typeof window !== 'undefined' && window.location?.origin) {
    return window.location.origin;
  }
  return 'http://localhost:8000';
})();

function ensureScheme(url) {
  if (!url) return url;
  return /^https?:\/\//i.test(url) ? url : `http://${url}`;
}

function normaliseBaseUrl(url) {
  if (!url) return DEFAULT_BASE_URL;
  const withScheme = ensureScheme(url.trim());
  return withScheme.endsWith('/') ? withScheme.slice(0, -1) : withScheme;
}

function buildNetworkError(url, err) {
  const baseMessage = `Network error calling ${url}: ${err.message}`;
  if (err?.message?.toLowerCase().includes('failed to fetch')) {
    return new Error(
      `${baseMessage}. Ensure the Operator Service is reachable from your browser, the URL includes the scheme (http/https), and CORS/network policies allow the request.`,
    );
  }
  return new Error(`${baseMessage}. Check service availability and connectivity.`);
}

async function requestJson(url, options = {}) {
  let response;
  try {
    response = await fetch(url, options);
  } catch (err) {
    throw buildNetworkError(url, err);
  }

  if (!response.ok) {
    let message;
    try {
      message = await response.text();
    } catch (err) {
      message = err?.message;
    }
    const detail = message ? `: ${message}` : '';
    throw new Error(`Request failed (${response.status}) for ${url}${detail}`);
  }

  return response.json();
}

export class GateClient {
  constructor(baseUrl = DEFAULT_BASE_URL) {
    this.baseUrl = normaliseBaseUrl(baseUrl);
  }

  setBaseUrl(baseUrl) {
    this.baseUrl = normaliseBaseUrl(baseUrl);
  }

  async get(path) {
    const url = `${this.baseUrl}${path}`;
    return requestJson(url);
  }

  async post(path, body) {
    const url = `${this.baseUrl}${path}`;
    return requestJson(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: body ? JSON.stringify(body) : undefined,
    });
  }

  // Core Operator Service endpoints surfaced for UI wiring.
  state() {
    return this.get('/state');
  }

  listScenarios() {
    return this.get('/scenarios');
  }

  getScenario(id) {
    return this.get(`/scenarios/${encodeURIComponent(id)}`);
  }

  updateScenario(id, payload) {
    return this.post(`/scenarios/${encodeURIComponent(id)}`, payload);
  }

  activateScenario(id) {
    return this.post(`/scenarios/${encodeURIComponent(id)}/activate`);
  }

  getGovernance() {
    return this.get('/governance');
  }

  updateGovernance(payload) {
    return this.post('/governance', payload);
  }

  startRun(payload) {
    return this.post('/runs', payload);
  }

  stopRun(runId) {
    return this.post(`/runs/${encodeURIComponent(runId)}/stop`);
  }

  getRunPillars(runId) {
    return this.get(`/runs/${encodeURIComponent(runId)}/pillars`);
  }

  getRunLogs(runId, options = {}) {
    const params = new URLSearchParams();
    if (options.cursor) params.append('cursor', options.cursor);
    if (options.level) params.append('level', options.level);
    if (options.event_type) params.append('event_type', options.event_type);
    const query = params.toString();
    const suffix = query ? `?${query}` : '';
    return this.get(`/runs/${encodeURIComponent(runId)}/logs${suffix}`);
  }

  listHistory() {
    return this.get('/history');
  }

  getHistoryEntry(runId) {
    return this.get(`/history/${encodeURIComponent(runId)}`);
  }

  exportHistoryEntry(runId) {
    return `${this.baseUrl}/history/${encodeURIComponent(runId)}/export`;
  }

  listDiagnostics() {
    return this.get('/diagnostics');
  }

  getDiagnosticsProfiles() {
    return this.get('/diagnostics/profiles');
  }

  startDiagnostics(payload) {
    return this.post('/diagnostics', payload);
  }

  getDiagnosticsRun(id) {
    return this.get(`/diagnostics/${encodeURIComponent(id)}`);
  }
}

export function loadSavedBaseUrl() {
  return normaliseBaseUrl(localStorage.getItem('gate_base_url') || DEFAULT_BASE_URL);
}

export function saveBaseUrl(url) {
  const normalised = normaliseBaseUrl(url);
  localStorage.setItem('gate_base_url', normalised);
  return normalised;
}
