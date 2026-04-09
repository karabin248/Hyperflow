from pathlib import Path

from hyperflow.checkpoint.snapshot import build_architecture_snapshot, save_architecture_snapshot


def test_build_architecture_snapshot_has_core_fields():
    snapshot = build_architecture_snapshot(limit_runs=5)

    assert snapshot["system_name"] == "Hyperflow"
    assert "version" in snapshot
    assert "modules" in snapshot
    assert "capabilities" in snapshot
    assert "core_operating_kernel" in snapshot


def test_save_architecture_snapshot_writes_file(tmp_path: Path):
    out = tmp_path / "checkpoint.json"
    snapshot = save_architecture_snapshot(str(out), limit_runs=5)

    assert out.exists()
    assert snapshot["system_name"] == "Hyperflow"