"""Helpers for DPI emulation fidelity comparisons (Phase 9 EPIC 5).

The emulation sweeps pair oracle probability/amplitude outputs with
full-stack runs and compute simple error metrics. The helper returns a
dictionary so callers can stash the metrics directly into `RunSummary`
extras for downstream reporting.
"""
from __future__ import annotations

import math
from typing import Iterable, Mapping, MutableMapping, Sequence


def _l1_gap(values_a: Sequence[float], values_b: Sequence[float]) -> float:
    if len(values_a) != len(values_b):  # pragma: no cover - config validation guard
        raise ValueError("Probability vectors must be the same length")
    return float(sum(abs(a - b) for a, b in zip(values_a, values_b)))


def _l2_gap(values_a: Sequence[float], values_b: Sequence[float]) -> float:
    if len(values_a) != len(values_b):  # pragma: no cover - config validation guard
        raise ValueError("Amplitude vectors must be the same length")
    return float(math.sqrt(sum((a - b) ** 2 for a, b in zip(values_a, values_b))))


def compute_emulation_metrics(
    *,
    oracle_probs: Iterable[float] | None,
    candidate_probs: Iterable[float] | None,
    oracle_amps: Iterable[float] | None = None,
    candidate_amps: Iterable[float] | None = None,
    prob_tolerance: float = 0.05,
    amp_tolerance: float = 0.1,
) -> Mapping[str, object]:
    """Compute error metrics and an `emulation_ok` flag.

    The helper assumes probabilities and amplitudes are already normalised
    upstream; it only computes absolute L1/L2 gaps and checks them against
    the provided tolerances.
    """

    metrics: MutableMapping[str, object] = {}
    if oracle_probs is not None and candidate_probs is not None:
        metrics["fidelity_prob_l1"] = _l1_gap(list(oracle_probs), list(candidate_probs))
    if oracle_amps is not None and candidate_amps is not None:
        metrics["fidelity_amp_l2"] = _l2_gap(list(oracle_amps), list(candidate_amps))

    emulation_ok = True
    if "fidelity_prob_l1" in metrics:
        emulation_ok = metrics["fidelity_prob_l1"] <= prob_tolerance
    if "fidelity_amp_l2" in metrics:
        emulation_ok = emulation_ok and metrics["fidelity_amp_l2"] <= amp_tolerance
    metrics["emulation_ok"] = emulation_ok

    metrics["prob_tolerance"] = prob_tolerance
    metrics["amp_tolerance"] = amp_tolerance
    return metrics

