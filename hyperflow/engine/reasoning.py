from __future__ import annotations

from typing import Any, Optional

from hyperflow.schemas.command_schema import CommandObject
from hyperflow.schemas.runtime_state_schema import RuntimeState


_llm_backend: Optional[Any] = None


def set_llm_backend(backend: Any) -> None:
    global _llm_backend
    _llm_backend = backend


def get_llm_backend() -> Optional[Any]:
    return _llm_backend


def run_extract_phase(command: CommandObject, state: RuntimeState) -> dict:
    state.phase = "extract"
    return {
        "task_core": command.cleaned_text or command.raw_input,
        "tokens": command.tokens,
        "constraints": command.constraints,
        "scope": "global" if "🌈" in command.tokens else "local",
    }


def run_discover_phase(command: CommandObject, state: RuntimeState, extract_bundle: dict) -> dict:
    state.phase = "discover"
    return {
        "strategy": f"{command.intent}:{command.mode}",
        "reasoning_depth": "high" if state.mps_level >= 4 else "medium",
        "selected_path": command.intent,
        "extract_bundle": extract_bundle,
    }


def _stub_do_result(command: CommandObject, state: RuntimeState) -> dict:
    draft_summary = (
        f"Hyperflow executed intent '{command.intent}' in mode '{command.mode}' "
        f"with operations: {', '.join(command.operations)}."
    )
    partial_insights = [
        f"Primary intent resolved as {command.intent}.",
        f"Mode selected: {command.mode}.",
        f"Output type expected: {command.output_type}.",
    ]
    actions = [f"Run operation: {op}" for op in command.operations] or ["Run operation: synthesize"]
    return {
        "draft_result": draft_summary,
        "partial_insights": partial_insights,
        "actions": actions,
        "coverage_status": "ok",
        "source": "stub",
        "model": None,
    }


async def run_do_phase_async(command: CommandObject, state: RuntimeState, decision_bundle: dict) -> dict:
    state.phase = "do"
    backend = get_llm_backend()
    if backend is None:
        return _stub_do_result(command, state)
    try:
        llm_text, model_used = await backend(command.raw_input, command.intent, command.mode)
    except Exception as exc:
        if hasattr(state, "llm_errors"):
            state.llm_errors.append(str(exc))
        return _stub_do_result(command, state)
    return {
        "draft_result": llm_text,
        "partial_insights": [
            f"LLM ({model_used}) executed intent '{command.intent}' in '{command.mode}' mode.",
            f"Output type: {command.output_type}. MPS level {state.mps_level} → {state.mps_state}.",
        ],
        "actions": [f"llm_response:{model_used}"],
        "coverage_status": "ok",
        "source": "llm",
        "model": model_used,
    }


def run_do_phase(command: CommandObject, state: RuntimeState, decision_bundle: dict) -> dict:
    import asyncio
    return asyncio.run(run_do_phase_async(command, state, decision_bundle))
