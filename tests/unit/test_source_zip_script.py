import runpy
import sys
from pathlib import Path

from hyperflow.release.source_zip import default_source_zip_name
from hyperflow.version import __version__


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_make_source_zip_script_uses_target_root_version(tmp_path, monkeypatch) -> None:
    root = tmp_path / "repo"
    (root / "hyperflow").mkdir(parents=True)
    (root / "hyperflow" / "version.py").write_text('__version__ = "9.9.9"\n', encoding="utf-8")
    (root / "README.md").write_text("hello\n", encoding="utf-8")

    script = _repo_root() / "scripts" / "make_source_zip.py"

    monkeypatch.chdir(root)
    monkeypatch.setattr(sys, "argv", [str(script)])

    try:
        runpy.run_path(str(script), run_name="__main__")
    except SystemExit as exc:
        assert exc.code == 0

    assert (root / "hyperflow-v9.9.9-source.zip").exists()
    assert not (root / f"hyperflow-v{__version__}-source.zip").exists()
    assert default_source_zip_name(root) == "hyperflow-v9.9.9-source.zip"
