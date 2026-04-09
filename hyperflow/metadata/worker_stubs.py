"""Metadata-only worker/workflow surface.

This module intentionally exposes stub metadata only. It is not a runtime,
not an orchestration authority, and not an alternate execution path.
"""

from __future__ import annotations

from copy import deepcopy

_WORKERS = [
    {
        "id": "research-worker",
        "role": "research",
        "capability": "repo inspection",
        "description": "Metadata-only research worker stub.",
        "execution": "stub.metadata_only",
        "integrated_with_runtime": False,
    },
    {
        "id": "reasoning-worker",
        "role": "reasoning",
        "capability": "reasoning review",
        "description": "Metadata-only reasoning worker stub.",
        "execution": "stub.metadata_only",
        "integrated_with_runtime": False,
    },
    {
        "id": "reporting-worker",
        "role": "reporting",
        "capability": "report synthesis",
        "description": "Metadata-only reporting worker stub.",
        "execution": "stub.metadata_only",
        "integrated_with_runtime": False,
    },
    {
        "id": "tools-worker",
        "role": "tools",
        "capability": "tool mediation",
        "description": "Metadata-only tools worker stub.",
        "execution": "stub.metadata_only",
        "integrated_with_runtime": False,
    },
    {
        "id": "external-executor-worker",
        "role": "external-executor",
        "capability": "subprocess boundary",
        "description": "Metadata-only external executor worker stub.",
        "execution": "stub.metadata_only",
        "integrated_with_runtime": False,
    },
]

_WORKFLOWS = [
    {
        "id": "canonical-run",
        "name": "Canonical Run",
        "description": "Metadata-only marker for the singular runtime spine.",
        "intent": "analysis",
        "mode": "standard",
    }
]

def _clone(items: list[dict]) -> list[dict]:
    return [deepcopy(item) for item in items]

def list_worker_specs() -> list[dict]:
    return _clone(_WORKERS)

def list_live_worker_specs() -> list[dict]:
    return _clone(_WORKERS)

def list_agents() -> list[dict]:
    return [{"id": item["id"], "role": item["role"], "capability": item["capability"]} for item in _clone(_WORKERS)]

def list_workflows() -> list[dict]:
    return _clone(_WORKFLOWS)
