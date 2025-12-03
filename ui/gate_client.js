const operatorConfig = (typeof window !== 'undefined' && window.OPERATOR_CONFIG) || {};

function deriveBaseUrl(config) {
  const loc = typeof window !== 'undefined' ? window.location : null;
  const protocol = (config.protocol || (loc && loc.protocol) || 'http:').replace(/:$/, '');
  const servicePort = config.servicePort || 8000;

  if (config.baseUrl && config.baseUrl !== 'auto') {
    return config.baseUrl;
  }

  if (!loc) {
    return `${protocol}://localhost:${servicePort}`;
  }

  let host = loc.hostname || 'localhost';

  // Codespaces/Gitpod-style forwarded hosts encode the port as the first hostname segment
  // (e.g. 9000-foo.github.dev). Swap that segment so the service port is addressed.
  if (/^\d+-/.test(host)) {
    const [, ...rest] = host.split('-');
    host = `${servicePort}-${rest.join('-')}`;
    return `${protocol}://${host}`;
  }

  if (loc.port) {
    return `${protocol}://${host}:${servicePort}`;
  }

  return `${protocol}://${host}:${servicePort}`;
}

const DEFAULT_BASE_URL = deriveBaseUrl(operatorConfig);

function normaliseBaseUrl(url) {
  if (!url) return DEFAULT_BASE_URL;
  return url.endsWith('/') ? url.slice(0, -1) : url;
}

export class GateClient {
  constructor(baseUrl = DEFAULT_BASE_URL) {
    this.baseUrl = normaliseBaseUrl(baseUrl);
  }

  setBaseUrl(baseUrl) {
    this.baseUrl = normaliseBaseUrl(baseUrl);
  }

  async get(path) {
    const response = await fetch(`${this.baseUrl}${path}`);
    if (!response.ok) {
      throw new Error(`Request failed (${response.status}) for ${path}`);
    }
    return response.json();
  }

  async post(path, body) {
    const response = await fetch(`${this.baseUrl}${path}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: body ? JSON.stringify(body) : undefined,
    });
    if (!response.ok) {
      const message = await response.text();
      throw new Error(`Request failed (${response.status}): ${message || path}`);
    }
    return response.json();
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
