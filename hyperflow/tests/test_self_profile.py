from hyperflow.engine.runtime_kernel import run
from hyperflow.language.command_builder import build_command
from hyperflow.memory.self_profile import build_self_profile


def test_self_profile_returns_expected_fields():
    raw1 = (
        "🌈💎🔥🧠🔀⚡ "
        "Task: create a Hyperflow MVP build plan "
        "Goal: extract module order "
        "Format: sections + priorities"
    )
    raw2 = (
        "🧠💎 "
        "Task: make a short analysis of the Hyperflow core "
        "Goal: extract the most important modules "
        "Format: list"
    )

    run(build_command(raw1))
    run(build_command(raw1))
    run(build_command(raw2))

    profile = build_self_profile(limit_runs=5)

    assert "dominant_work_style" in profile
    assert "core_operating_kernel" in profile
    assert "satellite_modes" in profile
    assert "development_phase" in profile
    assert "short_self_description" in profile
    assert "narrative_summary" in profile

def test_self_profile_planning_text_matches_canonical_core_wording():
    raw = (
        "🌈💎🔥🧠🔀⚡ "
        "Task: create a Hyperflow MVP build plan "
        "Goal: extract module order "
        "Format: sections + priorities"
    )

    run(build_command(raw))
    run(build_command(raw))

    profile = build_self_profile(limit_runs=5)

    assert "option comparison" in profile["short_self_description"]
    assert "structure building" not in profile["short_self_description"]
