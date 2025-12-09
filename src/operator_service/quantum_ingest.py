"""Quantum ingestion helpers for statevector loading and TBP quantization.

The goal is to keep Phase 8 work self-contained and offline-friendly while
we wait for upstream engine hooks. Functions here intentionally avoid heavy
dependencies so they can run in constrained environments.
"""
from __future__ import annotations

import cmath
import json
import math
import random
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

from core.tick_loop import TickLoopWindowSpec, run_cmp0_tick_loop
from gate.gate import PFNAIngressQueue, PFNAInputV0, PFNATransformV1
from umx.profile_cmp0 import gf01_profile_cmp0
from umx.topology_profile import gf01_topology_profile


def load_statevector(input_path: Optional[Path] = None, *, qubits: int = 2) -> Tuple[List[complex], str]:
    """Load or synthesize a quantum statevector.

    - If ``input_path`` is provided, the loader expects a JSON array of complex
      amplitudes. Each entry may be a complex number encoded as ``[real, imag]``
      or a plain float (interpreted as a real amplitude).
    - If no path is supplied, a normalized Bell state |00> + |11> is returned
      with a brief source hint.
    - The vector is normalized to unit length to avoid propagation of invalid
      inputs.
    """

    if input_path:
        raw = json.loads(Path(input_path).read_text())
        amplitudes: List[complex] = []
        for entry in raw:
            if isinstance(entry, complex):
                amplitudes.append(entry)
            elif isinstance(entry, (list, tuple)) and len(entry) == 2:
                amplitudes.append(complex(float(entry[0]), float(entry[1])))
            elif isinstance(entry, (int, float)):
                amplitudes.append(complex(float(entry), 0.0))
            else:
                raise ValueError("statevector entries must be complex encodings [real, imag] or floats")
        source = f"loaded:{input_path}"
    else:
        width = max(int(qubits or 2), 2)
        size = 2**width
        amp = 1 / math.sqrt(size)
        amplitudes = [amp] * size
        source = f"synthetic:superposition(qubits={width})"

    normalized = _normalize_statevector(amplitudes, expected_qubits=qubits)
    return normalized, source


def quantize_with_auto_tune(statevector: List[complex], params: Dict[str, object]):
    """Quantize a statevector while filling η/P defaults via heuristics."""

    auto_tune = bool(params.get("auto_tune", False))
    qubits = int(params.get("qubits", 2))
    user_eta = params.get("eta") if "eta" in params else None
    user_phase_bins = params.get("phase_bins") if "phase_bins" in params else None
    tune_notes: List[str] = []

    eta = user_eta
    phase_bins = user_phase_bins
    if auto_tune and (user_eta is None or user_phase_bins is None):
        tuned = auto_tune_quantization(
            statevector,
            qubits=qubits,
            eta_hint=user_eta,
            phase_bins_hint=user_phase_bins,
        )
        eta = tuned["eta"]
        phase_bins = tuned["phase_bins"]
        tune_notes = tuned.get("notes", [])

    eta = float(eta if eta is not None else params.get("eta"))
    phase_bins = int(phase_bins if phase_bins is not None else params.get("phase_bins"))

    encoded = quantize_statevector(statevector, eta=eta, phase_bins=phase_bins)
    fidelity = compute_fidelity_metrics(statevector, encoded)
    params["eta"] = eta
    params["phase_bins"] = phase_bins
    return encoded, fidelity, tune_notes


