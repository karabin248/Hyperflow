"""
test_llm_integration.py — Tests for OpenRouter integration in EDDE pipeline.
Verifies that LLM backend is called correctly and stub fallback works.

FIX #5: Removed duplicate local MockLLM class.
All tests now use MockLLMBackend from conftest.py for consistency.
calls format: list of dicts {prompt, intent, mode} — not tuples.
"""
import asyncio
import inspect
import pytest
from hyperflow.language.command_builder import build_command
from hyperflow.engine.reasoning import (
    run_extract_phase, run_discover_phase, run_do_phase_async,
    set_llm_backend, get_llm_backend,
)
from hyperflow.engine.runtime_state import init_runtime_state
from hyperflow.engine.edde_orchestrator import run_edde
# Re-use canonical mock from conftest — no local MockLLM needed
from tests.conftest import MockLLMBackend




def resolve_maybe_async(value):
    return asyncio.run(value) if inspect.isawaitable(value) else value


def get_cmd_and_state(prompt="analyze architecture"):
    cmd   = build_command(prompt)
    state = init_runtime_state(cmd)
    return cmd, state


# ── run_do_phase_async ─────────────────────────────────────────────────────────

def test_do_phase_uses_llm_when_backend_set():
    original = get_llm_backend()
    try:
        llm = MockLLMBackend(response=("LLM result for analyze", "test-model"))
        set_llm_backend(llm)
        cmd, state = get_cmd_and_state()
        extract    = run_extract_phase(cmd, state)
        discover   = run_discover_phase(cmd, state, extract)
        result     = asyncio.run(run_do_phase_async(cmd, state, discover))
        assert result["source"] == "llm"
        assert "LLM result" in result["draft_result"]
        assert len(llm.calls) == 1
    finally:
        set_llm_backend(original)


def test_do_phase_falls_back_to_stub_on_llm_failure():
    original = get_llm_backend()
    try:
        set_llm_backend(MockLLMBackend(fail=True))
        cmd, state = get_cmd_and_state()
        extract    = run_extract_phase(cmd, state)
        discover   = run_discover_phase(cmd, state, extract)
        result     = asyncio.run(run_do_phase_async(cmd, state, discover))
        assert result["source"] == "stub"
        assert result["draft_result"]  # not empty
    finally:
        set_llm_backend(original)


def test_do_phase_uses_stub_when_no_backend():
    original = get_llm_backend()
    try:
        set_llm_backend(None)
        cmd, state = get_cmd_and_state()
        extract    = run_extract_phase(cmd, state)
        discover   = run_discover_phase(cmd, state, extract)
        result     = asyncio.run(run_do_phase_async(cmd, state, discover))
        assert result["source"] == "stub"
        assert result["draft_result"]
    finally:
        set_llm_backend(original)


def test_llm_receives_intent_and_mode():
    original = get_llm_backend()
    try:
        llm = MockLLMBackend()
        set_llm_backend(llm)
        cmd, state = get_cmd_and_state("plan the database migration strategy")
        extract    = run_extract_phase(cmd, state)
        discover   = run_discover_phase(cmd, state, extract)
        asyncio.run(run_do_phase_async(cmd, state, discover))
        assert len(llm.calls) == 1
        call = llm.calls[0]  # FIX #5: calls are dicts, not tuples
        assert isinstance(call["intent"], str) and len(call["intent"]) > 0
        assert isinstance(call["mode"], str) and len(call["mode"]) > 0
    finally:
        set_llm_backend(original)


# ── Full EDDE pipeline ─────────────────────────────────────────────────────────

def test_full_edde_pipeline_with_llm(mock_llm):
    cmd, state = get_cmd_and_state("generate a function that adds two numbers")
    bundle     = resolve_maybe_async(run_edde(cmd, state))
    assert bundle["llm_source"] == "llm"
    assert bundle["llm_model"] == "mock-model-v1"
    assert "summary" in bundle
    assert bundle.get("pipeline_path")


def test_full_edde_pipeline_stub_fallback(no_llm):
    cmd, state = get_cmd_and_state("analyze the codebase")
    bundle     = resolve_maybe_async(run_edde(cmd, state))
    assert bundle["llm_source"] in ("stub", "stub_sync_shim")
    assert bundle.get("summary") or bundle.get("draft_result")


def test_edde_pipeline_sets_correct_phases(mock_llm):
    cmd, state = get_cmd_and_state("explain the EDDE pipeline")
    bundle     = resolve_maybe_async(run_edde(cmd, state))
    path = bundle.get("pipeline_path", [])
    assert any("extract" in p for p in path)
    assert any(("do" in p) or (p in {"interpret", "orchestrate", "remix"}) for p in path)
    assert any(("evaluate" in p) or (p == "output") for p in path)


def test_edde_emoji_combo_parsed_and_used():
    original = get_llm_backend()
    try:
        llm = MockLLMBackend()
        set_llm_backend(llm)
        cmd, state = get_cmd_and_state("🌈💎 analyze global architecture")
        assert "🌈" in cmd.tokens or "🌈" in cmd.raw_input
        bundle = resolve_maybe_async(run_edde(cmd, state))
        assert bundle.get("emoji_control") is not None
    finally:
        set_llm_backend(original)


def test_multiple_prompts_each_get_llm_call():
    original = get_llm_backend()
    try:
        llm = MockLLMBackend()
        set_llm_backend(llm)
        prompts = ["analyze X", "generate Y", "plan Z"]
        for p in prompts:
            cmd, state = get_cmd_and_state(p)
            e = run_extract_phase(cmd, state)
            d = run_discover_phase(cmd, state, e)
            asyncio.run(run_do_phase_async(cmd, state, d))
        assert len(llm.calls) == len(prompts)
    finally:
        set_llm_backend(original)


# FIX #4: Verify LLM errors land in state.llm_errors (formal field, not dynamic attribute)
def test_llm_errors_stored_in_state_field():
    original = get_llm_backend()
    try:
        set_llm_backend(MockLLMBackend(fail=True))
        cmd, state = get_cmd_and_state("test error capture")
        extract  = run_extract_phase(cmd, state)
        discover = run_discover_phase(cmd, state, extract)
        asyncio.run(run_do_phase_async(cmd, state, discover))
        assert hasattr(state, "llm_errors"), "llm_errors must be a schema field"
        assert len(state.llm_errors) == 1
        assert "Mock LLM failure" in state.llm_errors[0]
    finally:
        set_llm_backend(original)
