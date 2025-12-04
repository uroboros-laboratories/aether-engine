import { GateClient, loadSavedBaseUrl, saveBaseUrl } from './gate_client.js';

const baseUrlInput = document.getElementById('base-url');
const saveEndpointButton = document.getElementById('save-endpoint');
const statusLine = document.getElementById('status-line');
const tabs = Array.from(document.querySelectorAll('.tab'));
const panels = Array.from(document.querySelectorAll('.panel'));
const runStateEl = document.getElementById('run-state');
const runIdEl = document.getElementById('run-id');
const runScenarioEl = document.getElementById('run-scenario');
const runStartedEl = document.getElementById('run-started');
const runFinishedEl = document.getElementById('run-finished');
const runScenarioInput = document.getElementById('run-scenario-input');
const runTicksInput = document.getElementById('run-ticks');
const startRunForm = document.getElementById('start-run-form');
const startRunButton = document.getElementById('start-run');
const stopRunButton = document.getElementById('stop-run');
const scenarioTitleEl = document.getElementById('scenario-title');
const scenarioIdEl = document.getElementById('scenario-id');
const scenarioDescriptionEl = document.getElementById('scenario-description');
const pillarListEl = document.getElementById('pillar-list');
const governanceModeEl = document.getElementById('governance-mode');
const governanceCodexEl = document.getElementById('governance-codex');
const governanceBudgetsEl = document.getElementById('governance-budgets');
const governanceSummaryMode = document.getElementById('governance-summary-mode');
const governanceSummaryCodex = document.getElementById('governance-summary-codex');
const governanceSummaryBudgets = document.getElementById('governance-summary-budgets');
const governanceForm = document.getElementById('governance-form');
const governanceModeInput = document.getElementById('governance-mode-input');
const governanceCodexInput = document.getElementById('governance-codex-input');
const budgetPoliciesEl = document.getElementById('budget-policies');
const addBudgetButton = document.getElementById('add-budget');
const governanceSaveButton = document.getElementById('governance-save');
const governanceErrorEl = document.getElementById('governance-error');
const governanceRefreshButton = document.getElementById('governance-refresh');
const governanceResetButton = document.getElementById('governance-reset');
const diagnosticStateEl = document.getElementById('diagnostic-state');
const diagnosticIdEl = document.getElementById('diagnostic-id');
const diagnosticForm = document.getElementById('diagnostic-form');
const diagnosticProfileSelect = document.getElementById('diagnostic-profile');
const diagnosticHistoryList = document.getElementById('diagnostic-history');
const historyListEl = document.getElementById('history-list');
const historyRefreshButton = document.getElementById('history-refresh');
const historyDetailTitle = document.getElementById('history-detail-title');
const historyRunId = document.getElementById('history-run-id');
const historyScenario = document.getElementById('history-scenario');
const historyResult = document.getElementById('history-result');
const historyStarted = document.getElementById('history-started');
const historyFinished = document.getElementById('history-finished');
const historyTicks = document.getElementById('history-ticks');
const historyGovernance = document.getElementById('history-governance');
const historyMetrics = document.getElementById('history-metrics');
const historyPillars = document.getElementById('history-pillars');
const historyExportButton = document.getElementById('history-export');
const diagnosticsArchiveList = document.getElementById('history-diagnostics');
const diagnosticDetailTitle = document.getElementById('diagnostic-detail-title');
const diagnosticDetailId = document.getElementById('diagnostic-detail-id');
const diagnosticDetailProfile = document.getElementById('diagnostic-detail-profile');
const diagnosticDetailState = document.getElementById('diagnostic-detail-state');
const diagnosticDetailRuns = document.getElementById('diagnostic-detail-runs');
const diagnosticChecksEl = document.getElementById('diagnostic-checks');
const logsRunInput = document.getElementById('logs-run-id');
const logsLevelSelect = document.getElementById('logs-level');
const logsEventInput = document.getElementById('logs-event');
const logsFollowCurrentInput = document.getElementById('logs-follow-current');
const logsAutoscrollInput = document.getElementById('logs-autoscroll');
const logsRefreshButton = document.getElementById('logs-refresh');
const logsMoreButton = document.getElementById('logs-more');
const logsListEl = document.getElementById('logs-list');
const logsCursorEl = document.getElementById('logs-cursor');
const scenarioListEl = document.getElementById('scenario-list');
const scenarioSearchInput = document.getElementById('scenario-search');
const scenarioRefreshButton = document.getElementById('refresh-scenarios');
const scenarioDetailTitle = document.getElementById('scenario-detail-title');
const scenarioDetailId = document.getElementById('scenario-detail-id');
const scenarioPillarsEl = document.getElementById('scenario-pillars');
const scenarioDescriptionInput = document.getElementById('scenario-description-input');
const scenarioRuntimeHintInput = document.getElementById('scenario-runtime-hint');
const scenarioTicksInput = document.getElementById('scenario-ticks');
const scenarioEnableCodexInput = document.getElementById('scenario-enable-codex');
const scenarioEnablePfnaInput = document.getElementById('scenario-enable-pfna');
const scenarioRunIdInput = document.getElementById('scenario-run-id');
const scenarioGidInput = document.getElementById('scenario-gid');
const scenarioForm = document.getElementById('scenario-form');
const scenarioSaveButton = document.getElementById('scenario-save');
const scenarioActivateButton = document.getElementById('scenario-activate');
const pillarRunIdInput = document.getElementById('pillar-run-id');
const pillarRefreshButton = document.getElementById('refresh-pillars');
const pillarRunLabel = document.getElementById('pillar-run-label');
const pillarRunState = document.getElementById('pillar-run-state');
const pillarCards = document.getElementById('pillar-cards');
const pillarDetailName = document.getElementById('pillar-detail-name');
const pillarDetailStatus = document.getElementById('pillar-detail-status');
const pillarDetailBody = document.getElementById('pillar-detail-body');

const client = new GateClient(loadSavedBaseUrl());
baseUrlInput.value = client.baseUrl;
updateStatus(`Ready — using ${client.baseUrl}`);

