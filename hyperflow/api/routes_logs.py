from __future__ import annotations

from fastapi import APIRouter

from hyperflow.api.models import TraceListResponse
from hyperflow.memory.session_memory import SESSION_MEMORY
from hyperflow.memory.traces import load_recent_traces

router = APIRouter(prefix="/v1/logs", tags=["logs"])



def _serialize_session_records(limit: int) -> list[dict[str, object]]:
    records = SESSION_MEMORY.get_recent(limit=limit)
    items: list[dict[str, object]] = []
    for record in reversed(records):
        items.append(
            {
                "run_id": record.run_id,
                "raw_input": record.raw_input,
                "intent": record.intent,
                "mode": record.mode,
                "summary": record.summary,
                "observer_status": record.observer_status,
            }
        )
    return items


@router.get('/recent', response_model=TraceListResponse)
def recent_logs(limit: int = 5) -> dict[str, object]:
    items = load_recent_traces(limit=limit)
    if not items:
        items = _serialize_session_records(limit=limit)
    return {"items": items}
