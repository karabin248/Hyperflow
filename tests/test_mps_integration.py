import asyncio
import pytest
from hyperflow.language.command_builder import build_command
from hyperflow.control.mps_controller import apply_mps_profile, resolve_mps_level
from hyperflow.engine.runtime_state import init_runtime_state
from hyperflow.engine.edde_orchestrator import run_edde
from hyperflow.engine.reasoning import run_extract_phase, run_discover_phase


def make_state(prompt="analyze architecture"):
    cmd = build_command(prompt)
    state = init_runtime_state(cmd)
    return cmd, state


def test_mps_resolve_level_safe_mode():
    cmd, _ = make_state("safe run")
    cmd.mode = "safe"
    assert resolve_mps_level(cmd) == 1


def test_mps_resolve_level_fusion_mode():
    cmd, _ = make_state("fusion run")
    cmd.mode = "fusion"
    assert resolve_mps_level(cmd) == 6


def test_mps_apply_profile_sets_state():
    cmd, state = make_state("analyze")
    state.mps_level = 3
    state = apply_mps_profile(state)
    assert state.mps_state == "Harmonize"
    assert state.observer_rigor


def test_mps_level_affects_reasoning_depth():
    cmd, state = make_state("deep analysis")
    state.mps_level = 5
    state = apply_mps_profile(state)
    extract = run_extract_phase(cmd, state)
    discover = run_discover_phase(cmd, state, extract)
    assert discover.get("reasoning_depth") == "high"


def test_mps_risk_state_set_on_high_level():
    cmd, state = make_state("planning")
    state.mps_level = 5
    state = apply_mps_profile(state)
    assert state.risk_state in ("high", "medium", "low")
    assert state.mps_state


def test_mps_observer_rigor_set():
    # FIX #11: MPS levels 6 and 7 set observer_rigor to 'very_high'/'maximum'
    # All valid values from mps_profiles.py:
    valid_rigor = ("low", "medium", "high", "very_high", "maximum")
    for level in range(1, 7):
        cmd, state = make_state("test")
        state.mps_level = level
        state = apply_mps_profile(state)
        assert state.observer_rigor in valid_rigor, (
            f"MPS level {level} produced unexpected observer_rigor={state.observer_rigor!r}"
        )