let statePoll;
let logsPoll;
let latestState;
let scenarios = [];
let selectedScenarioId;
let pillarStatuses = [];
let selectedPillarId;
let governanceSnapshot;
let governanceDirty = false;
let budgetPolicies = [];
let historyEntries = [];
let diagnosticsArchive = [];
let selectedHistoryRunId;
let selectedDiagnosticId;
let logsCursor = 0;
let logEntries = [];
let logsActiveRunId = '';
let lastCurrentRunId = '';
let activeTab = tabs.find((tab) => tab.classList.contains('active'))?.dataset.tab || 'dashboard';

setScenarioFormEnabled(false);
renderPillars([], null);
renderBudgetPolicies([], { force: true });
renderHistoryDetail(null);
renderDiagnosticDetail(null);
renderHistoryList();
renderDiagnosticsArchive();
renderLogs('');

function updateStatus(text) {
  statusLine.textContent = text;
}

function formatTimestamp(value) {
  if (!value) return '—';
  try {
    const dt = new Date(value);
    return dt.toLocaleString();
  } catch (err) {
    return value;
  }
}

function setScenarioFormEnabled(enabled) {
  [
    scenarioDescriptionInput,
    scenarioRuntimeHintInput,
    scenarioTicksInput,
    scenarioEnableCodexInput,
    scenarioEnablePfnaInput,
    scenarioRunIdInput,
    scenarioGidInput,
    scenarioSaveButton,
    scenarioActivateButton,
  ].forEach((el) => {
    if (el) {
      el.disabled = !enabled;
    }
  });
}

function formatBudgetPolicies(policies) {
  if (!policies || !policies.length) return '—';
  return policies
    .map((policy) => {
      const actions =
        policy.max_actions_per_window ?? policy.max_proposals_per_window ?? policy.max_topology_changes;
      const suffix = actions === undefined ? '—' : actions;
      return `${policy.policy_id || 'policy'}: ${suffix}`;
    })
    .join(', ');
}

function formatMetrics(metrics) {
  if (!metrics) return '—';
  if (Array.isArray(metrics)) return metrics.join(', ');
  return Object.entries(metrics)
    .map(([key, value]) => `${key}: ${value}`)
    .join(', ');
}

function formatList(items) {
  if (!items || !items.length) return '—';
  return items.join(', ');
}

function renderRunStatus(status) {
  if (!status) {
    runStateEl.textContent = 'No active run';
    runIdEl.textContent = '—';
    runScenarioEl.textContent = '—';
    runStartedEl.textContent = '—';
    runFinishedEl.textContent = '—';
    stopRunButton.disabled = true;
    startRunButton.disabled = false;
    return;
  }

  runStateEl.textContent = status.state?.toUpperCase() || 'Unknown';
  runIdEl.textContent = status.run_id || '—';
  runScenarioEl.textContent = status.scenario_id || '—';
  runStartedEl.textContent = formatTimestamp(status.started_at);
  runFinishedEl.textContent = formatTimestamp(status.finished_at);

  const activeStates = new Set(['running', 'pending']);
  stopRunButton.disabled = !activeStates.has(status.state);
  startRunButton.disabled = activeStates.has(status.state);
}

function renderScenario(scenario) {
  if (!scenario) {
    scenarioTitleEl.textContent = 'Unknown';
    scenarioIdEl.textContent = '—';
    scenarioDescriptionEl.textContent = 'No active scenario available.';
    pillarListEl.innerHTML = '';
    return;
  }

  scenarioTitleEl.textContent = scenario.name || scenario.scenario_id || 'Scenario';
  scenarioIdEl.textContent = scenario.scenario_id || '—';
  scenarioDescriptionEl.textContent = scenario.description || 'Scenario description not provided.';
  runScenarioInput.value = scenario.scenario_id || '';

  pillarListEl.innerHTML = '';
  (scenario.pillars || []).forEach((pillar) => {
    const chip = document.createElement('span');
    chip.className = 'chip';
    chip.textContent = pillar;
    pillarListEl.appendChild(chip);
  });
}

function renderScenarioDetail(detail) {
  if (!detail) {
    scenarioDetailTitle.textContent = 'Select a scenario';
    scenarioDetailId.textContent = '—';
    scenarioDescriptionInput.value = '';
    scenarioRuntimeHintInput.value = '';
    scenarioTicksInput.value = '';
    scenarioEnableCodexInput.checked = false;
    scenarioEnablePfnaInput.checked = false;
    scenarioRunIdInput.value = '';
    scenarioGidInput.value = '';
    scenarioPillarsEl.innerHTML = '';
    setScenarioFormEnabled(false);
    return;
  }

  setScenarioFormEnabled(true);
  scenarioDetailTitle.textContent = detail.runtime_hint || detail.description || detail.scenario_id || 'Scenario';
  scenarioDetailId.textContent = detail.scenario_id || '—';
  scenarioDescriptionInput.value = detail.description || '';
  scenarioRuntimeHintInput.value = detail.runtime_hint || '';

  const runConfig = detail.run_config || {};
  scenarioTicksInput.value = runConfig.ticks ?? '';
  scenarioEnableCodexInput.checked = Boolean(runConfig.enable_codex);
  scenarioEnablePfnaInput.checked = Boolean(runConfig.enable_pfna);
  scenarioRunIdInput.value = runConfig.run_id || '';
  scenarioGidInput.value = runConfig.gid || '';

  scenarioPillarsEl.innerHTML = '';
  (detail.pillars || []).forEach((pillar) => {
    const chip = document.createElement('span');
    chip.className = 'chip';
    chip.textContent = pillar;
    scenarioPillarsEl.appendChild(chip);
  });

  runScenarioInput.value = detail.scenario_id || '';
}