def auto_tune_ingestion_params(params: Dict[str, object]) -> Dict[str, object]:
    """Fill in missing eta/P values using heuristics and capture notes."""

    params = dict(params)
    auto_tune = bool(params.get("auto_tune", False))
    eta = params.get("eta")
    phase_bins = params.get("phase_bins")
    if not auto_tune or (eta is not None and phase_bins is not None):
        return params

    qubits = int(params.get("qubits", 2))
    input_path = params.get("input")
    statevector, source = load_statevector(Path(input_path) if input_path else None, qubits=qubits)
    tuned = auto_tune_quantization(
        statevector,
        qubits=qubits,
        eta_hint=eta if isinstance(eta, (int, float)) else None,
        phase_bins_hint=phase_bins if isinstance(phase_bins, int) else None,
    )
    params["eta"] = tuned.get("eta", eta)
    params["phase_bins"] = tuned.get("phase_bins", phase_bins)
    params["input_source"] = params.get("input_source") or source

    notes = list(params.get("tuning_notes", []))
    for note in tuned.get("notes", []):
        if note not in notes:
            notes.append(note)
    if notes:
        params["tuning_notes"] = notes

    return params


def quantize_statevector(statevector: Iterable[complex], *, eta: float, phase_bins: int) -> Dict[str, object]:
    """Quantize a statevector into TBP (mass, phase, residual) format.

    This follows the Trinity Gate L0 encoding described in the Quantum Ingest
    issue pack. The function is intentionally dependency-light and returns a
    serializable dictionary ready for persistence or transport.
    """

    masses: List[int] = []
    phases: List[int] = []
    residuals: List[int] = []

    for amp in statevector:
        probability = abs(amp) ** 2
        scaled = eta * probability
        mass = math.floor(scaled)
        masses.append(mass)

        phase = _quantize_phase(amp, phase_bins)
        phases.append(phase)

        residual = math.floor((scaled - mass) * (2**32))
        residuals.append(residual)

    return {
        "masses": masses,
        "phases": phases,
        "residuals": residuals,
        "eta": eta,
        "P": phase_bins,
    }


def compute_fidelity_metrics(statevector: Iterable[complex], encoded: Dict[str, object]) -> Dict[str, float]:
    """Approximate fidelity between the input and quantized payload.

    Returns a lightweight pair of metrics:

    - ``prob_l1``: L1 distance between input probabilities and reconstructed
      probabilities from TBP masses/residuals.
    - ``amp_l2``: L2 distance between the original amplitudes and an
      approximate reconstruction using quantized phases.
    """

    approximate, approx_probs = _reconstruct_statevector(encoded)
    original = list(statevector)
    if len(original) != len(approximate):
        raise ValueError("statevector length mismatch during fidelity calculation")

    prob_l1 = 0.0
    amp_l2_accum = 0.0
    for original_amp, prob_hat, approx_amp in zip(original, approx_probs, approximate):
        prob_l1 += abs(abs(original_amp) ** 2 - prob_hat)
        amp_l2_accum += abs(original_amp - approx_amp) ** 2

    return {
        "prob_l1": prob_l1,
        "amp_l2": math.sqrt(amp_l2_accum),
    }


def auto_tune_quantization(
    statevector: Iterable[complex],
    *,
    qubits: int,
    eta_hint: Optional[float] = None,
    phase_bins_hint: Optional[int] = None,
    min_phase_bins: int = 32,
    max_phase_bins: int = 1024,
) -> Dict[str, object]:
    """Choose η and P heuristically when callers omit them.

    The heuristic aims to:
    - scale the largest probability mass to a configurable target so integer
      masses retain meaningful signal even for small amplitudes, and
    - pick a power-of-two phase bucket count large enough to reflect the
      observed phase diversity without inflating payload size.

    Hints are honored when provided so explicit caller inputs always win.
    """

    amplitudes = list(statevector)
    probs = [abs(val) ** 2 for val in amplitudes]
    max_prob = max(probs) if probs else 0.0
    notes: List[str] = []

    eta = eta_hint
    if eta is None:
        target_mass = 10_000 * max(1, qubits)
        if max_prob > 0:
            eta = max(target_mass / max_prob, 1_000.0)
            notes.append(
                f"auto-tuned eta to {eta:.0f} to target masses near {target_mass} (max_prob={max_prob:.4f})"
            )
        else:
            eta = 1_000_000.0
            notes.append("auto-tuned eta fallback to 1e6 (empty probabilities)")

    phase_bins = phase_bins_hint
    if phase_bins is None:
        # Estimate a reasonable bin count from observed phases and qubit width.
        rough_bins = max(qubits * 8, min_phase_bins)
        observed_bins = len(
            {
                int(
                    math.floor(
                        ((cmath.phase(val) % (2 * math.pi)) / (2 * math.pi)) * max_phase_bins
                    )
                )
                for val in amplitudes
                if val != 0
            }
        )
        desired = max(rough_bins, observed_bins * 2)
        power = max(min_phase_bins, 1 << math.ceil(math.log2(max(desired, 1))))
        phase_bins = min(max(power, min_phase_bins), max_phase_bins)
        notes.append(
            f"auto-tuned P to {phase_bins} based on qubits={qubits} observed_phase_bins={observed_bins}"
        )

    return {"eta": float(eta), "phase_bins": int(phase_bins), "notes": notes}


