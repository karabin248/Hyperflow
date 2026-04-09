from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from hyperflow.api.models import CheckpointListResponse
from hyperflow.checkpoint.history import build_checkpoint_history, load_checkpoint_by_identity
from hyperflow.checkpoint.snapshot import build_architecture_snapshot

router = APIRouter(prefix="/v1/checkpoints", tags=["checkpoints"])


@router.get("", response_model=CheckpointListResponse)
def checkpoints(limit: int = 10) -> dict[str, object]:
    history = build_checkpoint_history(limit=limit)
    return {"items": history["timeline"]}


@router.get("/latest")
def latest_checkpoint() -> dict[str, Any]:
    history = build_checkpoint_history(limit=1)
    if history["latest"] is not None:
        return history["latest"]
    return build_architecture_snapshot(limit_runs=10)


@router.get("/{checkpoint_id}")
def checkpoint_by_id(checkpoint_id: str) -> dict[str, Any]:
    item = load_checkpoint_by_identity(checkpoint_id)
    if item is None:
        raise HTTPException(status_code=404, detail="checkpoint_not_found")
    return item