function renderScenarioList(filterText = '') {
  scenarioListEl.innerHTML = '';
  const query = filterText.trim().toLowerCase();
  const activeScenarioId = latestState?.active_scenario?.scenario_id;

  const filtered = scenarios.filter((scenario) => {
    if (!query) return true;
    const haystack = `${scenario.scenario_id || ''} ${scenario.runtime_hint || ''} ${scenario.description || ''}`.toLowerCase();
    return haystack.includes(query);
  });

  if (!filtered.length) {
    const empty = document.createElement('li');
    empty.textContent = query ? 'No scenarios match your filter.' : 'No scenarios available.';
    scenarioListEl.appendChild(empty);
    return;
  }

  filtered.forEach((scenario) => {
    const li = document.createElement('li');
    const button = document.createElement('button');
    const title = document.createElement('div');
    title.textContent = scenario.scenario_id || 'Scenario';
    const meta = document.createElement('div');
    meta.className = 'small';
    meta.textContent = scenario.runtime_hint || scenario.description || '—';
    button.appendChild(title);
    button.appendChild(meta);
    button.addEventListener('click', () => selectScenario(scenario.scenario_id));

    const right = document.createElement('div');
    if (scenario.scenario_id === activeScenarioId) {
      const badge = document.createElement('span');
      badge.className = 'chip';
      badge.textContent = 'Active';
      right.appendChild(badge);
    }

    li.appendChild(button);
    li.appendChild(right);
    if (scenario.scenario_id === selectedScenarioId) {
      li.classList.add('active');
    }
    scenarioListEl.appendChild(li);
  });
}

async function loadScenarioDetail(scenarioId) {
  if (!scenarioId) {
    renderScenarioDetail(null);
    return;
  }
  try {
    renderScenarioDetail(null);
    scenarioDetailTitle.textContent = 'Loading scenario...';
    const detail = await client.getScenario(scenarioId);
    renderScenarioDetail(detail);
  } catch (err) {
    updateStatus(`Failed to load scenario: ${err.message}`);
  }
}

async function loadScenarios(preferredId) {
  try {
    const list = await client.listScenarios();
    scenarios = Array.isArray(list) ? list : [];
    renderScenarioList(scenarioSearchInput.value);
    const defaultId =
      preferredId || latestState?.active_scenario?.scenario_id || scenarios[0]?.scenario_id || selectedScenarioId;
    if (defaultId) {
      await selectScenario(defaultId);
    }
  } catch (err) {
    scenarios = [];
    renderScenarioList('');
    updateStatus(`Failed to load scenarios: ${err.message}`);
  }
}

async function selectScenario(scenarioId) {
  if (!scenarioId || scenarioId === selectedScenarioId) return;
  selectedScenarioId = scenarioId;
  renderScenarioList(scenarioSearchInput.value);
  await loadScenarioDetail(scenarioId);
}

async function selectHistory(runId) {
  if (!runId) {
    renderHistoryDetail(null);
    return;
  }

  selectedHistoryRunId = runId;
  renderHistoryList();
  try {
    const detail = await client.getHistoryEntry(runId);
    renderHistoryDetail(detail);
    if (!logsRunInput.value) {
      logsRunInput.value = runId;
    }
    logEntries = [];
    logsCursor = 0;
    await loadLogs({ reset: true });
  } catch (err) {
    updateStatus(`Failed to load history entry: ${err.message}`);
  }
}

function exportHistoryBundle() {
  const runId = (selectedHistoryRunId || historyRunId.textContent || '').trim();
  if (!runId || runId === '—') {
    updateStatus('Select a completed run to export.');
    return;
  }

  const url = client.exportHistoryEntry(runId);
  if (historyExportButton) historyExportButton.disabled = true;
  setTimeout(() => {
    if (historyExportButton) historyExportButton.disabled = false;
  }, 400);
  window.open(url, '_blank');
}

async function selectDiagnostic(diagnosticId) {
  if (!diagnosticId) {
    renderDiagnosticDetail(null);
    return;
  }

  selectedDiagnosticId = diagnosticId;
  renderDiagnosticsArchive();
  try {
    const detail = await client.getDiagnosticsRun(diagnosticId);
    renderDiagnosticDetail(detail);
    const linkedRun = detail.related_run_ids?.[0];
    if (linkedRun && !logsRunInput.value) {
      logsRunInput.value = linkedRun;
    }
  } catch (err) {
    updateStatus(`Failed to load diagnostics: ${err.message}`);
  }
}

async function loadHistory(preferredRunId) {
  try {
    const payload = await client.listHistory();
    historyEntries = payload.entries || payload.history || [];
    diagnosticsArchive = payload.diagnostics || diagnosticsArchive;
    renderHistoryList();
    renderDiagnosticsArchive();

    const defaultRun = preferredRunId || selectedHistoryRunId || historyEntries[0]?.run_id;
    if (defaultRun) {
      await selectHistory(defaultRun);
    } else {
      renderHistoryDetail(null);
    }

    const defaultDiag = selectedDiagnosticId || diagnosticsArchive[0]?.diagnostic_id;
    if (defaultDiag) {
      await selectDiagnostic(defaultDiag);
    } else {
      renderDiagnosticDetail(null);
    }
  } catch (err) {
    historyEntries = [];
    diagnosticsArchive = [];
    renderHistoryList();
    renderDiagnosticsArchive();
    renderHistoryDetail(null);
    renderDiagnosticDetail(null);
    updateStatus(`Failed to load history: ${err.message}`);
  }
}

function renderGovernanceSummary(governance) {
  const mode = governance?.governance_mode || governance?.mode || '—';
  const codex = governance?.codex_action_mode || '—';
  const budgets = governance?.budget_policies || [];

  governanceModeEl.textContent = mode;
  governanceCodexEl.textContent = `Codex ${codex}`;
  governanceBudgetsEl.textContent = formatBudgetPolicies(budgets);

  if (governanceSummaryMode) governanceSummaryMode.textContent = mode;
  if (governanceSummaryCodex) governanceSummaryCodex.textContent = `Codex ${codex}`;
  if (governanceSummaryBudgets) {
    governanceSummaryBudgets.innerHTML = '';
    if (!budgets.length) {
      const empty = document.createElement('li');
      empty.textContent = 'No budget policies set yet.';
      governanceSummaryBudgets.appendChild(empty);
    } else {
      budgets.forEach((policy) => {
        const li = document.createElement('li');
        const title = document.createElement('div');
        title.textContent = policy.policy_id || 'policy';
        const meta = document.createElement('div');
        meta.className = 'small';
        const max =
          policy.max_actions_per_window ??
          policy.max_proposals_per_window ??
          policy.max_topology_changes ??
          '—';
        meta.textContent = `Actions/window: ${max}`;
        li.appendChild(title);
        li.appendChild(meta);
        governanceSummaryBudgets.appendChild(li);
      });
    }
  }
}