def _quantize_phase(amp: complex, phase_bins: int) -> int:
    # Normalize angle to [0, 2π) then bin into P buckets.
    theta = cmath.phase(amp) % (2 * math.pi)
    bucket = int(math.floor((theta / (2 * math.pi)) * phase_bins)) % max(phase_bins, 1)
    return bucket


def _normalize_statevector(raw: List[complex], *, expected_qubits: int) -> List[complex]:
    if not raw:
        raise ValueError("statevector is empty")

    norm = math.sqrt(sum(abs(val) ** 2 for val in raw))
    if norm == 0:
        raise ValueError("statevector has zero norm")

    normalized = [val / norm for val in raw]
    expected_length = 2**expected_qubits
    if len(normalized) != expected_length:
        raise ValueError(f"statevector length {len(normalized)} does not match qubits={expected_qubits}")
    return normalized


def simulate_preset_statevector(
    circuit: str,
    *,
    qubits: int = 2,
    layers: int = 1,
) -> Tuple[List[complex], str]:
    """Generate lightweight preset circuits without external deps."""

    circuit = (circuit or "bell").lower()
    if circuit == "bell":
        base = [1 / math.sqrt(2), 0, 0, 1 / math.sqrt(2)]
        state = _normalize_statevector(base, expected_qubits=max(qubits, 2))
        return state, "bell entanglement"

    if circuit.startswith("ghz"):
        width = qubits or 4
        on_state = (2**width) - 1
        state = [0j] * (2**width)
        amp = 1 / math.sqrt(2)
        state[0] = amp
        state[on_state] = amp
        return state, f"ghz(q={width})"

    if circuit.startswith("qft"):
        width = qubits or 4
        size = 2**width
        state = [cmath.exp(2j * math.pi * k / size) / math.sqrt(size) for k in range(size)]
        return state, f"qft(q={width})"

    if circuit == "random_clifford":
        width = qubits or 3
        rng = random.Random(width + layers)
        size = 2**width
        phases = [rng.choice([1j, -1j, 1, -1]) for _ in range(size)]
        magnitudes = [1 / math.sqrt(size)] * size
        state = [mag * phase for mag, phase in zip(magnitudes, phases)]
        return _normalize_statevector(state, expected_qubits=width), f"random_clifford(q={width},seed={width+layers})"

    # Fallback to a balanced superposition if the circuit is unknown.
    width = max(qubits or 2, 2)
    size = 2**width
    amp = 1 / math.sqrt(size)
    state = [amp] * size
    return state, f"superposition(q={width})"


def run_experiment_statevector(
    name: str,
    *,
    qubits: int = 4,
    ticks: int = 4,
    episodes: int = 1,
) -> Tuple[List[complex], str]:
    """Approximate a lightweight experiment (e.g., spin chain) state."""

    width = max(qubits or 4, 2)
    size = 2**width
    base_amp = 1 / math.sqrt(size)
    # Modulate phases along the chain to mimic evolution across ticks/episodes.
    phase_step = (episodes + ticks) / max(size, 1)
    state = [base_amp * cmath.exp(1j * phase_step * idx) for idx in range(size)]
    label = f"{name or 'spin_chain'}(q={width},ticks={ticks},episodes={episodes})"
    return _normalize_statevector(state, expected_qubits=width), label


