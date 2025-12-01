"""CMP-0 numeric profile definition."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict


@dataclass(frozen=True)
class ProfileCMP0V1:
    """Numeric constants and rule metadata for CMP-style numeric profiles."""

    name: str = "CMP-0"
    modulus_M: int = 1_000_000_007
    C0: int = 1_234_567
    SC: int = 32
    epsilon_cap: int | None = None
    I_block_spacing_W: int = 8
    flux_rule: Dict[str, object] = field(default_factory=lambda: {
        "type": "CMP0_flux_v1",
        "du_formula": "du = pre_u[i] - pre_u[j]",
        "raw_formula": "raw = floor(k * abs(du) / SC)",
        "f_e_formula": "f_e = sign(du) * min(raw, cap, abs(du))",
        "conservation": "sum(pre_u) == sum(post_u)",
    })
    chain_rule: Dict[str, object] = field(default_factory=lambda: {
        "type": "CMP0_chain_v1",
        "update": "C_t = (17 * C_{t-1} + 23 * s_t + seq_t) mod M",
        "constants": {"a": 17, "b": 23},
    })
    s_t_rule: Dict[str, object] = field(default_factory=lambda: {
        "type": "CMP0_s_t_v1",
        "description": "GF-01 uses a constant s_t = 9 for all ticks.",
        "gf01_constant": 9,
    })
    epsilon_policy: Dict[str, object] = field(
        default_factory=lambda: {
            "description": "Optional epsilon clamp for raw flux magnitude.",
            "cap_field": "epsilon_cap",
        }
    )
    nap_defaults: Dict[str, object] = field(default_factory=lambda: {
        "v": 1,
        "layer": "DATA",
        "mode": "P",
    })
    press_defaults: Dict[str, object] = field(default_factory=lambda: {
        "preferred_schemes": ["R", "GR", "ID"],
        "gf01_streams": ["S1_post_u_deltas", "S2_fluxes"],
    })

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name:
            raise ValueError("Profile name must be a non-empty string")
        if not self.name.startswith("CMP-"):
            raise ValueError("Profile name must start with 'CMP-'")
        if not all(
            isinstance(v, int) and v > 0
            for v in (self.modulus_M, self.C0, self.SC, self.I_block_spacing_W)
        ):
            raise ValueError("CMP numeric constants must be positive integers")
        if self.epsilon_cap is not None and (
            not isinstance(self.epsilon_cap, int) or self.epsilon_cap <= 0
        ):
            raise ValueError("epsilon_cap, when set, must be a positive integer")


def gf01_profile_cmp0() -> ProfileCMP0V1:
    """Return the canonical CMP-0 profile used by GF-01."""

    return ProfileCMP0V1()
