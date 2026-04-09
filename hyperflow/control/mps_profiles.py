from __future__ import annotations

from hyperflow.config import get_mps_regulator_config

DEFAULT_MPS_PROFILES = {
    1: {
        "name": "Observation",
        "depth": "low",
        "observer_rigor": "high",
        "risk_state": "low",
        "execution_policy": "observe",
    },
    2: {
        "name": "Stabilize",
        "depth": "medium",
        "observer_rigor": "high",
        "risk_state": "low",
        "execution_policy": "stabilize",
    },
    3: {
        "name": "Harmonize",
        "depth": "high",
        "observer_rigor": "medium",
        "risk_state": "medium",
        "execution_policy": "coordinate",
    },
    4: {
        "name": "Amplify",
        "depth": "high",
        "observer_rigor": "medium",
        "risk_state": "medium",
        "execution_policy": "amplify",
    },
    5: {
        "name": "Dominant Core",
        "depth": "very_high",
        "observer_rigor": "high",
        "risk_state": "high",
        "execution_policy": "core_dominant",
    },
    6: {
        "name": "Satellite Ops",
        "depth": "very_high",
        "observer_rigor": "very_high",
        "risk_state": "high",
        "execution_policy": "satellite_ops",
    },
    7: {
        "name": "Emergency",
        "depth": "recovery_only",
        "observer_rigor": "maximum",
        "risk_state": "critical",
        "execution_policy": "return_to_core",
    },
}


def _build_profiles() -> dict[int, dict]:
    profiles = {level: profile.copy() for level, profile in DEFAULT_MPS_PROFILES.items()}
    configured_levels = get_mps_regulator_config().get("mps_levels", [])

    for entry in configured_levels:
        level = int(entry.get("level", 0))
        if level <= 0:
            continue
        profile = profiles.get(level, {}).copy()
        profile["name"] = str(entry.get("name", profile.get("name", f"L{level}")))
        profile["notes"] = str(entry.get("notes", ""))
        profiles[level] = profile

    return profiles


MPS_PROFILES = _build_profiles()