def _reconstruct_statevector(encoded: Dict[str, object]) -> Tuple[List[complex], List[float]]:
    masses = encoded.get("masses", [])
    phases = encoded.get("phases", [])
    residuals = encoded.get("residuals", [])
    eta = float(encoded.get("eta", 1))
    phase_bins = int(encoded.get("P", 1))

    approximate: List[complex] = []
    approx_probs: List[float] = []
    two_pi = 2 * math.pi
    bin_width = two_pi / max(phase_bins, 1)

    for mass, phase, residual in zip(masses, phases, residuals):
        prob_hat = (float(mass) + float(residual) / (2**32)) / eta
        approx_probs.append(prob_hat)

        magnitude = math.sqrt(max(prob_hat, 0.0))
        # Use the center of the bucket for reconstruction to avoid biasing to edges.
        angle = bin_width * (float(phase) + 0.5)
        approximate.append(magnitude * cmath.exp(1j * angle))

    return approximate, approx_probs


def tbp_to_pfna_inputs(
    encoded: Dict[str, object],
    *,
    pfna_id: str = "tbp_ingest",
    gid: str = "GATE",
    run_id: str = "SESSION",
    nid: str = "quantum",
    tick: int = 0,
) -> Tuple[PFNAInputV0, ...]:
    """Convert TBP payloads into PFNA inputs for Gate harness replay."""

    masses = encoded.get("masses", [])
    phases = encoded.get("phases", [])
    residuals = encoded.get("residuals", [])
    eta = float(encoded.get("eta", 0))
    phase_bins = int(encoded.get("P", 0))

    if not (isinstance(masses, list) and isinstance(phases, list) and isinstance(residuals, list)):
        raise ValueError("encoded TBP payload must contain list fields for masses, phases, residuals")
    if not masses:
        raise ValueError("encoded TBP payload has no masses to convert to PFNA inputs")
    if not (len(masses) == len(phases) == len(residuals)):
        raise ValueError("encoded TBP payload lists must share the same length")

    base_kwargs = {"gid": str(gid), "run_id": str(run_id), "nid": str(nid)}
    masses_input = PFNAInputV0(
        pfna_id=f"{pfna_id}:masses",
        tick=int(tick),
        values=tuple(int(mass) for mass in masses),
        description=f"TBP masses; eta={eta:g} P={phase_bins}",
        **base_kwargs,
    )
    residuals_input = PFNAInputV0(
        pfna_id=f"{pfna_id}:residuals",
        tick=int(tick),
        values=tuple(int(residual) for residual in residuals),
        description="TBP residuals scaled to 2^32",
        **base_kwargs,
    )
    phases_input = PFNAInputV0(
        pfna_id=f"{pfna_id}:phases",
        tick=int(tick),
        values=tuple(int(phase) for phase in phases),
        description=f"TBP phase bins (P={phase_bins})",
        **base_kwargs,
    )

    return (masses_input, residuals_input, phases_input)


def tbp_to_pfna_bundle(
    encoded: Dict[str, object],
    *,
    pfna_id: str = "tbp_ingest",
    gid: str = "GATE",
    run_id: str = "SESSION",
    nid: str = "quantum",
    tick: int = 0,
) -> Dict[str, object]:
    """Build a PFNA V0 bundle from TBP payloads for file-based ingestion."""

    inputs = tbp_to_pfna_inputs(
        encoded, pfna_id=pfna_id, gid=gid, run_id=run_id, nid=nid, tick=tick
    )
    return {
        "v": 0,
        "pfna_id": pfna_id,
        "gid": gid,
        "run_id": run_id,
        "nid": nid,
        "entries": [
            {
                "pfna_id": item.pfna_id,
                "tick": item.tick,
                "values": list(item.values),
                "description": item.description,
            }
            for item in inputs
        ],
    }


