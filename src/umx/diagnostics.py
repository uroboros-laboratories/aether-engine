"""Optional diagnostics and invariant checks for UMX runs."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Sequence


@dataclass
class UMXDiagnosticsConfig:
    """Configuration for optional UMX diagnostics.

    When ``enabled`` is True, the run context records per-tick diagnostic
    summaries that can flag conservation issues, negative values, or numeric
    overflow. Violations are surfaced via the returned diagnostics record and
    can optionally raise an exception when ``raise_on_violation`` is True.
    """

    enabled: bool = False
    check_conservation: bool = True
    allow_negative: bool = True
    overflow_limit: Optional[int] = None
    raise_on_violation: bool = False

    def evaluate_tick(
        self,
        *,
        tick: int,
        pre_u: Sequence[int],
        post_u: Sequence[int],
        sum_pre_u: Optional[int] = None,
        sum_post_u: Optional[int] = None,
        z_check: Optional[int] = None,
    ) -> "UMXDiagnosticsRecord":
        """Evaluate invariants for a single tick and return diagnostics."""

        record = UMXDiagnosticsRecord.from_arrays(
            tick=tick,
            pre_u=pre_u,
            post_u=post_u,
            sum_pre_u=sum_pre_u,
            sum_post_u=sum_post_u,
            z_check=z_check,
            config=self,
        )
        if self.raise_on_violation and record.violations:
            raise ValueError(
                f"UMX diagnostics failed at tick {tick}: " + ", ".join(record.violations)
            )
        return record


@dataclass
class UMXDiagnosticsRecord:
    """Per-tick diagnostic summary for a UMX run."""

    tick: int
    sum_pre_u: int
    sum_post_u: int
    conservation_ok: bool
    min_pre: int
    max_pre: int
    min_post: int
    max_post: int
    has_negative_pre: bool
    has_negative_post: bool
    overflow_limit: Optional[int]
    overflow_pre: bool
    overflow_post: bool
    violations: List[str] = field(default_factory=list)

    @classmethod
    def from_arrays(
        cls,
        *,
        tick: int,
        pre_u: Sequence[int],
        post_u: Sequence[int],
        config: UMXDiagnosticsConfig,
        sum_pre_u: Optional[int] = None,
        sum_post_u: Optional[int] = None,
        z_check: Optional[int] = None,
    ) -> "UMXDiagnosticsRecord":
        """Create a diagnostics record from state arrays and config."""

        computed_sum_pre = sum(pre_u)
        computed_sum_post = sum(post_u)
        sum_pre_val = computed_sum_pre if sum_pre_u is None else sum_pre_u
        sum_post_val = computed_sum_post if sum_post_u is None else sum_post_u
        z_target = sum_pre_val if z_check is None else z_check

        conservation_ok = sum_pre_val == sum_post_val == z_target

        min_pre = min(pre_u) if pre_u else 0
        max_pre = max(pre_u) if pre_u else 0
        min_post = min(post_u) if post_u else 0
        max_post = max(post_u) if post_u else 0

        has_negative_pre = any(value < 0 for value in pre_u)
        has_negative_post = any(value < 0 for value in post_u)

        overflow_pre = False
        overflow_post = False
        if config.overflow_limit is not None:
            limit = config.overflow_limit
            overflow_pre = any(abs(value) > limit for value in pre_u)
            overflow_post = any(abs(value) > limit for value in post_u)

        violations: List[str] = []
        if config.check_conservation and not conservation_ok:
            violations.append(
                f"conservation failed (pre={sum_pre_val}, post={sum_post_val}, z={z_target})"
            )
        if not config.allow_negative and (has_negative_pre or has_negative_post):
            violations.append("negative values detected")
        if config.overflow_limit is not None and (overflow_pre or overflow_post):
            violations.append(
                f"overflow detected beyond limit {config.overflow_limit}"
            )

        return cls(
            tick=tick,
            sum_pre_u=sum_pre_val,
            sum_post_u=sum_post_val,
            conservation_ok=conservation_ok,
            min_pre=min_pre,
            max_pre=max_pre,
            min_post=min_post,
            max_post=max_post,
            has_negative_pre=has_negative_pre,
            has_negative_post=has_negative_post,
            overflow_limit=config.overflow_limit,
            overflow_pre=overflow_pre,
            overflow_post=overflow_post,
            violations=violations,
        )
