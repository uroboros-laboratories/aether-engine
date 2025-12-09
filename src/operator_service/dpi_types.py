"""Shared DPI enums used across registry, schemas, and CLI."""
from __future__ import annotations

from enum import Enum


class DpiJobKind(str, Enum):
    INGESTION = "INGESTION"
    SIMULATION = "SIMULATION"
    EXPERIMENT = "EXPERIMENT"
