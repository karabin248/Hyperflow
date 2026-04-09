from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any



def _serialize_command(command: Any) -> dict[str, Any]:
    if is_dataclass(command):
        return asdict(command)
    return dict(getattr(command, "__dict__", {}))



def serialize_run_payload(command: Any, result: Any) -> dict[str, Any]:
    return {
        "command": _serialize_command(command),
        "intent": getattr(command, "intent", ""),
        "mode": getattr(command, "mode", ""),
        "output_type": getattr(command, "output_type", ""),
        "result": result.to_dict(),
        "run_id": getattr(result, "run_id", ""),
        "contract": getattr(result, "edde_contract", {}),
    }


__all__ = ["serialize_run_payload"]
