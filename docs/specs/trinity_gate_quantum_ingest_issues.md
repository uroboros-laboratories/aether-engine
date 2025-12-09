## Epic: Trinity Gate — Real Quantum Data Ingest

---

### 🔧 Issue 1: Build Dual-Source Quantum Data Loader

**Title**: Implement dual-source quantum statevector loader (real/simulated)

**Description**:
- Create a module (`quantum_loader.py`) that:
  - Fetches real data from IBM Quantum (`ibmq_lima`, 5 qubits max)
  - Falls back to Qiskit Aer simulation when offline
  - Returns normalized statevector `ψ ∈ ℂⁿ` (unit norm)

**Acceptance Criteria**:
- Works with/without IBM token
- Logs backend used (real/simulated)
- Returns `np.array(complex)` of shape (4,) or (8,) depending on qubits used

---

### 🔧 Issue 2: Quantize Quantum State into TBP Format

**Title**: Encode quantum state into TBP (mass + phase + residual) format

**Description**:
- Implement `quantize_statevector(ψ, η, P)` to:
  - Apply magnitude quantization: `m_i = floor(η * |ψ_i|²)`
  - Bin phase: `p_i ∈ [0, P-1]` via wrap+bin
  - Store per-state residual: `Q0.32` as `r_i = floor((η|ψ_i|² - m_i) * 2³²)`
- Must match Trinity Gate canonical L0 format

**Acceptance Criteria**:
- Function passes test vectors from TBP fixtures (F1–F3)
- Output is dictionary with keys: `masses`, `phases`, `residuals`, `eta`, `P`

---

### 🔧 Issue 3: Wire TBP Quantum Payload into Test Harness

**Title**: Inject quantized quantum payload into Trinity Gate test harness

**Description**:
- Add test case in Trinity Gate test suite:
  - Calls quantum loader + quantizer
  - Feeds output into `engine.inject_quantum_payload(payload)`
  - Advances 1 tick, checks state update and NAP output

**Acceptance Criteria**:
- Tick completes with no runtime errors
- NAP envelope and internal ledger reflect tick + quantization metadata

---

### 🔧 Issue 4: Validate TBP Fidelity Metrics from Fixtures

**Title**: Compute and assert TBP fidelity metrics (Prob‑L1, Amp‑L2)

**Description**:
- Implement canonical fidelity checks from spec:
  - Prob-L1 = ∑|p_i - p̂_i|
  - Amp-L2 = √(∑|ψ_i - ψ̂_i|²)
- Use these to verify reconstruction quality after L0 encode/decode

**Acceptance Criteria**:
- Metrics match thresholds for Dev/Research tier:
  - Prob-L1 ≤ 1e-3
  - Amp-L2 ≤ 1e-2
- Include assert in regression suite

---

### 🔧 Issue 5: Support Tier-Based Auto-Tune of η and P

**Title**: Add auto-tune logic for η, P based on fidelity metrics

**Description**:
- Implement logic to:
  1. Start with tier defaults (e.g., `η=1e6`, `P=32`)
  2. Increase values until metrics fall below thresholds
  3. Cap at hard-coded max (`η=1e9`, `P=128`)

**Acceptance Criteria**:
- Utility function `auto_tune_tbp(ψ, target_tier)` returns stable encoding
- Tier targets from spec table are met

---

### 🔧 Issue 6: Implement Qubit Count Ceiling Stress-Test Harness

**Title**: Simulate quantum statevector scaling to test TBP ceiling

**Description**:
- Build test suite to sweep qubit count from 4 to 24 (or max RAM limits)
- For each count:
  - Generate Haar-random statevector
  - Apply TBP quantization
  - Compute fidelity metrics (Amp-L2, Prob-L1)
  - Track memory usage and compressed output size

**Acceptance Criteria**:
- Test completes cleanly up to 20 qubits (or soft limit)
- Logs include: qubits, L1, L2, output size, η, P
- Fail gracefully if memory exceeded or quantization collapses

---

### 🔧 Issue 7: Generate Graphs for Fidelity and Storage Scaling

**Title**: Visualize TBP performance vs. qubit count

**Description**:
- From output of stress-test harness, plot:
  - Qubits vs. Amp-L2, Prob-L1
  - Qubits vs. compressed output size
  - Qubits vs. quantization time or memory usage
- Use matplotlib or Aether-native visual export tools

**Acceptance Criteria**:
- Graphs are auto-generated after stress test
- Saved as PNGs or embedded in test report
- Used to define practical ceiling for η, P vs. state width