def replay_tbp_as_pfna_events(
    encoded: Dict[str, object],
    *,
    pfna_id: str = "tbp_ingest",
    gid: str = "GATE",
    run_id: str = "SESSION",
    nid: str = "quantum",
    tick: int = 0,
    transform: PFNATransformV1 | None = None,
):
    """Quantize TBP payloads into PFNA ingress events using the Gate shim.

    This mirrors the path a Gate harness would follow when loading PFNA bundles:
    TBP -> PFNA V0 inputs -> PFNA ingress queue -> integerized events. The helper
    returns the ready-to-consume events for the requested tick so callers can
    inspect integerized values without wiring a full engine run.
    """

    inputs = tbp_to_pfna_inputs(
        encoded, pfna_id=pfna_id, gid=gid, run_id=run_id, nid=nid, tick=tick
    )
    queue = PFNAIngressQueue(transform=transform)
    queue.extend(inputs)
    return queue.pop_ready(tick)


def summarize_pfna_replay(
    encoded: Dict[str, object],
    *,
    pfna_id: str = "tbp_ingest",
    gid: str = "GATE",
    run_id: str = "SESSION",
    nid: str = "quantum",
    tick: int = 0,
    transform: PFNATransformV1 | None = None,
) -> Dict[str, object]:
    """Replay TBP payloads through PFNA ingress and compute simple metrics."""

    events = replay_tbp_as_pfna_events(
        encoded,
        pfna_id=pfna_id,
        gid=gid,
        run_id=run_id,
        nid=nid,
        tick=tick,
        transform=transform,
    )
    if not events:
        return {"events": 0, "values": 0, "clamped": 0}

    integerized = [val for event in events for val in event.integerized]
    audits = [audit for event in events for audit in event.audit]
    clamped = sum(1 for audit in audits if audit.get("clamped") != audit.get("rounded"))
    summary: Dict[str, object] = {
        "events": len(events),
        "values": len(integerized),
        "clamped": clamped,
    }

    if integerized:
        summary.update(
            {
                "min": min(integerized),
                "max": max(integerized),
                "mean": sum(integerized) / len(integerized),
            }
        )

    return summary


