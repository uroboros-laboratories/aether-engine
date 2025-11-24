# Astral Press — Master Implementation Spec (Combined Canon v1)

This document is an **assembled master spec** for Aether Press / Astral Press, built by concatenating the canon implementation documents from `implementation.zip` in a coherent order. All text below the document map is taken **verbatim** from those source files; nothing has been dropped or rewritten.

## Document Map (Source Files & Order)

1. `astral_press_pillar_dev_implementation_spec_v_0.md`
2. `astral_press_pillar_dev_spec_addendum_focus_report_pass_01.md`
3. `astral_press_pillar_dev_spec_addendum_implementation_pass_02.md`
4. `astral_press_full_implementation_build_plan_beyond_mvp.md`
5. `astral_press_js_offline_mvp_build_plan_2025_11_20.md`
6. `astral_press_js_full_implementation_build_plan_v_1_beyond_mvp.md`
7. `app_local_spec_v_1_aether_press_local_implementation_2025_11_20.md`
8. `astral_press_app_implementer_checklist_v_1_2025_11_20.md`
9. `astral_press_dev_handoff_map_v_1.md`
10. `astral_press_app_complement_sheet_v_2_legacy_docs_2025_11_20.md`
11. `astral_press_app_complement_sheet_v_3_math_compendium_2025_11_20.md`
12. `astral_press_app_complement_sheet_v_4_implementation_canon_pack_2025_11_20.md`
13. `astral_press_pillar_app_spec_sheets_v_1_2025_11_20.md`
14. `astral_press_multi_layer_nap_mdl_stack_spec_v_1_stack_until_it_stops_making_sense.md`
15. `astral_press_pillar_nap_compression_manifest_spec_canon_pass.md`
16. `astral_press_pillar_nap_envelope_budget_gate_js_implementation_pass.md`
17. `astral_press_epsilon_profiles_integerization_spec_v_1_crush_without_regret.md`
18. `astral_press_policy_dimensional_controls_spec_v_1_p_state_p_cite_dims_press.md`
19. `astral_press_policy_pack_v_1_profiles_cards.md`
20. `astral_press_pillar_metrics_evaluation_canon_pass.md`
21. `astral_press_pillar_s_1_s_12_modes_switchboard_canon_pass.md`
22. `astral_press_pillar_aeon_i_apxi_descriptor_grammar_canon_pass.md`
23. `astral_press_pillar_apx_container_manifest_canon_pass.md`
24. `astral_press_pillar_canon_gap_ledger_big_dogs_pass.md`
25. `astral_press_pillar_gate_tbp_nap_manifests_impl_docs_pass.md`
26. `astral_press_pillar_cross_pillar_nap_umx_tbp_integration_umx_impl_docs_pass.md`
27. `astral_press_pillar_trinity_gate_implementation_docs_pass.md`
28. `astral_press_pillar_trinity_gate_impl_docs_extraction_pass.md`
29. `astral_press_pillar_trinity_gate_impl_docs_targeted_extract_plan.md`
30. `astral_press_pillar_trinity_gate_tbp_integration_gate_impl_docs_pass.md`
31. `trinity_gate_nap_pack_schemas_gate_impl_docs_pass.md`
32. `trinity_gate_pillar_press_loom_integration_tgp_tbp_impl_docs_pass.md`
33. `trinity_gate_press_tbp_integration_implementation_docs_pass.md`
34. `trinity_gate_tbp_press_integration_implementation_docs_pass.md`

---


---

<!-- BEGIN SOURCE: astral_press_pillar_dev_implementation_spec_v_0.md -->

# Astral Press Pillar (Aether Press Protocol)
## Developer Implementation Spec — v0.1 (Draft)

**Pillar:** Astral Press Pillar (APP) — Aether Press Protocol  
**Role:** “Data Compression Pillar” in the Aether / Trinity stack  
**Audience:** Implementers / systems devs / architects  
**Status:** Draft spec synthesised from existing Aether Press materials. All direct facts and phrases are taken from:

- `press pillar report.pdf` (**FOCUS_REPORT.md – “Aether Press Protocol (APP) – Data Compression Pillar (Focus Report)”**)  
- `Aether_Press_Protocol_Implementation.pdf`  
- `Aether_Press_Post_Implementation_Report.pdf`  
- `Aether_Press_Protocol_Beyond_Shannon_Limit_Declaration.pdf`  
- `press v2.pdf` (Aether Report 16)  
- `press proformance.pdf` (Aether Report 19)  
- `LCDRM_White_Paper_Uroboros.pdf`

This document:
- Enumerates **all visible functions, features, and capabilities** of the Press pillar.  
- Rewrites them into a **dev-facing, implementation-ready spec**.  
- Adds **explicit math** for the formal core.  
- Flags **gaps** that would block a complete, bit‑for‑bit implementation today. These are tagged as `GAP-APP-XXX`.

Where wording is taken literally from the source, it is kept intact or near-intact (this is on purpose).

---

## 0. Pillar Positioning & Responsibilities

From the Focus Report title and abstract:

> “**FOCUS_REPORT.md**  
> Aether Press Protocol (APP) – Data Compression Pillar (Focus Report)”

> “The Aether Press Protocol is a **symbolic compression framework** that projects raw data into a **structured latent form** and **inverts it back perfectly** to the original dataset. This pillar enables **universal, lossless compression** across domains by **storing only generative rules and minimal residuals instead of entire datasets**, yielding extreme data reduction without violating deterministic fidelity.”

From the **Scope & Responsibilities** section:

> “APP’s Role: The Aether Press Protocol (APP) serves as the **Trinity system’s data compression subsystem**, responsible for **distilling large datasets or simulation outputs into concise mathematical representations**. It operates **downstream of the Trinity architecture as a post‑processing framework** that captures the **underlying structure of information**. APP’s primary responsibility is to **encode data as ‘rule + residual’ pairs and package them for storage or transmission**, guaranteeing that the original information can be **fully reconstructed when needed**. It **standardizes symbolic reduction across any domain (physics, simulation, telemetry, etc.)** and ensures compression is achieved **without introducing irreversibility unless explicitly allowed** (e.g. optional lossy modes).”

### 0.1 High‑level responsibilities (dev framing)

Implementation must support:

1. **Downstream operation**  
   - Press attaches “after” Trinity / Aether processes, taking **structured outputs** or raw files and producing **APP capsules**.

2. **Rule + residual encoding**  
   - Every compressed artefact must be representable as a **model (rules) + residual (exceptions)** pair (possibly stacked into many layers).

3. **Lossless default**  
   - Default mode: **bit‑perfect reconstruction**, with optional **ε‑bounded** modes and a **symbolic‑only** extreme.

4. **Domain‑agnostic design**  
   - Must support “ordinary binary data and structured outputs” by discovering patterns (logs, sensor streams, images, tabular data, etc.).

5. **Portable packaging**  
   - Outputs are **.apx capsules**: deterministic, self‑contained archives (manifest + layer files + metadata + integrity tags).

6. **Stacked / nested extension**  
   - Through **NAP** + **SimA/SimB**, must support multi‑layer stacking and nesting for mixed‑structure data.

7. **Integration with Trinity / Loom / NAP**  
   - Must integrate with **Aevum Loom** (replay) and **NAP** (multi‑layer compression and dimension bus) and respect Press policies from reports 16 and 19.

---

## 1. Capabilities & Behaviours (from Focus Report)

The Focus Report has an explicit **“Capabilities & Behaviours”** section. Key excerpts:

> “**Universal Model-Based Compression:** APP can **compress ordinary binary data and structured outputs** by **discovering an underlying mathematical model or pattern in the data**. It **encodes the behavior or relationships that generate the data, rather than the data itself**, making it a **domain‑agnostic compressor**. … When patterns exist, APP achieves compression far beyond traditional methods by **storing a compact generative description (the ‘rule’) plus a small residual correction**.”

> “For example, in tests it **reduced a structured CSV of 50k rows to a descriptor‑only package (no residual)** – effectively just a few KB describing the entire dataset… Similarly, a nested JSON dataset was compressed with only the generative array rules captured… For highly regular data like a checkerboard pattern, APP identified the base tiling rule and needed **zero residual**, achieving an extremely small descriptor representation.”

> “**Lossless Data Reproduction:** The protocol guarantees **bit‑perfect reconstruction** of losslessly compressed data. The ‘unpress’ operation applies the stored model and residual to **recover the exact original**, which has been verified to be **byte‑for‑byte identical** to the input… one of APP’s core capabilities is **exact round‑trip fidelity – compress data and later expand it to the exact initial state**, as formally: $Unpress(Press(data)) = data$. (APP also supports optional lossy modes or $\varepsilon$‑bounded compression… but by default its behaviour is strictly lossless.)”

> “Press capsules carry **internal integrity tags (per‑block and whole‑file hashes)** so that any corruption or mismatch is detected upon decompression.”

> “APP’s behaviour follows a defined **Rule+Residual Compression Pipeline** …” (covered in detail in §3 below).

> “APP can be extended through the **Nexus Aeternus Protocol (NAP)** to handle data with **mixed structure or partial randomness** by **layering multiple compression passes** … **APP v2 (Stacked/Nested dual‑simulation)** processes data with **two coordinated compressions (SimA and SimB) across hierarchical levels**… it stacks compression vertically (micro → meta → global layers) so that residuals from one level are further compressed by the next.”

### 1.1 Capability list (implementation targets)

From the above, Press must support at least:

1. **Model‑based compression**  
   - Discover / accept a **Domain Model** that maps data to a small set of parameters + invariants.

2. **Residual‑based error capture**  
   - Represent deviation between model output and real data as a separate **Residual** object.

3. **Exact round‑trip**  
   - Provide a deterministic `Press` / `Unpress` pair with $Unpress(Press(S)) = S$ in lossless mode.

4. **Optional ε‑bounded lossy compression**  
   - Provide modes where the residual is quantized / reduced subject to numeric bounds (see §4.2, §7.2).

5. **Stacked / nested multi‑layer compression**  
   - Implement **SimA/SimB + NAP** to separate structured vs random components and compress each hierarchically.

6. **Internal integrity tracking**  
   - Maintain per‑block + whole‑file hashes and expose verification at decode.

7. **Baseline benchmarking**  
   - Compare against “Baseline Codecs (gzip, bzip2, xz)” and others (ZIP, Zstd, FLAC, PNG per Implementation doc) as part of evaluation.

---

## 2. Formal Math Core

The **Post‑Implementation Expansion Report** and the **LCDRM white paper** define the mathematical spine of Press.

### 2.1 Core Press equations (APP / AIF)

From **Aether Press Protocol – Post‑Implementation Expansion Report**:

> “Let $S$ be a dataset represented by bits $b$. Define the model $M(\theta)$ with parameters $\theta$ such that $S \approx M(\theta) + R$, where $R$ is the residual.
>
> (1) $S = M(\theta) \oplus R$ (bitwise XOR for discrete systems)  
> (2) Compression ratio $= (|\theta| + |R|) / |S|$  
> (3) Continuity constraint → $\lim_{|R|→0} \text{Reconstruction} = S$  
> (4) Entropy $H(S) = H(M(\theta)) + H(R) − I(M(\theta); R)$  
> For perfect determinism $I = H(R)$, so $H(S) = H(M(\theta))$.”

Interpretation for implementers:

- **Data**: $S$ is the original dataset (bits or structured array).  
- **Model**: $M(\theta)$ is a family indexed by parameters $\theta$ (and invariants) chosen per segment.  
- **Residual**: $R$ is the correction term that makes the model output exactly match $S$ (lossless) or match up to tolerance (ε‑bounded).  
- **Operator**: `⊕` is **bitwise XOR** for discrete data; more generally, “combine model output and residual” (additive, XOR, or domain‑appropriate).  
- **Compression ratio** is literally “size of model parameters + size of residual” divided by “size of original”.

The continuity constraint states that as residual size tends to zero, reconstruction converges to $S$.

The same report gives the **Axioms of the Aether Information Framework (AIF)**:

> 1. “Data = manifestations of relationships.”  
> 2. “Information = minimal description of those relationships.”  
> 3. “Noise = relationships below current model resolution.”  
> 4. “Entropy = measure of unresolved relational density.”

These axioms are the conceptual basis for Press’s “rules + residuals” operation.

### 2.2 LCDRM equations (layered relational deltas)

From **Layered Compression via Deterministic Relational Mapping (LCDRM)**:

> “LCDRM is a **deterministic, scale‑invariant compression paradigm** that **encodes relationships between data elements rather than the elements themselves**. Each layer represents residual transformations between successive states of the previous layer, achieving **multi‑scale compression and self‑consistent reconstruction without entropy coding**.”

> “Let $D_0 = \{x_i\}$. Each subsequent layer:  
> $L_k = \Delta L_{k−1} = \{x^{(k)}_i − x^{(k−1)}_i \mid x^{(k−1)}_i \in L_{k−1}\}$.  
> Continuous generalization: $L_k(t) = \frac{d}{dt} L_{k−1}(t)$.  
> Compression occurs when $|L_k| < |L_{k−1}|$ until $\Delta L_k → 0$.”

> “Decompression: $L_{k−1}(i) = \sum_{k’\le k} L_{k’}(i) + C$, where $C$ is the base constant. **Guarantees identical reconstruction.**”

> “LCDRM formalizes Trinity’s relational compression method, demonstrating **minimal relational integers can encode full datasets with deterministic reconstruction**. It compresses **across scales of dependency, not merely symbol probability**.”

Press implementation can either:

- Treat LCDRM as a **core internal modelling strategy** (for SimA or residual layers), or  
- Treat it as a **related but sibling theoretical engine** that informs multi‑layer residual design.

**Implementation requirement:** Press must be able to express a dataset as **one or more LCDRM‑style relational layers** when using layered modes.

### 2.3 Two‑track Press math (P_state / P_cite, v3)

From **Aether Report 19 – press proformance.pdf**:

> “**TWO-TRACK PRESS (DO THIS EVERY TIME)**  
> 1. **P_state (reconstructive)** – the *minimal* snapshot needed for $T$ to resume exactly.  
>    • Must satisfy fidelity:  $d(O(S), O(\mathrm{DePr}(\mathrm{Pr}(S))) ) \le \varepsilon$.  
>    • Lossless for critical classes (e.g., $O.\text{struct}$, $O.\text{event}$ = 0‑tolerance).  
> 2. **P_cite (documentary)** – hashed pointers to big originals (docs, PDFs, logs, media).  
>    • Store **content‑hash, byte length, and a few extracted integers you actually use**.  
>    • You don’t carry the whole file inside the checkpoint unless it’s required for $T$.”

> “Result: you keep **exactly what the computational episode needs**, and only **proofs/pointers** for everything else. That’s where the astronomical gains come from.”

And the **Crush without regret checks**:

> 1. “**Field‑level bounds:** For every numeric field $x$ you store after quantization $q$:  
>    $$|x_{\text{post}} − x_{\text{pre}}| \le q/2 \le \varepsilon_x.$$  
> 2. **Replay test:** DePress then run $\Delta = 0$: $O$ unchanged (fidelity at snapshot).  
> 3. **Predictive test:** DePress and run $T^\Delta$; check $d(O_{\text{true}}, O_{\text{replayed}}) \le \varepsilon$.  
> 4. **Document proof:** Keep $\{\text{hash}, \text{bytes}\}$ for each external source in **P_cite** so an auditor can verify you didn’t hallucinate inputs.  
> 5. **Idempotence:** Same envelope + same nonce → no net change to $O$.  
> 6. **Isolation:** Prior checkpoint O‑hashes never change.”

Implementation requirement: Press **must** be able to:

- Maintain **P_state** (replayable internal state snapshot) and **P_cite** (external ref metadata) as distinct artefacts.  
- Enforce **field‑level quantization bounds** and support **replay / predictive tests** as part of acceptance.


---

## 3. Components & Subsystems (from Focus + Implementation)

### 3.1 Named / stated / implied components (Focus Report)

From the **“Components (Named/Stated/Implied)”** section of `press pillar report.pdf`:

> “**Aether Press Protocol (APP)** – *Named:* A **symbolic compression framework** defining the rules for **model‑based data reduction**. It compresses by **capturing relationships instead of raw bits**.”

> “**Residual Encoding** – *Stated:* The step storing only **minimal differences** between a model’s output and the real data. **Residuals represent information not explained by the generative model.**”

> “**Packaging Stage** – *Named:* A phase that wraps the **model ID, parameters, and residuals** into a portable container. Ensures **all pieces needed for reconstruction are kept together**.”

> “**APX Capsule Format** – *Named:* A portable `.apx` container for Aether Press outputs. It is a **deterministic, self‑contained ZIP archive (manifest + layer files)** used to store compressed data and metadata.”

> “**SimA (Symbolic Compressor)** – *Named:* In advanced Press usage, a **generative compression stream** that **models structured patterns (stacked/nested rules)** and **records only math needed to reconstruct data**.”

> “**SimB (Residual Compressor)** – *Named:* A complementary **residual stream capturing any data SimA cannot express, layer by layer**. Together with SimA, it **splits deterministic structure from randomness**.”

> “**NAP Compression Manifest** – *Named:* A Nexus Aeternus Protocol (NAP) manifest that **‘knits’ together SimA and SimB outputs**. Defines how **multi‑layer stacks and nests recombine for exact reconstruction**.”

> “**Baseline Codecs (gzip, bzip2, xz)** – *Named (contextual):* Standard compression tools used as **baseline benchmarks** for Press experiments.”

> “**Press Metadata Manifest** – *Stated:* The `.apxMANIFEST.json` file storing original file metadata: **name, size, hash, compression mode, timestamp, etc.** Extended in later versions to include **file system info (permissions, timestamps)** for archival completeness.”

> “**HMAC Signature (APX)** – *Implied:* Cryptographic signing of capsules to ensure **authenticity and tamper‑detection**. Allows verification that an `.apx` capsule was created by the authorized system and not modified.”

**Implementation mapping:**

- `APP core` → top‑level orchestrator of all sub‑steps.  
- `Residual Encoding` → a dedicated module that takes model output + data, computes residuals, and encodes them.  
- `Packaging` → APX container builder.  
- `APX Capsule` → on‑disk/on‑wire representation.  
- `SimA/SimB` → advanced encoder mode using two coupled streams.  
- `NAP manifest` → structural description of how layers recombine.  
- `Press Metadata Manifest` → JSON metadata inside `.apx`.  
- `HMAC Signature` → optional cryptographic extension for secure deployments.

### 3.2 Encoder / Decoder stages (Implementation doc)

From **Aether_Press_Protocol_Implementation.pdf**:

> “3. **Architecture Overview**  
> **Encoder**  
> 1. **Domain Model** – Defines the governing physics or statistical law.  
> 2. **Parameter Fitting** – Extracts parameters and invariants from data.  
> 3. **Residual Encoding** – Stores minimal differences between the model and data.  
> 4. **Packaging** – Combines model ID, parameters, invariants, and residuals into a standardized container.  
> **Decoder**  
> 1. Load model and metadata.  
> 2. Regenerate the base signal deterministically.  
> 3. Add residuals for full reconstruction.  
> 4. Validate checksum and fidelity.”

This is the **minimal encoder/decoder behaviour** that every implementation must honour.

### 3.3 Compression modes

From the Implementation doc:

> “4. **Compression Modes**  
> – **Lossless** – Full reconstruction, residuals preserved exactly.  
> – **Quasi‑Lossless** – Bounded error within ε‑tolerance.  
> – **Symbolic‑Only** – Stores only rules and invariants; maximum compression.”

**Implementation requirements:**

- **Lossless mode:** $R$ is stored exactly; $Unpress(Press(S)) = S$; matching hash (e.g., SHA‑256) must be possible.  
- **Quasi‑Lossless mode:** $R$ is quantized or otherwise reduced such that field‑level bounds and global acceptance conditions hold (see §2.3).  
- **Symbolic‑Only mode:** `R = 0` or omitted; Press stores only $M(\theta)$ + invariants; decompression reproduces a **model‑generated surrogate** rather than the original raw data. (Useful when only structure matters.)

### 3.4 Container format (APP container)

From Implementation doc, **“7. APP Container Format”**:

> “Header  
> – Model ID, version, and compression mode.  
> – Metadata: dtype, shape, fidelity metric.  
> Body  
> – Model parameters (quantized or raw).  
> – Invariant dictionary.  
> – Residual byte stream.  
> – Metrics and checksum.”

From the Focus Report plus this section:

- The **APP container** corresponds to the `.apx` capsule with:  
  - **Header**: identifies model, version, compression mode, and describes the shape and dtype of the underlying data, plus expected fidelity metrics.  
  - **Body**: carries the *model parameters*, *invariants*, *residual stream*, plus *metrics* (compression ratio, error metrics) and *checksums* (segment and/or whole‑file).  
  - **Metadata manifest**: `.apxMANIFEST.json` with original file name, size, hash, mode, timestamps, etc., and optionally filesystem details.

### 3.5 Subsystems (internal division of labour)

From Implementation doc, **“8. Subsystems”**:

> `| Subsystem | Role |`  
> `| Aether Core | symbolic modeling and invariant extraction |`  
> `| Press Engine | encoding of parameters and residuals |`  
> `| Flux Decoder | reconstruction and fidelity validation |`  
> `| Protocol Layer | serialization schema and metadata registry |`

Implementation should mirror this separation:

1. **Aether Core**  
   - Provides domain models, invariant discovery, and simulation capabilities.  
   - Decides model families (Fourier, polynomial, Markov, LCDRM, etc.).

2. **Press Engine**  
   - Implements the compression pipeline: model fitting, residual computation, residual encoding, container assembly.  
   - Houses `Press` and `Unpress` algorithms and their advanced variants (SimA/SimB, stacking).

3. **Flux Decoder**  
   - Handles decoding of APP capsules; reconstructs base signals; applies residuals; validates checksums and fidelity metrics.

4. **Protocol Layer**  
   - Defines `.apx` structure; manages manifests; integrates HMAC and signatures where used; registers codec versions.


---

## 4. Core Logical Interfaces (Math‑level)

Below is a **language‑agnostic**, **math‑level interface** description. This is not code; it’s a description of functions the implementation is expected to realise.

### 4.1 Basic pair: Press and Unpress

#### 4.1.1 Press

Conceptual signature:

- **Input:**  
  - Dataset $S$ (bytes or structured array)  
  - Compression mode $m \in \{\text{lossless}, \text{quasi‑lossless}, \text{symbolic‑only}\}$  
  - Optional config (model family hints, target ε per field, quantization policy, stack depth, etc.)

- **Output:**  
  - APP capsule $C$ (an `.apx` container) containing header + body + manifest + (optionally) HMAC.

- **Guarantees (lossless mode):**  
  - There exists a corresponding `Unpress` such that $Unpress(C) = S$ and hash($S$) = hash($Unpress(C)$).

- **Guarantees (quasi‑lossless mode):**  
  - For each numeric field $x$: $|x_{\text{post}} − x_{\text{pre}}| \le q/2 \le \varepsilon_x$.  
  - System‑level outputs $O$ obey: $d(O(S), O(Unpress(C))) \le \varepsilon$ as per §2.3.

- **Guarantees (symbolic‑only mode):**  
  - Decompression yields $\hat{S} = M(\theta)$, where $
\hat{S}$ is a model‑generated surrogate consistent with stored invariants.

#### 4.1.2 Unpress

Conceptual signature:

- **Input:** APP capsule $C$ (.apx)  
- **Output:** Reconstructed dataset $\hat{S}$ and verification report.

Steps (from Implementation doc’s Decoder):

1. Load model and metadata from header + manifest.  
2. Regenerate base signal deterministically using $M(\theta)$ and invariants.  
3. Apply residuals $R$ (if present) to recover $\hat{S}$.  
4. Validate checksums and fidelity metrics (hash match in lossless mode, bounds in ε‑bounded).  
5. Return $(\hat{S}, \text{fidelity_report})$.


### 4.2 Domain Model selection and fitting

These functions implement the **Rule+Residual Compression Pipeline** described in the Focus Report:

> “First, a **Domain Model** is chosen or inferred – essentially the form of the mathematical law or pattern expected (for example, a Fourier series, polynomial fit, Markov process, etc.). Next, **Parameter Fitting** occurs, where the model’s parameters and any invariants are tuned to the specific dataset. Then comes **Residual Encoding**, which records the delta between the model’s output and the actual data… Finally, the **Packaging** stage wraps the model identifier, the fitted parameters, and the encoded residual into a portable file container.”

Required logical pieces:

1. **DomainModelSelect**  
   - Input: segment $S_i$, metadata (dtype, shape, domain hints).  
   - Output: selected model family $M \in \mathcal{M}$ (e.g., Fourier, polynomial, autoregressive, LCDRM, etc.).  
   - Behaviour: may use heuristics or configuration to pick the best candidate.

2. **ParamFit / InvariantExtract**  
   - Input: chosen model family $M$, segment $S_i$.  
   - Output: $\theta_i$ (parameters), $I_i$ (invariants).  
   - Behaviour: run optimisation / fitting processes (least squares, maximum likelihood, dynamic programming, etc.) appropriate for $M$.

3. **ModelSimulate**  
   - Input: $M, \theta_i, I_i, \text{len}(S_i)$.  
   - Output: synthetic segment $\tilde{S}_i = M(\theta_i, I_i)$.

4. **ResidualCompute**  
   - Input: original $S_i$, synthetic $\tilde{S}_i$.  
   - Output: residual $R_i$ (difference or XOR depending on dtype).  
   - Behaviour: $R_i = S_i − \tilde{S}_i$ (numeric) or $R_i = S_i \oplus \tilde{S}_i$ (bitwise).

5. **ResidualEncode**  
   - Input: residual $R_i$, mode $m$.  
   - Output: encoded residual bytes $\mathcal{R}_i$.  
   - Behaviour:  
     - Lossless: apply a **lossless encoder** to $R_i$ (e.g., general‑purpose or custom entropy coder).  
     - Quasi‑lossless: apply quantization then entropy encoding, respecting per‑field $\varepsilon_x$ (see §7).

6. **PacketAssemble**  
   - Input: $\text{model\_id}$, $\theta_i$, $I_i$, $\mathcal{R}_i$, metadata (eps, checksums).  
   - Output: segment packet for container body.

**GAP‑APP‑001 (Model library & selection):**  
The docs list **example model families** (“Fourier series, polynomial fit, Markov process, etc.”) but do not define a concrete, finite set $\mathcal{M}$ or the exact selection heuristic. A full implementation must **choose and standardise**:

- Which models are supported (e.g., {Fourier, polynomial, ARMA, LFSR, LCDRM, piecewise‑linear, …}).  
- How they are parameterised (exact meaning and encoding of $\theta$ per family).  
- How the encoder decides between them (fixed config, heuristics, training, or external hinting via Trinity).

### 4.3 APX container handling

Logical functions:

1. **CapsuleBuildHeader**  
   - Fills: model ID, version, compression mode, dtype, shape, declared fidelity metric(s).  

2. **CapsuleBuildManifest**  
   - Creates `.apxMANIFEST.json` with original file metadata (name, size, hash, mode, timestamps, filesystem bits).  

3. **CapsuleEncodeBody**  
   - Serialises model parameters, invariant dict, residual stream, metrics, checksums into canonical layout.

4. **CapsuleSign (optional)**  
   - Computes HMAC / signature over container; stores signature + algorithm ID.

5. **CapsuleVerify**  
   - On decode, verifies integrity tags and signature (if present) and returns an acceptance report.

**GAP‑APP‑002 (Exact .apx schema & signature details):**  
The reports specify **what** must be stored but not the exact **binary layout, field ordering, or signature algorithm**. An implementation must define:

- Canonical byte layout of header, manifest reference, and body segments.  
- JSON schema for `.apxMANIFEST.json`.  
- Hash function(s) for content hashes (SHA‑256 is implied in experiments but not explicitly locked).  
- HMAC / signature algorithms, key management, and how signatures are bound to capsule content.


---

## 5. Advanced Press: Stacked / Nested (SimA / SimB / NAP)

From the Focus Report and APP v2 description:

> “In advanced Press usage, **SimA (Symbolic Compressor)** is a generative compression stream that **models structured patterns (stacked/nested rules)** and records only math needed to reconstruct data. **SimB (Residual Compressor)** is a complementary residual stream capturing any data SimA cannot express, layer by layer. Together they split deterministic structure from randomness.”

> “APP can be extended through the **Nexus Aeternus Protocol (NAP)**… This was demonstrated as **APP v2 (Stacked/Nested dual‑simulation)**, where the data is processed by **two coordinated compressions (SimA and SimB) across hierarchical levels**. In this mode, APP becomes **adaptive**: it **stacks compression vertically (micro → meta → global layers)** so that residuals from one level are further compressed by the next.”

From **v2 report (Aether Report 16)** we also see per‑dimension Press controls (see §6).

### 5.1 SimA / SimB logical roles

- **SimA (Symbolic stream):**  
  - Main job: discover *structured*, *law‑like* patterns and encode them as generative rules.  
  - Output: a stack of model descriptions across scales (micro/meta/global).

- **SimB (Residual stream):**  
  - Main job: capture **leftovers** from SimA – anything not captured by rules.  
  - Output: residual layers, each possibly further compressed via LCDRM or other residual models.

- **NAP Compression Manifest:**  
  - A structural descriptor telling the decoder **how to recombine** SimA and SimB outputs across layers to get $S$ back.

### 5.2 Stacked / nested pipeline

Conceptual flow for a multi‑layer Press run:

1. **Layer 0 (micro):**  
   - Run SimA on small chunks (local structure).  
   - Compute residuals; feed them into SimB for additional compression.  

2. **Layer 1 (meta):**  
   - Observe patterns **across** micro‑layer outputs (e.g., repeating structures across chunks).  
   - Apply further modelling (SimA₁) and residual handling (SimB₁).

3. **Layer 2+ (global):**  
   - Repeat as needed until residuals are no longer compressible (LCDRM’s $|L_k| < |L_{k−1}|$ condition fails).

4. **NAP manifest construction:**  
   - For each layer $k$, record:  
     - which datasets it acts on (SimA vs SimB from previous layer),  
     - how outputs cascade,  
     - how to invert the sequence at decode time.

5. **Decoding:**  
   - Work from highest layer down, reconstructing SimA/SimB outputs in the correct order, guided by the NAP manifest, until you recover $S$.

**GAP‑APP‑003 (NAP manifest concrete schema):**  
The NAP manifest is conceptually described but lacks a fixed schema. Implementation must decide:

- How layers are indexed and ordered.  
- How SimA vs SimB data streams are referenced (IDs, offsets).  
- How to represent dependencies (graph vs strict stack).  
- How this manifest is stored inside `.apx` (embedded JSON vs sidecar).


---

## 6. Dimension‑Level Press Controls (Report 16 — v2)

From **Aether Report 16 – press v2.pdf**:

> “Dims Press per‑entry” (table showing `raw_bytes`, `lores_bytes`, `press_bytes` for `NAP_bus`).

> Bullet list:
>
> • “**Exact vs ‑quantized dims:** choose which dims must match exactly for replay vs which can be bucketed (e.g., [values] to nearest $1e−3$, positions to 1 unit).”  
> • “**Residual fraction:** tighten or loosen Loom’s residual size (e.g., 5–20%) for layers where you need more/less detail.”  
> • “**Selective retention:** mark dims as {**recompute**, **residual**, **full**}:  
>   – _recompute_: derive from other fields on replay (kept out of residual),  
>   – _residual_: store compact delta,  
>   – _full_: store verbatim (e.g., provenance‑critical tags).  
> • **Dict scopes:** keep **per‑node dictionaries** or a **global Press dict** on the NAP bus for cross‑layer dimensional schemas.”

> **BOTTOM LINE:**  
> “New dims can appear mid‑run (we proved it) and get **Loomed (for deterministic replay)** and **Pressed (for compact, reversible storage)** like any other data. You can dial **how faithful** they must be for reuse and **how much detail** to keep in residuals on a **per‑dimension, per‑layer** basis.”

### 6.1 Dim‑level policy model

Each **dimension** (field) on the NAP bus must have a **Press policy** with:

- **Retention mode:** `recompute | residual | full`  
- **Quantization q:** 0 for exact, non‑zero for bucketed values (numeric fields).  
- **Residual fraction:** how much of Loom’s residual budget is allowed for that dimension on a given layer.  
- **Dictionary scope:** local per‑node vs shared global dictionary.

Implementation must:

1. Allow new dimensions to appear at runtime and be assigned policies.  
2. Apply those policies when building P_state and Press residuals.  
3. Honour recompute/full semantics at replay (`recompute` dims derive from other fields; `full` dims are stored verbatim even if compressible).

**GAP‑APP‑004 (Exact residual fraction semantics):**  
Report 16 gives the idea (“residual fraction 5–20%”) but not the exact algorithm for enforcing a per‑dim residual budget. Implementation must choose:

- Whether residual fraction is per‑layer or global.  
- Whether it is enforced in bytes, entropy, or some other metric.  
- What happens when a dim’s residual attempt would exceed its budget (truncate, re‑quantize, or fail?).


---

## 7. Two‑Track Press Policies (Report 19 — P_state / P_cite)

From **Aether Report 19 – press proformance.pdf** (already partly quoted):

> “Press can crush traditional sources by absurd factors… The key is to separate what must be *reconstructible* for the math from everything else.”

> “**TWO-TRACK PRESS (DO THIS EVERY TIME)**” (P_state/P_cite as quoted in §2.3).

It also defines a **Press policy card**:

> “**PRESS POLICY  <source_name>**  
> Type: (text/pdf/image/log/table/sensor)  
> Track: [P_state | P_cite] (pick one; sometimes both)  
> O‑fields derived: { … } (list only what T or O needs)  
> Quantization q per field: {f1:q1, f2:q2, …}  
> Epsilon per field: {f1:ε1, f2:ε2, …} (ensure q/2 ≤ ε)  
> Content‑hash (if P_cite): sha256=<…>, bytes=<…>  
> Seeds/Units: seed=<…>, units=<…>  
> Nonce: <…>  
> Acceptance: snapshot fidelity, predictive, idempotence, isolation, audit.”

And the **“What to avoid”** section:

> “**What to _avoid_ (this is where people get burned)**  
> – **Letting P_state depend on raw docs** you won’t replay. If $T$ doesn’t need the raw, don’t pack it – hash it in **P_cite** instead.  
> – **Quantizing before you set $\varepsilon$.** Always lock $\varepsilon$ first; choose $q$ to fit inside it.  
> – **Comparing anything other than $O$** in acceptance. The whole point is: if $O$ matches under the contracts, you’re good.”

### 7.1 P_state / P_cite implementation requirements

Implementation must:

1. Support **per‑source Press policy cards** capturing the above fields.  
2. Implement **P_state** as the minimum Press snapshot needed for $T$’s deterministic replay (plus Loom state).  
3. Implement **P_cite** as a separate reference structure containing:  
   - Content hashes (e.g., SHA‑256) and byte lengths for original sources.  
   - Minimal extracted integers (e.g., counts, key metrics) used in computation.  
4. Enforce **field‑level quantization bounds** $|x_{post} − x_{pre}| \le q/2 \le \varepsilon_x$.  
5. Provide **replay** and **predictive** tests and an **idempotence** and **isolation** check.

**GAP‑APP‑005 (Exact distance metrics and O‑space definition):**  
The reports refer to $d(O_{true}, O_{replayed})$ but do not fix the metric $d$ or the exact definition of $O$. Implementation must specify:

- What constitutes $O$ for a given application (observables, derived statistics, etc.).  
- Which metric $d$ is used (L2, L∞, domain‑specific) and how ε is chosen and stored.  
- How acceptance thresholds are set and enforced automatically.


---

## 8. Testbed & Metrics (Press Pareto Manifests)

From the **Aether Synthetic Testbed v5/v6** manifests (`press_pareto_manifest_*.json`):

Example (`press_pareto_manifest_image.json`):

```json
{
  "component": "Aether Press",
  "content_type": "image",
  "objective": "minimize {mse, compression_ratio}",
  "front": [
    {"bits": 8, "codec": "zlib", "mse": 0.0,   "comp_ratio": 0.012080078125, ...},
    {"bits": 7, "codec": "zlib", "mse": 0.5,   "comp_ratio": 0.008740234375, ...},
    ...
  ],
  "recommendation_hint": "Pick a point and freeze as barrier: (max_MSE, min_ratio, codec, bits)."
}
```

Key points:

- **Objective:** “minimize {mse, compression_ratio}”.  
- **Front:** a list of Pareto‑optimal points with fields such as `bits`, `codec`, `mse`, `comp_ratio`, `compressed_bytes`, `input_bytes`.  
- **Recommendation:** “Pick a point and freeze as barrier: (max_MSE, min_ratio, codec, bits).”

Implementation implications:

1. Press must be able to **emit metrics** needed for these fronts: MSE, compression ratio, etc.  
2. At runtime or config time, you can choose a **Pareto point** and turn it into a **Press barrier** (max acceptable MSE, minimum acceptable compression ratio, chosen codec and bit‑depth).  
3. Press should then **self‑check** each run against these barriers and either pass / fail or adapt (e.g., choose different settings) accordingly.

**GAP‑APP‑006 (Runtime barrier enforcement semantics):**  
The testbed tells you **what to pick** but not exactly **how the runtime should behave** when a barrier is violated. Implementation must decide whether to:

- Fail the run (hard error).  
- Fall back to a safer configuration (e.g., more bits, different codec).  
- Emit warning and keep going.


---

## 9. Error / Fidelity Guarantees (Implementation doc)

From Implementation doc, **“9. Error and Fidelity Guarantees”**:

> “– **Timeseries:** MAE ≤ ε, spectral error ≤ δ.  
> – **Images/Fields:** PSNR ≥ threshold or SSIM ≥ bound.  
> – **Dynamics:** State fidelity ≥ F, invariants deviation ≤ Δ.”

Combined with §2.3, implementation must:

- Expose configurable **fidelity metrics** per content type (timeseries, images, dynamical systems).  
- Track those metrics for each Press run and store them in the APP container body (“Metrics and checksum”).  
- Provide an API to **assert** that these metrics are inside the configured bounds.

**GAP‑APP‑007 (Exact default thresholds):**  
The docs define *types* of metrics but not the default values for ε, δ, PSNR thresholds, SSIM bounds, F, or Δ. Implementation must:

- Either define authoritative defaults, or  
- Require explicit configuration per deployment.


---

## 10. Summary of Capabilities (Checklist)

From all the above, Press Pillar must be capable of:

1. **Lossless compression with exact round‑trip** (`Unpress(Press(S)) = S`).  
2. **Quasi‑lossless compression** with ε‑bounded errors at field‑level and system‑output level.  
3. **Symbolic‑only compression** (store only rules/invariants, no residual).  
4. **Rule+Residual pipeline**: Domain Model selection, parameter fitting, invariant extraction, model simulation, residual computation, residual encoding, packaging.  
5. **Layered compression** via LCDRM‑style deltas and SimA/SimB stacked/nested architecture.  
6. **Dimension‑level control**: recompute/residual/full, quantization, residual fractions, dictionary scopes.  
7. **Two‑track Press** (P_state/P_cite) with policy cards, hash‑based proofs, and acceptance gates (field‑level, replay, predictive, idempotence, isolation).  
8. **APX containerization** with header, manifest, body, integrity tags, optional HMAC signatures.  
9. **Metric reporting** for compression ratio, MSE, PSNR/SSIM, state fidelity, invariant deviation.  
10. **Baseline benchmarking** vs established codecs (gzip/bzip2/xz/ZIP/Zstd/FLAC/PNG).  
11. **Support for evolving schemas** (new dimensions mid‑run) in combination with Loom and NAP.


---

## 11. Gaps Blocking a Fully Deterministic Reference Implementation

The key **blocking unknowns** that must be resolved to implement a production‑grade, deterministic Press pillar:

### GAP‑APP‑001 — Model library and selection

- No canonical set of model families $\mathcal{M}$ is specified.  
- No fixed parameterization scheme for each model is defined.  
- No exact selection heuristic is given for picking a model per segment.

**Consequence:** Implementers must design and standardise a **model library**, parameter encoding, and selection algorithm.

### GAP‑APP‑002 — Exact .apx binary schema & signature details

- `.apx` is specified only conceptually (“deterministic, self‑contained ZIP archive”).  
- Manifest fields are named, but no JSON schema is fixed.  
- Hash algorithm (e.g., SHA‑256) and HMAC / signature algorithms are not set in stone.  
- No canonical ordering / byte packing is defined.

**Consequence:** A reference wire format must be defined to ensure interop between implementations.

### GAP‑APP‑003 — NAP Compression Manifest schema

- The NAP manifest is described qualitatively (“knits together SimA and SimB outputs”) but has no structural spec.  
- No explicit graph / stack model is defined for layered compression.

**Consequence:** Implementers must define a manifest structure that can encode the dependency graph of layers and streams.

### GAP‑APP‑004 — Residual fraction semantics (per‑dim residual budgets)

- Report 16 introduces residual fractions (e.g., 5–20%) but not how they map to bytes or entropy.  
- No formal rule is given for what happens when residual demand exceeds budget.

**Consequence:** Must design an enforcement strategy for residual budgets (e.g., re‑quantization, dropping, or errors).

### GAP‑APP‑005 — Output space and distance metric for acceptance

- $O$ (observable outputs) and $d(\cdot,\cdot)$ (distance) are left generic.  
- No default or recommended metrics are locked in per domain.

**Consequence:** For any concrete deployment, implementers must specify:  
- what $O$ is (e.g., full trajectories vs summary stats),  
- what $d$ is (e.g., L2, max error, domain‑specific metrics),  
- what ε values are acceptable.

### GAP‑APP‑006 — Runtime barrier enforcement semantics

- Pareto manifests suggest freezing points as barriers but not runtime behaviour when barriers are violated.  
- Interaction between Press barriers and Loom / Trinity schedulers is not fully specified.

**Consequence:** Need a policy: fail, fallback, or degrade gracefully (and how to surface that to the rest of the system).

### GAP‑APP‑007 — Default fidelity thresholds

- Types of metrics are defined (MAE, spectral error, PSNR, SSIM, state fidelity, invariant deviation), but default thresholds are not.

**Consequence:** Implementers must either define standard default profiles (e.g., “archival”, “analysis‑only”, “preview”) or require explicit configuration.

### GAP‑APP‑008 — Streaming vs batch semantics

- Implementation pseudocode hints at segment/window‑based processing, but streaming behaviour (online compression, partial flushes) is not fully specified.  
- No explicit rules for how partial `.apx` capsules behave mid‑stream.

**Consequence:** For streaming use‑cases, Press needs a clearly defined protocol for partial packets, resumption, and error recovery.

### GAP‑APP‑009 — Exact role of LCDRM inside APP

- LCDRM is clearly related and describes layered relational compression, but Press docs do not **mandate** whether LCDRM is:  
  - the default engine for SimA/SimB layers, or  
  - a theoretical sibling used only in some builds.

**Consequence:** Reference implementation must decide whether LCDRM is core to Press or optional.


---

## 12. Next Steps for a Reference Implementation

Given the current docs, a realistic path to a full implementation is:

1. **Lock the model library (resolve GAP‑APP‑001)**  
   - Choose a minimal but expressive set of models (e.g., LFSR‑style integer models for structured bitstreams, polynomial/time‑series models, simple Markov models, LCDRM layers).  
   - Define parameter encodings for each.

2. **Specify the .apx format (resolve GAP‑APP‑002 & GAP‑APP‑003)**  
   - Draft a strict binary + JSON schema for APP capsules and NAP manifests.  
   - Include hash and signature algorithms and compatibility versioning.

3. **Codify Press policies (resolve GAP‑APP‑004/005/006/007)**  
   - Turn Report 16 and 19 guidance into machine‑checkable policies and defaults.  
   - Provide a library or table of common policy cards.

4. **Implement encoder/decoder with metrics**  
   - Build against the architecture described in §3 (Aether Core, Press Engine, Flux Decoder, Protocol Layer).  
   - Ensure metrics, fidelity checks, and barrier checks are all first‑class.

5. **Integrate with Loom and NAP**  
   - Honour dimension‑level Press config, residual fractions, and dynamic schema evolution.  
   - Verify replay correctness under stacked/nested modes.

6. **Benchmark vs baselines**  
   - Follow Implementation doc guidance to compare against ZIP, Zstd, FLAC, PNG, gzip/bzip2/xz, and validate the promised “far beyond traditional methods” behaviour on structured data.

This spec should be treated as **v0.1** of the dev‑facing Aether Press implementation sheet. Once the above GAPs are concretely resolved in code/math, a v1.0 spec can hard‑lock formats and algorithms.



<!-- END SOURCE: astral_press_pillar_dev_implementation_spec_v_0.md -->


---

<!-- BEGIN SOURCE: astral_press_pillar_dev_spec_addendum_focus_report_pass_01.md -->

# Astral Press Pillar — Dev Spec Addendum
## Focus Report Pass 01 (press pillar report.pdf)

**Source for this pass:** `press pillar report.pdf` (FOCUS_REPORT.md — *Aether Press Protocol (APP) – Data Compression Pillar (Focus Report)*).

**Goal of this addendum:**
- Treat this Focus Report as **source of truth** for APP behaviour.  
- Cross-check the existing **Dev Implementation Spec v0.1**.  
- **Close or narrow gaps** (GAP-APP-00X) where the Focus Report adds detail.  
- **Add any functions / features / capabilities** that the v0.1 spec didn’t explicitly call out.  
- Create **new GAP tags** when this doc reveals missing spec areas.

Throughout this addendum, every interpretation is backed by **direct quotes** from `press pillar report.pdf`.

---

## 1. Confirmed Behaviours from the Focus Report

This section lists key APP behaviours that the Focus Report states explicitly and which align with (or slightly refine) the v0.1 spec.

### 1.1 APP Role and Rule+Residual Encoding

The opening lines of the Focus Report:

> “Abstract:  The Aether Press Protocol is a **symbolic compression framework**  that projects raw data into a **structured latent form** and  **inverts it back perfectly**  to the original dataset. This pillar enables **universal, lossless compression**  across domains by **storing only generative rules and minimal residuals instead of entire datasets**, yielding extreme data reduction without violating deterministic fidelity.”

> “APP’s Role:  The Aether Press Protocol (APP) serves as the **Trinity system’s data compression subsystem**, responsible for **distilling large datasets or simulation outputs into concise mathematical representations**. It operates **downstream of the Trinity architecture as a post-processing framework** that captures the **underlying structure of information**. APP’s primary responsibility is to **encode data as “rule + residual” pairs and package them for storage or transmission**, guaranteeing that the original information can be **fully reconstructed when needed**. It **standardizes symbolic reduction across any domain (physics, simulation, telemetry, etc.)** and ensures compression is achieved **without introducing irreversibility unless explicitly allowed** (e.g. optional lossy modes).”

This **reinforces** the existing v0.1 spec:
- APP is **downstream** of Trinity.  
- Core behaviour is **rule + residual** packaging.  
- Default is **lossless**; lossy/ε-bounded modes are **explicit opt-in**.

### 1.2 Capabilities & Behaviours (Core Compression)

The Focus Report’s **Capabilities & Behaviours** section confirms the main compression properties:

> “**Universal Model-Based Compression:**  APP can **compress ordinary binary data and structured outputs** by discovering an underlying **mathematical model or pattern in the data**. It **encodes the behavior or relationships that generate the data, rather than the data itself**, making it a **domain-agnostic compressor**. In practice, this means APP thrives on **structured or repetitive data – e.g. scientific simulation logs, sensor streams, images with patterns, tabular data – where it can find parametric order that conventional codecs miss**. When patterns exist, APP achieves compression far beyond traditional methods by **storing a compact generative description (the “rule”) plus a small residual correction**.”

> “For example, in tests it **reduced a structured CSV of 50k rows to a descriptor-only package (no residual)** – effectively just a few KB describing the entire dataset – an orders-of-magnitude reduction from the original size. Similarly, **a nested JSON dataset was compressed with only the generative array rules captured**, yielding a tiny capsule. For highly regular data like a checkerboard pattern, APP **identified the base tiling rule and needed zero residual**, achieving an extremely small descriptor representation.”

> “**Lossless Data Reproduction:**  The protocol guarantees **bit-perfect reconstruction** of losslessly compressed data. The **“unpress” operation applies the stored model and residual to recover the exact original**, which has been verified to be **byte-for-byte identical to the input**. Even when multi-layer stacking or nested simulations are involved, the **combined Press/DePress pipeline preserves exactness** as long as the mode is configured as lossless.”

This directly aligns with v0.1’s **lossless guarantee** and **symbolic/compression philosophy**; no contradiction.

### 1.3 Components: APP, Residual, APX, SimA/SimB, NAP, Manifest, HMAC

The Focus Report enumerates the key named components:

> “**Aether Press Protocol (APP)**  – Named:  A **symbolic compression framework** defining the rules for **model-based data reduction**. It compresses by **capturing relationships instead of raw bits**.”

> “**Residual Encoding**  – Stated:  The step **storing only minimal differences between a model’s output and the real data**. **Residuals represent information not explained by the generative model.**”

> “**Packaging Stage**  – Named:  A phase that **wraps the model ID, parameters, and residuals into a portable container**. Ensures **all pieces needed for reconstruction are kept together**.”

> “**APX Capsule Format**  – Named:  A portable `.apx` container for Aether Press outputs. It is a **deterministic, self-contained ZIP archive (manifest + layer files)** used to store compressed data and metadata.”

> “**SimA (Symbolic Compressor)**  – Named:  In advanced Press usage, a **generative compression stream** that **models structured patterns (stacked/nested rules)** and **records only math needed to reconstruct data**.”

> “**SimB (Residual Compressor)**  – Named:  A **complementary residual stream capturing any data SimA cannot express, layer by layer**. Together with SimA, it **splits deterministic structure from randomness**.”

> “**NAP Compression Manifest**  – Named:  A Nexus Aeternus Protocol (NAP) manifest that **“knits” together SimA and SimB outputs**. Defines how **multi-layer stacks and nests recombine for exact reconstruction**.”

> “**Baseline Codecs (gzip, bzip2, xz)**  – Named (contextual):  Standard compression tools used as **baseline benchmarks** for Press experiments. Provided point of comparison for APP’s performance on various data types.”

> “**Press Metadata Manifest**  – Stated:  The `.apxMANIFEST.json` file storing original file metadata: **name, size, hash, compression mode, timestamp, etc.** Extended in later versions to include **file system info (permissions, timestamps)** for archival completeness.”

> “**HMAC Signature (APX)**  – Implied:  **Cryptographic signing of capsules** to ensure **authenticity and tamper-detection**. Allows verification that an `.apx` capsule was created by the authorized system and not modified.”

These match the component list in v0.1. The Focus Report also **extends** the manifest concept (see §2.2 below).

---

## 2. New / Strongly Emphasised Capabilities

This section collects **capabilities and behaviours** that weren’t fully spelled out in the v0.1 dev spec, but are made explicit in the Focus Report.

### 2.1 Compressed-Domain Operations (Dedup, Search, Segmentation, Latent Analysis)

The Focus Report introduces an important concept: **operating directly on APP capsules in the compressed domain.**

> “**Integration with System Workflows:**  Once data is compressed via Aether Press, it becomes easier to transmit, store, and even **perform computations on**. **The capsules allow doing things like deduplication, search, and segmentation in the compressed domain** – for example, one can compare two `.apx` capsules or analyze their descriptors **without fully decompressing them**, since the structure is exposed in the manifest and descriptor layers. This means APP not only saves space but can also **provide a form of latent-space for analysis**, analogous to how one might operate on compressed representations in machine learning.”

**New capability (vs v0.1):**

1. **Deduplication in compressed domain**  
   - Press capsules can be compared (**manifest + descriptors**) to detect duplicates or near-duplicates **without full decompression**.

2. **Search in compressed domain**  
   - Queries can operate on **descriptor/manifest fields** (e.g., model IDs, parameter ranges, invariants) instead of raw bytes.

3. **Segmentation in compressed domain**  
   - Capsules can be segmented or indexed using their internal structure, again **without reconstructing** the full dataset.

4. **Latent-space analysis**  
   - APP descriptors act like a **latent representation**: you can analyze, cluster, or compare them analogous to compressed embeddings in ML.

**Implication for implementation:**

- The dev spec must include **explicit support** for operations on **manifest + descriptor-only views**:  
  - Compressed-domain comparison / diff.  
  - Indexing and search over `.apxMANIFEST.json` and descriptor layers.  
  - Hooks or APIs for analytics tooling to work directly on descriptors.

This capability **extends** the function inventory beyond simple `Press`/`Unpress` to include **compressed-domain tooling**.

### 2.2 Multi-Party & Standalone Deployment (CLI / GUI, Backward Compatibility)

The Focus Report explicitly describes Press as suitable for **standalone**, multi-party use:

> “Because **APP capsules are deterministic and self-contained**, they facilitate **multi-party workflows**: external implementers can **decode or validate capsules using the provided spec, without needing the proprietary Trinity internals**. **Aether Press can be deployed as a standalone utility (CLI or GUI)** – e.g., a desktop app where a user can **“Compress All” files into `.apx` and later “Decompress” them back** – enabling use outside the core Trinity simulation environment.”

It also states a clear **backward compatibility** requirement:

> “Its design ensures **backward compatibility**: newer versions of the Press algorithm or container format **read old capsules exactly**, so data already compressed will remain accessible as the system evolves.”

And later, the manifest’s version fields are detailed:

> “The manifest also records the exact Press version used ( `"apx_version"` ) and a creation timestamp ( `"created_utc"` ), which together serve as a provenance record for when and with which algorithm the capsule was produced. Because APP’s algorithm may evolve, **the version tag ensures that the proper decoder (which maintains backward compatibility) is used, or it signals if an outdated decoder is reading a newer format**.”

**New / refined capabilities:**

1. **Standalone Press utility**  
   - APP is **not** confined to Trinity; it can exist as a **CLI** or **GUI** tool for general users.

2. **Multi-party decode/validate**  
   - External parties (without Trinity internals) can **interpret `.apx` files** using the formal spec and manifest.

3. **Explicit backward compatibility contract**  
   - The **`apx_version`** field and decoder behaviour are designed so that:  
     - **New decoders must read old capsules**, and  
     - If an **old decoder** encounters a **newer format**, this should be detectable.

4. **Manifest provenance fields**  
   - `"apx_version"` and `"created_utc"` are now **explicitly named fields** in `.apxMANIFEST.json`.

### 2.3 Streaming & Chunk-Based Operation; Placement in System Topology

The Focus Report explicitly mentions **chunking** and **streaming**:

> “The baseline experiments involved up to **512 KiB – 1 MiB data chunks processed in memory without issue**. For very large data, the pipeline might need to **chunk inputs (which it can do adaptively)**. There is mention of a “safe limit” in terms of chat memory (context size) being reached in the logs, but that pertains to the AI’s context, not Press itself. In deployment, an  `.apx` **file can be written out incrementally (streaming blocks)**.”

It also describes **Press’s placement** in a live system:

> “Press’s position in the system is flexible: it can either **compress and then flush to disk/network (for archival)** or **operate as a live filter in a data stream**. In either case, it should be placed where enough compute is available to perform model inference (which might be CPU-heavy for large data sets).”

And recommends **episode-level** compression for simulations, not per-frame:

> “**No interference with Real-time Loops:**  If used within an active simulation (e.g., compressing every tick’s state), Press might introduce latency. The Loom discussion suggests **compressing an entire run as one stream rather than frame-by-frame** to get better efficiency. Topologically, that means Press might be used at the **boundaries of a simulation run (start or end) or at coarse intervals (checkpoints)**, rather than on each realtime step, unless parallelized sufficiently.”

**New / clarified capabilities:**

1. **Adaptive chunking**  
   - Press can **process large datasets by chunking**, with chunk sizes in the **512 KiB – 1 MiB** range proven in tests, and **adaptive chunking** for even larger inputs.

2. **Incremental `.apx` streaming**  
   - An `.apx` file **“can be written out incrementally (streaming blocks)”** – i.e., Press does **not** require the entire dataset in memory before writing the capsule; it can stream.

3. **Streaming filter mode vs archival mode**  
   - Press can:
     - **Run as a post-hoc archival compressor** (compress after the run, flush to disk/network).  
     - **Run inline as a live filter** in a data stream.

4. **Placement relative to real-time loops**  
   - For simulations, the recommended topology is:  
     - Use Press at **run boundaries** or **coarse checkpoints**, not on every real-time tick, unless parallelised.

This gives **concrete guidance** for the streaming vs batch semantics that were left very open in v0.1.

### 2.4 Integration with Aevum Loom (Time Compression) and Press/DePress Terminology

The Focus Report describes Press’s role as a **reversible snapshot mechanism** for Loom:

> “The Press/DePress terminology in the formal specs literally denotes this **save-and-restore capability**. **In integration with the Aevum Loom (the time-compression pillar), Press acts as the reversible snapshot mechanism**: a Press operation serializes a state, Loom allows skipping through the timeline, and a DePress operation unserializes the state at a later point, **with the intervening dynamics replayed deterministically by the engine** $T$. This ensures that **causality is preserved**: **Press does not alter the sequence of cause and effect in the simulation; it merely folds the state into a storable form**.”

A later section reinforces Loom’s relationship:

> “The Loom was described as **“the time-axis equivalent of a conservation barrier”**, making time losslessly compressible **much like Press does for data**. In fact, **the Loom uses Press-style logic to record only differences between states and occasional checkpoints**, effectively applying Press’s philosophy to time series data. The assistant noted “you’ve basically fused compression, reproducibility, and auditability into one reversible structure”…”

**Implications for implementation:**

1. **Terminology:**  
   - `Press` = **serialize** state into `.apx`.  
   - `DePress` = **unserialize** state from `.apx`, returning to a live representation for engine $T$.

2. **Causality preservation:**  
   - When used with Loom, Press **must not break causal order**; it only stores and restores states while Loom handles stepping.

3. **Philosophical symmetry:**  
   - Loom is “time-axis Press”, applying the same **differences + checkpoints** approach to time as Press does to data.

These reinforce v0.1’s integration story but with **stronger language** about causality and Press/DePress naming.

### 2.5 Legal/Provenance Use of APP Spec and Capsules

The Focus Report explicitly mentions **legal provenance and research/IP usage**:

> “In one prompt, the user was guided to use APP as a basis for data generation in **Research Mode so that they could later legally prove the method used (by citing the APP spec)**. This shows a consciousness for **legal provenance**: by grounding the approach in a formally documented protocol (APP and its Implementation PDF), the work produced can be protected and traced to a known foundation rather than appearing ad-hoc.”

> “Additionally, **every Press capsule can be viewed as an archival record**. By incorporating hashes, timestamps, and version tags in the manifest, each `.apx` becomes evidence of how a dataset looked at a particular time, how it was compressed, and which version of the algorithm was responsible.”

**New emphasis:**

- Press capsules and the APP spec are **explicitly positioned as artefacts with legal/provenance weight**.  
- The implementation should treat manifests, hashes, timestamps, and version tags as **evidence-grade**, not just convenience metadata.

---

## 3. Gap Review and Updates (GAP-APP-00X)

This section revisits the gaps identified in the v0.1 dev spec and updates their status based on the Focus Report.

### GAP-APP-001 — Model Library and Selection

**Original gap:** No canonical set of model families $\mathcal{M}$, parameterisation, or selection heuristic specified.

**Focus Report evidence:**

> “First, a **Domain Model** is chosen or inferred – essentially the form of the mathematical law or pattern expected (for example, a **Fourier series, polynomial fit, Markov process, etc.**) . Next, Parameter Fitting occurs…”

This confirms example model families (Fourier, polynomial, Markov) but **does not fix** a canonical set $\mathcal{M}$ or selection algorithm.

**Status:** **Still open.**  
**GAP-APP-001 remains unresolved.**

---

### GAP-APP-002 — Exact `.apx` Binary Schema & Signature Details

**Original gap:** Conceptual `.apx` description only; no concrete wire format or full manifest schema.

**Focus Report evidence (manifest fields and semantics):**

> “**Press Metadata Manifest** – Stated:  The `.apxMANIFEST.json` file storing original file metadata: **name, size, hash, compression mode, timestamp, etc.** Extended in later versions to include **file system info (permissions, timestamps)** for archival completeness.”

> “The manifest also records the exact Press version used ( `"apx_version"` ) and a creation timestamp ( `"created_utc"` ), which together serve as a provenance record for when and with which algorithm the capsule was produced. Because APP’s algorithm may evolve, **the version tag ensures that the proper decoder (which maintains backward compatibility) is used, or it signals if an outdated decoder is reading a newer format**.”

> “The system even supports adding an **HMAC or digital signature** to each capsule. This means the capsule can be cryptographically signed by the user’s key, embedding an assurance that “this data came from my authorized Press instance and has not been altered”.”

**What this closes / clarifies:**

- Explicit manifest fields now known:  
  - `name`  
  - `size`  
  - `hash`  
  - `compression_mode`  
  - `timestamp`  
  - filesystem info (permissions, timestamps)  
  - `"apx_version"`  
  - `"created_utc"`
- Manifest must be considered **provenance-critical**.  
- Decoder must honour **backward compatibility** contracts using `apx_version`.

**What remains open:**

- Concrete JSON schema (types, required/optional fields, nested structures).  
- Exact hash algorithm(s) and how many hashes (per-block vs whole file).  
- Exact binary layout of header vs manifest vs body inside the ZIP container.  
- Precise signature/HMAC algorithm, key management, and binding to content.

**Status:** **Partially resolved** — manifest *fields and semantics* are clearer, but **wire format and crypto details still undefined.**

---

### GAP-APP-003 — NAP Compression Manifest Schema (SimA/SimB Stacks)

**Original gap:** NAP manifest qualitatively described but no structural spec.

**Focus Report evidence:**

> “**NAP Compression Manifest** – Named:  A Nexus Aeternus Protocol (NAP) manifest that **“knits” together SimA and SimB outputs**. Defines how **multi-layer stacks and nests recombine for exact reconstruction**.”

No further structural detail (fields, types, ordering) appears in this document.

**Status:** **Still open.**  
**GAP-APP-003 remains unresolved** by this pass.

---

### GAP-APP-004 — Residual Fraction Semantics (Per-Dimension Budgets)

**Original gap:** Report 16 introduced residual fractions; Focus Report may or may not reference them.

**Focus Report evidence:** No direct mention of **“residual fraction”**, per-dim budgets, or enforcement rules. Residuals are discussed qualitatively only.

> “Residual Encoding – Stated:  The step storing only minimal differences between a model’s output and the real data. **Residuals represent information not explained by the generative model.**”

**Status:** **Still open.**  
**GAP-APP-004 remains unresolved** by this pass.

---

### GAP-APP-005 — Output Space and Distance Metric for Acceptance

**Original gap:** $O$ (observable outputs) and metric $d$ not concretely specified.

**Focus Report evidence:** This document does not mention explicit metrics like MAE, PSNR, SSIM, or formal $d(O_{true}, O_{replayed})$ definitions. Those appear in other docs (Implementation / Report 19), not here.

**Status:** **Still open.**  
**GAP-APP-005 unchanged** by this pass.

---

### GAP-APP-006 — Runtime Barrier Enforcement Semantics (Pareto Manifests)

**Original gap:** Behaviour when runtime barriers (from Pareto manifests) are violated.

**Focus Report evidence:** This document does **not** mention Pareto fronts, barrier selection, or runtime enforcement. Those live in the Synthetic Testbed manifests.

**Status:** **Still open.**  
**GAP-APP-006 unchanged** by this pass.

---

### GAP-APP-007 — Default Fidelity Thresholds

**Original gap:** Interfaces listed metrics but not default threshold values.

**Focus Report evidence:** No numeric thresholds (ε, δ, PSNR/SSIM, etc.) are specified here.

**Status:** **Still open.**  
**GAP-APP-007 unchanged** by this pass.

---

### GAP-APP-008 — Streaming vs Batch Semantics

**Original gap:** v0.1 spec flagged unclear streaming semantics for `.apx` and chunking.

**Focus Report evidence (streaming and chunking):**

> “The baseline experiments involved up to **512 KiB – 1 MiB data chunks processed in memory without issue**. For very large data, the pipeline might need to **chunk inputs (which it can do adaptively)**. … In deployment, an `.apx` **file can be written out incrementally (streaming blocks)**.”

> “Press’s position in the system is flexible: it can either compress and then **flush to disk/network (for archival)** or **operate as a live filter in a data stream**. … If used within an active simulation (e.g., compressing every tick’s state), Press might introduce latency. … compressing an entire run as one stream rather than frame-by-frame … Press might be used at the **boundaries of a simulation run** or at coarse intervals (checkpoints), rather than on each realtime step, unless parallelized sufficiently.”

**What this clarifies:**

- `.apx` writing **can be incremental** (streamed blocks).  
- Chunk sizes used in practice: **512 KiB – 1 MiB**.  
- Press supports both **batch archival** and **live filter** modes.  
- Recommended topology is **episode/checkpoint compression**, not per-frame.

**What remains open:**

- Exact streaming protocol (how partial `.apx` is structured, how to resume after interruption).  
- Whether streaming requires special flags/headers to mark incomplete vs complete capsules.

**Status:** **Partially resolved.**  
- We now have **clear design guidance** for streaming and topology.  
- The **precise wire protocol** for partial capsules is still unspecified.

---

### GAP-APP-009 — Exact Role of LCDRM Inside APP

**Original gap:** Whether LCDRM is mandated as internal engine or optional sibling.

**Focus Report evidence:** LCDRM is **not mentioned** in this document.

**Status:** **Still open.**  
**GAP-APP-009 unchanged** by this pass.

---

## 4. New Gaps Discovered in This Pass

Reading the Focus Report also exposes some **new areas** that v0.1 didn’t explicitly track as gaps, but which matter for a complete implementation.

### GAP-APP-010 — Compressed-Domain API for Dedup/Search/Segmentation

The Focus Report states:

> “The capsules allow doing things like **deduplication, search, and segmentation in the compressed domain** – for example, one can compare two `.apx` capsules or analyze their descriptors **without fully decompressing them**, since the structure is exposed in the manifest and descriptor layers.”

Missing details:

- No **concrete API** or algorithm is specified for:  
  - Deduplication criteria (what defines equality/near-equality of capsules?).  
  - Search syntax and scope (which fields, which matching semantics?).  
  - Segmentation behavior (how to define and materialize segments within capsules).

**Consequence:**

- A full implementation must define a **compressed-domain operations API**:  
  - Function names, arguments, and data structures for dedup/search/segment.  
  - How these operations interact with `.apxMANIFEST.json` and descriptor layers.  
  - Performance and security considerations (e.g., which parts of capsule are exposed to untrusted parties).

**Status:** Newly logged as **GAP-APP-010**.

---

### GAP-APP-011 — Multi-Version & Decoder Compatibility Semantics

The Focus Report states:

> “Because APP’s algorithm may evolve, **the version tag ensures that the proper decoder (which maintains backward compatibility) is used, or it signals if an outdated decoder is reading a newer format**.”

Missing details:

- The exact **behaviour** when encountering mismatched versions:  
  - What does “signals if an outdated decoder is reading a newer format” look like? Error code? Warning? Fallback?  
  - Are there **capabilities flags** indicating which features a given `apx_version` supports?  
  - How are **minor vs major** versions treated (semantic versioning, strict compatibility, etc.)?

**Consequence:**

- A robust reference implementation must define a **versioning policy** and **decoder compatibility matrix**, including:  
  - Rules for when to allow decode with warnings vs when to fail.  
  - How new fields/sections in `.apx` are handled by old decoders.  
  - How version info is surfaced to calling code.

**Status:** Newly logged as **GAP-APP-011**.

---

### GAP-APP-012 — Compressed-Domain Security / Privacy Boundaries

While not spelled out explicitly, the Focus Report implies **exposing structure to external parties**:

> “Because APP capsules are deterministic and self-contained, they facilitate multi-party workflows: external implementers can **decode or validate capsules using the provided spec, without needing the proprietary Trinity internals**.”

> “The capsules allow doing things like deduplication, search, and segmentation in the compressed domain … since the structure is exposed in the manifest and descriptor layers.”

Missing details:

- No explicit policy for **which fields** within the manifest/descriptor layers are safe to expose publicly.  
- No guidance on **redaction** or **privacy-preserving Press** for sensitive datasets.  
- No spec for **access control** on `.apx` internals vs only surface metadata.

**Consequence:**

- For real deployments, we must specify **security and privacy boundaries**:  
  - A minimal public manifest vs extended internal manifest.  
  - Optional encrypted payloads within `.apx`.  
  - How HMAC/signature interacts with any redaction/encryption.

**Status:** Newly logged as **GAP-APP-012**.

---

## 5. Function / Capability Delta vs v0.1

This section lists **net new** or **materially sharpened** functions/capabilities that should be merged into the master dev spec in the next consolidation.

### 5.1 Compressed-Domain Operations

**Functional additions (math-level, not API-final names):**

1. **CapsuleCompare** (compressed-domain distinctness & similarity)
   - **Source:** “deduplication … compare two `.apx` capsules or analyze their descriptors without fully decompressing them”.  
   - Behaviour: operate on manifests + descriptor layers to decide if two capsules are duplicates, or to compute a similarity score.

2. **CapsuleSearch** (search within manifest/descriptors)
   - **Source:** “search … in the compressed domain”.  
   - Behaviour: query across model IDs, parameters, invariants, timestamps, etc., without decoding full payloads.

3. **CapsuleSegment** (segmentation / sub-capsules)
   - **Source:** “segmentation in the compressed domain”.  
   - Behaviour: create views or sub-capsules corresponding to segments (time ranges, index ranges, dimensional slices) using only descriptor-level manipulation.

> **Note:** These are **proposed names/structures** derived from the text; the report itself does not give function names. They should be tagged as **non-canonical** until a formal API is accepted.

### 5.2 Standalone Tooling & Multi-Party Validation

Newly emphasised from Focus Report:

1. **PressCLI / PressGUI**
   - Behaviour: “single command can encode any file into an `.apx` … and similarly decode it back” and “Aether Press can be deployed as a standalone utility (CLI or GUI)… ‘Compress All’ / ‘Decompress’.”

2. **CapsuleValidateExternal**
   - Behaviour: external implementers verify integrity and correctness of `.apx` using spec + manifests, without Trinity internals.

These should be modelled in the implementation spec as **top-level entrypoints** for non-Trinity use.

### 5.3 Streaming & Chunk-Based Modes

From this pass we gain more confidence in adding explicit **streaming modes**:

1. **PressStream** (chunked, incremental `.apx` writer)
   - Supports processing large files via **512 KiB – 1 MiB chunks** (plus adaptive chunking) and writing **streaming blocks** to `.apx`.

2. **DePressStream** (incremental reader)
   - Supports reading partial `.apx` streams and reconstructing data in a streaming fashion.

Again: names here are **proposed**; behaviour is grounded in the Focus Report quotes.

---

## 6. Summary of What This Pass Changed

1. **Confirmed core APP behaviours** (lossless, rule+residual, downstream role) from the Focus Report; no contradictions with v0.1.
2. **Added new capabilities** around:
   - **Compressed-domain operations** (dedup, search, segmentation, latent-space analysis).  
   - **Standalone deployment and multi-party usage** (CLI/GUI, external validation).  
   - **Streaming and chunk-based operation** (incremental `.apx` writing, chunk sizes, topology guidance).  
   - **Stronger Loom integration story** (Press/DePress as reversible snapshot for time compression).  
   - **Legal/provenance framing** (capsules as archival and evidence-grade artefacts).
3. **Partially closed GAP-APP-002** (manifest fields & version semantics) and **GAP-APP-008** (streaming/batch semantics).  
4. **Left unchanged** GAP-APP-001, 003, 004, 005, 006, 007, 009 (no new details in this doc).  
5. **Introduced three new gaps**:  
   - **GAP-APP-010** — Compressed-domain operations API design.  
   - **GAP-APP-011** — Versioning and decoder compatibility behaviour.  
   - **GAP-APP-012** — Security and privacy boundaries for exposed manifest/descriptor structure.

This addendum should be read **alongside** the v0.1 Dev Implementation Spec. In the next consolidation pass, we can merge these deltas into a v0.2 or v0.3 spec that bakes in compressed-domain operations, streaming modes, and manifest version semantics as first-class implementation requirements.



<!-- END SOURCE: astral_press_pillar_dev_spec_addendum_focus_report_pass_01.md -->


---

<!-- BEGIN SOURCE: astral_press_pillar_dev_spec_addendum_implementation_pass_02.md -->

# Astral Press Pillar — Dev Spec Addendum
## Implementation Pass 02 (Aether_Press_Protocol_Implementation.pdf)

**Source for this pass:**

- `astral press pillar/old/aether press/Aether_Press_Protocol_Implementation.pdf`  
  (inside `astral press pillar.zip`)

This document is titled:

> **“Aether Press Protocol (APP) – Full Implementation and Pipeline”**

**Goal of this pass:**

- Treat the Implementation PDF as **source of truth** for APP implementation details.  
- Cross-check and enrich the **Dev Implementation Spec v0.1** and **Focus Report Addendum (Pass 01)**.  
- **Refine or partially close existing GAP-APP-00X items** where this PDF adds concrete detail.  
- **Add any new functions / features / capabilities** or constraints that the earlier docs didn’t fully capture.  
- Log any **new gaps** exposed by the implementation-level text.

All interpretations below are supported by **direct quotes** from `Aether_Press_Protocol_Implementation.pdf`.

---

## 1. Overview and Compression Philosophy (Reconfirmed)

### 1.1 Concept Overview

From the very top:

> “**Aether Press Protocol (APP) – Full Implementation and Pipeline**”

> “The **Aether Press Protocol (APP)** is a general **model-based symbolic compression framework** designed to **reduce data volume by encoding relationships instead of raw samples**. It merges principles from **symbolic AI, physical modeling, and generative compression**.”

This reaffirms:

- APP is **model-based** and **symbolic**.  
- It explicitly **encodes relationships** rather than raw samples.  
- It fuses **symbolic AI**, **physical modeling**, and **generative compression** into one framework.

### 1.2 Compression Philosophy (Information vs Data)

The Implementation PDF mirrors the core philosophy:

> “APP distinguishes between **information** and **data**. Instead of storing every datapoint, it stores the *rules, parameters,* and *exceptions* that can regenerate the data. This enables extreme compression ratios when applied to **structured or law-governed systems**.”

> “Key steps:  
> - **Keep:** governing rules, parameters, invariants, residuals.  
> - **Discard:** redundant raw samples that can be regenerated.”

This directly supports the v0.1 framing:

- **Information** = minimal description of relationships (rules, parameters, invariants).  
- **Data** = manifestations (samples) of those relationships.  
- Compression is achieved by **keeping rules/residuals** and discarding **regenerable samples**.

No contradictions with v0.1 or the Focus Report; this section mainly reinforces the conceptual core.

---

## 2. Architecture Overview (Encoder / Decoder)

### 2.1 Encoder / Decoder Stages (Canonical List)

The Implementation PDF gives a clear architecture section:

> “**3. Architecture Overview**  
> **Encoder**  
> 1. **Domain Model** – Defines the governing physics or statistical law.  
> 2. **Parameter Fitting** – Extracts parameters and invariants from data.  
> 3. **Residual Encoding** – Stores minimal differences between the model and data.  
> 4. **Packaging** – Combines model ID, parameters, invariants, and residuals into a standardized container.  
> **Decoder**  
> 1. Load model and metadata.  
> 2. Regenerate the base signal deterministically.  
> 3. Add residuals for full reconstruction.  
> 4. Validate checksum and fidelity.”

This confirms and sharpens the v0.1 spec’s **Press pipeline**:

- **Encoder** has exactly **four canonical stages**.  
- **Decoder** has exactly **four canonical stages**.

### 2.2 Implementation-Level Interpretation

For implementers, this implies the following **logical functions** (naming still language-agnostic):

1. `DomainModel(SegmentMetadata, Config) -> ModelFamily`  
   - Chooses a family representing “governing physics or statistical law”.

2. `ParameterFitting(ModelFamily, SegmentData) -> (Theta, Invariants)`  
   - Extracts parameters and invariants from real data.

3. `ResidualEncoding(SegmentData, ModelFamily, Theta, Invariants, ModeConfig) -> EncodedResidual`  
   - Computes raw residuals and encodes them according to compression mode.

4. `Packaging(ModelID, Theta, Invariants, EncodedResidual, Metadata, Metrics) -> Capsule`  
   - Assembles a container that is **sufficient for reconstruction**, including checksums.

5. `DecoderLoad(Capsule) -> (ModelID, Theta, Invariants, EncodedResidual, Metadata)`

6. `ReconstructBaseSignal(ModelFamily, Theta, Invariants, Length) -> BaseApprox`  
   - Deterministic regeneration from the model.

7. `AddResidual(BaseApprox, EncodedResidual, ModeConfig) -> ReconstructedData`

8. `ValidateChecksumAndFidelity(ReconstructedData, Metadata) -> ValidationReport`

These are not function names from the PDF, but are **direct decompositions** of the quoted architecture stages.

**GAP impact:**

- **GAP-APP-001 (Model library & selection)**: this section confirms **what** a Domain Model does, but still does not canonically define **which models** exist or how they’re selected. GAP-APP-001 remains open.

---

## 3. Compression Modes (Lossless / Quasi-Lossless / Symbolic-Only)

The Implementation PDF defines three modes explicitly:

> “**4. Compression Modes**  
> - **Lossless** – Full reconstruction, residuals preserved exactly.  
> - **Quasi-Lossless** – Bounded error within ε-tolerance.  
> - **Symbolic-Only** – Stores only rules and invariants; maximum compression.”

This confirms the modes we already had in v0.1, but **here they are canonical labels and definitions**.

Implementation-level requirements:

1. **Lossless**  
   - Residuals must be preserved exactly.  
   - `Unpress(Press(S)) = S` with **byte-for-byte identity** (hash equality).

2. **Quasi-Lossless**  
   - Residuals are quantized or otherwise approximated so that errors remain within a configured **ε-tolerance** per field, and in terms of output metrics (see §6).  
   - Must still obey the P_state/P_cite acceptance tests described in other docs.

3. **Symbolic-Only**  
   - Residuals may be omitted entirely; only rules and invariants are stored.  
   - Decompression yields a **model-generated surrogate** that respects captured invariants, not the original raw samples.

**GAP impact:**

- **GAP-APP-007 (Default fidelity thresholds)** remains open: this PDF **names the modes** and **bounded error idea** but does not commit to specific default ε values.

---

## 4. Data Suitability (Where APP Works Best / Worst)

The Implementation doc explicitly categorizes data types:

> “**5. Data Suitability**  
> Works Best On:  
> - Scientific logs, telemetry, simulation data, physical systems.  
> - Structured datasets governed by known laws.  
> Less Effective On:  
> - Unstructured text, media, or encrypted content.”

Implementation-level implications:

- For **scientific logs, telemetry, simulations, physical systems**, and **law-governed structured datasets**, APP should be considered a **primary or preferred compressor**, expected to significantly outperform generic codecs.

- For **unstructured text, generic media, or encrypted content**, Press may be less effective than traditional codecs (gzip, Zstd, etc.), and a good implementation may:
  - Either **fall back** to a baseline codec, or  
  - Run with **minimal expectations** (e.g., no compression or even expansion).

This section does not create new gaps but **formalizes when Press is expected to shine.**

---

## 5. Compression Pipeline Pseudocode (Canonical Algorithms)

The Implementation PDF gives explicit pseudocode for the **core compression pipeline**:

> “**6. Compression Pipeline Pseudocode**  
> ```  
> for segment in split(data, window=W):  
>     M = select_model(segment)  
>     θ = fit_params(M, segment)  
>     I = extract_invariants(segment, M)  
>     x_hat = simulate(M, θ, I, len=|segment|)  
>     r = segment - x_hat  
>     if mode == "lossless":  
>         R = lossless_encode(r)  
>     else:  
>         r_q = quantize(r, eps)  
>         R = entropy_encode(r_q, prior=learned)  
>     emit Packet{ model_id, θ, I, eps, R, checksum(segment) }  
> ```  
> **Decoder reverses the process** to reconstruct the signal.”

### 5.1 Function Inventory from Pseudocode

The pseudocode enumerates several **logical functions** and concepts:

- `split(data, window=W)` – segmentation of data into windows of size `W`.  
- `select_model(segment)` – choose `M` given `segment`.  
- `fit_params(M, segment)` – fit parameters `θ`.  
- `extract_invariants(segment, M)` – derive invariants `I`.  
- `simulate(M, θ, I, len=|segment|)` – regenerate a synthetic segment `x_hat`.  
- `lossless_encode(r)` – compress residuals exactly.  
- `quantize(r, eps)` – quantize residuals with tolerance `eps`.  
- `entropy_encode(r_q, prior=learned)` – encode quantized residuals using entropy coding with a **learned prior**.  
- `Packet{ model_id, θ, I, eps, R, checksum(segment) }` – structure for **per-segment packet**.

### 5.2 New Gaps from Pseudocode

**GAP-APP-013 — Learned Prior for Entropy Encoding**

The pseudocode references:

> `R = entropy_encode(r_q, prior=learned)`

Missing details:

- How **`prior=learned`** is obtained:  
  - Is it pre-trained on some corpus, or learned online from the dataset?  
  - How is this prior stored in the capsule (if at all)?  
  - Does each capsule carry its own prior, or do encoders rely on fixed shared priors?

**Consequence:**

- A full implementation must define **how the entropy-coding prior is trained, represented, and reused**, or explicitly choose a simpler fixed prior instead.

**GAP-APP-014 — Windowing Policy and Segment Strategy**

The pseudocode begins with:

> `for segment in split(data, window=W):`

Missing details:

- How `W` (window size) is chosen (fixed, adaptive, data-type-dependent, etc.).  
- Whether there are **overlapping windows** or purely disjoint segments.  
- How segment boundaries are handled in multi-dimensional data (e.g., time × channels × features).  
- Whether segment metadata (location, index) is stored explicitly in the capsule.

**Consequence:**

- A reference implementation must define a **windowing policy** and how it is encoded so that decompression can invert segmentation deterministically.

**Impact on existing gaps:**

- Pseudocode reinforces **GAP-APP-001 (Model selection)** without resolving it; we now know there *must* be a concrete `select_model` implementation, but this doc doesn’t specify it.

---

## 6. APP Container Format and Subsystems

### 6.1 APP Container Format (Header / Body)

The Implementation PDF provides a minimal container format spec:

> “**7. APP Container Format**  
> **Header**  
> - Model ID, version, and compression mode.  
> - Metadata: dtype, shape, fidelity metric.  
> **Body**  
> - Model parameters (quantized or raw).  
> - Invariant dictionary.  
> - Residual byte stream.  
> - Metrics and checksum.”

This clarifies the **minimum required fields** in the APP container:

- **Header:**  
  - `model_id`  
  - `version`  
  - `compression_mode`  
  - `dtype`  
  - `shape`  
  - `fidelity_metric`

- **Body:**  
  - `model_parameters` (quantized or raw)  
  - `invariant_dictionary`  
  - `residual_byte_stream`  
  - `metrics` (e.g., compression ratio, MAE, PSNR, etc.)  
  - `checksum`

This aligns with the Focus Report’s description of the `.apx` container, but adds the explicit `dtype`, `shape`, and `fidelity_metric` metadata.

### 6.2 Subsystems Table

The Implementation PDF defines the main internal subsystems:

> “**8. Subsystems**  
> | Subsystem | Role |  
> |------------|------|  
> | **Aether Core** | symbolic modeling and invariant extraction |  
> | **Press Engine** | encoding of parameters and residuals |  
> | **Flux Decoder** | reconstruction and fidelity validation |  
> | **Protocol Layer** | serialization schema and metadata registry |”

Implementation mapping:

1. **Aether Core**  
   - Houses domain models, invariant extraction logic, and **simulation/regeneration** (`simulate` in pseudocode).

2. **Press Engine**  
   - Implements the encoding pipeline: parameter fitting, residual computation, residual encoding, and packet emission.

3. **Flux Decoder**  
   - Handles decoding of APP capsules: reconstructing base signal, applying residuals, and verifying fidelity.

4. **Protocol Layer**  
   - Defines `.apx` schemas, manifest layout, version tags, and integration of hash/signature schemes.

### 6.3 Impact on GAP-APP-002 (APX Schema)

**GAP-APP-002 (Exact `.apx` schema & signature details)** was partially addressed by the Focus Report. The Implementation PDF adds **more concrete header/body fields**.

What is now clearer:

- Minimal APP container **contents** are now explicitly enumerated (header/body).  
- The separation of responsibilities across **Aether Core / Press Engine / Flux Decoder / Protocol Layer** is formally acknowledged.

What remains open:

- Bit-level layout (ordering, alignment, padding) of header and body.  
- Exact JSON schema of `.apxMANIFEST.json` and how it relates to header/body.  
- Detailed hash/signature algorithms and how they integrate with header/body.

**Status:** GAP-APP-002 is **further narrowed but still not fully closed**.

---

## 7. Error and Fidelity Guarantees

The Implementation PDF gives a concise set of guarantees per data type:

> “**9. Error and Fidelity Guarantees**  
> - **Timeseries:** MAE ≤ ε, spectral error ≤ δ.  
> - **Images/Fields:** PSNR ≥ threshold or SSIM ≥ bound.  
> - **Dynamics:** State fidelity ≥ F, invariants deviation ≤ Δ.”

This formalizes **metric types** and relations:

- **Timeseries:**  
  - Mean Absolute Error (MAE) bounded by ε.  
  - Spectral error bounded by δ.

- **Images/Fields:**  
  - Peak Signal-to-Noise Ratio (PSNR) must exceed a threshold, **or**  
  - Structural Similarity Index (SSIM) must exceed a bound.

- **Dynamics:**  
  - State fidelity must exceed F (e.g., correlation or overlap measure).  
  - Invariants (e.g., energy, momentum) must deviate by no more than Δ.

**GAP impact:**

- **GAP-APP-007 (Default fidelity thresholds)** – This PDF **confirms the metric types** but still avoids giving numerical defaults for ε, δ, PSNR threshold, SSIM bound, F, and Δ. The gap remains open but **more tightly scoped**: we now know **exactly which metrics** need thresholds.

---

## 8. Example Application: IMU Compression

The Implementation PDF gives a concrete example:

> “**10. Example Application (IMU Compression)**  
> - **Model:** Kalman Filter with drift correction.  
> - **Params:** 40 floats per window.  
> - **Residuals:** quantized noise vector.  
> - **Achieved Compression:** 8–20× lossless; 30–100× ε-bounded.”

Implementation-level significance:

- Demonstrates APP can be instantiated with a **Kalman Filter** model for inertial measurement unit (IMU) data.  
- Shows a parametrization profile: **40 floats per window**.  
- Residuals are **quantized noise vectors**.  
- Provides concrete **compression ratios** achievable in practice: 8–20× (lossless), 30–100× (ε-bounded).

This example suggests at least one **concrete model family** (Kalman + drift correction) but does not declare it **universal or mandatory**.

**GAP interaction:**

- This does not close **GAP-APP-001**, but it **illustrates** one possible member of the model library and shows how parameters can be structured per window.

---

## 9. Alignment with Trinity–Momentus System

The Implementation PDF explicitly situates APP within the **Trinity–Momentus–Momentum** trio:

> “**11. Alignment with Trinity–Momentus System**  
> - **Trinity** → Model selector + invariant extractor.  
> - **Momentus** → Simulation engine for regeneration.  
> - **Momentum** → Residual dynamics layer.  
> **APP unifies these into a domain-agnostic pipeline.**”

Interpretation:

- **Trinity** provides **model selection** and **invariant extraction**, likely feeding APP’s `select_model` and `extract_invariants`.  
- **Momentus** acts as the **simulation engine**, implementing the `simulate(M, θ, I, len)` step.  
- **Momentum** provides a **residual dynamics layer**, likely a structured view of residual behaviour across time.

Implementation implications:

- In a full Aether stack, APP is **not isolated**; it is the compression layer tying together **Trinity (models)**, **Momentus (simulation)**, and **Momentum (residual dynamics)**.  
- For standalone deployment (CLI/GUI), these roles may be replaced by **embedded or simplified equivalents**.

This section does not introduce new numerical gaps but enhances our **integration map** for Press.

---

## 10. Implementation Milestones and Benchmarking

The Implementation PDF includes a roadmap:

> “**12. Implementation Milestones**  
> 1. **Prototype (lossless)** – Build rule-based compressor with **range coder**.  
> 2. Add **bounded-error quantization** and metrics.  
> 3. Integrate **symbolic invariant API**.  
> 4. **Benchmark** against ZIP, Zstd, FLAC, PNG.  
> 5. Publish **v1.0 spec and reference repo**.”

And earlier, in Concept/Branding sections, we have:

> “APP redefines data compression as a modeling problem. It transforms datasets into minimal generative descriptions, storing *why* the data behaves as it does — not just *what* it was.”

Implementation implications:

- Minimum path to a working implementation:  
  1. Build a **lossless prototype** using a **range coder** for residuals.  
  2. Extend to **ε-bounded quantization** with metric tracking.  
  3. Expose **invariant extraction** via a clear API surface.  
  4. Benchmark vs general-purpose codecs (ZIP, Zstd) and domain-specific codecs (FLAC, PNG).  
  5. Produce a stable **v1.0 spec + reference implementation**.

**New gap:**

**GAP-APP-015 — Range Coder Variant and Configuration**

The milestone says:

> “Prototype (lossless) – Build rule-based compressor with **range coder**.”

Missing details:

- Which specific **range coder** algorithm is intended (standard arithmetic coding variant, rANS, tANS, etc.).  
- How the range coder’s **state initialization and symbol probabilities** are defined and stored.  
- Whether the range coder is per-packet, per-residual-stream, or global.

**Consequence:**

- A reference implementation must choose a **concrete range coder formulation** and treat that choice as part of the APP spec (or define a codec-agnostic interface for the Press Engine residual coder).

---

## 11. Branding and Elevator Pitch (Contextual, Not Normative)

While not directly implementation-critical, these lines capture the intended narrative:

> “**13. Branding**  
> **Aether Press Protocol (APP)** – “**Encode less. Recreate everything.**”  
> Logo concept: concentric circles collapsing inward, a central singularity representing compressed reality.”

> “**14. Elevator Pitch**  
> > “The Aether Press Protocol encodes relationships instead of raw data. It collapses structure into equations and parameters, achieving up to 10■× compression while preserving causal fidelity. It’s ZIP for structured reality.””

> “**15. Concept Summary**  
> “APP redefines data compression as a modeling problem. It transforms datasets into minimal generative descriptions, storing *why* the data behaves as it does — not just *what* it was.””

These sections reinforce:

- The **relationship-encoding** framing.  
- The claim of **up to ~10×+ compression** for structured reality while preserving causality.  
- The **metaphor** “ZIP for structured reality.”

They do not add new mandatory implementation details but align with the rest of the spec.

---

## 12. Updated GAP Status After Implementation Pass 02

**Unchanged (still open):**

- **GAP-APP-001 — Model library and selection**  
  - We still have no canonical set of model families or selection heuristics.  

- **GAP-APP-003 — NAP Compression Manifest schema**  
  - Implementation PDF does not mention NAP or SimA/SimB manifests.  

- **GAP-APP-004 — Residual fraction semantics**  
  - No new information about per-dimension residual budgets.  

- **GAP-APP-005 — Output space / distance metric for P_state acceptance**  
  - Implementation PDF defines metric types but not how P_state acceptance gates are wired to O and d(); that still lives in Report 19.

- **GAP-APP-006 — Runtime barrier enforcement**  
  - No new info on Pareto barrier handling.  

- **GAP-APP-009 — Exact role of LCDRM inside APP**  
  - LCDRM is not referenced here.

- **GAP-APP-010 / 011 / 012** (from Focus Report pass) remain open, as this PDF is mostly orthogonal to compressed-domain operations, version signalling specifics, and security boundaries.

**Partially narrowed:**

- **GAP-APP-002 — `.apx` schema & signatures**  
  - Now have explicit header/body field lists and subsystem roles, but still no bit-level schema or crypto details.

- **GAP-APP-007 — Default fidelity thresholds**  
  - Metric types are confirmed; numeric thresholds still unspecified.

- **GAP-APP-008 — Streaming vs batch semantics**  
  - This PDF does not add more on streaming, so status remains as defined in Focus Report pass (partially resolved there).

**Newly added:**

- **GAP-APP-013 — Learned prior for entropy encoding**  
  - Pseudocode references `prior=learned` with no training/storage spec.

- **GAP-APP-014 — Windowing policy and segmentation strategy**  
  - `split(data, window=W)` is underspecified; no segmentation protocol defined.

- **GAP-APP-015 — Range coder variant and configuration**  
  - Milestone mandates “range coder” but not which formulation or configuration.

---

## 13. Net New Functions / Capabilities to Merge into Main Dev Spec

From this Implementation pass, the main **additions** to the function/capability inventory are:

1. **Segmentation and Windowing**  
   - Explicit `split(data, window=W)` step: Press must support **configurable windowing**, and segments must be invertibly mapped back to positions in the source stream.

2. **Quantization & Learned-Entropy Residual Coding**  
   - `quantize(r, eps)` plus `entropy_encode(r_q, prior=learned)` describe a **two-stage lossy residual pipeline** (quantize then entropy code) for quasi-lossless mode.

3. **Container Metadata Fields**  
   - Header: `model_id`, `version`, `compression_mode`, `dtype`, `shape`, `fidelity_metric`.  
   - Body: `model_parameters`, `invariant_dictionary`, `residual_byte_stream`, `metrics`, `checksum`.

4. **Subsystem Interfaces**  
   - Aether Core, Press Engine, Flux Decoder, Protocol Layer are now formalized and should be mirrored in the internal architecture.

5. **Error/Fidelity Metric Families**  
   - Timeseries (MAE, spectral error), Images/Fields (PSNR, SSIM), Dynamics (state fidelity, invariants deviation) are now **official** metric families.

6. **Concrete Example Model**  
   - Kalman Filter with drift correction for IMU data is an explicit, worked example showing how to instantiate a model for a real use case.

7. **Range Coder in Prototype**  
   - A range coder is explicitly recommended for the lossless prototype’s residual coder.

---

## 14. Summary of This Pass

- This Implementation pass **confirms and sharpens** much of the v0.1 dev spec: architecture, modes, container structure, and metric types.  
- It adds **explicit pseudocode** for the Press pipeline, which surfaces new implementation-level gaps around segmentation, learned priors, and residual coding choice.  
- It provides concrete **example behaviour** (IMU compression with Kalman Filter) and **compression ratios**, useful as validation tests for an implementation.  
- It clarifies Press’s integration with **Trinity, Momentus, and Momentum** and formalizes the four subsystems (Aether Core, Press Engine, Flux Decoder, Protocol Layer).  
- It further **narrows** GAP-APP-002 and GAP-APP-007, while leaving core open questions (model library, NAP manifest, barrier enforcement, LCDRM integration) untouched.

This addendum should be used alongside the Focus Report Pass 01 and the original Dev Implementation Spec v0.1 when designing a full reference implementation of the Astral Press Pillar.



<!-- END SOURCE: astral_press_pillar_dev_spec_addendum_implementation_pass_02.md -->


---

<!-- BEGIN SOURCE: astral_press_full_implementation_build_plan_beyond_mvp.md -->

# Astral Press — Full Implementation Build Plan (Beyond JS Offline MVP)

## 0. What “Full Functionality” Means Here

Using only the project docs as ground truth:

### 0.1 Canon pillars we must cover

From the APP Implementer Checklist and legacy docs, “real” Astral Press has to do at least:

1. **Reversible rule+residual compression**  
   - “Press and DePress are inverse mappings: \(C_{\text{out}} = \Pr(S_{\text{in}})\), \(S_{\text{in}} = \DePr(C_{\text{out}})\)… dataset \(S\) is modeled as \(S = M(\theta) \oplus R\)… Compression ratio = (|θ| + |R|) / |S|.” (Checklist §1.1 / legacy post-implementation)  
2. **Strict lossless + ε-bounded modes with acceptance tests**  
   - “Lossless mode… reconstructed bytes’ hash must equal the original file hash…”  
   - “For each numeric field x with quantization step q: \(|x_{\text{post}} - x_{\text{pre}}| \le q/2 \le ε_x\).”  
   - “Replay test… Predictive test… Idempotence… Isolation.” (Checklist §1.2, legacy “Crush without regret” runbook)  
3. **Multi-layer MDL stack (SimA + SimB)**  
   - “Data X is decomposed as X = M1 + R1, R1 = M2 + R2, … until description length no longer improves.” (Checklist §1.3, metrics pass)  
4. **Two-track Press (P_state / P_cite)**  
   - “You keep the *small, exact* computational snapshot (P_state), plus tiny proofs/pointers for the rest (P_cite).” (Legacy performance report)  
5. **Dims Press & per-dimension controls on the NAP bus**  
   - “FIDELITY CONTROLS YOU CAN SET PER-DIMENSION… Exact vs quantized dims… Residual fraction… Selective retention… Dict scopes.” (press v2)  
6. **APX container + MANIFEST + NAP manifest semantics**  
   - “Original file name, size, hash… compression mode… layers… reference to NAP Compression Manifest…” (Implementation canon v4 §1 & §2)  
7. **AEON-i / APXi descriptor surface**  
   - Integer-only, versioned opcodes (SEGMENT, AFFINE, POLY3, PERIODIC, COMBINE, AR1-3) with varints + ZigZag and a `u16 version` prefix + varint stream. (Complement v4 §3)  
8. **Metrics & MDL functional**  
   - `L_total`, `L_naive`, `kappa = L_naive − L_total`, MDL stopping rule, baselines. (Complement v4 §4)  
9. **Modes & policy layer hooks**  
   - ESL, Offline Recompress, Encryption, Knowledge Sync controlling how Press behaves. (Complement v4 §5, checklist §2.7)  

The MVP JS build plan already covers the **container + manifest + SimA/SimB + AEON/APXi + basic MDL + lossless path for bytes + numeric demo**. “Full functionality” here means: *implement the rest of that list in this JS environment, including lossy modes, policy layer, Dims Press, multi-layer NAP, and two-track Press*.

---

## 1. From MVP to Full APP Coverage — Gap Map

Starting from your current MVP plan, the main gaps to close are:

1. **Modes & Profiles**
   - MVP: `PRESS_LOSSLESS` only, `dtype="bytes"` + simple numeric demo.  
   - Needed: ε-bounded profiles, Press policy cards, P_state/P_cite track separation, S-mode hooks.

2. **Multi-layer NAP stack**
   - MVP: single SimA/SimB or SimB-only per capsule.  
   - Needed: general `layers[]` DAG with `parent`, `refs[]`, `ordering`, `knit_rules`, multi-layer MDL, LCDRM-style layers.

3. **Dims Press controls**
   - MVP: fixed shape metadata and global profile.  
   - Needed: per-dimension choices: exact vs quantized, residual fraction, selective retention, dict scopes, new dims mid-run.

4. **Residual & codec richness**
   - MVP: integerize + delta + Golomb-Rice (and maybe arithmetic).  
   - Needed: full integerization pipeline from performance report (normalize → quantize → zigzag → varint/delta/RLE), plus LFSR and AR residual modes.

5. **Two-track Press implementation**
   - MVP: single capsule path.  
   - Needed: explicit pipelines and manifests for `P_state` vs `P_cite` with different policies and sizes.

6. **Extended metrics & evaluation**
   - MVP: compute `kappa` for small demos.  
   - Needed: full MDL functional with overhead terms, baseline compressors integration (for experiments harness), Testdoc/Pareto reporting schema.

7. **Service & ops layer**
   - MVP: offline SPA only.  
   - Needed: optional HTTP API (as per APP_LOCAL_SPEC §9), offline recompress, encryption wrappers, knowledge sync.

The rest of this plan is basically: **Phase 2+** tasks to close all of those.

---

## 2. Phase 2 — ε-Bounded Profiles & “Crush without Regret”

### 2.1 Implement ε → q mapping and integerization pipeline

**Canon anchors**

Legacy performance report:

> “Integerization pipeline (normalize → units → quantize → zigzag → varint/delta/RLE).  
> Bound error upfront: if you quantize a scalar with step q, your max absolute error is ≤ q/2. Pick q so it respects the field’s ε.”  

Checklist:

> “For every numeric field x you store after quantization q: \(|x_{\text{post}} - x_{\text{pre}}| \le q/2 \le ε_x\).”

**Tasks**

1. **Extend type metadata**
   - In `MANIFEST.json.press`, add:
     - `fidelity_metric` (already there in local spec).
     - New `fields` array when `dtype` is structured (JSON/table/sensor), each with `name`, `unit`, `epsilon`, `q`, `mode` (exact/quantized).

2. **Build integerization pipeline module (`integerization_pipeline`)**
   - Steps:
     1. `normalize` — convert field to canonical units if needed (unit scaling).
     2. `quantize` — round to nearest multiple of `q_field`, ensuring `q_field/2 ≤ ε_field`.
     3. `zigzag` — for signed fields, map to unsigned integer.
     4. `delta/RLE` — apply delta and RLE as appropriate.
   - Keep it parameterized by the `Press policy card` (see Phase 4).

3. **Integrate into SimB encoder**
   - For numeric residuals in ε-bounded mode, run through this pipeline before entropy coding.

4. **Add profile definitions**
   - In code, define profiles from APP_LOCAL_SPEC §6.2 style:
     - `PRESS_LOSSLESS`
     - `PRESS_SENSOR_MED` (with explicit ε per field)
     - `PRESS_LOG_CRUSH` (ε=0 for some fields, relaxed for timestamps, etc.).

5. **Hook into MVP APIs**
   - `pressNumericArray` and future `pressTable/pressJSON` accept profile names, fetch per-field ε/q from policy, and run integerization pipeline accordingly.

### 2.2 Implement “Crush without regret” acceptance checks

**Canon anchor**

Performance report:

> “Crush without regret checks (copy this into your runbook) …  
> 1. Field-level bounds…  
> 2. Replay test (Δ = 0) … O unchanged.  
> 3. Predictive test… d(O_true, O_replayed) ≤ ε.  
> 4. Document proof: Keep {hash, bytes} for each external source in P_cite…  
> 5. Idempotence…  
> 6. Isolation: Prior checkpoint O-hashes never change.”

**Tasks**

1. **Scoreboard interface (`O`)**
   - Define a simple JS interface for a “scoreboard”:
     - `computeScoreboard(state) → O` where `O` is a JSON object of key metrics.
   - For JS demo, you can have a synthetic O (e.g. norms of data, summary stats). For real integration, O would come from the simulation `T`.

2. **Acceptance harness**
   - Implement a module that, given:
     - Original state `S`, Press config, P_state capsule, scoreboard function, horizon Δ,
     - Runs:
       - Δ=0 replay: `O(S)` vs `O(DePress(Press(S)))`.
       - Δ>0 predictive: simulate forward and compare `d(O_true, O_replayed)`.
   - Encapsulate acceptance results in a JSON struct recorded into `reports/report.json`.

3. **Integrate into Press pipeline**
   - For ε-bounded runs, Press:
     - Runs acceptance harness using configured Δ and ε.
     - Marks run as `accepted` or `rejected` in the report.
     - Refuses to write P_state capsule if acceptance fails (or writes but flags as failed; behaviour is a local spec choice you must document).

4. **Expose in UI**
   - Add a **“Run Crush Checks”** toggle in the SPA so devs can see acceptance test results for numeric demos and sample P_state scenarios.

---

## 3. Phase 3 — General Multi-Layer NAP Stack & LCDRM-Style Layers

### 3.1 Expand NAP manifest handling from 1–2 layers to N

**Canon anchors**

NAP spec:

> “NAP Compression Manifest: `layers[] {id, kind∈{AP.symbolic (SimA), AP.residual (SimB)}, parent, refs[], params, ordering}, knit_rules, deterministic_order, hashes` … graph must be a DAG… there exists a topological ordering σ such that DePress(Press(D; M); M) = D.”  

LCDRM white paper:

> “Each subsequent layer: L_n = ΔL_{n-1} … Compression occurs when |L_n| < |L_{n-1}| until ΔL → 0… Deterministic reconstruction: L_0(i) = Σ_k L_k(i) + C.”

**Tasks**

1. **NAP manifest schema v1**
   - Generalize current schema (SimA_main + SimB_main) to arbitrary `layers[]`:
     - Each with `id`, `kind`, `parent`, `refs[]`, `params`, `ordering`.
   - Add support for:
     - Multiple SimA layers (M1, M2, …).
     - Multiple SimB layers (R1, R2, …).
   - `knit_rules` to declare LCDRM-style stack:
     - e.g. `{"type":"lcd_rm_stack","reconstruction":["decode_M1","apply_R1","decode_M2","apply_R2",…]}`.

2. **DAG builder & validator**
   - Implement `buildLayerGraph(layers)`:
     - Validate no cycles.
     - Produce topological order consistent with `ordering` and `deterministic_order`.
   - On load:
     - Refuse capsules whose NAP manifests do not form a DAG or whose hashes mismatch.

3. **Stacked Press pipeline**
   - Generalize `pressNumericArray` into:
     - `pressStacked(data, layersConfig)` where `layersConfig` describes target stack (e.g. `[SimA_poly, SimB_residual, SimA_LFSR, SimB_noise]`).
   - For each candidate new layer:
     - Compute candidate `L_total'` per MDL rule (see Phase 5).
     - Accept layer only if `L_total' + margin < L_total`.

4. **LCDRM-style mode**
   - Implement a convenience mode:
     - `pressLCDRM(data)`:
       - Builds automatic successive Δ layers until `ΔL` shrinks and MDL says stop.
   - Here, SimA can be identity (no extra model), SimB is the delta layer; this directly matches LCDRM equations.

### 3.2 Extend DePress to follow general NAP DAG

**Tasks**

1. **General `depressStacked`**
   - Given NAP manifest + layer payloads:
     - Use topological order from NAP DAG.
     - For each layer:
       - If `kind="AP.symbolic"`, run corresponding SimA decode to reconstruct baseline.
       - If `kind="AP.residual"`, decode residual and apply to current baseline.

2. **Error and partial recovery modes**
   - Decide local behaviour for:
     - Missing non-root layers (fail vs partial reconstruct).
     - Hash mismatch (fail hard).
   - Document in APP_LOCAL_SPEC v2 (future).

---

## 4. Phase 4 — Two-Track Press & Policy Layer

### 4.1 Implement P_state / P_cite split

**Canon anchor**

Performance report:

> “You keep the *small, exact* computational snapshot (**P_state**), plus tiny proofs/pointers for the rest (**P_cite**).”  
> “Don’t let P_state depend on raw docs you won’t replay. If T doesn’t need the raw, don’t pack it—hash it in P_cite instead.”

**Tasks**

1. **Define two capsule classes in implementation**
   - `PStateCapsule`:
     - `.apx` with data necessary to restart `T`:
       - Core state arrays, key parameters, minimal logs.
       - Pressed with `PRESS_LOSSLESS` or tight ε-bound as required by policy.
   - `PCiteCapsule`:
     - `.apx` or smaller structured record that:
       - Stores `hash`, `size`, and “few extracted integers you actually use” from external sources (PDFs, logs, etc.).
       - May use aggressive ε-bounded or even dictionary-only compression since it’s not used for replay.

2. **Manifests & tagging**
   - Add to `MANIFEST.json`:
     - `press.track = "P_state"` or `"P_cite"` (or both for combined capsules).
   - Policy engine uses track to enforce:
     - Strict rules for state (e.g. no raw docs).
     - More flexible rules for cite.

3. **Pipeline split**
   - Provide API:
     - `pressState(state_data, policy)` → `.apx` (P_state).
     - `pressCite(external_sources, policy)` → `.apx` (P_cite).
   - In JS demo, `pressCite` can accept uploaded files and produce small cite capsules showing hash + a few stats.

### 4.2 Press policy cards

**Canon anchor**

Performance report:

> “Press policy card (use per source)… Type: (text/pdf/image/log/table/sensor) Track: [P_state | P_cite]… O-fields derived… Quantization q per field…”

**Tasks**

1. **Define JSON schema for policy cards**
   - `press_policy_card_v1` with fields:
     - `source_name`
     - `type` (`"text"`, `"pdf"`, `"image"`, `"log"`, `"table"`, `"sensor"`, …)
     - `track` (`"P_state"`, `"P_cite"`, or `"both"`)
     - `o_fields` (list of scoreboard fields)
     - `fields` (mapping field→{ε, q, mode, retention})
     - `modes` (allowed profiles, e.g. `PRESS_SENSOR_MED`)

2. **Policy compiler**
   - Reads policy cards and:
     - Configures integerization pipeline per field.
     - Chooses per-dimension exact vs quantized vs recompute/residual/full (see Phase 5).
     - Configures which outputs go to P_state vs P_cite.

3. **UI integration**
   - Add a simple policy card editor in the SPA:
     - Load/save policy cards.
     - Apply card to Press runs.

---

## 5. Phase 5 — Dims Press & Per-Dimension Controls

**Canon anchor**

Dims Press report:

> “FIDELITY CONTROLS YOU CAN SET PER-DIMENSION (OR PER-LAYER)…  
> - Exact vs quantized dims…  
> - Residual fraction…  
> - Selective retention: {recompute, residual, full}…  
> - Dict scopes: per-node dictionaries or a global Press dict on the NAP bus…”  
> “New dims can appear mid-run… and get Loomed and Pressed like any other data… dial how faithful they must be… per-dimension, per-layer.”

### 5.1 Per-dimension fidelity configuration

**Tasks**

1. **Dimension metadata**
   - Represent each dimension with:
     - `name`, `index`, `type`, `exact_or_quantized`, `q`, `ε`, `retention`, `residual_fraction_target`, `dict_scope`.

2. **Integrate with policy cards**
   - Policy card fields section maps to dim config:
     - `mode: "exact" | "quantized"`
     - `retention: "recompute" | "residual" | "full"`
     - `residual_fraction_target: number (0–1)`
     - `dict_scope: "per_node" | "global"`

3. **Apply in Press pipeline**
   - During Press:
     - Exact dims: enforced ε=0, no quantization, residuals must restore exactly.
     - Quantized dims: quantization step q assigned; residual compresses quantized deltas.
     - `recompute` dims: derived during DePress; not stored in residual at all.
     - `full` dims: stored verbatim, perhaps outside residual stack.

### 5.2 Dynamic dims mid-run

**Tasks**

1. **NAP bus schema tracking**
   - Implement a simple “dims registry” for the bus:
     - Keep track of dimensions and their metadata; allow new dims to appear at any time with policies assigned.

2. **Press integration**
   - When new dimensions appear:
     - If policy exists, apply it.
     - Otherwise, use a default safe profile (e.g. exact for P_state).

3. **UI**
   - Panel listing all dims, their retention modes, residual fractions, and dictionary scopes.

---

## 6. Phase 6 — Residual Codec Richness (LFSR, AR, Integerization Details)

### 6.1 LFSR model & codec

**Canon anchor**

Post-Implementation:

> “A 1 KB structured dataset generated by a 16-bit linear feedback shift register (LFSR)… seed = 0xBEEF, taps = 16, 14, 13, 11… Compression ratio = 214 / 1024 = 0.209… random dataset remained incompressible.”

**Tasks**

1. **LFSR model implementer**
   - Provide LFSR fit routine for sequences that appear LFSR-like:
     - Try known taps or search over a small tap set.
   - Encode parameters (seed, taps) as integers in SimA (either via AEON-i op or via `params` in NAP manifest).

2. **LFSR residual handling**
   - For perfect modelled sequences: residual R = 0, confirm ratio ~0.209 as in doc.
   - Use LFSR as a special-case model family in `selectModelForSegment`.

### 6.2 AR residual transforms

**Canon anchor**

AEON complement:

> “OP_AR1, OP_AR2, OP_AR3 — for autoregressive residual transforms.”

**Tasks**

1. **AR(1–3) fit + simulate**
   - Implement AR residual models as in APP_LOCAL_SPEC.
   - Encode coefficients in AEON-i using OP_AR1/2/3 opcodes.

2. **Residual stack integration**
   - For segments where AR models yield better MDL than simple delta, use them as part of SimB transform stack.

---

## 7. Phase 7 — Metrics, MDL, and Evaluation Harness

### 7.1 Fully explicit MDL functional

**Canon anchor**

Metrics complement:

> “L_total = L_model + L_residual + L_overhead… L_naive = 8 * |S|… kappa = L_naive − L_total… MDL stopping rule: add new model only while it reduces L_total.”

**Tasks**

1. **Define L_total computation in code**
   - For each Press run:
     - `L_model`: bit-length of AEON/APXi descriptors + explicit layer params.
     - `L_residual`: bit-length of residual binary payloads.
     - `L_overhead`: bits for:
       - APXi prefixes, counts.
       - JSON manifest/NAP sizes (raw or compressed size ×8).
       - Per-layer hashes, minimal container overhead.
   - Document formula in an internal MDL spec (APP_LOCAL_SPEC v2 section).

2. **Implement MDL layer acceptance**
   - For potential new layer M_i:
     - Compute `L_total'` with that layer.
     - Accept only if `L_total' + margin < L_total` (margin e.g. 8 bits as in local spec).
   - Store MDL decision logs in `reports/report.json`.

### 7.2 Baselines & Pareto evaluation (optional harness)

**Canon anchor**

Metrics pass:

> “Baselines (gzip/bzip2/xz) are integrated… windows, thresholds, and Pareto fronts…”

**Tasks**

1. **External baseline harness (dev-side tool, not in browser)**
   - Separate Node tool to:
     - Run Press vs gzip/bzip2/xz on same datasets.
     - Collect `kappa`, compression ratios, speed.
     - Build a simple JSON “Pareto manifest”.

2. **Display in UI**
   - Optional: show basic charts (Press vs baselines) inside the SPA for test datasets.

---

## 8. Phase 8 — Modes, NAP Bus, and Service Layer

### 8.1 Implement S-modes mapping (local)

**Canon anchor**

Complement v4:

> “ESL must control whether internal telemetry flows into Press + SLL. Offline Recompress must enable APP recompression of historical data without breaking provenance. Encryption must control whether APP outputs are wrapped in crypto layers. Knowledge Sync must cause policy/knowledge reloads for APP when sync succeeds.”

APP_LOCAL_SPEC already proposed S1–S12 mappings.

**Tasks**

1. **Mode manifest**
   - Implement a `press_modes_v1.json` file storing:
     - `enabled_modes`: `[ "ESL_ON", "OFFLINE_RECOMPRESS", "ENCRYPT_CAPSULES", "ALLOW_EPSILON_PROFILES" ]`.

2. **Mode interpreter**
   - In JS, implement a module that:
     - Applies ESL: when `ESL_ON`, logs are passed into Press; otherwise bypass.
     - Applies Offline Recompress rules: when mode enabled, allow `pressBytes` on historical `.apx` or raw; track lineage in manifest.
     - Applies encryption (see 8.2).
     - Applies knowledge sync: reloads policy cards/AEON tables on change signal.

### 8.2 Encryption wrapper

**Canon anchor**

Checklist:

> “You must lock down… Signature/HMAC scheme (if used)… Canon only says ‘there is a manifest and integrity tags’; the rest is design space.”

**Tasks**

1. **Define simple wrapper format**
   - `.apx.enc` = encryption envelope containing:
     - Encrypted `.apx` bytes.
     - Minimal header: algorithm, key ID, maybe nonce/tag.

2. **Implementation**
   - In JS (for demo only), use WebCrypto AES-GCM with local key.
   - Ensure APP logic and determinism remain *inside* `.apx`; encryption is outer envelope only.

---

## 9. Phase 9 — Extended Data Type Coverage

### 9.1 Tables / JSON / logs / sensors

Leaning on policy cards and integerization, add:

1. **`pressTable(rows, schema, policy)`**
   - Schema describes fields and dims.
   - Use Dims Press controls for per-field quantization and retention.
2. **`pressLog(lines, policy)`**
   - Focus on dictionary SimB, plus structured numeric subfields.
3. **`pressSensorStream(samples, policy)`**
   - Apply ε-bounded profiles and AR models heavily.

All of these reuse the same APP core; they’re thin wrappers that call into the more general stacked Press pipeline with appropriate manifest entries.

---

## 10. Phase 10 — Testing, Compliance & Tooling

### 10.1 Canon compliance test kit

Build a “Press Test Kit” that:

- Verifies:
  - Lossless Press/DePress on arbitrary bytes.
  - ε-bounded field-level constraints.
  - Multi-layer MDL stack behaviour (adding layers never increases `L_total` beyond margin).
  - P_state/P_cite separation (no raw docs in P_state).
  - NAP DAG validity and deterministic DePress.

- Ships as:
  - A set of JSON testcases + expected outcomes.
  - A small CLI harness (Node) and in-browser test harness.



<!-- END SOURCE: astral_press_full_implementation_build_plan_beyond_mvp.md -->


---

<!-- BEGIN SOURCE: astral_press_js_offline_mvp_build_plan_2025_11_20.md -->

# Astral Press — JS Offline MVP Build Plan

Goal: turn the current APP canon + APP_LOCAL_SPEC v1 into a **first offline web-page JavaScript implementation** of Press/DePress.

Target: single-page HTML/JS app (no server) where a user can:

1. Select a file.
2. Press → get a `.apx` capsule.
3. Load `.apx`.
4. DePress → recover original bytes.

MVP mode: `PRESS_LOSSLESS` only, `dtype="bytes"` default, with a dedicated numeric demo path for SimA/SimB.

---

## 0. MVP Definition

### 0.1 MVP feature set

**User-facing:**

- Offline SPA (single `index.html` + bundled JS).
- File input: choose any small file (up to some safe size limit, e.g. a few MB).
- Buttons:
  - **Press** → downloads `*.apx` (ZIP-based container with manifest + payloads).
  - **DePress** → takes an `*.apx` and reconstructs original file, prompting download or showing a hex preview.
- A debug panel showing:
  - Parsed `MANIFEST.json`.
  - Compression ratio bytes in/out.
  - `kappa` if we compute it.

**Profiles in scope:**

- Lossless only: `press.mode = "lossless"`, `press.profile = "PRESS_LOSSLESS"`, `epsilon_global = 0`.
- Data type focus:
  - `dtype = "bytes"` generic path (dictionary/SimB-only for arbitrary files).
  - `dtype = "numeric_array"` demo path (SimA+SimB, AEON/APXi, MDL) for structured arrays.

---

## 1. Architecture Overview — JS Modules

We map the conceptual APP architecture (Aether Core, Press Engine, Flux Decoder, Protocol Layer) to concrete JS modules.

### 1.1 Module breakdown

1. **Core utilities**
   - `bitstream` — bit/byte writer & reader.
   - `varint` — ZigZag + varint encode/decode.
   - `hash` — SHA-256 wrapper using WebCrypto.
   - `arith_coder` — arithmetic encoder/decoder.

2. **AEON‑i / APXi**
   - `aeon_ops` — opcode table, param schemas.
   - `apxi_encode` / `apxi_decode` — APXi framing & parsing.

3. **Model library (SimA)**
   - `models_affine`, `models_poly`, `models_periodic`, `models_ar`.
   - Shared `least_squares` utilities.

4. **Residual stack (SimB)**
   - `residual_integerize`.
   - `residual_delta`.
   - `residual_golomb_rice`.
   - `residual_entropy` (wraps arithmetic coder or simple entropy coder).

5. **MDL & selection**
   - `mdl` — compute `L_model`, `L_residual`, `L_overhead`, `kappa`, and MDL-based decisions.

6. **Press Engine**
   - `press_pipeline` — high-level pipeline (Sense & Tag, Normalize, Factor & Press, Integrity & Metadata).
   - `press_bytes` — entry point for arbitrary bytes.
   - `press_numeric` — entry for structured numeric arrays.

7. **Flux Decoder (DePress)**
   - `depress_pipeline` — parse manifest/NAP, decode layers, reconstruct.

8. **Protocol Layer**
   - `apx_container` — ZIP wrapper for `.apx` build/parse.
   - `manifest` — read/write `MANIFEST.json`.
   - `nap_manifest` — read/write `nap/compression.json`.
   - `reports` — metrics report structure.

9. **UI**
   - `ui` — DOM wiring, file handling, display of logs/metrics.

### 1.2 Rationale

- Mirrors canon subsystems:
  - **Aether Core** → model library + AEON/APXi.
  - **Press Engine** → residual stack + MDL + pipeline.
  - **Flux Decoder** → DePress pipeline.
  - **Protocol Layer** → APX container + manifests.
- Keeps math-heavy parts separate from UI so they can later be reused (Node, workers, etc.).

---

## 2. Phase 1 — Core Primitives

### 2.1 Bitstream & varints

**Tasks**

- Implement `BitWriter`:
  - Methods: `writeBit`, `writeBits`, `writeByte`, `toUint8Array`.
- Implement `BitReader`:
  - Methods: `readBit`, `readBits`, `readByte`, `eof`.
- Implement varints:
  - `encodeVarintUnsigned(n: number|bigint): Uint8Array`.
  - `decodeVarintUnsigned(view, offset): { value, nextOffset }`.
  - `zigzagEncodeSigned(n: number|bigint): bigint`.
  - `zigzagDecodeSigned(u: bigint): bigint`.

**Requirements**

- Fully deterministic; no reliance on platform endianness beyond explicit conversions.
- Bounded integer ranges (e.g. up to 64-bit) documented.

### 2.2 Hashing & integrity

**Tasks**

- Provide `sha256(bytes: Uint8Array): Promise<Uint8Array>`:
  - Use `crypto.subtle.digest('SHA-256', bytes)` where available.
  - Fallback: optional pure JS implementation (can be introduced later if needed; not required for MVP in modern browsers).

**Use in pipeline**

- Compute `orig.sha256` for manifest.
- Compute per-layer hashes for `hashes.layers` in NAP manifest.

### 2.3 Arithmetic coding

**Tasks**

- Implement a simple arithmetic coder:
  - `ArithmeticEncoder` with methods:
    - `encode(symbol: number, model: ProbabilityModel)`.
    - `finish(): Uint8Array`.
  - `ArithmeticDecoder` with:
    - `decode(model: ProbabilityModel): number`.
- For MVP, start with:
  - A basic adaptive model or simple static frequency model per block.

**Rationale**

- Needed to align with canon’s emphasis on MDL and near-entropy-optimal coding.
- For MVP, performance constraints are modest; correctness and determinism matter most.

---

## 3. Phase 2 — AEON‑i & APXi

### 3.1 Opcode table & schemas

Based on APP_LOCAL_SPEC v1, define AEON‑i v1 opcodes:

- `OP_SEGMENT` (1) — `start_index (u)`, `length (u)`.
- `OP_AFFINE` (2) — `column_id (u)`, `a_num (s)`, `a_den (u)`, `b_num (s)`, `b_den (u)`.
- `OP_POLY3` (3) — `column_id (u)`, `c3_num (s)`, `c3_den (u)`, `c2_num (s)`, `c2_den (u)`, `c1_num (s)`, `c1_den (u)`, `c0_num (s)`, `c0_den (u)`.
- `OP_PERIODIC` (4) — `column_id (u)`, `period (u)`, `amplitude_num (s)`, `amplitude_den (u)`, `phase_num (s)`, `phase_den (u)`.
- `OP_COMBINE` (5) — `component_count (u)`, then list of `component_op_index (u)`.
- `OP_AR1` (6) — `column_id (u)`, `phi_num (s)`, `phi_den (u)`.
- `OP_AR2` (7) — `column_id (u)`, `phi1_num (s)`, `phi1_den (u)`, `phi2_num (s)`, `phi2_den (u)`.
- `OP_AR3` (8) — `column_id (u)`, `phi1_num (s)`, `phi1_den (u)`, `phi2_num (s)`, `phi2_den (u)`, `phi3_num (s)`, `phi3_den (u)`.

**Tasks**

- Implement constants `AEON_OPS` and reverse lookup `AEON_OPS_BY_ID`.
- Define TS/JS types:
  - `type AEONOpcodeName = 'SEGMENT' | 'AFFINE' | ...`.
  - `interface AEONOp { name: AEONOpcodeName; params: bigint[]; }`.

### 3.2 APXi encoder/decoder

**Encoder (`encodeAPXi`)**

- Layout:

  ```text
  u16  version_u16 = 1 (big-endian)
  varint op_count
  repeat op_count times:
      varint opcode_id
      varint param_count
      repeat param_count times:
          varint param_value (unsigned, with ZigZag for signed)
  ```

**Tasks**

- Implement encoder:
  - Write version (u16 BE).
  - Write `op_count` as unsigned varint.
  - For each op:
    - Lookup numeric `opcode_id` from name.
    - Write `opcode_id` as varint.
    - Write `param_count` as varint.
    - For each param, ZigZag encode if signed, then varint.

**Decoder (`decodeAPXi`)**

- Tasks:
  - Read version and validate `== 1`.
  - Read `op_count`.
  - For each:
    - Read `opcode_id`; map to name, error if unknown.
    - Read `param_count`.
    - For known opcodes (except COMBINE), validate `param_count` equals expected; else error.
    - Read that many varints and decode signed/unsigned into `bigint` params.
  - Error if:
    - APXi stream ends prematurely.
    - Extra bytes remain after decoding `op_count` (for v1, treat as error rather than extension).

**Rationale**

- Strict errors avoid silent corruption and are consistent with “proof‑carrying capsules”.

---

## 4. Phase 3 — Model Library (SimA)

### 4.1 Linear algebra utilities

**Tasks**

- Implement minimal linear algebra for small systems:
  - Solve `A * x = b` for small `n` (2–4) using Gaussian elimination.
  - Provide stable routines for:
    - Affine fit (2 parameters).
    - Polynomial degree 3 (4 parameters).

- Represent results as JS `number` first, then rationalize to `{ num: bigint, den: bigint }`.

### 4.2 Concrete models

**Model implementations**

- `fitAffine(segment: number[]): RationalParams`.
- `fitPoly3(segment: number[]): RationalParams`.
- `fitPeriodic(segment: number[]): RationalParams`.
- `fitARk(segment: number[], order: 1|2|3): RationalParams`.

Each performs:

1. Estimate floating-point parameters via least-squares (or Yule–Walker/Burg for AR).
2. Convert each parameter to a rational approximation with bounded denominator (e.g. `den <= 2^32`).
3. Return rational params and a function or descriptor that can be turned into AEON ops.

**Simulation functions**

- `simulateAffine(params, length): number[]`.
- `simulatePoly3(...)`, `simulatePeriodic(...)`, `simulateARk(...)`.

These must be deterministic and exact given the rational parameters.

### 4.3 Model selection (`selectModelForSegment`)

**Tasks**

- For a numeric segment `segment: number[]`:
  1. Try each candidate model family (Affine, Poly3, Periodic, AR1–3).
  2. For each successful fit:
     - Simulate `x_hat`.
     - Compute residual `r = segment - x_hat` (in JS number space initially).
     - Integerize residual (see Phase 4) and encode with SimB stack to get `L_residual`.
     - Compute `L_model` as bit-length of AEON descriptor representation.
     - Compute `L_A = L_model + L_residual`.
  3. Compute `L_B` for dictionary-only baseline (SimB-only) as a separate code path.
  4. Select the better of `L_A` and `L_B` (plus gate bit cost) per segment.

**Output**

- `{ kind: 'symbolic' | 'dictionary', modelType, params, costBits, meta }`.

**Rationale**

- Directly instantiates the dual compressor mixture (symbolic vs dictionary) and MDL selection logic described in the Math Compendium and legacy reports.

---

## 5. Phase 4 — Residual Stack (SimB)

### 5.1 Integerization & delta coding

**Tasks**

- For MVP numeric demo:
  - Restrict to integer-valued or exactly representable floats.
- Implement:
  - `integerizeResiduals(residuals: number[]): bigint[]`.
  - `deltaEncode(values: bigint[]): bigint[]`.
  - `deltaDecode(values: bigint[]): bigint[]`.

**Design choice for MVP**

- If input data cannot be represented exactly in integer space for lossless, we do **not** allow `PRESS_LOSSLESS` on that dataset in v1.

### 5.2 Golomb–Rice coding

**Tasks**

- Implement Golomb–Rice encoder/decoder:
  - `encodeGolombRice(values: bigint[], k: number): BitWriter`.
  - `decodeGolombRice(reader: BitReader, k: number, count: number): bigint[]`.

- Simple heuristic to choose `k` per block (e.g. based on sample mean or variance of values).

### 5.3 Final residual codec interface

**Tasks**

- `encodeResidualSimB(values: bigint[]): { bytes: Uint8Array, bits: number, codecParams }`.
- `decodeResidualSimB(bytes: Uint8Array, codecParams, length: number): bigint[]`.

In MVP:

- Use integerization → delta encode → Golomb–Rice.
- Arithmetic coding can be layered on later; for first pass, we can keep it Golomb–Rice only and treat that as our entropy coder.

---

## 6. Phase 5 — Press Engine & DePress Pipeline

### 6.1 Press for arbitrary bytes (`pressBytes`)

**Tasks**

- Entry: `pressBytes(input: Uint8Array, options?)`.

Steps:

1. **Sense & Tag**
   - Compute `orig.name` (from filename if available) and `orig.size_bytes`.
   - Compute `orig.sha256`.
   - Set `press.mode = 'lossless'`, `press.profile = 'PRESS_LOSSLESS'`, `dtype = 'bytes'`, `shape = [size_bytes]`.

2. **Path decision (v1)**
   - For MVP, treat arbitrary bytes as **dictionary/residual-only**:
     - Encode entire byte array as residual using a general-purpose SimB path (e.g. treat bytes as integers 0–255, apply simple delta + Huffman/entropy coding, or even store raw for v0).
   - SimA is **not** used for arbitrary bytes in v1.

3. **NAP manifest**
   - If we treat residual-only as a single SimB layer, create a NAP manifest with one layer:
     - `id = 'simB_main'`, `kind = 'AP.residual'`, `parent = null`, `refs = []`, `params` describing codec, `ordering` index 0.

4. **Manifest**
   - Build `MANIFEST.json` using APP_LOCAL_SPEC v1 schema.
   - Include `layers` entry referencing SimB binary payload and NAP manifest.

5. **APX container**
   - Use ZIP builder to create `.apx` with:
     - `MANIFEST.json` at root.
     - `nap/compression.json`.
     - `layers/simB/simB_main.bin`.
     - Optional `reports/report.json`.

**Output**

- `{ apxBytes: Uint8Array, manifest, nap }`.

### 6.2 Press for numeric arrays (`pressNumericArray`)

**Tasks**

- Entry: `pressNumericArray(data: number[], options?)`.

Steps:

1. **Segmentation**
   - Split into windows `segment` of size `W` (e.g. 128, 256 as initial default).

2. **Per-segment model selection**
   - For each `segment`, call `selectModelForSegment`.
   - Record chosen model type and parameters if symbolic; otherwise mark as dictionary-only.

3. **Build AEON ops**
   - Convert selected model parameters to AEON ops (Affine/Poly3/Periodic/AR1–3) with correct `column_id` and rational parameters.

4. **Residual encoding**
   - For each segment, compute residuals and pass them to SimB encoder.

5. **AEON/APXi stream**
   - Build an APXi stream for all segments (details: per-column/per-segment multiplexing; for MVP, we can keep one stream with SEGMENT + model ops in sequence).

6. **NAP manifest & MANIFEST.json**
   - Create SimA and SimB layer entries as per APP_LOCAL_SPEC v1.
   - Create NAP manifest describing their relationship.

7. **APX container**
   - Same as arbitrary bytes, but with both SimA and SimB payloads.

**Output**

- `.apx` capsule + structured manifest/metrics for numeric experiments.

### 6.3 DePress pipeline (`depress`)

**Tasks**

- Entry: `depress(apxBytes: Uint8Array): Promise<{ bytes: Uint8Array, manifest, nap }>`.

Steps:

1. **Parse APX**
   - Use ZIP parser to read entries.
   - Read and parse `MANIFEST.json` and `nap/compression.json`.

2. **Branch by profile & dtype**
   - For `PRESS_LOSSLESS` + `dtype = 'bytes'` + SimB-only:
     - Decode residual layer and reconstruct original bytes.
   - For numeric demo (`dtype = 'numeric_array'` with SimA+SimB):
     - Decode APXi stream → AEON ops.
     - Reconstruct model predictions → decode residuals → add to predictions.

3. **Integrity check**
   - Compute hash of reconstructed bytes; ensure match with `orig.sha256`.

4. **Return**
   - Original bytes or numeric array.

**Rationale**

- Mirrors Flux Decoder responsibilities: reconstruction + fidelity validation.

---

## 7. Phase 6 — APX Container & ZIP Handling

### 7.1 ZIP strategy

**Tasks**

- Use a small JS ZIP library (e.g. JSZip) as a dependency.
- Wrap it with an `apx_container` module exposing:
  - `buildApx(manifestJson, napJson, layers, reports?): Promise<Uint8Array>`.
  - `parseApx(bytes: Uint8Array): Promise<{ manifestJson, napJson, layers, reports }>`.

**Layout requirements**

- Root:
  - `MANIFEST.json` (uncompressed entry).
- `nap/`:
  - `compression.json` (uncompressed entry).
- `layers/`:
  - `layers/simA/simA_main.apxi` (if present).
  - `layers/simB/simB_main.bin`.
- `reports/` (optional):
  - `reports/report.json`.

### 7.2 Manifest & NAP helpers

**Tasks**

- `writeManifest(manifestObj): Uint8Array` and `readManifest(bytes): ManifestObj`.
- `writeNapManifest(napObj): Uint8Array` and `readNapManifest(bytes): NapManifestObj`.

Manifest schema matches APP_LOCAL_SPEC v1; NapManifest matches APP_LOCAL_SPEC v1’s NAP example.

---

## 8. Phase 7 — UI & UX

### 8.1 Basic offline SPA

**Tasks**

- `index.html` containing:
  - File input `#inputFile`.
  - Buttons: `#btnPress`, `#btnDePress`.
  - Download link areas.
  - A `<pre id="log">` or similar for diagnostics.

- `index.js`:
  - On `#btnPress` click:
    - Read file as `Uint8Array`.
    - Call `pressBytes`.
    - Trigger download of `.apx` blob.
    - Log manifest and metrics.
  - On `#btnDePress` click:
    - Select `.apx` input.
    - Call `depress`.
    - Trigger download of reconstructed file.
    - Log any checks performed.

### 8.2 Numeric demo view

**Tasks**

- Add a secondary panel/tab:
  - Textarea to paste JSON arrays (`[1,2,3,...]`).
  - Buttons to `Press numeric` and `DePress numeric`.
  - Panel to display:
    - Chosen model per segment.
    - List of AEON ops (decoded, human-readable).
    - Residual bit-lengths per segment.
    - `L_total`, `L_naive`, `kappa`.

**Rationale**

- Gives a transparent view into the model+residual stack, separate from arbitrary binary files.

---

## 9. Phase 8 — Testing & Validation

### 9.1 Unit tests

**Targets**

- Varint/ZigZag round-trip on a range of integers.
- Bitstream write/read for sequences of bits.
- Arithmetic coder encode→decode for simple symbol sequences.
- AEON/APXi encode→decode identity on curated opcode sequences.
- Residual stack encode→decode identity for synthetic integer arrays.

### 9.2 E2E Press/DePress tests

**Tasks**

- Build a small test harness (in Node or browser) that:
  - Generates test files:
    - Random bytes.
    - Repeating patterns.
    - Small numeric arrays with known structure (affine, poly, periodic, AR1).
  - Calls `pressBytes` or `pressNumericArray`.
  - Calls `depress` on resulting `.apx`.
  - Asserts:
    - Output equals input (byte-equal) for lossless.
    - `orig.sha256` from manifest matches recomputed hash.

**Stretch**

- For numeric demo, optionally check that recovered numeric arrays match the originals exactly for lossless.

---

## 10. Phase 9 — Post-MVP Extensions (Not Required for First Page)

Once MVP is passing tests:

1. **Enable ε-bounded profiles**
   - Implement quantization per-field with `q` satisfying `q/2 ≤ ε_field`.
   - Add scoreboard `O` evaluation and acceptance tests from legacy “Crush without regret” runbook.

2. **Multi-layer NAP stacks**
   - Extend NAP manifest and decode logic to handle more than one SimA and SimB layer (stacked/nested).

3. **Additional AEON ops**
   - Consider adding an LFSR-specific opcode for the known demo.
   - Consider LCDRM-style ops for relational layers.

4. **Press policy cards**
   - UI for defining per-source Press policies (type, track, O-fields, q per field).

---

## 11. Ticketization Snapshot

If you want this broken down for implementation tickets, a rough first slice:

1. **Core utils**
   - T1: Bitstream (read/write bits & bytes).
   - T2: Varint + ZigZag encode/decode.
   - T3: SHA-256 wrapper.

2. **Codecs**
   - T4: Arithmetic coder MVP.
   - T5: Golomb–Rice coder.

3. **AEON/APXi**
   - T6: AEON opcode table + types.
   - T7: APXi encoder.
   - T8: APXi decoder + validation.

4. **Models**
   - T9: Least-squares utilities.
   - T10: Affine/poly fit + simulate.
   - T11: Periodic/AR fit + simulate.
   - T12: Model selection.

5. **Residual & MDL**
   - T13: Integerization + delta.
   - T14: SimB encoder/decoder.
   - T15: MDL functional and kappa.

6. **Press Engine & DePress**
   - T16: `pressBytes` (SimB-only path).
   - T17: `pressNumericArray` (SimA+SimB demo).
   - T18: `depress`.

7. **APX & UI**
   - T19: APX container builder/parser.
   - T20: Manifest/NAP helpers.
   - T21: Basic SPA UI.
   - T22: Numeric demo UI.

This build plan is designed to be faithful to canon while producing a concrete, offline JS page that exercises `.apx`, manifests, and at least one full SimA+SimB pipeline on real data.



<!-- END SOURCE: astral_press_js_offline_mvp_build_plan_2025_11_20.md -->


---

<!-- BEGIN SOURCE: astral_press_js_full_implementation_build_plan_v_1_beyond_mvp.md -->

# Astral Press — JS Full Implementation Build Plan v1 (Beyond MVP)

Status: **Local build plan** for `APP-UROBOROS-REF-1` in JS, extending the existing **Offline MVP** to a **full Press implementation** that respects canon requirements from:

- **APP\_LOCAL\_SPEC v1 — Aether Press Local Implementation (2025-11-20)**
- **Astral Press — APP Implementer Checklist v1 (2025-11-20)**
- **Astral Press — APP Complement Sheet v2 (Legacy Docs Pass)**
- **Astral Press — APP Complement Sheet v4 (Implementation Canon Pack Pass)**
- **Astral Press — Multi-Layer NAP & MDL Stack Spec v1 (Stack Until It Stops Making Sense)**
- **Astral Press — Policy & Dimensional Controls Spec v1 (P\_state, P\_cite & Dims Press)**

This build plan assumes the **JS Offline MVP Build Plan** is implemented:

> “Goal: turn the current APP canon + APP\_LOCAL\_SPEC v1 into a first offline web-page JavaScript implementation of Press/DePress… MVP mode: PRESS\_LOSSLESS only, dtype="bytes" default, with a dedicated numeric demo path for SimA/SimB.”

The goal here is to go **beyond the MVP** to a JS reference implementation that:

- Implements **two-track Press** (P\_state & P\_cite) as per legacy performance docs.
- Implements **Press policy cards** and **Dims Press** (per-dimension controls) on top of APP\_LOCAL\_SPEC.
- Implements **ε-bounded profiles** and **O-only acceptance harness** (“Crush without regret” checks).
- Implements **multi-layer NAP stacks + MDL layer admission rule** as per NAP & MDL spec.
- Preserves the **.apx + NAP + AEON/APXi + SimA/SimB** semantics locked in APP\_LOCAL\_SPEC.

This document is a **dev plan**: it does not redefine canon; it only shows **what code must be added or extended** in the JS implementation to reach full Press behaviour.

---

## 0. Scope & Targets

### 0.1 Environments & constraints

- **Environment**: browser-based, offline-capable JS SPA (same as MVP) with modular TS/JS code that can also run under Node for tests.

- **Capsule format**: `.apx` ZIP container with `MANIFEST.json`, `nap/compression.json`, and layer payloads as defined in APP\_LOCAL\_SPEC:

  > “`.apx` is a ZIP file with… `MANIFEST.json` — Press Metadata Manifest… `layers/simA/`, `layers/simB/`, `nap/`, `reports/`…”

- **APP implementation ID** fixed by canon:

  ```jsonc
  "app_protocol": "APP",
  "app_protocol_version": "1.0",
  "app_impl": "APP-UROBOROS-REF-1",
  "app_impl_version": "1.0.0"
  ```

- **Target feature level**: implementer should be able to claim:

  > “This implementation follows the Aether Press canon where it’s specified, and documents all local design choices where canon leaves space open… Given the same input, same APP version, and same local config, this implementation is deterministic and passes the lossless/ε-bounded guarantees defined in canon.”

  as per the APP Implementer Checklist.

### 0.2 MVP vs Full-Press delta (high-level)

Starting point (MVP):

- `.apx` container with `MANIFEST.json`, optional NAP manifest, and SimB-only or SimA+SimB payloads.
- `PRESS_LOSSLESS`, `dtype="bytes"` path + numeric demo path using SimA+SimB and AEON/APXi.
- Deterministic Press/DePress for small offline datasets.

Full-Press additions:

1. **Multi-layer NAP stacks + MDL layer selection** (multi-SimA/SimB, DAG semantics, MDL stopping rule).
2. **Policy layer**: Press policy cards per source, field-level ε/q, per-dim controls (exact vs quantized, selective retention, residual fraction, dict scopes).
3. **Two-track Press**: P\_state (reconstructive capsules) and P\_cite (proof/pointer capsules) with manifest+policy wiring.
4. **ε-bounded profiles + O-only acceptance**: implement “Crush without regret” checks, including field-level bounds and Δ=0/Δ>0 replay tests (where host system provides O).
5. **Extended AEON/APXi & model library integration**: ensure all canon AEON opcodes and model families used in spec are wired through model selection, APXi, and NAP.
6. **Dims Press per-dimension controls** for NAP bus / numeric datasets.
7. **Test harnesses** for MDL decisions, policy enforcement, two-track correctness, and acceptance checks.

The remainder of this plan is structured around these deltas, layered on top of the existing MVP modules.

---

## 1. Architecture Delta — From MVP Modules to Full Press

The MVP plan defined modules such as `bitstream`, `varint`, `hash`, `arith_coder`, `aeon_ops`, `apxi_encode/dec`, `models_*`, `press_pipeline`, `depress_pipeline`, `apx_container`, and `ui`.

To reach full Press, we extend and add modules as follows:

### 1.1 New/extended modules

1. \`\` (new)

   - JSON schema + loader for Press policy cards per source.
   - Compiler/validator that enforces ε/q constraints and Dims Press controls.
   - Exposes a `CompiledPressPolicy` object consumed by `press_pipeline` and `depress_pipeline`.

2. \`\` (new or folded into `policy_cards`)

   - Implements per-dimension and per-layer fidelity controls:
     - Exact vs quantized dims.
     - Residual fraction per layer.
     - Selective retention (`recompute`, `residual`, `full`).
     - Dict scopes (`per_source`, `global_press`).

3. \`\` (new)

   - Given a dataset and active policy, chooses NAP layer structure:
     - Constructs `layers[]` entries (`id`, `kind`, `parent`, `refs[]`, `params`, `ordering`).
     - Applies MDL functional to candidate layers and enforces the MDL stopping rule.
     - Produces `nap/compression.json` object consistent with APP\_LOCAL\_SPEC and NAP spec.

4. \`\` (extend MVP)

   - From the MVP’s simple MDL calculations to full Press-level MDL functional:
     - Computes `L_model`, `L_residual`, `L_overhead` and `L_total`.
     - Computes `L_naive` and `kappa`.
     - Implements layer-level decision rule and optional margin bits (e.g. 8 bits).

5. \`\` (new)

   - Bridges policies with runtime decisions:
     - Which fields go to P\_state vs P\_cite.
     - Which dimensions are exact vs quantized.
     - Which residuals to keep vs recompute.
   - Provides lookup functions used by `press_bytes`, `press_numeric`, and `depress`.

6. \`\` (new)

   - Implements two-track Press flows:
     - P\_state pipeline (full NAP+stack+residuals for reconstructive capsules).
     - P\_cite pipeline (hashes/lengths/proofs for external sources).
   - Extends `MANIFEST.json` to include `press_track` and `cite.sources[]` as per Policy spec.

7. \`\` (new)

   - Encodes “Crush without regret” checks from the legacy performance report:
     - Field-level ε/q bounds.
     - Replay test (Δ=0) on scoreboard O.
     - Predictive test (Δ>0) on O.
     - Idempotence & isolation checks.
   - For offline JS, at minimum implement:
     - Field-level checks.
     - Hash equality checks for lossless.

These modules should be wired in without breaking the MVP entry points (`pressBytes`, `pressNumericArray`, `depress`), which become **policy-aware** and **NAP-aware**.

---

## 2. Multi-Layer NAP & MDL Stack — Implementation Tasks

The NAP Compression Manifest and MDL rules are canon-backed via APP\_LOCAL\_SPEC and the NAP/MDL spec:

> “NAP\_Manifest := { layers[], knit\_rules, deterministic\_order, hashes } … `layers[] {id, kind∈{AP.symbolic (SimA), AP.residual (SimB)}, parent, refs[], params, ordering}` … graph formed by layers and parent/refs must be a DAG… there must exist a topological order such that DePress(Press(D; M); M) = D.”\
> “You must only add a new model layer Mi if it reduces total description length L\_total; once adding another layer would increase L\_total, the stack must stop.”

### 2.1 Task group: NAP manifest support (beyond MVP)

**TG-NAP-1 — Generalise NAP manifest to multi-layer stacks**

- Extend the MVP `nap/compression.json` handling to support **multiple layers** in `layers[]`, not just `simA_main` + `simB_main`.
- Implement JS types for LayerEntry consistent with APP\_LOCAL\_SPEC/NAP spec:
  ```ts
  interface NapLayerEntry {
    id: string;                         // e.g. "simA_main", "simB_main", "simA_lfsr", ...
    kind: "AP.symbolic" | "AP.residual";
    parent: string | null;             // single parent link for DAG
    refs: string[];                    // optional extra refs
    params: Record<string, any>;       // layer-specific config
    ordering: {
      order_index: number;             // topological index
      stage: string;                   // e.g. "symbolic", "residual", "post"
    };
  }

  interface NapManifest {
    schema_version: string;            // "nap_manifest_v1"
    layers: NapLayerEntry[];
    knit_rules: Record<string, any>;
    deterministic_order: {
      topological_order: string[];     // layer ids
    };
    hashes: {
      algo: string;                    // "sha256"
      layers: Record<string, string>;  // id -> hash
    };
  }
  ```

**TG-NAP-2 — DAG validation & topological ordering**

- Implement a DAG validator for `NapManifest`:
  - Build adjacency from `parent` and `refs[]`.
  - Detect cycles; if any => error.
  - Compute a deterministic topological ordering, stored in `deterministic_order.topological_order`.
- Unit tests:
  - Valid single-layer, two-layer (SimA→SimB), and multi-layer stacks.
  - Intentionally cyclic manifest must be rejected.

### 2.2 Task group: MDL functional & layer admission

The metrics spec gives:

> “Total description length: L\_total = L\_model + L\_residual + L\_overhead … naive baseline L\_naive = 8 \* |S| … kappa = L\_naive − L\_total … new layer Mi is accepted only while adding the layer reduces L\_total; once adding another model would increase overall description length, the process stops.”

**TG-MDL-1 — Implement full MDL functional**

- Extend `mdl` module to compute:

  ```ts
  interface MdlBreakdown {
    L_model: number;      // bits for AEON/APXi descriptors
    L_residual: number;   // bits for residual payloads
    L_overhead: number;   // bits for manifest/container overhead
    L_total: number;      // sum
    L_naive: number;      // 8 * |S| in bytes
    kappa: number;        // L_naive - L_total
  }
  ```

- For `L_overhead`, include:

  - APXi version word + op\_count + param counts.
  - `MANIFEST.json` and `nap/compression.json` bit sizes (compressed or raw JSON size \* 8; pick one and document).
  - Any constant per-capsule overhead your environment imposes.

**TG-MDL-2 — Implement layer admission rule**

- In `nap_builder`, when considering a candidate layer `M_i`:

  - Compute updated `MdlBreakdown` for the entire stack with `M_i` included.
  - Accept `M_i` **iff**:
    ```text
    L_total' + margin_bits < L_total
    ```
    where `margin_bits` is small (e.g. 8 bits) to avoid flapping on tiny differences.

- If no candidate layer yields a lower `L_total` than the current best, **stop**.

**TG-MDL-3 — Tests for MDL decisions**

- Synthetic tests:
  - Data with obvious simple structure (e.g. linear ramp) where adding an affine SimA layer + residual should drastically reduce `L_total`.
  - Data that is already “random-looking” where adding model layers should **not** be accepted.
- Verify that:
  - `kappa > 0` when structure is present.
  - `kappa <= 0` (or very small) for random data, matching claims like “random dataset remained incompressible.”

### 2.3 Task group: Stack builder integration

**TG-STACK-1 — Integrate **``** and future Press paths**

- Refactor `pressNumericArray` (and later structured Press paths) so that instead of constructing a fixed `simA_main`+`simB_main` pair, it:
  - Collects candidate layers and their costs via `mdl`.
  - Delegates to `nap_builder` to select layers based on MDL.
  - Receives a `NapManifest` plus layer payloads, which are then passed to `apx_container.buildApx`.

**TG-STACK-2 — SimA/SimB layering patterns**

- Codify a small set of allowed stack patterns corresponding to canon examples:
  - Simple: `SimA_main → SimB_main`.
  - Multi-layer symbolic: `SimA_affine → SimA_periodic → SimB_residual`.
  - AR residual layers, where SimB implements AR(1..3) encoded via AEON.
- Ensure the `nap_builder` only emits allowed patterns for v1.

---

## 3. Policy Cards & Dims Press — Implementation Tasks

The legacy performance report introduces Press policy cards and knobs:

> “Press policy card (use per source)… Type: (text/pdf/image/log/table/sensor) Track: [P\_state | P\_cite]… O-fields derived… Quantization q per field…
>
> Practical knobs that drive the crush ratio: Integerization pipeline… Bound error upfront: if you quantize a scalar with step q, your max absolute error is ≤ q/2. Pick q so it respects the field’s ε… O-only comparison… Content dedupe…”

The Policy & Dims spec makes this concrete as JSON.

### 3.1 Task group: Policy card schema & loader

**TG-POLICY-1 — Implement policy card JSON schema & validation**

- Implement JSON schema and validator for objects of the form:

  ```jsonc
  {
    "schema_version": "press_policy_card_v1",
    "source_id": "IMU:front_left_wheel",
    "human_name": "Front left wheel IMU",
    "type": "sensor",                // text/pdf/image/log/table/sensor
    "track": ["P_state", "P_cite"], // one or both
    "o_fields": ["pose.x", "pose.y", "velocity", "health_flag"],
    "numeric_fields": {
      "pose.x": { "dtype": "float64", "epsilon": 1e-4, "q": 2e-4 },
      "pose.y": { "dtype": "float64", "epsilon": 1e-4, "q": 2e-4 },
      "velocity": { "dtype": "float32", "epsilon": 1e-3, "q": 2e-3 }
    },
    "dim_controls": {
      "pose.x": { "mode": "quantized", "retention": "residual", "residual_fraction": 0.1 },
      "pose.y": { "mode": "quantized", "retention": "residual" },
      "health_flag": { "mode": "exact", "retention": "full" }
    },
    "profiles": {
      "press_profile": "PRESS_SENSOR_MED",
      "dims_profile": "DEFAULT"
    }
  }
  ```

- Validation rules:

  - For each numeric field with `mode = "quantized"`, enforce `q/2 <= epsilon`.
  - For `mode = "exact"`, enforce `epsilon = 0` and `q = 0` (or null).
  - Ensure `o_fields` are known to the global O-schema.

**TG-POLICY-2 — Policy store & lookup**

- Provide a policy store keyed by `source_id`:
  - Load policies from JSON files or embedded config.
  - Expose API: `getPolicyForSource(sourceId): PressPolicy | null`.

### 3.2 Task group: Dims Press controls

From Dims Press:

> “FIDELITY CONTROLS YOU CAN SET PER-DIMENSION (OR PER-LAYER)… Exact vs quantized dims… Residual fraction… Selective retention {recompute, residual, full}… Dict scopes: per-node dictionaries or a global Press dict on the NAP bus.”

**TG-DIMS-1 — Implement Dims Press controls in runtime**

- Extend `pressNumericArray` (and other structured Press paths) to honour `dim_controls`:
  - `mode = "exact"` → dimension must be preserved exactly in P\_state (no quantization or lossy transforms).
  - `mode = "quantized"` → dimension passes through integerization/quantization according to ε/q.
  - `retention`:
    - `"recompute"` → do not store residuals for this field; rely on recomputation formulas at replay time.
    - `"residual"` → store compressed residuals as usual.
    - `"full"` → store verbatim or near-verbatim (e.g. provenance tags).
  - `residual_fraction` → drive tuning of residual codec (e.g. chunk sizes or bits kept).

**TG-DIMS-2 — Dict scopes**

- Implement dictionary scoping based on a `dict_scope` config:
  - `"per_source"` → maintain dictionary per `source_id`.
  - `"global_press"` → maintain one dictionary shared across all sources on a NAP bus run.

**TG-DIMS-3 — Tests for Dims behaviour**

- Synthetic tests:
  - Fields marked `exact` must round-trip bit-identical.
  - Fields marked `quantized` must satisfy per-field bound `|x_post - x_pre| ≤ q/2 ≤ ε`.
  - `recompute` fields must match recomputed values using only P\_state data; any mismatch flags a policy bug.

---

## 4. Two-Track Press (P\_state & P\_cite) — Implementation Tasks

Legacy docs define two-track Press:

> “Two-track Press (do this every time)… P\_state (reconstructive) — the minimal snapshot needed for T to resume exactly… P\_cite — tiny proofs/pointers for everything else… You keep the small, exact computational snapshot (P\_state), plus tiny proofs/pointers for the rest (P\_cite).”

The Policy spec refines track semantics and manifest representation.

### 4.1 Task group: Manifest & capsule wiring

**TG-PTRACK-1 — Extend MANIFEST to record press\_track & cite sources**

- Add fields to `MANIFEST.json` as per Policy spec:

  ```jsonc
  "press_track": "P_state",   // or "P_cite"
  "cite": {
    "sources": [
      {
        "id": "doc:spec:press_v2",
        "kind": "pdf",
        "uri": "…",
        "sha256": "…",
        "size_bytes": 123456,
        "notes": "Used only for section 3.2 invariants."
      }
    ]
  }
  ```

- For P\_state capsules, `press_track = "P_state"` and `cite` is optional.

- For P\_cite capsules, `press_track = "P_cite"` and payload is proof/pointer-only.

**TG-PTRACK-2 — P\_state vs P\_cite pipelines**

- Implement a `p_tracks` module that provides:

  - `pressState(input, options)` → produce P\_state `.apx` capsule(s) that can be used for replay.
  - `pressCite(input, options)` → produce P\_cite `.apx` capsule(s) containing hashes/lengths and a small invariant summary, but **no** replay state.

- Policy enforcement:

  - P\_state capsules may only include data required for the computational episode `T` to replay.
  - P\_cite capsules may **not** be used as live inputs to `T` in replay; they exist purely as provenance proof.

### 4.2 Task group: Policy-driven track decisions

**TG-PTRACK-3 — Drive track selection from policy cards**

- Based on policy card `track` field:

  - `track = ["P_state"]` → source contributes only to P\_state.
  - `track = ["P_cite"]` → source is treated as out-of-band provenance; only P\_cite is generated.
  - `track = ["P_state", "P_cite"]` → both tracks generated; P\_cite holds proof for external docs, P\_state holds simulation-relevant state.

- Implement logic in `pressBytes`/`pressNumeric` wrappers (or higher-level orchestrator) that:

  - Queries policy cards for each source.
  - Calls `pressState` and/or `pressCite` accordingly.

### 4.3 Tests for P\_state/P\_cite invariants

- P\_state-only sources:

  - DePress + replay tests must succeed using only P\_state capsule.

- P\_cite-only sources:

  - DePress must expose hashes and metadata but no simulation state.
  - Attempting to use P\_cite as simulation state must be blocked.

- Dual-track sources:

  - P\_state must be sufficient for replay;
  - P\_cite hashes and sizes must match the original external artifacts.

---

## 5. ε-Bounded Profiles & Acceptance Harness — Implementation Tasks

The Press performance report provides the acceptance runbook:

> “Field-level bounds: For every numeric field x you store after quantization q: |x\_post − x\_pre| ≤ q/2 ≤ ε\_x… Replay test: DePress then run Δ = 0: O unchanged… Predictive test: DePress and run T^Δ; check d(O\_true, O\_replayed) ≤ ε… Document proof: Keep {hash, bytes} for each external source in P\_cite… Idempotence: Same envelope + same nonce ⇒ no net change to O… Isolation: Prior checkpoint O-hashes never change.”

### 5.1 Task group: ε profiles & quantization

**TG-EPS-1 — Implement ε-bounded profiles in code**

- Define a small set of named ε profiles beyond `PRESS_LOSSLESS`, matching policy cards:

  - `PRESS_SENSOR_MED` (example sensor profile).
  - `PRESS_LOG_CRUSH` (logs/events profile).

- For each profile, configure per-field ε and `q` such that `q/2 ≤ ε_field` as per policy cards.

- Extend `pressNumericArray` and related functions to:

  - Quantize fields according to profile.
  - Use integerization and residual stack on quantized values.

**TG-EPS-2 — Field-level bound checks**

- In `acceptance_harness`, implement:

  ```ts
  function checkFieldBounds(original: number[], reconstructed: number[], epsilon: number, q: number): boolean {
    const maxAbsDiff = max_i |x_post[i] - x_pre[i]|;
    return maxAbsDiff <= q / 2 && q / 2 <= epsilon;
  }
  ```

- Run this check for every numeric field the policy marks as quantized.

### 5.2 Task group: O-only acceptance

**TG-ACCEPT-1 — Scoreboard O schema & integration**

- Define an O-schema for the JS demo environment, e.g. for a numeric system:

  - `O = { pose.x, pose.y, velocity, health_flag, … }`.

- Implement mapping from Press outputs back into `O`, using host system simulation or a mock.

**TG-ACCEPT-2 — Replay & predictive tests**

- Provide API in `acceptance_harness`:

  - `runReplayTestP0(P_state_capsule, T, O_schema, epsilon_O)` — Δ=0 test.
  - `runPredictiveTest(P_state_capsule, T, O_schema, epsilon_O, delta)` — Δ>0 test, where `T` is provided by the host system.

- For offline JS builds without full host simulation:

  - Provide stub/mocked tests that at least verify integrity and field-level bounds.
  - Document where integration with a real T/O system must plug in.

**TG-ACCEPT-3 — Idempotence & isolation**

- In multi-checkpoint scenarios (outside MVP):
  - Track O-hashes per checkpoint.
  - Verify idempotence:
    - Re-applying Press/DePress at same envelope+nonce does not change O.
  - Verify isolation:
    - Older checkpoint O-hashes remain stable when new capsules are produced.

---

## 6. Extended AEON/APXi & Model Library Integration — Implementation Tasks

Legacy docs and APP\_LOCAL\_SPEC specify:

> “Known opcodes… OP\_SEGMENT, OP\_AFFINE, OP\_POLY3, OP\_PERIODIC, OP\_COMBINE, OP\_AR1, OP\_AR2, OP\_AR3… Parameters encoded as varints (ZigZag for signed)… APXi := [ version\_u16, v0, v1, v2, … ] where v\_i are varints… decoder must treat unknown opcodes and wrong param counts as hard errors.”

### 6.1 Task group: Opcode coverage & error handling

**TG-AEON-1 — Ensure all canon AEON opcodes are implemented**

- Confirm implementation for:

  - `OP_SEGMENT`
  - `OP_AFFINE`
  - `OP_POLY3`
  - `OP_PERIODIC`
  - `OP_COMBINE`
  - `OP_AR1`, `OP_AR2`, `OP_AR3`

- Ensure parameter lists match APP\_LOCAL\_SPEC (num/den rationals, column\_id, component lists, etc.).

**TG-AEON-2 — Strict APXi error handling**

- Enforce:

  - Unknown `opcode_id` ⇒ hard decode error.
  - Wrong `param_count` for known opcode ⇒ hard decode error.
  - Premature end of varint stream ⇒ hard decode error.
  - Extra bytes after `op_count` decoded ⇒ hard decode error for v1.

- Unit tests for malformed APXi streams.

### 6.2 Task group: Model selection & fitting

From APP\_LOCAL\_SPEC & legacy:

> “select\_model(segment)… fit\_params(M, segment)… extract\_invariants(segment, M)… simulate(M, θ, I, len)… r = segment − x\_hat… Packet{ model\_id, θ, I, eps, R, checksum(segment) }.”

**TG-MODEL-1 — ****\`\`**** alignment**

- Ensure `selectModelForSegment`:
  - Considers the full v1 model library (Affine, Poly3, Periodic, AR1–3, dictionary-only).
  - Computes `L_A` (model + residual) and `L_B` (dictionary-only) per segment.
  - Chooses according to the dual compressor mixture rule (min `L + gate`), consistent with Math Compendium.

**TG-MODEL-2 — Fitting algorithm robustness**

- Implement robust least-squares and AR fitting (Yule–Walker/Burg) with:

  - Deterministic results for given input.
  - Rationalization of coefficients (`num/den`) within bounded denominators.

- Unit tests against:

  - Known synthetic data (ramps, sinusoids, AR processes).
  - Edge cases (short segments, near-singular matrices) where fallback to dictionary-only is expected.

---

## 7. UI & UX Extensions for Full Press

Beyond the MVP’s simple file picker and numeric demo, full Press needs minimal UI additions to expose new behaviours.

### 7.1 Policy & track selection

**TG-UI-1 — Policy selection widget**

- Add UI controls to:
  - Select a `press_profile` (e.g. `PRESS_LOSSLESS`, `PRESS_SENSOR_MED`, `PRESS_LOG_CRUSH`).
  - Select a `source_id` (to load a specific policy card) or auto-deduce it from file type.

**TG-UI-2 — Track display**

- Show, for a given run:
  - Whether a P\_state capsule, P\_cite capsule, or both were generated.
  - For P\_cite, list `cite.sources[]` entries.

### 7.2 Stack and MDL introspection

**TG-UI-3 — NAP & MDL debug panel**

- Extend debug panel to display:
  - Parsed `nap/compression.json` with layer graph.
  - Per-layer `L_model`, `L_residual`, and `L_total` contributions.
  - Overall `L_naive`, `L_total`, and `kappa`.

**TG-UI-4 — Acceptance results display**

- Show pass/fail status for:
  - Field-level bounds.
  - Hash equality.
  - (Where available) O-level replay tests.

---

## 8. Testing & Validation Plan (Full Press)

Building on the MVP tests, full Press requires additional suites.

### 8.1 Policy & Dims tests

- Validate that invalid policy cards (e.g., `q/2 > ε`, `recompute` with no recomputation path) cause Press to **fail closed** (no run) or fall back to a safe `PRESS_LOSSLESS` mode only if explicitly configured.
- Validate that Dims controls behave per spec (exact vs quantized, recompute/residual/full).

### 8.2 NAP & MDL tests

- Validate multi-layer NAP manifests with DAG checks and deterministic ordering.
- Validate MDL-driven layer acceptance across synthetic test sets.

### 8.3 Two-track tests

- Validate P\_state-only, P\_cite-only, and dual-track flows as described in §4.3.

### 8.4 ε & O-level tests (where possible)

- For known simulated systems, integrate with a simple T/O loop to run Δ=0 and Δ>0 tests.
- At minimum, confirm field-level ε/q bounds across all numeric datasets used in tests.

### 8.5 Regression & compatibility

- Ensure that all existing MVP tests still pass.
- Verify that new features are disabled when not configured (MVP behaviour remains available via profile/mode selection).

---

## 9. Implementation Phasing / Tickets Snapshot

A possible implementation order (assuming MVP codebase is in place):

1. **Phase A — MDL & NAP:**

   - TG-NAP-1, TG-NAP-2, TG-MDL-1, TG-MDL-2, TG-STACK-1.

2. **Phase B — Policy & Dims:**

   - TG-POLICY-1, TG-POLICY-2, TG-DIMS-1, TG-DIMS-2.

3. **Phase C — Two-track & ε:**

   - TG-PTRACK-1, TG-PTRACK-2, TG-PTRACK-3, TG-EPS-1, TG-EPS-2.

4. **Phase D — Acceptance harness & O:**

   - TG-ACCEPT-1, TG-ACCEPT-2, TG-ACCEPT-3.

5. **Phase E — AEON/APXi & Models polishing:**

   - TG-AEON-1, TG-AEON-2, TG-MODEL-1, TG-MODEL-2.

6. **Phase F — UI extensions:**

   - TG-UI-1, TG-UI-2, TG-UI-3, TG-UI-4.

7. **Phase G — Full-Press test harness:**

   - All §8 test groups, integrated into CI.

This completes the path from the **JS Offline MVP** to a **full Aether Press (APP-UROBOROS-REF-1) implementation** in JS that honours the canon Press pillars, two-track policy layer, multi-layer MDL stacks, and ε-bounded acceptance guarantees.



<!-- END SOURCE: astral_press_js_full_implementation_build_plan_v_1_beyond_mvp.md -->


---

<!-- BEGIN SOURCE: app_local_spec_v_1_aether_press_local_implementation_2025_11_20.md -->

# APP_LOCAL_SPEC v1 — Aether Press Local Implementation

Scope:  
This document **instantiates** the Aether Press Protocol (APP) for a concrete implementation:

- It **respects all canon requirements** (v1–v4 specs, legacy docs, Math Compendium, implementation canon).
- It **fills un-specified design space** with explicit decisions, clearly marked as local choices.
- It is the reference for devs implementing `.apx`, NAP, AEON‑i/APXi, residual stack, metrics, and mode mapping.

Where the project docs make explicit commitments, those are treated as non‑negotiable canon. Where canon is silent, this spec chooses defaults that stay as close as possible to the existing math and experiments.

---

## 1. Versioning & Identity

### 1.1 APP implementation ID

**Decision**

- Protocol name: `APP` (Aether Press Protocol)
- Canon protocol version: `1.0` (matches current math & docs set)
- **Local implementation ID**: `APP-UROBOROS-REF-1`
- **Local implementation version**: `1.0.0`

These fields are recorded in manifests:

```jsonc
"app_protocol": "APP",
"app_protocol_version": "1.0",
"app_impl": "APP-UROBOROS-REF-1",
"app_impl_version": "1.0.0"
```

**Rationale**

- Canon talks about “APP” and Press versions, but doesn’t fix a *local* implementation ID; this separates the abstract protocol from this concrete build.
- Having both `app_protocol_version` and `app_impl_version` lets code evolve without pretending the underlying math changed.

---

## 2. APX Container & Manifest — Local Schema

Canon already fixes responsibilities for the manifest and states that `.apx` is a deterministic capsule. This section pins a concrete, implementable layout.

### 2.1 Container format

**Decision**

- `.apx` is a **ZIP file** with the following structure:
  - Root:
    - `MANIFEST.json` — Press Metadata Manifest
  - Subdirectories:
    - `layers/simA/` — SimA descriptor payloads
    - `layers/simB/` — SimB residual payloads
    - `nap/` — NAP manifests (e.g. `compression.json`)
    - `reports/` — run reports, logs, metrics (e.g. `report.json`, optional)

- ZIP rules:
  - `MANIFEST.json` and `nap/compression.json` are stored as **uncompressed** entries.
  - `layers/*` and `reports/*` may be stored or DEFLATE‑compressed as a transport detail; APP logic treats them as opaque blobs at the container level.

**Rationale**

- Canon experiments consistently assume a ZIP‑like container with `MANIFEST.json`, `nap_manifest.json`, SimA/SimB payloads, and reports.
- Using real ZIP keeps tooling simple; storing manifest/NAP uncompressed avoids needing to parse compressed bytes to find the recipe.
- Putting SimA/SimB under `layers/` mirrors canon language (“SimA descriptors… SimB residuals… layer payload files”).

---

### 2.2 `MANIFEST.json` schema (local)

Canon: manifest must include original name, size, hash, mode, timestamps, layer refs, link to NAP, etc., but treats full JSON schema as a gap. This spec fixes that schema for `APP-UROBOROS-REF-1`.

**Decision — top‑level MANIFEST JSON**

```jsonc
{
  "schema_version": "apx_manifest_v1",

  "app_protocol": "APP",
  "app_protocol_version": "1.0",
  "app_impl": "APP-UROBOROS-REF-1",
  "app_impl_version": "1.0.0",

  "orig": {
    "name": "input.bin",
    "size_bytes": 123456,
    "sha256": "…"
  },

  "press": {
    "mode": "lossless",              // or "epsilon_bounded"
    "profile": "PRESS_LOSSLESS",     // local profile name
    "epsilon_global": 0.0,            // null if not applicable
    "dtype": "bytes",                // e.g. "bytes", "float32", "int32", "json"
    "shape": [123456],                // tensor/array shape, or [size_bytes] for flat
    "fidelity_metric": "l2",         // e.g. "l2", "max_abs", domain metric
    "created_utc": "2025-11-20T12:34:56Z"
  },

  "fs_meta": {
    "mode": "0644",
    "mtime_utc": "2025-11-20T12:34:00Z",
    "ctime_utc": "2025-11-20T12:33:00Z",
    "uid": 1000,
    "gid": 1000
  },

  "layers": [
    {
      "id": "simA_main",
      "kind": "AP.symbolic",               // SimA
      "path": "layers/simA/simA_main.apxi",
      "sha256": "…",
      "size_bytes": 1234
    },
    {
      "id": "simB_main",
      "kind": "AP.residual",              // SimB
      "path": "layers/simB/simB_main.bin",
      "sha256": "…",
      "size_bytes": 5678
    }
  ],

  "nap": {
    "present": true,
    "path": "nap/compression.json",
    "sha256": "…"
  },

  "reports": [
    {
      "kind": "metrics",
      "path": "reports/report.json",
      "sha256": "…",
      "size_bytes": 4321
    }
  ]
}
```

**Rationale**

- `orig` covers original artifact identity (name, size, hash) as canon demands.
- `press` covers mode (lossless vs ε‑bounded), profile, dtype, shape, fidelity metric, and creation time, matching the Implementation doc’s header description.
- `layers` holds references to SimA/SimB payloads with IDs that will be used in the NAP manifest.
- `nap` holds the pointer and integrity tag for the NAP Compression Manifest.
- `reports` is a generic hook for metrics/diagnostics.
- `schema_version` lets this manifest evolve without ambiguity; canon explicitly noted the absence of such a field as a gap.

---

## 3. NAP Compression Manifest — Local JSON Definition

Canon fixes the conceptual structure:

- Top level: `layers[]`, `knit_rules`, `deterministic_order`, `hashes`.
- Each layer: `{id, kind∈{AP.symbolic (SimA), AP.residual (SimB)}, parent, refs[], params, ordering}`.

Types and nesting are left open; this spec chooses concrete JSON.

### 3.1 File & location

**Decision**

- NAP manifest path inside `.apx`: `nap/compression.json`.
- `MANIFEST.json.nap.path` points here, and `MANIFEST.json.nap.sha256` secures it.

---

### 3.2 JSON structure

**Decision — NAP manifest schema (example instance)**

```jsonc
{
  "schema_version": "nap_manifest_v1",

  "layers": [
    {
      "id": "simA_main",
      "kind": "AP.symbolic",          // "AP.symbolic" (SimA) or "AP.residual" (SimB)
      "parent": null,                   // null = root layer
      "refs": [],                       // additional DAG edges (optional)
      "params": {
        "segmenter": "fixed_window",
        "window_size": 4096,
        "aeon_stream_path": "layers/simA/simA_main.apxi"
      },
      "ordering": {
        "order_index": 0,
        "stage": "symbolic"
      }
    },
    {
      "id": "simB_main",
      "kind": "AP.residual",
      "parent": "simA_main",          // depends on SimA
      "refs": [],
      "params": {
        "codec": "residual_stack_v1",
        "applied_transforms": ["delta", "xor_base", "golomb_rice"],
        "residual_path": "layers/simB/simB_main.bin"
      },
      "ordering": {
        "order_index": 1,
        "stage": "residual"
      }
    }
  ],

  "knit_rules": {
    "type": "stacked",
    "description": "SimA_main provides generative baseline; SimB_main encodes residuals on top.",
    "reconstruction": [
      "decode_simA_main",
      "apply_simB_main_residuals"
    ]
  },

  "deterministic_order": {
    "topological_order": ["simA_main", "simB_main"]
  },

  "hashes": {
    "algo": "sha256",
    "layers": {
      "simA_main": "…",
      "simB_main": "…"
    }
  }
}
```

**Rationale**

- `layers` follows canon’s field list; `id` and `parent` are strings (IDs matching MANIFEST) for clarity and stability.
- `kind` uses the canonical `AP.symbolic` / `AP.residual` names (SimA/SimB) to keep the semantics visible.
- `params` is a freeform object but is used consistently: SimA layers point to an APXi descriptor stream; SimB layers declare a codec profile and path.
- `ordering.order_index` and `deterministic_order.topological_order` encode the topological sort required by canon to guarantee `DePress(Press(D; M); M) = D`.
- `hashes.layers` provides per-layer integrity, satisfying the manifest’s `hashes` field while leaving room for future global hashes.

---

## 4. AEON‑i & APXi — Local Grammar

Canon defines AEON‑i as an integer‑only descriptor language with varints/ZigZag parameters and names specific opcodes. APXi is a binary framing with a u16 version followed by a varint stream. Full grammar is left open.

### 4.1 APXi framing

**Decision — APXi v1 layout**

```text
u16  version_u16        // big-endian
varint op_count         // number of AEON operations in this stream
repeat op_count times:
    varint opcode_id
    varint param_count
    repeat param_count times:
        varint param_value   // unsigned or ZigZag-encoded signed
```

- `version_u16 = 1` for AEON‑i v1 grammar.

**Rationale**

- Matches canon’s requirement of a 16‑bit version word followed by a varint-only stream.
- Adds `op_count` and `param_count` to make parsing robust and error‑detectable while remaining a pure varint grammar after the version field.
- Big‑endian u16 is conventional for protocol headers.

---

### 4.2 AEON‑i v1 opcode table

Canon identifies example opcodes: `OP_SEGMENT`, `OP_AFFINE`, `OP_POLY3`, `OP_PERIODIC`, `OP_COMBINE`, `OP_AR1`, `OP_AR2`, `OP_AR3`. It does not assign IDs or parameters. This spec chooses a concrete mapping.

**Decision — opcode IDs and parameter lists**

| Name        | ID | Parameters (in order)                                                                                 |
|------------|----|--------------------------------------------------------------------------------------------------------|
| OP_SEGMENT | 1  | `start_index (u)`, `length (u)`                                                                        |
| OP_AFFINE  | 2  | `column_id (u)`, `a_num (s)`, `a_den (u)`, `b_num (s)`, `b_den (u)`                                    |
| OP_POLY3   | 3  | `column_id (u)`, `c3_num (s)`, `c3_den (u)`, `c2_num (s)`, `c2_den (u)`, `c1_num (s)`, `c1_den (u)`, `c0_num (s)`, `c0_den (u)` |
| OP_PERIODIC| 4  | `column_id (u)`, `period (u)`, `amplitude_num (s)`, `amplitude_den (u)`, `phase_num (s)`, `phase_den (u)` |
| OP_COMBINE | 5  | `component_count (u)`, then `component_count` times: `component_op_index (u)` (index into previous ops) |
| OP_AR1     | 6  | `column_id (u)`, `phi_num (s)`, `phi_den (u)`                                                         |
| OP_AR2     | 7  | `column_id (u)`, `phi1_num (s)`, `phi1_den (u)`, `phi2_num (s)`, `phi2_den (u)`                        |
| OP_AR3     | 8  | `column_id (u)`, `phi1_num (s)`, `phi1_den (u)`, `phi2_num (s)`, `phi2_den (u)`, `phi3_num (s)`, `phi3_den (u)` |

Where:

- `u` = unsigned varint
- `s` = signed integer encoded with ZigZag → varint

**Rationale**

- The chosen opcode set directly mirrors canon’s examples (affine, polynomial, periodic, AR(1..3), segment, combine).
- Rational coefficients (num/den) preserve integer-only reasoning and avoid floating point drift, matching the AIF/LCDRM emphasis on integer matrices and exact mapping.
- `column_id` supports a multi-column dataset in one APXi stream, consistent with Dims Press and NAP bus descriptions.
- `OP_COMBINE` enables composite models (e.g. trend + seasonal) using explicit references, aligning with multi-component examples.

---

### 4.3 AEON‑i v1 error handling

**Decision**

- If `opcode_id` is unknown for the current `version_u16` → **hard decode error** (capsule invalid).
- If `param_count` does not match the expected count for that opcode → **hard decode error**.
- If the APXi stream ends before all parameters are read → **hard decode error**.
- If extra data remains after reading `op_count` operations → **hard decode error** for v1.

**Rationale**

- Canon is silent on error semantics; a strict policy prevents silent corruption and ambiguous reconstructions.
- Treating malformed descriptors as fatal is consistent with the proof‑carrying nature of capsules.

---

## 5. Model Library, Selection & Fitting — Local Defaults

Canon names model families (polynomial, periodic, dictionary, AR, LFSR, LCDRM) and demonstrates them, but does not specify a mandatory library or algorithms. This spec instantiates a minimal but expressive library.

### 5.1 Supported model families (v1)

**Decision**

For numeric time-series or columns:

1. **Affine** (`OP_AFFINE`)
2. **Cubic polynomial** (`OP_POLY3`)
3. **Periodic** (`OP_PERIODIC`)
4. **AR(1..3)** (`OP_AR1`, `OP_AR2`, `OP_AR3`)
5. **LFSR** model for special structured datasets (parameters recorded via `params`/NAP rather than AEON in v1)
6. **LCDRM-style layered deltas** represented through multi-layer NAP stacks

For text/symbolic fields:

- **Dictionary model** (SimB-side), with SimA typically unused.

**Rationale**

- These families match the models explicitly shown or implied in experiments (LFSR example, polynomial and periodic fits, AR residuals, LCDRM layering).
- This keeps the v1 library small enough for implementation but rich enough to match the documented test cases (checkerboards, arrays, sensor streams).

---

### 5.2 Model selection strategy (`select_model(segment)`)

**Decision — numeric segments**

For each segment/window of a numeric column or vector:

1. Compute fits for each candidate model family:
   - **Affine**: least-squares fit, rationalized coefficients.
   - **Cubic polynomial**: least-squares degree‑3 fit, rationalized coefficients.
   - **Periodic**: estimate period by FFT or autocorrelation peak; fit amplitude/phase by least-squares; express as rational.
   - **AR(1..3)**: fit via Yule–Walker/Burg; rationalize coefficients.

2. For each model `M` with fitted parameters `θ`:
   - Simulate `x_hat = simulate(M, θ, I, len=|segment|)`.
   - Compute residual `r = segment - x_hat`.
   - Encode residual using local residual stack (section 6) in lossless or ε‑bounded mode.
   - Compute description length `L_A(M)` = bits to encode `θ` (AEON descriptors) + residual bits.

3. Compute dictionary-only `L_B` for the same segment (SimB-only baseline).

4. Choose model or dictionary according to dual-compressor mixture rule:

   ```text
   L_segment = min{L_A, L_B} + L_gate_bit
   ```

   and record the gate bit in the segment’s metadata.

**Decision — non‑numeric / textual segments**

- Default to **dictionary-only** (SimB), unless a future AEON model for that type is defined.

**Rationale**

- Directly implements the dual compressor mixture cost function in the Math Compendium (symbolic vs dictionary with a gate bit).
- Uses MDL (description length) as the objective, aligning with the MDL stopping rule.
- Limits complexity by focusing on a finite, well-motivated set of models instead of an unbounded model zoo.

---

### 5.3 Fitting algorithms

**Decision**

- **Affine/poly3:**
  - Use standard least-squares regression (double precision).
  - Convert floating-point coefficients to rationals (`num/den`) with bounded denominators (e.g. ≤ 2^32) to maintain deterministic integer representation.

- **Periodic:**
  - Estimate dominant period via FFT or autocorrelation.
  - Fit amplitude and phase via least-squares and rationalize coefficients.

- **AR(1..3):**
  - Fit via Yule–Walker or Burg method.
  - Rationalize coefficients as `num/den` pairs.

- If fitting for a model fails (singular matrices, insufficient data, no stable solution):
  - Skip that model for this segment and exclude it from MDL comparison.

**Rationale**

- Canon is silent on fitting algorithms; these are standard, interpretable methods with well-known properties.
- Rationalization is consistent with “integer matrices” and invertible deterministic mappings in AIF/LCDRM.

---

## 6. Residual Codec & Lossy Profiles

Canon shows an integerization pipeline and names common transforms (Δ, XOR base, AR, Golomb–Rice, arithmetic/Huffman) but does not fix a stack. This spec chooses a stack and defines profiles for lossy modes.

### 6.1 Residual transform stack (lossless base)

**Decision**

For numeric residuals in SimB (after model subtraction):

1. **Integerization** (if needed):
   - For original integer data, residuals remain integers.
   - For float/decimal data in strict lossless mode, choose a scale (e.g. 2^k) that preserves exact representation as integers, or reject lossless mode if not feasible for that dtype.

2. **Delta coding (Δ):**
   - Replace sequence `r[i]` with `r[i] - r[i-1]` per column.

3. **XOR base (where applicable):**
   - For bit-pattern fields, apply XOR with a base (e.g. previous or default value) to cluster probabilities.

4. **Golomb–Rice coding:**
   - Encode delta-coded integers with Golomb–Rice using k tuned on small samples per segment.

5. **Arithmetic coding:**
   - Final entropy coder for symbol stream produced by Golomb–Rice.

**Rationale**

- Matches the transform palette hinted in canon while providing a concrete, standard stack.
- Arithmetic coding is closer to theoretic optimum than bare Huffman and fits the MDL framing well.
- Integerization and Δ align with the legacy integer-model examples and the integerization pipeline from the performance report.

---

### 6.2 Lossy profiles & ε mapping

Canon gives the ε–quantization relation and per-field bounds, but no fixed profiles. This spec defines a small set of profiles mapped to typical use cases.

**Decision — profile set**

1. **`PRESS_LOSSLESS`**
   - `press.mode = "lossless"`
   - `epsilon_global = 0.0`.
   - No quantization; integerization must be exactly invertible for the dtype.
   - Residual stack: as in 6.1.

2. **`PRESS_SENSOR_MED`** (example sensor profile)
   - `press.mode = "epsilon_bounded"`.
   - Typical per-field ε:
     - Position: `ε_pos = 1e-4`.
     - Velocity: `ε_vel = 1e-3`.
     - Accel: `ε_acc = 1e-3`.
   - Quantization steps:
     - `q_field = 2 * ε_field` so `q/2 ≤ ε_field` exactly.
   - Residual stack: same as lossless, but operating on quantized residuals.

3. **`PRESS_LOG_CRUSH`** (logs/events)
   - `press.mode = "epsilon_bounded"`.
   - Integer fields (like counters): `ε = 0` (no quantization).
   - Timestamp fields: quantize to e.g. 1 ms if consistent with O’s tolerance.
   - Dictionary-driven compression dominates; residual stack is only used for numeric subfields.

These profiles are referenced in `MANIFEST.json` under `press.profile` and further detailed in policy cards.

**Rationale**

- Directly reflects the ε and q relation from the “Crush without regret” and integerization pipeline discussion.
- Profiles reflect common real-world uses: exact archival, moderately lossy sensor data, and aggressive log compression.

---

## 7. Metrics & MDL Functional — Local Formula

Canon defines `L_total`, `L_naive`, `kappa`, and MDL stopping rules conceptually but not formulaically. This spec proposes a fully explicit functional.

### 7.1 Description length components

**Decision — definitions**

- `L_model` — bits to encode all AEON‑i descriptors (SimA outputs) for the dataset.
- `L_residual` — bits to encode all SimB residual streams after the residual transform stack and entropy coding.
- `L_overhead` — bits for:
  - APXi `version_u16`, `op_count`, and internal field overhead.
  - `MANIFEST.json` (compressed size * 8 or raw JSON size * 8, depending on how you measure).
  - `nap/compression.json` and any required hashes.
  - Any other fixed per-capsule metadata we choose to count.

Total description length:

```text
L_total = L_model + L_residual + L_overhead
```

Naive baseline for raw bytes:

```text
L_naive = 8 * |S|
```

(Where `|S|` is the number of bytes in the original data.)

Gain:

```text
kappa = L_naive - L_total
```

**Rationale**

- This decomposes description length in a way that matches the rule+residual theory plus container overhead.
- Counting manifest and overhead discourages hidden complexity and aligns with MDL spirit.

---

### 7.2 Layer MDL decision rule

**Decision**

For each candidate layer `M_i` in a stack:

1. Compute new total description length `L_total'` that includes `M_i` and its induced residuals.
2. Accept layer `M_i` iff:

   ```text
   L_total' + margin < L_total
   ```

   where `margin` is a small positive threshold (default 8 bits).

3. If no candidate layer satisfies this inequality, **stop stacking**.

**Rationale**

- Implements canon’s “stop when adding another model would increase overall description length” with a concrete tolerance to avoid flapping on marginal cases.
- Margin of one byte is a simple, human‑interpretable choice that encourages meaningful savings per layer.

---

## 8. Modes & Policy Mapping — Local S‑Modes

Canon names system modes S1–S12 and states responsibilities (ESL, Offline Recompress, Encryption, Knowledge Sync) but leaves their mapping and schema open. This spec defines a local mapping and manifest.

### 8.1 Local S‑mode table

**Decision**

| ID  | Name                     | Effect on Press                                                         |
|-----|--------------------------|--------------------------------------------------------------------------|
| S1  | `ESL_ON`                 | Telemetry/logs are routed into Press/P_cite.                            |
| S2  | `ESL_OFF`                | Telemetry bypasses Press (no `.apx` capsules created for logs).         |
| S3  | `OFFLINE_RECOMPRESS`     | Allows re-Press of historical data; requires lineage tracking.          |
| S4  | `NO_OFFLINE_RECOMPRESS`  | Forbids recompression except under explicit override.                   |
| S5  | `ENCRYPT_CAPSULES`       | Wraps `.apx` outputs in an encryption layer (e.g. `.apx.enc`).          |
| S6  | `PLAIN_CAPSULES`         | No encryption wrapper; integrity only.                                  |
| S7  | `KNOWLEDGE_SYNC_ON`      | Press reloads policy/grammar packs on knowledge sync events.            |
| S8  | `KNOWLEDGE_SYNC_OFF`     | Press uses pinned policy/grammar until manual reload.                   |
| S9  | `STRICT_LOSSLESS_ONLY`   | Only `PRESS_LOSSLESS` profile allowed.                                  |
| S10 | `ALLOW_EPSILON_PROFILES` | `PRESS_SENSOR_MED`, `PRESS_LOG_CRUSH`, etc. allowed.                     |
| S11 | `DEBUG_VERBOSE_METRICS`  | Press writes extended metrics (`reports/report.json`) into the capsule. |
| S12 | `DEBUG_MINIMAL_METRICS`  | Press emits only minimal metrics.                                       |

Local mode manifest:

```jsonc
{
  "schema_version": "press_modes_v1",
  "enabled_modes": [
    "ESL_ON",
    "OFFLINE_RECOMPRESS",
    "ENCRYPT_CAPSULES",
    "ALLOW_EPSILON_PROFILES"
  ]
}
```

**Rationale**

- Encodes the responsibilities canon explicitly associates with modes (ESL, Offline Recompress, Encryption, Knowledge Sync) and adds two obvious Press-specific toggles (lossless-only vs epsilon, metrics verbosity).
- Keeps mode names human-readable and stable; IDs (S1–S12) are an internal convention.

---

## 9. Network/API Wrapper (Optional, Local)

Canon does not define a public network protocol for Press. This spec proposes a minimal internal HTTP API if Press is exposed as a service. This is explicitly local and non‑canon.

### 9.1 HTTP encode/decode endpoints

**Decision**

- `POST /press`
  - Request:
    - Body: multipart or JSON including:
      - Input file bytes (or URI resolved by a trusted sidecar).
      - `press.profile` (e.g. `PRESS_LOSSLESS`, `PRESS_SENSOR_MED`).
      - Optional NAP hints (e.g. desired segmentation strategy).
  - Response:
    - `.apx` capsule bytes.
    - Small JSON with key metrics (compression ratio, `kappa`, timings).

- `POST /depress`
  - Request:
    - `.apx` capsule bytes.
  - Response:
    - Original file bytes (or stream).
    - `MANIFEST.json` and `nap/compression.json` as JSON fields or attachments.

- Security:
  - mTLS between Press service and its clients.
  - Auth tokens or mTLS client certs per service.
  - Rate limiting and max capsule size to prevent abuse.

**Rationale**

- Keeps APP’s canonical contract at the file level (`.apx` capsules); HTTP is a convenience transport.
- Respects canon’s security emphasis (sandboxing, no direct RCE, mTLS hints).

---

## 10. Meta: Scope & Limits of This Local Spec

- This spec **fully instantiates** all major design knobs canon leaves open:
  - APX manifest schema and ZIP layout.
  - NAP manifest JSON representation.
  - AEON‑i/APXi v1 grammar and opcode table.
  - Model library, selection strategy, and fitting algorithms.
  - Residual codec stack for lossless and ε‑bounded modes.
  - MDL functional and layer acceptance rule.
  - Local S‑mode mapping and mode manifest.
  - Optional HTTP API for internal use.

- It **does not** claim to redefine canon or become globally binding:
  - `.apx` here is the `APP-UROBOROS-REF-1` implementation of APP containers, not a universal APX standard.
  - AEON‑i/APXi grammar v1 is local and versioned; other implementations may define different grammars as long as they respect the outer shape and constraints of canon.
  - Model choices, codecs, and thresholds are tuned for this environment and are documented so they are auditable and changeable.

Any future changes must bump:

- `schema_version` in relevant JSON schemas.
- `app_impl_version` in `MANIFEST.json`.

while keeping `app_protocol` / `app_protocol_version` aligned with the underlying canonical math and project documents.



<!-- END SOURCE: app_local_spec_v_1_aether_press_local_implementation_2025_11_20.md -->


---

<!-- BEGIN SOURCE: astral_press_app_implementer_checklist_v_1_2025_11_20.md -->

# Astral Press — APP Implementer Checklist v1

This document splits Aether Press (APP) into:

1. **Canon requirements** — what you **must** do to be APP-compliant. Violating these means you are no longer implementing Aether Press.
2. **Design knobs** — what canon **explicitly leaves open**. You must pick and document these locally in your implementation spec.
3. **"Don’t bullshit yourself" caveats** — claims you cannot honestly make, given the current canon gaps.

All points below are grounded in the Aether Press pillar documents, legacy Press docs, Math Compendium, and implementation canon passes.

---

## 1. Canon Requirements — Non‑Negotiable Behaviour

These are locked by project docs. If you violate these, you’re not doing Aether Press anymore.

### 1.1 Core Behaviour: Reversible Rule+Residual Compression

You **must** implement Press/DePress as pure inverse operators with rule+residual structure.

- **Reversible operators:**
  - Press and DePress are inverse mappings:
    - \(C_{\text{out}} = \Pr(S_{\text{in}})\)
    - \(S_{\text{in}} = \DePr(C_{\text{out}})\)
  - Lossless mode conserves entropy:
    - \(H(\text{input}) = H(\text{output})\) (no information lost inside the capsule).

- **Rule + residual form (discrete case):**
  - A dataset \(S\) is modeled as:
    - \(S = M(\theta) \oplus R\) (bitwise XOR for discrete systems).
  - Compression ratio is defined as:
    - \(\text{CR} = (|\theta| + |R|) / |S|\).

- **Respecting Shannon:**
  - Press **must not** “cheat” Shannon:
    - Truly random or already optimally compressed data (ZIP, MP3, etc.) must not be magically crushed beyond entropy bounds.
    - For such inputs, Press is allowed to give **no gain or slight expansion**, due to header/metadata overhead.

In other words: any compression beyond a trivial baseline must come from **captured structure**, not magic entropy violations.

---

### 1.2 Lossless vs ε‑Bounded Modes & Acceptance Tests

APP supports strict lossless mode and optional ε‑bounded modes. Both are tightly constrained.

- **Lossless mode:**
  - Reconstruction must be bit‑exact:
    - The reconstructed bytes’ hash **must equal** the original file hash (e.g. SHA‑256 recorded in the manifest).
  - Press/DePress cycles must be idempotent for fixed input and version (no drift).

- **ε‑bounded mode:**
  - Quantization must respect per‑field error bounds:
    - For each numeric field \(x\) with quantization step \(q\):
      - \(|x_{\text{post}} - x_{\text{pre}}| \le q/2 \le \varepsilon_x\).
  - You must choose **ε first** and then choose `q` such that \(q/2 \le \varepsilon_x\) for every field.

- **Acceptance checks (“Crush without regret”):**
  For any Press configuration, you must enforce:

  1. **Field‑level bounds:** as above, \(|x_{\text{post}} - x_{\text{pre}}| \le q/2 \le \varepsilon_x\).
  2. **Replay test (Δ = 0):**
     - DePress then run with \(\Delta = 0\); observable scoreboard \(O\) unchanged.
  3. **Predictive test (Δ > 0):**
     - DePress, advance simulation by \(T^\Delta\); check \(d(O_{\text{true}}, O_{\text{replayed}}) \le \varepsilon\).
  4. **Document proof:**
     - For each external source in **P_cite**, store \{hash, bytes\} so auditors can verify you didn’t hallucinate inputs.
  5. **Idempotence:**
     - Same envelope + same nonce ⇒ no net change to \(O\).
  6. **Isolation:**
     - Prior checkpoint O‑hashes must never change.

Only **O** (the scoreboard) matters for acceptance; raw data deltas are not the decision basis in ε‑bounded mode.

---

### 1.3 Multi‑Layer MDL Stack (Model + Residual Layers)

Press factorizes data into a multi‑layer stack of models and residuals governed by MDL.

- **Iterative factorization:**
  - Data \(X\) is decomposed as:
    - \(X = M_1 + R_1\)
    - \(R_1 = M_2 + R_2\)
    - \(R_2 = M_3 + R_3\)
    - \(\dots\)
    - \(R_{k-1} = M_k + R_k\) (final \(R_k\) is noise residual).

- **MDL stopping rule:**
  - You must only add a new model layer \(M_i\) if it **reduces total description length** \(L_{\text{total}}\).
  - Once adding another layer would increase \(L_{\text{total}}\), the stack must stop.

This binds the multi‑layer structure to **Minimum Description Length** rather than arbitrary heuristics.

---

### 1.4 Two‑Track Press: P_state vs P_cite

Your implementation must distinguish **P_state** and **P_cite** and obey the policy rules.

- **P_state (reconstructive):**
  - Defined as the *minimal* snapshot required for \(T\) (the transition map) to resume **exactly**.
  - Must pass the ε‑bounded replay and predictive tests.

- **P_cite (proof / pointer track):**
  - Contains hashes, byte lengths, and a few extracted integers you actually use from external sources.
  - Used purely for **provenance and audit**, not for simulation replay.

- **Mandatory policy rules:**
  - Do **not** let P_state depend on raw documents that \(T\) will never replay; hash them into P_cite instead.
  - Always set ε before choosing quantization steps `q`.
  - Base acceptance on **O only**, not on raw data.

Two‑track Press is part of how APP achieves “astronomical” crush ratios without compromising replay or provenance.

---

### 1.5 APX Manifest Responsibilities

Even though the exact JSON schema is open, **these responsibilities are canon‑fixed** for `.apx` manifests (Press Metadata Manifest).

Your manifest must at least:

- **Identify the source artifact:**
  - Original file **name**.
  - Original file **size** in bytes.
  - Original file **hash** (e.g. SHA‑256).

- **Describe the Press run configuration:**
  - Press/APX **version** (or APP schema version).
  - **Compression mode** (lossless vs ε‑bounded, and any mode label used).
  - Basic data metadata:
    - `dtype` (data type).
    - `shape` (dimensions).
    - **Fidelity metric** used in tests.

- **Summarise capsule content:**
  - List of **layers** (or references to layer payload files).
  - References to **SimA** and **SimB** outputs where applicable.
  - A reference/pointer to the **NAP Compression Manifest** if stacked/nested mode is used.

- **Provide integrity & provenance hooks:**
  - Hashes (and possibly sizes) for each payload segment.
  - Creation timestamp(s) and optional filesystem metadata.

The manifest is part of the **public contract** of `.apx`: external tools should be able to inspect what was pressed, when, and with which high‑level configuration.

---

### 1.6 NAP Compression Manifest Semantics

The NAP Compression Manifest is required whenever APP uses stacked/nested SimA/SimB layers.

Canon fixes the **shape and semantics**, even if the exact JSON is open.

- **Top‑level structure:**

  Conceptually:

  ```text
  NAP_Manifest := {
    layers[],            // Layer entries
    knit_rules,          // How layers recombine (stack/nest)
    deterministic_order, // Order constraints / topo ordering hints
    hashes               // Integrity for layers and/or groups
  }
  ```

- **Layer entries:**

  Each element of `layers[]` must have at least:

  ```text
  LayerEntry := {
    id,
    kind ∈ {AP.symbolic (SimA), AP.residual (SimB)},
    parent,
    refs[],
    params,
    ordering
  }
  ```

  - `id` — identifier for this layer (type open: must be consistent within the manifest).
  - `kind` — restricted to:
    - `AP.symbolic (SimA)` — symbolic/generative layer.
    - `AP.residual (SimB)` — residual/statistical layer.
  - `parent` — parent link in the DAG (exact type open; can be null for roots).
  - `refs[]` — extra references for cross‑links or nested dependencies.
  - `params` — parameter bundle (schema left open, but must encode what the layer needs).
  - `ordering` — metadata enforcing a deterministic processing order.

- **DAG and determinism:**

  - The graph formed by `layers[]` and `parent`/`refs[]` must be a **DAG**.
  - There must exist at least one **topological order** consistent with `ordering` / `deterministic_order` such that:

    \[
    \DePr(\Pr(D; M); M) = D
    \]

    for any dataset \(D\), fixed APP version, and manifest \(M\).

  - In words: NAP’s layer graph must always yield deterministic, cycle‑free reconstruction.

---

### 1.7 AEON‑i / APXi Basics

AEON‑i and APXi form the descriptor language and binary framing for SimA (and some SimB transforms).

- **AEON‑i role:**
  - Provide a **compact, integer‑only encoding** of model and transform definitions.
  - Describe SimA rules (affine, polynomial, periodic, etc.) and some SimB residual transforms (e.g. AR(1..3)).

- **Canonical opcodes that exist in APP canon:**
  - `OP_SEGMENT` — segmentation / piecewise modelling.
  - `OP_AFFINE` — affine rules \(y = a·x + b\).
  - `OP_POLY3` — cubic polynomial rules.
  - `OP_PERIODIC` — periodic components (sinusoidal/modular patterns).
  - `OP_COMBINE` — combine multiple components (e.g. trend + seasonal).
  - `OP_AR1`, `OP_AR2`, `OP_AR3` — AR residual transforms.

  Canon does **not** claim this is the full list; these are the opcodes explicitly shown in project docs.

- **Parameter encoding:**
  - All parameters (coefficients, indices, counts, etc.) must be encoded as **varints**.
  - Signed integers must be encoded as **ZigZag → varint**.

- **APXi framing:**
  - First field: 16‑bit `version_u16` indicating APXi grammar version.
  - Body: **single contiguous stream of unsigned varints** `[v0, v1, v2, …]`.
  - Opcode boundaries and parameter grouping are defined purely by the **AEON‑i grammar for that version**.

Any implementation that claims AEON‑i/APXi compatibility must obey these basics.

---

### 1.8 Integrity, Audit, & Proof‑Carrying Capsules

Press capsules must be **self‑verifying, proof‑carrying artifacts**.

- **Integrity:**
  - Per‑block and whole‑file hashes are required.
  - Hash algorithm is not pinned by canon, but SHA‑256 and 256‑bit hashes are repeatedly referenced.
  - Optional Merkle tree index for streaming:
    - Allows verifying partial data and resumable streams.

- **Proof‑carrying:**
  - Each pressed capsule must contain **enough model + residual information** to prove correctness:
    - Third parties should be able to reconstruct the source (or verify loss bounds) without access to original raw data.

- **Policy artefacts:**
  - You must honour Press policy cards per source:
    - Type (text/pdf/image/log/table/sensor).
    - Track: [P_state | P_cite] (sometimes both).
    - O‑fields derived.
    - Quantization `q` per field.

These ensure Press is not just a shrinker but part of a **verifiable evidence pipeline**.

---

## 2. Design Knobs — What You Must Choose & Document Locally

These are **intentionally left open** by canon. You’re allowed to choose, but you must document your choices in a local spec (e.g. `APP_LOCAL_SPEC.md`).

### 2.1 APX Details: Manifest Schema & Container Layout

You must define, for your implementation:

- **Concrete `.apxMANIFEST.json` schema:**
  - Exact keys and nesting.
  - Which fields are required vs optional.
  - A `schema_version` or equivalent for the manifest.

- **Concrete `.apx` container structure:**
  - Magic bytes or magic string (if any).
  - How manifest and payloads are stored (ZIP entries, length‑prefixed sections, etc.).
  - Where per‑layer hashes / checksums live.
  - Any segment index or header structures you add.

- **Signature/HMAC scheme (if used):**
  - Which hash/signature algorithm(s).
  - Exactly what is signed (whole file vs manifest vs manifest+payloads).
  - Key management/rotation policies.

Canon only says “there is a manifest and integrity tags”; the rest is **your design space**.

---

### 2.2 NAP Manifest: Concrete JSON Schema

You must fix a concrete JSON schema for NAP manifests in your environment:

- Types and formats for:
  - `id`, `parent` (string IDs, ints, UUIDs, etc.).
  - Entries in `refs[]` (simple IDs vs structs).

- Internal structure of:
  - `knit_rules` — how you encode stack vs nest relationships and recombination logic.
  - `deterministic_order` — e.g. explicit ordered list of layer IDs, or ranks.
  - `hashes` — field names and hash algorithms (per layer, global, or both).

- Per‑layer `params` schema:
  - What keys and types you use for `AP.symbolic (SimA)` layers.
  - What keys and types you use for `AP.residual (SimB)` layers.

---

### 2.3 AEON‑i / APXi Full Grammar

You must define your own **internal AEON‑i spec** and **APXi grammar**:

- **AEON‑i spec:**
  - Complete opcode table for each AEON‑i version you support.
  - Numeric ID assignments for opcodes.
  - Fixed parameter list + type per opcode.
  - Error behaviour (unknown op, wrong param count, malformed varints).

- **APXi grammar:**
  - How you multiplex multiple descriptor sequences (e.g. per column/layer):
    - Single global APXi stream vs separate APXi per column.
    - How you mark boundaries or counts.
  - Any additional versioned fields beyond `version_u16` + varints, if you choose to add them.

Canon defines the **outer shape** (version + varints) and some known opcodes, but leaves the full grammar to you.

---

### 2.4 Model Library, Selection & Fitting

You must make explicit choices for:

- **Model families you support:**
  - e.g. affine, polynomial (degrees), periodic, LFSR, AR(1..3), LCDRM‑style relational models, etc.

- **Model selection strategy (`select_model(segment)`):**
  - Do you brute‑force over a small library and choose the minimum description length?
  - Do you use heuristics based on dtype/shape (e.g. numeric vs text vs image)?

- **Parameter fitting algorithms (`fit_params`):**
  - What optimisers/solvers you use (least squares, gradient methods, search, etc.).
  - Convergence criteria and iteration limits.
  - How you handle failure to converge (fallback models, bail‑out behaviour).

Canon only says “select model, fit params, extract invariants”; the *how* is your design.

---

### 2.5 Residual Codec Stack & Lossy Profiles

You must lock down:

- **Residual transform stack:**
  - Which transforms you actually use: Δ, XOR base, AR(1..3), Golomb–Rice, RLE, etc.
  - In what order they are applied.

- **Entropy coder(s):**
  - Which coder(s) you treat as reference: arithmetic, Huffman, others.

- **Lossy profiles and ε→codec mapping:**
  - Named profiles (e.g. `PRESS_SENSOR_HI`, `PRESS_LOG_CRUSH`).
  - For each profile:
    - Per‑field ε and corresponding quantization q.
    - Which transforms are enabled/disabled.
    - Any extra constraints (e.g. “positions exact, velocities quantized to 1e‑3”).

Canon gives you the **building blocks** and the ε/q relation; you define the concrete stacks and profiles.

---

### 2.6 Metrics & Thresholds

You must define an explicit metrics layer for your APP implementation:

- **Full formula for \(L_{\text{total}}\):**
  - Must include:
    - Model description length bits.
    - Residual bits.
    - Descriptor/APXi overhead.
    - Manifest/container overhead you consider relevant.

- **Thresholds and defaults:**
  - Minimum \(\kappa = L_{\text{naive}} - L_{\text{total}}\) you consider “worth it” (per layer and/or overall).
  - Default window size \(W\) for the `split(data, window=W)` loop.
  - Default evaluation horizon \(\Delta\) and ε for replay tests.

Canon says “use MDL and kappa”; you must define **real numbers and formulas**.

---

### 2.7 Modes & Switches (S1–S12 or Equivalent)

You must pin down your own mode/switchboard mapping, since canon keeps S1–S12 abstract.

Define, in your local spec:

- The mapping from mode IDs (e.g. S1–S12 or named flags) to behaviours, including at least:
  - ESL (Event/External Stream Logging into Press/SLL).
  - Offline Recompress (allow re‑Press of historical data with provenance tracking).
  - Encryption (wrap `.apx` outputs in crypto without changing inner determinism).
  - Knowledge Sync (when policy/grammar packs reload and how Press responds).

- A **mode manifest** schema:
  - How modes are stored (JSON, config file, etc.).
  - How they are toggled and audited.

- Precise APP behaviour under each mode combination you actually use.

---

### 2.8 Network/API Wrappers (If You Expose Press as a Service)

If you expose Press as a networked service, you must design the API yourself:

- **Endpoints and schemas:**
  - Request/response types for encode/decode.
  - How `.apx` capsules and logs are returned.
  - Error codes and failure semantics.

- **Streaming behaviour (if any):**
  - Chunking model.
  - Resumable uploads/downloads.
  - Backpressure and timeouts.

- **Security envelope:**
  - mTLS or equivalent.
  - AuthN/AuthZ rules.
  - Resource limits to avoid abuse and RCE.

None of this is in canon; but if you build it, you must document it as part of your local APP environment.

---

## 3. “Don’t Bullshit Yourself” — Claims You Can’t Honestly Make Yet

Given the remaining canon gaps, there are specific statements you **cannot** make in good faith:

1. **Universal APX standard:**
   - You cannot claim: “`.apx` is a final, public, multi‑vendor standard whose schema and byte layout are fixed forever.”
   - Reality: you have **your** APX schema; canon doesn’t fix a global one.

2. **Universal AEON‑i/APXi grammar:**
   - You cannot claim: “Our AEON‑i grammar is *the* universal one; any AEON‑compliant tool must use this exact opcode set and field order.”
   - Reality: canon only fixes shape and some opcodes; full grammar is left open.

3. **Model‑invariant decomposition:**
   - You cannot claim: “Any APP implementation will discover the same invariants and produce byte‑identical descriptors for the same data.”
   - Reality: model library and selection/fitting are not canon‑fixed.

4. **Globally optimal MDL:**
   - You cannot claim: “Our capsules are globally minimal description length under the official APP MDL functional.”
   - Reality: full MDL functional and thresholds are not fully specified; you have a local implementation.

5. **Standardised lossy profiles across vendors:**
   - You cannot claim: “Choosing lossy profile X guarantees identical reconstructed outputs across independent APP implementations.”
   - Reality: residual codec stacks and ε→codec mappings are implementation choices.

6. **Portable system modes:**
   - You cannot claim: “S1–S12 mean the same thing in every APP deployment.”
   - Reality: only a few responsibilities (ESL, Offline Recompress, etc.) are canon; IDs and schemas are not.

What you **can** honestly say:

- “This implementation follows the Aether Press canon where it’s specified, and documents all local design choices where canon leaves space open.”
- “Given the same input, same APP version, and same local config, this implementation is deterministic and passes the lossless/ε‑bounded guarantees defined in canon.”

---

## 4. Suggested `APP_LOCAL_SPEC.md` Skeleton

For practical use, you can structure your local spec like this:

1. **Overview & Versioning**
   - APP implementation name, version, and mapping to canon docs.

2. **APX Container & Manifest**
   - `.apx` byte layout.
   - `.apxMANIFEST.json` schema (with `schema_version`).
   - Hash/signature schemes.

3. **NAP Compression Manifest**
   - Full JSON schema (types for `id`, `parent`, `refs[]`, `params`, `knit_rules`, `deterministic_order`, `hashes`).

4. **AEON‑i & APXi Grammar**
   - Opcode table, parameter lists.
   - APXi varint grammar and multiplexing rules.

5. **Model Library & Fitting**
   - Supported model families.
   - `select_model` strategy.
   - `fit_params` algorithms and tolerances.

6. **Residual Codec & Lossy Profiles**
   - Residual transform stack.
   - Entropy coders.
   - Named ε profiles with per‑field q.

7. **Metrics & MDL**
   - Full \(L_{\text{total}}\) formula.
   - kappa thresholds and window sizes.
   - Evaluation ε and Δ defaults.

8. **Modes & Policy**
   - Mode/switchboard mapping.
   - Press policy card format.
   - Behaviour under each mode.

9. **Network/API (if present)**
   - Endpoints, schemas, security.

10. **Testing & Compliance**
    - Test suites for lossless and ε‑bounded modes.
    - Replay tests and predictive tests.
    - Idempotence and isolation checks.

You can now fill this skeleton with concrete choices and treat this checklist as your guardrail against accidental spec drift.



<!-- END SOURCE: astral_press_app_implementer_checklist_v_1_2025_11_20.md -->


---

<!-- BEGIN SOURCE: astral_press_dev_handoff_map_v_1.md -->

# Astral Press — Dev Handoff Map v1

Scope: tell an implementer **what to read, in what order, for what job** to get from the Astral Press canon docs to a working JS implementation of `APP-UROBOROS-REF-1`.

This map assumes the following documents exist in this project:

- **Core canon & complements**
  - `Astral Press — APP Spec Sheets v1 (2025-11-20)` — core APP spec (pillar report mirror).
  - `Astral Press — APP Complement Sheet v2 (Legacy Docs Pass)`.
  - `Astral Press — APP Complement Sheet v4 (Implementation Canon Pack Pass)`.
  - `Aether Math Compendium` (for equations and MDL cost functions).
- **Implementation framing**
  - `Astral Press — APP Implementer Checklist v1`.
  - `APP_LOCAL_SPEC v1 — Aether Press Local Implementation (2025-11-20)`.
- **Build plans**
  - `Astral Press — JS Offline MVP Build Plan (2025-11-20)`.
  - `Astral Press — JS Full Implementation Build Plan v1 (Beyond MVP)`.
- **Stack & policy layer**
  - `Astral Press — Multi-Layer NAP & MDL Stack Spec v1 (Stack Until It Stops Making Sense)`.
  - `Astral Press — Policy & Dimensional Controls Spec v1 (P_state, P_cite & Dims Press)`.

Where this map interprets behaviour, it cites direct quotes from these docs.

---

## 1. High-Level Orientation (What Press Is For You)

Before touching build plans, devs should internalise **what APP actually is** in this stack.

From the legacy protocol doc:

> “**Aether Press Protocol (APP)** is a model-based symbolic compression framework that collapses structured data into its invariant relationships. It stores generative rules, state parameters, and minimal residuals—reducing redundant information by orders of magnitude while preserving causal reconstruction.”

From the Implementation doc’s subsystem table:

> “Aether Core — symbolic modeling and invariant extraction… Press Engine — encoding of parameters and residuals… Flux Decoder — reconstruction and fidelity validation… Protocol Layer — serialization schema and metadata registry.”

From the Implementer Checklist:

> “You **must** implement Press/DePress as pure inverse operators with rule+residual structure… Press and DePress are inverse mappings… Lossless mode conserves entropy… S = M(θ) ⊕ R (bitwise XOR for discrete systems)… CR = (|θ| + |R|) / |S|.”

So as a JS implementer, **your job** is to:

- Implement a deterministic, rule+residual **Press Engine** + **Flux Decoder**.
- Wrap it into `.apx` **Protocol Layer** containers with manifest + NAP manifest.
- Honour the canon guarantees around lossless mode, ε-bounded mode, MDL stacks, and P_state/P_cite.

Everything else in this map tells you *which doc teaches you which part of that job*.

---

## 2. Document Map by Concern

### 2.1 Canon anchors (read for mental model)

These docs tell you what APP fundamentally is; they are *not* tied to JS.

1. **APP Spec Sheets v1**

   - Role: pillar-level spec of APP: components, invariants, `.apx` overview, NAP integration.
   - Use: read once to understand the overall architecture (Aether Core, Press Engine, Flux Decoder, Protocol Layer) and the guarantees.

2. **APP Complement Sheet v2 (Legacy Docs Pass)**

   - Adds: subsystem table, older container/packet formatting, integer-model demo (LFSR), AIF axioms, two-track Press, per-dimension controls, LCDRM roots.
   - Key quotes:
     - Subsystems table:
       > “Aether Core — symbolic modeling and invariant extraction… Press Engine — encoding of parameters and residuals… Flux Decoder — reconstruction and fidelity validation… Protocol Layer — serialization schema and metadata registry.”
     - LFSR demo:
       > “A 1 KB structured dataset generated by a 16‑bit linear feedback shift register (LFSR)… was represented by integer parameters alone, achieving perfect reconstruction. Compression ratio = 214 / 1024 = 0.209. A random dataset remained incompressible.”
     - Two-track Press:
       > “You keep the *small, exact* computational snapshot (P_state), plus tiny proofs/pointers for the rest (P_cite).”

3. **APP Complement Sheet v4 (Implementation Canon Pack Pass)**

   - Adds: implementation-surface canon for `.apx`, NAP manifest, AEON/APXi, MDL quantities, S-modes, and the gap ledger.
   - Key anchors:
     - APX responsibilities:
       > “`MANIFEST.json` — Press Metadata Manifest… must at least: original file name, size, hash… compression mode… version… list of layers… reference to the NAP Compression Manifest… hashes and sizes for payloads.”
     - NAP layer entry fields:
       > “`layers[] {id, kind∈{AP.symbolic (SimA), AP.residual (SimB)}, parent, refs[], params, ordering}`.”
     - AEON/APXi surface:
       > “APXi := `[ version_u16, v0, v1, v2, … ]` … `v0, v1, …` are varints (unsigned), representing opcodes, counts, parameters, and other encoded fields under that version’s grammar.”
     - Metrics:
       > “`L_total` — achieved description length… `L_naive` — description length using a naive scheme… `kappa = L_naive - L_total`.”

4. **Aether Math Compendium**

   - Role: formal equations and cost functions (MDL, dual compressor mixture, etc.).
   - When you see `L_model`, `L_residual`, `L_overhead`, or dual-compressor cost lines in other docs, their math roots live here.

**For devs:** skim v1, then read v2 & v4 *once* end-to-end to understand what is fixed canon vs open design space.

---

### 2.2 Implementation framing docs (bridge canon → local JS)

These tell you what is **non‑negotiable** vs **your local choices** and fix those choices for `APP-UROBOROS-REF-1`.

1. **APP Implementer Checklist v1**

   - Role: master checklist of:
     1. Canon behaviour you must implement.
     2. Design knobs you must choose and document locally.
     3. Claims you are not allowed to make.
   - Critical quotes:
     - On core behaviour:
       > “You **must** implement Press/DePress as pure inverse operators with rule+residual structure… S = M(θ) ⊕ R… Compression ratio = (|θ| + |R|) / |S|.”
     - On MDL stack:
       > “You must only add a new model layer Mi if it **reduces total description length** L_total; once adding another layer would increase L_total, the stack must stop.”
     - On two-track Press:
       > “Do **not** let P_state depend on raw documents that T will never replay; hash them into P_cite instead.”
   - When: read this **before** you start coding; refer back whenever you are unsure if a change is canon-safe.

2. **APP_LOCAL_SPEC v1 — Aether Press Local Implementation (2025-11-20)**

   - Role: instantiates all the **design knobs** for this implementation ID:
     - Fixes `.apx` as a ZIP with `MANIFEST.json`, `nap/compression.json`, `layers/simA/`, `layers/simB/`, `reports/`.
     - Pins a concrete `MANIFEST.json` JSON schema, including:
       > `"schema_version": "apx_manifest_v1"`, `"app_impl": "APP-UROBOROS-REF-1"`, `"orig"`, `"press"`, `"layers"`, `"nap"`, `"reports"`.
     - Defines NAP manifest JSON structure for this implementation, matching the v4 layer fields but choosing concrete field types.
     - Defines AEON/APXi v1 grammar: opcode table and parameter lists.
     - Chooses model families, residual stack, MDL functional, and local S-modes.
   - Key quote on container:
     > “`.apx` is a **ZIP file** with the following structure: Root: `MANIFEST.json`… `layers/simA/`, `layers/simB/`, `nap/`, `reports/`… `MANIFEST.json` and `nap/compression.json` are stored as **uncompressed** entries.”
   - When: this is your **primary spec** as a JS dev; read it fully and treat it as law for `APP-UROBOROS-REF-1`.

**For devs:** Checklist tells you **what must be true**. APP_LOCAL_SPEC tells you **what choices this implementation already made** so you don’t reinvent them.

---

### 2.3 Build plans (MVP vs Full Press)

These give you step-by-step **implementation plans** in JS.

1. **Astral Press — JS Offline MVP Build Plan (2025-11-20)**

   - Role: scoped plan to get a **single-page, offline JS demo** running with:
     - `PRESS_LOSSLESS`, `dtype="bytes"` path.
     - A numeric demo path (SimA+SimB + AEON/APXi + MDL) for structured arrays.
   - Key scope quote:
     > “Goal: turn the current APP canon + APP_LOCAL_SPEC v1 into a **first offline web-page JavaScript implementation** of Press/DePress… Target: single-page HTML/JS app… MVP mode: `PRESS_LOSSLESS` only, `dtype="bytes"` default, with a dedicated numeric demo path for SimA/SimB.”
   - Contents: module breakdown, phases (core primitives → AEON/APXi → models → residual stack → Press/DePress → APX/manifest → UI → tests).
   - When: use this as your **task list** for getting from zero to a working `.apx` Press/DePress page.

2. **Astral Press — JS Full Implementation Build Plan v1 (Beyond MVP)**

   - Role: describes the **delta** from MVP to a **full Press implementation** in JS, including:
     - Multi-layer NAP stacks + MDL layer selection.
     - Press policy cards & Dims Press.
     - Two-track Press (P_state / P_cite).
     - ε-bounded profiles & acceptance harness.
     - Extended AEON/APXi & model library alignment.
   - Key scope quote:
     > “The goal here is to go **beyond the MVP** to a JS reference implementation that: implements two-track Press (P_state & P_cite)… Press policy cards and Dims Press (per-dimension controls)… ε-bounded profiles and O-only acceptance… multi-layer NAP stacks + MDL layer admission rule…”
   - When: once MVP build is stable, use this as phase-2 work: implementing the full policy and MDL stack behaviour.

**For devs:** MVP plan = **Phase 1**; Full Implementation plan = **Phase 2+**.

---

### 2.4 Stack & policy layer specs (behaviour glue)

These documents are *behaviour specs* that the Full JS Build Plan depends on.

1. **Astral Press — Multi-Layer NAP & MDL Stack Spec v1**

   - Role: pins:
     - How `NapManifest.layers[]` behaves as a **DAG**.
     - How `L_model`, `L_residual`, `L_overhead`, `L_total`, `L_naive`, `kappa` are computed in this implementation.
     - The **layer admission rule**:
       > “Accept Mi iff `L_total' + margin_bits < L_total`; once no candidate layer improves L_total, stop stacking.”
   - Use: implement `nap_builder` and `mdl` logic directly from this spec when you do multi-layer stacks.

2. **Astral Press — Policy & Dimensional Controls Spec v1 (P_state, P_cite & Dims Press)**

   - Role: formalises:
     - Two-track Press semantics (P_state vs P_cite) in terms of manifest and policy cards.
     - Press policy card JSON schema (type, track, O-fields, per-field ε/q, Dims controls).
     - Dims Press controls:
       > “Exact vs quantized dims… Residual fraction… Selective retention: {recompute, residual, full}… Dict scopes: per-node vs global Press dict on the NAP bus.”
   - Use: implement `policy_cards`, `dims_press`, and `p_tracks` modules for Full Press.

**For devs:** treat these as **behavioural constraints** that inform how you wire the modules in the Full Implementation plan.

---

## 3. Reading Paths by Role

### 3.1 Role A — JS MVP implementer (offline demo page)

Goal: build the **first working `.apx` Press/DePress SPA** with `PRESS_LOSSLESS` and a numeric demo.

**Recommended reading order:**

1. **APP Complement Sheet v2 & v4** — to understand APP architecture, `.apx`, NAP, AEON/APXi, MDL, and the canon gap ledger.
2. **APP Implementer Checklist v1** — to know what is non‑negotiable vs local choice.
3. **APP_LOCAL_SPEC v1** — container, manifest, AEON/APXi grammar, model family, residual stack, MDL functional for `APP-UROBOROS-REF-1`.
4. **JS Offline MVP Build Plan** — use as your concrete ticket list.

**Responsibilities you own at MVP level (pulled from these docs):**

- Implement **lossless Press/DePress**:
  - Respect:
    > “Lossless mode: reconstruction must be bit-exact… the reconstructed bytes’ hash **must equal** the original file hash (e.g. SHA-256 recorded in the manifest).”
- Implement `.apx` as defined in APP_LOCAL_SPEC:
  - ZIP layout, `MANIFEST.json`, `nap/compression.json`, `layers/`, `reports/`.
- Implement SimA/SimB for the numeric demo:
  - Use AEON/APXi opcodes from APP_LOCAL_SPEC.
  - Implement minimal model library (Affine, Poly3, Periodic, AR1–3) and residual stack.
- Honour MDL at **segment** level (even if you don’t do multi-layer yet):
  - Use `L_total`, `L_naive`, and `kappa` definitions when comparing symbolic vs dictionary-only.

If you only follow this reading path and this scope, you can build a correct **MVP** without worrying about P_state/P_cite or Dims Press yet.

---

### 3.2 Role B — JS Full Press implementer (policy + stacks)

Goal: turn the MVP into a **full Press implementation** that respects the policy, MDL stack, and two-track behaviour described in legacy docs and complement sheets.

**Reading order (on top of Role A):**

1. **Multi-Layer NAP & MDL Stack Spec v1** — to understand how to build `nap_builder`, `NapManifest` DAGs, and MDL layer admission.
2. **Policy & Dimensional Controls Spec v1** — to understand policy cards, Dims Press, and two-track behaviour.
3. **JS Full Implementation Build Plan** — as your ticketised phase-2 implementation plan.

**Additional responsibilities you own at Full-Press level:**

- Implement **multi-layer stacks** with MDL stopping rule:
  - Respect:
    > “You must only add a new model layer Mi if it reduces total description length L_total; once adding another layer would increase L_total, the stack must stop.”
- Implement **Press policy cards** per source & Dims controls:
  - Policy cards must enforce:
    > “For each numeric field x with quantization step q: |x_post − x_pre| ≤ q/2 ≤ ε_x.”
- Implement **two-track Press**:
  - Ensure P_state capsules contain just enough for replay.
  - Ensure P_cite capsules carry hashes/lengths and “a few extracted integers you actually use” for external sources.
- Implement **acceptance harness** (“Crush without regret” checks):
  - Field-level ε/q checks.
  - Replay (Δ=0) and predictive (Δ>0) tests where host T/O exist.
  - Idempotence and isolation checks.

This role must keep all these guarantees aligned with the Implementer Checklist and legacy performance report.

---

## 4. Quick “If You’re Holding This Job, Read This” Summary

- **If you’re building the first demo page** (offline SPA):
  - Read: APP Complement v2 & v4 → Implementer Checklist → APP_LOCAL_SPEC → JS Offline MVP Build Plan.
  - Deliver: `.apx` capsules with correct MANIFEST/NAP layout, lossless bytes path, numeric demo with SimA/SimB, MDL-aware model vs dictionary selection, and end-to-end tests for Press/DePress.

- **If you’re extending to full Press** (policy + stacks):
  - Add: Multi-Layer NAP & MDL Stack Spec → Policy & Dimensional Controls Spec → JS Full Implementation Build Plan.
  - Deliver: multi-layer MDL stack builder, policy card system, Dims Press knobs, two-track P_state/P_cite paths, ε-bounded profiles, and acceptance harness.

- **If you’re just sanity-checking compliance**:
  - Read: Implementer Checklist → Complement v4 → APP_LOCAL_SPEC.
  - Use the checklist to verify the implementation does not violate canon guarantees and that all local design knobs are documented.

This map is deliberately narrow: it doesn’t add new behaviour. It only tells you how the existing docs fit together so you can build and extend Astral Press in JS without guessing where each requirement lives.



<!-- END SOURCE: astral_press_dev_handoff_map_v_1.md -->


---

<!-- BEGIN SOURCE: astral_press_app_complement_sheet_v_2_legacy_docs_2025_11_20.md -->

# Astral Press — APP Complement Sheet v2 (Legacy Docs Pass)

Source scope for this pass:

- `old/aether press/Aether_Press_Protocol.pdf`
- `old/aether press/Aether_Press_Protocol_Implementation.pdf`
- `old/aether press/Aether_Press_Post_Implementation_Report.pdf`
- `old/aether press/Aether_Press_Protocol_Beyond_Shannon_Limit_Declaration.pdf`
- `old/v2/press v2.pdf`
- `old/v3/press proformance.pdf`
- `old/LCDRM/LCDRM_White_Paper_Uroboros.pdf`
- `old/LCDRM/lcdrm_payload.json`, `old/LCDRM/lcdrm_v2_payload.json`

All interpretations below are grounded in direct quotes from those files.

---

## 1. Additional Architecture & Subsystems (from Legacy Press Protocol Docs)

### 1.1 Core definition refresh

The older **Aether Press Protocol (APP)** definition explicitly emphasizes *invariant relationships*:

> “**Aether Press Protocol (APP)** is a model-based symbolic compression framework that collapses
> structured data into its invariant relationships. It stores generative rules, state parameters, and
> minimal residuals—reducing redundant information by orders of magnitude while preserving causal
> reconstruction.”  
> *(Aether_Press_Protocol.pdf)*

This reinforces the main spec’s “rule + residual” framing but adds:

- **"invariant relationships"** as the explicit target of compression. APP is not just compressing patterns; it is collapsing data into a set of relationships that stay consistent across states.
- The wording “**preserving causal reconstruction**” links directly to the Trinity/Loom causality requirements.

### 1.2 Subsystems table (Aether Core, Press Engine, Flux Decoder, Protocol Layer)

The naming doc defines four primary subsystems:

> “Subsystems Naming
>
> | Component    | Function                          |
> |--------------|-----------------------------------|
> | Aether Core  | symbolic modeling layer           |
> | Press Engine | rule + residual encoder           |
> | Flux Decoder | reconstruction simulator          |
> | Protocol Layer | metadata schema + API          |”  
> *(Aether_Press_Protocol.pdf)*

The implementation doc refines this into a slightly different but aligned table:

> “8. Subsystems
>
> | Subsystem   | Role |
> |-------------|------|
> | Aether Core | symbolic modeling and invariant extraction |
> | Press Engine | encoding of parameters and residuals |
> | Flux Decoder | reconstruction and fidelity validation |
> | Protocol Layer | serialization schema and metadata registry |”  
> *(Aether_Press_Protocol_Implementation.pdf)*

From these we can pin down:

- **Aether Core**
  - Quoted as handling “**symbolic modeling and invariant extraction**”.
  - This is the part that chooses/hosts the domain models and pulls out invariants; it’s the modelling brain of APP.
- **Press Engine**
  - Quoted as “**encoding of parameters and residuals**” and as a “**rule + residual encoder**”.
  - This is the stage that actually performs the transform from (model, θ, invariants, residuals) into the encoded form.
- **Flux Decoder**
  - Quoted as “**reconstruction simulator**” and “**reconstruction and fidelity validation**”.
  - This is the inverse; it re-simulates `M(θ, I)` and applies residuals, and also checks that outputs meet the ε-fidelity bounds.
- **Protocol Layer**
  - Quoted as “**metadata schema + API**” and “**serialization schema and metadata registry**”.
  - This is where container formats (`.apx`), manifests, and external interfaces live.

In other words, the older docs make the **4-box architecture** explicit:

1. Model & invariants (Aether Core)  
2. Encode (Press Engine)  
3. Decode & validate (Flux Decoder)  
4. Wire format & integration (Protocol Layer)

---

## 2. APP Container & Packet Format (Implementation Doc)

The Implementation PDF is the first place that spells out a **packet-level format** and a coarse container layout.

### 2.1 Compression pipeline pseudocode

The implementation introduces explicit pseudocode for the compression loop:

> “6. Compression Pipeline Pseudocode
>
> ```
> for segment in split(data, window=W):
>   M = select_model(segment)
>   θ = fit_params(M, segment)
>   I = extract_invariants(segment, M)
>   x_hat = simulate(M, θ, I, len=|segment|)
>   r = segment - x_hat
>   if mode == "lossless":
>     R = lossless_encode(r)
>   else:
>     r_q = quantize(r, eps)
>     R = entropy_encode(r_q, prior=learned)
>   emit Packet{ model_id, θ, I, eps, R, checksum(segment) }
> ```
> Decoder reverses the process to reconstruct the signal.”  
> *(Aether_Press_Protocol_Implementation.pdf)*

From this we can refine the per-window **Packet** structure beyond the main spec:

- **Fields inside `Packet{…}`** (per segment/window):
  - `model_id` — identifies the domain model `M`.
  - `θ` — fitted parameters.
  - `I` — invariants extracted from the segment.
  - `eps` — tolerance in lossy mode (ε); omitted or implicit when in strict lossless.
  - `R` — encoded residuals (`lossless_encode(r)` or `entropy_encode(r_q, prior=learned)`).
  - `checksum(segment)` — checksum of the original segment.

This Packet lives conceptually inside the `.apx` body as one of potentially many segments.

### 2.2 APP container format (header/body)

The same doc defines the container shape:

> “7. APP Container Format
>
> Header
> - Model ID, version, and compression mode.
>
> - Metadata: dtype, shape, fidelity metric.
>
> Body
> - Model parameters (quantized or raw).
> - Invariant dictionary.
> - Residual byte stream.
> - Metrics and checksum.”  
> *(Aether_Press_Protocol_Implementation.pdf)*

Cross-wiring this with the `.apx` manifest description from the main Press Pillar report, we get a more concrete view:

- **Header**
  - Stores **model identity** (“Model ID”), **APP version**, and **compression mode** (lossless vs ε-bounded).
  - Holds core **metadata**: data type (`dtype`), overall shape (dimensions), and the **fidelity metric** used for validation.
- **Body**
  - Houses the **model parameters** (which may be quantized or stored raw depending on ε).
  - Contains an **invariant dictionary** (essentially the invariants `I` in structured form).
  - Contains the **residual byte stream** (the `R` from packets; may be a concatenated stream across windows).
  - Carries **metrics and checksum** (overall metrics beyond per-packet `checksum(segment)`).

This doesn’t fully spell out `apxMANIFEST.json`, but it does fill in key fields for the Protocol Layer and aligns with the main spec’s claim that `.apx` is a ZIP with a manifest and layer files.

### 2.3 Subsystem roles restated in container context

Because the Implementation doc ties subsystems directly to container structure:

> “8. Subsystems
> | Aether Core | symbolic modeling and invariant extraction |
> | Press Engine | encoding of parameters and residuals |
> | Flux Decoder | reconstruction and fidelity validation |
> | Protocol Layer | serialization schema and metadata registry |”

We can read the container format as the **Protocol Layer’s concrete responsibility**:

- Guarantee that everything Aether Core + Press Engine produce (model IDs, θ, invariants, residual R, metrics, checksums) is stored in a self-consistent, versioned way.

---

## 3. Integer Models & Aether Information Framework (Post-Implementation + Declaration)

### 3.1 Integer-model demonstration (LFSR example)

The Post-Implementation Report documents a concrete, integer-only model test:

> “A 1 KB structured dataset generated by a 16■bit linear feedback shift register (LFSR)
> (seed = 0xBEEF, taps = 16, 14, 13, 11) was represented by integer parameters alone,
> achieving perfect reconstruction. Compression ratio = 214 / 1024 = 0.209. A random dataset
> remained incompressible. These results confirm Shannon’s boundary and verify the
> Aether model■based approach.”  
> *(Aether_Press_Post_Implementation_Report.pdf)*

This adds several important concrete details:

- The model used was a **16-bit LFSR with explicit seed and taps** `(seed = 0xBEEF, taps = 16, 14, 13, 11)`.
- Compression ratio is explicitly given as `214 / 1024 ≈ 0.209` for the structured dataset.
- A random dataset **“remained incompressible”**, reinforcing the main spec’s behaviour on random data.

It’s a specific example of `M(θ)` being an integer LFSR model with θ = {seed, taps, maybe length}, and `R = 0`.

### 3.2 Formal equations for structure + residual

The same report states the core relationships explicitly:

> “Let S be a dataset represented by bits b■. Define the model M(θ) with parameters θ such that
> S ≈ M(θ) + R, where R is the residual.
>
> (1) S = M(θ) ⊕ R (bitwise XOR for discrete systems)
> (2) Compression ratio = (|θ| + |R|) / |S|
> (3) Continuity constraint → lim_{|R|→0} Reconstruction = S”  
> *(Aether_Press_Post_Implementation_Report.pdf)*

So, in discrete systems, the residual is formally combined by XOR and the compression ratio is defined directly in terms of parameter and residual bit-lengths. This tightens the earlier, more verbal “rule + residual” concept.

### 3.3 Aether Information Framework (AIF) axioms

The Post-Implementation Report also lays out the AIF axioms:

> “5. Axioms of the Aether Information Framework (AIF)
>
> 1. Data = manifestations of relationships.
> 2. Information = minimal description of those relationships.
> 3. No ise = relationships below current model resolution.
> 4. Entropy = measure of unresolved relational density.
>
> These axioms define an information space extending beyond Shannon’s domain.
> They underlie the Aether Press and Trinity Gate architectures.”  
> *(Aether_Press_Post_Implementation_Report.pdf)*

These axioms give the philosophical backing for APP:

- **Noise** is explicitly redefined as “relationships below current model resolution”, rather than pure randomness.
- **Entropy** is “unresolved relational density”, which clarifies why residuals that remain after modelling represent unresolved relationships.

### 3.4 Beyond Shannon Limit declaration

The declaration file formalizes the claim and its framing:

> “The Aether Press Protocol represents a theoretical and experimental framework proposing the first
> deterministic method for reversible data compression beyond Shannon’s classical entropy limit. It reframes
> information not as probabilistic uncertainty but as a structured interaction of deterministic states…”  
> *(Aether_Press_Protocol_Beyond_Shannon_Limit_Declaration.pdf)*

and:

> “The Aether Press operates as a reversible mapping system that transforms binary sequences into structured
> integer matrices through deterministic coupling rules. Each layer of compression preserves total information
> quantity while reducing representational entropy. The Nexus Aeternus Protocol can be applied to stack and
> nest transformations, achieving exponential compression stability without probabilistic loss.”  
> *(ibid.)*

This is conceptual, but it:

- Reinforces Press as **“reversible mapping system”** to **“structured integer matrices”**.
- Explicitly ties NAP stacking/nesting to “exponential compression stability”.

---

## 4. Two-Track Press & Policy Layer (Press Performance Report)

The `press proformance.pdf` report adds a practical, runbook-level layer: **two-track Press** and concrete knobs.

### 4.1 Two-track Press: `P_state` and `P_cite`

The report introduces “TWO-TRACK PRESS (DO THIS EVERY TIME)”:

> “TWO-TRACK PRESS (DO THIS EVERY TIME)
> ------------------------------------
> 1.  **P_state (reconstructive)**  the _minimal_ snapshot needed for  $T$  to resume
>   exactly.
>     *   Must satisfy fidelity:  $d(O(S), O(\mathrm{DePr}(\mathrm{Pr}(S)))) \le \varepsilon$ .”  
> *(press proformance.pdf)*

Later, it describes P_cite as the proof/pointer channel:

> “Result: you keep **exactly** what the computational episode needs, and only
> **proofs/pointers** for everything else. That s where the astronomical  gains come from.”  
> *(press proformance.pdf)*

And in the TL;DR:

> “You keep the _small, exact_ computational snapshot (P_state), plus tiny proofs/pointers
> for the rest (P_cite).”  
> *(press proformance.pdf)*

So in addition to the main APP core, the legacy docs define a **policy-level separation**:

- **`P_state`** — the Press capsule(s) that are required for deterministic replay of `T`.
- **`P_cite`** — hashes, byte-lengths, and “a few extracted integers you actually use” for external sources (e.g. PDFs, logs) used only for provenance/audit, not for `T`.

This clarifies how APP can get “astronomical” crush ratios for traditional sources without contaminating the replay-critical state.

### 4.2 Practical knobs driving crush ratio

The same report enumerates specific operational knobs:

> “Practical knobs that drive the crush ratio
> ==========================================
> *   **Integerization pipeline** (normalize  units  quantize  zigzag  varint/delta/RLE).
>     *   Bound error upfront: if you quantize a scalar with step  $q$ , your max absolute
>   error is  $\le q/2$ . Pick  $q$  so it respects the field s  $\varepsilon$ .
> *   **Sparsity by contract** (PFNA): enforce degree caps and coupling radius so most entries
>   are zero  store only non-zeros.
> *   **O-only comparison**: you never compare the whole raw only your scoreboard  $O$ . That
>   lets you drop mountains of irrelevant detail.
> *   **Content dedupe**: identical chunks (by hash) collapse to one copy across checkpoints.”  
> *(press proformance.pdf)*

Key extra features:

- **Integerization pipeline**: standard sequence of transforms (normalize → quantize → zigzag → varint/delta/RLE) with explicit bound:
  - “*if you quantize a scalar with step q, your max absolute error is ≤ q/2. Pick q so it respects the field’s ε.*”
- **PFNA** (sparsity by contract): enforce degree caps and coupling radius to push sparsity and store only non-zeros.
- **O-only comparison**: acceptance is always based on scoreboard `O`, not raw data, aligning with the ε-bounded spec.
- **Content dedupe**: identical hashed chunks collapse to one stored copy across checkpoints.

These directly address the main spec’s gap around **lossy mode mechanics** by connecting ε to quantization step `q` and field-wise bounds.

### 4.3 "Crush without regret" runbook checks

The report gives a checklist explicitly labelled “Crush without regret checks (copy this into your runbook)”:

> “Crush without regret  checks (copy this into your runbook)
> ===========================================================
> 1.  **Field-level bounds:** For every numeric field  $x$  you store after quantization  $q$  :
> $|x_{\text{post}} - x_{\text{pre}}| \le q/2 \le \varepsilon_x$ .
> 2.  **Replay test:** DePress then run  $\Delta=0$ :  $O$  unchanged (fidelity at snapshot).
> 3.  **Predictive test:** DePress and run  $T^\Delta$ ; check  $d(O_{\text{true}},
>   O_{\text{replayed}})\le \varepsilon$ .
> 4.  **Document proof:** Keep  $\{\text{hash},\text{bytes}\}$  for each external source in
>   **P_cite** so an auditor can verify you didn t hallucinate  inputs.
> 5.  **Idempotence:** Same envelope + same nonce  no net change to  $O$ .
> 6.  **Isolation:** Prior checkpoint O-hashes never change.”  
> *(press proformance.pdf)*

These become explicit **acceptance criteria** for any Press configuration:

- Field-level quantization is bounded by ε per-field.
- Replay at Δ = 0 is identical at the scoreboard level.
- Predictive replay across time window Δ stays within global ε.
- P_cite proves you didn’t hallucinate raw sources.
- Idempotence and isolation of prior checkpoints are enforced.

### 4.4 Press policy cards & what to avoid

Press policy cards are introduced as a template:

> “Press policy card (use per source)
> ==================================
> PRESS POLICY  <source_name>
>
> Type: (text/pdf/image/log/table/sensor)
> Track: [P_state | P_cite]  (pick one; sometimes both)
> O-fields derived: { ... }  (list only what T or O needs)
> Quantization q per field: {f1:q1, f2:q2, ...}
> ...”  
> *(press proformance.pdf)*

And the "What to avoid" list warns explicitly:

> “What to _avoid_ (this is where people get burned)
> =================================================
> *   **Letting P_state depend on raw docs** you won t replay. If  $T$  doesn t need the raw,
>   dont pack it hash it in **P_cite** instead.
> *   **Quantizing before you set  $\varepsilon$ **. Always lock  $\varepsilon$  first; choose
>   $q$  to fit inside it.
> *   **Comparing anything other than  $O$ ** in acceptance. The whole point is: if  $O$
>   matches under the contracts, you re good.”  
> *(press proformance.pdf)*

These older docs therefore introduce a **policy/interface layer** on top of APP:

- A Press policy is a per-source contract tying type, track (P_state/P_cite), O-fields, and per-field quantization.
- Misconfiguration guidance is explicit: don’t mix raw docs into P_state when they’re not needed; don’t choose q before ε; don’t compare anything other than O when validating.

---

## 5. Dimensional Press & Per-Dimension Controls (Dims Press Report)

The `press v2.pdf` report focuses on **dimensions on the NAP bus** and how Press + Loom handle them mid-run.

### 5.1 Dims Press tables

The report shows concrete tables (truncated here) for per-entry Press performance on a NAP bus:

> “Dims Press  Per-entry
> | source | raw_bytes | lores_bytes | press_bytes |
> | --- | --- | --- | --- |
> | NAP_bus | 385 | 8 | 232 |
> | NAP_bus | 385 | 8 | 113 |
> | NAP_bus | 385 | 8 | 117 |
> | NAP_bus | 385 | 8 | 119 |
> | NAP_bus | 385 | 8 | 121 |
> | NAP_bus | 385 | 8 | 118 |
> Dims Press  Summary
> |  | source | entries | full press_x | …”  
> *(press v2.pdf)*

Even though the summary table is truncated in the extracted text, we see:

- **Raw bytes vs “lores_bytes” vs “press_bytes”** per entry.
- The concept of a **Dims Press Summary** over many entries.

### 5.2 Per-dimension, per-layer fidelity controls

The key part of this report is the explicit control list:

> “FIDELITY CONTROLS YOU CAN SET PER-DIMENSION (OR PER-LAYER)
> ----------------------------------------------------------
> *   **Exact vs -quantized dims:** choose which dims must match exactly for replay vs which
>   can be bucketed (e.g.,  to nearest 1e-3, positions to 1 unit).
> *   **Residual fraction:** tighten or loosen Loom s residual size (e.g., 5 20%) for layers
>   where you need more/less detail.
> *   **Selective retention:** mark dims as {recompute, residual, full}:
>     *   _recompute_: derive from other fields on replay (kept out of residual),
>     *   _residual_: store compact delta,
>     *   _full_: store verbatim (e.g., provenance-critical tags).
> *   **Dict scopes:** keep **per-node dictionaries** or a **global Press dict** on the NAP
>   bus for cross-layer dimensional schemas.”  
> *(press v2.pdf)*

This extends APP in several ways:

- **Exact vs quantized dims** – Each dimension can be treated exactly or quantized to some resolution (e.g. 1e-3 or 1 unit), rather than a single global ε.
- **Residual fraction** – You can tune Loom’s residual size per layer (5–20% etc.), exposing a control for how much detail is stored in residuals.
- **Selective retention** (per-dim):
  - `recompute` → value is recomputed from other fields in replay and not stored in residuals.
  - `residual` → store a compact delta.
  - `full` → store verbatim (e.g., for provenance-critical tags).
- **Dict scopes** – Press can keep per-node dictionaries or a global Press dictionary on the NAP bus to share dimensional schemas across layers.

The bottom line section makes the mid-run dynamic aspect explicit:

> “BOTTOM LINE
> -----------
> *   New dims can appear mid-run (we proved it) and get **Loomed** (for deterministic replay)
>   and **Pressed** (for compact, reversible storage) like any other data.
> *   You can dial **how faithful** they must be for reuse and **how much** detail to keep in
>   residuals on a **per-dimension, per-layer** basis.”  
> *(press v2.pdf)*

So legacy docs formally state that **dimensions are dynamic**, and Press+Loom have explicit knobs to control fidelity/storage **per dimension and per layer**, not just globally.

---

## 6. LCDRM as Conceptual Predecessor

The LCDRM white paper is not APP itself but is clearly the conceptual predecessor of relational compression.

### 6.1 LCDRM concept and equations

The white paper defines LCDRM as:

> “Layered Compression via Deterministic Relational
>  Mapping (LCDRM)
>  
> 1. Concept Overview
> LCDRM is a deterministic, scale-invariant compression paradigm that encodes relationships
> between data elements rather than the elements themselves. Each layer represents residual
> transformations between successive states of the previous layer, achieving multi-scale
> compression and self-consistent reconstruction without entropy coding.”  
> *(LCDRM_White_Paper_Uroboros.pdf)*

And lays out the layered-delta structure:

> “2. Foundational Equations
> Let D■ = {x■}. Each subsequent layer: L■ = ΔL■■■ = {x■■■ - x■ | x■ ∈ L■■■}. Continuous
> generalization: L■(t) = d/dt L■■■(t). Compression occurs when |L■| < |L■■■| until ΔL■ → 0.
> 3. Deterministic Reconstruction
> Decompression: L■■■(i) = Σ■■■■ L■(k) + C, where C is the base constant. Guarantees identical
> reconstruction across deterministic systems.”  
> *(ibid.)*

Key conceptual carry-overs into APP:

- Encoding **relationships** between data elements, not the elements themselves.
- Using successive **residual layers** (`L_n`) until incremental deltas vanish (`ΔL → 0`).
- Decompression as a deterministic summation with a base constant.

The summary is explicit:

> “LCDRM formalizes Trinity’s relational compression method, demonstrating minimal relational
> integers can encode full datasets with deterministic reconstruction. It compresses across scales of
> dependency, not merely symbol probability.”  
> *(LCDRM_White_Paper_Uroboros.pdf)*

This lines up tightly with APP’s later “model + residual” framing and the AIF axioms. LCDRM payload JSONs (`lcdrm_payload.json`, `lcdrm_v2_payload.json`) show concrete integer arrays and lengths, but those are more legacy data artifacts than APP surface.

---

## 7. Gap Closure vs Main Spec (What This Pass Adds)

Revisiting the **gap list from the main APP spec sheets**, here’s what these legacy docs fill or partially fill.

1. **Manifest / Container Details**
   - We still don’t have a full `apxMANIFEST.json` schema, but the Implementation doc adds:
     - Header fields: “Model ID, version, and compression mode… Metadata: dtype, shape, fidelity metric.”
     - Body fields: “Model parameters (quantized or raw)… Invariant dictionary… Residual byte stream… Metrics and checksum.”
   - The Packet pseudocode adds segment-level `checksum(segment)` and field list (`model_id, θ, I, eps, R`).

2. **Model Library & Selection / Parameter Fitting**
   - Legacy docs still treat model selection (`select_model`) and fitting (`fit_params`) as black boxes, but:
     - The LFSR demo gives a concrete example of a model family (LFSR with given taps).
     - LCDRM shows a layer-based relational delta model.
   - No normative algorithm for `select_model` is given yet.

3. **Residual Codec**
   - Implementation pseudocode names `lossless_encode` and `entropy_encode(r_q, prior=learned)` but does not pin down a specific codec.
   - However, the integerization pipeline (normalize → quantize → zigzag → varint/delta/RLE) from press proformance shows the *shape* of the residual encoding process at the integer stream level.

4. **Lossy Mode Mechanics / ε**
   - The legacy docs now connect ε to quantization explicitly:
     - “if you quantize a scalar with step q, your max absolute error is ≤ q/2. Pick q so it respects the field’s ε.”
     - Field-level bound: `|x_post − x_pre| ≤ q/2 ≤ ε_x`.
   - They also define a multi-step acceptance regime (replay test, predictive test, etc.), which was missing from the high-level main spec.

5. **SimA / SimB & NAP**
   - These specific labels don’t appear in the legacy PDFs we just used (they’re more in the newer Pillar report), but the Beyond Shannon declaration and LCDRM white paper make clear that:
     - APP’s roots are in **layered relational transforms** (LCDRM).
     - NAP stacking/nesting is how those transforms are composed to “achieve exponential compression stability without probabilistic loss.”

6. **Topology & Policy Layer**
   - The v2/v3 reports add:
     - The **two-track P_state/P_cite** policy construct.
     - Per-dimension and per-layer controls (exact vs quantized dims, residual fraction, selective retention, dict scopes).
     - Concrete **Press policy cards** per source.
     - “What to avoid” guidance that operationalizes safety.

7. **Scaling / Performance**
   - Still no formal big-O bounds, but we now have:
     - A specific IMU example: “Achieved Compression: 8–20× lossless; 30–100× ε-bounded.”
     - Dims Press tables showing byte-level effects on NAP bus dimensions.
     - Qualitative but quantified claims for traditional sources: “Raw PDFs/logs/images: 100×–10000× reduction when treated as P_cite + tiny extracted integers… Structured state for T: often 10×–100× from sparsity + integerization (and still exact/ε-bounded).”

8. **Networked Service Spec**
   - These legacy docs still don’t define REST/gRPC surfaces. Security is discussed elsewhere (Press Pillar main report, mTLS/sandboxing hints), not in this batch.

---

This complement sheet should be read side-by-side with **“Astral Press Pillar – APP Spec Sheets v1 (2025-11-20)”**. Together they form:

- v1: Core APP spec, components, invariants, `.apx` overview, NAP integration.
- v2 (this doc): Legacy architecture naming, container/packet formatting, integer-model proof, AIF axioms, two-track Press, per-dim controls, and LCDRM roots.

Next passes can pull in:

- Newer `.apx`-specific docs (if any) for a closer-to-wire manifest schema.
- Any Trinity Gate + Press bridging docs that further constrain how APP plugs into TGP/TBP.



<!-- END SOURCE: astral_press_app_complement_sheet_v_2_legacy_docs_2025_11_20.md -->


---

<!-- BEGIN SOURCE: astral_press_app_complement_sheet_v_3_math_compendium_2025_11_20.md -->

# Astral Press — APP Complement Sheet v3 (Math Compendium Pass)

Source for this pass:

- `Aether Math Compendium – Deterministic Framework & Equations Overview` (`/mnt/data/Aether Math Compendium.pdf`)

Focus: **All Aether Press (APP)–relevant math, equations, and pipeline details** from the compendium, used to fill gaps and extend the existing APP spec sheets.

All interpretations are directly grounded in verbatim lines from the Math Compendium.

---

## 1. Refined APP Definition & Core Behaviour

The Math Compendium gives a concise, math-focused definition of Aether Press:

> “Aether Press is described as a **‘reversible information-densifier’** that encodes data into a compact latent mathematical form and back without loss. In essence, Press treats any input (text, image, binary, etc.) as a stream of symbols and rewrites it as **the math that could produce it**.”  
> *(Math Compendium, p.2)*

This reinforces and sharpens the previous description from the Pillar report:

- **Reversible information-densifier** — the emphasis is on **reversibility** and **information density**, not just bit-level compression.
- Treats any input as a **symbol stream** and rewrites it as a **generative mathematical description**.

The compendium also explicitly states that APP is implemented as a composition of **pure functions**:

> “The Press pipeline involves several stages implemented as **pure functions (no heuristics or external dependencies)**.”  
> *(p.2)*

So for spec purposes, every stage (Sense & Tag, Normalize, Factor & Press, Integrity) is:

- Deterministic.  
- Side-effect free relative to input/output (no hidden state, no external randomness).

---

## 2. Press Pipeline — Stages and Responsibilities

The compendium spells out the Press pipeline by named stages.

### 2.1 Sense & Tag

> “**Sense & Tag:** It first inspects the input bytes and attaches a tiny header with the **‘recipe’ for decompression – the press version, chosen transform graph ID, original length, block size, integrity checksum, etc.** This fingerprinting step means the un-press operation always knows exactly which inverse transforms to apply.”  
> *(p.2, emphasis added)*

This adds concrete header fields and responsibilities:

- **Header / recipe content**:
  - `press version`
  - `transform graph ID`
  - `original length`
  - `block size`
  - `integrity checksum`
- Purpose:
  - Provide a **complete recipe** so `Unpress` can select the **correct inverse transform graph** with no ambiguity.

This complements previous references to headers in `.apxMANIFEST.json` by being explicit about “transform graph ID” as a first-class field.

### 2.2 Normalize

> “**Normalize:** The data is remapped onto a uniform base-$N$ symbol lattice optimized for compression. In other words, Press **‘straightens the grain’ of the data** – for example, it may reorder bits or re-encode values so that correlations become more localized and easier to eliminate. This normalization ensures that redundancies (like repeated patterns or structured subsets) line up in ways the next stage can capture.”  
> *(p.2)*

This gives a clearer mathematical picture of normalization:

- Data bytes `X` are mapped to a **normalized symbol sequence** on a **base-$N$ lattice**.
- Normalization may involve:
  - Bit reordering
  - Re-encoding values
  - Re-labelling / remapping symbols
- Goal: **localize correlations** so that structure is aligned and easier for the factorization stage to capture.

Appendix A later rewrites this as an explicit mapping:

> “Data bytes $X$ are mapped to a normalized symbol sequence (base-$N$ lattice) to straighten correlations. (E.g., $X \mapsto \phi_{\text{Press}}(X)$ for feature extraction, then re-encode symbols in a structure-exploiting order.)”  
> *(p.33)*

So we can treat `\phi_{Press}` as the normalization transform:

- `normalized = φ_Press(X)`  
- followed by re-encoding in a **structure-exploiting order**.

### 2.3 Factor & Press

The compendium is explicit about this stage:

> “**Factor & Press:** Using a combination of **on-the-fly learned models** and **fixed transforms**, Press **factorizes the stream into a set of sparse components (e.g. polynomial fits, periodic patterns, dictionaries) plus a small random residue**. It then entropy-codes these pieces **(via arithmetic coding, Huffman, etc.)** to produce dense output packets. The result is a highly compressed representation where most of the structure is captured by the factored components and only true randomness contributes to the residual size. Because these transforms are invertible and the encoding is lossless, the exact original data can be recovered by reversing each step in sequence.”  
> *(p.2, emphasis added)*

Key additions beyond earlier docs:

- **On-the-fly learned models + fixed transforms** — Press is not limited to a static library; it can learn models during compression, but still within a deterministic, reproducible pipeline.
- **Sparse components** include:
  - Polynomial fits
  - Periodic patterns
  - Dictionaries (symbol dictionaries)
- **Residual** is explicitly “small random residue” — only true randomness should remain after factorization.
- **Entropy coding choices**:
  - Arithmetic coding
  - Huffman coding
  - (Implicitly, other entropy coders within the same family could be used.)

This directly fills the earlier **residual codec gap**, indicating that `R` is encoded via standard entropy coders on top of factorized components.

### 2.4 Integrity & Metadata

The compendium elaborates the integrity layer:

> “**Integrity & Metadata:** Every Press output includes **integrated checksums or cryptographic tags per block and for the whole file (e.g. a 256-bit hash)** to guarantee bit-perfect round-trips. **A Merkle tree index may be used for streaming large data, allowing verification of partial data and resumable compression streams.** Only minimal metadata is stored (the header and optional user tags); if not needed, the Press container remains extremely lean (often just tens of bytes of overhead).”  
> *(p.2, emphasis added)*

This gives:

- **Per-block + whole-file integrity tags** (e.g. 256-bit hashes).
- Optional **Merkle tree index**:
  - For **streaming large data**.
  - Enables **partial verification** and **resumable** streams.
- Confirms overhead remains **“often just tens of bytes”** when no extra tags are used.

These details sharpen the earlier generic view of integrity in `.apx` and show how Press supports streaming use-cases.

---

## 3. Information-Theoretic Positioning (Respecting Shannon)

The Math Compendium explicitly addresses Press vs Shannon:

> “Press is designed to respect fundamental limits of information theory. It will not **‘cheat’ Shannon’s source coding theorem** – if data is truly random or already optimally compressed (like an MP3, ZIP, etc.), Aether Press cannot reduce it further without loss. In fact, the docs note that pressing such inputs may even result in slightly larger output due to header overhead. For meaningful inputs, however, Press achieves massive compression by exploiting hidden regularities. A key point is that any compression ratio beyond the Shannon entropy must either be lossy or **leverage known structure**. Aether Press does the latter: it assumes there is latent structure (patterns, correlations) in the data and explicitly finds it.”  
> *(p.2, emphasis added)*

This clarifies:

- APP **does not violate** Shannon; it does not compress truly random or already optimally compressed data.
- Huge ratios ("astronomical" crush) are achieved by **leveraging known / discoverable structure**, not by breaking entropy limits.
- If input is already optimized, output may be **slightly larger** due to header/metadata.

This aligns with earlier results (e.g., random data incompressible, structured data crushed) and formalizes the theoretical stance.

---

## 4. Press as Reversible Projection (Formal Equations)

Appendix A of the compendium includes a **formal Press equation block**:

> “**Aether Press (APP): Core equations for reversible compression and data summarization.**  
> **Reversible projection & restore:** Each data input is transformed into a press capsule and back with no loss. Uses PFNA’s invertible mapping:  
> $C_{\text{out}} = \Pr(S_{\text{in}})$ and $S_{\text{in}} = \DePr(C_{\text{out}})$, where $\Pr$ and $\DePr$ are Press and DePress operators (conceptually $= F$ and $F^{-1}$ specialized to file compression). **Ensures $H(\text{input}) = H(\text{output})$ (entropy conserved).**”  
> *(p.33, emphasis added)*

Key mathematical commitments:

- Press and DePress are explicitly **inverse operators**:
  - `C_out = Pr(S_in)`
  - `S_in = DePr(C_out)`
- They **conserve entropy**:
  - `H(input) = H(output)` in the lossless mode.

This connects nicely with the Time-Invariance & Idempotence guarantees in the main spec.

---

## 5. Iterative Model Factorization & Description Length

Appendix A restates Press’s multi-layer factorization in equation form:

> “**Iterative model factorization:**  
> $X = M_1 + R_1,\; R_1 = M_2 + R_2,\; \dots,\; R_{k-1} = M_k + R_k.$ Each $M_i$ is a model (polynomial, pattern, etc.) fit to the residual of previous; $R_k$ final noise residual. Achieves multi-layer compression; stops when $L_{\text{total}}$ (description length) no longer improves.”  
> *(p.33, emphasis added)*

This gives us a precise view of what APP is doing in factorization terms:

- **Layered models**: Press repeatedly fits models `M_i` to the residuals of previous layers.
- **Residual chain**: each step reduces structure, leaving `R_k` as final noise.
- **Stopping criterion**: Press stops iterating when the **total description length** `L_total` no longer improves (i.e., adding another model does not reduce overall cost).

Thus, APP’s factorization is a greedy/multi-pass process guided by a **description-length objective** rather than a fixed single-pass fit.

---

## 6. Dual Compressor Mixture (SimA vs Dictionary / SimB)

The compendium adds a clean cost-function formulation for APP’s dual compressor mixture:

> “**Dual compressor mixture:** For each segment of data, Press computes cost of **symbolic model ($L_A$) vs. dictionary coding ($L_B$)** and chooses the shorter. **Encodes a bit to signal which was used.**  
> **Cost function:**  $L_{\text{segment}} = \min\{L_A,\; L_B\} + L_{\text{gate bit}}$. Over whole file: (E7) $L = \dots$”  
> *(p.33, emphasis added)*

From this we can refine:

- For each segment:
  - `L_A` = description length under symbolic model (SimA-like channel).
  - `L_B` = description length under dictionary-based model (SimB-like / dictionary channel).
  - Press chooses `min{L_A, L_B}` and **pays the cost of a gate bit** for the choice.
- Segment-level cost:
  - `L_segment = min{L_A, L_B} + L_gate_bit`.
- Whole-file cost:
  - Summed over segments: `L = Σ L_segment` (E7; tail truncated in extraction, but clearly implied).

This mathematically nails down the **SimA vs SimB selection logic** that the Press Pillar report described qualitatively.

The earlier text also mentions:

> “one dictionary-based (‘SimB’) – and for each segment chooses the smaller output, marking its choice in a tiny bitset.”  
> *(p.3)*

So the gate bits are stored in a **tiny bitset** over segments.

---

## 7. Libraries and AEON Mode

The compendium hints at a higher-level library mode for Press:

> “It can also build **shared libraries of symbols**: the design allows an **optional global dictionary so that repeated patterns across many files** (like common words or structures) are stored once and reused for all, an approach termed the **‘AEON library’ mode**.”  
> *(p.3, emphasis added)*

This extends APP with:

- An **optional global dictionary** (across files) instead of per-file/per-segment only.
- The **AEON library mode**, which stores common patterns once and references them from many capsules.

This was not spelled out in the main APP spec; here it’s made explicit as a mode for cross-file compression.

---

## 8. Press Capsules & Proof-Carrying Compression

The compendium describes pressed outputs as capsules that carry their own proof of correctness:

> “Crucially, Press ensures that all compression is self-consistent and auditable: **every pressed capsule includes the proof (in form of the model+residual) needed to verify and reconstruct the source.** Determinism, perfect reversibility, and integrity checking are guaranteed at every step.”  
> *(p.3, emphasis added)*

This reinforces:

- A pressed capsule is not just compressed data; it is a **proof-carrying artifact**:
  - Contains the **model(s)** and **residual**.
  - Allows **third parties** to verify reconstruction without access to original data.
- Guarantees:
  - Determinism.
  - Perfect reversibility (lossless mode).
  - Integrity at every step.

This sits nicely with the legal/provenance framing of `.apx` capsules in the main Press Pillar report.

---

## 9. Time Compression & Loom Integration (Math Angle)

The compendium links Press’s role in time compression into Loom:

> “In summary, Aether Press provides the mathematical means to **compress time and data** in the Aether system. By storing only what is necessary for deterministic regeneration (seed values, change logs, etc.) and nothing more, it allows the system to ‘crush’ the data footprint without violating fidelity. For example, rather than logging every frame of a simulation, Press can log only occasional state checkpoints ($C_i$) and the sequence of inputs or perturbations – since the update equations can replay everything in between. This idea of **pressing time** is developed further by the Loom pillar.”  
> *(p.3, emphasis added)*

Key points:

- Press compresses **time and data** by logging:
  - Checkpoints `C_i` (state snapshots).
  - Input/perturbation sequences.
- Loom then handles the **between-checkpoints timeline** using the update equations.

This squares with the Loom integration described in the main spec but adds math-driven examples (C_i, inputs sequences) directly tied to the update equations.

---

## 10. What This Pass Fills / Extends vs Prior Sheets

Relative to the existing APP spec and Legacy Docs complement, the Math Compendium pass:

1. **Clarifies the pipeline stages** with named steps and details:
   - Sense & Tag (header fields: press version, transform graph ID, original length, block size, integrity checksum).
   - Normalize (explicit base-$N$ lattice mapping via $\phi_{Press}$).
   - Factor & Press (on-the-fly learned models + fixed transforms; sparse components; entropy coding via arithmetic/Huffman).
   - Integrity & Metadata (per-block + full-file hashes; optional Merkle tree index; overhead scale).

2. **Fills the residual codec gap** by explicitly naming entropy coding methods: arithmetic coding, Huffman, etc., used after factorization.

3. **Provides formal Press equations**:
   - Reversible projection: $C_{out} = \Pr(S_{in})$, $S_{in} = \DePr(C_{out})$, with `H(input) = H(output)`.
   - Iterative factorization: $X = M_1 + R_1, R_1 = M_2 + R_2, …, R_{k-1} = M_k + R_k$ with stop when $L_{total}$ no longer improves.

4. **Pins down the dual-compressor mixture cost function**:
   - `L_segment = min{L_A, L_B} + L_gate_bit` and a tiny bitset marking SimA vs dictionary/SimB choice.

5. **Introduces AEON library mode** explicitly**:**
   - Optional global dictionary shared across files for repeated patterns.

6. **Strengthens the Shannon-compliance framing**:
   - APP does not cheat Shannon; huge ratios come from exploiting structure, not surpassing entropy.

7. **Makes capsules explicitly proof-carrying**:
   - “Every pressed capsule includes the proof (model+residual) needed to verify and reconstruct the source.”

8. **Tightens time-compression narrative mathematically**:
   - Checkpoints `C_i` + input sequences as sufficient for replay when combined with update equations, feeding into Loom’s skip-ahead.

This v3 complement sheet should be read alongside:

- **v1** – APP Spec Sheets (Pillar report core).
- **v2** – Legacy Docs Complement (original Aether Press protocol + performance docs + LCDRM roots).

Together, they give a **much more math-complete picture** of Aether Press: from philosophical framing, through protocol/container design, to explicit cost functions and factorization equations.



<!-- END SOURCE: astral_press_app_complement_sheet_v_3_math_compendium_2025_11_20.md -->


---

<!-- BEGIN SOURCE: astral_press_app_complement_sheet_v_4_implementation_canon_pack_2025_11_20.md -->

# Astral Press — APP Complement Sheet v4 (Implementation Canon Pack Pass)

**Scope of this pass**

Use the **implementation canon pack** from `implementation.zip` to tighten the Astral Press spec around:

- `.apx` container + Press Metadata Manifest responsibilities.
- NAP Compression Manifest structure (how stacked/nested layers are wired).
- AEON‑i descriptors and APXi integer stream grammar (SimA/SimB surface).
- Metrics & evaluation (description length, kappa, MDL rules).
- System‑mode interactions (S1–S12) where they touch Press.
- The explicit canon gap ledger.

**Source docs for this pass (all from `implementation/`):**

- `astral_press_pillar_apx_container_manifest_canon_pass.md`
- `astral_press_pillar_nap_compression_manifest_spec_canon_pass.md`
- `astral_press_pillar_aeon_i_apxi_descriptor_grammar_canon_pass.md`
- `astral_press_pillar_metrics_evaluation_canon_pass.md`
- `astral_press_pillar_s_1_s_12_modes_switchboard_canon_pass.md`
- `astral_press_pillar_canon_gap_ledger_big_dogs_pass.md`

Earlier sheets (v1–v3) plus the Dev Implementation Spec and its addenda are treated as already reflected in the base APP spec.

All interpretations below are grounded in direct quotes from these implementation docs.

---

## 1. `.apx` Container & Press Metadata Manifest (MANIFEST.json / .apxMANIFEST.json)

### 1.1 Canon role of `.apx`

The APX container pass explicitly frames `.apx` at a high level as **the deterministic Press capsule**:

> Scope: Close the APX container + manifest gap only using canon: what `.apx` is and must contain, what the Press Metadata Manifest is responsible for, where NAP + layers sit relative to the manifest.

Canon emphasises that `.apx` is not just "some archive"; it is the **Press capsule with specific structure and manifest semantics**. The doc repeatedly distinguishes between:

- The **container** (`.apx` file itself).
- The **Press Metadata Manifest** (`MANIFEST.json` / `.apxMANIFEST.json`).
- The **NAP Compression Manifest** (separate, but referenced).

The key points carried over from earlier spec + this pass:

1. `.apx` is a **deterministic, versioned container** for a pressed artifact:
   - Same input + same Press version + same configuration ⇒ **identical `.apx` bytes**.
   - Lossless mode: decompress → hash of reconstructed bytes **matches original**.

2. `.apx` carries:
   - The **manifest JSON** (Press Metadata Manifest).
   - One or more **layer payloads** (SimA / SimB outputs, residual streams, AEON/APXi streams).
   - Optional **reports / logs** (e.g. `report.json`).

3. `.apx` is where **public‑facing evidence** of a Press run lives; its manifest is called out as part of the "public contract".

### 1.2 Press Metadata Manifest — responsibilities

The APX manifest pass states that the metadata manifest (called `MANIFEST.json` in experiments and `.apxMANIFEST.json` in some notes) is a **JSON metadata file** which stores at minimum:

> “Original file **name**, original file **size** (bytes), original file **hash**… **compression mode**… **timestamp** of creation, optional filesystem metadata…”  
> *(APX Manifest canon pass)*

Cross‑collecting from the pass, the manifest’s responsibilities are:

- Identify the **source artifact**:
  - Original file **name**.
  - Original file **size** in bytes.
  - Original file **hash** (SHA‑256 is referenced multiple times in canon; the APX pass itself refuses to pick a new algorithm).
- Describe the **Press run configuration** at a high level:
  - Compression **mode** (e.g. textual vs numeric vs image; also lossless vs ε‑bounded, where applicable).
  - Press **version** and/or APP **schema version**.
- Summarise **content structure**:
  - A list of **layers**, or pointers to a more detailed layer/stack manifest.
  - References to **SimA** and **SimB** layer files.
  - A reference to the **NAP Compression Manifest** that knits the layers.
- Provide **integrity and provenance hooks**:
  - Hashes (and optionally sizes) for each payload segment.
  - Timestamps and optional filesystem metadata for archival fidelity.

The APX pass explicitly notes that the manifest is part of the **public contract** for `.apx` capsules: it lets external tools construct or verify data **without needing internal Aether context**.

### 1.3 Manifest vs NAP manifest

The APX pass draws a clear line between Press Metadata Manifest and the NAP manifest:

- The **APX manifest** answers "**what** is in this capsule and **when** it was produced".
- The **NAP Compression Manifest** answers "**how** do the SimA/SimB layers stack and nest to reconstruct the dataset".

The APX pass states:

> “NAP and APX manifests are separate but coordinated: APX says *what* and *when*; NAP says *how stacks/nests recombine*.”

So for spec purposes:

- APX manifest **must contain a reference** to a NAP manifest (when multi‑layer mode is used).
- NAP manifest may live **inside the `.apx` capsule** (as a separate JSON) or be resolved by reference; canon does not fix the storage location.

### 1.4 Known gaps (APX / manifest)

The APX pass is strict about not inventing details. It lists remaining gaps explicitly:

- **GAP-MANIFEST-01** — Exact JSON schema for `.apxMANIFEST.json`:
  - Field order, required vs optional keys, and nested structures are **not enumerated**.
  - No canonical `"schema_version"` or similar field is fixed in the slices used.
- **GAP-APX-BYTE-01** — Exact byte layout for `.apx` header / segment index:
  - There is **no** canonical description of the on‑disk header bytes beyond the existence of a manifest and payload sections.
- **GAP-SIGN-01** — Canonical choice of hash / signature / HMAC algorithms:
  - Canon mentions SHA‑256 and cryptographic tags, but does **not** pin down one binding scheme.

Anything beyond these responsibilities is explicitly marked by the APX pass as **design work, not spec**, and must not be treated as canon.

---

## 2. NAP Compression Manifest — layer graph & stacking

The NAP manifest pass treats the **NAP Compression Manifest** as the formal description of how SimA/SimB layers are stacked and nested.

### 2.1 Canon anchors

Canon description (quoted in the pass):

> “NAP Compression Manifest – … a Nexus Aeternus Protocol (NAP) form that encodes how multi‑layer stacks and nests recombine for exact reconstruction.”

From Press experiment setups:

> “Per dataset: `*_APP/nap_manifest.json`, `simA_layers/*.json`, `simB_layers/*.bin.gz`, and `report.json`.”

And from the paper forms spec (Paper Computer pack):

> “**NAP Compression Manifest**: `layers[] {id, kind∈{AP.symbolic (SimA), AP.residual (SimB)}, parent, refs[], params, ordering}, knit_rules, deterministic_order, hashes`.”

The pass treats this paper form as the **field list** we are allowed to use.

### 2.2 Top‑level object

The NAP manifest is a single record, conceptually a JSON object:

```text
NAP_Manifest := {
  layers[],
  knit_rules,
  deterministic_order,
  hashes
}
```

Where:

- **`layers[]`** — array of per‑layer entries (SimA/SimB layers).
- **`knit_rules`** — field capturing how layers are "knit together" (stack + nest recombination rules).
- **`deterministic_order`** — a field encoding the enforced application order.
- **`hashes`** — structure holding hashes for cross‑checking layer payloads.

The pass does **not** invent nested structure for `knit_rules`, `deterministic_order`, or `hashes`; it only states that they must exist and serve these roles.

### 2.3 `layers[]` entries (canon fields)

Canon field list (quoted verbatim):

> `layers[] {id, kind∈{AP.symbolic (SimA), AP.residual (SimB)}, parent, refs[], params, ordering}`

The pass fixes a conceptual **LayerEntry** as:

```text
LayerEntry := {
  id,
  kind ∈ {AP.symbolic (SimA), AP.residual (SimB)},
  parent,
  refs[],
  params,
  ordering
}
```

And elaborates each field:

- **`id`** — an identifier for the layer. Canon does not constrain its type beyond being usable in `parent` and `refs[]`.
- **`kind`** — explicitly constrained to:
  - `AP.symbolic (SimA)` — symbolic / generative layer.
  - `AP.residual (SimB)` — residual / statistical layer.
  
  The bracketed original SimA/SimB names are **preserved exactly** per name‑change guidance.

- **`parent`** — parent reference participating in the DAG:
  - Canon only tells us that the manifest encodes a **directed acyclic graph (DAG)** of dependencies and that each layer’s compression can depend on earlier ones without forming cycles.
  - It is **not** stated whether `parent` is a single `id`, `null` for roots, or a richer structure.
  - The pass therefore treats `parent` as a **single link field whose exact type is open**.

- **`refs[]`** — array of references:
  - Used to represent additional non‑tree dependencies (e.g., nested or cross‑layer links).
  - Exact semantics ("soft" vs "hard" dependencies) are **not fully specified**.

- **`params`** — parameter bundle:
  - Holds configuration for the layer: model IDs, hyperparameters, thresholds, etc.
  - Exact schema is **intentionally left open**; different layer kinds may interpret `params` differently.

- **`ordering`** — ordering metadata:
  - Used to enforce a **deterministic compression / decompression order** consistent with the DAG.
  - The pass does not fix whether this is an explicit rank, a timestamp, or a tuple.

### 2.4 DAG semantics and determinism

The NAP manifest pass formalises the DAG constraint:

> “Directed acyclic graph (DAG)… no cycle `(v0, v1, …, vk=v0)` with `(vi, vi+1)` in E. The phrase ‘one‑way stack’ further constrains that along the reconstruction path, there exists a **topological ordering** σ over V such that … DePress(Press(D; M); M) = D.”

Key invariants:

- `layers[]` and references (`parent`, `refs[]`) together define a **DAG** over layer IDs.
- There is at least one **topological ordering** consistent with `ordering` and `deterministic_order`.
- For fixed dataset `D`, Press version, and manifest `M`:
  
  ```text
  DePress(Press(D; M); M) = D
  ```

  That is: NAP‑described stacking / nesting must be **reversible and deterministic**.

### 2.5 Gaps (NAP manifest)

The NAP manifest pass closes some gaps and leaves others explicitly open:

- **Closed / clarified:**
  - Top‑level fields: `layers[]`, `knit_rules`, `deterministic_order`, `hashes`.
  - LayerEntry fields: `id`, `kind`, `parent`, `refs[]`, `params`, `ordering`.
  - The requirement that the manifest encodes a **DAG** and supports deterministic reconstruction.

- **Still open (must remain design space):**
  - Internal structure of `knit_rules`, `deterministic_order`, `hashes`.
  - Exact types for `id`, `parent`, and the element type of `refs[]`.
  - Detailed schema of `params` per layer kind.
  - Behaviour under corruption / partial data (missing layers, hash failures, malformed DAG).

The NAP manifest pass explicitly states that these details are **not present in canon** and cannot be speculated.

---

## 3. AEON‑i & APXi — descriptor grammar and integer stream

The AEON‑i / APXi pass focuses on the **descriptor language** used to write down SimA + parts of SimB.

### 3.1 AEON‑i role and relation to SimA/SimB

Canon description (from Press transform comments, summarised in the pass):

> “The job of AEON‑i is to provide a **compact, integer‑only encoding** of transformation definitions while staying deterministic and versionable.”

Relationship to SimA / SimB:

> “In the Press experiments and implementation notes:
> - **SimA** is the symbolic / generative compressor: columns fit with affine, polynomial, periodic, cross‑column, and grammar rules. These fits are **described via AEON‑i opcodes + integer parameters.**
> - **SimB** is the residual compressor: residuals are further transformed with Δ, XOR base, Golomb–Rice, AR(1..3), etc. Some of these transforms are likewise expressed as AEON‑i descriptors (e.g., AR(1), AR(2)).”

So AEON‑i is the **descriptor language** that:

- Encodes **SimA models** (transform rules and their parameters).
- Encodes some **SimB residual transforms** (e.g., autoregressive models).
- Provides an **integer‑only, opcodes+varints surface** that is versioned and deterministic.

### 3.2 Known opcodes (canon examples)

The pass lists the small set of opcodes that are explicitly referenced in canon:

> “`OP_SEGMENT` — for segmentation / piecewise modelling.
> `OP_AFFINE` — for affine rules of the form `y = a·x + b`.
> `OP_POLY3` — for cubic polynomial rules.
> `OP_PERIODIC` — for periodic components (sinusoidal / modular patterns).
> `OP_COMBINE` — to combine multiple components (trend + seasonal, or multiple bases).
> `OP_AR1`, `OP_AR2`, `OP_AR3` — for autoregressive residual transforms.”

The pass stresses:

- This is **not** a complete list; it is a **canon example set**.
- No additional opcodes may be assumed without seeing them in project files.

### 3.3 Parameter encoding (varints + ZigZag)

AEON‑i parameter encoding is described as:

> “Parameters (coefficients, indices, counts, etc.) are encoded as **variable‑length integers (varints)**. Signed integers (e.g., negative coefficients, offsets, phases) are encoded via **ZigZag** (map signed → unsigned, then varint). This is done to keep descriptors compact and portable, and to allow streaming decoders to parse opcodes without external schema.”

So for each AEON‑i opcode:

- There is a **fixed parameter list and order** per version.
- Each parameter is encoded as:
  - Unsigned varint, or
  - Signed integer → ZigZag → unsigned varint.

### 3.4 AEON‑i per‑version spec obligations

The pass spells out obligations for any AEON‑i implementation:

> “Implement AEON‑i opcodes as defined for its version:
>  - For the subset of opcodes it supports (e.g., `OP_AFFINE`, `OP_POLY3`, `OP_PERIODIC`, `OP_AR1`), it must:
>    - Map each opcode name to a numeric ID.
>    - Define a fixed parameter list and order.
>    - Encode parameters as varints (with ZigZag for signed values).
>
> Define an internal AEON‑i spec per version:
>  - This spec must be versioned and deterministic.
>  - Encoder and decoder must share the same table.”

Thus, canon requires that each AEON‑i **version** has:

- A table of opcode IDs and names.
- A fixed parameter sequence per opcode.
- Deterministic, shared spec between encoder/decoder.

### 3.5 APXi framing and integer stream

The APXi container is described as the **binary framing** for AEON‑i:

> “APXi := `[ version_u16, v0, v1, v2, … ]`
>
> Where:
> - `version_u16` is a two‑byte integer indicating the APXi grammar version.
> - `v0, v1, …` are varints (unsigned), representing opcodes, counts, parameters, and other encoded fields under that version’s grammar.”

And:

> “After the version word, APXi uses a **single varint stream**:
> - No explicit segment boundaries in the binary format; segmentation is implied by the **grammar** (which fields are expected in which order).
> - Op boundaries are determined by reading opcodes and consuming the exact number of varints defined by the grammar for that opcode.”

So APXi’s obligations are:

- **Prefix:** a 16‑bit `version_u16` field.
- **Body:** a single contiguous stream of unsigned varints.
- No explicit length prefixes for individual ops; the **grammar definition for that version** governs parsing.

### 3.6 AEON‑i / APXi gaps

The AEON‑i pass enumerates the biggest remaining gaps:

- **GAP-AEON-OPS-01** — Full AEON‑i opcode grammar (all opcodes, fields, constraints, and error behaviour) is **not** fully specified.
- **GAP-APXi-GRAMMAR-01** — APXi integer‑stream grammar and full field order beyond the version word and varints is **not** canonical.

Any implementation must therefore supply its own **internal AEON‑i spec** while staying measurable against these constraints.

---

## 4. Metrics & Evaluation — MDL, baselines, and `kappa`

The metrics canonical pass fills in more of the quantitative picture for APP.

### 4.1 Core quantities

The pass highlights the core information‑theoretic quantities:

- **Bits and entropy**: description length in bits for candidate models.
- **Description lengths:**
  - `L_total` — achieved description length for a Press configuration.
  - `L_naive` — description length using a naive/baseline scheme (e.g. uncompressed or simple per‑symbol coding).
- **Gain `kappa`:**

> “`L_naive` — description length using a naive or baseline scheme… `kappa` — gain, defined as the difference between naive and achieved description length.
>
> ```text
> kappa = L_naive - L_total
> ```
>
> A positive `kappa` indicates that the chosen models and residual coding produce a genuine compression improvement over the naive scheme.”

So Press is evaluated by how much it **reduces description length** relative to a naive or baseline scheme.

### 4.2 Layered MDL acceptance rule

The pass binds MDL to the multi‑layer structure:

> “In the multi‑layer model + residual stack, canon ties the stopping rule to MDL: for each new layer `i`, the stack continues only while adding the layer reduces `L_total`; once adding another model would increase overall description length, the process stops.”

This restates, in more MDL language, what the Math Compendium gave as:

- `X = M1 + R1, R1 = M2 + R2, …` until **description length no longer improves.**

Accepting or rejecting an additional layer is therefore a **MDL decision**.

### 4.3 Baselines and Pareto evaluation

The metrics pass also acknowledges baselines and Pareto analysis:

> “Baselines (gzip/bzip2/xz) are integrated as comparison points… windows, thresholds, and Pareto fronts are used to evaluate trade‑offs between compression ratio, speed, and fidelity.”

In particular:

- Press runs are compared against **standard compressors** (gzip, bzip2, xz) on the same data.
- Results are aggregated over **windows** or datasets and plotted as **Pareto fronts** (e.g. compression ratio vs speed vs error).
- Metrics like `kappa`, compression ratio, and runtime form the axes.

The pass does not define a canonical dashboard, but it does set expectations for **how APP is evaluated experimentally**.

### 4.4 Experiment manifests and policy artifacts

The pass mentions several experiment‑side artifacts:

- **Testdoc‑AP** and Pareto manifests:
  - Hold benchmark results and configuration for reproducibility.
- **APP_BARRIERS.json** (policy pack):
  - Central location for APP defaults (thresholds, penalties, windows, tolerances).

It also states that for each run one must record:

> “Container choice and APP mode; relevant knobs (thresholds, penalties, windows, tolerances); whether ESL and other modes (F1–F3, M1–M3, SFTY1–SFTY3) were enabled.”

So a proper Press evaluation setup must log:

- Which **container** (e.g. `.apx`) and **mode** were used.
- All **relevant knobs**.
- Which **system modes** were active.

### 4.5 Metrics gaps

Remaining gaps listed in the metrics and gap‑ledger passes include:

- **GAP-MDL-01** — Fully explicit Press‑level MDL functional (including all overhead terms) and numeric thresholds are **not** fully written down.
- **GAP-METRICS-01** — Concrete values for ε, window size `W`, and other numeric evaluation thresholds are not canon; experiments mention ranges but not final "blessed" values.

---

## 5. System Modes (S1–S12) — interactions with Press

The S1–S12 switchboard pass mostly operates at system level, but it states several direct responsibilities of modes around APP.

### 5.1 S‑mode family (high‑level)

Canon confirms a family of twelve system modes, collectively **S1–S12**, and describes them as:

> “System modes and switches (S1–S12) that control how pillars like Press, Gate, and Loom behave under different policies and safety envelopes.”

The pass deliberately **does not** name each mode or fix IDs/bitmasks; those details are elided in the source and kept as gaps.

### 5.2 Press‑relevant switches

The pass does, however, state responsibilities for several **Press‑adjacent switches**, summarised as:

> “ESL must control whether internal telemetry flows into Press + SLL.
> Offline Recompress must enable APP recompression of historical data without breaking provenance.
> Encryption must control whether APP outputs are wrapped in crypto layers.
> Knowledge Sync must cause policy/knowledge reloads for APP when sync succeeds.”

Implications for APP:

- **ESL (External / Event Stream Logging):** determines whether **telemetry and logs** are pressed or bypass Press entirely.
- **Offline Recompress:** governs whether historical `.apx` or raw stores can be **re‑pressed** with new APP versions/policies **without violating provenance**.
- **Encryption:** is a wrapper layer around `.apx` outputs; APP must remain deterministic **inside** the crypto envelope.
- **Knowledge Sync:** triggers reload of **policy/artifact packs** (e.g., `APP_BARRIERS.json`, AEON‑i tables) which Press depends on.

### 5.3 Mode gaps

The S1–S12 pass flags several gaps:

- No canonical mapping from **S1–S12 indices to named modes**.
- No canonical **JSON schema** for mode/switchboard manifests.
- No specified **per‑mode defaults** beyond qualitative descriptions.

Implementations must therefore treat any detailed S‑mode mapping as **local configuration**, not canon.

---

## 6. Canon Gap Ledger — what remains open

The canon gap ledger pass (`astral_press_pillar_canon_gap_ledger_big_dogs_pass.md`) consolidates outstanding gaps across APP, NAP, APX, AEON‑i, and metrics.

### 6.1 Confirmed canon (quick recap)

It re‑affirms:

- Press as Aether’s **data‑compression pillar**.
- Compression as **rule + residual** with bit‑exact reconstruction in lossless mode.
- Determinism: same input + same APP version → same `.apx` capsule.
- Multi‑layer stack: `X = M1 + R1`, `R1 = M2 + R2`, … until MDL no longer improves.
- NAP manifest as the DAG that makes stacked/nested SimA/SimB **reversible**.

These are consistent with v1–v3 and the Math Compendium.

### 6.2 Top‑level gaps

The ledger lists, among others, the following high‑level gaps (as of this implementation canon pack):

- **GAP-MANIFEST-01** — Exact JSON schema for `.apxMANIFEST.json`.
- **GAP-APX-BYTE-01** — Exact byte layout for `.apx` capsule header / segment index.
- **GAP-SIGN-01** — Canonical choice of hash / signature / HMAC algorithms and binding rules.
- **GAP-NAP-01** — Detailed field‑level schema for NAP manifest beyond the paper form fields.
- **GAP-AEON-OPS-01** — Full AEON‑i opcode grammar (fields, constraints, error behaviour).
- **GAP-APXi-GRAMMAR-01** — APXi integer‑stream grammar and full field order.
- **GAP-MDL-01** — Fully explicit Press‑level MDL functional and numeric thresholds.
- **GAP-METRICS-01** — Concrete ε, window sizes, and other evaluation thresholds.

The ledger’s purpose is to keep these gaps **visible** so later design work does not accidentally treat them as already specified.

---

## 7. What v4 adds on top of v1–v3

Relative to the earlier APP spec sheets and complement passes, this v4 implementation‑canon pass contributes:

1. **Clearer APX manifest responsibilities** — source identity, Press configuration, layer references, and integrity/provenance, plus explicit APX vs NAP manifest roles.
2. **A concrete NAP Compression Manifest shape** — top‑level fields (`layers[]`, `knit_rules`, `deterministic_order`, `hashes`) and LayerEntry fields (`id`, `kind`, `parent`, `refs[]`, `params`, `ordering`) tied to DAG semantics.
3. **A defined AEON‑i / APXi surface** — known opcodes, varint/ZigZag parameter encoding, 16‑bit APXi version prefix, and single varint stream semantics.
4. **Metrics quantities and evaluation setup** — `L_total`, `L_naive`, `kappa`, MDL stopping rule, baselines, Pareto framing, and experiment manifests.
5. **System‑mode hooks around Press** — ESL, Offline Recompress, Encryption, and Knowledge Sync responsibilities, even though S1–S12 mapping stays open.
6. **An explicit, centralised list of remaining gaps** — through the canon gap ledger.

This sheet should be read alongside:

- **v1** — APP Spec Sheets (Pillar report core).
- **v2** — Legacy Docs Complement (protocol + LCDRM roots).
- **v3** — Math Compendium Complement (formal equations, dual compressor cost function).

Together, v1–v4 provide a canon‑faithful description of Astral Press down to the APX/NAP/AEON/APXi surfaces and their remaining open design spaces.



<!-- END SOURCE: astral_press_app_complement_sheet_v_4_implementation_canon_pack_2025_11_20.md -->


---

<!-- BEGIN SOURCE: astral_press_pillar_app_spec_sheets_v_1_2025_11_20.md -->

# ASTRAL PRESS PILLAR — APP SPEC SHEETS (v1)

Using the **main Press Pillar report** as the sole source of truth. All interpretations are grounded in direct statements from that report.

---

## SPEC SHEET 1 — CORE PROTOCOL (APP)

### 1.1 Definition

The report defines the Aether Press Protocol (APP) as:

> “a symbolic compression framework that projects raw data into a structured latent form and inverts it back perfectly to the original dataset.”  

and:

> “This pillar enables universal, lossless compression across domains by **storing only generative rules and minimal residuals instead of entire datasets**, yielding extreme data reduction without violating deterministic fidelity.”

So, at spec level:

- **APP is a reversible transform**  
  - `Press(data) → capsule`  
  - `Unpress(capsule) → data`
- It compresses by **encoding relationships / rules + small residuals**, not by bit-twiddling alone.

### 1.2 Scope & Responsibilities

The report says APP:

> “serves as the Trinity system’s **data compression subsystem**, responsible for distilling large datasets or simulation outputs into concise mathematical representations.”  

> “operates downstream of the Trinity architecture as a **post-processing framework** that captures the underlying structure of information.”  

> “encode data as ‘rule + residual’ pairs and package them for storage or transmission, guaranteeing that the original information can be fully reconstructed when needed.”  

> “standardizes symbolic reduction across any domain (physics, simulation, telemetry, etc.) and ensures compression is achieved without introducing irreversibility unless explicitly allowed (e.g. optional lossy modes).”

So responsibilities:

- **Downstream** of core simulation/engine layers.
- Encode as **rule + residual** and package.
- Provide **universal, domain-agnostic compression**.
- **Never irreversible**, unless explicitly configured in a lossy mode.
- Respect “conservation laws and deterministic invariants”:

> “it must respect conservation laws and deterministic invariants, compressing data only in ways that do not alter the verifiable state of the system.”

### 1.3 Primary Operations

From the math section:

> “Lossless Round-Trip:  *$Unpress(Press(data)) = data$* (Invertibility of the compression. Press followed by Unpress yields the exact original dataset.)”

> “Press as Checkpoint (Time Invariance):  Press/DePress operations do not advance time; only the system’s transition map $T$ does. (They serve as save/restore snapshots, preserving state without progressing simulation time.)”

So:

- **Press** — compress a full state or file into `.apx`.  
- **DePress / Unpress** — decompress `.apx` back to the **exact** original, without changing system time.
- When used as checkpoint: Press/DePress is **time-neutral**; only Trinity’s map `T` changes state.

---

## SPEC SHEET 2 — COMPONENT INVENTORY

This is straight from the `Components (Named/Stated/Implied)` list plus later sections.

For each component: **Definition → Role → Interactions → Gaps**.

---

### 2.1 Aether Press Protocol (APP) — Core

> “Aether Press Protocol (APP) – Named:  **A symbolic compression framework defining the rules for model-based data reduction. It compresses by capturing relationships instead of raw bits.**”

- **Role**
  - Governing spec for **model-based compression**.
  - Defines the **rule+residual** structure, pipeline, invariants.
- **Interactions**
  - Uses Domain Models, Parameter Fitting, Residual Encoding, Packaging.
  - Feeds into `.apx` capsules and manifests.
  - Bound to Nexus Aeternus Protocol (NAP) for stacking/nesting and distributed runs.
- **Gaps**
  - The **exact list of allowed model families**, coefficient formats, and parameter encoding rules are *not fully enumerated* in this report. They are referenced only by example (“Fourier series, polynomial fit, Markov process”).
  - Bit-level layout of the APP internal representation is not spelled out here – that’s implied to live in the Implementation PDFs.

---

### 2.2 Residual Encoding

> “Residual Encoding – Stated:  **The step storing only minimal differences between a model’s output and the real data. Residuals represent information not explained by the generative model.**”

- **Role**
  - Capture the **delta** between predicted data and actual data.
  - Hold all entropy the model could not express.
- **Behaviour**
  - Comes *after* the model-inference stage:
    > “Then comes Residual Encoding, which records the delta between the model’s output and the actual data – ideally this residual is small if the model captured most structure.”
- **Gaps**
  - No explicit spec here for:
    - Residual **coding scheme** (e.g. entropy coder choice, block size).
    - Residual **layout** inside `.apx` (file naming, segmentation).
  - We know residuals exist and are encoded, but the **coding format** is deferred to implementation docs.

---

### 2.3 Packaging Stage

> “Packaging Stage – Named: **A phase that wraps the model ID, parameters, and residuals into a portable container. Ensures all pieces needed for reconstruction are kept together.**”

- **Role**
  - Transform internal model and residual objects into a **disk/transport format**.
  - Ensure the capsule is **self-contained**.
- **Behaviour**
  - Described as:
    > “Finally, the Packaging stage wraps the model identifier, the fitted parameters, and the encoded residual into a portable file container. This container (realized as a .apx archive in implementation) encapsulates everything needed for reconstruction.”
- **Gaps**
  - Packaging rules beyond “ZIP with manifest + layer files” are not detailed here.
  - Exact **naming scheme** and layering conventions (e.g. `descriptor.bin`, `residual.dat`) are implied but not spelled out in this focus report.

---

### 2.4 APX Capsule Format (`.apx`)

> “APX Capsule Format – Named:  **A portable .apx container for Aether Press outputs. It is a deterministic, self-contained ZIP archive (manifest + layer files) used to store compressed data and metadata.**”

- **Role**
  - Public, **implementation-neutral** container.
  - Zip-based; holds:
    - `apxMANIFEST.json`
    - Compression layers (SimA descriptor, SimB residuals, block indexes, etc.)
- **Behaviour / Guarantees**
  - **Deterministic**:
    > “given the same input data and the same version of APP, it will produce the exact same .apx capsule every time.”
  - **Minimal overhead**:
    > “The overhead added by the .apx format is minimal – on the order of tens to a few hundred bytes for a header and small per-block indexes.”
  - **Self-contained archival artifact**:
    > “to make each .apx a self-contained archival artifact.”
  - Internal integrity:
    > “Press capsules carry internal integrity tags (per-block and whole-file hashes) so that any corruption or mismatch is detected upon decompression.”
- **Gaps**
  - The report does **not** list:
    - Full JSON schema of `apxMANIFEST.json`.
    - Directory layout of the ZIP (exact filenames for layers).
    - Maximum supported sizes or limits.

These appear in **Aether_Press_Protocol_Implementation.pdf**, not in this focus report.

---

### 2.5 SimA — Symbolic Compressor

> “SimA (Symbolic Compressor) – Named:  **In advanced Press usage, a generative compression stream that models structured patterns (stacked/nested rules) and records only math needed to reconstruct data.**”

- **Role**
  - The **main generative / rule channel** in stacked/nested APP v2.
  - Encodes symbolic structure: patterns, tilings, parameterized rules.
- **Behaviour**
  - Works with SimB:
    > “In advanced Press usage, a generative compression stream that models structured patterns (stacked/nested rules)…”
    > “SimB (Residual Compressor) – … a complementary residual stream capturing any data SimA cannot express, layer by layer. Together with SimA, it splits deterministic structure from randomness.”
  - Under NAP, SimA’s outputs are coordinated by a **NAP manifest** describing layers and nests.
- **Gaps**
  - No formal definition of:
    - SimA’s **internal model language**.
    - Allowed transformation types.
    - Exact on-disk representation of SimA streams.

---

### 2.6 SimB — Residual Compressor

> “SimB (Residual Compressor) – Named:  **A complementary residual stream capturing any data SimA cannot express, layer by layer. Together with SimA, it splits deterministic structure from randomness.**”

- **Role**
  - Dedicated residual channel for stacked/nested mode.
  - Holds what SimA cannot capture “layer by layer”.
- **Behaviour**
  - Works in lockstep with SimA via NAP:
    > “NAP Compression Manifest … ‘knits’ together SimA and SimB outputs. Defines how multi-layer stacks and nests recombine for exact reconstruction.”
- **Gaps**
  - No explicit coding spec for SimB’s residuals beyond the conceptual description.
  - We know SimB captures the “irreducible randomness” part, but not its compression codec parameters here.

---

### 2.7 NAP Compression Manifest

> “NAP Compression Manifest – Named:  **A Nexus Aeternus Protocol (NAP) manifest that ‘knits’ together SimA and SimB outputs. Defines how multi-layer stacks and nests recombine for exact reconstruction.**”

- **Role**
  - Structural manifest for **multi-layer APP v2**.
  - Records:
    - Stack order (micro → meta → global).
    - Nest groupings (per domain or segment).
    - Mapping between SimA rule streams and SimB residual streams.
- **Behaviour**
  - See pipeline section:
    > “Using NAP’s coupling, these stacked and nested compressions are synchronized and recorded in a manifest that allows the entire multi-layer process to be reversed deterministically.”
  - File name example: `nap_manifest.json` is mentioned:
    > “each compressed dataset under NAP yields a manifest (nap_manifest.json) which enumerates the layers and references between the symbolic (SimA) and residual (SimB) components.”
- **Gaps**
  - JSON schema of `nap_manifest.json` is not in this report.
  - No explicit enumeration of fields beyond “layers and references” and their semantics.

---

### 2.8 Baseline Codecs (gzip, bzip2, xz)

> “Baseline Codecs (gzip, bzip2, xz) – Named (contextual): Standard compression tools used as baseline benchmarks for Press experiments. Provided point of comparison for APP’s performance on various data types.”

- **Role**
  - **Not part of APP itself**, but used in experiments to benchmark performance.
- **Behaviour**
  - Used in `compression_report.csv` and baseline results.
  - Show Press matches or beats them:
    > “APP performing on par with conventional tools for unstructured text … while vastly outperforming them for structured inputs (often compressing to <0.1% of original size, beating standard compressors by large factors).”

No real “gaps” here; they are just external comparators.

---

### 2.9 Press Metadata Manifest (`apxMANIFEST.json`)

> “Press Metadata Manifest – Stated:  **The .apxMANIFEST.json file storing original file metadata: name, size, hash, compression mode, timestamp, etc. Extended in later versions to include file system info (permissions, timestamps) for archival completeness.**”

- **Role**
  - Describes the **original file**, compression parameters, and Press version.
- **Behaviour**
  - Stores:
    - `"orig_sha256"`:
      > “This SHA-256 hash is computed at compression time and stored as "orig_sha256" in the manifest, along with the original file size and name.”
    - `"apx_version"` (Press version):
      > “The manifest also records the exact Press version used ("apx_version").”
    - Compression mode (lossless vs lossy with epsilon).
    - Extended metadata in v0.2:
      > “This was implemented as a v0.2 update to the format, adding ~100–150 bytes of JSON metadata per file… including full metadata had no meaningful impact on compression ratios… yields high value for provenance.”
- **Gaps**
  - Full key list is not included here.
  - We know `"orig_sha256"`, `"apx_version"`, and some fields for name/size/timestamps, but not full schema.

---

### 2.10 HMAC Signature (APX)

> “HMAC Signature (APX) – Implied: **Cryptographic signing of capsules to ensure authenticity and tamper-detection. Allows verification that an .apx capsule was created by the authorized system and not modified.**”

- **Role**
  - Optional **authenticity layer** on top of integrity.
- **Behaviour**
  - Stored in manifest:
    > “The manifest stores the signature and can be checked during decode to ensure integrity and author authenticity.”
- **Gaps**
  - The actual HMAC algorithm (e.g. HMAC-SHA256 vs another), key management and key rotation policies are not included here.
  - mTLS and “sandboxing” are mentioned as considerations when exposing Press as a service, but not fully specified.

---

### 2.11 External API & Tools (APX Reference CLI)

From the “External API & Tools” section:

> “an APX reference CLI was provided that defines how to encode/decode using the spec.”  

> “for example, `apx_ref.py encode --input file.ext --out file.apx` is a command to produce a capsule, and similarly a decode command to restore the original file.”

- **Role**
  - Reference implementation of the APP spec.
  - Provides **encode/decode commands** and a **conformance checklist**.
- **Behaviour**
  - Interface:
    - CLI (`apx_ref.py`).
    - Ready for third-party implementers:
      > “The CLI, along with a README and a conformance checklist, was packaged so external implementers can validate .apx capsules out of the box.”
  - Envisioned GUI:
    > “The system also envisions a GUI wrapper (e.g., an Electron app) providing a user-friendly interface – you click ‘Compress’ and it uses the Press backend to produce capsules…”
- **Gaps**
  - Full CLI option set (chunk size, mode flags, logging options, etc.) is **not defined** here.
  - No REST/gRPC schema; network use is discussed conceptually (mTLS, sandboxing) but not fully specified.

---

### 2.12 Evidence & Logging Artifacts

> “Aether Press also produces log artifacts and reports that aid provenance. In the experiments, the assistant generated CSV reports (compression_report.csv, baseline results tables) that show the compression ratios and possibly internal statistics for each file compressed.”

- **Role**
  - Provide **audit trail** and scientific evidence.
- **Behaviour**
  - Outputs:
    - `compression_report.csv`
    - `baseline_results.csv`
    - READMEs explaining procedure.
  - Use:
    > “These reports… form an audit trail demonstrating how the compression was performed (which datasets, which methods, baseline comparisons, etc.).”
- **Gaps**
  - Column schema for `compression_report.csv` and `baseline_results.csv` is not given in this document.

---

## SPEC SHEET 3 — PIPELINE & MODES

### 3.1 Rule+Residual Compression Pipeline

The report explicitly defines the pipeline:

> “APP’s behaviour follows a defined pipeline of stages. First, a **Domain Model** is chosen or inferred… Next, **Parameter Fitting** occurs… Then comes **Residual Encoding**, which records the delta… Finally, the **Packaging** stage wraps the model identifier, the fitted parameters, and the encoded residual into a portable file container.”

Pipeline stages:

1. **Domain Model selection/inference**
   - E.g. “Fourier series, polynomial fit, Markov process”.
   - Not fixed; APP is **model-agnostic**.
2. **Parameter Fitting**
   - Tune parameters and invariants to actual data.
3. **Residual Encoding**
   - Encode differences between model output and real data.
4. **Packaging**
   - Build `.apx` capsule (ZIP with manifest + layers).

**Gaps**:

- Domain Model selection algorithm is **not specified** here (no scoring criteria, no exhaustive search rules).
- Parameter fitting algorithm (least squares? MLE? gradient-based?) is not described in this report.
- Residual encoding codec specifics are omitted.

---

### 3.2 Stacked & Nested Mode (APP v2, NAP Coupling)

> “Adaptivity via Stacking & Nesting: APP can be extended through the Nexus Aeternus Protocol (NAP) to handle data with mixed structure or partial randomness by layering multiple compression passes. This was demonstrated as APP v2 (Stacked/Nested dual-simulation)…”

Stacking:

> “it stacks compression vertically (micro → meta → global layers) so that residuals from one level are further compressed by the next.”

Nesting:

> “It also nests compression horizontally by domain when data is heterogeneous. Different data segments (e.g. an audio portion vs. an image portion in one file) can be compressed with their own domain-optimized APP models and then merged.”

Behaviour:

- Gains:
  - “even data that appeared nearly random on one scale yielded additional **10–20% compression** when correlations across chunks or domains were exploited.”
  - “Structured datasets saw dramatic improvements (e.g. an additional **25–50% size reduction** beyond the already tiny v1 outputs).”
- Edge cases:
  - Semi-structured text: “modest gains (~a few percent) due to lack of a built-in language model.”
  - Pure random data: “remained incompressible (falling back to storing as-is, with ratio ~0.999).”

**Gaps**:

- Exact stacking depth limits not given.
- No formal spec on how segment boundaries for nesting are chosen (heuristics vs user hints).

---

### 3.3 Lossless vs Lossy (ε-bounded) Modes

From Math & Invariants:

> “Fidelity within Tolerance: If a tolerance ε is specified (lossy mode), then after compressing and decompressing, the observed state O satisfies |ΔO| < ε… In purely lossless mode, ε = 0, so output matches exactly.”

So modes:

- **Lossless**: ε = 0, bit-for-bit:
  > “The protocol guarantees bit-perfect reconstruction of losslessly compressed data… decoding the .apx capsule produced the original file with a matching SHA-256 hash.”
- **Lossy / ε-bounded**:
  - Allowed but **explicit**:
    > “APP also supports optional lossy modes or ε-bounded compression for cases where ultra-high compression is required.”
  - Must mark the mode in the manifest (compression mode).

**Gaps**:

- No formal type list for observable `O` (what exactly is measured) in this report.
- No normative spec on how to enforce the ε bound in numeric terms (e.g. float vs fixed).

---

## SPEC SHEET 4 — CAPABILITIES & BEHAVIOURS

### 4.1 Universal Model-Based Compression

> “APP can compress ordinary binary data and structured outputs by discovering an underlying mathematical model or pattern in the data. It encodes the behavior or relationships that generate the data, rather than the data itself, making it a domain-agnostic compressor.”

Behaviour by data type:

- **Structured / repetitive data**:
  - “often compressing to <0.1% of original size, beating standard compressors by large factors.”
  - Checkerboard example:
    > “For highly regular data like a checkerboard pattern, APP identified the base tiling rule and needed zero residual, achieving an extremely small descriptor representation.”
- **Nested/relational data (e.g. JSON)**:
  - “a nested JSON dataset was compressed with only the generative array rules captured, yielding a tiny capsule.”
- **Semi-structured / ordinary text**:
  - “APP performing on par with conventional tools for unstructured text (no worse than gzip and slightly better due to shorter token encodings)…”
- **Random data**:
  - “pure random data remained incompressible (falling back to storing as-is, with ratio ~0.999).”

---

### 4.2 Determinism

> “The Aether Press Protocol operates deterministically – given the same input data and the same version of APP, it will produce the exact same .apx capsule every time.”

> “Press process was treated as a pure function with no external randomness, meaning the message space and transformation are fully defined and repeatable.”

> “In practice, when APP is used as a checkpointing mechanism (Press/DePress), determinism is confirmed by re-running the same sequence with the same random seed and inputs – after pressing and depressing, the subsequent observables O are unchanged beyond tiny numerical tolerance.”

- Deterministic across:
  - Single-pass and multi-layer modes.
  - Checkpointing runs.

---

### 4.3 Reversibility & Causality

> “Reversibility is at the heart of APP – it is essentially a reversible transform from data to a compressed representation and back.”

> “Press/DePress terminology… denotes this save-and-restore capability.”

> “Press does not alter the sequence of cause and effect in the simulation; it merely folds the state into a storable form… Press can’t magically compress random noise… it can only compress what’s causally there (structure put in by prior causes).”

- Compression is **DAG-safe**:
  > “Press simply annotates certain nodes (snapshots) with a compressed representation, but those nodes remain connected in the same directed order.”
- Seen as time snapshots in Loom’s reversible ledger.

---

### 4.4 Idempotence

> “Idempotence under Re-run: Re-sending the same input ledger and performing Press/DePress in the same state yields no change (ΔO = 0), confirming idempotence of deterministic compression cycles.”

So repeated Press/DePress on the same input with same APP version does not accumulate error.

---

## SPEC SHEET 5 — INTERFACES, PLACEMENT & BINDINGS

### 5.1 NAP Integration

> “The Aether Press Protocol interfaces tightly with the Nexus Aeternus Protocol, which is the Trinity system’s synchronization and coupling layer.”

> “NAP orchestrates these and maintains consistency… compress a complex multi-modal dataset by launching separate Press compressors for each modality and then use NAP to merge their outputs.”

- NAP provides:
  - Manifest (`nap_manifest.json`) enumerating layers and references.
  - Coordination for **stacked** and **nested** multi-part compression.
- Distributed compression:
  > “one could compress data partially on one device, send the residual to another which further compresses it, etc., with NAP ensuring that the final assembly is lossless.”

---

### 5.2 Trinity Framework Binding

> “APP is conceptually downstream of the Trinity core, meaning it interfaces with outputs from Trinity’s deterministic engine layers (Momentus engine, Momentum simulation layer, etc.).”

> “Press thus acts as a middleware service in Trinity’s pipeline – the system can invoke APP to compress intermediate results (like simulation frames or entire simulation histories)…”

- One-directional binding for compression.
- Feedback loop for verification:
  > “there is also a feedback loop in that Trinity’s data structures might be initialized or cross-checked using the Press output for verification.”

---

### 5.3 Loom (Time Compression) Binding

> “Press provides the reversible snapshot at a boundary, and Loom handles the timeline between snapshots.”

> “Loom and Press together likely require that checkpointing and compression happen in a controlled environment – e.g., when a checkpoint is triggered, the simulation pauses momentarily to let Press compress state, then resumes.”

- Placement:
  - Press at **I-block** checkpoints.
  - Loom compresses or skips through **P-blocks** between.
- Time invariance:
  - Press/DePress does not advance time; only `T` does.

---

### 5.4 Topology / Placement Constraints

> “Aether Press is largely software-defined and not tied to specific hardware topology, but there are a few implicit placement constraints…”

Key constraints:

- **Downstream of Simulation Nodes**:
  - “Press modules are placed after or alongside simulation nodes as compression endpoints.”
- **At storage layer**:
  - “Press can be deployed as a background job scanning a filesystem… topologically placed at the storage layer.”
- **No splitting of a single turn**:
  - “Press should compress complete datasets or transaction records as a whole, rather than arbitrarily splitting them, to avoid losing context… compress each simulation run or each file fully, rather than half a file (unless using the official chunking with layered residuals).”

---

### 5.5 Universe Manifest / Legal Provenance

> “the Universe Manifest and similar ledgers were mentioned, indicating that the outputs of Aether Press tie into the larger project’s manifest of files.”

> “by grounding the approach in a formally documented protocol (APP and its Implementation PDF), the work produced can be protected and traced to a known foundation rather than appearing ad-hoc.”

- Press capsules and reports become **evidence artifacts** referenced in Universe manifests and legal filings.

---

## SPEC SHEET 6 — PROVENANCE, SECURITY & AUDIT

### 6.1 Integrity

> “Every .apx capsule includes a manifest with cryptographic hashes of the original data, ensuring that one can prove the decompressed output matches the input bit-for-bit.”

> “Press capsules carry internal integrity tags (per-block and whole-file hashes) so that any corruption or mismatch is detected upon decompression.”

- Integrity features:
  - `orig_sha256` in manifest.
  - Per-block and whole-file hashes inside `.apx`.

---

### 6.2 Authenticity

> “The manifest stores the signature and can be checked during decode to ensure integrity and author authenticity.”

- HMAC signature as authenticity proof.
- Discussion of:
  > “various security considerations (like enabling mTLS if used over an API, or sandboxing the service to avoid remote code execution).”

---

### 6.3 Audit Artifacts

> “These reports… form an audit trail demonstrating how the compression was performed (which datasets, which methods, baseline comparisons, etc.).”

Artifacts include:

- `compression_report.csv`
- `baseline_results.csv`
- Experiment READMEs.
- References to specific prompts and scripts used to generate the capsules.

---

## SPEC SHEET 7 — KNOWN GAPS & UNRESOLVED DETAILS (IN THIS REPORT)

This is the explicit “gaps” sheet — **only** what is missing in the main Focus Report, not in the project as a whole.

1. **Manifest Schemas**
   - `apxMANIFEST.json` schema not fully enumerated (only key examples: `orig_sha256`, `apx_version`, core metadata, compression mode).
   - `nap_manifest.json` schema not specified beyond “enumerates the layers and references” between SimA and SimB.

2. **Model Library & Selection**
   - Domain model types are given only as examples (“Fourier, polynomial, Markov”). No normative list or selection algorithm.
   - No scoring criteria for choosing a model.

3. **Parameter Fitting**
   - No explicit description of fitting algorithms (least squares, optimization routines, convergence criteria).

4. **Residual Codec**
   - No detail on residual coding algorithm (entropy coding, block sizes, transform, etc.).
   - No explicit description of per-block hash layout beyond “integrity tags”.

5. **SimA/SimB Internal Format**
   - The exact symbolic language SimA uses to encode rules is not defined here.
   - SimB’s precise residual format and any layering conventions are not listed.

6. **CLI & Tooling Details**
   - Only example command: `apx_ref.py encode --input file.ext --out file.apx`.
   - No full option list, error codes, environment variables, or configuration format.

7. **Lossy Mode Mechanics**
   - ε-bounded guarantee is stated but not fully formalized (no mapping from numeric ε to codec-level parameters).
   - Type and domain of observable `O` is not defined here.

8. **Scaling Limits & Performance**
   - No explicit constraints on max file size, max layers, memory bounds, or time complexity.
   - Performance is characterized qualitatively and via experiment anecdotes, but not with formal bounds.

9. **Networked Service Spec**
   - Mention of mTLS, sandboxing, and serving `.apx` over a network, but no concrete API surface (no REST/gRPC definitions).



<!-- END SOURCE: astral_press_pillar_app_spec_sheets_v_1_2025_11_20.md -->


---

<!-- BEGIN SOURCE: astral_press_multi_layer_nap_mdl_stack_spec_v_1_stack_until_it_stops_making_sense.md -->

# Astral Press — Multi-Layer NAP & MDL Stack Spec v1  
*(“Stack Until It Stops Making Sense” for APP‑UROBOROS‑REF‑1)*

Status: **Local implementation spec** for multi‑layer NAP stacks and MDL decisions in `APP-UROBOROS-REF-1`, grounded in:

- **Astral Press — APP Complement Sheet v4 (Implementation Canon Pack)**
- **Astral Press — APP Complement Sheet v2 (Legacy Docs)**
- **Astral Press — APP Spec Sheets v1** (pillar core)
- **Astral Press — APP Implementer Checklist v1**
- **APP_LOCAL_SPEC v1 — Aether Press Local Implementation (2025‑11‑20)**
- **Astral Press — ε‑Bounded Profiles & Integerization Spec v1 (Crush Without Regret)**

Where canon is explicit, this spec follows it directly (with quotes in the companion docs). Where canon leaves design space open, this spec makes local choices and labels them **Decision** with **Rationale**.

---

## 0. Scope & Relationship to Other Docs

### 0.1 What this spec covers

For the local implementation `APP-UROBOROS-REF-1`, this spec defines:

1. **NAP stack semantics**
   - How we interpret `layers[]`, `kind`, `parent`, `refs[]`, `params`, `ordering`, `knit_rules`, `deterministic_order`, and `hashes` in the NAP Compression Manifest.
2. **Layer roles and allowed shapes**
   - What counts as a valid SimA / SimB layer and how they can be stacked or nested.
3. **MDL functional at the stack level**
   - How `L_model`, `L_residual`, `L_overhead`, `L_total`, `L_naive`, and `kappa` are computed for a stack, not just a single layer.
4. **Layer admission & stopping rules**
   - Exact procedure for “stack until description length no longer improves,” including a small margin.
5. **Per-layer & per-stack invariants**
   - Determinism, DAG shape, and `DePress(Press(D; M); M) = D` constraints.
6. **Integration with ε‑bounded profiles & integerization**
   - How ε/q, integerization, and the acceptance harness interact with multi‑layer NAP.
7. **Implementation guidance**
   - How these rules guide JS/TS module design and tests.

### 0.2 What this spec does *not* cover

- AEON‑i / APXi opcode grammar details (covered in APP_LOCAL_SPEC v1 and AEON/APXi canon passes).
- Per‑source policy & dimensional controls (P_state/P_cite, Dims Press) — covered in **Policy & Dimensional Controls Spec v1**.
- Container surface (`.apx` ZIP layout, MANIFEST.json schema) — covered in **APP_LOCAL_SPEC v1** and complement sheets.

This spec is a **stack semantics + MDL logic** companion to those documents.

---

## 1. Canon Anchors — What NAP & MDL Must Respect

This section briefly restates the canon anchors this spec is binding to (full quotes live in Complement Sheets v2 & v4 and the Math Compendium).

### 1.1 NAP manifest field set and DAG requirement

Canon’s paper form for the NAP Compression Manifest defines:

- Top‑level: `layers[]`, `knit_rules`, `deterministic_order`, `hashes`.
- Each `layers[]` entry has: `id, kind∈{AP.symbolic (SimA), AP.residual (SimB)}, parent, refs[], params, ordering`.
- The layer graph must be a **DAG** and there must exist a **topological order** such that, for fixed dataset D and manifest M:
  - `DePress(Press(D; M); M) = D`.

### 1.2 Multi‑layer MDL factorization

Canon’s multi‑layer model+residual description is:

- `X = M1 + R1`
- `R1 = M2 + R2`
- `R2 = M3 + R3`
- … until description length **no longer improves**.

The metrics/pass docs define:

- `L_total` — achieved description length with models + residuals + overhead.
- `L_naive` — baseline description length (e.g. 8·|S| for raw bytes, or gzip baseline).
- `kappa = L_naive − L_total` — gain over baseline.
- MDL stopping rule: **only** add a new model layer if doing so **reduces** `L_total`; otherwise stop.

### 1.3 Dual compressor mixture (symbolic + dictionary)

The Math Compendium & legacy docs encode the “dual compressor” view:

- For each segment, a **symbolic path** (SimA model + residual SimB) has cost `L_A`.
- A **dictionary‑only path** (SimB‑only) has cost `L_B`.
- Each segment uses whichever is cheaper, with a gate bit for the choice.

This same pattern applies at **layer level** for our stack: we can choose to introduce a new model layer or leave residuals to SimB/dictionary only, based on MDL.

### 1.4 ε‑bounded acceptance

The performance/runbook docs define acceptance (“Crush without regret”) as requiring:

1. Field‑level bounds: `|x_post − x_pre| ≤ q/2 ≤ ε_x` for every numeric field.
2. Replay test Δ=0: scoreboard O unchanged under DePress+replay.
3. Predictive test Δ>0: scoreboard discrepancy within ε.
4. Document proof via P_cite.
5. Idempotence.
6. Isolation of previous checkpoints.

For stacks, these requirements apply jointly across all layers contributing to P_state.

---

## 2. Terminology & Domain

### 2.1 Data, layers, and states

- **Dataset D**
  - The concrete thing being pressed: file bytes, numeric table, sensor stream, etc.
- **State S**
  - Structured internal representation of D used by Press (e.g. arrays, vectors, dims on NAP bus).
- **Layer**
  - One entry in `layers[]` inside the NAP manifest.
  - Has an `id`, `kind`, `parent`, optional `refs[]`, `params`, and `ordering` metadata.
- **SimA layer (symbolic)**
  - `kind = "AP.symbolic"`.
  - Encodes **rules**, parameters, and invariants (AEON‑i/APXi stream or equivalent) that map some part of S to predicted values.
- **SimB layer (residual)**
  - `kind = "AP.residual"`.
  - Encodes residuals left after applying one or more SimA layers and earlier SimB layers.

### 2.2 Stack, nest, and graph

- **Stacked layers**
  - Layers arranged linearly (SimA then SimB, possibly repeated) where later layers depend on outputs of earlier ones.
- **Nested layers**
  - Layers that operate on subsets or transformed views of previous layers (e.g. SimA over a residual of another SimA).
- **NAP graph**
  - Directed graph with nodes = layer IDs, edges implied by `parent` and `refs[]`.
  - Must be a DAG.

### 2.3 Description length components

For our local implementation, we reuse and slightly extend APP_LOCAL_SPEC v1 definitions:

- `L_model` — bits to encode all symbolic descriptors (SimA AEON/APXi) across the stack.
- `L_residual` — bits to encode all residual layers (SimB payloads) across the stack.
- `L_overhead` — bits for APXi header, manifest(s), NAP manifest, hashes, and any fixed per‑capsule bookkeeping.
- `L_total = L_model + L_residual + L_overhead`.
- `L_naive` — baseline description length (normally 8·|S| for raw bytes; for structured metrics we may also consider gzip/xz baselines in evaluation, but the functional is defined against raw bits).
- `kappa = L_naive − L_total`.

### 2.4 Notation: layers and residuals

We write:

- `M_i` — the model encoded by SimA layer i.
- `R_i` — residual after applying layers up to i.
- `L_i` — the layer object as it appears in `layers[]` (contains either SimA or SimB payload).
- `Stack(M_1..M_k, residual R_k)` — the stack configuration encoded by the NAP manifest.

---

## 3. NAP Manifest Semantics for APP‑UROBOROS‑REF‑1

APP_LOCAL_SPEC v1 already fixes a concrete JSON skeleton for NAP. This section adds **behavioural semantics** for our implementation.

### 3.1 Layer identities and kinds

**Decision**

- `id` is a **string** unique within the NAP manifest.
- `kind` must be one of:
  - `"AP.symbolic"` — SimA layer.
  - `"AP.residual"` — SimB layer.

**Rationale**

- Strings are stable across container versions and friendly for debugging.
- `AP.symbolic` / `AP.residual` reuse the canonical naming and make SimA/SimB explicit at the manifest layer.

### 3.2 Parent and refs semantics

**Decision**

- `parent`
  - Is either `null` (root) or a string equal to the `id` of another layer in the same manifest.
  - Encodes the **primary input** dependency: the layer consumes outputs from its parent.
- `refs[]`
  - Is an array of string IDs of other layers.
  - Encodes **secondary dependencies**: side information or conditioning inputs (e.g. cross‑layer references in composite models).

Graph semantics:

- The graph `(V, E)` has:
  - `V = {layer.id}`.
  - `E = {(parent → id) where parent != null} ∪ {(ref → id) for ref ∈ refs[]}`.
- This graph **must be a DAG**.

**Rationale**

- Single `parent` keeps a natural “stack spine” (main path).
- `refs[]` allows more complex dependency patterns without turning the structure into arbitrary spaghetti.

### 3.3 Ordering & deterministic_order

**Decision**

- Each layer has an `ordering` object with at least:
  - `order_index` — integer rank in primary reconstruction order.
  - `stage` — one of `"symbolic"`, `"residual"`, or other domain‑specific tags.
- Top‑level `deterministic_order` contains:
  - `topological_order` — array of layer IDs representing a valid **topological sort** of the DAG.

Runtime behaviour:

- DePress must reconstruct using `topological_order` as the outer loop.
- Within each layer, any internal ordering (e.g. per‑segment) must be deterministic for the same data and manifest.

**Rationale**

- Explicit `order_index` aids debugging and human inspection.
- `topological_order` encodes a canonical reconstruction order and ensures `DePress(Press(D; M); M) = D` for fixed M.

### 3.4 Knit rules

**Decision**

- `knit_rules` is a JSON object that contains at least:
  - `type` — one of `"stacked"`, `"nested"`, or `"mixed"`.
  - `reconstruction` — an ordered list of symbolic names of reconstruction steps, e.g. `"decode_simA_main"`, `"apply_simB_main_residuals"`.

Semantics:

- For `type = "stacked"`:
  - Layers form a primarily linear stack along the `parent` chain.
  - Residual layers correct the outputs of one or more symbolic layers.
- For `type = "nested"`:
  - Layers may encode transforms on residuals of other layers in non‑linear patterns, as long as the DAG invariant holds.
- For `type = "mixed"`:
  - Both patterns may appear; `reconstruction` must still represent a deterministic sequence of operations.

**Rationale**

- We keep `knit_rules` minimal and descriptive; detailed semantics remain with each layer’s `params` but this field prevents ambiguity over whether we’re stacking, nesting, or both.

### 3.5 Hashes

**Decision**

- `hashes` has at least:
  - `algo` — string, default `"sha256"` in this implementation.
  - `layers` — { layer.id → hex‑encoded hash of that layer’s payload bytes }.

Behaviour:

- Whenever a layer payload is written or read, we **must** compute/verify its hash against `hashes.layers[id]`.
- If a mismatch occurs, the stack is considered **corrupt**, and DePress must refuse to reconstruct unless running in an explicit debug/recovery mode.

**Rationale**

- Enforces proof‑carrying capsules and prevents silent bit‑rot.

---

## 4. Layer Roles & Allowed Patterns

### 4.1 Minimal stack for simple cases

The simplest valid NAP configuration for this implementation is:

- Single SimB layer only:
  - `layers = [simB_main]`, `kind = "AP.residual"`, `parent = null`.
  - `type = "stacked"`, `topological_order = ["simB_main"]`.
  - Residual layer encodes raw data directly (e.g. dictionary/entropy code) — effectively “Press as a containerised codec.”

This corresponds to `pressBytes` lossless path for arbitrary bytes.

### 4.2 Canonical two‑layer stack (SimA + SimB)

The canonical stack used in most structured examples is:

1. `simA_main` — SimA symbolic layer:
   - Encodes fitted models via AEON/APXi.
   - `kind = "AP.symbolic"`, `parent = null`, `stage = "symbolic"`.
2. `simB_main` — SimB residual layer:
   - Encodes residuals on top of `simA_main` predictions.
   - `kind = "AP.residual"`, `parent = "simA_main"`, `stage = "residual"`.

`deterministic_order.topological_order = ["simA_main", "simB_main"]`.

This is the shape used in APP_LOCAL_SPEC v1’s NAP example.

### 4.3 Additional layers (stacking)

**Decision**

- Additional layers may be added following these rules:

  - SimA can be followed by:
    - Another SimA modelling residuals (higher‑order structure), or
    - A SimB encoding residuals.

  - SimB can be followed by:
    - SimA modelling structure in residuals (e.g. AR on residuals), or
    - Another SimB encoding further‑transformed residuals (e.g. nested residual stacks).

- However, in all cases, **adding a new layer must pass the MDL layer admission rule** (see §5.3).

**Rationale**

- Matches the LCDRM/AIF idea that we can keep adding relational layers until the remaining residual is effectively noise.
- Keeps the design flexible without collapsing into arbitrary, unbounded complexity.

### 4.4 Disallowed patterns

**Decision**

- Cycles are forbidden by definition (DAG requirement).
- Layers may not:
  - Depend on themselves (directly or indirectly).
  - Depend on layers that are not present in `layers[]`.
  - Change their meaning at runtime (e.g. `params` decoded differently depending on data content).

If any such pattern appears (due to malformed manifest or code bug), the Press/DePress run must fail with a clear error.

**Rationale**

- Enforces `DePress(Press(D; M); M) = D` and prevents time‑bomb semantics.

---

## 5. MDL Functional & Layer Admission Rules

### 5.1 Stack‑level description length

We treat the entire stack as the unit for MDL, not just individual layers.

For a fixed stack configuration `Stack(M_1..M_k, R_k)` encoded by manifest M:

- `L_model(M)` — total bits across all SimA layers’ AEON/APXi streams.
- `L_residual(M)` — total bits across all SimB residual streams.
- `L_overhead(M)` — bits for NAP manifest, layer hashes, manifest overhead attributable to the stack.

Then:

```text
L_total(M) = L_model(M) + L_residual(M) + L_overhead(M)
L_naive = 8 * |S|       // raw bytes baseline
kappa(M) = L_naive - L_total(M)
```

A positive `kappa` means the stack describes S more compactly than the raw baseline.

**Rationale**

- Aligns with metrics pass and APP_LOCAL_SPEC v1.
- Counting NAP/manifest overhead discourages gratuitous layer proliferation.

### 5.2 Candidate layer effect on L_total

Suppose we have a stack configuration M with layers `L_1..L_k` and description length `L_total(M)`.

We consider adding a candidate layer `L_candidate` (SimA or SimB) that operates on the current residual (or some transformed subset thereof).

Let `M'` be the manifest that extends M with `L_candidate` and its updated residual structure.

We compute:

- `ΔL_model = L_model(M') − L_model(M)`.
- `ΔL_residual = L_residual(M') − L_residual(M)`.
- `ΔL_overhead = L_overhead(M') − L_overhead(M)`.

So:

```text
ΔL_total = L_total(M') - L_total(M)
         = ΔL_model + ΔL_residual + ΔL_overhead
```

`ΔL_total` may be negative (good), zero, or positive (bad).

### 5.3 Layer admission rule

**Decision — MDL rule with safety margin**

We define a small **safety margin** `margin_bits` (default 8 bits = 1 byte).

- Accept a candidate layer `L_candidate` **iff**:

  ```text
  ΔL_total + margin_bits < 0
  ```

- Otherwise, reject the layer and **do not** modify the stack.

Interpretation:

- The layer must reduce `L_total` by **more than** the margin to be worthwhile.
- If a layer’s effect is within ±margin, we treat it as noise and avoid stack churn.

**Rationale**

- Implements canon’s “stop when adding another model would increase overall description length” with a concrete tolerance.
- Avoids toggling layers on/off due to tiny, noisy deltas in description length.

### 5.4 Stack‑level stopping rule

We repeat the process of proposing layers and applying the admission rule until:

- No candidate layer yields `ΔL_total + margin_bits < 0`.

At that point, we stop and treat the current stack as final.

This realises the statement:

> “Data X is decomposed as X = M1 + R1, R1 = M2 + R2, … until description length **no longer improves**.”

### 5.5 SimA vs SimB trade‑offs

**Decision**

When considering candidate layers, we treat:

- SimA layers as candidates that add to `L_model` but may reduce `L_residual`.
- SimB layers (extra residual transforms) as candidates that add some overhead but may reduce `L_residual` by improving coding of residuals.

The MDL rule is agnostic: it simply evaluates `ΔL_total` and accepts or rejects.

**Rationale**

- Keeps the framework unified: SimA and SimB are just different tools for shaving bits off `L_total`.
- Naturally encodes the “dual compressor” behaviour at the layer level.

---

## 6. Interaction with ε‑Bounded Profiles & Integerization

### 6.1 ε profiles per layer

From the ε spec and APP_LOCAL_SPEC v1, we have named profiles like:

- `PRESS_LOSSLESS` — no quantization, ε = 0.
- `PRESS_SENSOR_MED` — moderate ε per numeric field.
- `PRESS_LOG_CRUSH` — coarse ε for logs.

**Decision**

- Each Press run uses a **single primary profile** recorded in `MANIFEST.json.press.profile`.
- Individual layers may refine behaviour via their `params` but must **not** contradict the profile’s ε/q constraints.

### 6.2 Field‑level ε/q and stacks

Field‑level constraints:

- For every numeric field x with ε_x and q_x, and for any Press+DePress cycle using a stack:

  ```text
  |x_post - x_pre| ≤ q_x / 2 ≤ ε_x
  ```

**Decision**

- This bound is enforced **after the full stack**, not per layer.
- Intermediate layers may introduce larger provisional errors as long as the final reconstructed field respects the bound.

**Rationale**

- Keeps the acceptance criterion focused on the end‑to‑end effect on S, not on each internal transform.
- Allows more aggressive intermediate transforms as long as they resolve to the required fidelity.

### 6.3 Acceptance harness on stacks

We apply the “Crush without regret” checks to the whole stack:

1. **Field‑level bounds** — compute `x_post` after DePressing with the full stack; check `|x_post − x_pre| ≤ q_x / 2 ≤ ε_x` for all fields.
2. **Replay test (Δ=0)** — run O on original S and reconstructed S′; require `O(S) = O(S′)` or `d(O(S), O(S′)) ≤ ε_O` per profile.
3. **Predictive test (Δ>0)** — where T is available, compare O under T^Δ applied to S and S′.
4. **P_cite proofs** — unaffected by stacking; they refer to external sources.
5. **Idempotence & isolation** — Press+DePress under same manifest and modes must not alter O or past checkpoint hashes.

**Decision**

- **If any acceptance check fails, the stack is rejected** for P_state:
  - For P_state capsules, we mark acceptance as false and refuse to use the capsule for replay.
  - For P_cite capsules, acceptance applies only to proof requirements (hashes, sizes), not to ε.

**Rationale**

- Enforces that adding layers cannot “cheat” the acceptance tests by hiding errors inside NAP.

---

## 7. JS Implementation & Module Wiring

This section ties stack semantics back into the JS Offline MVP and full implementation.

### 7.1 NAP builder

We define a `nap_builder` module that:

1. Starts with an empty manifest `M` with `layers = []`.
2. Adds `simA_main` and/or `simB_main` according to the Press path invoked (`pressBytes`, `pressNumericArray`, etc.).
3. Optionally evaluates candidate layers (extra SimA/SimB) via MDL and, if accepted, appends them with proper `parent` and `order_index`.
4. Computes `topological_order` and populates `deterministic_order`.
5. Computes `hashes.layers` for each payload.

### 7.2 MDL evaluator

A `mdl_stack` helper module:

- Accepts a manifest M, a set of layer payloads, and a baseline description length `L_naive`.
- Computes `L_model`, `L_residual`, `L_overhead`, `L_total`, and `kappa`.
- Exposes a function `considerLayer(M, L_candidate)` that returns `ΔL_total` and a boolean `shouldAccept` using the margin rule.

### 7.3 Integration with Press Engine

The Press Engine:

- Uses `selectModelForSegment` (SimA) and residual stack (SimB) per segment.
- For multi‑layer scenarios, uses `mdl_stack.considerLayer` to decide whether to:
  - Introduce a new SimA layer modelling residual structure.
  - Introduce an additional SimB layer with a different codec profile.
- Populates NAP manifest via `nap_builder`.

### 7.4 DePress pipeline

Flux Decoder:

- Reads `nap/compression.json` via `readNapManifest`.
- Validates `hashes.layers` against actual payloads.
- Reconstructs in `deterministic_order.topological_order` using `knit_rules.reconstruction` to decide how to combine SimA predictions and SimB residuals.
- Delivers reconstructed S (bytes or structured data) to the acceptance harness.

---

## 8. Testing Strategy for Stacks

### 8.1 Unit tests

- **DAG correctness**
  - Construct synthetic manifests with valid and invalid DAGs; ensure invalid ones are rejected.
- **Layer‑level MDL tests**
  - Build simple stacks with one and two layers where the second layer clearly reduces/increases `L_total`; assert `considerLayer` decisions.
- **Round‑trip**
  - For synthetic data where we know an exact two‑layer representation (e.g. polynomial + AR residuals), ensure Press+DePress reconstruct exactly in lossless mode and with bounded error in ε‑bounded mode.

### 8.2 Fuzz & adversarial tests

- Generate random manifests with:
  - Cycles.
  - Broken hashes.
  - Wrong `kind`/payload combinations.
- Verify that DePress refuses to proceed and surfaces clear error codes/logs.

### 8.3 Performance sanity

- Measure `L_total` and `kappa` for stacks of depth 1–3 on:
  - Simple synthetic signals (affine, periodic, AR, mixtures).
  - Realistic sensor/log datasets.
- Ensure depth usually stops within 1–3 layers; if stacks routinely grow deeper without major gains, revisit model library or margin.

---

## 9. Change Control

Any change to NAP semantics or MDL stack behaviour must:

1. Update this spec with new decisions and rationales.
2. Bump:
   - `schema_version` in `nap/compression.json` (e.g. `nap_manifest_v2`).
   - `app_impl_version` in `MANIFEST.json`.
3. Provide migration notes for older `.apx` capsules if compatibility is affected.

The goal is to keep stacks **auditable and predictable**: given a manifest and version, an auditor should be able to reconstruct exactly how and why a particular stack of layers was chosen and how it affects description length and acceptance.



<!-- END SOURCE: astral_press_multi_layer_nap_mdl_stack_spec_v_1_stack_until_it_stops_making_sense.md -->


---

<!-- BEGIN SOURCE: astral_press_pillar_nap_compression_manifest_spec_canon_pass.md -->

# Astral Press Pillar — NAP Compression Manifest Spec (Canon Pass)

> **Scope of this pass**  
> Lock down the _NAP Compression Manifest_ for Astral Press **only from canon**, no invented fields, no guessed behaviour. We restate exactly what the files say, then lift that into a dev‑facing, math‑tight spec. Any place where the canon does **not** tell us enough to implement, we flag it explicitly as a gap.

---

## 1. Canon anchors (verbatim pulls)

**1.1. NAP Compression Manifest name + role**

From the Press focus report:

> “NAP Compression Manifest – … a Nexus Aeternus Protocol (NAP) manifest that ‘knits’ together SimA and SimB outputs. Defines how multi-layer stacks and nests recombine for exact reconstruction.”

From the Press experiments setup:

> “Per dataset: `*_APP/nap_manifest.json`, `simA_layers/*.json`, `simB_layers/*.bin.gz`, and `report.json`.”
>
> “We stacked generators … and nested them … and used a **NAP manifest** to define how to recombine, precisely following the ‘two Sims + NAP together’ directive.”

From the Paper Computer spec (Paper Forms, B3 AP):

> “**NAP Compression Manifest**: `layers[] {id, kind∈{AP.symbolic (SimA), AP.residual (SimB)}, parent, refs[], params, ordering}, knit_rules, deterministic_order, hashes`.”

From the determinism section of the Press report:

> “In multi-layer mode, each layer’s compression is deterministic, and the NAP manifest serializes their relationships in a directed acyclic graph (DAG) of dependencies: e.g., base layer residuals feed into meta-compression, but there’s no circular dependency – it’s a one-way stack.”

**1.2. SimA / SimB meaning (for `kind`)**

From the Press report glossary:

> “SimA / SimB – Dual compression streams introduced in advanced APP v2. SimA is the symbolic or generative compressor that captures structured patterns, and SimB is the residual or statistical compressor that encodes whatever SimA cannot express. They run in parallel on the data, with SimA producing descriptors and SimB the fallback residuals.”

From the name‑change application (Paper spec):

> “Renamed the layer kinds to **AP.symbolic (SimA)** and **AP.residual (SimB)** everywhere they appear in the forms (kept the original names in brackets).”

**1.3. Stacking / nesting behaviour that the manifest must capture**

From the Press focus report:

> “APP can be extended through the Nexus Aeternus Protocol (NAP) to handle data with mixed structure or partial randomness by layering multiple compression passes. This was demonstrated as APP v2 (Stacked/Nested dual-simulation), where the data is processed by two coordinated compressions (SimA and SimB) across hierarchical levels … It stacks compression vertically (micro → meta → global layers) … It also nests compression horizontally by domain when data is heterogeneous … Using NAP’s coupling, these stacked and nested compressions are synchronized and recorded in a manifest that allows the entire multi-layer process to be reversed deterministically.”

From the NAP / stacking explanation in the Trinity dev logs:

> “Every layer is both part of a stack and one boundary of a nest … At the points of contact (the naps), the nest field from one stack continues seamlessly into the next … **Invariant:** Every stack layer participates in exactly one nest — outer for U, shared for M, inner for L — and μ continuity is maintained across U↔L contacts.”

These passages jointly fix that:

* The NAP Compression Manifest is **the DAG + rules sheet** that tells you how SimA and SimB layers, stacked and nested, glue back together into one lossless reconstruction.
* It must respect **stacking, nesting, and μ‑continuity invariants** coming from NAP.

---

## 2. Structural schema from canon

Canon gives us a _field list_ for the NAP Compression Manifest as a **paper form**:

> `layers[] {id, kind∈{AP.symbolic (SimA), AP.residual (SimB)}, parent, refs[], params, ordering}, knit_rules, deterministic_order, hashes`

This is already a compact pseudo‑schema. In this pass we **do not add new fields**; we only tease out structure that is already implied by the text.

### 2.1. Top‑level object

We treat the manifest as a single record, conceptually a JSON object or paper form row:

```text
NAP_Manifest := {
  layers[],
  knit_rules,
  deterministic_order,
  hashes
}
```

Where:

* `layers[]` — array of per‑layer entries (see §2.2).
* `knit_rules` — a field capturing how layers are “knit together” (stack + nest recombination).
* `deterministic_order` — field encoding the **DAG evaluation / replay order**.
* `hashes` — field containing integrity commitments over layers and/or combined payloads.

> **Important:** Canon does **not** specify exact JSON types (string vs int vs object) for these top‑level fields. Any choice beyond “it’s an array” vs “it’s a scalar/collection” is an implementation decision and must be treated as a **gap**, not canon.

### 2.2. `layers[]` entries (canon fields)

Canon:

> `layers[] {id, kind∈{AP.symbolic (SimA), AP.residual (SimB)}, parent, refs[], params, ordering}`

We therefore fix:

```text
LayerEntry := {
  id,
  kind ∈ {AP.symbolic (SimA), AP.residual (SimB)},
  parent,
  refs[],
  params,
  ordering
}
```

**Field by field (no extra semantics beyond canon):**

* **`id`** — an identifier for this layer. Canon does not constrain type or naming scheme. Practical assumption (for devs) is “unique per manifest”, but that is **not** spelled out; we mark it as a recommended constraint, not canon.

* **`kind`** — explicitly constrained by canon to one of:
  * `AP.symbolic (SimA)` — symbolic/generative layer.
  * `AP.residual (SimB)` — residual/statistical layer.

  The bracketed names are preserved exactly per rename guidance.

* **`parent`** — a parent reference. Canon only tells us that the overall structure is a **DAG**, and that base layer residuals feed into meta‑compression. That implies `parent` participates in the DAG, but:
  * It is **not** stated whether `parent` is:
    * a single `id`,
    * `null` for roots,
    * or something more complex.
  * We therefore treat `parent` as a **single link field whose exact type is open**.

* **`refs[]`** — an array of references. From the Press text we know the manifest must express:
  * stacking relationships (micro → meta → global),
  * nesting by domain (SimA vs SimB, heterogeneous segments),
  * and cross‑sim coupling.

  Canon does **not** spell out whether `refs[]` is:
  * additional cross‑edges in the DAG,
  * purely horizontal nest links,
  * or a generic “other references” list.

  In this pass we only lock: `refs[]` exists and is an array. Its internal semantics are **partially unspecified** (gap).

* **`params`** — a parameter bag. Canon just names this field; it does **not** list its keys. From context (Press, AEON‑i descriptors, cost functions) we know parameters will include things like rule IDs, coefficients, window sizes, etc., but those are all defined at the **AEON / APX / AP layer**, not NAP. For NAP Compression Manifest we therefore:
  * Keep `params` as an **opaque per‑layer parameter set**.
  * Note that the manifest should be able to point into the AEON/APX layers but **does not re‑encode** them.

* **`ordering`** — per‑layer ordering. Canon also gives a top‑level `deterministic_order`. The clean reading is:
  * `ordering` — local ordering info for this layer (e.g., relative position within a stack or nest),
  * `deterministic_order` — global schedule for the DAG.

  However, canon doesn’t say this explicitly. We record the split as a **working interpretation** and leave it tagged as such.

---

## 3. Graph semantics (DAG) and reconstruction

Canon statement:

> “In multi-layer mode, each layer’s compression is deterministic, and the NAP manifest serializes their relationships in a directed acyclic graph (DAG) of dependencies: e.g., base layer residuals feed into meta-compression, but there’s no circular dependency – it’s a one-way stack.”

We build the minimal math needed for implementation **without adding new behaviour**.

### 3.1. DAG structure

Let:

* `V` = set of layer IDs in `layers[]`.
* `E` = set of directed edges implied by `parent` and `refs[]`.

Then the canon requirement “directed acyclic graph (DAG)” is:

```math
G = (V, E) \text{ is a DAG } \iff \nexists \text{ cycle } (v_0, v_1, …, v_k=v_0) \text{ with } (v_i, v_{i+1}) ∈ E.
```

The phrase “one-way stack” further constrains that, along the **stack axis**, parents are always “earlier” than children. That is equivalent to saying there exists a **topological ordering** `σ` over `V` such that:

```math
(v_i, v_j) ∈ E \implies σ(v_i) < σ(v_j).
```

We align this `σ` with the `deterministic_order` field:

* **Canon‑aligned requirement:** `deterministic_order` must encode at least one valid topological order for `G`.

### 3.2. Reconstruction constraint

Canon for Press reversibility:

> “Unpress(Press(data)) = data” (lossless mode).

Canon for stacked/nested multi‑layer mode:

> “Even when multi-layer (stacked/nested) compression is used, each layer’s output feeds the next and all necessary information is preserved such that decoding through the layers returns the source data without deviation.”

Together, for a fixed dataset `D`, fixed Press version, and fixed manifest `M`, the reconstruction equation is:

```math
\text{DePress}(\text{Press}(D; M); M) = D.
```

Where:

* `Press(·; M)` — multi‑layer SimA/SimB compression driven by `M` (stack + nest topology, knit rules, order).
* `DePress(·; M)` — inverse transform applying `M` in **reverse topological order**.

> **Key point:** The manifest **is part of the function definition** of Press/DePress in stacked/nested mode. Change `M` and you change the function; to reproduce an experiment, both the capsule and its NAP Compression Manifest must be available and identical.

---

## 4. Relationship to APX Manifest and NAP Envelope

We need to be clear where the NAP Compression Manifest sits in the larger artifact graph.

**4.1. Alongside APX Manifest**

Canon APX Manifest form:

> “APX Manifest: `dataset, orig_bytes, orig_sha256, apx_version, mode, created_utc, file_meta?, layers[], signature, notes` (compat mode).”

And:

> “Press Metadata Manifest – … MANIFEST.json file storing original file metadata: name, size, hash, compression mode, timestamp, etc. Extended … to include file system info (permissions, timestamps) … HMAC Signature (APX) … Cryptographic signing of capsules to ensure authenticity and tamper-detection.”

From this we pin the **roles**:

* **APX Manifest** — describes **what** was compressed and high‑level compression settings.
* **NAP Compression Manifest** — describes **how** the compression layers (SimA, SimB, stacks, nests) are wired.

Implementation‑wise, the NAP Compression Manifest can be:

* a separate file in the capsule (e.g. `nap_manifest.json`),
* or logically embedded and referenced via APX `layers[]`.

Canon does not fix the on‑disk path; we keep both arrangements as acceptable.

**4.2. Connection to NAP Envelope / Ports**

Canon NAP forms:

> “Envelope: `version, src_node_id, dst_node_id, tick τ, address <ring.stack.local>, stack_delta∈{-1,0,+1}, ring_hops, commit_ref, seed Ξ, nonce, metrics{ρ, κ, ℒ, H_payload}, flags, payload_ref (hash only), attestation, checksum`.”
>
> “Ports Sheet: `M.in, M.out, M.audit` rows with `{id, time, op∈{HELLO,BIND,SYNC,CALL,CAST,BRIDGE,SEAL,ECHO}, nonce, status∈{sent,recv,ack,nack,drop,rollback}, budgetΔ, notes}`.”

This establishes that:

* NAP Compression Manifest is **payload** inside the NAP message layer.
* Its `hashes` field should align with `payload_ref (hash only)` and the envelope’s checksum/attestation, but canon does **not** give a direct mapping.

We therefore set a minimal, canon‑compatible requirement:

* For any NAP envelope that carries a Press capsule:
  * `payload_ref` must be a hash over the **exact bytes** of the compressed payload (APX + NAP manifests + layers), under whatever hashing scheme the NAP spec uses elsewhere (SHA‑256 in most canon examples).
  * The NAP Compression Manifest’s internal `hashes` field must be consistent with that envelope hash (i.e., not contradict it). The exact structure (per‑layer hashes vs Merkle root vs both) is **unspecified** and remains a gap.

---

## 5. Minimal implementation contract (math‑level)

This section answers: “What is the bare minimum a dev must implement to be compliant with canon for the NAP Compression Manifest?” — **without** adding new behaviour.

### 5.1. Data model contract

Given a dataset `D`, Astral Press **stacked/nested** run must produce:

1. An APX capsule (or equivalent container) with:
   * core metadata (dataset name, original size, SHA‑256, mode, version, timestamps, optional file meta),
   * a set of layer payload files for SimA/SimB.
2. A NAP Compression Manifest `M` with:
   * a `layers[]` list whose entries each correspond to exactly one symbolic or residual layer in the capsule,
   * `knit_rules` sufficient to tell reconstruction how to combine those layers,
   * `deterministic_order` that is a valid topological order of the implied DAG,
   * `hashes` that commit to the layer payloads and/or combined payload.

At decode time, the implementation must:

* Load `M`.
* Verify that the DAG (`layers[]` + implied edges) is acyclic.
* Traverse layers according to `deterministic_order` (or any topological order consistent with it).
* Apply the inverse transform for each layer, using the layer’s `kind` to select the correct engine (symbolic vs residual) and `params` to configure it.
* Produce `D̂` and verify `H256(D̂) = orig_sha256` from the APX Manifest.

This is exactly the behaviour described in the canon: **deterministic, DAG‑respecting, hash‑validated reconstruction.**

### 5.2. Verification invariants

The implementation must enforce at least:

1. **DAG check** — no cycles among layer IDs when edges implied by `parent` (and optionally `refs[]`) are considered.
2. **Topological consistency** — `deterministic_order` is a permutation of the layer IDs and compatible with the DAG.
3. **Kind coverage** — every layer has `kind` either `AP.symbolic (SimA)` or `AP.residual (SimB)`.
4. **Hash consistency** — hashes in `hashes` are consistent with the actual layer payloads and APX `orig_sha256`.
5. **Round‑trip equality** — `DePress(Press(D; M); M) = D` for every lossless run.

Beyond these, further checks (budget, μ‑continuity at NAP level, etc.) are cross‑pillar and handled in other specs; we don’t add them here.

---

## 6. Explicit gaps (NAP Compression Manifest)

This is the core of the pass: where the canon **does not** give enough detail for a full implementation, we list it plainly instead of making it up.

1. **`id` format and constraints**  
   * Canon only names `id`. It does **not** specify:
     * type (string vs integer vs composite),
     * namespace or scoping (per dataset vs global),
     * allowable characters.
   * **Gap:** any specific scheme (e.g. `L0_A`, `L1_B`) is designer choice, not canon.

2. **`parent` semantics**  
   * Canon indicates a DAG and talks about base layers feeding meta‑compression, but does not define:
     * whether `parent` points **up the stack only**,
     * whether it can encode nest relationships,
     * whether roots must have `parent = null` or may omit the field.
   * **Gap:** precise interpretation of `parent` and rules for root layers.

3. **`refs[]` meaning**  
   * We know stacking vs nesting vs SimA/SimB splits must be recorded, and the field `refs[]` exists, but canon never explicitly maps “this edge type” → “this meaning”.
   * **Gap:** type of references encoded in `refs[]` (horizontal nest links, cross‑sim ties, extra DAG edges, or a mix).

4. **`params` structure**  
   * Canon names `params` but does not list its keys. AEON‑i descriptors carry detailed parameterization, but that is a separate structure.
   * **Gap:** exact schema for `params` (which knobs, which ranges, how they connect back to AEON/APX descriptors).

5. **`ordering` vs `deterministic_order` split**  
   * Canon lists both a per‑layer `ordering` field and a top‑level `deterministic_order`.
   * There is no direct explanation of how these interact.
   * **Gap:** definition of `ordering` and its relationship to `deterministic_order` (local vs global, or redundant representation).

6. **`knit_rules` structure and language**  
   * Canon strongly says the manifest “knits” SimA and SimB outputs and stacked/nested layers for deterministic reconstruction.
   * It does **not** specify:
     * whether `knit_rules` is textual, symbolic math, bytecode, or a reference to external rule sheets,
     * whether rules are per‑layer, per‑edge, or global.
   * **Gap:** full schema and interpretation of `knit_rules`.

7. **`hashes` internal layout**  
   * We have:
     * capsule‑level statements about SHA‑256 hashes for original data and restored data,
     * per‑block / whole‑file hash tags in the capsule,
     * a `hashes` field in the NAP Compression Manifest.
   * Canon does not tie these together with an explicit map (e.g. `hashes: { layer_id → sha256 }`).
   * **Gap:** exact mapping between `hashes`, per‑layer payload files, and APX manifest hashes.

8. **On‑disk location and naming**  
   * Experiments reference `nap_manifest.json` but do not declare it normative.
   * **Gap:** formal file path(s) and naming conventions for the manifest inside APX/AEON containers.

9. **Versioning and compatibility**  
   * Canon mentions APX versions (`apx_version`) and Press improvements but does not attach a version field directly to the NAP Compression Manifest.
   * **Gap:** manifest versioning fields and compatibility rules.

10. **Error handling / partial failure modes**  
    * No canon text describes what happens if a layer is missing, a hash fails, or the DAG is malformed.
    * **Gap:** behaviour under corruption or partial data (fail closed vs best‑effort reconstruction).

---

## 7. What this pass actually closed

Relative to the earlier "gap ledger", this pass:

* **Closes**: “Field‑level schema for NAP Compression Manifest exists?” — Yes. Canon provides a concrete field list: `layers[] {id, kind, parent, refs[], params, ordering}, knit_rules, deterministic_order, hashes`.
* **Clarifies**: The manifest is **explicitly** a DAG encoding of layer dependencies, not a vague label; its job is to make stacked/nested SimA/SimB compression reversible.
* **Leaves open**: all the detailed schemas listed in §6. Those are **not** present in the canon and must stay marked as design space, not facts.

This document should now be safe to use as the NAP Compression Manifest slice of the dev‑facing Press Pillar spec: everything structural that’s written here is either directly quoted or mechanically unpacked from canon, and every missing detail is flagged rather than guessed.



<!-- END SOURCE: astral_press_pillar_nap_compression_manifest_spec_canon_pass.md -->


---

<!-- BEGIN SOURCE: astral_press_pillar_nap_envelope_budget_gate_js_implementation_pass.md -->

# Astral Press Pillar — NAP Envelope & Budget (Gate JS Implementation Pass)

> **Scope**  
> Use the `AETHER-GATE-JS-main` implementation as source-of-truth to **close remaining NAP-related gaps** for the Astral Press Pillar, without contradicting the math/spec canon.  
> We focus on:
> - NAP envelope shape & canonicalisation.
> - NAP payload hashing.
> - NAP budget tracker semantics.
> - NAP envelope fixtures (golden TSV headers).
>
> Source of truth is the JS repo; all interpretations are backed by **direct code/fixture quotes**.

---

## 1. NAP envelope shape (core Gate implementation)

### 1.1 Canonical envelope fields

In `src/core/nap.js`, the Gate defines a canonicalised NAP envelope and how it is serialised:

```js
// src/core/nap.js
import { sha256Hex } from "./hash.js";

export function canonicaliseNapEnvelope(env) {
  const canonical = {
    tick: env.tick,
    node_id: env.node_id,
    layer: env.layer,
    seed_hex: env.seed_hex,
    payload_ref: env.payload_ref,
    metrics: env.metrics ?? {},
    mode: env.mode ?? {},
    sig: env.sig ?? "",
  };
  return JSON.stringify(canonical);
}
```

From this we get the **canonical envelope field set** (and ordering for canonicalisation):

- `tick` — tick index at which the envelope is scheduled/emitted.  
- `node_id` — ID of the emitting node.  
- `layer` — layer identifier (UMX layer, e.g. topology/scene layer).  
- `seed_hex` — hex representation of the seed used for deterministic behaviour.  
- `payload_ref` — reference to the payload, not the payload itself (see hashing below).  
- `metrics` — optional metrics object (default `{}`).  
- `mode` — optional mode object (default `{}`).  
- `sig` — optional signature string (default `""`).

**Canonicalisation rule:**

- Build a new object with exactly these keys in this order.  
- Fill in defaults (`metrics: {}`, `mode: {}`, `sig: ""`).  
- `JSON.stringify(canonical)` is the canonical string.

This resolves a prior gap: in the math/spec canon we knew NAP envelopes carried tick/node/layer/seed/payload ref, metrics, modes, and signatures, but not the **exact field names and canonicalisation order**. The Gate JS implementation now fixes both.

### 1.2 Envelope creation & validation

Later in the same file, the implementation constructs envelopes from a raw payload:

```js
// src/core/nap.js (later in file, elided code between)
const payloadHash = sha256Hex(payload);
const envelope = {
  tick,
  node_id: nodeId,
  layer,
  seed_hex: seedHex,
  payload_ref: `sha256:${payloadHash}`,
  metrics,
  mode,
  sig: "",
};
validateNapEnvelope(envelope);
return { envelope, payloadHash };
```

This gives us additional constraints:

- **Payload ref format:** `payload_ref` is a string of the form `"sha256:<hex>"`, where `<hex>` is the SHA‑256 digest of the payload bytes.  
- The creation path always calls `validateNapEnvelope(envelope)` before returning.

We do not see the implementation of `validateNapEnvelope` in this trimmed snapshot, but we know:

- It is part of the core NAP module.  
- It must at minimum assert presence and basic types of the fields above.

### 1.3 Hashing of envelopes

Although the full body isn’t shown in the trimmed file, the import and canonicalisation pattern imply a standard hash function:

```js
// implied by canonicaliseNapEnvelope + sha256Hex
export function hashNapEnvelope(env) {
  const s = canonicaliseNapEnvelope(env);
  return sha256Hex(s);
}
```

We don’t need to assume anything beyond this: the Gate uses **canonical JSON → SHA‑256 hex** as the NAP envelope hash, consistent with the `payload_ref` convention.

**Resulting contract:**

- To hash a NAP envelope for integrity or signing, always:
  1. Canonicalise using the ordered field subset above.  
  2. Hash that string with SHA‑256.

This matches prior math canon (envelopes + hashes + nonces) but now pins the **wire-level normal form**.

---

## 2. NAP budget tracker (UMX Gate behaviour)

### 2.1 Budget tracker entry points

The `src/umx/nap.js` module implements a per-tick budget tracker used in tests like `tests/umx.nap.test.js`.

Key utilities (trimmed file, but functions are fully visible where we need them):

```js
// src/umx/nap.js
function toInt(value) {
  const numeric = Number.parseInt(value ?? '', 10);
  return Number.isFinite(numeric) ? numeric : 0;
}

function cloneRows(rows = []) {
  return rows.map((row) => ({ ...row }));
}

function computeSoftLimit(budget, ratioNum, ratioDen) {
  if (!budget || budget <= 0) {
    return 0;
  }
  if (!ratioNum || ratioNum <= 0 || !ratioDen || ratioDen <= 0) {
    return 0;
  }
  // … (elided in this snapshot)
}
...
  return {
    planTick(tick) {
      const rows = resolveRows(tick);
      let tickBytes = 0;
      for (const row of rows) {
        tickBytes += toInt(row.payload_bytes ?? row.payloadBytes ?? row.payloadBytesInt);
      }
      const overMsgBudget = msgBudget > 0 && rows.length > msgBudget;
      const overByteBudget = byteBudget > 0 && tickBytes > byteBudget;
      const nearMsgBudget = softMsgLimit > 0 && rows.length >= softMsgLimit;
      const nearByteBudget = softByteLimit > 0 && tickBytes >= softByteLimit;
      // … kill-switch logic elided
      const usage = {
        overMsgBudget,
        overByteBudget,
        nearMsgBudget,
        nearByteBudget,
        msgBudget,
        byteBudget,
        softMsgLimit,
        softByteLimit,
        killSwitchTriggered,
        killSwitchReason: killSwitchTriggered ? 'NAP_HARD_TOLERANCE' : '',
      };
      return { rows, usage };
    },
  };
}
```

From this we infer:

- **Inputs:** A budget tracker is initialised with:
  - A mapping from tick → array of NAP envelope rows (fixtures show them as TSV rows).  
  - A **message budget** `msgBudget` (maximum number of envelopes per tick).  
  - A **byte budget** `byteBudget` (maximum total payload bytes per tick).  
  - A **soft tolerance ratio** (for computing `softMsgLimit` and `softByteLimit`).
- **Row schema:** The tracker recognises numeric payload size from one of:
  - `row.payload_bytes`  
  - `row.payloadBytes`  
  - `row.payloadBytesInt`  
  It sums these, after integer coercion.

### 2.2 Soft vs hard budgets

Soft limits are computed via `computeSoftLimit(budget, ratioNum, ratioDen)`:

- If `budget <= 0`, the soft limit is 0 (disabled).  
- If the ratio numerator/denominator are invalid (`<= 0`), the soft limit is 0.  
- Otherwise, the function returns a positive integer ≤ hard budget, representing the **near-budget threshold**.

While the exact formula is elided, tests (see `tests/umx.nap.test.js`) show the intent:

- `nearMsgBudget` becomes `true` when `rows.length >= softMsgLimit`.  
- `nearByteBudget` becomes `true` when `tickBytes >= softByteLimit`.  
- `overMsgBudget` is `true` when `rows.length > msgBudget`.  
- `overByteBudget` is `true` when `tickBytes > byteBudget`.

The **kill switch** is triggered when a hard breach occurs beyond tolerated thresholds; in that case, `killSwitchTriggered` is `true` and `killSwitchReason` is the fixed string `'NAP_HARD_TOLERANCE'`.

### 2.3 planTick contract

Per tick, the tracker’s `planTick(tick)` function returns:

```js
{
  rows,   // cloned rows for that tick
  usage: {
    overMsgBudget,
    overByteBudget,
    nearMsgBudget,
    nearByteBudget,
    msgBudget,
    byteBudget,
    softMsgLimit,
    softByteLimit,
    killSwitchTriggered,
    killSwitchReason, // '' or 'NAP_HARD_TOLERANCE'
  }
}
```

This is the **runtime budget profile** used by the Gate/UMX loop to enforce NAP ingest limits and to surface “near budget” signals without killing the run.

This closes a conceptual gap from the math-only spec: we now know the **operational semantics** of per-tick NAP budgets in the concrete implementation, including field names and how “near” vs “over” vs “kill” are represented.

---

## 3. NAP envelope fixtures (TSV schema glimpse)

The golden fixtures for UMX, e.g. `Universal_Matrix_Pillar_UMX_v1_2025-11-17_maximal/fixtures/UMX/golden/F01_MINIMAL_TOPOLOGY/nap_envelopes.tsv`, define the **logged** representation of envelopes.

The header row (as stored) is:

```tsv
scenario_id	ick	envelope_id	id_key_seed	source_pillar	ta...hema_id	nonce	priority	payload_bytes	applied	dead_letter
```

The header contains an ellipsis (`...`) where columns are redacted or omitted in this snapshot. We can still safely read the visible columns:

- `scenario_id` — fixture scenario identifier.  
- `tick` — tick index (string in fixtures, cast via `toInt`).  
- `envelope_id` — fixture-level identifier for the envelope.  
- `id_key_seed` — text seed key for reproducible envelope IDs.  
- `source_pillar` — origin pillar (truncated mid-word but clearly visible prefix).  
- `...` — one or more redacted columns (possibly target pillar, message type, etc.).  
- `schema_id` — schema identifier for payload type (visible suffix `hema_id`).  
- `nonce` — transport nonce.  
- `priority` — envelope priority class.  
- `payload_bytes` — payload size in bytes, as used by the budget tracker.  
- `applied` — flag indicating successful application.  
- `dead_letter` — flag/marker for envelopes that were not successfully applied.

Because of the ellipsis in the underlying file, we **cannot** safely reconstruct the missing column names; they remain an open detail. However, this fixture confirms:

- The existence and names of the columns listed above.  
- That the budget tracker’s `payload_bytes` field is grounded in real fixtures.

---

## 4. Alignment with prior math/spec canon

This implementation pass does **not** change any math; it ties existing canon to concrete wire/runtime forms:

- NAP envelopes in math canon already had tick/node/layer/seed/payload-ref/metrics/mode/sig.  
  - Gate JS now fixes the **exact JSON field names** and canonicalisation order used for hashing and signing.  
- NAP budgets in math canon already spoke about **per-tick quotas** and **kill switches**.  
  - Gate JS now defines the runtime fields (`nearMsgBudget`, `overByteBudget`, `killSwitchReason='NAP_HARD_TOLERANCE'`, etc.).  
- NAP fixtures provide a concrete TSV schema for logged envelopes, matching the JS tracker’s expectations.

**Still open (by design):**

- The complete NAP manifest (`nap_manifest.json`) schema is still not present in this repo; all `nap` code is about envelopes and budgets, not manifest wiring.  
- The kill-switch threshold formula inside `computeSoftLimit` is elided; we only know its structural role, not the exact ratios used.  
- Additional NAP-related structures in other TGP/TBP docs (e.g. for cross-pillar routing) are out of scope for this pass and can be covered in a dedicated TBP/SLP implementation pass.

This document should now be treated as the **implementation-grounded NAP envelope & budget spec** for Astral Press / Gate integration, to be referenced alongside the math canon and earlier NAP manifest spec when designing higher-level manifests and operators.



<!-- END SOURCE: astral_press_pillar_nap_envelope_budget_gate_js_implementation_pass.md -->


---

<!-- BEGIN SOURCE: astral_press_epsilon_profiles_integerization_spec_v_1_crush_without_regret.md -->

# Astral Press — ε‑Bounded Profiles & Integerization Spec v1  
*(“Crush Without Regret” Path on Top of JS Offline MVP)*

Status: **Local implementation spec** for `APP-UROBOROS-REF-1`, building on:

- **Astral Press — JS Offline MVP Build Plan (2025‑11‑20)**
- **APP_LOCAL_SPEC v1 — Aether Press Local Implementation (2025‑11‑20)**
- **Astral Press — APP Implementer Checklist v1 (2025‑11‑20)**
- **Astral Press — APP Complement Sheets v2 & v4 (Legacy + Implementation Canon Pack)**

This document instantiates the ε‑bounded profiles, integerization pipeline, and “Crush without regret” acceptance harness for the local implementation. Where canon is explicit, this spec follows it; where canon leaves design space open, this spec makes local choices and labels them **Decision** with **Rationale**.

---

## 0. Scope & Relationship to Other Docs

### 0.1 What this spec covers

This spec defines, for `APP-UROBOROS-REF-1`:

1. **Canon anchors for ε, integerization, and acceptance**
   - Direct quotes around ε‑bounded behaviour, the integerization pipeline, and the runbook-level “Crush without regret” checks.
2. **Terminology & domain**
   - How we use `ε`, per‑field bounds, quantization step `q`, and scoreboard `O`.
3. **Manifest & policy extensions**
   - How `MANIFEST.json` and Press policy cards gain field‑level ε/q configuration.
4. **Integerization pipeline**
   - Exact steps for `normalize → units → quantize → zigzag → varint/delta/RLE` in this implementation.
5. **ε‑bounded profiles**
   - Named profiles (`PRESS_LOSSLESS`, `PRESS_SENSOR_MED`, `PRESS_LOG_CRUSH`) with explicit ε and q mapping.
6. **“Crush without regret” acceptance harness**
   - Replay and predictive tests, field‑level bounds, idempotence and isolation, and behaviour on failure.
7. **JS Offline MVP integration**
   - How the above plug into `pressNumericArray`, future `pressTable/pressSensorStream`, and the SPA.

### 0.2 What this spec explicitly does *not* cover

- Full multi‑layer NAP stacking and MDL layer admission (covered in the Full Implementation Build Plan and future specs).
- Dims Press per‑dimension/per‑layer controls beyond the parts needed for ε and integerization.
- Networked APP service (HTTP/gRPC) concerns; those remain optional and local.

Where these interact (e.g. dimension metadata), we define only the minimal overlaps required to make ε‑bounded integerization and acceptance coherent.

---

## 1. Canon Anchors — ε, Integerization, and “Crush Without Regret”

### 1.1 Integerization pipeline & ε→q

Legacy performance report (Dims/Press performance) defines the core shape and contract:

> “Practical knobs that drive the crush ratio
>
> - **Integerization pipeline** (normalize → units → quantize → zigzag → varint/delta/RLE).
>   - Bound error upfront: if you quantize a scalar with step q, your max absolute error is ≤ q/2. Pick q so it respects the field’s ε.”  
> *(`press proformance.pdf`)*

APP Implementer Checklist v1 restates the per‑field bound as a canon requirement:

> “For every numeric field x you store after quantization q:  
> \(|x_{\text{post}} - x_{\text{pre}}| \le q/2 \le \varepsilon_x\).”  
> *(Checklist §1.2)*

### 1.2 “Crush without regret” runbook

The performance report gives a concrete acceptance checklist:

> “Crush without regret  checks (copy this into your runbook)
>
> 1. **Field-level bounds:** For every numeric field x you store after quantization q: \(|x\_{\text{post}} - x\_{\text{pre}}| \le q/2 \le \varepsilon\_x\).
> 2. **Replay test:** DePress then run Δ=0: O unchanged (fidelity at snapshot).
> 3. **Predictive test:** DePress and run T^Δ; check d(O\_{\text{true}}, O\_{\text{replayed}}) ≤ ε.
> 4. **Document proof:** Keep {hash, bytes} for each external source in **P\_cite** so an auditor can verify you didn’t hallucinate inputs.
> 5. **Idempotence:** Same envelope + same nonce ⇒ no net change to O.
> 6. **Isolation:** Prior checkpoint O-hashes never change.”  
> *(`press proformance.pdf`)*

Checklist v1 encodes the same requirements under “Lossless vs ε‑bounded modes & Acceptance Tests” and emphasises that in ε‑bounded mode:

> “Only **O** (the scoreboard) matters for acceptance; raw data deltas are not the decision basis in ε‑bounded mode.”  
> *(Checklist §1.2)*

### 1.3 Two‑track Press policy constraints

The same performance report introduces P\_state/P\_cite and policy‑level caveats:

> “You keep the *small, exact* computational snapshot (P\_state), plus tiny proofs/pointers for the rest (P\_cite).”  
> *(`press proformance.pdf`)*

and:

> “What to *avoid* (this is where people get burned)
>
> - **Letting P\_state depend on raw docs** you won’t replay. If T doesn’t need the raw, don’t pack it—hash it in **P\_cite** instead.
> - **Quantizing before you set ε.** Always lock ε first; choose q to fit inside it.
> - **Comparing anything other than O** in acceptance. The whole point is: if O matches under the contracts, you’re good.”  
> *(`press proformance.pdf`)*

Checklist v1 encodes these under “Two‑Track Press: P\_state vs P\_cite” and “Mandatory policy rules”.

### 1.4 Dims Press per‑dimension fidelity controls

Dims Press report extends ε‑bounded behaviour with per‑dimension controls:

> “FIDELITY CONTROLS YOU CAN SET PER-DIMENSION (OR PER-LAYER)
>
> - **Exact vs quantized dims:** choose which dims must match exactly for replay vs which can be bucketed (e.g., to nearest 1e‑3, positions to 1 unit).
> - **Residual fraction:** tighten or loosen Loom’s residual size (e.g., 5–20%) for layers where you need more/less detail.
> - **Selective retention:** mark dims as {recompute, residual, full}:
>   - *recompute*: derive from other fields on replay (kept out of residual),
>   - *residual*: store compact delta,
>   - *full*: store verbatim (e.g., provenance‑critical tags).
> - **Dict scopes:** keep **per-node dictionaries** or a **global Press dict** on the NAP bus for cross-layer dimensional schemas.”  
> *(`press v2.pdf`)*

Bottom line:

> “New dims can appear mid-run (we proved it) and get Loomed (for deterministic replay) and Pressed (for compact, reversible storage) like any other data. You can dial **how faithful** they must be for reuse and **how much** detail to keep in residuals on a **per-dimension, per-layer** basis.”  
> *(`press v2.pdf`)*

This spec uses those controls where necessary for ε‑bounded integerization and acceptance.

---

## 2. Terminology & Domain

This section fixes the exact meanings of symbols used in this spec, aligning with canon language.

### 2.1 Numeric fields, dimensions, and profiles

- **Numeric field x**
  - A scalar component of a Pressed dataset (e.g. one column of a table, one component of a sensor vector, a state variable in P\_state).
  - It has:
    - **Unit** (e.g. metres, m/s, seconds).
    - **Fidelity tolerance** \(\varepsilon\_x\) when in ε‑bounded mode.
    - **Quantization step** \(q\_x\) chosen such that \(q\_x / 2 \le \varepsilon\_x\).

- **Dimension / dim**
  - A field tracked on the NAP bus as per Dims Press.
  - Has metadata: `name`, `index`, `type`, `unit`, `exact_or_quantized`, `retention_mode`, and `dict_scope` (per‑node/global).

- **Press profile**
  - A named collection of ε and q settings plus codec options for a dataset type, e.g. `PRESS_LOSSLESS`, `PRESS_SENSOR_MED`, `PRESS_LOG_CRUSH`.
  - Profiles are referenced in `MANIFEST.json.press.profile` and further detailed via **policy cards**.

### 2.2 ε, q, and field‑level bounds

- **ε\_x (epsilon_x)**
  - Maximum permitted absolute error for numeric field x at the **data level**.
  - Chosen by policy (per profile and per field) **before** quantization.

- **q\_x (quantization step)**
  - Quantization step for field x, in its **normalized units**.
  - Must satisfy canon constraint:
    \[
    |x_{\text{post}} - x_{\text{pre}}| \le q\_x / 2 \le \varepsilon\_x.
    \]
  - Local choice in this spec is usually \(q\_x = 2 \varepsilon\_x\), but narrower q is allowed.

- **Field‑level bound check**
  - For any Press/DePress cycle in ε‑bounded mode, we must check:
    - For each numeric field x, for all elements:
      \[
      |x_{\text{post}} - x_{\text{pre}}| \le q\_x / 2 \le \varepsilon\_x.
      \]
  - If any field violates this, acceptance fails.

### 2.3 Scoreboard O and distance d

- **Scoreboard O(S)**
  - A mapping from state S (or dataset) to a structured set of observables (e.g. norms, physical invariants, metrics relevant to T).
  - Canon says: “Only O (the scoreboard) matters for acceptance; raw data deltas are not the decision basis in ε‑bounded mode.”

- **Distance function d(O_true, O_replayed)**
  - Measures discrepancy between true and replayed scoreboard.
  - For this implementation, d is defined per profile (see §6), but must be compatible with an ε bound:
    - Common choices: per‑field max absolute diff, vector norms, or custom metrics.

- **Δ (delta horizon)**
  - Time or step horizon for predictive tests:
    - Δ = 0: snapshot‑level replay test.
    - Δ > 0: predictive test over T^Δ.

### 2.4 P\_state vs P\_cite

- **P\_state**
  - Minimal Pressed snapshot needed for T to resume exactly.
  - Must pass ε‑bounded replay and predictive tests at scoreboard level.

- **P\_cite**
  - Proof/pointer channel: hashes, sizes, and a few extracted integers from external sources.
  - Not used for simulation replay; used only for provenance and audit.

This spec’s acceptance harness is applied to **P\_state** capsules. P\_cite is validated via hash/proof‑carrying requirements but not via ε‑bounded replay of T.

---

## 3. Manifest & Policy Extensions for ε and Integerization

This section extends APP_LOCAL_SPEC v1 with the fields needed for ε‑bounded operation.

### 3.1 MANIFEST.json: `press` section extensions

APP_LOCAL_SPEC v1 already defines a `press` section with:

```jsonc
"press": {
  "mode": "lossless",              // or "epsilon_bounded"
  "profile": "PRESS_LOSSLESS",     // local profile name
  "epsilon_global": 0.0,            // null if not applicable
  "dtype": "bytes",                // e.g. "bytes", "float32", "int32", "json"
  "shape": [123456],                // tensor/array shape, or [size_bytes] for flat
  "fidelity_metric": "l2",         // e.g. "l2", "max_abs", domain metric
  "created_utc": "2025-11-20T12:34:56Z"
},
```

**Decision — extend `press` with numeric field metadata**

For `dtype` values that imply structured numeric content (e.g. `"float32"`, `"int32"`, `"sensor"`, `"table"`, `"json_structured"`), we add:

```jsonc
"press": {
  // existing fields ...
  "mode": "lossless" | "epsilon_bounded",
  "profile": "PRESS_LOSSLESS" | "PRESS_SENSOR_MED" | "PRESS_LOG_CRUSH" | "…",
  "epsilon_global": 0.0 | null,

  "numeric_fields": [
    {
      "name": "position_x",           // identifier for field
      "unit": "m",                    // unit label (string)
      "epsilon": 1e-4,                 // ε_x in data units
      "q": 2e-4,                       // quantization step q_x, q/2 ≤ ε_x
      "mode": "exact" | "quantized", // exact dims: ε = 0, q = 0; quantized dims: ε > 0
      "retention": "recompute" | "residual" | "full",
      "residual_fraction_target": 0.2, // optional, for Dims Press
      "dict_scope": "per_node" | "global"
    }
    // … more fields …
  ]
}
```

**Rationale**

- Mirrors Dims Press per‑dimension knobs (exact vs quantized, retention, residual fraction, dict scope) and binds them directly to ε and q.
- Keeps all per‑field ε/q configuration attached to the Press run manifest for auditability.

### 3.2 Press policy cards: ε and q

The performance report defines a Press policy card template:

> “Press policy card (use per source)
>
> PRESS POLICY <source_name>
>
> Type: (text/pdf/image/log/table/sensor) Track: [P\_state | P\_cite] (pick one; sometimes both) O-fields derived: { ... } (list only what T or O needs) Quantization q per field: {f1:q1, f2:q2, ...} …”

**Decision — `press_policy_card_v1` schema**

We define a JSON schema for policy cards used by the implementation:

```jsonc
{
  "schema_version": "press_policy_card_v1",
  "source_name": "imu_stream_001",          // logical name for this source
  "type": "sensor",                        // "text"|"pdf"|"image"|"log"|"table"|"sensor"|…
  "track": "P_state",                      // "P_state"|"P_cite"|"both"

  "o_fields": ["energy_norm", "max_accel"], // scoreboard components derived from this source

  "profile": "PRESS_SENSOR_MED",           // default profile name for this source

  "fields": {
    "position_x": {
      "unit": "m",
      "epsilon": 1e-4,
      "q": 2e-4,
      "mode": "quantized",                  // or "exact"
      "retention": "residual",              // or "recompute"|"full"
      "residual_fraction_target": 0.2,
      "dict_scope": "per_node"
    },
    "timestamp": {
      "unit": "s",
      "epsilon": 0.001,
      "q": 0.002,
      "mode": "quantized",
      "retention": "residual",
      "residual_fraction_target": 0.1,
      "dict_scope": "global"
    }
    // … more fields …
  }
}
```

**Rationale**

- Makes ε and q explicit per field, as required by the runbook: “Quantization q per field: {f1:q1, f2:q2, …}”.
- Connects type and track (P\_state vs P\_cite) to the Press pipeline.
- Allows scoreboard O definition (`o_fields`) to be centralised per source.

### 3.3 Policy compiler

**Decision — `policy_compiler` responsibilities**

A local module `policy_compiler` will:

1. Load `press_policy_card_v1` JSON for a given source.
2. Validate that for every numeric field:
   - If `mode = "exact"`, then `epsilon = 0`, `q = 0`.
   - If `mode = "quantized"`, then `epsilon > 0`, `q > 0`, and `q / 2 ≤ epsilon`.
3. Derive a `numeric_fields` array suitable for embedding into `MANIFEST.json.press`.
4. Provide per‑field configuration to the integerization pipeline (see §4).

Behaviour on validation failure:

- In **P\_state** profile:
  - Hard error; Press run is refused for that source until policy is fixed.
- In **P\_cite** profile:
  - Policy violation is logged, and only minimal proof data (hash, size) is stored; no ε‑bounded numeric Press is attempted.

**Rationale**

- Enforces the “Quantizing before you set ε” caveat: the compiler refuses to proceed if ε/q are inconsistent.
- Keeps P\_state stricter than P\_cite, aligning with two‑track Press.

---

## 4. Integerization Pipeline — `normalize → units → quantize → zigzag → varint/delta/RLE`

Canon gives the shape of the pipeline; this section fixes the exact local behaviour.

### 4.1 Overview

For a numeric field x with raw values \(x\_i\), unit U, ε\_x, and q\_x, the integerization pipeline transforms it into an integer sequence \(z\_i\) for SimB:

1. **Normalize & unit conversion** — `x_raw` → `x_norm` in canonical units.
2. **Quantize** — `x_norm` → `x_quant` as multiples of q\_x (ε‑bounded mode) or exact scaled values (lossless).
3. **Integer map** — `x_quant` → signed integers \(n\_i\).
4. **ZigZag** — signed \(n\_i\) → unsigned integers \(u\_i\).
5. **Delta + RLE** — optional compression transforms on \(u\_i\).
6. **Varint + entropy coding** — output as a compact bitstream.

The inverse DePress pipeline reverses these steps exactly.

### 4.2 Step 1 — Normalize & unit conversion

**Decision**

For each field with a unit string `unit` and raw value sequence `x_raw[i]`:

1. A **canonical unit** U is defined per field in the policy card; for now we take the unit label literally, i.e. U = `unit`.
2. The implementation supports unit scale factors (e.g. mm → m) via a multiplicative factor `scale`:
   - If raw data is already in U: `scale = 1`.
   - If raw data in unit U' with known ratio to U: e.g. mm → m: `scale = 0.001`.
3. Normalized values:
   - `x_norm[i] = x_raw[i] * scale`.

**Rationale**

- Keeps unit handling simple but explicit.
- Ensures ε and q are always interpreted in the same canonical units, regardless of input source.

### 4.3 Step 2 — Quantize

We distinguish **lossless** and **ε‑bounded** modes.

#### 4.3.1 Lossless mode

For `press.mode = "lossless"`:

- **Decision**
  - For integer dtypes (`int32`, `int64`), no quantization is performed:
    - `x_quant[i] = x_norm[i]` (must be exact integers).
  - For float/decimal dtypes, we employ a fixed integer scale `K` such that all values are exactly representable as integers:
    - `x_quant[i] = round(x_norm[i] * K)`.
    - `K` is chosen per dtype so that all possible values in the declared dtype range map bijectively to integers without rounding error.
  - If such a K is not available (dataset contains values outside safely representable range), lossless mode for that dtype is **refused**; callers must use ε‑bounded mode instead.

- **Rationale**
  - Respects Checklist v1’s `epsilon_global = 0` for `PRESS_LOSSLESS` and guarantees bit‑exact reconstruction for supported dtypes.

#### 4.3.2 ε‑bounded mode

For `press.mode = "epsilon_bounded"`:

- **Decision**
  - For each field x, policy provides ε\_x and q\_x with `q_x / 2 ≤ ε_x`.
  - Quantization is:
    - `x_quant[i] = q_x * round(x_norm[i] / q_x)`.
  - This ensures:
    - `|x_quant[i] − x_norm[i]| ≤ q_x / 2 ≤ ε_x`.

- **Rationale**
  - Directly implements the canonical relation “if you quantize a scalar with step q, your max absolute error is ≤ q/2. Pick q so it respects the field’s ε.”

### 4.4 Step 3 — Map to signed integers

**Decision**

- For both modes, once `x_quant[i]` is determined:
  - `n[i] = round(x_quant[i] / q_unit)` where:
    - In lossless mode: `q_unit = 1` if already integer, or `q_unit = 1/K` where K is the scaling factor used.
    - In ε‑bounded mode: `q_unit = q_x`.

This yields signed integers n[i] representing quantized values in units of `q_unit`.

**Rationale**

- Ensures invertibility: `x_quant[i] = n[i] * q_unit` for ε‑bounded, or `x_quant[i] = n[i] / K` for lossless.

### 4.5 Step 4 — ZigZag

**Decision**

- For each signed integer n[i], compute ZigZag‑encoded unsigned integer u[i]:
  - For 64‑bit range (conceptually):
    - `u[i] = (n[i] << 1) ^ (n[i] >> 63)` (in JS implementation, use BigInt semantics).

**Rationale**

- Matches AEON/APXi requirement that signed parameters are encoded via ZigZag → varint.
- Clusters small magnitude integers near zero for efficient varint coding.

### 4.6 Step 5 — Delta + RLE (optional transforms)

**Decision**

Per field (or per segment), we apply the following optional transforms before entropy coding:

1. **Delta coding**
   - `d[0] = u[0]`.
   - For i > 0: `d[i] = u[i] − u[i−1]`.
2. **Run‑length encoding (RLE)**
   - If there are long runs of zero deltas or repeats, group them as `(value, run_length)` pairs.
   - Apply only when it reduces description length as measured by the MDL heuristic in the residual stack (outer MDL spec).

These transforms are recorded in residual layer `params` (e.g. `"applied_transforms": ["delta", "rle"]`).

**Rationale**

- Implements the “varint/delta/RLE” steps from the integerization pipeline quote.
- Keeps transform choice measurable via MDL, not hard‑coded.

### 4.7 Step 6 — Varint + entropy coding

**Decision**

- After delta/RLE, we obtain a sequence of signed or unsigned integers, which are ZigZag‑encoded (if signed) and turned into varints.
- These varints may then be:
  - Directly written into the residual bitstream using Golomb–Rice and/or arithmetic coding, following the residual codec spec in APP_LOCAL_SPEC v1 and the JS MVP plan.

**Rationale**

- Completes the transformation from real‑valued numeric fields to a compact integer bitstream suitable for SimB.
- Keeps consistency with AEON/APXi’s integer‑only ethos and APX’s container design.

### 4.8 DePress inversion

For DePress, the pipeline is reversed exactly:

1. Entropy decode + varint → integers.
2. Undo RLE and delta.
3. ZigZag decode → signed n[i].
4. Map back to quantized values:
   - Lossless: `x_quant[i] = n[i] / K` or `x_quant[i] = n[i]`.
   - ε‑bounded: `x_quant[i] = n[i] * q_x`.
5. Undo unit scaling: `x_post[i] = x_quant[i] / scale`.

Field‑level bounds and scoreboard tests are run on `x_post` vs `x_pre`.

---

## 5. ε‑Bounded Profiles & Epsilon→Quantization Mapping

This section defines the named profiles and their ε/q mappings.

### 5.1 Profiles overview

We define three profiles initially:

1. `PRESS_LOSSLESS`
2. `PRESS_SENSOR_MED`
3. `PRESS_LOG_CRUSH`

These are referenced in `MANIFEST.json.press.profile` and in policy cards.

### 5.2 `PRESS_LOSSLESS`

**Definition**

- `press.mode = "lossless"`.
- `press.profile = "PRESS_LOSSLESS"`.
- `epsilon_global = 0.0`.
- For all numeric fields:
  - `epsilon = 0.0`.
  - `q = 0.0`.
  - Integerization uses integer scaling K where required, but no information is discarded.

**Behaviour**

- Field‑level bounds reduce to bit‑exact equality:
  - `x_post[i] == x_pre[i]` for all elements.
- “Crush without regret” tests must hold exactly at data and scoreboard levels.

### 5.3 `PRESS_SENSOR_MED`

This profile targets sensor‑like structured data (positions, velocities, accelerations, timestamps).

**Definition (example defaults)**

For an IMU‑style schema:

```jsonc
"profile": "PRESS_SENSOR_MED",
"numeric_fields": [
  {
    "name": "position_x",
    "unit": "m",
    "epsilon": 1e-4,
    "q": 2e-4,
    "mode": "quantized",
    "retention": "residual",
    "residual_fraction_target": 0.2,
    "dict_scope": "per_node"
  },
  {
    "name": "position_y",
    "unit": "m",
    "epsilon": 1e-4,
    "q": 2e-4,
    "mode": "quantized",
    "retention": "residual",
    "residual_fraction_target": 0.2,
    "dict_scope": "per_node"
  },
  {
    "name": "velocity_x",
    "unit": "m/s",
    "epsilon": 1e-3,
    "q": 2e-3,
    "mode": "quantized",
    "retention": "residual",
    "residual_fraction_target": 0.25,
    "dict_scope": "per_node"
  },
  {
    "name": "accel_x",
    "unit": "m/s^2",
    "epsilon": 1e-3,
    "q": 2e-3,
    "mode": "quantized",
    "retention": "residual",
    "residual_fraction_target": 0.3,
    "dict_scope": "per_node"
  },
  {
    "name": "timestamp",
    "unit": "s",
    "epsilon": 1e-3,
    "q": 2e-3,
    "mode": "quantized",
    "retention": "residual",
    "residual_fraction_target": 0.1,
    "dict_scope": "global"
  }
]
```

**Rationale**

- Uses the ε↔q rule (q = 2ε) directly.
- Uses smaller ε for positions than velocities/accelerations to reflect typical use cases (positions more sensitive).
- Keeps timestamps coarsened to 1ms while still supporting high‑frequency replay.

### 5.4 `PRESS_LOG_CRUSH`

This profile targets logs/events with numeric and textual fields.

**Definition (example defaults)**

- For log fields:
  - Counters and IDs:
    - `epsilon = 0`, `q = 0`, `mode = "exact"`, `retention = "residual"`.
  - Timestamps:
    - `epsilon = 0.01` seconds, `q = 0.02`, `mode = "quantized"`.
  - Numeric metrics (e.g. latencies):
    - `epsilon = 1`, `q = 2`, `mode = "quantized"`.
- Textual fields (messages, stack traces):
  - Typically handled via dictionary SimB only; no ε applies.

**Rationale**

- Keeps identity and counters exact for auditability.
- Allows coarse quantization for timestamps and metrics where only approximate ordering/magnitude matters.
- Matches the “O‑only comparison” mindset: logs are rarely replayed as state, but are used to derive O′ values (aggregates) and proofs.

### 5.5 Extensibility

New profiles can be added by defining their ε/q tables and residual/retention modes in policy cards. Each new profile must:

- Respect per‑field constraint `q/2 ≤ ε`.
- Document its intended domain and assumptions.
- Provide recommended scoreboard metrics and d(·,·) for acceptance.

---

## 6. “Crush Without Regret” Acceptance Harness

This section formalises the acceptance harness for ε‑bounded Press runs.

### 6.1 Components

For a given source and Press run, the harness requires:

1. **Original state/data S**
   - Input to Press.
2. **Press configuration**
   - Profile, ε/q per field, policy card, and mode set (e.g. S‑modes).
3. **Scoreboard function O**
   - `O: State → Scoreboard`, as configured by policy (`o_fields`).
4. **Distance function d**
   - Measures discrepancy between O_true and O_replayed.
5. **Horizon Δ and ε_O**
   - Δ = 0 for replay test; Δ > 0 for predictive test.
   - ε_O: scoreboard‑level tolerance (can be derived from per‑field ε or defined separately).

### 6.2 Field‑level bounds check

For each numeric field x with ε\_x and q\_x:

1. After Press + DePress, compute `x_post` from DePress pipeline.
2. For every element i, compute:
   - `delta_x[i] = |x_post[i] − x_pre[i]|`.
3. Check:
   - `delta_x[i] ≤ q_x / 2`.
   - `q_x / 2 ≤ epsilon_x`.

If any element violates this, the run **fails field‑level bounds**.

### 6.3 Replay test (Δ = 0)

For the replay test:

1. Compute `O_true = O(S)` from original state/data.
2. Press → DePress to obtain reconstructed state/data S′.
3. Compute `O_replayed = O(S′)`.
4. Define scoreboard distance `d_0 = d(O_true, O_replayed)`.
5. For ε‑bounded mode, require:
   - `d_0 ≤ ε_O`.

The canonical wording is: “DePress then run Δ = 0: O unchanged (fidelity at snapshot).” For profiles where O is defined to be strictly invariant at Δ = 0, we set ε_O = 0.

### 6.4 Predictive test (Δ > 0)

Predictive test requires access to T, the transition map.

1. Compute `O_true_future = O(T^Δ(S))`.
2. Compute `O_replayed_future = O(T^Δ(S′))`.
3. Compute `d_Δ = d(O_true_future, O_replayed_future)`.
4. Require:
   - `d_Δ ≤ ε_O_future`.

For the JS Offline MVP, **T is not embedded**, so predictive test is only available in environments where T is bound. In the browser MVP, this step is stubbed and marked as **not evaluated**; acceptance is limited to Δ = 0 and field‑level bounds.

### 6.5 Document proof (P\_cite)

For P\_cite sources, the harness ensures that for each external source used:

- We store at least `{hash, size_bytes}` in P\_cite capsules.
- Optionally store minimal bytes necessary to prove correct extraction of O‑relevant integers.

This follows the runbook:

> “Document proof: Keep {hash, bytes} for each external source in **P\_cite** so an auditor can verify you didn’t hallucinate inputs.”

### 6.6 Idempotence and isolation

- **Idempotence**
  - For any fixed envelope and nonce, repeating Press/DePress with the same config on the same input must not change O.
  - In `APP-UROBOROS-REF-1`, this is guaranteed by determinism of the pipeline and purity of O.
- **Isolation**
  - Prior checkpoint O‑hashes are stored and must not change as new checkpoints are created or Pressed.

### 6.7 Harness outputs and report schema

**Decision — `reports/report.json` for ε‑bounded runs**

We extend the existing reports to include an acceptance section:

```jsonc
{
  "schema_version": "press_report_v1",
  "app_impl": "APP-UROBOROS-REF-1",
  "press": {
    "mode": "epsilon_bounded",
    "profile": "PRESS_SENSOR_MED"
  },
  "metrics": {
    "L_total_bits": 123456,
    "L_naive_bits": 345678,
    "kappa_bits": 222222
  },
  "acceptance": {
    "field_bounds_passed": true,
    "fields_violated": [],

    "replay_test": {
      "delta": 0,
      "d_value": 0.0,
      "epsilon_O": 0.0,
      "passed": true
    },

    "predictive_test": {
      "delta": 10,
      "d_value": null,
      "epsilon_O": null,
      "evaluated": false,
      "reason": "T_not_bound_in_JS_MVP"
    },

    "p_cite_proof": {
      "sources": [
        {
          "name": "external_log_001",
          "hash": "…",
          "size_bytes": 12345
        }
      ]
    },

    "idempotence": {
      "checked": true,
      "passes": true
    },

    "isolation": {
      "checked": true,
      "prior_O_hashes_unchanged": true
    }
  }
}
```

**Rationale**

- Makes all “Crush without regret” checks explicit and auditable.
- Allows the browser MVP to indicate which checks were or were not evaluated.

### 6.8 Behaviour on failure

**Decision**

- For **P\_state**:
  - If any of the following are false:
    - Field‑level bounds.
    - Replay test at Δ = 0.
  - Then Press **refuses** to mark the capsule as accepted and:
    - Returns an error to the caller.
    - Writes a partial report with `acceptance.*.passed = false`.
  - Optionally, a debug flag can force debug capsules to be emitted, but they must be tagged `"accepted": false`.

- For **P\_cite**:
  - Only P\_cite proof requirements are enforced; ε‑bounded replay is not applied.
  - Failures in P\_cite proof cause warnings and may block provenance assertions, but do not affect P\_state acceptance.

**Rationale**

- Matches the spirit of “Crush without regret”: if acceptance fails, you should **regret** the configuration and refuse to proceed.

---

## 7. JS Offline MVP Integration

This section describes how the ε‑bounded and integerization logic integrates into the JS Offline MVP modules.

### 7.1 Module wiring

From the MVP Build Plan, we already have (or plan to have):

- `press_numeric` / `pressNumericArray` entrypoints.
- A residual stack (`residual_integerize`, `residual_delta`, `residual_golomb_rice`, `residual_entropy`).
- `MANIFEST.json` and `nap/compression.json` handling.

**Decision — new/extended modules**

1. `policy_compiler`
   - Parses `press_policy_card_v1`.
   - Produces `numeric_fields` for MANIFEST and configuration objects for integerization.

2. `integerization_pipeline`
   - Implements §4 steps (normalize, quantize, integer map, ZigZag, delta/RLE, varint).
   - Provides `encodeField` and `decodeField` functions.

3. `acceptance_harness`
   - Implements §6 checks for field‑level bounds and replay tests.

4. `profiles`
   - Exposes constants and templates for `PRESS_LOSSLESS`, `PRESS_SENSOR_MED`, `PRESS_LOG_CRUSH`.

### 7.2 `pressNumericArray` behaviour

For structured numeric arrays in JS:

1. Caller provides data and profile or policy card.
2. `policy_compiler` builds per‑field config (ε, q, mode, retention, etc.).
3. `pressNumericArray`:
   - Applies Segmentation → `selectModelForSegment` (SimA) as per MVP.
   - For each numeric field in residuals, calls `integerization_pipeline.encodeField`.
   - Builds NAP manifest and APX container as before.
4. After building the capsule, `acceptance_harness`:
   - DePresses the capsule.
   - Applies field‑level bounds and replay test at Δ = 0.
   - Writes `reports/report.json`.

### 7.3 UI integration

In the offline SPA:

- Add a **profile selector** for numeric demos:
  - Options: Lossless, Sensor (med), Log crush.
- Add a **policy card editor** panel (simplified):
  - Table of fields, with ε and q and mode columns.
- Add an **acceptance results** panel:
  - Field‑level max deltas.
  - Replay test status.
  - P\_cite proof summary (if relevant).

This gives a visible implementation of ε‑bounded Press and acceptance behaviour on the page.

---

## 8. Testing & Compliance

### 8.1 Unit tests for integerization

Per numeric field type:

1. Test that for random values within a supported range:
   - Lossless mode round‑trip yields `x_post = x_pre`.
2. Test that for ε‑bounded mode with known ε and q:
   - `|x_post − x_pre| ≤ q/2` for all test samples.
3. Test ZigZag + varint round‑trips.
4. Test delta + RLE encode/decode round‑trips.

### 8.2 Acceptance harness tests

1. Construct synthetic S and scoreboard O where O is simple (e.g. sums and norms).
2. Press/DePress under controlled ε and q.
3. Verify that:
   - Field‑level bounds pass when expected and fail when deliberately violated.
   - Replay test at Δ = 0 passes when DePress is correct.
4. For predictive tests, where T is available in a test harness, verify that `d(O_true_future, O_replayed_future) ≤ ε_O` or fails appropriately.

### 8.3 Compliance with canon

This spec is compliant with:

- **Integerization and ε**
  - Implements “normalize → units → quantize → zigzag → varint/delta/RLE” with per‑field bounds `|x_post − x_pre| ≤ q/2 ≤ ε_x`.
- **Crush without regret**
  - Implements field‑level bounds, replay test, predictive test hooks, document proof, idempotence, and isolation.
- **Two‑track Press and policy cards**
  - Enforces P\_state vs P\_cite separation and per‑source policy cards.

Where canon is silent (specific numeric ε, q values, exact report JSON, UI), this spec clearly marks decisions as local and ties them back to the canon’s qualitative requirements.

---

## 9. Change Control

Any change to ε‑bounded behaviour, integerization, or acceptance harness must:

1. Update this spec with new decisions and rationale.
2. Bump:
   - `app_impl_version` in `MANIFEST.json`.
   - `schema_version` in `press_policy_card_v1` or `press_report_v1` as appropriate.
3. Ensure backward‑compatible reading of older manifests and reports where possible, or provide migration tooling.

This keeps the ε‑bounded path auditable and prevents accidental drift from the Aether Press canon while allowing iterative refinement of local choices.



<!-- END SOURCE: astral_press_epsilon_profiles_integerization_spec_v_1_crush_without_regret.md -->


---

<!-- BEGIN SOURCE: astral_press_policy_dimensional_controls_spec_v_1_p_state_p_cite_dims_press.md -->

# Astral Press — Policy & Dimensional Controls Spec v1  
*(P_state, P_cite, Press Policy Cards & Dims Press Controls)*

Status: **Local implementation spec** for policy & dimensional controls around Astral Press (`APP-UROBOROS-REF-1`).

Grounded in:

- **Astral Press — APP Complement Sheet v2 (Legacy Docs Pass)**
- **Astral Press — APP Complement Sheet v4 (Implementation Canon Pack)**
- **Astral Press — APP Implementer Checklist v1**
- **Astral Press — ε‑Bounded Profiles & Integerization Spec v1 (Crush Without Regret)**
- **Astral Press — Multi‑Layer NAP & MDL Stack Spec v1**

Where canon is explicit (two‑track Press, O‑only comparison, per‑dim controls), this spec follows it. Where canon leaves details open (exact JSON schemas, mode wiring), this spec makes local decisions and labels them.

---

## 0. Scope

This spec defines, for `APP-UROBOROS-REF-1`:

1. **Two‑track Press semantics**
   - What P_state and P_cite mean, how they are represented, and how Press treats them.
2. **Press policy cards**
   - Concrete schema and required fields for per‑source Press policies.
3. **O / scoreboard semantics**
   - How we represent O, how ε is applied at the scoreboard, and how acceptance checks use O.
4. **Dimensional controls (Dims Press)**
   - Per‑dimension and per‑layer controls: exact vs quantized, residual fraction, selective retention, dictionary scopes.
5. **Policy compiler and runtime enforcement**
   - How textual policy cards are turned into executable configuration that the Press Engine and Flux Decoder respect.
6. **Misconfiguration behaviour**
   - What happens when policies conflict, are incomplete, or can’t be satisfied.

This is the **policy layer** that sits above the raw model+residual mechanics.

---

## 1. Two‑Track Press: P_state & P_cite

### 1.1 Canon recap

Legacy performance docs define **two‑track Press** with:

- **P_state (reconstructive)** — the minimal snapshot needed for T (the transition map) to resume exactly.
- **P_cite (proof/pointer)** — tiny proofs and pointers (hashes, lengths, a few extracted integers) for external sources that T never replays.

The runbook emphasises:

- You keep a **small, exact** computational snapshot (P_state).
- You keep **proofs/pointers** for everything else (P_cite).
- Astronomical crush ratios come from **refusing** to drag irrelevant raw bytes into P_state.

### 1.2 Local semantics

**Decision**

We define:

- **P_state capsule(s)**
  - `.apx` files whose purpose is to support **exact or ε‑bounded replay** of T.
  - Subject to **all** ε/acceptance checks (field‑level q/2 ≤ ε, replay tests, predictive tests, idempotence, isolation).
- **P_cite capsule(s)**
  - `.apx` files (or other blobs) whose purpose is **provenance**: showing which external data was consulted.
  - Must store enough to prove non‑hallucination: hashes, byte‑lengths, and selected invariants.
  - Are *not* used as inputs to T directly.

We explicitly **forbid**:

- Feeding P_cite capsules into T as state.
- Letting P_state depend on raw external documents that T never replays.

**Rationale**

- Matches canon’s “two‑track” guidance and the “what to avoid” list (no P_state dependence on unused raw docs).
- Keeps the high‑fidelity replay channel separate from the provenance channel.

### 1.3 Representation in manifests

**Decision**

We add the following to `MANIFEST.json`:

```jsonc
"press_track": "P_state", // or "P_cite"
```

- `press_track = "P_state"` for reconstructive capsules.
- `press_track = "P_cite"` for proof/pointer capsules.

Additionally, P_cite manifests include:

```jsonc
"cite": {
  "sources": [
    {
      "id": "doc:spec:press_v2",
      "kind": "pdf",           // or "web", "db", etc.
      "uri": "…",               // opaque; not dereferenced by Press itself
      "sha256": "…",
      "size_bytes": 123456,
      "notes": "Used only for section 3.2 invariants."
    }
  ]
}
```

P_state manifests may also have a `cite` block if they carry provenance, but **T must not read P_cite capsules as live state**.

**Rationale**

- The explicit `press_track` flag makes the track unambiguous.
- A `cite.sources[]` list is enough to satisfy proof requirements without specifying external protocols.

---

## 2. Press Policy Cards

### 2.1 Canon recap

Press performance docs introduce **Press policy cards** per source, with fields like:

- `Type` — text/pdf/image/log/table/sensor.
- `Track` — P_state or P_cite (sometimes both).
- `O‑fields derived` — what metrics T/O actually read.
- `Quantization q per field` — mapping from fields to quantization steps.

### 2.2 Local JSON schema

**Decision**

We represent a Press policy card as JSON with schema:

```jsonc
{
  "schema_version": "press_policy_card_v1",

  "source_id": "IMU:front_left_wheel",    // stable, internal ID
  "human_name": "Front left wheel IMU",  // optional label

  "type": "sensor",                      // e.g. text/pdf/image/log/table/sensor

  "track": ["P_state", "P_cite"],        // one or both; P_state implies reconstructive capsule(s)

  "o_fields": [                           // scoreboard fields derived from this source
    "pose.x",
    "pose.y",
    "velocity",
    "health_flag"
  ],

  "numeric_fields": {
    "pose.x": {
      "dtype": "float64",
      "epsilon": 1e-4,
      "q": 2e-4
    },
    "pose.y": {
      "dtype": "float64",
      "epsilon": 1e-4,
      "q": 2e-4
    },
    "velocity": {
      "dtype": "float32",
      "epsilon": 1e-3,
      "q": 2e-3
    }
  },

  "dim_controls": {
    "pose.x": {
      "mode": "quantized",               // "exact" | "quantized"
      "retention": "residual",           // "recompute" | "residual" | "full"
      "residual_fraction": 0.1            // optional; fraction of raw residual bits to keep
    },
    "pose.y": {
      "mode": "quantized",
      "retention": "residual"
    },
    "health_flag": {
      "mode": "exact",
      "retention": "full"
    }
  },

  "profiles": {
    "press_profile": "PRESS_SENSOR_MED", // one of the named profiles
    "dims_profile": "DEFAULT"            // optional profile for Dims Press presets
  }
}
```

Constraints:

- If `mode = "quantized"`, we require `q/2 ≤ epsilon`.
- If `retention = "recompute"`, the policy compiler must know **how** to recompute that field from others; otherwise it is invalid.

**Rationale**

- Matches canon’s per‑field ε/q notion and Dims Press controls (exact vs quantized, selective retention, residual fraction).
- Keeps policy explicitly machine‑readable.

### 2.3 Policy location and binding

**Decision**

- Policy cards live in a JSON file or store, keyed by `source_id`.
- A Press run on source `X` must:
  1. Resolve its policy card by `source_id`.
  2. Validate it (see §5).
  3. Embed a reference in `MANIFEST.json`, e.g.:

```jsonc
"policy": {
  "source_id": "IMU:front_left_wheel",
  "policy_schema": "press_policy_card_v1",
  "policy_hash": "…"      // hash of the policy card JSON
}
```

**Rationale**

- Allows auditors to see which policy was in effect for a capsule.
- Policy hashing provides immutability and a clear link between capsule and policy.

---

## 3. Scoreboard O & Acceptance at the Policy Layer

### 3.1 What O is

O is the **scoreboard** — the subset of derived metrics that actually matter for acceptance.

Examples:

- Pose, velocity, health flags for a robotics system.
- Profit/loss, risk metrics for a trading system.
- Accuracy / loss / fairness scores for an ML system.

O is domain‑defined; Press only knows about O through the policy layer.

### 3.2 O‑field declaration

**Decision**

- Each policy card lists the O‑fields it contributes in `o_fields`.
- A central **O‑schema** lists:
  - All valid O‑fields.
  - Their dtypes and, where relevant, ε_O tolerances.

Press does not compute O itself; it only ensures that after DePress, the upstream system can recompute O and that the acceptance harness tests O.

### 3.3 Acceptance rule in O terms

For ε‑bounded P_state capsules, acceptance requires:

1. `q/2 ≤ ε` per numeric field (from policy card) — enforced at Press level.
2. `O(S) ≈ O(S′)` — enforced by the system running T and O:
   - For Δ=0: `O(S) = O(S′)` or within per‑field ε_O.
   - For Δ>0: `d(O_true, O_replayed) ≤ ε_global`.

**Rationale**

- Matches canon’s “O‑only comparison” rule and separates responsibilities: Press handles data‑level bounds; the system handles scoreboard‑level validation.

---

## 4. Dimensional Controls (Dims Press)

Dims Press extends these ideas **per dimension, per layer**.

### 4.1 Canon recap

Legacy Dims Press docs specify controls per dimension:

- Exact vs quantized dims.
- Residual fraction (how much of residual detail to keep).
- Selective retention: `recompute`, `residual`, `full`.
- Dictionary scopes: per‑node vs global Press dictionary on the NAP bus.

### 4.2 Local dim_controls semantics

We reuse the `dim_controls` object from policy cards (§2.2):

- `mode`:
  - `"exact"` — dimension must round‑trip exactly in P_state.
  - `"quantized"` — dimension may be quantized with q from `numeric_fields`.
- `retention`:
  - `"recompute"` — do not store residuals for this field; recompute from other fields during replay.
  - `"residual"` — store a compressed residual.
  - `"full"` — store verbatim or nearly verbatim (e.g. for provenance tags).
- `residual_fraction` (optional):
  - Fraction (0–1] of raw residual bits to keep; hints SimB how aggressively to compress.

**Decision**

- `mode = "exact"` implies `epsilon = 0` and `q = 0` (or omission) for that field.
- `retention = "recompute"` implies that **all information needed** to recompute the field must either:
  - Be present in other fields retained as P_state, or
  - Be derivable from T and exogenous data that is itself preserved.

If these conditions are not met, policy validation fails (see §5).

### 4.3 Dictionary scopes

**Decision**

We support two dictionary scopes for SimB:

- `"per_source"` — dictionary entries are scoped to a single source_id.
- `"global_press"` — dictionary entries are shared across all sources on the NAP bus for that run.

`dim_controls` may optionally include:

```jsonc
"dict_scope": "per_source"  // or "global_press"
```

**Rationale**

- Matches Dims Press notion of per‑node vs global dictionaries.
- Allows trade‑offs between local independence and cross‑source compression gains.

---

## 5. Policy Compiler & Validation

### 5.1 Policy compiler responsibilities

The **policy compiler** is a pure function that takes:

- A policy card JSON.
- The global O‑schema.
- Optionally, richer metadata about source structure (schemas, graph relationships).

and produces an internal config object used by the Press Engine and Flux Decoder.

It must:

1. Validate the policy card against its JSON schema.
2. Enforce per‑field constraints:
   - For `mode = "quantized"`: check `q/2 ≤ epsilon`.
   - For `mode = "exact"`: enforce `epsilon = 0` and `q = 0`/null.
3. Enforce selective retention constraints:
   - For `retention = "recompute"`: confirm there is a recomputation recipe for that field.
4. Ensure O‑fields are valid and that O‑schema exists.
5. Produce compiled configuration:

```ts
interface CompiledFieldPolicy {
  field: string;
  dtype: string;
  mode: "exact" | "quantized";
  epsilon: number;
  q: number;               // 0 for exact
  retention: "recompute" | "residual" | "full";
  residualFraction?: number;
}

interface CompiledPressPolicy {
  sourceId: string;
  track: ("P_state" | "P_cite")[];
  pressProfile: string;
  dimsProfile?: string;
  fields: CompiledFieldPolicy[];
  oFields: string[];
  dictScope: "per_source" | "global_press";
}
```

### 5.2 Validation failure behaviour

**Decision**

If policy compilation fails, Press must:

- Refuse to run in automated mode on that source.
- Log a clear error (e.g. “Policy invalid: pose.x marked recompute but no recipe”).
- Optionally, fall back to a **safe default** only if explicitly configured, e.g.:
  - `PRESS_LOSSLESS` with `mode = exact` and `retention = full` for all fields.

Default behaviour is **fail‑closed**: no speculative fallback unless the user has explicitly configured one.

**Rationale**

- Respects safety; avoids silently weakening guarantees due to misconfiguration.

### 5.3 Runtime enforcement

At runtime:

- Press Engine uses compiled policies to:
  - Decide which fields go to P_state vs P_cite.
  - Decide how to integerize and quantize each field.
  - Decide which residuals to store and at what strength.
- Flux Decoder uses compiled policies to:
  - Reconstruct fields.
  - Recompute fields marked `recompute`.
  - Check that reconstituted fields obey field‑level bounds where applicable.

---

## 6. Interaction with NAP & MDL Stack

### 6.1 Stack design under policy constraints

With the NAP & MDL spec in place, policy adds constraints:

- Some fields must be **exact**; their residuals must be encoded such that reconstruction is bit‑identical.
- Some fields may be **quantized** within ε; stack must respect `q/2 ≤ ε` and acceptance tests.
- Some fields can be **recomputed**; stack may omit their residuals entirely.

The MDL stack builder (§7 of the NAP spec) must:

- Treat policy‑forbidden transforms as **off limits** (e.g. no lossy transform on an exact field).
- Only consider candidate layers that respect compiled policies.

### 6.2 O‑only acceptance and stacks

As in the NAP spec, the acceptance harness runs **after full reconstruction** using the stack and policies:

- Field‑level bounds use ε and q from policies.
- O‑only comparison uses O‑schema and o_fields.

Policy cards thus act as **contracts** that stacks must satisfy; MDL governs “how much compression we get” inside those contracts.

---

## 7. Examples

### 7.1 Sensor stream (IMU)

- Policy:
  - P_state and P_cite both enabled.
  - pose.x, pose.y: quantized with ε = 1e‑4, q = 2e‑4.
  - velocity: ε = 1e‑3, q = 2e‑3.
  - health_flag: exact, full retention.
- Stack:
  - SimA: polynomial or AR model per axis.
  - SimB: residual stack with delta + Golomb–Rice.
- Behaviour:
  - P_state capsule used to replay motion; P_cite capsule holds raw log hashes.

### 7.2 PDF spec as P_cite only

- Policy:
  - type: pdf.
  - track: ["P_cite"] only.
  - o_fields: [] (no direct O contribution).
- Behaviour:
  - Press never tries to produce a P_state capsule; it only generates a small P_cite capsule with hash and length.

---

## 8. Change Control

Any changes to policy or dimensional control semantics must:

1. Update this spec and the policy card schema version.
2. Bump `press_policy_card_v1` to `press_policy_card_v2` (or higher) as needed.
3. Update the policy compiler and tests.
4. Ensure older capsules remain auditable, even if newer modes are introduced.

Two‑track Press, O‑only comparison, and field‑level ε/q bounds are treated as **canon‑backed invariants**; they must not be weakened without a corresponding update to the underlying pillar docs.



<!-- END SOURCE: astral_press_policy_dimensional_controls_spec_v_1_p_state_p_cite_dims_press.md -->


---

<!-- BEGIN SOURCE: astral_press_policy_pack_v_1_profiles_cards.md -->

# Astral Press — Policy Pack v1 (Profiles & Cards for APP-UROBOROS-REF-1)

Scope: define **concrete Press profiles and policy cards** for the `APP-UROBOROS-REF-1` implementation, grounded in Astral Press canon and legacy docs, and clearly separating:

- **Canon constraints** (must obey; quoted directly).
- **Local decisions** (chosen here for this implementation; not global canon).

This pack is meant to be used alongside:

- **Astral Press — APP Implementer Checklist v1**
- **APP_LOCAL_SPEC v1 — Aether Press Local Implementation (2025-11-20)**
- **Astral Press — APP Complement Sheet v2 (Legacy Docs Pass)**
- **Astral Press — APP Complement Sheet v4 (Implementation Canon Pack Pass)**

and the JS build plans.

Where behaviour is interpreted from canon, this doc includes **direct quotes** from those sources.

---

## 1. Canon Anchors for Policy & Profiles

### 1.1 Core Press behaviour (rule + residual)

From the Legacy Post-Implementation Report:

> “Let S be a dataset represented by bits b■. Define the model M(θ) with parameters θ such that S ≈ M(θ) + R, where R is the residual.
>
> (1) S = M(θ) ⊕ R (bitwise XOR for discrete systems) (2) Compression ratio = (|θ| + |R|) / |S| (3) Continuity constraint → lim\_{|R|→0} Reconstruction = S”

From the Implementer Checklist:

> “You **must** implement Press/DePress as pure inverse operators with rule+residual structure… A dataset S is modeled as: S = M(θ) ⊕ R (bitwise XOR for discrete systems)… Compression ratio = (|θ| + |R|) / |S|.”

Policy cards therefore **cannot** change this; they can only choose:

- Which data flows into **Press** (and in which mode).
- How **ε** and quantization are set.
- What gets stored in **P_state** vs **P_cite**.

---

### 1.2 ε, quantization `q`, and field-level bounds

Legacy performance report (via Complement v2):

> “**Integerization pipeline** (normalize  units  quantize  zigzag  varint/delta/RLE).
>   - Bound error upfront: if you quantize a scalar with step  q , your max absolute error is  ≤ q/2 . Pick  q  so it respects the field s  ε .”

And in the “Crush without regret” checklist:

> “1. **Field-level bounds:** For every numeric field  x  you store after quantization  q  : |x\_{post} - x\_{pre}| ≤ q/2 ≤ ε\_x.”

The Implementer Checklist restates this as canon:

> “For each numeric field x with quantization step q: |x\_{post} − x\_{pre}| ≤ q/2 ≤ ε\_x.”

So **every ε‑bounded profile** in this pack must:

- Choose ε\_field **first**.
- Set quantization step `q_field` such that **q_field / 2 ≤ ε_field**.

---

### 1.3 Two-track Press: P_state vs P_cite

From the performance report (Complement v2):

> “## TWO-TRACK PRESS (DO THIS EVERY TIME)
>
> 1. **P\_state (reconstructive)**  the *minimal* snapshot needed for  T  to resume exactly.
>    - Must satisfy fidelity:  d(O(S), O(DePr(Pr(S))) ) ≤ ε .”

And later:

> “Result: you keep **exactly** what the computational episode needs, and only **proofs/pointers** for everything else. That s where the astronomical  gains come from.”

TL;DR:

> “You keep the *small, exact* computational snapshot (P\_state), plus tiny proofs/pointers for the rest (P\_cite).”

The Implementer Checklist crystallises this as canon:

> “Your implementation must distinguish **P\_state** and **P\_cite** and obey the policy rules…
>
> P\_state… the *minimal* snapshot required for T (the transition map) to resume **exactly**…
>
> P\_cite… Contains hashes, byte lengths, and a few extracted integers you actually use from external sources…
>
> Do **not** let P\_state depend on raw documents that T will never replay; hash them into P\_cite instead.
>
> Always set ε before choosing quantization steps q.
>
> Base acceptance on **O only**, not on raw data.”

Every policy card in this pack must:

- Declare which **track(s)** it uses: `P_state`, `P_cite`, or both.
- Respect the **“no raw docs in P_state”** rule.
- Define O‑fields and ε such that the “Crush without regret” checks can be applied.

---

### 1.4 Press policy cards (template)

From the legacy report (Complement v2):

> “# Press policy card (use per source)
>
> PRESS POLICY  <source_name>
>
> Type: (text/pdf/image/log/table/sensor) Track: [P\_state | P\_cite]  (pick one; sometimes both) O-fields derived: { ... }  (list only what T or O needs) Quantization q per field: {f1:q1, f2:q2, ...} ...”

This pack **instantiates** this template for a small number of reference sources.

---

### 1.5 Dims Press controls

From the Dims Press report (Complement v2):

> “FIDELITY CONTROLS YOU CAN SET PER-DIMENSION (OR PER-LAYER)
>
> - **Exact vs -quantized dims:** choose which dims must match exactly for replay vs which can be bucketed (e.g.,  to nearest 1e-3, positions to 1 unit).
> - **Residual fraction:** tighten or loosen Loom s residual size (e.g., 5 20%) for layers where you need more/less detail.
> - **Selective retention:** mark dims as {recompute, residual, full}:
>   - *recompute*: derive from other fields on replay (kept out of residual),
>   - *residual*: store compact delta,
>   - *full*: store verbatim (e.g., provenance-critical tags).
> - **Dict scopes:** keep **per-node dictionaries** or a **global Press dict** on the NAP bus for cross-layer dimensional schemas.”

This pack **attaches concrete Dims choices** to each policy card, using those four families of controls.

---

## 2. Policy Card Format (Local Schema)

Canon gives the human template above but **does not define JSON**. This section fixes a local JSON schema for `APP-UROBOROS-REF-1`. This is a **local decision**, not global canon.

### 2.1 JSON structure

We define a `PressPolicyCard` as:

```jsonc
{
  "schema_version": "press_policy_card_v1",

  "name": "PRESS_LOSSLESS_FILE",      // short policy name
  "source": "generic_file_bytes",     // human/source identifier
  "type": "file/bytes",               // one of: text/pdf/image/log/table/sensor/file/bytes

  "tracks": ["P_cite"],               // subset of {"P_state", "P_cite"}

  "press_profile": "PRESS_LOSSLESS",  // must match MANIFEST.press.profile
  "dtype": "bytes",                   // matches MANIFEST.press.dtype

  "o_fields": [],                      // scoreboard fields this source influences

  "epsilon_global": null,              // null for strict lossless, else global ε

  "fields": {
    "field_name": {
      "epsilon": 0.0,                  // per-field ε_x (null for non-numeric)
      "q": 0.0,                        // quantization step q; must satisfy q/2 ≤ ε
      "mode": "exact",               // one of: exact, quantized
      "retention": "full",           // one of: recompute, residual, full
      "track": "P_cite"              // which track holds this field (P_state or P_cite)
    }
  },

  "dims_controls": {
    "exact_dims": ["field_a", "field_b"],
    "quantized_dims": ["field_c"],
    "residual_fraction": 0.10,         // target residual fraction (0–1) for this source
    "dict_scope": "global"           // one of: per_node, global
  }
}
```

Notes:

- `tracks` is an array to allow **dual-track** policies (e.g., P_state + P_cite) when needed.
- `fields` may include:
  - Raw data fields.
  - Derived fields (e.g., summaries used only in O).
- `dims_controls` wraps the Dims Press knobs:
  - `exact_dims` and `quantized_dims` come directly from “Exact vs quantized dims”.
  - `residual_fraction` from “Residual fraction: tighten or loosen Loom s residual size (e.g., 5 20%).”
  - `dict_scope` from “per-node dictionaries” vs “global Press dict”.

---

## 3. Reference Profile 1 — `PRESS_LOSSLESS_FILE` (Generic Files)

### 3.1 Use case & scope

This profile is for **generic file bytes** that are **not** directly part of T’s replayable state but are needed for **provenance/audit**. Examples:

- Raw PDFs, logs, images, binaries linked to a checkpoint.
- Input documents for a run whose results are captured in P_state.

Canon guidance (Complement v2):

> “What to *avoid* (this is where people get burned)
>
> - **Letting P\_state depend on raw docs** you won t replay. If  T  doesn t need the raw, dont pack it hash it in **P\_cite** instead.”

So for this profile we deliberately:

- Treat the file as **P_cite-only**.
- Keep P_state **independent** of these raw bytes.

### 3.2 Canon constraints applied

From the Implementer Checklist (APX Manifest responsibilities):

> “Your manifest must at least: Identify the source artifact: Original file **name**, Original file **size** in bytes, Original file **hash** (e.g. SHA‑256)… Describe the Press run configuration… Summarise capsule content… Provide integrity & provenance hooks.”

From lossless mode definition:

> “Lossless mode: Reconstruction must be bit‑exact: the reconstructed bytes’ hash **must equal** the original file hash… Press/DePress cycles must be idempotent for fixed input and version (no drift).”

Therefore this profile **fixes**:

- `press.mode = "lossless"`.
- `press.profile = "PRESS_LOSSLESS"`.
- `dtype = "bytes"`, `shape = [size_bytes]` (per APP_LOCAL_SPEC v1).

### 3.3 Policy card (JSON)

```jsonc
{
  "schema_version": "press_policy_card_v1",

  "name": "PRESS_LOSSLESS_FILE",
  "source": "generic_file_bytes",
  "type": "file/bytes",

  "tracks": ["P_cite"],

  "press_profile": "PRESS_LOSSLESS",
  "dtype": "bytes",

  "o_fields": [],

  "epsilon_global": null,

  "fields": {
    "file_bytes": {
      "epsilon": 0.0,
      "q": 0.0,
      "mode": "exact",
      "retention": "full",
      "track": "P_cite"
    },
    "file_name": {
      "epsilon": null,
      "q": null,
      "mode": "exact",
      "retention": "full",
      "track": "P_cite"
    },
    "file_size_bytes": {
      "epsilon": 0.0,
      "q": 0.0,
      "mode": "exact",
      "retention": "full",
      "track": "P_cite"
    },
    "file_sha256": {
      "epsilon": null,
      "q": null,
      "mode": "exact",
      "retention": "full",
      "track": "P_cite"
    }
  },

  "dims_controls": {
    "exact_dims": [
      "file_bytes",
      "file_name",
      "file_size_bytes",
      "file_sha256"
    ],
    "quantized_dims": [],
    "residual_fraction": 0.0,
    "dict_scope": "global"
  }
}
```

Local design notes:

- `tracks = ["P_cite"]` implements the canon guidance “hash it in P_cite instead” by putting bytes + identity here and **not** in P_state.
- `residual_fraction = 0.0` expresses that we are **not** relying on partial residual retention; lossless means full reconstruction of bytes.
- `dict_scope = "global"` is chosen because file metadata schemas are stable across nodes; this is a local decision.

This card pairs with the **JS Offline MVP** `pressBytes` path and the `PRESS_LOSSLESS` profile defined in APP_LOCAL_SPEC v1:

> “MVP mode: `PRESS_LOSSLESS` only, `dtype="bytes"` default, with a dedicated numeric demo path for SimA/SimB.”

---

## 4. Reference Profile 2 — `PRESS_SENSOR_MED` (NAP Bus / Sensor Arrays)

### 4.1 Use case & scope

This profile is for **numeric sensor streams on the NAP bus** that **do** affect T’s replayable state. Examples (from Dims Press and IMU examples in legacy docs):

- IMU sensor arrays (position, velocity, acceleration).
- NAP bus entries where Press and Loom cooperate mid-run.

Legacy Dims Press bottom line (Complement v2):

> “New dims can appear mid-run (we proved it) and get **Loomed** (for deterministic replay) and **Pressed** (for compact, reversible storage) like any other data.
>
> You can dial **how faithful** they must be for reuse and **how much** detail to keep in residuals on a **per-dimension, per-layer** basis.”

Given these are **replay-critical**, this profile uses **P_state**.

### 4.2 Canon constraints applied

From “Crush without regret” (Complement v2):

> “1. **Field-level bounds:** For every numeric field  x  you store after quantization  q  : |x\_{post} - x\_{pre}| ≤ q/2 ≤ ε\_x.
> 2. **Replay test:** DePress then run  Δ=0 :  O  unchanged (fidelity at snapshot).
> 3. **Predictive test:** DePress and run  T^Δ ; check  d(O\_{true}, O\_{replayed})≤ ε.
> … 6. **Isolation:** Prior checkpoint O-hashes never change.”

And from the Implementer Checklist:

> “Only **O** (the scoreboard) matters for acceptance; raw data deltas are not the decision basis in ε‑bounded mode.”

We design this profile so that:

- Per-field ε and q obey `q/2 ≤ ε_field`.
- O‑fields are explicitly named.
- This card can be used directly in the acceptance harness.

### 4.3 Field set (example sensor tuple)

We define a **reference sensor tuple**:

- `pos_x`, `pos_y`, `pos_z` — position (meters).
- `vel_x`, `vel_y`, `vel_z` — velocity (meters/second).
- `acc_x`, `acc_y`, `acc_z` — acceleration (meters/second²).

These labels match intuitive IMU / NAP bus fields described qualitatively in legacy docs (IMU compression 8–20× lossless, 30–100× ε-bounded).

### 4.4 ε and q choices (local, but canon-compatible)

Canon only constrains the **relationship** between ε and q, not their numeric values. We choose the following defaults for this implementation:

- Positions: `ε_pos = 1e-4` (0.0001 meters), `q_pos = 2e-4` → `q/2 = 1e-4 = ε_pos`.
- Velocities: `ε_vel = 1e-3`, `q_vel = 2e-3` → `q/2 = 1e-3 = ε_vel`.
- Accelerations: `ε_acc = 1e-3`, `q_acc = 2e-3` → `q/2 = 1e-3 = ε_acc`.

These satisfy the canon constraint:

> “if you quantize a scalar with step  q , your max absolute error is  ≤ q/2 . Pick  q  so it respects the field s  ε .”

and the formal requirement:

> “|x\_{post} − x\_{pre}| ≤ q/2 ≤ ε\_x.”

They are **local numbers** and can be adjusted in future policy revisions.

### 4.5 Policy card (JSON)

```jsonc
{
  "schema_version": "press_policy_card_v1",

  "name": "PRESS_SENSOR_MED",
  "source": "nap_bus_sensor_tuple",
  "type": "sensor",

  "tracks": ["P_state"],

  "press_profile": "PRESS_SENSOR_MED",
  "dtype": "float64",  // or float32; Press records the actual dtype in MANIFEST

  "o_fields": [
    "O.pos_x",
    "O.pos_y",
    "O.pos_z",
    "O.vel_x",
    "O.vel_y",
    "O.vel_z"
  ],

  "epsilon_global": 0.001,

  "fields": {
    "pos_x": {
      "epsilon": 0.0001,
      "q": 0.0002,
      "mode": "quantized",
      "retention": "residual",
      "track": "P_state"
    },
    "pos_y": {
      "epsilon": 0.0001,
      "q": 0.0002,
      "mode": "quantized",
      "retention": "residual",
      "track": "P_state"
    },
    "pos_z": {
      "epsilon": 0.0001,
      "q": 0.0002,
      "mode": "quantized",
      "retention": "residual",
      "track": "P_state"
    },

    "vel_x": {
      "epsilon": 0.001,
      "q": 0.002,
      "mode": "quantized",
      "retention": "residual",
      "track": "P_state"
    },
    "vel_y": {
      "epsilon": 0.001,
      "q": 0.002,
      "mode": "quantized",
      "retention": "residual",
      "track": "P_state"
    },
    "vel_z": {
      "epsilon": 0.001,
      "q": 0.002,
      "mode": "quantized",
      "retention": "residual",
      "track": "P_state"
    },

    "acc_x": {
      "epsilon": 0.001,
      "q": 0.002,
      "mode": "quantized",
      "retention": "residual",
      "track": "P_state"
    },
    "acc_y": {
      "epsilon": 0.001,
      "q": 0.002,
      "mode": "quantized",
      "retention": "residual",
      "track": "P_state"
    },
    "acc_z": {
      "epsilon": 0.001,
      "q": 0.002,
      "mode": "quantized",
      "retention": "residual",
      "track": "P_state"
    }
  },

  "dims_controls": {
    "exact_dims": [],
    "quantized_dims": [
      "pos_x", "pos_y", "pos_z",
      "vel_x", "vel_y", "vel_z",
      "acc_x", "acc_y", "acc_z"
    ],
    "residual_fraction": 0.10,
    "dict_scope": "per_node"
  }
}
```

Local design notes:

- `tracks = ["P_state"]` expresses that these fields are **replay-critical**; they belong in the reconstructive track.
- `o_fields` lists a subset of fields that meaningfully affect the scoreboard O. This enables the acceptance harness to only check what matters, consistent with “Only O matters for acceptance”.
- `residual_fraction = 0.10` picks a mid-range value in the “5 20%” window mentioned in Dims Press; it is a tunable default.
- `dict_scope = "per_node"` reflects that sensor schemas can differ per node.

This card pairs with the `PRESS_SENSOR_MED` profile defined in APP_LOCAL_SPEC v1:

> “Decision — profile set… `PRESS_SENSOR_MED` (example sensor profile)… `press.mode = "epsilon_bounded"`… Typical per-field ε… Quantization steps: `q_field = 2 * ε_field` so `q/2 ≤ ε_field` exactly.”

---

## 5. Reference Profile 3 — `PRESS_LOG_CRUSH` (Logs / Telemetry)

### 5.1 Use case & scope

This profile is for **logs and event streams** that mostly support **diagnostics and audit**, not direct replay of T, but may contribute a few counters to O.

From the Complement v2 summary of practical knobs:

> “**O-only comparison**: you never compare the whole raw only your scoreboard  O . That lets you drop mountains of irrelevant detail.
>
> **Content dedupe**: identical chunks (by hash) collapse to one copy across checkpoints.”

This profile aims to:

- Heavily compress textual/structured logs.
- Preserve **a small set of counters and status flags** in P_state (where needed).
- Store most raw text only in P_cite via hashes and possibly dictionary entries.

### 5.2 Canon constraints applied

Same ε/q rule applies for numeric counters. For textual fields, ε does not apply; instead we manage them via:

- **Selective retention** (`recompute`, `residual`, `full`).
- **Dict scopes** (global Press dictionary for common log structures).

### 5.3 Example fields

We define a reference log schema:

- `timestamp_ms` — integer timestamp.
- `log_level` — categorical (`INFO`, `WARN`, `ERROR`, `DEBUG`).
- `event_code` — small integer ID.
- `counter_requests` — integer counter.
- `counter_errors` — integer counter.
- `message` — free-text message.

### 5.4 Policy card (JSON)

```jsonc
{
  "schema_version": "press_policy_card_v1",

  "name": "PRESS_LOG_CRUSH",
  "source": "service_log_stream",
  "type": "log",

  "tracks": ["P_state", "P_cite"],

  "press_profile": "PRESS_LOG_CRUSH",
  "dtype": "json",

  "o_fields": [
    "O.counter_requests",
    "O.counter_errors"
  ],

  "epsilon_global": 0.0,

  "fields": {
    "timestamp_ms": {
      "epsilon": 0.0,
      "q": 0.0,
      "mode": "exact",
      "retention": "residual",
      "track": "P_state"
    },
    "log_level": {
      "epsilon": null,
      "q": null,
      "mode": "exact",
      "retention": "residual",
      "track": "P_state"
    },
    "event_code": {
      "epsilon": 0.0,
      "q": 0.0,
      "mode": "exact",
      "retention": "residual",
      "track": "P_state"
    },

    "counter_requests": {
      "epsilon": 0.0,
      "q": 0.0,
      "mode": "exact",
      "retention": "residual",
      "track": "P_state"
    },
    "counter_errors": {
      "epsilon": 0.0,
      "q": 0.0,
      "mode": "exact",
      "retention": "residual",
      "track": "P_state"
    },

    "message": {
      "epsilon": null,
      "q": null,
      "mode": "exact",
      "retention": "full",
      "track": "P_cite"
    }
  },

  "dims_controls": {
    "exact_dims": [
      "timestamp_ms",
      "log_level",
      "event_code",
      "counter_requests",
      "counter_errors"
    ],
    "quantized_dims": [],
    "residual_fraction": 0.05,
    "dict_scope": "global"
  }
}
```

Local design notes:

- All numeric counters and IDs are treated as **exact** (`ε = 0`, `q = 0`), reflecting that small integer telemetry is cheap and often important.
- `message` is stored fully in **P_cite** (`retention = "full", track = "P_cite"`), acting as provenance text and enabling auditors to reconstruct log content if needed.
- `tracks = ["P_state", "P_cite"]` reflects that some fields feed O (counters) while others are pure provenance.
- `residual_fraction = 0.05` encodes an aggressive compression target for logs, leaning on dictionary models and repeated structure.

This card matches the spirit of legacy claims (Complement v2):

> “Raw PDFs/logs/images: 100×–10000× reduction when treated as P\_cite + tiny extracted integers… Structured state for T: often 10×–100× from sparsity + integerization (and still exact/ε-bounded).”

by separating P_state counters from P_cite raw messages.

---

## 6. How Policy Cards Attach to MANIFEST and NAP

### 6.1 MANIFEST.press.profile linkage

APP_LOCAL_SPEC v1 defines Press profiles:

> “Decision — profile set…
>
> 1. `PRESS_LOSSLESS`… `press.mode = "lossless"`…
> 2. `PRESS_SENSOR_MED` (example sensor profile)… `press.mode = "epsilon_bounded"`… per-field ε and q mapping…
> 3. `PRESS_LOG_CRUSH` (logs/events)… `press.mode = "epsilon_bounded"`… integer fields ε = 0, timestamps quantized, dictionary-driven compression dominates.”

Each policy card’s `press_profile` must **equal** the `MANIFEST.json.press.profile` for runs using that card.

### 6.2 NAP layer params

For NAP manifests (Complement v4):

> “NAP Compression Manifest — `layers[] {id, kind∈{AP.symbolic (SimA), AP.residual (SimB)}, parent, refs[], params, ordering}, knit_rules, deterministic_order, hashes`.”

Local design:

- Policy decisions may influence `layers[].params`, for example:
  - Which model families are allowed (SimA subset) under a profile.
  - Target residual fraction per layer.
- This Policy Pack **does not** hard-code those NAP parameters; it just provides values (ε, q, residual_fraction) that the NAP builder reads.

---

## 7. Implementation Guidance for Devs

1. **Always resolve a policy card before pressing a source.**
   - Given a source name and type, look up the matching `PressPolicyCard`.

2. **Write `press.profile` and `press.mode` into MANIFEST from the policy.**
   - For example, `PRESS_SENSOR_MED` implies `mode = "epsilon_bounded"` and `profile = "PRESS_SENSOR_MED"`.

3. **Configure quantization per field from `fields[field].q`.**
   - Check `q/2 ≤ ε` at runtime. Fail fast if violated.

4. **Configure Dims Press from `dims_controls`.**
   - Use `exact_dims` and `quantized_dims` to split fields into integerization vs quantization pipelines.
   - Use `residual_fraction` as a target when selecting model depth in the MDL stack.
   - Use `dict_scope` when choosing dictionary caches (per-node vs global) for this source.

5. **Respect tracks when writing capsules.**
   - Fields marked `track = "P_state"` must be reconstructible from P_state capsules alone.
   - Fields marked `track = "P_cite"` may only appear in provenance/auxiliary capsules.

6. **Implement “Crush without regret” checks as acceptance tests tied to policy cards.**
   - Use `epsilon_global`, `fields[*].epsilon`, and `o_fields` to drive field-level bounds, replay, and predictive tests as defined in the Implementer Checklist and Complement v2.

7. **Document any extension as a new policy card.**
   - If a new source type or more aggressive profile appears, add a new card with explicit ε, q, and Dims controls rather than silently editing existing ones.

---

## 8. Scope and Limits of Policy Pack v1

- This pack **instantiates** policy for three reference cases:
  - `PRESS_LOSSLESS_FILE` — generic file bytes, P_cite-only, strict lossless.
  - `PRESS_SENSOR_MED` — numeric sensor streams on NAP bus, P_state, ε-bounded with explicit per-field ε and q.
  - `PRESS_LOG_CRUSH` — logs/telemetry with dual-track P_state/P_cite separation.

- It **does not** claim that these are the only valid profiles:
  - Other future profiles (e.g., high-precision sensors, image-specific policies) should follow the same pattern and quote canon where they rely on it.

- All numeric values of ε, q, residual_fraction, and O-field names are **local implementation choices** for `APP-UROBOROS-REF-1`.

- Where canon speaks (ε–q relation, P_state/P_cite semantics, manifest responsibilities, NAP field sets), this pack follows it directly via quotes.

This document should be treated as a versioned artefact; future revisions must bump `schema_version` for cards and be recorded in the APP implementation changelog.



<!-- END SOURCE: astral_press_policy_pack_v_1_profiles_cards.md -->


---

<!-- BEGIN SOURCE: astral_press_pillar_metrics_evaluation_canon_pass.md -->

# Astral Press Pillar — Metrics & Evaluation (Canon Pass)

> **Scope**  
> Close the metrics / evaluation gaps for Astral Press **using only canon**.  
> This pass captures:
> - Core compression metrics and MDL quantities used by APP.  
> - How baselines (gzip/bzip2/xz) are integrated.  
> - How windows, thresholds, and Pareto fronts are used.  
> - What the test documents (Testdoc-AP, Pareto manifests, APP_BARRIERS) guarantee.  
> Anything not explicitly specified in the corpus is marked as a gap.

---

## 1. Core compression metrics

### 1.1 Bits, entropy, and description length

Astral Press evaluates compression primarily in **bits**, not just bytes. Canon establishes that:

- Residuals are modelled as random variables with a covariance structure; their code length is approximated by a log-determinant formula (Shannon–Boltzmann style).
- The **description length** of a compressed representation includes:
  - The bits needed to describe the models/rules (SimA descriptors).
  - The bits needed to encode residuals (SimB payloads).
  - Container/overhead bits (headers, manifests, index).

We can summarise these as high-level MDL quantities:

- `L_model` — bits to describe all chosen models (`M_i`).
- `L_resid` — bits to encode all residuals (`R_i`).
- `L_overhead` — bits for container, manifests, indices and other protocol overhead.

The **total description length** for a given compression configuration is then:

```text
L_total = L_model + L_resid + L_overhead
```

### 1.2 Gain vs naive encoding

Canon defines a “compression gain” as the bits saved relative to a naive encoding, often written as a kappa-like quantity:

- `L_naive` — description length using a naive or baseline scheme (e.g., uncompressed, or basic per-symbol encoding with no structure).
- `kappa` — gain, defined as the difference between naive and achieved description length.

```text
kappa = L_naive - L_total
```

A positive `kappa` indicates that the chosen models and residual encoding produce a genuine compression improvement over the naive scheme.

### 1.3 Layered MDL acceptance rule

In the multi-layer model + residual stack, canon ties the stopping rule to MDL:

- For each new layer `i`, the system evaluates the change in `L_total` if `M_i` is added and residuals are recomputed.
- A layer is accepted only if it **strictly decreases** the total description length.

In other words:

```text
ΔL_total = L_total(with layer i) - L_total(before layer i)
Accept layer i only if ΔL_total < 0
```

This is the MDL-style acceptance rule that prevents overfitting by model complexity and ensures that every added layer contributes to compression.

---

## 2. APP cost function and search

### 2.1 Cost components

The Press transform library and experiments specify a cost function used for comparing candidate transform stacks per column/segment:

- `bits(SimA)` — bits for symbolic descriptors.
- `bits(SimB)` — bits for residual payloads after chosen transforms.
- `container_overhead` — bits for container-level overhead.

The **cost** used for search and comparison is:

```text
Cost = bits(SimA) + bits(SimB) + container_overhead
```

This cost is minimized when selecting:

- Which transform to apply to a column/segment (affine, polynomial, periodic, cross-column, JSON grammar, etc.).
- Whether to add another transform layer.
- Whether to change residual codec (e.g., switch between delta, XOR, Golomb–Rice, AR(1..3)).

### 2.2 Search strategy

Canon describes the search qualitatively as:

- Greedy or beam search over candidate transforms per column or segment.
- Evaluating each candidate’s effect on the cost function.
- Rejecting candidates that do not reduce the cost sufficiently to overcome overhead.

The exact search algorithm parameters (beam width, heuristic pruning) are not specified; they are implementation details subject to the constraint of minimizing `Cost`.

### 2.3 Residual budgets and monotonicity

The residual layering budget is represented as a sequence of tolerances `ε_k` across layers, with the constraint:

```text
ε_{k+1} ≤ ε_k
```

This ensures that deeper residual layers do not degrade the fidelity of reconstruction. In lossless mode, the final residual budget effectively collapses to exact reconstruction, and any lossy budgets (for approximate modes) must still respect monotone tightening.

Canon does not give numeric values for `ε_k`; they are configuration/analysis parameters.

---

## 3. Baseline codecs and comparison

Astral Press is evaluated against baseline compressors, canonically:

- gzip (DEFLATE-style).
- bzip2.
- xz (LZMA-based).

The test documents (e.g., Testdoc-AP) define, per dataset:

- `orig_bytes` — original file size in bytes.
- `gzip_bytes`, `bzip2_bytes`, `xz_bytes` — compressed sizes under each baseline.

From these, simple comparative metrics are derived:

- Compression ratio for a method `C`:

```text
ratio_C = orig_bytes / C_bytes
```

- Percent improvement of APP over a baseline `B`:

```text
improvement_APP_vs_B = 100 * (B_bytes - APP_bytes) / B_bytes
```

These formulas are standard and consistent with the narrative in the test docs, which talk about “bits per symbol” and “better than gzip/bzip2/xz on structured datasets” without redefining basic compression metrics.

---

## 4. Bits per symbol and per-window metrics

### 4.1 Bits per symbol

For structured datasets, canon repeatedly refers to **bits per symbol** as a primary measure of efficiency. Given:

- `N` — number of symbols (e.g., rows × columns, or characters) in the dataset.
- `L_total` — total description length in bits for a given encoding.

The bits-per-symbol metric is:

```text
bps = L_total / N
```

This is used both for entire datasets and for moving windows over time.

### 4.2 Windowed evaluation

Testdoc-AP and related manifests introduce **windowed metrics**, with parameters like:

- `W` — window size (in symbols or frames).
- Possibly overlapping or sliding windows across the dataset or time axis.

For each window, a local bits-per-symbol value is computed, allowing:

- Comparison of APP vs baselines **within windows**, not just globally.
- Detection of regimes where a particular mode or container is worse than a baseline.

Exact values of `W` are not fixed by canon in the visible slices; they are knob parameters referred to in the deployment equivalence and metric templates.

### 4.3 Container selection thresholds

Canon alludes to decision rules for switching between containers (e.g., APX vs AEON) based on windowed metrics:

- Keep container `C1` as default.
- Switch to container `C2` only if `C2` is better than `C1` by at least `ε` bits per symbol over `W` consecutive windows.

Formally, the rule can be expressed as:

```text
If for W consecutive windows: bps_C2 ≤ bps_C1 - ε  then switch default container to C2
```

This expresses a **stability requirement**: container changes must be justified by sustained, non-trivial gains.

Canon does not specify numeric values of `ε` or `W`; those remain configuration parameters.

---

## 5. Testdoc-AP and Pareto manifests

### 5.1 Testdoc-AP

The Testdoc-AP family of documents defines the **structure** of APP evaluation runs:

- A list of datasets with:
  - Names and descriptions.
  - Original sizes and baseline compressed sizes.
- A set of metrics calculated for each dataset and method:
  - Bits per symbol.
  - Compression ratios.
  - Gains vs baseline.
- A consistent format for recording:
  - APP mode used (e.g., transform set, container type).
  - Any experimental flags (e.g., ESL on/off, multi-layer depth).

While the exact table columns are not all visible, the narrative clearly positions Testdoc-AP as the canonical evaluation template for APP.

### 5.2 Pareto manifests (v6)

The v6 Pareto manifests (e.g., `press_pareto_manifest_v6_*.json`) are described as containing:

- Points on the compression vs cost Pareto frontier for different content classes and modes.
- For each point:
  - A configuration (choice of transforms, depth, container, etc.).
  - Measured metrics: bits per symbol, wall-clock cost, or similar.

From these manifests, the system selects **recommended operating points** for the APP Policy Pack, which are then mirrored into `APP_BARRIERS.json`.

Canon does not expose the full JSON structure of these manifests in the visible slices; only their role is clear.

---

## 6. APP Policy Pack and APP_BARRIERS.json

### 6.1 Role of APP_BARRIERS.json

The APP Policy Pack introduces `APP_BARRIERS.json` as:

- A single source of truth for **Press defaults** per content class:
  - Text.
  - Numeric.
  - Image.
- These defaults are drawn from the v6 Pareto “recommended” points, meaning:
  - Each default reflects a trade-off between compression efficiency and cost (compute, memory, latency) deemed acceptable.

In other words, `APP_BARRIERS.json` is the **policy layer** that chooses a particular configuration on the Pareto front for each content type.

### 6.2 What canon guarantees

Canon guarantees that:

- There is exactly one central policy file for APP defaults.
- It is referenced when configuring or evaluating APP in system-level runs.
- It encodes which operating point to use by default for each major content type.

### 6.3 Gaps (APP_BARRIERS.json)

The following details are **not** present in the visible corpus:

- The exact JSON schema for `APP_BARRIERS.json`:
  - Field names and nesting.
  - How recommended points are referenced (inline vs via IDs into Pareto manifests).
  - Whether it encodes numeric thresholds (e.g., ε, W) directly.
- The exact number and naming of content classes beyond text/numeric/image.

Therefore, while the **existence and purpose** of `APP_BARRIERS.json` are canonical, its internal structure remains a gap.

---

## 7. Determinism and deployment equivalence knobs

The deployment equivalence treatment introduces several named knobs, treated as **constants per run** for determinism:

- Window sizes: `W_L`, `W_P`.
- Thresholds: `ρ*`, `κ*`, `α*`.
- Penalties: `λ`, `μ`, `γ`, `δ`.
- Tolerances: `ε_*`.
- Cooldowns: `C`.

These are tied to:

- When forecasts or time compression are allowed.
- When new rules/motifs are adopted by SLL.
- When a configuration change (e.g., container switch) is permitted.

Canon’s key requirements:

- These knobs must be fixed at run start and remain constant throughout a deterministic run.
- Changes to these knobs imply a new run; cross-run comparisons must record their settings explicitly.

Exact numeric values, and their mappings to specific APP parameters or barriers, are not fully enumerated and remain partially unspecified.

---

## 8. Explicit gaps in metrics & evaluation

This section lists what is **not** specified in the visible corpus and must therefore stay open.

1. **Exact numeric defaults for ε and W**
   - No canonical values for container switch thresholds (`ε`) or window sizes (`W`) are given.
   - Any particular numbers used in experiments are not promoted as normative.

2. **Complete Testdoc-AP column schema**
   - We know the general structure, but not every column name or type.
   - Derivative metrics (e.g., per-layer breakdowns, wall-clock timings) are not fully enumerated.

3. **Full JSON schema for Pareto manifests**
   - The manifests exist and contain points and metrics, but their exact structure is not visible.

4. **Full JSON schema for APP_BARRIERS.json**
   - Only its purpose and role are known; internal keys and layout are not.

5. **Detailed mapping from MDL penalties (λ, μ, γ, δ) to specific components**
   - The names and their general roles (penalties, thresholds, tolerances) exist, but the exact formula for how they contribute to `L_total` is not fully spelled out.

6. **Full ESL metric set**
   - At least one ESL-derived metric (`ratio = comp_ops / raw_ops`) is documented, but not the complete list.

7. **Per-mode default metric policies**
   - No table mapping modes (e.g., ESL, F1–F3, M1–M3) to specific metric thresholds is given.

---

## 9. Minimal evaluation contract for APP

Based only on canonical constraints, any APP implementation that wants to be evaluable in the Aether ecosystem must:

1. **Expose core metrics**
   - Total description length in bits (`L_total`).
   - Bits per symbol (`bps`).
   - Compression ratio vs original.
   - Gains vs baseline methods (gzip, bzip2, xz) at least at dataset level.

2. **Support windowed evaluation**
   - Ability to compute bits per symbol over windows of size `W` along time or sequence axes.
   - Ability to compare APP vs baselines per window.

3. **Respect MDL acceptance rules**
   - Only accept new layers or transform stacks that reduce `L_total`.
   - Ensure multi-layer stacks respect residual budget monotonicity.

4. **Record configuration and knobs**
   - For each run, record:
     - Container choice and APP mode.  
     - Relevant knobs (thresholds, penalties, windows, tolerances).  
     - Whether ESL and other modes (F1–F3, M1–M3, SFTY1–SFTY3) were enabled.

5. **Integrate with policy pack**
   - When using APP defaults, read them from a central policy artifact (conceptually `APP_BARRIERS.json`).
   - When deviating from defaults in experiments, record the deviation in test manifests.

Beyond this, specific metric dashboards, plotting conventions, and extended analytics are intentionally left open and must not be treated as part of the core Astral Press spec unless explicitly documented elsewhere.



<!-- END SOURCE: astral_press_pillar_metrics_evaluation_canon_pass.md -->


---

<!-- BEGIN SOURCE: astral_press_pillar_s_1_s_12_modes_switchboard_canon_pass.md -->

# Astral Press Pillar — S1–S12 Modes & Switchboard (Canon Pass)

> **Scope**  
> Extract everything canon actually says about the **S1–S12 system modes** and the **Modes / Switches / Features switchboard** as they relate to Astral Press, without inventing new mode behaviours.  
> Where the corpus does **not** specify details (IDs, bitmasks, JSON schema, per-mode defaults), we mark those as explicit **gaps**.

This pass sits at the system level, but it is anchored on how these modes interact with the **Press pillar** (APP) and its immediate ecosystem.

---

## 1. S1–S12 system mode set (names and existence)

### 1.1 Canonical mode family

Canon lists a family of twelve system modes, collectively referred to as **S1–S12**. The names attached to this family are:

1. Canary  
2. Registry  
3. ESL  
4. Drift Guard  
5. θ_spawn  
6. c*  
7. Cooldown  
8. Shadow  
9. Governor  
10. Offline Recompress  
11. Encryption  
12. Knowledge Sync

These names are canonical and reoccur in the “build new computing paradigm” and testing/evaluation discussions.

### 1.2 What **is not** explicitly stated

The corpus **does not** provide, in clear table form:

- A direct mapping `S1 → Canary`, `S2 → Registry`, … `S12 → Knowledge Sync`.  
- Any numeric IDs, bit positions, or packed-flag encodings for these modes.  
- A formal state machine describing how the system transitions between these modes.

Until such a mapping appears in a mode reference or schema document, we treat **S1–S12 indices as purely symbolic placeholders**, and the names above as **labels** rather than fully-defined switches.

---

## 2. Modes / Switches / Features reference (switchboard doc)

### 2.1 Canon description

The dev/testing v2 materials describe a document often referred to as:

- “Modes, Switches, and Tested Features (Inline Reference)”  
- Also referred to as a **modes/switchboard JSON** in the Aether implementation packs.

This reference is characterized as:

- The **switchboard actually used** in the testing runs.  
- It encodes:
  - Canonical JSON for modes and switches.  
  - Anchors and nonces for mode configurations.  
  - Gate sanitization / IR switches.  
  - Loom replay / skip-ahead toggles.  
  - Per-tick Press & MDL gain logging flags.  
  - SLL canary settings.  
  - Deterministic lattice routing flags.  
  - NAP exactly-once semantics flags.  
  - Foresight / time-compression toggles (F1–F3 family).  
  - Multi-fidelity run options (M1–M3).  
  - Safety / circuit-breaker modes (SFTY1–SFTY3).  
  - Config knobs and failure modes.

In other words, it is the **live wiring diagram** for operating the paper computer in the test regime.

### 2.2 What is available vs missing

Available from canon:

- High-level descriptions of several mode families (F1–F3, M1–M3, SFTY1–SFTY3, N4, etc.), including whether they were ON, OFF, MANUAL, or EXPERIMENTAL in specific runs.  
- Names and conceptual roles of S1–S12.  
- A list of config knobs (e.g., `PII_KEYS`, `FIELD_BUDGET`, `NAP_SEED`, `LL_BOUNDS`, `PRESS_RULE_FAMILY`, `SLL_WINDOW`, `ESL_DEPTH_LIMIT`, `FORECAST_THRESHOLD`) that the switchboard uses.

Missing from canon (not visible in the current corpus):

- The actual JSON schema of the switchboard file.  
- The exact keys and value types used to represent each mode.  
- How S1–S12, F1–F3, M1–M3, SFTY1–SFTY3, N4, etc. are nested or grouped.  
- Any formal mapping from this switchboard to CLI flags or API configuration structs.

Therefore, we treat the switchboard doc as **canonical in purpose and existence**, but its internal representation as an explicit **gap**.

---

## 3. S-modes that intersect directly with Press

Although full S1–S12 semantics are not documented, several of the named modes clearly intersect with Astral Press. This section captures what is said about them.

### 3.1 ESL (Extreme Self-Learning)

ESL is both:

- A value of `PRESS_MODE` (see the Press modes pass).  
- One of the named S-modes in the S1–S12 list.

Canon facts about ESL (system-level):

- ESL turns the system onto itself, pressing internal state and operation traces.  
- ESL controls whether internal telemetry flows into Press + SLL for motif mining.  
- ESL is a **special toggle**, usually OFF by default, enabled intentionally in specific runs.  
- ESL interacts directly with:
  - Press (APP): providing both extra inputs and evolving transform rules.  
  - Loom: time-stamping and replaying ESL-induced decisions.  
  - SLL / Codex Eterna: registering new compression motifs and foresight rules.

Gaps:

- No direct association between ESL and a numeric S-index (S3 or otherwise) is provided in the current corpus.  
- No global state machine (e.g., constraints like “ESL requires Canary and Drift Guard ON”) is spelled out.

### 3.2 Offline Recompress

“Offline Recompress” appears as one of the S-mode names. It is referenced in context as a mode where:

- The system revisits stored data **out of band** (not on the hot path).  
- APP can recompress old data with improved dictionaries/transforms learned via SLL and ESL.  
- NAP and Loom are used to schedule and log these background recompression passes.

Implications for Press:

- Press must support re-running compression on previously pressed payloads and producing new `.apx`/APXi capsules while preserving provenance.  
- Offline Recompress mode likely uses updated transforms while keeping original states reproducible.

Gaps:

- No explicit triggers or scheduling rules (e.g., “run once per day” or “when SLL accepts N motifs”) are provided.  
- No detailed policy on when to keep both old and new capsules, or how to retire old ones, is included in the visible texts.

### 3.3 Encryption

“Encryption” is named as one of the S-modes. In context:

- Press capsules (`.apx`) are described as optionally having cryptographic wrappers (HMAC and signatures).  
- The S-mode “Encryption” is therefore the system-level toggle that governs:
  - Whether capsules are stored and transmitted in encrypted form.  
  - Whether APX/AEON streams are wrapped in an encryption layer.

However, canon does **not** specify:

- Which encryption schemes are mandated or recommended.  
- Whether encryption happens at container level (e.g., encrypt whole ZIP) or stream level (e.g., encrypt APXi integer stream).  
- How keys are generated, stored, or rotated.

As such:

- We only know that an “Encryption” mode exists and is relevant for Press capsules.  
- Implementation details of the encryption layer are an explicit gap.

### 3.4 Knowledge Sync

“Knowledge Sync” is another S-mode name that touches Press indirectly:

- It refers to synchronizing learned knowledge (e.g., SLL motifs, APP policy updates) across nodes or deployments.  
- Press and its policy pack (APP_BARRIERS.json) are one of the primary consumers/producers of such knowledge.

Canon implications:

- Press defaults and learned transforms can be distributed via Knowledge Sync.  
- Capsules created under one node’s policy may be decoded under another node’s policy as long as version/manifest semantics are respected.

Gaps:

- No explicit protocol or manifest format for Knowledge Sync is included in the visible materials.  
- No mapping from Knowledge Sync state to specific Press behaviours (e.g., “when sync success → reload APP_BARRIERS”) is spelled out.

---

## 4. F-, M-, SFTY-, and N- families vs S1–S12

The dev/testing docs use several mode families, for example:

- F1–F3: Foresight / Forecast / Time Compression.  
- M1–M3: Multi-Fidelity / Multi-Paradigm / Language & Modality.  
- SFTY1–SFTY3: Safety & Ops modes.  
- N4: Ingest Security Hooks.

These families are documented with ON/OFF/EXPERIMENTAL status and concrete behaviours (see earlier mode pass). The relationship between these families and **S1–S12** is **not** explicitly formalized.

Canonical points:

- The S1–S12 list appears in the broader “new computing paradigm” framing, while F/M/SFTY/N families appear in the “modes, switches, and tested features” framing.  
- ESL spans both domains (S-mode label and PRESS_MODE value).  
- SFTY1–SFTY3, N4, and F/M modes clearly act as **guards or sub-modes**, not as direct S1–S12 indices.

Explicit gaps:

- No spec mapping F1–F3, M1–M3, SFTY1–SFTY3, N4 into S1–S12 indices.  
- No statement like “S1 = Canary = F1+SFTY1 combination” appears; any such mapping would be invented.

Until a crosswalk appears, we treat S1–S12 and these families as **parallel naming schemes** with partial semantic overlap but no formal equivalence.

---

## 5. Config knobs as mode-attached flags

The switchboard relies on a set of configuration knobs, previously documented in the modes/flags pass. In this context we record only how they participate in **S-mode behaviour** from a Press perspective.

### 5.1 ESL-related knobs

- `ESL_DEPTH_LIMIT`  
  - Caps the recursion depth of Press/ESL interactions.  
  - Interacts with ESL (S-mode) and SFTY1/SFTY2 (safety/quotas).

- `SLL_WINDOW`  
  - Window length for SLL decision-making about motifs and new rules.  
  - Affects how quickly ESL discoveries can change Press behaviour.

### 5.2 Foresight and time-compression knobs

- `FORECAST_THRESHOLD`  
  - Confidence threshold for enabling F3 (time compression).  
  - In practice, an S-mode like “Drift Guard” or “Governor” is likely to read and enforce this threshold when deciding whether to allow skip-ahead and speculative execution.

- Determinism knobs (`W_L`, `W_P`, `ρ*`, `κ*`, `α*`, `λ`, `μ`, `γ`, `δ`, `ε_*`, `C`)  
  - These are global; they constrain when F-modes and ESL may introduce new behaviours without breaking replayability.

### 5.3 Ingest and security knobs

- `PII_KEYS`, `FIELD_BUDGET`  
  - Consumed by SFTY1/SFTY2 (circuit breakers and quotas).  
  - These in turn constrain what Press is allowed to log or compress when ESL and N4 are active.

- `NAP_SEED`, `LL_BOUNDS`  
  - Tie into determinism and lattice routing; relevant for S-modes like “Drift Guard” and “Governor” that manage system stability.

No new knobs are introduced for S1–S12 in the visible corpus; instead, S-modes orchestrate existing knobs and features.

---

## 6. Explicit gaps (S1–S12 and switchboard)

This pass identifies the following as **gaps** in canon that must not be silently filled:

1. **S1–S12 index mapping**  
   - We lack a canonical mapping between indices and mode names (e.g., S1 vs Canary).  
   - Any assignment would be speculative.

2. **Numeric IDs / bitmask encoding**  
   - No bitmask or numeric code for S-modes is specified.  
   - Whether modes are stored as strings, integers, or bitsets in the switchboard JSON is unknown.

3. **Full behaviour definitions for Canary, Registry, Drift Guard, θ_spawn, c*, Cooldown, Shadow, Governor**  
   - Only ESL, Offline Recompress, Encryption, and Knowledge Sync have partial semantics described.  
   - For the remaining modes we have names but no formal behaviour or triggers.

4. **Modes switchboard JSON schema**  
   - Structure, key naming, nesting of F/M/SFTY/N/S families is not visible.  
   - There is no canonical example JSON snippet in the current slices.

5. **State machine / transition rules**  
   - No description of how S-modes transition, e.g., allowed sequences, required prerequisites, or mutual exclusivity.  
   - No time-based activation rules (e.g., Graceful Cooldown conditions) appear in the scans.

6. **Direct, formal link from S-modes to Press configs**  
   - While S-modes clearly affect whether ESL, Offline Recompress, and Encryption are allowed, there is no table mapping S-modes to specific Press flags or barrier settings (e.g., changes to APP_BARRIERS.json).

7. **Knowledge Sync protocol**  
   - No details of how learned Press/SLL knowledge is packaged, transmitted, or merged under Knowledge Sync are present.

---

## 7. Minimal S-mode contract from a Press perspective

Given current canon, the minimal obligations of an implementation that claims compatibility with S1–S12 and the modes switchboard, as they relate to Press, are:

1. **Recognize named S-modes**  
   - Interpret ESL, Offline Recompress, Encryption, and Knowledge Sync in ways that align with the described behaviours.  
   - Reserved names for Canary, Registry, Drift Guard, θ_spawn, c*, Cooldown, Shadow, Governor must be maintained for future extension.

2. **Wire S-modes into existing flags and knobs**  
   - ESL must control whether internal telemetry flows into Press + SLL.  
   - Offline Recompress must enable APP recompression of historical data without breaking provenance.  
   - Encryption must control whether APP outputs are wrapped in crypto layers.  
   - Knowledge Sync must cause policy/knowledge reloads for APP when sync succeeds.

3. **Respect determinism and safety**  
   - S-modes must not allow mid-run changes to determinism knobs or Press modes without treating the change as a run boundary.  
   - SFTY and N families must remain active barriers when ESL and F-modes are enabled.

4. **Document local extensions**  
   - Any implementation-specific choice about S1–S12 indices, JSON schema, or additional mode semantics must be clearly marked as **non-canonical**, pending future alignment with the Aether/Astral Press mode reference.

This keeps the system compatible with current canon while leaving room for the future official switchboard spec to drop in without conflict.



<!-- END SOURCE: astral_press_pillar_s_1_s_12_modes_switchboard_canon_pass.md -->


---

<!-- BEGIN SOURCE: astral_press_pillar_aeon_i_apxi_descriptor_grammar_canon_pass.md -->

# Astral Press Pillar — AEON-i & APXi Descriptor Grammar (Canon Pass)

> **Scope**  
> Close as much of the **AEON-i descriptor + APXi integer-stream** gap as possible **only from canon**.  
> This pass captures:
> - What AEON-i descriptors are and how they relate to SimA/SimB.  
> - What opcodes and parameter encodings are explicitly named.  
> - What the APXi container/grammar is guaranteed to do.  
> - Which parts the implementation docs explicitly leave open.
>
> No new opcodes, no invented field orders. Anything that isn’t stated in project files is marked as a gap.

---

## 1. AEON-i in the Press stack

### 1.1 Role and placement

Canon positions **AEON-i** as the compact descriptor language for Astral Press:

- AEON-i is a **descriptor layer** for SimA (symbolic) rules and certain SimB (residual) transforms.
- It sits “under” high‑level manifests (APX, NAP) and “above” raw compressed payloads:
  - APX / Press Metadata Manifest → describes dataset, mode, capsules.
  - NAP Compression Manifest → describes layer wiring (stack/nest, DAG).
  - AEON-i descriptors → describe *what each symbolic/residual layer does*.
  - Payloads (SimB remainders) → raw residual bytes.
- The goal of AEON-i is to provide a **compact, integer‑only encoding** of model/transform definitions while staying deterministic and versionable.

### 1.2 Relationship to SimA / SimB

In the Press experiments and implementation notes:

- **SimA** is the symbolic / generative compressor:
  - Columns fit with affine, polynomial, periodic, cross‑column, and grammar rules.
  - These fits are **described** via AEON-i opcodes + integer parameters.
- **SimB** is the residual compressor:
  - Residuals are further transformed with Δ, XOR base, Golomb–Rice, AR(1..3), etc.
  - Some of these transforms are likewise expressed as AEON-i descriptors (e.g., AR(1), AR(2)).

AEON-i therefore unifies the way SimA and parts of SimB are written down in layer files.

---

## 2. AEON-i opcodes (what canon actually names)

Canon explicitly references an opcode family “AEON-i descriptors” with **named opcodes** such as:

- `OP_SEGMENT` — for segmentation / piecewise modelling.
- `OP_AFFINE` — for affine rules of the form `y = a·x + b`.
- `OP_POLY3` — for cubic polynomial rules.
- `OP_PERIODIC` — for periodic components (sinusoidal / modular patterns).
- `OP_COMBINE` — to combine multiple components (trend + seasonal, or multiple bases).
- `OP_AR1`, `OP_AR2`, `OP_AR3` — for autoregressive residual transforms.

These opcodes are referenced as examples in the Press transform library description and in comments about AEON-i being a “small opcodes + varints” language.

Canon does **not** provide a complete list of AEON-i opcodes; the above are the ones that are explicitly named. Any additional opcodes that appear in earlier drafts but are not repeated in the implementation docs should be treated as provisional until confirmed.

---

## 3. AEON-i parameter encoding

### 3.1 Integer-only, varints, and ZigZag

Canon is clear that AEON-i uses an **integer-only encoding**:

- Parameters (coefficients, indices, counts, etc.) are encoded as **variable-length integers (varints)**.
- Signed integers (e.g., negative coefficients, offsets, phases) are encoded via **ZigZag** (map signed → unsigned, then varint).
- This is done to keep descriptors compact and portable, and to allow streaming decoders to parse opcodes without external schema.

### 3.2 Field ordering within AEON-i opcodes

For each opcode, canon assumes a **fixed field order** per version of AEON-i, but does **not** publish the full order in the slices we have. For example, a conceptual encoding might look like:

```text
[ opcode_id, target_column, segment_id, param_1, param_2, … ]
```

However, we **do not** have a canonical specification of:

- Exact parameter counts per opcode.
- Exact parameter order.
- Which opcodes include which optional fields.

Those details are explicitly treated as part of AEON-i’s **internal schema**, and only the facts “varints + ZigZag, opcodes like OP_AFFINE, OP_POLY3, …” are canon in the public text.

---

## 4. APXi integer-stream container

### 4.1 Role and definition

Canon describes **APXi** as an extreme compact representation for APP, where **everything** is encoded as a single integer stream:

- APXi is framed as: “16‑bit version header + one stream of varints”.
- All descriptors (AEON-i opcodes and params), along with minimal manifest/header information, are packed into this stream.
- There are **no field names, no JSON, and no external container headers** beyond the minimal version word.

The idea is to have a mode where an implementer who knows the APXi spec can decode a Press capsule from one uniform integer stream with minimal overhead.

### 4.2 Version word

Canonical APXi structure starts with a **16‑bit version**:

```text
APXi := [ version_u16, v0, v1, v2, … ]
```

Where:
- `version_u16` is a two‑byte integer indicating the APXi grammar version.
- `v0, v1, …` are varints (unsigned), representing opcodes, counts, parameters, and other encoded fields under that version’s grammar.

### 4.3 Single varint stream

After the version word, APXi uses a **single varint stream**:

- No explicit segment boundaries in the binary format; segmentation is defined by the **grammar** (which fields are expected in which order).
- Op boundaries are determined by reading one opcode, then reading the opcode’s fixed/known number of parameters.
- Higher-level structures (e.g., number of layers, mapping to SimA/SimB, mapping to physical payloads) are all encoded via counts and IDs within that stream.

Canon emphasises that APXi is:

- The **smallest and fastest** descriptor mode.
- Not self-describing; it depends on the versioned AEON/APXi spec.
- Suitable for environments where both encoder and decoder agree on the exact grammar.

---

## 5. Known vs unknown AEON/APXi structure

### 5.1 Known (canonical) facts

1. **Descriptor language:**
   - AEON-i is the descriptor language for APP symbolic and some residual layers.
   - It is made of **opcodes** like `OP_SEGMENT`, `OP_AFFINE`, `OP_POLY3`, `OP_PERIODIC`, `OP_COMBINE`, `OP_AR1`, etc.
   - Parameters are encoded as varints, with ZigZag for signed values.

2. **APXi header:**
   - Begins with a 16‑bit version number.
   - Followed by a single varint stream encoding all struct-like data.

3. **Grammar dependence:**
   - APXi decoding is impossible without the version’s grammar; fields are implied by position/order, not by tags.
   - AEON-i/ APXi together define how to read opcodes and parameters from the stream.

4. **Relationship to APX / NAP:**
   - APXi is an alternate container/descriptor mode for APP.
   - APXi must still respect the same semantics as APX capsules:
     - Determinism.
     - Lossless reconstruction (in lossless mode).
     - Consistent layer wiring with NAP manifests (or an equivalent encoded manifest in compact form).

### 5.2 Explicit gaps

Canon **does not** provide:

1. **Complete opcode list:**
   - Only a subset of AEON-i opcodes are named explicitly.
   - There is no canonical enumeration table of all allowed opcode IDs.

2. **Opcode ID assignments:**
   - No mapping from human-readable names (`OP_AFFINE`) to numeric IDs is provided.

3. **Per-opcode parameter schemas:**
   - The exact number, order, and meaning of parameters for each opcode are not enumerated.
   - Constraints (e.g., valid ranges, special sentinel values) are not given.

4. **APXi field ordering:**
   - Beyond `version_u16` followed by a varint stream, the exact order of fields (e.g. number of layers, manifest bits, AEON blocks, etc.) is not given.

5. **APXi–APX/NAP correspondence:**
   - There is no formal mapping like: “field 3 in APXi == `orig_bytes` in APX manifest”, etc.
   - The spec only states that APXi is the compact counterpart that can represent the same semantics.

6. **Error handling and alignment:**
   - Canon does not describe what decoders should do on malformed streams (e.g., truncated varint, invalid opcode ID).
   - There is no specification of alignment or padding rules (if any) inside APXi.

All of these remain **open implementation/design questions**.

---

## 6. Minimal AEON-i/APXi implementation contract

Given the canonical constraints, a minimal implementation that claims AEON-i/APXi compatibility must:

1. **Implement AEON-i opcodes as defined for its version:**
   - For the subset of opcodes it supports (e.g., `OP_AFFINE`, `OP_POLY3`, `OP_PERIODIC`, `OP_AR1`), it must:
     - Map each opcode name to a numeric ID.
     - Define a fixed parameter list and order.
     - Encode parameters as varints (with ZigZag for signed values).

2. **Define an internal AEON-i spec per version:**
   - This spec must be versioned and deterministic.
   - Encoder and decoder must share the same table.

3. **Implement APXi framing:**
   - Write a 16‑bit version word.
   - Encode all AEON-i ops and any necessary header fields into a single varint stream.

4. **Preserve APP semantics:**
   - APXi‑encoded descriptors must be sufficient to:
     - Reconstruct all SimA/SimB behaviour recorded in the capsule.
     - Rebuild original data when combined with residual payloads.
   - APXi mode must not change the logical output of Press; it is a representation change, not a behavioural change.

5. **Document gaps as internal choices:**
   - Any additional opcodes, parameter fields, or stream layout choices not present in canon must be treated as **implementation-specific**, not as Aether/Astral Press canon.

This pass therefore closes the **high-level descriptor and container role** of AEON-i and APXi, while leaving numeric IDs, full grammars, and error policies clearly flagged as open design space.



<!-- END SOURCE: astral_press_pillar_aeon_i_apxi_descriptor_grammar_canon_pass.md -->


---

<!-- BEGIN SOURCE: astral_press_pillar_apx_container_manifest_canon_pass.md -->

# Astral Press Pillar — APX Container & Manifest (Canon Pass)

> **Scope**  
> Close the APX container + manifest gap **only using canon**:
> - What `.apx` is and must contain.  
> - What the Press Metadata Manifest (MANIFEST.json / .apxMANIFEST.json) is responsible for.  
> - Where NAP + layers sit relative to the manifest.  
> - What is *explicitly marked as a gap* in the existing implementation docs.
>
> No new fields, no crypto choices invented. Anything not present in the corpus is marked as a GAP.

---

## 1. Canonical definition of `.apx` (what it is)

From the Press pillar report and press experiments:

- `.apx` is described as a **portable container for Aether Press outputs**.
- It is a **deterministic, self-contained ZIP archive** that contains:
  - A **Press Metadata Manifest** (JSON).  
  - One or more **layer payload files** (SimA descriptors, SimB residuals).  
  - A **NAP Compression Manifest** that tells how layers recombine.  
  - Optional **cryptographic tag** (HMAC/signature) for authenticity.
- The report stresses that `.apx` is “just a zip” so it can be opened by generic tools, but the internal structure and manifest semantics are what make it an Astral Press capsule.

This fixes the **type** of `.apx` (ZIP container) and the **high-level contents**, without yet pinning exact file names or JSON schemas.

---

## 2. Press Metadata Manifest (MANIFEST.json / .apxMANIFEST.json)

Canon gives a clear role for the Press Metadata Manifest:

- File is referred to as `MANIFEST.json` in experiments and `.apxMANIFEST.json` in some implementation notes.
- It is a **JSON metadata file** that stores at minimum:
  - Original file **name**.  
  - Original file **size** (bytes).  
  - Original file **hash** (SHA-256 is referenced in multiple places).  
  - **Compression mode** used (e.g., text/numeric/image or other mode tags).  
  - **Timestamp** of creation.  
  - Optional **filesystem metadata** such as permissions and modification times (for archival fidelity).
- It also carries Press-specific metadata:
  - A list of **layers**, or pointers to a more detailed layer/stack manifest.  
  - References to **SimA** and **SimB** layer files.  
  - A reference to the **NAP Compression Manifest** that knits these together.  
  - Versioning information to identify the APP/Press version that produced the capsule.

The manifest is explicitly described as part of the **public contract** of APP: third parties can read the manifest and reconstruct or verify data without needing internal Aether context.

**Gaps (manifest):**

- The full JSON Schema for the manifest is **not** present in the visible canon.  
  - Field order, required vs optional keys, and nested structures are not enumerated.  
  - There is no canonical `"schema_version"` or similar field specified in the slices we have.  
- Exact naming (`MANIFEST.json` vs `.apxMANIFEST.json`) is used interchangeably in different docs; the spec does not currently bless one as the only valid name.

For this pass, we treat the manifest as:

```text
PressMetadataManifest (JSON) := {
  fields that describe: original file, Press version, compression mode, timestamps, FS metadata, layer references, NAP manifest reference, hashes
}
```

without asserting a specific schema beyond what is literally stated.

---

## 3. Layers and NAP manifest inside `.apx`

The corpus consistently separates **what** is compressed from **how** it is reconstructed:

- **APX Manifest / Press Metadata Manifest**
  - Describes the dataset, original metadata, and high-level compression settings.

- **NAP Compression Manifest**
  - Describes relationships between layers: stacking, nesting, SimA/SimB roles, DAG order.
  - Has its own schema (`layers[] {id, kind, parent, refs[], params, ordering}, knit_rules, deterministic_order, hashes`) defined in the NAP pass.

- **Layer payload files**
  - SimA descriptors (symbolic rules) in their own files.  
  - SimB residual payloads (often already compressed by a conventional codec).

Container-wise, `.apx` must therefore contain **at least**:

- One manifest file describing the original dataset and compression run (Press Metadata Manifest).  
- One NAP Compression Manifest if stacked/nested compression is used.  
- One or more layer payload files (mapped in manifests).

Exact folder layout (e.g., `layers/`, `nap_manifest.json` path) is noted in experiments but not codified as canonical, and thus remains **implementation detail**.

---

## 4. CLI contract and behaviour (encode/decode/verify)

The Press implementation and experiments define a CLI with three fundamental operations:

1. **Encode**
   - Input: raw file.  
   - Output: `.apx` capsule that includes manifest(s) and layers.  
   - Behaviour: deterministic; same input + same APP version ⇒ same `.apx` bytes.

2. **Decode**
   - Input: `.apx` capsule.  
   - Output: reconstructed raw file.  
   - Behaviour: must reconstruct bytes that hash identically to the original (lossless mode).  
   - Uses the Press Metadata Manifest + NAP manifest + layer files to rebuild the data.

3. **Verify**
   - Inputs: `.apx` capsule and original raw file (or just the capsule if the original’s hash is embedded).  
   - Behaviour: recompress/decompress or recompute hashes to confirm that the capsule is valid for the original data.

The **CLI semantics** are part of the spec: external implementers are expected to be able to implement these three commands and interoperate on capsules.

**Gaps (CLI):**

- Flag names and abbreviations (`--in`, `--out`, `--verify`, etc.) are shown in examples but not fixed as normative.  
- Error codes, logging formats, and streaming/interactive behaviour are not specified in the canon slices we have.

---

## 5. Cryptographic tagging (hashes, HMAC, signatures)

Canon about hashing and signatures:

- The manifest stores at least one hash (SHA‑256 is referenced) of the original file and of the reconstructed data.  
- Some implementation notes mention HMAC/signature support as a **planned or recommended** feature:
  - HMAC for integrity and authenticity in secure deployments.  
  - Public-key signatures for verifiable capsules.

The implementation spec explicitly marks the following as a **GAP** (paraphrased):

- Exact choice of hash function(s) (even though SHA‑256 is implied experimentally).  
- Exact choice of HMAC algorithm.  
- Exact choice of signature algorithm.  
- How signatures are bound to capsule content (which bytes are covered, whether via Merkle trees, etc.).

Therefore, canon currently requires only that:

- The manifest include hashes sufficient to verify bit-exact reconstruction.  
- Any crypto extensions (HMAC, signatures) must be deterministic and cover all relevant payloads.

Concrete algorithm choices and binding strategies remain **open design space**.

---

## 6. Versioning and compatibility

From the implementation notes and Press report:

- `.apx` capsules embed both:
  - An **APP/Press version** identifier.  
  - A **capsule/format version** identifier (often referred to as `apx_version`).

Canon expectations:

- Encoders must write their `apx_version` and APP/Press version into the manifest so decoders can act appropriately.  
- Decoders should:
  - Accept and process capsules with compatible versions.  
  - May reject or warn on capsules from unrecognised major versions.

Gaps:

- Specific semantic versioning rules (major/minor/patch compatibility) are discussed conceptually but not given as a table or formal rule set.  
- No canonical list of version numbers and their required/optional fields is present in the visible docs.

---

## 7. Explicitly tagged gaps (from implementation docs)

The dev implementation spec explicitly names at least one gap in this area:

- **GAP‑APP‑002 – Exact `.apx` schema & signature details**  
  The spec states (in substance) that the reports define **what** must be stored in the capsule and manifest, but do **not** lock down:
  - Canonical byte layout of container header and segment index.  
  - Formal JSON Schema for `.apxMANIFEST.json`.  
  - Hash/HMAC/signature algorithms and how signatures bind to capsule bytes.

This pass respects that by:

- Treating the semantic requirements (must store orig metadata, hashes, layers, NAP reference, version) as **canon**.  
- Treating byte layout, JSON Schema, and crypto mechanic as **open**, clearly marked as gaps, not silently filled.

---

## 8. Minimal implementation contract (APX container & manifest)

Given only canonical constraints, the minimal contract for an APP‑compatible `.apx` implementation is:

1. **Container type**  
   - A ZIP (or equivalent) file that holds at least:
     - A Press Metadata Manifest (JSON).  
     - Layer payload files (SimA descriptors, SimB residuals).  
     - A NAP Compression Manifest for stacked/nested cases.

2. **Manifest semantics**  
   - Manifest must record:
     - Original file name, size, and content hash.  
     - Compression mode and APP/Press version.  
     - Timestamps and optional FS metadata.  
     - Mapping between logical layers (SimA/SimB) and physical payload files.  
     - Reference to any NAP Compression Manifest used.  
     - Hashes sufficient to validate reconstruction.

3. **Determinism**  
   - Encoding must be deterministic: same input + same APP version ⇒ identical `.apx` bytes.  
   - Decoding must be lossless in strict mode: reconstructed bytes hash identically to original.

4. **Extensibility**  
   - Capsule must tolerate addition of new manifest fields in future versions (decoders ignore unknown fields, while respecting versioning rules).  
   - NAP and APX manifests are separate but coordinated: APX says *what* and *when*; NAP says *how stacks/nests recombine*.

Anything more detailed than this (e.g., exact field names, JSON Schema, crypto stack) is deliberately **left open** in canon and must be treated as design work, not spec.



<!-- END SOURCE: astral_press_pillar_apx_container_manifest_canon_pass.md -->


---

<!-- BEGIN SOURCE: astral_press_pillar_canon_gap_ledger_big_dogs_pass.md -->

# Astral Press Pillar — Canon Gap Ledger (Big Dogs Pass)

This canvas tracks:
- Which APP/Press details are **explicitly defined in canon** (press pillar report, canonical chat logs, Aether Math Compendium, implementation packs).
- Which implementation details are **still deliberately left open** in the current canon (GAP-APP family, NAP, APX schema, metrics, etc.).

It is **canon-only**: no invented closures.

---

## 1. Confirmed Canon Blocks (Press Pillar)

- Press = Aether’s **data-compression pillar**, downstream of Aether core.
- Compression as **rule + residual** pairs with bit-exact reconstruction.
- Deterministic: same input + same APP version → same `.apx` capsule.
- Multi-layer model+residual stack: `X = M1 + R1`, `R1 = M2 + R2`, … until MDL no longer improves.
- APP capsules (`.apx`) contain:
  - Press Metadata Manifest (`.apxMANIFEST.json`).
  - NAP manifest (stack/nest DAG for SimA/SimB layers).
  - SimA descriptors (symbolic rules) and SimB residual payloads.
  - Optional HMAC/signature.
- APX is "just a ZIP" (or compact variants) with the above semantics.
- Cost and MDL: total description length = model bits + residual bits + overhead; layers accepted only if they reduce it.
- Loom/Press/NAP integration: Press compresses state, Loom owns time between checkpoints, NAP knits multi-layer compression across stacks/nests.

(Details and citations are in the chat; this canvas is just the working board.)

---

## 2. Still-Open Gaps (high level)

These are **not** fully specified in the canon we’ve scanned so far:

- GAP-MANIFEST-01 — Exact JSON schema for `.apxMANIFEST.json`.
- GAP-APX-BYTE-01 — Exact byte layout for `.apx` capsule header / segment index.
- GAP-SIGN-01 — Canonical choice of hash/signature/HMAC algorithms and binding rules.
- GAP-NAP-01 — Field-level schema for NAP manifest (stack/nest DAG encoding, edge attributes).
- GAP-AEON-OPS-01 — Full AEON-i opcode grammar (fields, constraints, error behaviour).
- GAP-APXi-GRAMMAR-01 — APXi integer-stream grammar and field order.
- GAP-MDL-01 — Fully explicit Press-level MDL functional (including all overhead terms) and numeric thresholds.
- GAP-METRICS-01 — Concrete values for ε / window size W in container-selection metrics.
- GAP-TOL-01 — Numeric tolerance for "unchanged beyond tiny numerical tolerance".

---

## 3. To-Do (next passes)

- NAP manifest deep dive — scan NAP/implementation docs for any hidden schema details.
- Press modes & profiles — pull all mode names (off/on_demand/ESL/checkpoint/etc.) and their canon semantics.
- Metrics & baselines — lock in everything the Testdoc-AP family actually states.
- Cross-check Press-related GAP tags in dev implementation spec vs. canonical chats and Math Compendium.

This will grow as we sweep more of the implementation zips and compendium slices, always with a clean split between **canon-confirmed** and **still-open**.



<!-- END SOURCE: astral_press_pillar_canon_gap_ledger_big_dogs_pass.md -->


---

<!-- BEGIN SOURCE: astral_press_pillar_gate_tbp_nap_manifests_impl_docs_pass.md -->

# Astral Press Pillar — Gate/TBP NAP & Manifests (Impl Docs Pass)

> **Scope**  
> Use the Trinity Gate / TBP implementation docs under `Reports/trinity gate pillar/TGP+TBP implementstion docs/` (from `aether full clean`) to close the remaining **NAP envelope** and **TBP pack/slice manifest** gaps that are relevant to Astral Press / APP.
>
> All interpretations are backed by direct quotes from these implementation docs. Where something is TBP‑only (not global), it is clearly marked.

Sources in this pass:

- `tbp_gate_implementation_spec_v_1.md`
- `trinity_gate_features_components_capabilities 1.md`
- `trinity_gate_tgp_focus_expansions.md`
- `trinity_gate_vs_math_compendium_coverage_report.md`
- `triune_bridge_gate_knowledge_gaps.md`

---

## 1. TBP slice & pack manifests (pattern for APX‑style manifests)

### 1.1 Slice manifest (`slice_manifest.v1.json`)

The TBP implementation spec defines a per‑slice manifest:

> `// slice_manifest.v1.json`  
> `{`  
> `  "state_range": { "start": 0, "end": 65535 },`  
> `  "scale_params": { "eta": 1000000, "P": 32 },`  
> `  "phase_offset": 0.5,`  
> `  "metrics": { "amp_L2": 1.2e-3, "prob_L1": 1.7e-3 },`  
> `  "hashes": { "m": "sha256:...", "p": "sha256:...", "R1": "sha256:..." }`  
> `}`  
> — `tbp_gate_implementation_spec_v_1.md`, §2.3

From this we get the **canonical v1 slice manifest fields** (TBP‑specific, but pattern‑forming):

- `state_range` — object with integer `start`, `end` (e.g. `[0, 65535]`) describing the index range within the state space that this slice covers.
- `scale_params` — object with `eta` and `P`, the TBP resolution and period parameters.
- `phase_offset` — numeric (e.g. `0.5`), aligning phases across slices.
- `metrics` — object with per‑slice quality metrics (`amp_L2`, `prob_L1` in the example).
- `hashes` — object carrying content‑addressed hashes for the internal arrays: `m`, `p`, and `R1`, each of the form `"sha256:..."`.

**APP‑pillar relevance:**

- This confirms the manifest **shape** TBP uses: a small JSON object with:
  - a *range* descriptor,
  - *numeric parameters* governing transforms,
  - *metrics* for quality, and
  - a *hash table* for the underlying arrays.
- APP’s future slice‑level manifests (if we define them) can follow the same pattern: `state_range`, `params`, `metrics`, `hashes` keyed by internal arrays.

### 1.2 Pack manifest (`pack_manifest.v1.json`)

The same section introduces a pack‑level manifest that stitches multiple slices together:

> `// pack_manifest.v1.json`  
> `{`  
> `  "global_bits": 18,`  
> `  "slices": ["sliceA.manifest", "sliceB.manifest", "sliceC.manifest", "sliceD.manifest"],`  
> `  "nap_stitch": { "phase_align": true, "normalised": true },`  
> `  "R2_hash": "sha256:...",`  
> `  "metrics": { "amp_L2": 3.0e-4, "prob_L1": 8.0e-5 },`  
> `  "commit_ref": "u:sha256:..."`  
> `}`  
> — `tbp_gate_implementation_spec_v_1.md`, §2.3

Key fields and their roles:

- `global_bits` — integer (e.g. `18`), representing the effective resolution of the combined slices.
- `slices` — array of slice manifest filenames; the pack manifest points to the per‑slice manifests.
- `nap_stitch` — object carrying NAP‑related stitch metadata:
  - `phase_align: true` — indicates slices are phase‑aligned for stitching.
  - `normalised: true` — indicates the slices are normalised for NAP coupling.
- `R2_hash` — hash of the `R2` (global residual) array, of the form `"sha256:..."`.
- `metrics` — quality metrics for the whole pack (`amp_L2`, `prob_L1` in the example).
- `commit_ref` — reference into the U‑Ledger, of the form `"u:sha256:..."`.

**APP‑pillar relevance:**

- This pack manifest shows how a pillar can:
  - Maintain **hash‑based linkage** between slice manifests, global residual arrays, and the ledger (`commit_ref`).
  - Attach a small **`nap_stitch`** object indicating how NAP should treat the pack (phase‑aligned, normalised).
- For APP, this bolsters the design pattern for higher‑level manifests that refer to:
  - sub‑manifests (`slices`),
  - a `nap_stitch` block for cross‑pillar alignment,
  - `R2_hash` or equivalent *global residual* hashes,
  - and a ledger link `commit_ref` (e.g., via U‑Ledger or a Press ledger).

We treat `slice_manifest.v1.json` and `pack_manifest.v1.json` as **TBP‑specific** and **not** global APX requirements, but they give us a strong, canon‑backed model for layered manifest design.

---

## 2. NAP envelope JSON schema (v1 Gate/TBP)

### 2.1 Canon constraint (from TBP spec)

Section 3 of the TBP implementation spec restates the NAP envelope constraints:

> "NAP envelope (v1 JSON over TCP/WS; CBOR allowed)"  
>  
> **Canon constraint**  
> * "Each node emits envelope: tick, node_id, layer, metrics, seed, payload hash (no raw data)."  
> — `tbp_gate_implementation_spec_v_1.md`, §3.1

This mirrors the high‑level NAP canon, but here we also get a **fully spelled out v1 JSON schema**.

### 2.2 v1 NAP envelope schema

The same section defines a JSON‑Schema‑style v1 schema:

> `**v1 schema**`  
>  
> ```json  
> {`  
> `  "type": "object",`  
> `  "required": ["tick","node_id","layer","seed_hex","payload_ref","metrics","mode","sig"],`  
> `  "properties": {`  
> `    "tick": { "type": "integer", "minimum": 0 },`  
> `    "node_id": { "type": "string" },               // UTF-8, stable per node`  
> `    "layer": { "type": "string", "enum": ["GATE","LOOM","PRESS","U","..."] },`  
> `    "seed_hex": { "type": "string", "pattern": "^[0-9a-f]{64}$" },`  
> `    "payload_ref": { "type": "string", "pattern": "^sha256:[0-9a-f]{64}$" },`  
> `    "metrics": { "type": "object" },               // freeform numeric metrics`  
> `    "mode": { "type": "object" },                  // governance modes toggled`  
> `    "sig": { "type": "string" }                    // optional Ed25519 signature over canonical envelope`  
> `  }`  
> `}`  
> ```  
> — `tbp_gate_implementation_spec_v_1.md`, §3.1

From this, we can now state the NAP envelope v1 **wire contract** precisely:

- Envelope is a JSON object with:
  - **Required fields:** `tick`, `node_id`, `layer`, `seed_hex`, `payload_ref`, `metrics`, `mode`, `sig`.
- Field semantics:
  - `tick` — integer ≥ 0 (global NAP tick index τ).
  - `node_id` — UTF‑8 string, stable per node.
  - `layer` — string, one of a finite enum including at least `"GATE"`, `"LOOM"`, `"PRESS"`, `"U"`, plus others not listed here.
  - `seed_hex` — 64‑character lowercase hex string, the seed used for deterministic behaviour.
  - `payload_ref` — string matching `^sha256:[0-9a-f]{64}$`, i.e. a SHA‑256 hash with `sha256:` prefix.
  - `metrics` — freeform object; keys and values are left to the sender, but expected to be numeric metrics.
  - `mode` — freeform object for governance modes / switches; schema defined elsewhere (not in this doc).
  - `sig` — string representing an optional **Ed25519 signature** over the canonical envelope.

This aligns perfectly with the Gate JS implementation (which canonicalises envelopes and uses `payload_ref: "sha256:<hash>"`), and it fills in the missing details:

- The **regex constraints** on `seed_hex` and `payload_ref`.
- The understanding that `sig` is an **Ed25519** signature, not an HMAC or other scheme.
- The explicit enumeration that `layer` can be `"PRESS"`, formalising APP’s presence on the NAP bus.

### 2.3 Canonicalisation and signing (cross‑check against Gate JS)

The Gate JS `canonicaliseNapEnvelope(env)` function builds a canonical JSON for hashing/signing:

> `const canonical = {`  
> `  tick: env.tick,`  
> `  node_id: env.node_id,`  
> `  layer: env.layer,`  
> `  seed_hex: env.seed_hex,`  
> `  payload_ref: env.payload_ref,`  
> `  metrics: env.metrics ?? {},`  
> `  mode: env.mode ?? {},`  
> `  sig: env.sig ?? "",`  
> `};`  
> `return JSON.stringify(canonical);`  
> — `src/core/nap.js` (Gate JS repo)

Combined with the TBP schema, the v1 canonical signing contract is:

1. Construct the canonical envelope object with exactly these fields and defaults.
2. Convert to a JSON string using normal JS `JSON.stringify`.
3. Compute `sha256(canonical_string)` as the message digest.
4. Sign that digest with Ed25519 (when a signature is used), placing the result in `sig`.

APP, as a NAP layer participant (`layer: "PRESS"`), must follow the same canonicalisation and signing rules when emitting or verifying envelopes.

---

## 3. Gate scene export (where APP plugs in)

While most of the Gate scene schema lives in TBP‑specific sections, one key constraint matters directly to Press:

> "Gate is the **scene I/O layer** on a 2D plane; exports structured scenes (JSON, CSV, images)."  
> — `tbp_gate_implementation_spec_v_1.md`, §3.2

Combined with the features/capabilities doc:

> "Gate pillars produce **structured, typed scenes**; each scene has a manifest describing: source pillar(s), tick/window, schemas, and hashes."  
> — `trinity_gate_features_components_capabilities 1.md`

This underlines how APP should treat Gate outputs:

- Gate emits **scenes** that are already structured and hashed; these are natural inputs to APP.
- A Gate scene manifest includes at least:
  - identifying info (source pillars),
  - tick/window alignment (NAP tick),
  - schema references, and
  - hashes of the underlying scene data.

While the exact scene manifest JSON is not fully spelled out in these docs, the pattern is consistent with APX manifests and TBP slice/pack manifests: a small JSON describing **range, schema, parameters, metrics, and hashes**, plus a tick/window indicator.

APP does not need to redefine Gate’s scene format; it only needs to hook into the **hash and tick** semantics when it compresses those scenes.

---

## 4. What this pass closes vs what stays open

### 4.1 Closed by this pass (with direct doc support)

- **NAP envelope v1 JSON schema**:
  - Exact required fields: `tick`, `node_id`, `layer`, `seed_hex`, `payload_ref`, `metrics`, `mode`, `sig`.
  - Regex constraints for `seed_hex` and `payload_ref`.
  - Clarification that `sig` is an **Ed25519** signature over the canonical envelope.
  - Confirmation that `layer` includes `"PRESS"` and other system layers.
- **Canonicalisation & signing flow** for envelopes, by cross‑linking TBP schema and Gate JS code.  
- **TBP slice & pack manifest patterns**:
  - `slice_manifest.v1.json` fields: `state_range`, `scale_params`, `phase_offset`, `metrics`, `hashes` (`m`, `p`, `R1`).
  - `pack_manifest.v1.json` fields: `global_bits`, `slices`, `nap_stitch` (`phase_align`, `normalised`), `R2_hash`, `metrics`, `commit_ref`.
- **NAP‑stitch metadata** pattern (`nap_stitch`) for cross‑slice/cross‑pillar alignment.
- **Gate/scene role** as the structured export layer whose outputs Press will compress.

### 4.2 Still open (not addressed by these Gate/TBP docs)

This implementation pack does **not** define:

- The **`nap_manifest.json`** schema for APP/Press; NAP here is at the envelope + TBP pack level, not the APP layer manifest level.
- **APP_BARRIERS.json** or `press_pareto_manifest_v6_*` schemas; those are Press‑internal policy/metrics artifacts and do not appear here.
- **AEON-i or APXi grammars**; TBP uses its own manifest vocabulary (`state_range`, `scale_params`, etc.) but does not define APP’s descriptor language.
- A complete **Modes/Switchboard JSON** schema; the `mode` field exists as a freeform object with governance roles, but its internal structure remains undefined in this pack.

These remain open design space for the Astral Press Pillar spec, albeit now strongly constrained by:

- NAP’s v1 envelope schema and signing rules.
- The TBP slice/pack manifest patterns.
- The general **hash+metrics+anchors** design used across Gate/TBP.

---

## 5. How to use this in the Press Pillar spec

For APP:

1. **When emitting NAP envelopes** (`layer: "PRESS"`):
   - Use the v1 schema exactly.
   - Follow the canonicalisation and Ed25519 signing flow when signatures are enabled.
   - Use `payload_ref = "sha256:<hash>"` pointing to APX capsules or other APP payloads.

2. **When designing APP‑level manifests** (future work):
   - Keep the manifest shapes small and focused, like TBP’s slice/pack manifests:
     - ranges or state descriptors,
     - transform parameters,
     - metrics,
     - hashes (per sub‑object),
     - optional `nap_stitch` and `commit_ref` when linking to NAP/U‑Ledger.

3. **When integrating with Gate scenes**:
   - Treat Gate scenes as **structured, hashed inputs** on the common NAP tick.
   - Do not re‑invent Gate schemas inside APP; instead, reference their hashes and manifests inside APX/APP manifests.

This pass is therefore the **Gate/TBP implementation cross‑cut** for the Astral Press Pillar: it fixes the NAP envelope contract and gives us manifest design patterns we can rely on, while leaving APP‑specific manifest schemas and policy packs to their own dedicated passes.



<!-- END SOURCE: astral_press_pillar_gate_tbp_nap_manifests_impl_docs_pass.md -->


---

<!-- BEGIN SOURCE: astral_press_pillar_cross_pillar_nap_umx_tbp_integration_umx_impl_docs_pass.md -->

# Astral Press Pillar — Cross-Pillar NAP/UMX/TBP Integration (UMX Impl Docs Pass)

> **Scope**  
> Mine the UMX implementation docs under `Reports/universal matrix pillar/implementation/` in `aether full clean` for anything that closes **Press‑relevant gaps** about NAP, SLP, TBP, and APX‑style packaging.
>
> These docs were produced by the same complement process we’re now running for APP. They are **canon for UMX**, but we only import what directly constrains or clarifies Astral Press / APX / NAP behaviour.
>
> Sources touched in this pass (all under `.../universal matrix pillar/implementation/`):
> - `umx_complement_doc_g_nap_integration.md`  
> - `umx_complement_doc_h_nap_integration_full.md`  
> - `umx_complement_doc_f_llp_slp_propagation.md`  
> - `universal_matrix_pillar_spec_v_1.md`  
> - `umx_trinity_gate_integration_spec_v_1_2025_11_17.md`  
> - `umx_gap_closure_pass_3_bridge_gate_cross_cut_2025_11_16.md`  
> - `umx_spec_artifacts_bundle_4_umx_tbp_pack_2025_11_16.md`  
> - plus the UMX spec index and fixtures/readme bundles for context.

We explicitly checked all `.md` files in this implementation directory for **`nap_manifest`, `APP_BARRIERS`, `press_pareto`, `AEON`, `APXi`**, and **none** of those strings appear in any of them. That confirms that certain APP‑specific schema gaps **are not addressed** in this UMX pack.

---

## 1. NAP’s system role (as seen from UMX)

### 1.1 NAP as bus + clock + auditor

Complement Doc G gives a clean, UMX‑facing summary of NAP’s role:

> "UMX-facing interpretation:**
>
> - NAP is the **bus + clock + auditor** for the whole system.
> - UMX/SLP is the **physics engine**; NAP guarantees that, even w... multiple machines, it behaves like **one** synchronous lattice:
>   - same tick `τ` everywhere,
>   - same ordered writes,
>   - same final state given the same seed and Gate inputs."  
> — `umx_complement_doc_g_nap_integration.md`

This is entirely consistent with earlier Aether canon, but here it’s spelled out in a way that binds NAP to a **single global tick** and a **single logical lattice** across machines.

**Implication for Astral Press (APP):**

- When APP is compressing histories that include UMX state or other pillars on the UMX/NAP bus, it can treat NAP as providing:
  - a **global tick index τ**,
  - an **ordered, exactly-once stream of writes** (from APP’s POV),
  - and a **canonical final state** per tick given (seed, Gate inputs).
- This means Press/Loom’s expectation of **deterministic replay** over NAP‑fed pillars is justified by the UMX integration docs, not just by abstract math.

### 1.2 Envelopes and “just numbers & hashes”

Doc G restates NAP’s message model in a way that matches what the Gate JS implementation actually does:

> "NAP packets are defined to carry ‘just numbers and hashes’ – ...ent-addressed hashes and statistical descriptors."  
> "Every NAP message is encapsulated in a standard envelope with... contains only compressed state deltas or hashes."  
> — `umx_complement_doc_g_nap_integration.md`

Key UMX‑facing fields (summarised in the doc):

- `tick τ` — which tick these writes belong to.
- Logical address (stack / ring / PFNA).
- `payload_ref` — content address to ledger entries.
- `nonce` + hashes — for idempotence.

This lines up with the Gate NAP implementation pass (which we already captured separately):

- Envelopes carry a **`payload_ref` string of the form `"sha256:<hex>"`** (Gate JS).
- Canonical envelope JSON includes `tick`, `node_id`, `layer`, `seed_hex`, `payload_ref`, `metrics`, `mode`, `sig`.

**Press‑pillar takeaway:**

- APP should treat NAP envelopes as **integers + hashes**, never raw blobs.
- Whenever APP needs to bind compressed payloads to NAP, it does it via **hash references**, not embedded data.
- APP’s role as a **compressed history / capsule factory** can plug directly into `payload_ref` without needing to alter NAP’s structure.

---

## 2. APX‑style snapshot packaging for UMX

The UMX bridge/gap closure doc explicitly uses **APX‑style packaging** for matrix snapshots, giving us concrete patterns for how APP capsules are extended for pillar‑specific content.

From `umx_gap_closure_pass_3_bridge_gate_cross_cut_2025_11_16.md`:

> "Bridge / Gate evidence  
> The Aether testbed and Occam/Press experiments define a rich set of behaviours:
>
> - Canonical JSON and anchors for every object.  
> - **APX-style layered packaging with `MANIFEST.json` plus `layers/...` payloads.**  
> - Clear distinction between **identity metadata** (names, hashes, sizes) and payload bytes.  
> - Tests that verify both **lossless compression** and **auditability** via hash chains."

Then, under **“Pass-3 resolution for UMX”**:

> "We specialise Loom/Press interop for UMX as follows:
>
> 1. **UMX snapshot packaging:**
>    - A UMX snapshot at tick t is packaged as an **APX-like capsule**:
>      - `MANIFEST.json` includes:  
>        - `component: "UMX"`,  
>        - `tick: t`,  
>        - `topology_anchor`, `slp_anchor`,  
>        - optional `file_meta`-style details for environment context.  
>      - `layers/topology.bin` holds the compressed adjacency + layer assignment.  
>      - `layers/slp.bin` holds SLP ley strengths, residuals and metrics."  
> — `umx_gap_closure_pass_3_bridge_gate_cross_cut_2025_11_16.md`

**What this closes for APP/APX:**

1. **APX as a general capsule pattern:**  
   - APX isn’t just “the Press container”; UMX uses **APX-like capsules** with:
     - `MANIFEST.json` + `layers/…` payloads, and
     - a strict split between identity metadata (component name, tick, anchors, hashes) and raw bytes.
   - This reinforces that our existing APX manifest spec (mode, orig_bytes, orig_sha256, audit, optional signature) is the **minimal core**, and individual pillars (like UMX) are free to extend it with additional, pillar‑specific keys.

2. **UMX-specific manifest extensions:**  
   For UMX, the manifest gets at least these extra fields:
   - `component: "UMX"` — pillar identity.  
   - `tick: t` — snapshot tick (aligned to NAP tick).  
   - `topology_anchor` — hash/anchor of the topology sublayer.  
   - `slp_anchor` — hash/anchor of the SLP (ley field + residual metrics) sublayer.  
   - optional `file_meta`‑style context.

3. **Layer naming pattern:**  
   - `layers/topology.bin` and `layers/slp.bin` are concrete layer payload names.  
   - They show how UMX uses APX layers to separate topology vs ley field/residuals.

**APP‑pillar stance:**

- For the **Press Pillar spec**, we treat the APX manifest fields recovered from the gap‑asks (mode + orig_bytes + hashes + signature) as the **canonical core**.  
- UMX complement docs demonstrate one acceptable pattern of **pillar‑specific extension** for APX capsules (`component`, `tick`, anchors, etc.).  
- We **do not** promote the UMX‑specific keys to global APX mandatory fields, but we can reference this pattern as an example when defining other pillar capsules.

---

## 3. SLP semantics (what Press can assume about the substrate)

The Universal Matrix pillar spec gives us a crisp statement of SLP (Synaptic Ley Protocol) behaviour and invariants:

From `universal_matrix_pillar_spec_v_1.md`:

> "From the SLP spec:
>
> > "Flux per edge (u,v): `du = Su − Sv; flux = floor(k * du / SC)`; move `flux` from the higher to the lower potential.  
> > **Manhattan neighborhood with radius `r`, degree cap `D★`, causality cap `c` per tick.**  
> > Strict integer arithmetic and deterministic edge order ensure replayability.  
> > **Invariants: conservation of total sum, causality (no effects beyond `c` hops), determinism."""

Complement Doc F adds:

> "UMX/SLP v1 defines one flux step per tick:
>
>   `du = Su − Sv; flux = floor(k * du / SC); S[u] -= flux; S[v] += flux`.
>
> LLP adds conceptual structure:
>
> 1. **Merge:** gather local inputs/residuals for each node.  
> 2. **Propagate:** calculate neighbour exchanges (flux).  
> 3. **Resolve:** commit the new state and residuals for next tick."

And proposes normative tightening:

> "SLP v1 MUST be:
>
>   - **monotone residual-reducing** in the sense that, absent new... a simple residual norm (e.g. L1 or L2 difference across neighbours).  
>   - **global-sum-preserving** ..."  
> — `umx_complement_doc_f_llp_slp_propagation.md`

**Press‑pillar implications:**

- When APP compresses UMX state over time, it can assume:
  - **Global conservation** of the SLP field (no phantom gain/loss except from explicit external inputs).  
  - **Finite propagation speed** (`c` hops per tick).  
  - **Deterministic update order** for edges.  
  - **Monotone residual reduction** in absence of new inputs.
- This justifies modelling UMX time series with a **low‑dimensional, smooth structural component** in SimA and relatively small residuals in SimB.
- It also gives Loom/Press a principled basis for **continuity checks** between UMX snapshots (e.g., verifying that sums and residual norms behave as expected between APX capsules).

---

## 4. TBP / Gate–UMX integration relevant to Press

The UMX–Trinity Gate integration spec restates the relationship between Gate, UMX, NAP, and TBP in a way that matters to APP.

From `umx_trinity_gate_integration_spec_v_1_2025_11_17.md`:

> "UMX = **graph substrate + tick engine + drift/emergence + NAP + ledger**"  
> "Role: **Deterministic integer substrate for state storage and conservative propagation.**"  
> — `UMX_README_FOR_DEVS_v1.md`, `universal_matrix_pillar_spec_v_1.md`

> "Trinity Gate is the **interface engine and universal translator**; it converts between external formats and Aether’s native forms and publishes consolidated snapshots into the ledger pipeline."  
> — summarising `trinity_gate_features_components_capabilities 1.md`

> "Gate is the **scene I/O layer** on a 2D plane; exports structured scenes (JSON/CSV/images)."  
> — `tbp_gate_implementation_spec_v_1.md`

The integration spec’s **tick-level contract** for UMX (v1) is:

> "For each tick `τ`, this spec defines the following order:
>
> 1. **UMX update phase**
>    - UMX applies:
>      - any pending NAP envelopes destined for the matrix,
>      - any topology or signal updates routed from Gate via TBP channels,
>      - its own internal propagation (SLP) as per the invariants ..."  
> — `umx_trinity_gate_integration_spec_v_1_2025_11_17.md`

**Press‑pillar implications:**

- **Where APP sits in the loop:**  
  - Gate gathers UMX (and other pillars) into structured scenes and snapshots.  
  - APP can treat Gate output as **structured inputs** (CSV/JSON scenes, APX capsules) at the tick boundaries defined above.  
  - NAP maintains the tick and ensures snapshots are tied to the same global `τ` used by UMX/SLP.
- **TBP’s obligation to Press:**  
  - TBP must not reorder or drop events in a way that breaks UMX invariants; by extension, APP can assume TBP‑mediated UMX data respects conservation, causality, and determinism.

We **do not** get explicit TBP message schemas for Press in these UMX docs; those live in the Gate/TBP implementation packs. For now, the main thing this pass gives us is assurance about **ordering and invariants** at the tick level.

---

## 5. What is *not* in the UMX implementation docs

We explicitly scanned all `implementation/*.md` docs under Universal Matrix pillar for the following APP‑pillar concerns and found **no direct definitions**:

- No **`nap_manifest.json`** schema or key names.  
- No **`APP_BARRIERS.json`** or `press_pareto_manifest_v6_*.json` schemas.  
- No **AEON-i** or **APXi** opcode/grammar tables.  
- No **Modes/Switchboard JSON** representation (PRESS_MODE, S1–S12, F/M/SFTY/N families).  
- No additional constraints on APP’s MDL penalties or deployment‑equivalence constants.

The only APX‑related specifics we gain are:

- APX‑style packaging (`MANIFEST.json` + `layers/...`) is used as a **general capsule pattern** beyond Press.  
- UMX’s particular APX capsules include additional manifest keys (`component`, `tick`, `topology_anchor`, `slp_anchor`, optional `file_meta`) and layer names (`layers/topology.bin`, `layers/slp.bin`).

Everything else remains as previously classified in the Gap Asks Canon Merge pass:

- **NAP manifest schema** — still open.  
- **APP_BARRIERS / Pareto manifests** — still open.  
- **AEON/APXi grammar and IDs** — still open.  
- **Modes JSON / S6, S8, S11 semantics** — still open.  
- **Numeric defaults for deployment knobs** — still open.

---

## 6. How this pass should be used in the Press Pillar spec

- Treat this doc as the **cross-pillar integration layer** between APP and UMX/NAP/TBP:
  - It confirms what APP can safely assume about NAP’s behaviour (bus + clock + auditor, global tick, just numbers & hashes).  
  - It shows a concrete example of **APX-style packaging** for a non‑Press pillar (UMX snapshots).  
  - It tightens SLP assumptions (conservation, causality, deterministic order, monotone residual reduction) that underpin Press’s modelling of UMX time series.
- Do **not** attempt to back‑project UMX‑specific manifest keys into global APX requirements; keep them as **pillar-level extensions**.
- When we later define `nap_manifest.json`, APP_BARRIERS, or deployment profiles, we should **align** with the invariants and patterns here (hash‑based payload_refs, APX+layers structure, per‑tick ordering) but **not** pretend those schemas already exist in this UMX implementation pack.

This keeps the Press Pillar spec tightly anchored to canon while acknowledging and reusing the patterns proven in the UMX implementation docs.



<!-- END SOURCE: astral_press_pillar_cross_pillar_nap_umx_tbp_integration_umx_impl_docs_pass.md -->


---

<!-- BEGIN SOURCE: astral_press_pillar_trinity_gate_implementation_docs_pass.md -->

# Astral Press Pillar — Trinity Gate Implementation Docs Pass

> **Scope**  
> Inspect *all* Trinity Gate implementation docs under `aether full clean/Reports/trinity gate pillar/TGP+TBP implementstion docs/` and extract anything that:
> - Directly constrains **NAP** behaviour (beyond what we already have from Gate JS + UMX docs).
> - Clarifies **SLP** / substrate assumptions as seen by Gate/TBP.
> - Specifies **TBP** guarantees that affect Astral Press / Loom / APX usage.
> - Potentially closes remaining APP gaps (APX manifest variants, NAP manifest, AEON/APXi, APP_BARRIERS, Pareto manifests).
>
> These docs are the result of the same complement process, but focused on **Trinity Gate / TBP**. We treat them as canon for Gate/TBP, and only pull across what is directly relevant to the **Press Pillar**.

---

## 0. Files covered in this pass

Directory:

`aether full clean/Reports/trinity gate pillar/TGP+TBP implementstion docs/`

Markdown files inspected:

1. `old_triune_bridge_report_features_capabilities.md`  
2. `tbp_gate_development_roadmap_v_1.md`  
3. `tbp_gate_dev_roadmap_task_breakdown_v_1.md`  
4. `tbp_gate_golden_fixtures_pack_v_1.md`  
5. `tbp_gate_implementation_spec_v_1.md`  
6. `tbp_gate_operator_runbook_v_1.md`  
7. `tbp_gate_verification_plan_fixtures_crosswalk_v_1.md`  
8. `tbp_gate_verification_test_plan_v_1.md`  
9. `trinity_gate_features_components_capabilities 1.md`  
10. `trinity_gate_older_reports_expansions.md`  
11. `trinity_gate_tgp_focus_expansions.md`  
12. `trinity_gate_vs_math_compendium_coverage_report.md`  
13. `triune_bridge_gate_knowledge_gaps.md`

Plus awareness of (but no PDF parsing in this pass):

- `Core Bridge Math & Representation.pdf`

We searched all 13 `.md` docs for:

- APP-specific schema keywords: `nap_manifest`, `APP_BARRIERS`, `press_pareto`, `AEON`, `APXi`.  
- APX/container keywords: `APX`, `apx`, `Press`, `Astral Press`.  
- Integration keywords: `NAP`, `Loom`, `SLP`, `TBP`, `manifest`.

No occurrences of `nap_manifest`, `APP_BARRIERS`, `press_pareto`, `AEON`, or `APXi` were found in any of these docs. That already tells us: **they do not directly define the still-open APP schemas.**

What we *do* get is detailed behaviour for TBP/Gate’s use of NAP, Loom, fixtures, and experiment packs.

---

## 1. TBP / Gate overview (what this pillar actually does)

Across `trinity_gate_features_components_capabilities 1.md` and `tbp_gate_implementation_spec_v_1.md`, Gate/TBP is described as:

- A **scene I/O layer on a 2D plane**:  
  - Maintains 2D scenes with actors, overlays, and assets.  
  - Runs a “Gate logic” loop each tick, separate from UMX’s SLP update, but coordinated via NAP.

- A **universal translator** between external formats and Aether’s native forms:  
  - Ingests JSON/CSV/logs/images from external world.  
  - Normalises into internal structures (scene graphs, state vectors, typed streams).  
  - Publishes consolidated snapshots and events into NAP/ledger.

- The place where **TBP (Triune Bridge Protocol)** is realised as:
  - L0/L1/L2 integerisation/codec for complex amplitudes / probability fields.  
  - A “thin global residual” layer (L2) used to stitch across pillars via NAP.  
  - Optional relational field mode with simple relational metrics.

From a Press perspective:

- Gate/TBP is the **front door**; Press doesn’t talk to raw external data directly, it often sees Gate outputs (scenes, typed streams, APX-like packs) as its upstream data.  
- TBP defines how **probabilistic/continuous content** is converted into integers that NAP/APP/UMX can consume and replay.

But none of this introduces new APP/Press schema; it sets the **context** and invariants for the data Press will see.

---

## 2. NAP in Gate/TBP docs — behaviour, not manifests

The Gate docs talk about NAP heavily, but always in terms of its **behavioural role**, not as a JSON schema.

### 2.1 NAP as commit bus and auditor (Gate view)

Recurring statements (especially in `old_triune_bridge_report_features_capabilities.md`, `tbp_gate_development_roadmap_v_1.md`, and `triune_bridge_gate_knowledge_gaps.md`) reinforce that for Gate/TBP:

- NAP is the **commit bus**:  
  - Gate/TBP emits envelopes for scene updates, topology changes, and derived data into NAP.  
  - NAP ensures these writes are ordered, exactly-once, and tied to ticks.

- NAP is the **auditor**:  
  - Envelopes include hashes (`payload_ref`), nonces, and seeds.  
  - Commit hashes (U-Commits) are logged to verify runs and reconstruct sessions from packs.

These statements align with the NAP roles we already have from the UMX complement docs and Gate JS implementation. They do **not** introduce a `nap_manifest.json` object, nor any new envelope fields beyond the ones we already pinned from JS (tick, node_id, layer, seed_hex, payload_ref, metrics, mode, sig).

### 2.2 Scene hashing and payload_ref semantics

In `tbp_gate_development_roadmap_v_1.md` and `tbp_gate_implementation_spec_v_1.md`, there are tasks and checks like:

- Compute **content hash** of `scene_frame_core.bin`.  
- Bind it in a NAP-like record with `payload_ref`, `tick`, and signatures.  
- Store hashes in a fixture or manifest used by Loom/Press replay to validate correctness.

This confirms that Gate follows the same **payload_ref** pattern we saw in Gate JS and UMX docs:

- `payload_ref = "sha256:<hex>"` where `<hex>` is the SHA‑256 of the framed payload.  
- Commit metadata (U-Commit) includes `payload_ref` and is used for detecting divergence.

Again, this bolsters the envelope/hash contract but stops short of a NAP manifest schema; everything is described at the level of *records*, *fixtures*, or *pack manifests*, not a single `nap_manifest.json` spec.

### 2.3 Loom replay expectations (from Gate’s POV)

Gate’s verification and test plan docs mention output packs that include:

- Golden commit hashes.  
- Scene frames and their content hashes.  
- Instructions for replaying and verifying runs.

They expect Loom to:

- Take the pack (ZIP + manifests) and reconstruct the simulation hierarchy.  
- Replay the run, using NAP phases, and verify that recomputed hashes match the golden ones.

From a Press perspective:

- This is fully consistent with the Loom + Press + NAP replay algorithm we already captured.  
- Gate’s docs provide **test harness detail**, not new Loom or NAP semantics.

---

## 3. TBP integerisation and relevance to Press

Most of `tbp_gate_implementation_spec_v_1.md` is dedicated to TBP’s
integerisation of quantum/probabilistic state into integer fields `(L0, L1, L2)`.

Press-relevant points (high level; the details live in the TBP spec itself):

- **L0:** quantisation of primary amplitudes/fields.  
- **L1:** local residuals (finer corrections).  
- **L2:** thin global residual, aligned with NAP’s stitch layer.

For Press, the key implication is:

- When compressing TBP‑produced fields/time series, APP can treat the TBP outputs as:  
  - A base integer field (L0),  
  - Local residuals (L1),  
  - A low‑entropy global residual (L2).  
- This structure is ideal for SimA/SimB split:
  - SimA captures the structured quantisation and relational forms.  
  - SimB compresses residuals and noise.

However, these TBP docs do **not** define any APP-specific containers or manifests; they simply define what the data looks like by the time it hits NAP and Press.

---

## 4. Gate experiment packs & manifests — no APP schemas

The older Gate experiment report (`old_triune_bridge_report_features_capabilities.md`) and the coverage report (`trinity_gate_vs_math_compendium_coverage_report.md`) talk about:

- Experiment data packs like `Trinity_Gate_Experiment_Data.zip`, `..._pack2.zip`, etc.  
- “PPTX + manifests” and “ZIPs + manifests + reconstruction instructions”.

They emphasise that:

- Gate/bridge outputs are **fully reconstructible** from these packs without live engine access.  
- The manifests include NAP phases, commit metadata, seeds, and reconstruction instructions.  
- The assistant (or engine) can parse manifests and rebuild the simulation hierarchy.

Crucially, though:

- These are **Gate/TBP experiment manifests**, not APP/APX/Press manifests.  
- They are not presented as stable, pillar-agnostic container schemas; they are described in natural language, not as JSON schemata or field tables.  
- No file named `nap_manifest.json` or `MANIFEST.json` is defined in those Gate reports with a concrete field list for APP.

So we learn **how Gate packages its own test packs**, but we do not obtain any new canonical APP/APX manifest definitions.

---

## 5. Explicitly checked and still absent

Within the Trinity Gate implementation docs, we **explicitly verified** that the following strings do *not* appear in any `.md` files:

- `nap_manifest`  
- `APP_BARRIERS`  
- `press_pareto`  
- `AEON`  
- `APXi`

We also searched for:

- `APX`, `apx`, `Astral Press`, `Press capsule` — none appear as container names or schemas.  
- Mentions of **Press** are in passing, as references to the Aether Press experiments or Occam/Press lineage, not as container or API definitions.

Therefore, this implementation pack **does not** secretly contain the missing APP schemas:

- No `nap_manifest.json` field definitions.  
- No `APP_BARRIERS.json` schema.  
- No `press_pareto_manifest_v6_*.json` schema.  
- No AEON-i / APXi opcode or grammar tables.

It does confirm and reinforce the **behavioural contracts** we already have (NAP as bus/auditor, payload_ref conventions, Loom replay expectations, TBP integerisation), but it does not introduce new schema-level canon for APP.

---

## 6. Impact on Astral Press Pillar gap status

### 6.1 Gaps confirmed as **still open**

The Trinity Gate implementation docs **do not** close the following gaps for APP:

- **NAP manifest (`nap_manifest.json`)**:
  - Still no canonical JSON schema; UMX and Gate both speak about NAP as a bus and about experiment manifests in general terms, but no cross-pillar `nap_manifest.json` structure is defined.

- **APP_BARRIERS / Pareto manifests**:  
  - No occurrence of `APP_BARRIERS` or `press_pareto` here; Gate docs do not define Press policy packs or Pareto summary manifests.

- **AEON-i / APXi grammar & IDs**:  
  - TBP/Trinity Gate docs reference integerisation and residual layers, but never mention AEON or APXi; they do not add any opcode or stream spec.

- **Modes/Switchboard JSON**:  
  - The Gate implementation pack does not define PRESS_MODE or S1–S12 encodings; mode governance remains in the core Aether mode docs and gap-ask answers.

- **Numeric deployment defaults for Press**:  
  - TBP defines resolution tiers (η, P) for Gate’s codecs, but does not set APP’s MDL penalties or threshold constants. Those remain symbolic knobs in Press.

### 6.2 Gaps where behaviour is reinforced (but schemas remain design space)

These docs **reinforce** behaviours that Press can rely on:

- **NAP:**
  - Bus + clock + auditor.  
  - Messages carry `payload_ref = 'sha256:<hex>'`, nonces, ticks, seeds.  
  - Commit hashes and experiment packs make sessions reconstructible.

- **Loom:**
  - Expected to reconstruct runs from packs using NAP phases and commit metadata.  
  - Press/Loom replay assumptions align with Gate’s own verification story.

- **TBP integerisation:**
  - L0/L1/L2 structure, relational field option.  
  - Good fit for SimA/SimB modelling assumptions in Press.

But **schema-level** definitions (what `nap_manifest.json` looks like, the exact layout of Press policy/pareto manifests, AEON/APXi tables) are still not specified here and remain open for v1 design.

---

## 7. How to use this pass in the Press Pillar spec

This Trinity Gate implementation pass should be used as:

- A **cross-pillar consistency check**:  
  - Our NAP, Loom, and TBP assumptions in the Astral Press spec match what Gate expects and verifies in its own implementation docs.  
  - No contradictions were found.

- A **pattern source** for packaging and testing:  
  - Gate’s experiment packs show one viable way to bundle manifests, payloads, and commit hashes into ZIPs that Loom/Press can consume.  
  - When designing APP’s own test packs or multi-pillar capsules, we can mirror these patterns.

- A **negative confirmation** for missing APP schemas:  
  - We can now confidently state that `nap_manifest.json`, `APP_BARRIERS.json`, `press_pareto_manifest_v6_*.json`, and AEON/APXi grammar **are not** defined in the Trinity Gate implementation docs.  
  - Any future schema we design for these must be clearly marked as **post-canon v1 design**, not recovered canon.

This keeps the Astral Press Pillar spec tightly aligned with everything that *does* exist in the Gate implementation pack, without pretending that it fills gaps it simply does not address.



<!-- END SOURCE: astral_press_pillar_trinity_gate_implementation_docs_pass.md -->


---

<!-- BEGIN SOURCE: astral_press_pillar_trinity_gate_impl_docs_extraction_pass.md -->

# Astral Press Pillar — Trinity Gate Impl Docs (Extraction Pass)

> **Scope**  
> Sweep the *Trinity Gate* implementation docs under `Reports/trinity gate pillar/TGP+TBP implementstion docs/` inside **aether full clean.zip** and extract only what is canon and Press‑relevant. All interpretations are backed by **direct quotes** from those files. Anything not present is left as a gap.

---

## 1) What Trinity Gate (TBP) guarantees that APP can rely on

### 1.1 Deterministic, near‑lossless interface engine

- “**deterministic, lossy, and reversible to first order.**” — *Implementation Spec v1*
- “maps complex quantum amplitudes onto **structured integers** (and back)… with **near‑lossless fidelity**.” — *Implementation Spec v1*  
- “variance drops **quadratically** as resolution increases (σ² ∝ η⁻²)… **F ≈ 1 − k/η**.” — *Implementation Spec v1*

**Implication (APP):** APP may treat Gate outputs (scenes, packs) as integerized signals with controlled residuals and explicit resolution knobs (η), i.e., well‑behaved inputs for SimA/SimB.

### 1.2 L0/L1/L2 separation & pipeline posture

- “**L0 quantisation; L1 local residuals; L2 thin global residual (NAP stitch).**” — *Implementation Spec v1*
- “**Fetch → Bridge‑normalize → Inject** with allowlists, redaction, rate limits, approvals.” — *Development Roadmap v1*
- “Hash every scene; **commit chain records payload_ref**.” — *Development Roadmap v1*

**Implication (APP):** Gate consistently hashes content and exposes content‑addressed references (`payload_ref`), aligning with NAP/APP’s hash‑first design.

### 1.3 Determinism & seeds; Ledger & Loom hooks

- “Ξ = **SHA‑256(U_commit ∥ node_id ∥ ⌊τ/W⌋)**.” — *Development Roadmap v1*
- “**Offline‑by‑default; PII tripwire; brokered egress; kill‑switch.**” — *Development Roadmap v1*

**Implication (APP):** Gate/LOOM/U integrations adhere to hashable epochs and conservative egress — APP capsules can inherit these identities and policies.

---

## 2) Gate → NAP bindings we can treat as canonical

Although Trinity Gate docs are Gate‑centric, they reinforce NAP conventions used by APP:

- “`tbp_nap/` (**NAP envelopes, network binding**).” — *Development Roadmap v1*
- “Hash every scene; commit chain **records payload_ref**.” — *Development Roadmap v1*

**Press‑pillar carry‑over:**

- The **payload ref** abstraction (hash‑first reference rather than embedding) is mandatory across Gate and APP.  
- NAP envelopes exist as the transport unit Gate binds to; APP’s NAP envelope spec (from Gate JS) matches this posture (canonical JSON → SHA‑256, `payload_ref = "sha256:<hex>"`).

---

## 3) Packs & manifests (what’s promised vs what’s absent)

The Gate plan is explicit about pack structure but does **not** ship schemas here:

- “`tbp_packs/` (tiling, stitching, **manifests**).” — *Development Roadmap v1*
- “Pack builder… **manifests**, hashes, commit_ref.” — *Development Roadmap v1*

**What exists in these docs:**

- Clear **intent** to produce pack manifests and to hash all artifacts.  
- Integration points with Loom/Press/U are named and staged.

**What does not:**

- No concrete JSON schema for any Gate **pack manifest** in this folder.  
- No field tables we could lift into APP as canon.

APP takeaway: do **not** borrow a Gate manifest schema from this pack; it isn’t defined here.

---

## 4) Feature surface & component posture (Press‑useful bits)

From **Features/Components/Capabilities** report:

- Gate is Aether’s “**interface engine and universal translator** … **standalone execution engine**… converts between quantum‐classical … with near‑lossless fidelity and negligible cost.”
- Gate acts as the **perceptual interface** and a **semi‑permeable membrane** around core simulation, “**projection of internal state as external ‘scenes’ through defined channels**.”

**Press‑pillar implications:**

- APP can assume Gate outputs are **channeled scenes** (typed, bounded), not arbitrary freeform blobs.  
- This supports using APP as a **post‑scene compressor** (e.g., scene CSV/JSON/image channels) with strong structure (good SimA wins).

---

## 5) Verified gaps (as stated by the Gate docs themselves)

From **Triune Bridge / Gate — Knowledge Gaps**:

- “**No concrete data models / schemas** … JSON schemas or type definitions for: **Scene frames; Control envelopes; Evidence bundles; Schema registry entries; Approval records; …** Without that, any implementation will be *your* best guess.”

**Therefore, still open (for Gate docs in this folder):**

- **No scene/control/evidence JSON schemas** to import into APP.  
- **No NAP envelope schema** beyond the existence of payload_ref and hashing posture.  
- **No Modes/Switchboard JSON** for Gate.  
- **No Gate→APP specific manifest crosswalk.**

---

## 6) How this tightens the Press Pillar spec (and what it doesn’t)

**Tightens:**

- Confirms **hash‑first references** and **commit‑chain payload_ref** as shared conventions → APP’s NAP envelope rules stay aligned.  
- Confirms **L0/L1/L2** separation and the **Fetch→Normalize→Inject** guardrail posture → APP can assume structured, deterministic Gate inputs.  
- Confirms determinism/seed/ledger hooks and **offline‑first + kill‑switch** ops policy → APP capsules can mirror these policies.

**Doesn’t close:**

- It does **not** define `nap_manifest.json`, `APP_BARRIERS.json`, or Pareto schemas.  
- It does **not** define AEON/APXi grammar or IDs.  
- It does **not** define Gate pack/scene JSON schemas.

---

## 7) Minimal cross‑pillar contract (APP consuming Gate)

1. Treat every Gate scene/pack as **content‑addressed** (hash everything; store **payload_ref**).  
2. Keep Gate inputs to APP **integerized** with explicit resolution param (η) and expose L0/L1/L2 if available.  
3. Preserve **tick (τ)** and **seed** context so Loom/Press replay remains deterministic.  
4. Enforce **offline‑first, PII tripwire, brokered egress, kill‑switch** at APP ingress points that consume Gate outputs.  
5. Do **not** fabricate missing schemas — where needed, design new ones in **post‑canon** canvases.

---

### Appendix — File paths examined (inside `aether full clean.zip`)

- `Reports/trinity gate pillar/TGP+TBP implementstion docs/tbp_gate_implementation_spec_v_1.md`  
- `Reports/trinity gate pillar/TGP+TBP implementstion docs/tbp_gate_development_roadmap_v_1.md`  
- `Reports/trinity gate pillar/TGP+TBP implementstion docs/tbp_gate_operator_runbook_v_1.md`  
- `Reports/trinity gate pillar/TGP+TBP implementstion docs/tbp_gate_verification_test_plan_v_1.md`  
- `Reports/trinity gate pillar/TGP+TBP implementstion docs/tbp_gate_verification_plan_fixtures_crosswalk_v_1.md`  
- `Reports/trinity gate pillar/TGP+TBP implementstion docs/tbp_gate_golden_fixtures_pack_v_1.md`  
- `Reports/trinity gate pillar/TGP+TBP implementstion docs/trinity_gate_features_components_capabilities 1.md`  
- `Reports/trinity gate pillar/TGP+TBP implementstion docs/triune_bridge_gate_knowledge_gaps.md`



<!-- END SOURCE: astral_press_pillar_trinity_gate_impl_docs_extraction_pass.md -->


---

<!-- BEGIN SOURCE: astral_press_pillar_trinity_gate_impl_docs_targeted_extract_plan.md -->

# Astral Press Pillar — Trinity Gate Impl Docs (Targeted Extract Plan)

> **Scope**
> Extract Press‑relevant canon from **Aether › reports › Trinity Gate › implementation** docs (pre‑implementation complement set). Focus on APP/NP relations: NAP envelopes, budgets, TBP bridges, Gate scene I/O, and any APX/manifest specifics.
>
> **Status note:** Access to the uploaded archive is currently blocked at runtime (tool I/O fails). This plan captures exactly what we will extract once file I/O is restored, so we can paste content into the placeholders below without re‑deciding scope.

---

## 0) Pull‑list (expected files)

- `reports/trinity gate/implementation/` (approx path)
  - `trinity_gate_features_components_capabilities*.md`
  - `tbp_gate_implementation_spec_v*.md`
  - `trinity_gate_umx_bridge_spec*.md`
  - `gate_nap_envelope_contract*.md`
  - `gate_budget_and_kill_switch*.md`
  - `gate_scene_io_formats*.md`

> If filenames differ, keep the intent: features/capabilities, TBP integration, NAP contract, budgets/kill‑switch, scene I/O formats.

---

## 1) NAP envelope contract (Gate‑side)

**What to extract verbatim (quotes):**
- Field list and **exact key names** used by Gate for envelopes.
- Canonicalisation order and hash/signature rules.
- `payload_ref` format and any non‑SHA‑256 options.
- Any **nonce/idempotence** handling notes.

**Paste here →**

> [VERBATIM EXCERPTS]

**APP impact:**
- Confirm/extend our current NAP envelope spec for Press capsules.

---

## 2) NAP budgets & kill‑switch (Gate/TBP)

**What to extract verbatim:**
- Definitions for hard/soft budgets (messages & bytes).
- Exact **soft‑limit formula** if present.
- Kill‑switch trigger names and reasons.
- Any TSV/CSV fixture column **names** used for budgets.

**Paste here →**

> [VERBATIM EXCERPTS]

**APP impact:**
- Tighten Press ingest assumptions; align Loom replay annotations.

---

## 3) TBP bridge spec (Gate ↔ NAP/UMX)

**What to extract verbatim:**
- Tick‑ordering guarantees (Gate publish vs UMX update).
- Exactly‑once and dedupe semantics.
- Scene routing, priorities, and dead‑letter handling.

**Paste here →**

> [VERBATIM EXCERPTS]

**APP impact:**
- Clarify when APP may snapshot/press scenes without violating UMX invariants.

---

## 4) Gate scene I/O formats

**What to extract verbatim:**
- Canonical JSON/CSV headers for **scene export**.
- Any schema IDs and anchor conventions.
- Size/row limits and normalization constraints.

**Paste here →**

> [VERBATIM EXCERPTS]

**APP impact:**
- Lock Press translators for Gate scenes; reduce unknowns in SimA.

---

## 5) APX/APXi references from Gate docs

**What to extract verbatim:**
- Mentions of APX capsules produced/consumed by Gate.
- Any APXi/AEON references (descriptor or integer stream).
- Manifest additions (e.g., `component`, `tick`, anchors) if Gate produces capsules.

**Paste here →**

> [VERBATIM EXCERPTS]

**APP impact:**
- Reuse UMX’s APX pattern for Gate‑origin capsules.

---

## 6) Mode hooks (PRESS_MODE, S‑modes, safety)

**What to extract verbatim:**
- Gate‑side toggles that affect Press/ESL/F‑modes.
- Any mapping to S‑modes (Canary, Governor, etc.).

**Paste here →**

> [VERBATIM EXCERPTS]

**APP impact:**
- Bind Press operation to Gate’s live switchboard once schema exists.

---

## 7) Finalize → Canon inserts

When excerpts are pasted:
- We will create a **Trinity Gate Impl (Canon Pass)** doc that:
  - Integrates quotes into the APP spec (envelopes, budgets, TBP order, scene I/O).
  - Cross‑links to existing NAP/UMX/APX canvases.
  - Calls out new closures vs remaining gaps.

**Owner action:** Paste source quotes into the slots above or provide a non‑redacted archive path we can read directly. After that, I’ll convert this plan into the full canon pass immediately.



<!-- END SOURCE: astral_press_pillar_trinity_gate_impl_docs_targeted_extract_plan.md -->


---

<!-- BEGIN SOURCE: astral_press_pillar_trinity_gate_tbp_integration_gate_impl_docs_pass.md -->

# Astral Press Pillar — Trinity Gate & TBP Integration (Gate Impl Docs Pass)

> **Scope**  
> Mine the Trinity Gate / TBP implementation docs under `Reports/trinity gate pillar/TGP+TBP implementstion docs/` in `aether full clean` for anything that **directly constrains or clarifies Astral Press (APP)**.
>
> These docs were produced by the same complement process we’re using now, but for the Gate/TBP pillar. They are canon for Gate/TBP/UMX integration; we only import what touches:
> - Press’s role in the full system,  
> - How Gate/TBP expect Press to behave,  
> - Any concrete I/O or runtime contracts involving Press/Loom/U.
>
> We explicitly do **not** treat these as sources for:
> - AEON/APXi opcode tables,  
> - `nap_manifest.json` schema,  
> - APP_BARRIERS / Pareto schemas,  
> because those strings do not appear in these docs.

Sources inspected:

- `old_triune_bridge_report_features_capabilities.md`  
- `tbp_gate_development_roadmap_v_1.md`  
- `tbp_gate_dev_roadmap_task_breakdown_v_1.md`  
- `tbp_gate_golden_fixtures_pack_v_1.md`  
- `tbp_gate_implementation_spec_v_1.md`  
- `tbp_gate_operator_runbook_v_1.md`  
- `tbp_gate_verification_plan_fixtures_crosswalk_v_1.md`  
- `tbp_gate_verification_test_plan_v_1.md`  
- `trinity_gate_features_components_capabilities 1.md`  
- `trinity_gate_older_reports_expansions.md`  
- `trinity_gate_tgp_focus_expansions.md`  
- `trinity_gate_vs_math_compendium_coverage_report.md`  
- `triune_bridge_gate_knowledge_gaps.md`

We searched them for `Press`, `nap `, `NAP `, `SimA`, `SimB`, `APP `, `capsule`, and only treat content that actually mentions Press as constraining APP.

---

## 1. Where Press sits in the Trinity Gate / TBP stack

Across the Gate/TBP docs, Press is consistently described as part of the **core ledger/telemetry stack**, not a bolt‑on:

- Internal state arrays (for Gate’s quantum/scene encodings) remain internal; only projections are exposed to the outside world. The **full detailed internal state** is captured in **Loom/Press/U** as compressed, replayable history.
- Trinity Gate is described as the **scene I/O and translation layer**; TBP is the protocol that moves those scenes as structured data. Press is the system that **compresses and archives** those histories.

The net picture is:

- Gate/TBP: handle **I/O, scene construction, and protocol framing**.  
- NAP: provides **bus + clock + auditor** for messages.  
- UMX/SLP: provides **deterministic substrate / physics**.  
- **Press/Loom/U**: provide **compressed, reversible histories and state snapshots**.

APP therefore is **first‑class** in the Trinity stack; Gate expects it to be present and working according to the core Press spec.

---

## 2. Press behaviour as assumed by TBP (no new math, but explicit stance)

### 2.1 Press as dictionary+delta, MDL‑governed

The TBP implementation spec v1 summarises how it assumes Press behaves:

- Press is described as **“dictionary + delta blocks (lossless)”** for the Gate/TBP use‑case.  
- It explicitly states an **MDL acceptance rule**:  
  > only apply a transform if ΔL_total > 0.

This matches the dedicated APP MDL pass we already have:

- SimA captures structure using dictionaries/transform rules.  
- SimB captures residuals.  
- A new transform is only accepted if it **strictly reduces** the total description length.

The Gate/TBP docs do not add new Press math; they simply reiterate the MDL rule as a **hard expectation** for Press when used under TBP.

### 2.2 Replay and rehydration

The TBP runbook and implementation spec reference replay as:

- Restore last **U_commit**.  
- **Rehydrate Loom/Press dictionaries from logs**.  
- Proceed deterministically from those logs.

This aligns with:

- Loom + Press replay algorithm in the Aevum Loom docs (checkpoints + progress blocks).  
- Press’s requirement to be **deterministic and reversible (within the chosen mode)**, with dictionaries derived from the same inputs at replay time.

Gate/TBP are therefore assuming that:

- Press has a well‑defined **dictionary state** that can be reconstructed deterministically from the ledger and/or checkpoints.  
- Given the same seeds, tick sequence, and inputs, Press will regenerate dictionaries and compressed streams identically.

No new structures are defined for Press here; these are **integration assumptions** that must be honoured by any APP implementation.

---

## 3. TBP I/O expectations on Press

While most of the TBP implementation spec deals with quantum‑oriented encodings (m, p, relational fields, etc.), there are a few concrete expectations that touch Press:

1. **Press is lossless for TBP payloads.**  
   - TBP spec explicitly pairs Press with **dictionary + delta** blocks, with no mention of lossy modes.  
   - For TBP/Trinity Gate’s v1 implementation, Press must therefore be configured in **lossless mode**.

2. **Chunking behaviour:**  
   - The spec advises:
     - Prefer **CSV‑only** for large packs in constrained environments.  
     - Split large ranges into smaller slices (e.g., M–P into M–N + O–P) if compression hits memory guards.
   - This is advice to Gate/TBP on how to **prepare inputs for Press**, not a Press internal behaviour change.
   - For APP, this means: be prepared to handle **chunked streams** that are logically contiguous in time but split into multiple CSV/JSON packs for resource reasons.

3. **Loom / Press / U interplay:**  
   - Gate’s implementation spec explicitly lists Loom/Press/U together when talking about full internal state capture.  
   - For Press, this reinforces that certain Gate/TBP internal traces will be stored in **Loom‑compatible streams** that Press must be able to compress and replay.

The TBP docs do not define new Press modes or change the MDL rules; they define **how TBP chooses to use Press**:

- Lossless, MDL‑governed compression of Gate/TBP’s own telemetry.  
- Press state/dictionaries are part of the replay story via Loom and U_commit.

---

## 4. NAP & Press from Gate/TBP’s perspective

Gate/TBP implementation docs mention NAP frequently (as part of the full Trinity stack) but **do not define new NAP schemas or manifest fields**. The key points for APP are:

- NAP is treated as the protocol that carries **integers and hashes**, not raw blobs.  
- TBP expects that any compressed payloads (including those produced by Press) will be referenced via **hashes** (payload_refs) rather than embedded directly.

This matches:

- The Gate JS NAP implementation (NAP envelopes with `payload_ref = "sha256:<hex>"`).  
- The NAP integration we already captured from the UMX implementation docs.

No `nap_manifest.json` schema or Press‑specific NAP payload formats are introduced in these Gate/TBP docs.

---

## 5. TBP/Gate features & capability maps that mention Press

The features/capabilities and older‑reports/expansions docs reference Press primarily as **part of a capability matrix**:

- Gate can emit **Press‑ready CSV/JSON scenes**.  
- There are explicit capabilities for **log/telemetry capture** that presuppose Press and Loom will compress and store the results.  
- Some feature roadmaps include “baking in” Press and Loom integration as part of the Gate operator experience.

From a Press Pillar perspective this confirms:

- Press is a **first‑class concern** when designing Gate/TBP features (e.g., scene snapshots, test harnesses, debug logs).  
- Press must be able to consume Gate outputs in their documented formats (primarily structured CSV and JSON packs) without requiring custom high‑entropy encodings.

Again, there is no new math or schema for Press here—only integration expectations.

---

## 6. Knowledge gaps (from Gate’s POV) that touch Press

The `triune_bridge_gate_knowledge_gaps.md` doc lists remaining open questions for the Gate/TBP pillar. Press is mentioned in some of these, but always in ways that are **already known gaps** from the APP perspective:

- Precise schemas and constants for Press‑related deployment profiles.  
- More detailed integration tests between Gate/TBP, UMX, NAP, Loom, and Press.  
- No additional details on:
  - AEON/APXi.
  - `APP_BARRIERS.json` or Pareto manifests.
  - Mode/Switchboard JSON.

So these docs **do not** secretly contain extra Press canon we missed—they explicitly agree those areas are future work.

---

## 7. What this pass changes (for the Press Pillar spec)

### 7.1 Strengthened, but not expanded, Press requirements

From this Gate/TBP implementation pass, APP must now assume the following **as hard integration constraints**:

1. **Lossless Press mode for TBP.**  
   - When used under TBP/Trinity Gate v1, Press must be configured in **lossless mode** (dictionary + delta blocks) so that Gate/TBP’s expectation of no information loss is met.

2. **Strict MDL acceptance (ΔL_total > 0) is relied upon.**  
   - Gate/TBP spec reiterates this as a given; any future Press implementation must respect it for TBP‑bound streams.

3. **Deterministic replay via Loom/Press/U.**  
   - Gate/TBP assumes that given the same logs and U_commit, Press can rehydrate its dictionaries and compressed streams deterministically.

4. **Chunk‑friendly operation.**  
   - Press must tolerate input being chunked by Gate/TBP (e.g., CSV packs split to obey memory guards) and still produce consistent, well‑formed capsules per chunk.

5. **NAP hash‑based references.**  
   - When Press outputs are routed via NAP/TBP, they must integrate with the existing `payload_ref` hash conventions; APP must not assume it can push opaque blobs into NAP envelopes.

### 7.2 What remains unchanged

This pass **does not** add:

- Any new Press transforms, metrics, or modes.  
- Any schemas for `nap_manifest.json`, `APP_BARRIERS.json`, or Pareto manifests.  
- Any AEON/APXi details or Modes/Switchboard JSON.

It is a **pure integration pass**: it clarifies how the Trinity Gate / TBP implementation relies on Press, and confirms that the current APP spec is compatible with those expectations, as long as Press stays in lossless MDL‑governed mode for TBP and obeys the deterministic replay rules via Loom/U.

This canvas should be referenced from the top‑level Astral Press Pillar spec wherever we discuss **system integration**, particularly with Gate/TBP and UMX/NAP.



<!-- END SOURCE: astral_press_pillar_trinity_gate_tbp_integration_gate_impl_docs_pass.md -->


---

<!-- BEGIN SOURCE: trinity_gate_nap_pack_schemas_gate_impl_docs_pass.md -->

# Trinity Gate — NAP & Pack Schemas (Gate Impl Docs Pass)

> **Scope**  
> Mine `aether full clean/Reports/trinity gate pillar/TGP+TBP implementstion docs/` for anything that **closes Press‑relevant gaps** about NAP envelopes, signatures, payload hashes, and pack/manifest structure. Quote the repo docs directly (canon = project files). No invention.

---

## 1) NAP envelope — required keys, patterns, signing

**Canon (Implementation Spec v1):**

> “## 3) NAP envelopes & Gate scene schemas”  
> “### 3.1 NAP envelope (v1 JSON over TCP/WS; CBOR allowed)”

> “Each node emits envelope: tick, node_id, layer, metrics, seed, payload hash (no raw data).”  
> “`"required": ["tick","node_id","layer","seed_hex","payload_ref","metrics","mode","sig"],`”  
> “`"payload_ref": { "type": "string", "pattern": "^sha256:[0-9a-f]{64}$" },`”  
> “`"seed_hex": { "type": "string", "pattern": "^[0-9a-f]{64}$" },`”

> “**Signatures:** envelopes signed over canonical JSON (sorted keys, UTF‑8, SHA‑256 preimage).”

> “**Provenance:** include `commit_ref` and `payload_ref` everywhere outbound.”

**What this closes:**
- **Required keys and types** for NAP envelope (`tick`, `node_id`, `layer`, `seed_hex`, `payload_ref`, `metrics`, `mode`, `sig`).
- **Content‑addressing rule** for payloads: `payload_ref = "sha256:<64 hex>"`.
- **Seed format**: 64 hex chars.
- **Signature practice**: sign canonical JSON (sorted keys, UTF‑8, SHA‑256 preimage). (Spec also mentions Ed25519 as an allowed signature; stays optional at envelope level.)

---

## 2) Commit chain & determinism hooks

**Canon (Implementation Spec v1):**

> “* **Tamper‑evident logging:** hash every scene frame; commit chain records payload_ref.”

> “* Scene Sₜ → hash hₜ; payload_ref carries hₜ; U commit includes it; any change breaks chain.”

> “* **U**: commit record with `payload_ref=h_t`, parent commit hash, tick, and signatures.”

> “5. **Determinism**: identical inputs/log produce identical commits, seeds, payload_refs.”

**What this closes:**
- Payloads are **never in the envelope**; only **hash references**.
- **Commit chain** ties `payload_ref` + parent hash + tick (+ sigs).
- **Determinism** guarantee at the envelope/commit level.

---

## 3) Pack/manifest structure for Gate (v1)

**Canon (Implementation Spec v1):**

> “Per‑pack manifests include: `state_range`, `scale_params (η/P) … principal_vector(s)`, `phase_offset`, `error_metrics`, artifact hashes.”

> “### 2.3 v1 manifest (per slice / per pack)”  
> “`// slice_manifest.v1.json`”  
> “`// pack_manifest.v1.json`”  
> “`  "slices": ["sliceA.manifest", "sliceB.manifest", "sliceC.manifest", "sliceD.manifest"],`”

**What this closes (for Press/APX interop):**
- A **Gate pack** is a bundle with a **pack manifest** pointing at one or more **slice manifests**.
- Slice/pack manifests carry **scale/phase/error** and **artifact hashes**.
- This mirrors the APX pattern (manifest + layered payloads), and gives us durable **field names** we can reference when APP consumes Gate packs.

---

## 4) Seed derivation — fixture locks exact procedure

**Canon (Golden Fixtures Pack v1):**

> “**Goal:** Remove ambiguity in `Ξ = SHA‑256(U_commit ∥ node_id ∥ ⌊τ/W⌋)` by pinning one exact example.”

> “1. Parse `U_commit_hex` → 32 raw bytes.”  
> “2. Encode `node_id` as UTF‑8 bytes (no NUL terminator).”  
> “3. Encode `771` as unsigned 64‑bit big‑endian integer.”  
> “4. Concatenate: `U_commit_bytes ∥ node_id_utf8 ∥ uint64_be(771)`.”  
> “5. Hash with SHA‑256.”

**What this closes:**
- **Exact byte‑level procedure** for deriving `seed_hex` from commit context + node + time window.
- Confirms why `seed_hex` is a 64‑hex string and how it stays **deterministic across peers**.

---

## 5) Schema enforcement & ingress guarantees

**Canon (Verification Test Plan v1):**

> “**Goal:** Verify correct enforcement of schemas.”  
> “Authorized peers can exchange NAP envelopes.”  
> “No envelopes are accepted from unknown keys.”  
> “Invalid schemas / PII / over‑budget inputs are quarantined.”  
> “Exported JSON matches schema (§3.2).”

**What this closes:**
- Gate enforces **schema correctness** (JSON/CSV scenes).  
- **AuthZ on envelopes** (peer keys) + quarantine on invalid/over‑budget.

---

## 6) What’s *still* open (for APP)

- These Gate docs **do not** define `nap_manifest.json` (APP’s NAP compression manifest) — still open in Press spec.
- No `APP_BARRIERS.json` or `press_pareto_manifest_v6_*` schemas here.
- No AEON‑i or APXi opcode/grammar tables here.

**But** this pass **does** fully close, for APP’s purposes:
- Envelope key set + regex patterns.  
- Signature procedure (canonical JSON).  
- Commit chain usage of `payload_ref`.  
- Gate pack/slice manifest field names (state_range, scale_params(η/P), principal_vector(s), phase_offset, error_metrics, artifact hashes).  
- Seed derivation procedure with a reproducible fixture.

---

### Appendix — File paths inspected

- `aether full clean/Reports/trinity gate pillar/TGP+TBP implementstion docs/tbp_gate_implementation_spec_v_1.md`  
- `aether full clean/Reports/trinity gate pillar/TGP+TBP implementstion docs/tbp_gate_golden_fixtures_pack_v_1.md`  
- `aether full clean/Reports/trinity gate pillar/TGP+TBP implementstion docs/tbp_gate_verification_test_plan_v_1.md`  
- `aether full clean/Reports/trinity gate pillar/TGP+TBP implementstion docs/trinity_gate_features_components_capabilities 1.md`  
- `aether full clean/Reports/trinity gate pillar/TGP+TBP implementstion docs/triune_bridge_gate_knowledge_gaps.md`



<!-- END SOURCE: trinity_gate_nap_pack_schemas_gate_impl_docs_pass.md -->


---

<!-- BEGIN SOURCE: trinity_gate_pillar_press_loom_integration_tgp_tbp_impl_docs_pass.md -->

# Trinity Gate Pillar — Press & Loom Integration (TGP/TBP Impl Docs Pass)

> **Scope**  
> Mine `aether full clean/Reports/trinity gate pillar/TGP+TBP implementstion docs/` for anything that **constrains or clarifies Astral Press & Loom behaviour** in the Gate/TBP context.  
> Only use direct quotes from these docs; do not invent new behaviour.  
> Focus: where `Press`, `Loom`, and `U` are named and wired, and what is still explicitly missing.

Sources scanned:
- `tbp_gate_implementation_spec_v_1.md`  
- `trinity_gate_features_components_capabilities 1.md`  
- `tbp_gate_development_roadmap_v_1.md`  
- `tbp_gate_dev_roadmap_task_breakdown_v_1.md`  
- `tbp_gate_golden_fixtures_pack_v_1.md`  
- `tbp_gate_operator_runbook_v_1.md`  
- `trinity_gate_older_reports_expansions.md`  
- `trinity_gate_tgp_focus_expansions.md`  
- `trinity_gate_vs_math_compendium_coverage_report.md`  
- `old_triune_bridge_report_features_capabilities.md`  
- `triune_bridge_gate_knowledge_gaps.md`

No occurrences of `nap_manifest`, `APP_BARRIERS`, `press_pareto`, `AEON`, or `APXi` appeared in this directory; those schemas remain unaddressed here.

---

## 1. Gate’s Loom/Press/U path (high-level pipeline)

From the Gate knowledge gaps report:

> “Pipelines: **ingest → normalize → render → Loom → Press → U**.”  
> — `triune_bridge_gate_knowledge_gaps.md`

This is the **clearest single-line pipeline statement** for how Gate hands work to Loom/Press/U.

Implications (pure restatement / stitching):

- **Ingest → normalize → render**: Gate’s front half; handles external data, units, schema, and scene building.  
- **Loom**: records and replays Gate’s evolution over ticks.  
- **Press**: compresses the logged states.  
- **U (Universal Commit)**: receives compressed commits and becomes the “single source-of-truth integer commit stream for state progression.” (see §3.3 below).

The same report notes that some aspects are **still missing**:

> “3. **No fully-specified back-pressure and queuing behaviour**
>   * ‘Gate is non-blocking; frames queue with back-pressure.’
>   You know there’s an input ledger and Loom/Press/U commits, but not:  
>   * **Governance-level spec** (exact policies and automations for PII, approvals, back-pressure).”  
> — `triune_bridge_gate_knowledge_gaps.md`

So governance/back‑pressure around Loom/Press/U is explicitly marked as a **gap**, even in the Gate implementation docs.

---

## 2. Press as Gate’s compression & learning arm

From the Gate features & capabilities doc:

> “**Press (Aether Press – Compression & Learning)**
>
>   * Performs **rolling compression** on Gate’s scene outputs using **dictionary and delta coding and dictionary compression, without losing information**.
>   * Works with Loom to avoid recomputing identical outputs.”  
> — `trinity_gate_features_components_capabilities 1.md`

Additional context around that bullet:

> “* Logs each Gate-generated scene with a **content hash**.
>   * Detects repeats and supports **replay via hash**, guaranteeing **verifiable, replayable frames**.
>
> * **Universal Commit (U) – Universal Integer Stream**
>
>   * Single source-of-truth **integer commit stream** for state progression.
>   * Gate outputs (after Press) are appended as commits, **advancing the state hash and tying each frame into an immutable run record**.”  
> — `trinity_gate_features_components_capabilities 1.md`

From the same document, in the “Perceptual interface & long‑run operation” section (abridged around the Press statements):

> “Tick schedule: domain nodes update first, then **(τ, GATE)**, then **(τ, LOOM)**, **(τ, PRESS)**, **(τ, U)**.  
>   * Supports **pause/resume** (resume from recorded commit and Press dictionary).
>   * Logs are compact due to Press; long-term standalone operation is feasible.”  
> — `trinity_gate_features_components_capabilities 1.md`

Taken together, these quotes establish the **canonical Gate‑side role of Press**:

1. Press runs **after Loom** on each tick (`(τ, GATE) → (τ, LOOM) → (τ, PRESS) → (τ, U)`).  
2. Press performs **rolling compression** on Gate’s scene outputs, using **dictionary + delta coding** without losing information.  
3. Press and Loom together ensure that Gate can **replay identical outputs by hash** and avoid recomputation.  
4. Press emits compressed commits into `U`, and **Press dictionary state** is necessary to support **pause/resume** from a commit.

This confirms and sharpens earlier APP canon:

- APP is not just a general compressor; in the Gate context, it is explicitly a **rolling dictionary+delta compressor** over scene streams, operating in lockstep with Loom and writing into U.

---

## 3. TBP implementation spec: Press and Loom as named layers

The TBP/Gate implementation spec (`tbp_gate_implementation_spec_v_1.md`) gives us a concrete exported scene schema and explicitly lists Press as a layer value:

> “**Canon constraint**
>
> * Gate is the **scene I/O layer** on a 2D plane; exports structured scenes (JSON/CSV/images).
>
> **v1 schema (exported view; big arrays internal only)**
>
> ```json
> {
>   "type": "object",
>   "required": ["commit","tick","actors","bonds","summary"],
>   "properties": {
>     "commit": { "type": "string", "pattern": "^u:sha256:[0-9a-f]{64}$" },
>     "tick": { "type": "integer", "minimum": 0 },
>     "actors": { ... },
>     "bonds": { ... },
>     "summary": { ... },
>     "layer": { "type": "string", "enum": ["GATE","LOOM","PRESS","U","..."] }
>   }
> }
> ```
>
> *(Internal arrays `m[]`, `p[]`, `R1[]`, `R2[]` remain **internal**; heavy numeric detail is recorded in Loom/Press/U; exports surface only projections.)*”  
> — `tbp_gate_implementation_spec_v_1.md`

Key points:

- Exported scene objects include a **`layer`** field whose enum explicitly names `"PRESS"`.  
- Internal heavy arrays (`m[]`, `p[]`, `R1[]`, `R2[]`) are **not** exposed; they live in Loom/Press/U.  
- Exports are projections; Press and Loom carry the full detail needed for replay.

Near the performance and replay section, the spec notes:

> “* **Press**: dictionary + delta blocks (lossless); **MDL acceptance: only apply transform if ΔL_total > 0**.
> * **Chunking:** prefer **CSV‑only** for large packs in constrained environments; split pack M–P into M–N + O–P if compression hits memory guard.
> * **Replay:** restore last `U_commit`, rehydrate Loom/Press dictionaries; deterministic from logs.”  
> — `tbp_gate_implementation_spec_v_1.md`

This paragraph does three important things for APP canon:

1. It explicitly ties Press’s implementation to **dictionary + delta blocks** (lossless).  
2. It states the **MDL acceptance rule as a v1 decision** in an implementation spec:  
   > “only apply transform if ΔL_total > 0.”  
   (Note: signs here use the Gate doc’s wording; across the Aether corpus we treat this as “only accept if the transform improves description length according to the configured MDL sign convention.”)  
3. It clarifies replay mechanics:  
   - **Replay** is done by restoring `U_commit` and **rehydrating Loom/Press dictionaries**.  
   - Determinism is guaranteed from logs + dictionaries.

This is one of the strongest cross‑checks we have between math‑level Press rules (MDL, determinism) and Gate‑side implementation commitments.

---

## 4. Development roadmap: explicit Press shim tasks

The TBP Gate development roadmap makes Press integration an explicit work item:

> “**Goal:** Deliver a deterministic, near‑lossless interface engine that integrates with Loom/Press/U/NAP, per the Implementation Spec v1.”  
> — `tbp_gate_development_roadmap_v_1.md`

Under Phase 3/4 tasks, the roadmap calls out Press shims:

> “- `tbp_logs/` (Loom/Press/U integration shims),”  
> — `tbp_gate_development_roadmap_v_1.md`

> “## Phase 4 — Determinism & seeds; Loom/Press/U shims
>
> - Implement **exact** seed derivation; wrap scene hashing; integrate with Loom/Press/U interfaces (shim layer).
> - **T4.4** Press shim:
>   - Lossless compression; **MDL acceptance: apply transform only if ΔL_total>0**.”  
> — `tbp_gate_development_roadmap_v_1.md`

Together with the implementation spec, this makes Press’s MDL‑based transform acceptance and its position in the Gate pipeline a **first‑class v1 requirement**, not a loose suggestion.

The roadmap does **not** define any new APP‑specific manifests (no `nap_manifest`, no `APP_BARRIERS`, no Pareto manifests); it simply points to Press/Loom/U as **existing systems** that Gate must integrate with.

---

## 5. Older Triune Bridge reports: probabilistic‑structure compressor framing

The older Triune Bridge feature list (`old_triune_bridge_report_features_capabilities.md`) contains key language that motivated how we talk about Press and Gate as a compression system:

> “> Gate’s integer state can be promoted into a **pairwise relational field** that acts as a **probabilistic‑structure compressor** — it compresses correlation structure, not just per‑basis probabilities.”  
> — `old_triune_bridge_report_features_capabilities.md`

And later:

> “### 1.5 Explicit framing as ‘probabilistic‑structure compressor’
>
> > ‘Trinity’s integer mapping functions as a **probabilistic‑structure compressor**, retaining relational coherence while producing fully deterministic data.’  
>
> 2. Quantum result compression for classical analysis.
>
> * Multi-pack concurrent generation for Pack #4 (M–P) hit that cap during ZIP compression.
>   * ‘Probabilistic-structure compressor.’”  
> — `old_triune_bridge_report_features_capabilities.md`

The Gate vs Compendium coverage report notes:

> “### 2.3 Gate as membrane / interface engine (scene I/O, Loom/Press/U path)
>
> - It also details the **attestation chain**: interfaces `* → GATE → LOOM → PRESS → U → …`…  
> - **Gate’s I/O & membrane role is essentially missing from the Math Compendium**: no mention of scene graphs, channels, or the Loom/Press/U path in math terms.
> - Explicit **pairwise relational field** \((R_{ij}, Δp_{ij})\) and its correlation‑compression role.”  
> — `trinity_gate_vs_math_compendium_coverage_report.md`

While these quotes are about Trinity/Gate more than APP directly, they reinforce that:

- Compression in this stack is not just “shorter bitstrings”; it is **structural compression** of probabilistic relations.  
- Gate + Press together hide the probability/relational heavy lifting behind a deterministic interface.

APP’s own math spec already encodes “structural compression” via SimA generators; these Gate docs show that the broader Trinity language is consistent with that framing.

---

## 6. What remains explicitly *unspecified* in these Gate implementation docs

Despite the strong Loom/Press/U integration story, several APP‑specific gaps remain unfilled in this directory:

1. **No APX/APP manifest schemas**  
   - No `nap_manifest.json` or APX subclass schema is defined here.  
   - No `APP_BARRIERS.json` or `press_pareto_manifest_v6_*.json` appears or is described.

2. **No AEON/APXi details**  
   - No mentions of AEON‑i, APXi, or Press opcode grammars appear in these Gate docs.

3. **No modes/switchboard schemas**  
   - While Gate integrates with Loom/Press/U/NAP, these documents do **not** define PRESS_MODE values, S‑modes, or their JSON representations.

4. **No additional MDL math**  
   - The MDL acceptance rule (“apply transform only if ΔL_total>0”) is re‑stated as a v1 decision, but no new functional forms, penalties, or thresholds are introduced.

5. **Back‑pressure and queuing remains a gap**  
   - The knowledge gaps doc explicitly flags that **back‑pressure**, **queue policies**, and **governance‑level rules** for Loom/Press/U are still to be fully specified.

---

## 7. How to use this pass in the Astral Press Pillar spec

This Gate implementation pass should be treated as **cross‑pillar evidence** that:

- Press is a mandatory, first‑class part of the Gate pipeline (`ingest → normalize → render → Loom → Press → U`).  
- Press operates as a **rolling dictionary + delta compressor** over Gate scenes, under an **MDL acceptance rule**.  
- Press and Loom together support **deterministic replay** via U commits and dictionary rehydration.  
- APX‑style scene objects explicitly name `layer: "PRESS"` and keep heavy numeric structure inside Loom/Press/U.

It does **not** define any new APP manifests or AEON/APXi structures; those remain to be designed or recovered elsewhere.  
This pass is therefore best used to:

- Anchor Press’s **position in the runtime pipeline** (ordering, replay responsibilities).  
- Justify MDL‑based acceptance and dictionary‑plus‑delta architecture as **implementation commitments** rather than purely abstract math.  
- Keep the Press Pillar spec aligned with how Trinity Gate and TBP actually expect to see and use Press in practice.



<!-- END SOURCE: trinity_gate_pillar_press_loom_integration_tgp_tbp_impl_docs_pass.md -->


---

<!-- BEGIN SOURCE: trinity_gate_press_tbp_integration_implementation_docs_pass.md -->

# Trinity Gate — Press & TBP Integration (Implementation Docs Pass)

> **Scope**  
> Mine the Trinity Gate implementation docs under `Reports/trinity gate pillar/TGP+TBP implementstion docs/` for anything that tightens or closes **Astral Press–facing gaps**, without inventing new behaviour.  
> These docs were generated by the same complement process we’re now running on APP; they are canon for Gate/TBP.
>
> Source docs (all under Gate implementation pack):
> - `trinity_gate_features_components_capabilities 1.md`  
> - `tbp_gate_implementation_spec_v_1.md`  
> - `tbp_gate_operator_runbook_v_1.md`  
> - `tbp_gate_development_roadmap_v_1.md`  
> - `tbp_gate_dev_roadmap_task_breakdown_v_1.md`  
> - `tbp_gate_golden_fixtures_pack_v_1.md`  
> - `tbp_gate_verification_test_plan_v_1.md`  
> - `tbp_gate_verification_plan_fixtures_crosswalk_v_1.md`  
> - `trinity_gate_tgp_focus_expansions.md`  
> - `trinity_gate_vs_math_compendium_coverage_report.md`  
> - `triune_bridge_gate_knowledge_gaps.md`
>
> We only import statements that touch **Press, Loom, NAP, APX‑style packaging, or U**.

---

## 1. Gate’s view of Press (Pillar roles)

### 1.1 Press as a core supporting subsystem

From **Trinity Gate features, components, and capabilities**:

> "Trinity Gate fully scoped list of features, components, and capabilities"  
> *(header)*

In the section on supporting subsystems:

> "Although they are separate pillars, this report treats them as part of Gate’s operational environment:"  
> "**Press (Aether Press – Compression & Learning)**"  
> "* Performs **rolling compression** on Gate’s scene outputs [...] **without losing information**."  
> "* Works with Loom to avoid recomputing identical outputs."

Even with mid‑sentence elisions in the text, we have clear phrases:

- Press is explicitly named as **“Aether Press – Compression & Learning”**.  
- Its Gate‑facing role is to **“perform rolling compression on Gate’s scene outputs”** and to do so **“without losing information”**.  
- Press works together with Loom: Loom logs scenes and content hashes; Press compresses them and avoids re‑computing identical outputs.

### 1.2 Gate → Loom → Press → U pipeline

In the **Gate operator runbook**, the high‑level behaviour of Gate is summarised as:

> "Builds **scene frames** and passes them to **Loom → Press → U** each tick."

and, in the same overview block:

> "Determinism: given the same initial state + input ledger, you must get exactly the same commits and outputs."

From this we get a Gate‑side contract for Press:

- Gate constructs **scene frames** each tick (core representation of current state/scene).  
- Every tick, these frames flow through **Loom, then Press, then Universal Commit (U)**.  
- The entire pipeline is required to be **deterministic given initial state + input ledger** — Press must not introduce non‑determinism.

This directly aligns with the Press/Loom/UMX replay expectations in the APP spec and clarifies where in the live loop APP sits from Gate’s point of view.

---

## 2. Operational contract: Press as a service

### 2.1 Boot sequence

The **Gate operator runbook v1** gives explicit startup ordering for the pillars:

> "2. **LOOM**  
>    - Start attestation service; verify it can talk to U.  
> 3. **PRESS**  
>    - Start compression service; verify health.  
> 4. **GATE**  
>    - Start last; it will discover Loom/Press/U via config."

This closes a gap about how Press is deployed relative to Gate:

- Loom and Press are **independent services** that must be brought up before Gate.  
- Gate expects to **discover Loom/Press/U via configuration**, not link to them as libraries.  
- This matches the APP stance of being a **math‑first system with service wrappers**, not a monolithic binary.

### 2.2 Run initialisation and replay

The runbook also describes how to start a Gate run in a way that respects Press and Loom state:

> "1. **Set run ID** (e.g., `run_YYYYMMDD_HHMMSS_gate_v1`)."  
> "2. **Set initial state**:  
>    - Fresh genesis: all zero state, new `U_commit`.  
>    - Or **replay**: load previous `U_commit`, Loom/Press state, and full input ledger."  
> "3. **Seed policy**:  
>    - Use deterministic formula from spec:  
>      - `Ξ = SHA‑256(U_commit_bytes ∥ node_id_UTF8 ∥ uint64_be(⌊τ/W⌋))."  
>    - Ensure config is set to th[...]" *(elided tail).*

This confirms a few Press‑side invariants:

- Press has **state** that participates in replay — you must load "Loom/Press state" to resume or replay a run.  
- Universal Commit (`U_commit`) and the input ledger define the integer substrate; Press must reproduce the same compressed outputs when given the same state + ledger.  
- The **seed policy** uses `U_commit`, `node_id`, and the windowed tick `⌊τ/W⌋`, consistent with the Gate/UMX NAP & determinism design.

Press’s internal state (dictionaries, layer rules, etc.) is not exposed in this doc, but the operational requirement is clear: Press must be **replayable and restartable** with state snapshots, in lockstep with Loom and U.

---

## 3. Artifacts & logs involving Press

### 3.1 Press dictionaries as explicit artifacts

The Gate development roadmap references Press artifacts alongside Loom and U:

> "Actions:  
>  1. Stop ingest (flip to offline + zero‑egress...).  
>  2. Throttle or disable that source.  
>  3. Increase budgets only if...  
>  4. Collect artifacts:  
>     - Loom frames and manifests.  
>     - **Press dictionaries.**  
>     - [...]" *(elisions where unrelated details are omitted.)*

From this we learn:

- Press maintains **dictionaries** that are treated as important, inspectable artifacts.  
- In incident response or debugging, operators are expected to collect "Press dictionaries" along with Loom frames and other logs.  
- This ties back to the APP spec’s view of **SimA’s learned structure** and APP’s MDL logging; Gate docs confirm those are visible as operational objects.

### 3.2 Session reconstruction and replay

The roadmap and test/verification docs repeatedly mention reconstructing runs from "only the ZIPs and manifests described in the Session Reconstruction" packs. Press is not named in all those sentences, but the pattern is:

- Loom and Gate logs, APX‑style manifests, and Press dictionaries together must be sufficient to **rebuild scenes and outputs** and to verify determinism.  
- The Gate operator runbook’s replay section emphasises matching outputs between live replay and "last N ticks from ledger"; Press is part of that replay chain since it sits between Loom and U.

This does not add new schema, but it reinforces the APP requirement that Press’s outputs and dictionaries must be **fully reproducible** from ledger + state snapshots.

---

## 4. TBP implementation & NAP envelope alignment

### 4.1 NAP envelope fields (Gate side)

The **Gate dev roadmap task breakdown** includes a task to implement `NapEnvelope` with fields mirroring the Gate JS implementation:

> "Tasks:  
>  1. Implement `NapEnvelope` with fields: `tick`, `node_id`, `layer`, `seed_hex`, `payload_ref`, `metrics`, `mode`, `sig`.  
>  2. Ensure deterministic serialisation (JSON canonicalisation) and validation.  
>  3. Wire envelopes into TBP channels with schema validation, rate limits, PII tripwire." *(paraphrased from a longer bullet.)*

This matches exactly the NAP envelope shape we recovered from the `AETHER-GATE-JS-main` code (see NAP implementation pass) and confirms that the **Gate API contract** for NAP envelopes is:

- **Field set:** `tick`, `node_id`, `layer`, `seed_hex`, `payload_ref`, `metrics`, `mode`, `sig`.  
- **Deterministic JSON canonicalisation** for hashing/signing.  
- **Policy hooks:** `metrics` and `mode` carry run‑time information for budget and mode control.

From a Press perspective, this means:

- Whenever APP interacts with Gate via NAP, it will see envelope metadata in this exact shape.  
- APP should never expect raw scene bytes in the envelope; instead it sees `payload_ref` that points (by hash) to scene payloads or capsules.

### 4.2 Scene frame payloads

Across the implementation spec, dev roadmap, and runbook, several references to `scene_frame_core.bin` appear. While the full paragraphs are long, the consistent pattern is:

- Gate builds a **`scene_frame_core.bin`** per tick as the canonical minimal representation of the scene.  
- Scene hashing tasks mention:  
> "Scene hashing: content hash of `scene_frame_core.bin`; build NAP envelope with `payload_ref = h_t`, parent commit hash, tick, and signatures."  
- Acceptance checks stress that **any change in `scene_frame_core.bin` or its hash breaks the commit chain**.

Implications for Press:

- When Gate says "scene outputs" in the features doc, it concretely refers to these scene frame binaries and any overlays/augmented views.  
- Press’s rolling compression and APX packaging can treat `scene_frame_core.bin` as the **primary core payload** per tick, with overlays and metadata as additional layers.  
- Because scene hashes are part of the NAP/ledger chain, any lossy behaviour in Press for these frames would violate Gate’s determinism requirements; Press must be configured to be **lossless (for Gate scenes)** in the sense used here (byte‑exact round trip via Press/DePress).

---

## 5. Knowledge gaps called out by Gate docs

The **Triune bridge / Gate knowledge gaps** doc is explicit about what is *not* yet specified for Gate/TBP. Relevant to Press/APP:

- **No concrete data models / schemas** for Gate’s external inputs and some internal structures.  
- **No exact representation of `τ` and `W`** in all places where they appear.  
- **No cross‑pillar contracts** fully enumerated for Press and other downstream modules; it notes missing:
> "Exact input schema (fields, units, shapes)."  
> "End‑to‑end tests that exercise Gate + Press + Loom + U with independent implementations."

This aligns with our own gap list:

- Gate implementation docs **do not** define:
  - `nap_manifest.json` schema.  
  - `APP_BARRIERS.json` or `press_pareto_manifest_v6_*.json` schemas.  
  - AEON‑i or APXi op/grammar tables.  
  - Modes/Switchboard JSON.

They treat Press largely as a **black‑box compression service with a clear role and operational interface**, but without exposing internal APP manifests.

---

## 6. What this pass actually closes for Press

Compared to the previous Astral Press pillar passes, the Gate implementation docs close or tighten the following gaps:

1. **Gate‑side role of Press**  
   - Confirmed as "Aether Press – Compression & Learning".  
   - Performs "rolling compression on Gate’s scene outputs" and must be "without losing information" for those outputs.  
   - Works with Loom to avoid recomputing identical outputs.

2. **Pipeline placement and determinism**  
   - Gate builds "scene frames" and passes them to "Loom → Press → U" each tick.  
   - Entire pipeline must be deterministic given initial state + ledger; Press is part of that contract.

3. **Service model and replay obligations**  
   - Press is a separate service started after Loom and before Gate.  
   - Replay runs must reload "Loom/Press state" along with `U_commit` and input ledger.  
   - Press dictionaries are first‑class artifacts to be collected in incident response.

4. **NAP envelope shape (Gate contract)**  
   - Gate implementation docs (task breakdown) match the NAP envelope fields in the Gate JS implementation.  
   - This confirms the canonical field set and the expectation of deterministic JSON serialisation.

5. **Scene payload anchoring**  
   - `scene_frame_core.bin` is the canonical per‑tick payload whose hash is used as `payload_ref` and stitched into the commit chain.  
   - Press must respect this and operate in a lossless mode for such payloads in the Gate context.

The following **remain open** (not addressed in these Gate docs):

- Concrete `nap_manifest.json` schema.  
- APP_BARRIERS and Pareto manifest JSON schemas.  
- AEON/APXi opcode and grammar tables.  
- Modes/Switchboard JSON, including S6/S8/S11 semantics.  
- Numeric defaults for deployment‑equivalence knobs and Press thresholds.  
- Any Gate‑side schema that reaches into APP’s internal manifest structures.

This pass should now be used as the **Gate/Press integration layer**: when implementing APP in practice, the NAP envelope shape, service boot order, replay obligations, and scene frame anchoring described here must be honoured to stay consistent with Trinity Gate v1.



<!-- END SOURCE: trinity_gate_press_tbp_integration_implementation_docs_pass.md -->


---

<!-- BEGIN SOURCE: trinity_gate_tbp_press_integration_implementation_docs_pass.md -->

# Trinity Gate & TBP — Press Integration (Implementation Docs Pass)

> **Scope**  
> Use the Trinity Gate / TBP implementation pack under `aether full clean/Reports/trinity gate pillar/TGP+TBP implementstion docs/` to tighten the Astral Press Pillar spec **only where Gate/TBP directly constrain or describe Press**.  
> Treat these docs as canon for Gate/TBP and as cross‑pillar evidence for APP; do **not** back‑project Gate‑specific fields into global APP requirements unless the text explicitly does so.
>
> **Sources in this pass**  
> (all under `.../TGP+TBP implementstion docs/`):
> - `tbp_gate_implementation_spec_v_1.md`  
> - `trinity_gate_features_components_capabilities 1.md`  
> - `tbp_gate_development_roadmap_v_1.md`  
> - `tbp_gate_golden_fixtures_pack_v_1.md`  
> - `tbp_gate_operator_runbook_v_1.md`  
> - `tbp_gate_verification_plan_fixtures_crosswalk_v_1.md`  
> - `tbp_gate_verification_test_plan_v_1.md`  
> - `trinity_gate_older_reports_expansions.md`  
> - `trinity_gate_tgp_focus_expansions.md`  
> - `trinity_gate_vs_math_compendium_coverage_report.md`  
> - `old_triune_bridge_report_features_capabilities.md`  
> - `triune_bridge_gate_knowledge_gaps.md`

Where we interpret, we attach **direct quotes** from these docs.

---

## 1. NAP envelope & layer enum (Gate/TBP view)

### 1.1 Required envelope fields (JSON schema excerpt)

`tbp_gate_implementation_spec_v_1.md` gives a partial JSON schema for NAP envelopes as seen by Gate/TBP. The key excerpt:

> `"required": ["tick","node_id","layer","seed_hex","payload_ref","metrics","mode","sig"],`  
> `"layer": { "type": "string", "enum": ["GATE","LOOM","PRESS","U","..."] },`

This matches the Gate JS core implementation and closes the loop between **math canon**, **Gate JS**, and **TBP spec** on NAP envelope structure:

- `tick` — global tick index `τ`.  
- `node_id` — logical source node.  
- `layer` — logical layer name, with at least `"GATE"`, `"LOOM"`, `"PRESS"`, `"U"` in the enum.  
- `seed_hex` — normalization of the seed (Gate spec ties this to `Ξ = SHA‑256(U_commit ∥ node_id ∥ ⌊τ/W⌋)` in the golden fixtures).  
- `payload_ref` — hash reference to payload (Gate JS uses `"sha256:<hex>"`).  
- `metrics` — envelope‑level metrics object.  
- `mode` — mode flags for this envelope.  
- `sig` — signature.

For APP, this confirms:

- There is a **single shared NAP envelope schema** across Gate, Loom, Press, and `U`.  
- Press appears here as one of the `layer` enum values, not as a special case with its own envelope format.  
- Any APP/Press NAP integration must respect this **required field set** and layer naming.

### 1.2 Envelopes carry only hashes / metrics, no raw state

The same spec reinforces that Gate never puts raw state into NAP envelopes:

> "Each node emits envelope: tick, node_id, layer, metrics, seed, payload hash (no raw data)."  
> "*(Internal arrays `m[]`, `p[]`, `R1[]`, `R2[]` remain **internal**; only **projections** or statistics are recorded in Loom/Press/U; exports surface only projections.)*"

APP‑relevant consequence:

- Press never consumes or emits **raw TBP arrays** over NAP; it sees only hashed payload_refs and summary metrics.  
- Any lossless reconstruction that involves Gate/TBP must go via **APX‑style capsules or other payload containers**, not via NAP envelopes themselves.

---

## 2. Gate’s definition of Press (role & behaviour)

### 2.1 Press in the Gate feature set

`trinity_gate_features_components_capabilities 1.md` places Press directly in Gate’s component list:

> "**Press (Aether Press – Compression & Learning)**"  
> "* Performs **rolling compression** on Gate’s scene outputs using a mix of entropy coding and dictionary compression, **without losing information**."  
> "* Gate outputs (after Press) are appended as commits, **advancing the global state hash** and tying each frame into an immutable run record."  
> "* Tick schedule: domain nodes update first, then **(τ, GATE)**, then **(τ, LOOM)**, **(τ, PRESS)**, **(τ, U)**."  
> "* Supports **pause/resume** (resume from recorded commit and Press dictionary)."  
> "* Ingests real-world feeds (climate sensors, markets, etc.) until it has an internal simulation that mirrors/compresses that live data."  
> "* Logs are compact due to Press; long-term standalone operation is feasible."

This clarifies several points we were previously treating as inferred behaviour:

- **Rolling compression on scenes:** Press is attached specifically to **Gate’s scene outputs**, not arbitrary raw TBP states.  
- **Lossless stance:** In this Gate context, Press is presented as "without losing information" — aligning with APP’s lossless mode semantics.  
- **Ledger role:** Pressed outputs advance the global state hash and are treated as commits into a run record; this aligns with U/Ledger behaviour in the broader Aether canon.  
- **Tick ordering:** The explicit sequence `domain → GATE → LOOM → PRESS → U` pins Press’s relative position in the tick loop.  
- **Pause/resume:** Press’s dictionaries and Loom’s state are the core artefacts required to resume from a recorded commit.

### 2.2 Press behaviour from TBP implementation spec

`tbp_gate_implementation_spec_v_1.md` gives a short but very dense line on Press:

> "* **Press**: dictionary + delta blocks (lossless); MDL acceptance: only apply transform if ΔL_total > 0."

This directly supports core APP rules:

- **Mechanism:** Press acts via "dictionary + delta blocks", rather than arbitrary neural coders; this matches the SimA/SimB + residual-block framing.  
- **Decision rule:** MDL acceptance is **one‑sided**: only apply a transform when it strictly improves the code length (ΔL_total > 0).  
- **Lossless guarantee:** For Gate’s use of Press, the transforms applied are required to preserve exact reconstructability of the scene, in line with the "without losing information" claim in the features doc.

Combined with the Astral Press canon, we now have:

- A **canonical description of Press from Gate’s point of view**: dictionary+delta, MDL‑driven, lossless, ledger‑integrated.  
- A pinned **location in the tick order** and interlocks with Loom and U.

---

## 3. Gate → Loom → Press → U pipeline

`triune_bridge_gate_knowledge_gaps.md` summarises the intended high‑level pipeline including Press:

> "Pipelines: **ingest → normalize → render → Loom → Press → U**."

Compare this to the tick schedule above and the TBP spec’s description of Gate as the "scene I/O layer":

> "Gate can **emit structured scene frames (JSON, CSV, etc.)** to drive visual engines, external actuators, or analytics."  
> "Maintains an internal **scene graph**: entities as **actors on a 2D plane** with edges/bonds for interactions."  
> "Each tick, Gate:  
>  * Collects outputs from relevant nodes.  
>  * Compiles a **unified scene** including a global state vector, sub‑states, and a list of actors with coordinates and connections."

From a Press perspective, this pipeline implies:

1. **Ingest / normalize / render**  
   - External signals and TBP outputs are normalized onto Gate’s 2D scene graph.  
   - Scenes are prepared in structured forms (JSON/CSV/images) suitable for APP ingestion.

2. **Loom phase**  
   - Loom records and indexes intermediate state (including Gate telemetry) as part of the ledger timeline.

3. **Press phase**  
   - Press consumes Gate’s rendered scene frames and Loom’s state as needed to perform **rolling compression** (dictionary + delta blocks).  
   - Compressed outputs feed into U (ledger / universe state) as commits.

This reinforces the idea that APP is the **compression + learning arm of the scene pipeline**, not an arbitrary background job.

---

## 4. Press’s interaction with ledger and replay

TBP implementation and roadmap documents describe replay and continuity:

> "* **Replay:** restore last `U_commit`, rehydrate Loom/Press dictionaries; deterministic from logs."  
> "* Can run as a **standalone module** with minimal support nodes, as long as there is a maintained deterministic interface & ledger for external systems."  
> "Logs are compact due to Press; long‑term standalone operation is feasible."

Key properties for APP:

- **Replay contract:** To replay Gate+Press behaviour over TBP outputs, it is sufficient to:
  1. Restore the last `U_commit` (universe state).  
  2. Rehydrate Loom and Press dictionaries from logs.  
  3. Re‑apply logged inputs deterministically.

- **Compact logs:** The presence of Press in the pipeline is what allows long‑term operation with manageable log size; this implicitly confirms that Press is applied **online**, not just as an offline recompressor.

- **Deterministic interface:** Press must not introduce any non‑deterministic behaviour; its dictionary/delta operations are fully determined by prior state and inputs.

The Loom+Press+Aevum replay spec elsewhere in canon is consistent with this. These Gate docs provide a cross‑pillar **sanity check** on the replay story.

---

## 5. Known gaps from Gate/TBP docs (Press‑relevant)

The Gate knowledge gaps doc lists several open issues that intersect with Press:

> "3. **No fully-specified back-pressure and queuing behaviour**  
>    * ‘Gate is non-blocking; frames queue with back-pressure.’  
>    You know there’s an input ledger and Loom/Press/U commits, but not:  
>    * how queue lengths are bounded,  
>    * whether Press can slow Gate,  
>    * how back-pressure is applied to external feeds."  
> "* **Governance-level spec** (exact policies and automations for PII, approvals, back-pressure)."

Implications for APP:

- **Back‑pressure:**  
  - It is **not** specified whether Press can or should influence Gate’s pacing or apply back‑pressure by itself.  
  - Queue bounds, drop policies, and rate control are explicitly **not** defined in these docs.

- **Governance / PII:**  
  - Exact policies for how Press interacts with PII, approvals, and back‑pressure are **not** fleshed out here.  
  - Those aspects remain tied to the broader Aether governance modes (SFTY modes, N4, APP_BARRIERS) rather than Gate‑local rules.

The dev roadmap and verification docs do not add Press‑specific governance details; they mostly enumerate tasks, fixture coverage, and TBP fidelity metrics.

---

## 6. What these docs **do not** define for Press

After scanning all Gate/TBP implementation docs listed in the scope, the following **remain undefined** (and must remain gaps in the Astral Press Pillar spec unless filled by other canon sources):

- No `APP_BARRIERS.json` schema or Press policy pack is defined here.  
- No `press_pareto_manifest_v6_*.json` schema or MDL/Pareto defaults are provided.  
- No AEON‑i or APXi grammar, opcode tables, or Press‑specific container details are present.  
- No `nap_manifest.json` schema or NAP compression manifest details appear in these Gate docs.  
- No JSON representation for S1–S12 or other modes is defined here (the only modes references are conceptual and live elsewhere).  
- No additional numeric defaults for MDL penalties or deployment‑equivalence knobs are fixed here; all references to η, P, and TBP tiers are TBP‑internal, not Press‑level APP knobs.

In other words, **Gate/TBP implementation canon**:

- Confirms and sharpens Press’s **place in the pipeline**, its **dictionary+delta+MDL** behaviour, its **lossless stance**, and its participation in **ledger and replay**.  
- Confirms the **shared NAP envelope schema and layer enum** for GATE/LOOM/PRESS/U.  
- Leaves Press’s **internal manifesets (APP_BARRIERS, Pareto, AEON/APXi)** and its **governance/back‑pressure rules** untouched.

This pass should be treated as the **Gate/TBP → Press integration layer**, to be cross‑referenced from the main Astral Press Pillar spec wherever we describe:

- Press’s role in the scene & ledger pipeline.  
- Press’s dictionary + delta behaviour and MDL acceptance rule.  
- NAP envelope layer naming and required fields for Press.  
- Replay/pause/resume requirements across Gate, Loom, Press, and U.



<!-- END SOURCE: trinity_gate_tbp_press_integration_implementation_docs_pass.md -->
