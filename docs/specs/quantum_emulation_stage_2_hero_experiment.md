# Quantum Emulation — Stage 2 Hero Experiment

## 0. Aim of Stage 2

Stage 1 answered: *"Why is quantum emulation inside Aether conceptually interesting?"*

Stage 2 answers: *"What is the smallest, cleanest experiment that actually **shows** those properties in action?"*

We pick one flagship implication:

> **Codex Eterna as a law‑finder over quantum‑like dynamics, inside a universal experiment machine.**

The hero experiment is designed to be:
- Small enough to implement in the current repo
- Rich enough to demonstrate:
  - Reversible, high‑D dynamics (Loom + UMX)
  - TBP quantum encoding
  - Press compression gains on weird trajectories
  - CE discovering reusable structure ("laws" / motifs)

---

## 1. Hero Experiment H1 — Quantum Spin Chain Law‑Finder

### 1.1 Narrative

We emulate a simple **1D quantum spin chain** (think: ring of qubits with nearest‑neighbour interactions). Instead of a full-blown physics solver, we use a **gate‑based approximation**:

- 8–12 "qubits" represented in TBP format via Trinity Gate
- A fixed gate sequence per tick that mimics local interactions
- Many independent runs from different initial states
- All dynamics executed on the Aether substrate (UMX + Loom)

Codex Eterna watches these runs and attempts to **compress** the evolving state space:
- It should discover **reusable gate motifs** (macro‑gates)
- It should learn **basis updates** that make the trajectories cheaper to encode
- Over time, the "library" becomes a compact description of this toy physics

If the experiment works, CE has effectively learned a mini "law of motion" for this quantum‑like system, in its own structural language.

---

### 1.2 Pillar Roles in H1

- **Trinity Gate (TBP)**
  - Encodes initial statevectors (ψ) into integer TBP payloads (masses, phases, residuals)
  - Ensures all inputs are deterministic, integerized, and logged at ingress

- **UMX (substrate)**
  - Holds the current encoded register state as part of the global state vector
  - Applies a deterministic update map U_t per tick that implements our chosen gate pattern (e.g. layer of nearest‑neighbour entangling gates + local rotations)

- **Aevum Loom**
  - Logs each tick as a sequence of I/P blocks
  - Guarantees we can replay any run exactly, or fork from any checkpoint

- **Astral Press**
  - Compresses periodic snapshots and  trajectories
  - Gives us MDL metrics on how efficiently the dynamics are represented

- **Codex Eterna**
  - Observes Loom/UMX streams (via PFNA integerized views)
  - Proposes structural updates (spawn/merge nodes, update bases) when it sees repetitive structure
  - Accepts only those changes that **reduce total description length** and pass governance

---

## 2. Experiment Design

### 2.1 Configuration

**State size**
- Qubit count: 8 (stretch goal: 12)
- Hilbert dimension: 2^8 = 256 amplitudes

**TBP quantization**
- η = 1e6 (mass resolution)
- P = 64 (phase bins)
- Fidelity thresholds: Amp‑L2 ≤ 1e‑2, Prob‑L1 ≤ 1e‑3

**Dynamics**
- Per‑tick gate pattern U_t:
  - Layer 1: parallel CZ (or CX) on pairs (0,1), (2,3), (4,5), (6,7)
  - Layer 2: single‑qubit rotations (e.g. RZ) on all qubits
  - Optional: ring shift (permute qubit indices) every k ticks

**Runs**
- Number of independent episodes: ~100–1000
- Initial states:
  - Random product states
  - Random low‑depth entangled states

---

### 2.2 Data Flow

1. **Initialisation**
   - For each episode e:
     - Generate ψ₀ᵉ via a small Qiskit circuit
     - TBP‑encode ψ₀ᵉ → integer payload
     - Inject through Trinity Gate at tick τ = 0

2. **Evolution**
   - For T ticks:
     - UMX applies U_t to the encoded state
     - Loom logs state trajectory
     - Press optionally compresses periodic I‑blocks

