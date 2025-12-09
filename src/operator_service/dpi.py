"""Domain Plug-in (DPI) data structures and registry helpers.

This module provides a minimal in-memory representation of DPIs so the
operator service can list available plug-ins without enabling UI or
engine changes. The registry is gated by a feature flag so Phase 7
behaviour remains untouched when Phase 8 is disabled.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional

from operator_service.dpi_jobs import DpiJobSchema, JOB_SCHEMAS
from operator_service.dpi_types import DpiJobKind


class DpiStatus(str, Enum):
    IDLE = "IDLE"
    ACTIVE = "ACTIVE"
    FAULT = "FAULT"
    DISABLED = "DISABLED"


class DpiJobStatus(str, Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


@dataclass
class DpiSummary:
    id: str
    name: str
    type: str
    description: str
    status: DpiStatus
    tags: List[str] = field(default_factory=list)


@dataclass
class DpiDetail(DpiSummary):
    capabilities: Dict[str, bool] = field(default_factory=dict)
    config_schema: Dict[str, object] = field(default_factory=dict)


@dataclass
class DpiJob:
    job_id: str
    dpi_id: str
    kind: DpiJobKind
    status: DpiJobStatus
    params: Dict[str, object] = field(default_factory=dict)
    run_id: Optional[str] = None
    result_summary: Optional[Dict[str, object]] = None


class DpiRegistry:
    """In-memory registry for DPIs and their jobs."""

    FEATURE_FLAG = "AETHER_FEATURE_DPI"

    def __init__(self) -> None:
        self._enabled = os.getenv(self.FEATURE_FLAG, "0") not in {"", "0", "false", "False"}
        self._dpis: Dict[str, DpiDetail] = {}
        self._jobs: Dict[str, List[DpiJob]] = {}
        self._job_counters: Dict[str, int] = {}
        self._run_index: Dict[str, List[str]] = {}
        self._bootstrap_quantum()

    @property
    def enabled(self) -> bool:
        return self._enabled

    def _bootstrap_quantum(self) -> None:
        quantum = DpiDetail(
            id="quantum",
            name="Quantum DPI",
            type="quantum",
            description="Quantum data ingestion, simulation, and emulation workflows",
            status=DpiStatus.IDLE,
            tags=["ingestion", "simulation", "emulation"],
            capabilities={
                "supports_ingestion": True,
                "supports_simulation": True,
                "supports_experiments": True,
            },
            config_schema=_build_job_schema(),
        )
        self._dpis[quantum.id] = quantum
        self._jobs[quantum.id] = []

    def list(self) -> List[DpiSummary]:
        return [
            DpiSummary(
                id=detail.id,
                name=detail.name,
                type=detail.type,
                description=detail.description,
                status=detail.status,
                tags=list(detail.tags),
            )
            for detail in self._dpis.values()
        ]

    def get(self, dpi_id: str) -> Optional[DpiDetail]:
        return self._dpis.get(dpi_id)

    def list_jobs(self, dpi_id: str) -> List[DpiJob]:
        return list(self._jobs.get(dpi_id, []))

    def list_jobs_for_run(self, run_id: str) -> List[DpiJob]:
        """Return all jobs associated with the given run id."""

        job_ids = self._run_index.get(run_id, [])
        results: List[DpiJob] = []
        for dpi_jobs in self._jobs.values():
            for job in dpi_jobs:
                if job.job_id in job_ids or job.run_id == run_id:
                    results.append(job)
        return results

    def add_job(self, job: DpiJob) -> None:
        jobs = self._jobs.setdefault(job.dpi_id, [])
        jobs.append(job)

    def attach_run(self, job: DpiJob, run_id: str) -> None:
        """Record that a job is associated with a run id."""

        job.run_id = run_id
        self._run_index.setdefault(run_id, []).append(job.job_id)

    def create_job(
        self,
        dpi_id: str,
        kind: DpiJobKind,
        *,
        params: Optional[Dict[str, object]] = None,
        status: DpiJobStatus = DpiJobStatus.QUEUED,
        run_id: Optional[str] = None,
        result_summary: Optional[Dict[str, object]] = None,
    ) -> DpiJob:
        if dpi_id not in self._dpis:
            raise KeyError(f"unknown dpi id {dpi_id}")

        sequence = self._job_counters.get(dpi_id, 0) + 1
        self._job_counters[dpi_id] = sequence
        job_id = f"{dpi_id}-job-{sequence:04d}"
        job = DpiJob(
            job_id=job_id,
            dpi_id=dpi_id,
            kind=kind,
            status=status,
            params=dict(params or {}),
            run_id=run_id,
            result_summary=result_summary,
        )
        self.add_job(job)
        if run_id:
            self._run_index.setdefault(run_id, []).append(job.job_id)
        return job


def _build_job_schema() -> Dict[str, object]:
    payload: Dict[str, object] = {}
    for kind, schema in JOB_SCHEMAS.items():
        if not isinstance(schema, DpiJobSchema):
            continue
        payload[kind.value.lower()] = schema.describe()
    return payload