function renderBudgetPolicies(policies, { force = false } = {}) {
  if (!force && governanceDirty) return;
  budgetPolicies = Array.isArray(policies) ? policies.map((p) => ({ ...p })) : [];

  budgetPoliciesEl.innerHTML = '';

  if (!budgetPolicies.length) {
    const empty = document.createElement('div');
    empty.className = 'empty';
    empty.textContent = 'No budget policies defined. Add one to set limits for Codex actions.';
    budgetPoliciesEl.appendChild(empty);
    return;
  }

  budgetPolicies.forEach((policy, index) => {
    const row = document.createElement('div');
    row.className = 'budget-row';
    row.dataset.index = String(index);

    const header = document.createElement('div');
    header.className = 'control-row';
    const policyLabel = document.createElement('label');
    policyLabel.textContent = 'Policy ID';
    const policyInput = document.createElement('input');
    policyInput.type = 'text';
    policyInput.value = policy.policy_id || '';
    policyInput.dataset.field = 'policy_id';
    policyInput.required = true;
    policyLabel.appendChild(policyInput);
    header.appendChild(policyLabel);

    const remove = document.createElement('button');
    remove.type = 'button';
    remove.className = 'ghost';
    remove.textContent = 'Remove';
    remove.addEventListener('click', () => {
      budgetPolicies.splice(index, 1);
      governanceDirty = true;
      renderBudgetPolicies(budgetPolicies, { force: true });
    });
    header.appendChild(remove);
    row.appendChild(header);

    const metrics = document.createElement('div');
    metrics.className = 'budget-grid';

    const actionsLabel = document.createElement('label');
    actionsLabel.textContent = 'Max actions/window';
    const actionsInput = document.createElement('input');
    actionsInput.type = 'number';
    actionsInput.min = '0';
    actionsInput.value = policy.max_actions_per_window ?? '';
    actionsInput.dataset.field = 'max_actions_per_window';
    actionsLabel.appendChild(actionsInput);
    metrics.appendChild(actionsLabel);

    const proposalsLabel = document.createElement('label');
    proposalsLabel.textContent = 'Max proposals/window';
    const proposalsInput = document.createElement('input');
    proposalsInput.type = 'number';
    proposalsInput.min = '0';
    proposalsInput.value = policy.max_proposals_per_window ?? '';
    proposalsInput.dataset.field = 'max_proposals_per_window';
    proposalsLabel.appendChild(proposalsInput);
    metrics.appendChild(proposalsLabel);

    const topologyLabel = document.createElement('label');
    topologyLabel.textContent = 'Max topology changes';
    const topologyInput = document.createElement('input');
    topologyInput.type = 'number';
    topologyInput.min = '0';
    topologyInput.value = policy.max_topology_changes ?? '';
    topologyInput.dataset.field = 'max_topology_changes';
    topologyLabel.appendChild(topologyInput);
    metrics.appendChild(topologyLabel);

    row.appendChild(metrics);

    const notesLabel = document.createElement('label');
    notesLabel.textContent = 'Notes';
    const notesInput = document.createElement('input');
    notesInput.type = 'text';
    notesInput.value = policy.notes || '';
    notesInput.dataset.field = 'notes';
    notesLabel.appendChild(notesInput);
    row.appendChild(notesLabel);

    [policyInput, actionsInput, proposalsInput, topologyInput, notesInput].forEach((input) => {
      input.addEventListener('input', () => {
        governanceDirty = true;
      });
    });

    budgetPoliciesEl.appendChild(row);
  });
}

function renderGovernanceForm(governance, { force = false } = {}) {
  if (!force && governanceDirty) return;
  governanceSnapshot = governance || null;
  governanceDirty = false;
  governanceErrorEl.textContent = '';

  const mode = governance?.governance_mode || governance?.mode || '';
  const codex = governance?.codex_action_mode || '';
  if (governanceModeInput) governanceModeInput.value = mode;
  if (governanceCodexInput) governanceCodexInput.value = codex;

  budgetPolicies = Array.isArray(governance?.budget_policies)
    ? governance.budget_policies.map((policy) => ({ ...policy }))
    : [];
  renderBudgetPolicies(budgetPolicies, { force: true });
}

function renderGovernanceSnapshot(governance, { forceForm = false } = {}) {
  renderGovernanceSummary(governance);
  renderGovernanceForm(governance, { force: forceForm });
}

function renderDiagnostics(current, history) {
  if (current) {
    diagnosticStateEl.textContent = current.state || 'RUNNING';
    diagnosticIdEl.textContent = current.diagnostic_id || '—';
  } else {
    diagnosticStateEl.textContent = 'Idle';
    diagnosticIdEl.textContent = '—';
  }

  diagnosticHistoryList.innerHTML = '';
  (history || []).forEach((entry) => {
    const li = document.createElement('li');
    const label = document.createElement('div');
    label.textContent = `${entry.profile_id || 'Profile'} — ${entry.state || 'Unknown'}`;
    const meta = document.createElement('div');
    meta.className = 'small';
    const runs = (entry.related_run_ids || []).join(', ');
    meta.textContent = `${entry.diagnostic_id || 'diag'} · runs: ${runs || '—'}`;
    li.appendChild(label);
    li.appendChild(meta);
    diagnosticHistoryList.appendChild(li);
  });
}