def summarize_gate_pfna_replay(
    encoded: Dict[str, object],
    *,
    pfna_id: str = "tbp_ingest",
    gid: str | None = None,
    run_id: str = "SESSION",
    nid: str = "quantum",
    tick: int = 1,
    transform: PFNATransformV1 | None = None,
) -> Dict[str, object]:
    """Run PFNA replay through the Gate harness to sanity-check payloads.

    This feeds the quantized TBP payload into the cmp0 tick loop using the
    standard gf01 topology/profile so we can observe integerized values and
    clamp counts inside a realistic execution context. The summary mirrors
    ``summarize_pfna_replay`` but leverages the full harness instead of the
    ingress queue alone.
    """

    transform = transform or PFNATransformV1()
    topo = gf01_topology_profile()
    gid = topo.gid
    pfna_inputs = tbp_to_pfna_inputs(
        encoded, pfna_id=pfna_id, gid=gid, run_id=run_id, nid=nid, tick=tick
    )

    adjusted_inputs: list[PFNAInputV0] = []
    for item in pfna_inputs:
        values = tuple(item.values)
        if len(values) < topo.N:
            values = values + (0,) * (topo.N - len(values))
        elif len(values) > topo.N:
            values = values[: topo.N]
        adjusted_inputs.append(
            PFNAInputV0(
                pfna_id=item.pfna_id,
                gid=gid,
                run_id=run_id,
                tick=item.tick,
                nid=item.nid,
                values=values,
                description=item.description,
            )
        )

    queue = PFNAIngressQueue(transform=transform)
    queue.extend(adjusted_inputs)
    events = queue.pop_ready(tick)
    integerized = [val for event in events for val in event.integerized]
    audits = [audit for event in events for audit in event.audit]
    clamped = sum(1 for audit in audits if audit.get("clamped") != audit.get("rounded"))

    summary: Dict[str, object] = {
        "events": len(events),
        "values": len(integerized),
        "clamped": clamped,
    }
    if integerized:
        summary.update(
            {
                "min": min(integerized),
                "max": max(integerized),
                "mean": sum(integerized) / len(integerized),
            }
        )

    profile = gf01_profile_cmp0()
    window_spec = TickLoopWindowSpec(
        window_id="GATE_CMP0_TICKS_1_2",
        apx_name="GATE_CMP0_TICKS_1_2",
        start_tick=tick,
        end_tick=tick + 1,
    )

    result = run_cmp0_tick_loop(
        topo=topo,
        profile=profile,
        initial_state=[0 for _ in range(topo.N)],
        total_ticks=window_spec.end_tick,
        window_specs=[window_spec],
        primary_window_id=window_spec.window_id,
        run_id=run_id,
        nid=nid,
        pfna_inputs=tuple(adjusted_inputs),
        pfna_transform=transform,
    )

    scenes = getattr(result, "scenes", ()) or ()
    pfna_meta = []
    for scene in scenes:
        pfna_meta.extend(getattr(scene, "meta", {}).get("pfna_integerization", []) or [])

    integerized = [val for entry in pfna_meta for val in entry.get("values", tuple())]
    audits = [audit for entry in pfna_meta for audit in entry.get("audit", tuple())]
    clamped = sum(1 for audit in audits if audit.get("clamped") != audit.get("rounded"))

    if integerized:
        summary["values"] = len(integerized)
        summary["clamped"] = clamped
        summary.update(
            {
                "min": min(integerized),
                "max": max(integerized),
                "mean": sum(integerized) / len(integerized),
            }
        )

    return summary


def generate_ingestion_outputs(params: Dict[str, object]):
    """Produce TBP encoding, fidelity, replay metrics, and source hints for ingestion."""

    params = dict(params)
    qubits = int(params.get("qubits", 2))
    statevector, source = load_statevector(
        Path(params["input"]) if params.get("input") else None, qubits=qubits
    )
    encoded, fidelity, tune_notes = quantize_with_auto_tune(statevector, params)
    replay = summarize_pfna_replay(
        encoded,
        pfna_id=str(params.get("run_id") or "tbp_ingest"),
        gid=str(params.get("gid") or "GATE"),
        run_id=str(params.get("run_id") or "dpi_quantum"),
        tick=int(params.get("pfna_tick") or 0),
    )
    gate_replay = summarize_gate_pfna_replay(
        encoded,
        pfna_id=str(params.get("run_id") or "tbp_ingest"),
        gid=str(params.get("gid") or "GATE"),
        run_id=str(params.get("run_id") or "dpi_quantum"),
        tick=int(params.get("pfna_tick") or 1),
    )
    return encoded, fidelity, tune_notes, replay, gate_replay, source


def build_ingestion_result_summary(params: Dict[str, object]) -> Dict[str, object]:
    """Create a compact ingestion summary suitable for job.result_summary."""

    (
        encoded,
        fidelity,
        tune_notes,
        replay,
        gate_replay,
        source,
    ) = generate_ingestion_outputs(params)
    summary: Dict[str, object] = {
        "source": source,
        "qubits": int(params.get("qubits", 2)),
        "eta": encoded.get("eta"),
        "phase_bins": encoded.get("P"),
        "masses": len(encoded.get("masses", [])),
        "fidelity": fidelity,
        "pfna_replay": replay,
        "gate_replay": gate_replay,
    }
    if tune_notes:
        summary["tuning_notes"] = tune_notes
    return summary

