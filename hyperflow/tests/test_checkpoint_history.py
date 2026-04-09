import json
from pathlib import Path

from hyperflow.checkpoint.history import build_checkpoint_history


def test_build_checkpoint_history(tmp_path: Path):
    checkpoint_dir = tmp_path / "storage" / "checkpoints"
    checkpoint_dir.mkdir(parents=True, exist_ok=True)

    item_1 = {
        "generated_at": "2026-03-15T01:00:00+00:00",
        "version": "0.1.0",
        "status": "stable-operational",
        "development_phase": "structured-operational",
        "dominant_work_style": "planning-fusion",
        "dominant_intent": "planning",
        "dominant_mode": "fusion",
        "core_operating_kernel": ["perceive", "extract_core", "set_direction", "synthesize", "generate_options", "choose"],
        "satellite_modes": ["analysis"],
    }

    item_2 = {
        "generated_at": "2026-03-15T02:00:00+00:00",
        "version": "0.1.0",
        "status": "stable-operational",
        "development_phase": "structured-operational",
        "dominant_work_style": "planning-fusion",
        "dominant_intent": "planning",
        "dominant_mode": "fusion",
        "core_operating_kernel": ["perceive", "extract_core", "set_direction", "synthesize", "generate_options", "choose", "structure"],
        "satellite_modes": [],
    }

    (checkpoint_dir / "cp1.json").write_text(json.dumps(item_1), encoding="utf-8")
    (checkpoint_dir / "cp2.json").write_text(json.dumps(item_2), encoding="utf-8")

    old_dir = Path.cwd()
    try:
        import os
        os.chdir(tmp_path)

        history = build_checkpoint_history(limit=10)
    finally:
        os.chdir(old_dir)

    assert history["count"] == 2
    assert history["latest"]["file_name"] == "cp2.json"
    assert history["previous"]["file_name"] == "cp1.json"
    assert any("Core kernel expanded" in item for item in history["evolution"])

def test_build_checkpoint_history_without_directory_is_side_effect_free(tmp_path: Path):
    old_dir = Path.cwd()
    try:
        import os
        os.chdir(tmp_path)

        history = build_checkpoint_history(limit=10)
    finally:
        os.chdir(old_dir)

    assert history["count"] == 0
    assert history["latest"] is None
    assert history["previous"] is None
    assert history["evolution"] == ["No checkpoints found."]
    assert not (tmp_path / "storage").exists()