function renderHistoryDetail(detail) {
  if (!detail) {
    historyDetailTitle.textContent = 'Select a run';
    historyRunId.textContent = '—';
    historyScenario.textContent = '—';
    historyResult.textContent = '—';
    historyStarted.textContent = '—';
    historyFinished.textContent = '—';
    historyTicks.textContent = '—';
    historyGovernance.textContent = '—';
    historyMetrics.textContent = '—';
    historyPillars.textContent = '—';
    if (historyExportButton) historyExportButton.disabled = true;
    return;
  }

  const status = detail.run || {};
  historyDetailTitle.textContent = status.state ? status.state.toUpperCase() : 'Run detail';
  historyRunId.textContent = status.run_id || '—';
  historyScenario.textContent = status.scenario_id || '—';
  historyResult.textContent = status.state || detail.result || '—';
  historyStarted.textContent = formatTimestamp(status.started_at || detail.started_at);
  historyFinished.textContent = formatTimestamp(status.finished_at || detail.ended_at);
  historyTicks.textContent = status.ticks_total ?? detail.ticks_total ?? '—';
  if (historyExportButton) historyExportButton.disabled = !status.run_id;

  const governance = detail.governance || {};
  const mode = governance.governance_mode || governance.mode;
  const codex = governance.codex_action_mode;
  const budgets = governance.budget_policies;
  const govParts = [mode, codex ? `Codex ${codex}` : null, formatBudgetPolicies(budgets)].filter(Boolean);
  historyGovernance.textContent = govParts.length ? govParts.join(' · ') : '—';

  historyMetrics.textContent = formatMetrics(detail.metrics || detail.summary_metrics);
  const pillars = detail.pillars || status.pillars || [];
  if (!pillars.length) {
    historyPillars.textContent = '—';
  } else {
    historyPillars.textContent = '';
    pillars.forEach((pillar) => {
      const chip = document.createElement('span');
      chip.className = 'chip';
      chip.textContent = pillar;
      historyPillars.appendChild(chip);
    });
  }
}

function renderHistoryList() {
  historyListEl.innerHTML = '';
  if (!historyEntries.length) {
    const empty = document.createElement('li');
    empty.textContent = 'No history yet. Completed runs will appear here.';
    historyListEl.appendChild(empty);
    return;
  }

  historyEntries.forEach((entry) => {
    const li = document.createElement('li');
    const button = document.createElement('button');
    const title = document.createElement('div');
    title.textContent = `${entry.run_id || 'run'} — ${entry.result || entry.status?.state || ''}`.trim();
    const meta = document.createElement('div');
    meta.className = 'small';
    meta.textContent = `${entry.scenario_id || 'scenario'} · ${formatTimestamp(entry.started_at)}`;
    button.appendChild(title);
    button.appendChild(meta);
    button.addEventListener('click', () => selectHistory(entry.run_id));
    li.appendChild(button);

    if (entry.run_id === selectedHistoryRunId) {
      li.classList.add('active');
    }

    historyListEl.appendChild(li);
  });
}

function renderDiagnosticsArchive() {
  diagnosticsArchiveList.innerHTML = '';
  if (!diagnosticsArchive.length) {
    const empty = document.createElement('li');
    empty.textContent = 'No diagnostics history yet.';
    diagnosticsArchiveList.appendChild(empty);
    return;
  }

  diagnosticsArchive.forEach((entry) => {
    const li = document.createElement('li');
    const button = document.createElement('button');
    const title = document.createElement('div');
    title.textContent = `${entry.diagnostic_id || 'diag'} — ${entry.state || 'unknown'}`;
    const meta = document.createElement('div');
    meta.className = 'small';
    const runs = formatList(entry.related_run_ids || []);
    meta.textContent = `${entry.profile_id || 'profile'} · runs: ${runs}`;
    button.appendChild(title);
    button.appendChild(meta);
    button.addEventListener('click', () => selectDiagnostic(entry.diagnostic_id));
    li.appendChild(button);
    if (entry.diagnostic_id === selectedDiagnosticId) {
      li.classList.add('active');
    }
    diagnosticsArchiveList.appendChild(li);
  });
}

function renderDiagnosticDetail(detail) {
  if (!detail) {
    diagnosticDetailTitle.textContent = 'Select a diagnostics run';
    diagnosticDetailId.textContent = '—';
    diagnosticDetailProfile.textContent = '—';
    diagnosticDetailState.textContent = '—';
    diagnosticDetailRuns.textContent = '—';
    diagnosticChecksEl.innerHTML = '';
    return;
  }

  const status = detail.status || {};
  diagnosticDetailTitle.textContent = status.state ? status.state.toUpperCase() : 'Diagnostics detail';
  diagnosticDetailId.textContent = status.diagnostic_id || '—';
  diagnosticDetailProfile.textContent = status.profile_id || '—';
  diagnosticDetailState.textContent = status.state || '—';
  diagnosticDetailRuns.textContent = formatList(detail.related_run_ids);

  diagnosticChecksEl.innerHTML = '';
  if (!detail.checks || !detail.checks.length) {
    const empty = document.createElement('div');
    empty.className = 'empty';
    empty.textContent = 'No checks recorded.';
    diagnosticChecksEl.appendChild(empty);
    return;
  }

  detail.checks.forEach((check) => {
    const panel = document.createElement('div');
    panel.className = 'check';
    const title = document.createElement('div');
    title.className = 'title';
    title.textContent = check.name || check.id || 'Check';
    const statusEl = document.createElement('span');
    statusEl.className = 'chip';
    statusEl.textContent = check.state || 'UNKNOWN';
    const desc = document.createElement('div');
    desc.className = 'desc';
    desc.textContent = check.description || check.message || '';
    title.appendChild(statusEl);
    panel.appendChild(title);
    panel.appendChild(desc);
    if (check.message) {
      const note = document.createElement('div');
      note.className = 'small';
      note.textContent = check.message;
      panel.appendChild(note);
    }
    diagnosticChecksEl.appendChild(panel);
  });
}

