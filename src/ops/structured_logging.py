"""Structured logging utilities for Phase 3 governance work."""
from __future__ import annotations

"""Structured logging utilities for Phase 3 governance work."""

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional


_ALLOWED_DESTINATIONS = {"memory", "stdout", "file"}


@dataclass(frozen=True)
class LoggingConfigV1:
    """Configuration for structured logging.

    This config is intentionally small for Phase 3: enable/disable, destination,
    and optional file path. Verbosity can be refined in later phases by
    expanding this structure without breaking the existing shape.
    """

    enabled: bool = False
    destination: str = "memory"
    file_path: Optional[str] = None
    include_ticks: bool = True
    include_windows: bool = True

    def __post_init__(self) -> None:
        if self.destination not in _ALLOWED_DESTINATIONS:
            raise ValueError(f"destination must be one of {sorted(_ALLOWED_DESTINATIONS)}")
        if self.destination == "file" and not self.file_path:
            raise ValueError("file_path must be provided when destination is 'file'")
        if self.file_path is not None and not isinstance(self.file_path, str):
            raise ValueError("file_path must be a string when provided")


@dataclass(frozen=True)
class StructuredLogEntryV1:
    """Single structured log entry emitted by an Aether run."""

    event: str
    gid: str
    run_id: str
    ts: str
    tick: Optional[int] = None
    window_id: Optional[str] = None
    payload: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        payload = {
            "event": self.event,
            "gid": self.gid,
            "run_id": self.run_id,
            "ts": self.ts,
        }
        if self.tick is not None:
            payload["tick"] = self.tick
        if self.window_id is not None:
            payload["window_id"] = self.window_id
        if self.payload:
            payload["payload"] = self.payload
        return payload


class StructuredLogger:
    """Minimal structured logger with in-memory, stdout, or file destinations."""

    def __init__(self, config: Optional[LoggingConfigV1] = None) -> None:
        self.config = config or LoggingConfigV1()
        self._entries: List[StructuredLogEntryV1] = []
        self._file_path: Optional[Path] = None

        if self.config.enabled and self.config.destination == "file":
            path = Path(self.config.file_path).expanduser().resolve()
            path.parent.mkdir(parents=True, exist_ok=True)
            self._file_path = path

    @property
    def enabled(self) -> bool:
        return bool(self.config.enabled)

    @property
    def entries(self) -> List[StructuredLogEntryV1]:
        return list(self._entries)

    def _emit(self, entry: StructuredLogEntryV1) -> None:
        if not self.enabled:
            return
        if self.config.destination == "memory":
            self._entries.append(entry)
        elif self.config.destination == "stdout":
            print(json.dumps(entry.to_dict(), sort_keys=True))
        elif self.config.destination == "file":
            assert self._file_path is not None  # for type checkers
            with self._file_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(entry.to_dict(), sort_keys=True))
                handle.write("\n")

    def log(
        self,
        event: str,
        *,
        gid: str,
        run_id: str,
        tick: Optional[int] = None,
        window_id: Optional[str] = None,
        payload: Optional[Mapping[str, Any]] = None,
    ) -> None:
        """Emit a structured log entry if logging is enabled."""

        if not self.enabled:
            return
        timestamp = datetime.now(timezone.utc).isoformat()
        entry = StructuredLogEntryV1(
            event=event,
            gid=gid,
            run_id=run_id,
            ts=timestamp,
            tick=tick,
            window_id=window_id,
            payload=dict(payload or {}),
        )
        self._emit(entry)

    def log_many(self, entries: Iterable[Mapping[str, Any]], *, gid: str, run_id: str) -> None:
        for payload in entries:
            self.log(
                event=str(payload.get("event", "unknown")),
                gid=gid,
                run_id=run_id,
                tick=payload.get("tick"),
                window_id=payload.get("window_id"),
                payload=payload.get("payload"),
            )