3. **Learning (Codex Eterna)**
   - CE sees streams of integerized states and residuals
   - It maintains nodes that capture local structure:
     - Basis vectors for typical state patterns
     - Motifs for common update patterns
   - When MDL gain exceeds threshold, CE spawns/merges nodes and updates the structural ledger

4. **Replay & Probing**
   - Use Loom to replay selected episodes exactly
   - Compare trajectories **with** and **without** CE’s library engaged

---

## 3. Evaluation & Metrics

### 3.1 Compression / MDL Metrics

- **Baseline**: cost to encode trajectories with no CE library (raw TBP + Press)
- **With CE**: cost after CE has learned basis and motifs

Key metrics:
- ΔMDL_total per episode (bits saved)
- Average κ (compression gain) per CE node
- Fraction of episodes that reuse learned motifs

### 3.2 Generalisation Test

- Train CE on a subset of gate patterns / initial states
- Then:
  - Change initial states (same gate pattern)
  - Or vary gate parameters slightly (same structure)
- Measure whether the existing CE library still yields MDL gains on these new runs

If yes, CE has learned something closer to a **general law of motion** than a memorised script.

### 3.3 Stability & Replay

- Verify Loom can replay selected episodes bit‑for‑bit (within ε thresholds)
- Verify that CE’s structural ledger is consistent across replays:
  - Same proposals at the same ticks
  - Same structural hashes

---

## 4. Conceptual Payoff of H1

If H1 works, even at modest scale (8 qubits, a few hundred ticks), it demonstrates:

1. **Aether as a universal experiment machine**
   - We can host a non‑trivial quantum‑like dynamics as just another UMX profile.
   - We can log, rewind, fork, and compress those experiments like any other.

2. **CE as a law‑finder**
   - It isn’t just fitting parameters; it’s discovering reusable structural motifs that reduce description length across episodes.
   - In plain language: CE is learning a compact internal "theory" of this toy spin chain.

3. **Deterministic mirror of probabilistic inputs**
   - Quantum‑like behavior is fed in as integer events and evolved deterministically.
   - Randomness lives at the boundary; inside, the story is pure ledger.

4. **A clear path from toy demo to larger ambitions**
   - Scaling qubits up becomes a question of performance, not architecture.
   - Swapping the toy spin chain dynamics for other "physics" (classical chaos, social models) reuses the same pattern.

---

## 5. Next Steps After Stage 2

Stage 2 (H1) gives you a concrete, end‑to‑end story.

Stage 3 can then:
- Map H1 into concrete issues against the current repo (Gate/UMX/Loom/Press/CE)
- Define acceptance tests per pillar
- Design visualisations (MDL over time, motif usage, replay traces)
- Prepare an external‑facing narrative: "We used Aether to discover laws in a toy quantum world."


---

## 6. Conceptual Limits & Implications (Full Stage 2 Notes)

This section captures the broader Stage 2 discussion about **pushing the Aether quantum emulation stack to its conceptual limits** and what that would mean.

### 6.1 What We Could Achieve at the Conceptual Limit

#### A. A "Virtual Quantum Computer" Inside Aether

At the limit, with TBP + Gate + UMX + Loom + Press + CE all fully wired and tuned, Aether acts as:

> A reversible, fully logged, self‑optimising virtual quantum computer.

Capabilities in principle:
- Emulate large Hilbert spaces (far beyond current 5q hardware), bounded only by available compute and memory.
- Represent full gate sequences as deterministic UMX update maps over TBP‑encoded states.
- Save, load, rewind, fork, and diff entire quantum‑like runs using Loom.
- Compress long trajectories with Press so even huge experiments are storable and replayable.

This is a "quantum playground with save/load/undo" inside Aether, not limited by today’s physical devices.

#### B. CE as a Self‑Optimising Quantum Compiler / Meta‑Model

Given many runs of these emulated circuits, Codex Eterna effectively becomes:

> A deterministic, fully audited, self‑optimising compiler for quantum‑like programs.

At the conceptual limit CE can:
- Detect recurring gate patterns and state trajectories across runs.
- Cluster them into **motifs** or macro‑gates.
- Learn **better bases** for whole families of circuits, reducing description length.
- Offer cheaper internal representations of specific workload families.

So CE is not just tuning parameters; it is learning **shorter, more reusable descriptions** of quantum‑like behaviour, with all changes ledgered and reversible.

#### C. A Universal Physics Sandbox

Once quantum is just a profile, Aether can treat *any structured process* as a "physics":

- Quantum dynamics
- Classical chaotic systems
- Social / economic simulations
- Hybrid systems where these influence each other

The core question the stack keeps asking is:
- Is there structure?
- Can I compress it?
- Can I replay it?
- Can I learn reusable motifs from it?

Pushing it hard yields a **universal experiment machine** where different "worlds" are just different UMX profiles and metric sets.

#### D. Near‑Optimal Compression of High‑Dimensional Behaviour

Over long runs:
- Press provides near‑MDL‑optimal compression of trajectories.
- Loom guarantees reversibility.
- CE searches for ever‑shorter structural descriptions.

For large families of experiments, this becomes a machine for converging toward **minimal programs** (or close) that generate that behaviour. In other words: Aether acts as a **law‑miner** for whatever domain you run inside it.

#### E. Quantum‑Aware Shell for Real Hardware

If and when real QPUs are available:
- Trinity Gate talks to hardware via TBP‑compatible interfaces.
- Loom + Press log and compress experiments.
- CE learns the device’s quirks and effective noise models.

Aether becomes the **stabilising, governing shell** around messy physical qubits, bridging "math quantum" and "industrial hardware quantum" under one ledger.

---

### 6.2 Implications of Approaching This Limit

#### 1. Epistemic Power: From Running Models to Discovering Laws

Because every run is:
- Logged (Loom),
- Compressed (Press),
- And structurally optimised (CE),

you don’t just simulate; you continually surface:
- Invariants (“what never changes”),
- Short descriptions (“what’s the core pattern here”),
- Highly reusable motifs.

This is powerful for:
- **Science**: turning brute‑force simulation into compact internal "theories".
- **Engineering**: using CE’s structural ledger to suggest better abstractions and designs.

#### 2. Safety & Governance: High Power, High Traceability

Upside:
- Every adaptation and decision path is traceable via time and structural ledgers.
- Hard constraints (conservation, risk, governance flags) can be enforced in UMX/CE profiles.

Downside / caution:
- A highly capable optimiser for representation and behaviour is a potent tool.
- Whoever controls the stack + library effectively controls a **very strong optimisation engine**.

So governance and operator intent matter a lot; the good news is the system is built to be auditable by design.

#### 3. Cognitive Shift: Thinking in Ledgers, MDL, and Invariants

Working with Aether at this level changes how you think:
- You start seeing problems as:
  - Ledgers to be kept consistent,
  - Compression problems to be solved,
  - Invariants to be discovered.
- "Is this good?" becomes "Does this shorten the description and generalise?".

This is a shift toward **MDL‑style, structure‑first thinking**, which can generalise from technical domains into how you reason about complex systems in general.

---

### 6.3 Hard Limits (What You Still *Can’t* Do)

Even at the conceptual limit, Aether does **not**:
- Break Shannon: it cannot compress true randomness beyond its entropy.
- Break complexity theory: NP‑complete problems don’t become easy in general.
- Break physics: no FTL signalling, no free energy, no retroactive history edits.
- Become an oracle: CE extrapolates from structure it has seen; it doesn’t magically know the future outside its distribution.

What you *do* get is a much sharper, controllable way to live right up against those boundaries — with better visibility into where the real constraints are.

---

This section, combined with the H1 hero experiment, completes **Stage 2**: both the conceptual ceiling view and a concrete experiment design that demonstrates the key properties in miniature.