function renderLogs(runId) {
  logsCursorEl.textContent = logsCursor;
  logsListEl.innerHTML = '';

  if (!runId) {
    const empty = document.createElement('div');
    empty.className = 'empty';
    empty.textContent = 'Enter a run ID to view logs.';
    logsListEl.appendChild(empty);
    return;
  }

  if (!logEntries.length) {
    const empty = document.createElement('div');
    empty.className = 'empty';
    empty.textContent = 'No logs available yet.';
    logsListEl.appendChild(empty);
    return;
  }

  logEntries.forEach((entry) => {
    const row = document.createElement('div');
    row.className = 'log-entry';
    const meta = document.createElement('div');
    meta.className = 'meta';
    const ts = document.createElement('div');
    ts.textContent = formatTimestamp(entry.ts || entry.timestamp);
    const level = document.createElement('div');
    level.textContent = entry.payload?.level || 'INFO';
    const eventType = document.createElement('div');
    eventType.textContent = entry.event || 'event';
    meta.appendChild(ts);
    meta.appendChild(level);
    meta.appendChild(eventType);
    const message = document.createElement('div');
    message.className = 'message';
    const payload = entry.payload || {};
    const text = payload.message || payload.msg || JSON.stringify(payload);
    message.textContent = text;
    row.appendChild(meta);
    row.appendChild(message);
    logsListEl.appendChild(row);
  });

  if (logsAutoscrollInput?.checked) {
    logsListEl.scrollTop = logsListEl.scrollHeight;
  }
}

function collectBudgetPolicies() {
  const rows = Array.from(budgetPoliciesEl.querySelectorAll('.budget-row'));
  return rows
    .map((row) => {
      const policy = {};
      row.querySelectorAll('[data-field]').forEach((input) => {
        const field = input.dataset.field;
        const value = input.value.trim();
        if (!value) return;
        if (['max_actions_per_window', 'max_proposals_per_window', 'max_topology_changes'].includes(field)) {
          const parsed = Number(value);
          if (!Number.isNaN(parsed)) {
            policy[field] = parsed;
          }
          return;
        }
        policy[field] = value;
      });
      return policy;
    })
    .filter((policy) => policy.policy_id);
}

async function loadGovernance(forceForm = false) {
  try {
    const response = await client.getGovernance();
    renderGovernanceSnapshot(response?.governance || response, { forceForm });
  } catch (err) {
    updateStatus(`Failed to load governance: ${err.message}`);
  }
}

function renderPillarDetail(pillar) {
  pillarDetailBody.innerHTML = '';

  if (!pillar) {
    pillarDetailName.textContent = 'Select a pillar';
    pillarDetailStatus.textContent = '—';
    const empty = document.createElement('div');
    empty.className = 'empty';
    empty.textContent = 'Choose a pillar card to see metrics.';
    pillarDetailBody.appendChild(empty);
    return;
  }

  pillarDetailName.textContent = pillar.name || pillar.pillar_id || 'Pillar';
  pillarDetailStatus.textContent = pillar.status ? pillar.status.toUpperCase() : '—';

  const metrics = document.createElement('div');
  metrics.className = 'metric-list';

  const headline = document.createElement('div');
  headline.className = 'metric';
  const headlineLabel = document.createElement('div');
  headlineLabel.className = 'label';
  headlineLabel.textContent = pillar.headline_metric_label || 'Metric';
  const headlineValue = document.createElement('div');
  headlineValue.className = 'value';
  headlineValue.textContent = pillar.headline_metric_value ?? '—';
  headline.appendChild(headlineLabel);
  headline.appendChild(headlineValue);
  metrics.appendChild(headline);

  (pillar.secondary_metrics || []).forEach((metric) => {
    const item = document.createElement('div');
    item.className = 'metric';
    const label = document.createElement('div');
    label.className = 'label';
    label.textContent = metric.label || 'Metric';
    const value = document.createElement('div');
    value.className = 'value';
    value.textContent = metric.value ?? '—';
    item.appendChild(label);
    item.appendChild(value);
    metrics.appendChild(item);
  });

  pillarDetailBody.appendChild(metrics);
}

function renderPillars(pillars, runStatus) {
  pillarRunLabel.textContent = runStatus?.run_id || pillarRunIdInput.value || 'No run selected';
  pillarRunState.textContent = runStatus?.state ? runStatus.state.toUpperCase() : '—';

  pillarCards.innerHTML = '';

  if (!pillars || pillars.length === 0) {
    const empty = document.createElement('div');
    empty.className = 'empty';
    empty.textContent = 'No pillar status available yet.';
    pillarCards.appendChild(empty);
    renderPillarDetail(null);
    return;
  }

  const hasSelection = pillars.some((p) => p.pillar_id === selectedPillarId);
  if (!hasSelection) {
    selectedPillarId = pillars[0].pillar_id;
  }

  pillars.forEach((pillar) => {
    const card = document.createElement('div');
    card.className = 'pillar-card';
    if (pillar.pillar_id === selectedPillarId) {
      card.classList.add('active');
    }

    const headline = document.createElement('div');
    headline.className = 'headline';
    headline.textContent = pillar.name || pillar.pillar_id || 'Pillar';

    const status = document.createElement('span');
    status.className = 'status-chip';
    status.textContent = pillar.status ? pillar.status.toUpperCase() : 'UNKNOWN';

    const metric = document.createElement('div');
    metric.className = 'metric';
    metric.textContent = `${pillar.headline_metric_label || 'Metric'}: ${pillar.headline_metric_value ?? '—'}`;

    card.appendChild(headline);
    card.appendChild(status);
    card.appendChild(metric);
    card.addEventListener('click', () => {
      selectedPillarId = pillar.pillar_id;
      renderPillars(pillars, runStatus);
    });
    pillarCards.appendChild(card);
  });

  const selected = pillars.find((p) => p.pillar_id === selectedPillarId);
  renderPillarDetail(selected || pillars[0]);
}

async function loadPillars(preferredRunId) {
  const runId = preferredRunId || pillarRunIdInput.value.trim() || latestState?.current_run?.run_id;
  if (runId) {
    pillarRunIdInput.value = runId;
  }

  if (!runId) {
    pillarStatuses = [];
    renderPillars([], latestState?.current_run);
    return;
  }

  try {
    updateStatus(`Loading pillars for ${runId}...`);
    const response = await client.getRunPillars(runId);
    pillarStatuses = response?.pillars || [];
    renderPillars(pillarStatuses, latestState?.current_run || { run_id: runId });
    updateStatus(`Pillars refreshed for ${runId}.`);
  } catch (err) {
    pillarStatuses = [];
    renderPillars([], latestState?.current_run);
    updateStatus(`Failed to load pillars: ${err.message}`);
  }
}

async function refreshState() {
  try {
    const [state, diagnostics] = await Promise.all([client.state(), client.listDiagnostics().catch(() => null)]);
    latestState = state;
    renderRunStatus(state.current_run);
    renderScenario(state.active_scenario);
    renderGovernanceSnapshot(state.governance);
    renderDiagnostics(state.diagnostics?.current, diagnostics?.entries);
    if (state.current_run?.run_id && !pillarRunIdInput.value) {
      pillarRunIdInput.value = state.current_run.run_id;
    }
    if (Array.isArray(state.pillars)) {
      pillarStatuses = state.pillars;
      renderPillars(pillarStatuses, state.current_run);
    }
    if (logsFollowCurrentInput?.checked && state.current_run?.run_id !== lastCurrentRunId) {
      loadLogs({ reset: true });
    }
    lastCurrentRunId = state.current_run?.run_id || '';
    renderScenarioList(scenarioSearchInput.value);
    updateStatus(`Connected — ${state.active_scenario?.name || state.active_scenario?.scenario_id || 'ready'}`);
  } catch (err) {
    updateStatus(`Failed to refresh state: ${err.message}`);
    clearInterval(statePoll);
    statePoll = undefined;
  }
}

async function loadLogs({ reset = false } = {}) {
  const followCurrent = logsFollowCurrentInput?.checked;
  const currentRunId = latestState?.current_run?.run_id;
  let runId = (logsRunInput.value || selectedHistoryRunId || '').trim();

  if (followCurrent && currentRunId) {
    runId = currentRunId;
  } else if (!runId && currentRunId) {
    runId = currentRunId;
  }

  if (runId && runId !== logsActiveRunId && !reset) {
    reset = true;
  }

  if (!runId) {
    logsActiveRunId = '';
    renderLogs('');
    return;
  }

  if (reset) {
    logsCursor = 0;
    logEntries = [];
  }

  logsRunInput.value = runId;

  const options = { cursor: logsCursor };
  const level = logsLevelSelect?.value;
  const eventType = logsEventInput?.value.trim();
  if (level) options.level = level;
  if (eventType) options.event_type = eventType;

  try {
    const response = await client.getRunLogs(runId, options);
    const entries = response.entries || [];
    const nextCursor = response.cursor ?? logsCursor;
    logEntries = reset ? entries : logEntries.concat(entries);
    logsCursor = nextCursor;
    logsActiveRunId = runId;
    renderLogs(runId);
    updateStatus(`Loaded ${entries.length} log entries for ${runId}.`);
  } catch (err) {
    updateStatus(`Failed to load logs: ${err.message}`);
  }
}

async function probeConnection() {
  try {
    updateStatus(`Checking service at ${client.baseUrl}...`);
    const state = await client.state();
    const scenarioLabel = state?.active_scenario?.name || state?.active_scenario?.scenario_id || 'no active scenario';
    updateStatus(`Connected — ${scenarioLabel}`);
    renderScenario(state.active_scenario);
    renderGovernanceSnapshot(state.governance, { forceForm: true });
    renderRunStatus(state.current_run);
    if (Array.isArray(state.pillars)) {
      pillarStatuses = state.pillars;
      renderPillars(pillarStatuses, state.current_run);
    }
    if (state.current_run?.run_id) {
      pillarRunIdInput.value = pillarRunIdInput.value || state.current_run.run_id;
    }
    await loadScenarios(state?.active_scenario?.scenario_id);
    await loadHistory();
    if (!statePoll) {
      statePoll = setInterval(refreshState, 4000);
    }
    if (pillarRunIdInput.value) {
      loadPillars(pillarRunIdInput.value);
    }
    refreshState();
  } catch (err) {
    updateStatus(`Failed to reach service: ${err.message}`);
    clearInterval(statePoll);
    statePoll = undefined;
  }
}

function activateTab(tabId) {
  tabs.forEach((tab) => {
    const active = tab.dataset.tab === tabId;
    tab.classList.toggle('active', active);
  });
  panels.forEach((panel) => {
    const active = panel.id === tabId;
    panel.classList.toggle('active', active);
    if (active) {
      panel.focus();
    }
  });
  activeTab = tabId;
  if (tabId === 'logs') {
    loadLogs({ reset: true });
    startLogsPoll();
  } else {
    stopLogsPoll();
  }
}

function startLogsPoll() {
  stopLogsPoll();
  if (activeTab !== 'logs') return;
  logsPoll = setInterval(() => loadLogs(), 3000);
}

function stopLogsPoll() {
  if (logsPoll) {
    clearInterval(logsPoll);
    logsPoll = undefined;
  }
}

saveEndpointButton.addEventListener('click', () => {
  const normalised = saveBaseUrl(baseUrlInput.value.trim());
  client.setBaseUrl(normalised);
  updateStatus(`Saved endpoint — ${normalised}`);
  probeConnection();
  loadDiagnosticsProfiles();
});

tabs.forEach((tab) => {
  tab.addEventListener('click', (event) => {
    const target = event.currentTarget;
    activateTab(target.dataset.tab);
  });
});

pillarRefreshButton?.addEventListener('click', () => {
  loadPillars();
});

historyRefreshButton?.addEventListener('click', () => {
  loadHistory(selectedHistoryRunId);
});

logsRefreshButton?.addEventListener('click', () => {
  loadLogs({ reset: true });
});

logsMoreButton?.addEventListener('click', () => {
  loadLogs();
});

logsRunInput?.addEventListener('change', () => {
  loadLogs({ reset: true });
});

logsLevelSelect?.addEventListener('change', () => {
  loadLogs({ reset: true });
});

logsEventInput?.addEventListener('change', () => {
  loadLogs({ reset: true });
});

logsFollowCurrentInput?.addEventListener('change', () => {
  if (logsFollowCurrentInput.checked) {
    loadLogs({ reset: true });
    startLogsPoll();
  } else {
    stopLogsPoll();
  }
});

logsAutoscrollInput?.addEventListener('change', () => {
  renderLogs(logsActiveRunId);
});

historyExportButton?.addEventListener('click', exportHistoryBundle);

startRunForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  startRunButton.disabled = true;
  const scenarioId = runScenarioInput.value.trim();
  const ticks = runTicksInput.value ? Number(runTicksInput.value) : undefined;
  const payload = { scenario_id: scenarioId };
  if (ticks && Number.isFinite(ticks)) {
    payload.overrides = { ticks };
  }

  try {
    updateStatus(`Starting run for ${scenarioId}...`);
    const status = await client.startRun(payload);
    latestState = { ...(latestState || {}), current_run: status };
    renderRunStatus(status);
    pillarRunIdInput.value = status.run_id || pillarRunIdInput.value;
    loadPillars(status.run_id);
    updateStatus(`Run ${status.run_id} started.`);
    refreshState();
  } catch (err) {
    updateStatus(`Failed to start run: ${err.message}`);
  } finally {
    if (!latestState?.current_run) {
      startRunButton.disabled = false;
    }
  }
});

stopRunButton.addEventListener('click', async () => {
  if (!latestState?.current_run) return;
  const runId = latestState.current_run.run_id;
  stopRunButton.disabled = true;
  try {
    updateStatus(`Requesting stop for ${runId}...`);
    await client.stopRun(runId);
    refreshState();
  } catch (err) {
    updateStatus(`Failed to stop run: ${err.message}`);
  }
});

scenarioSearchInput?.addEventListener('input', (event) => {
  renderScenarioList(event.target.value);
});

scenarioRefreshButton?.addEventListener('click', () => {
  loadScenarios(selectedScenarioId);
});

scenarioForm?.addEventListener('submit', async (event) => {
  event.preventDefault();
  if (!selectedScenarioId) return;
  scenarioSaveButton.disabled = true;

  const payload = {
    description: scenarioDescriptionInput.value.trim(),
    runtime_hint: scenarioRuntimeHintInput.value.trim(),
    ticks: scenarioTicksInput.value ? Number(scenarioTicksInput.value) : undefined,
    enable_codex: scenarioEnableCodexInput.checked,
    enable_pfna: scenarioEnablePfnaInput.checked,
    run_id: scenarioRunIdInput.value.trim() || undefined,
    gid: scenarioGidInput.value.trim() || undefined,
  };

  if (!payload.ticks) {
    delete payload.ticks;
  }

  try {
    updateStatus(`Saving ${selectedScenarioId}...`);
    const detail = await client.updateScenario(selectedScenarioId, payload);
    renderScenarioDetail(detail);
    updateStatus(`Saved ${selectedScenarioId}.`);
    refreshState();
  } catch (err) {
    updateStatus(`Failed to save scenario: ${err.message}`);
  } finally {
    scenarioSaveButton.disabled = false;
  }
});

scenarioActivateButton?.addEventListener('click', async () => {
  if (!selectedScenarioId) return;
  scenarioActivateButton.disabled = true;
  try {
    updateStatus(`Activating ${selectedScenarioId}...`);
    await client.activateScenario(selectedScenarioId);
    await refreshState();
    loadScenarios(selectedScenarioId);
    updateStatus(`Activated ${selectedScenarioId}.`);
  } catch (err) {
    updateStatus(`Failed to activate scenario: ${err.message}`);
  } finally {
    scenarioActivateButton.disabled = false;
  }
});

if (governanceModeInput) {
  governanceModeInput.addEventListener('input', () => {
    governanceDirty = true;
  });
}

if (governanceCodexInput) {
  governanceCodexInput.addEventListener('input', () => {
    governanceDirty = true;
  });
}

addBudgetButton?.addEventListener('click', () => {
  budgetPolicies.push({ policy_id: `policy-${budgetPolicies.length + 1}` });
  governanceDirty = true;
  renderBudgetPolicies(budgetPolicies, { force: true });
});

governanceResetButton?.addEventListener('click', () => {
  renderGovernanceForm(governanceSnapshot, { force: true });
});

governanceRefreshButton?.addEventListener('click', () => {
  loadGovernance(true);
});

governanceForm?.addEventListener('submit', async (event) => {
  event.preventDefault();
  governanceSaveButton.disabled = true;
  governanceErrorEl.textContent = '';

  const payload = {};
  const mode = governanceModeInput?.value.trim();
  const codex = governanceCodexInput?.value.trim();
  if (mode) payload.governance_mode = mode;
  if (codex) payload.codex_action_mode = codex;

  const policies = collectBudgetPolicies();
  if (policies.length) {
    payload.budget_policies = policies;
  }

  try {
    updateStatus('Saving governance...');
    const response = await client.updateGovernance(payload);
    const snapshot = response?.governance || response;
    renderGovernanceSnapshot(snapshot, { forceForm: true });
    governanceDirty = false;
    updateStatus('Governance saved.');
  } catch (err) {
    governanceErrorEl.textContent = err.message;
    updateStatus(`Failed to save governance: ${err.message}`);
  } finally {
    governanceSaveButton.disabled = false;
  }
});

diagnosticForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const profileId = diagnosticProfileSelect.value;
  try {
    updateStatus(`Starting diagnostics ${profileId}...`);
    const result = await client.startDiagnostics({ profile_id: profileId });
    diagnosticStateEl.textContent = result.state || 'RUNNING';
    diagnosticIdEl.textContent = result.diagnostic_id || '—';
    refreshState();
  } catch (err) {
    updateStatus(`Diagnostics failed to start: ${err.message}`);
  }
});

async function loadDiagnosticsProfiles() {
  try {
    const profiles = await client.getDiagnosticsProfiles();
    diagnosticProfileSelect.innerHTML = '';
    profiles.forEach((profile) => {
      const option = document.createElement('option');
      option.value = profile.id;
      option.textContent = `${profile.id} — ${profile.description || ''}`.trim();
      diagnosticProfileSelect.appendChild(option);
    });
  } catch (err) {
    diagnosticProfileSelect.innerHTML = '';
    const option = document.createElement('option');
    option.value = 'SMOKE';
    option.textContent = 'SMOKE';
    diagnosticProfileSelect.appendChild(option);
    updateStatus(`Diagnostics profiles unavailable: ${err.message}`);
  }
}

// Initial connectivity check on load.
probeConnection();
loadDiagnosticsProfiles();
loadScenarios();
loadHistory();
