from pathlib import Path
from zipfile import ZipFile

from hyperflow.release.source_zip import (
    build_source_zip,
    default_source_zip_name,
    default_source_zip_root_name,
    get_version_from_root,
    iter_source_files,
)
from hyperflow.version import __version__


def test_source_zip_excludes_generated_artifacts(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    (root / "hyperflow").mkdir(parents=True)
    (root / "hyperflow" / "version.py").write_text(f'__version__ = "{__version__}"\n', encoding="utf-8")
    (root / "README.md").write_text("hello\n", encoding="utf-8")

    (root / "build").mkdir()
    (root / "build" / "temp.txt").write_text("x\n", encoding="utf-8")
    (root / "storage").mkdir()
    (root / "storage" / "graph_memory.json").write_text("{}\n", encoding="utf-8")
    (root / "hyperflow.egg-info").mkdir()
    (root / "hyperflow.egg-info" / "PKG-INFO").write_text("pkg\n", encoding="utf-8")
    (root / "__pycache__").mkdir()
    (root / "__pycache__" / "mod.pyc").write_bytes(b"x")

    files = {path.relative_to(root).as_posix() for path in iter_source_files(root)}
    assert "README.md" in files
    assert "hyperflow/version.py" in files
    assert "build/temp.txt" not in files
    assert "storage/graph_memory.json" not in files
    assert "hyperflow.egg-info/PKG-INFO" not in files
    assert "__pycache__/mod.pyc" not in files


def test_build_source_zip_writes_clean_archive(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    (root / "hyperflow").mkdir(parents=True)
    (root / "hyperflow" / "__main__.py").write_text("print(\'ok\')\n", encoding="utf-8")
    (root / "hyperflow" / "version.py").write_text('__version__ = "9.9.9"\n', encoding="utf-8")
    (root / "README.md").write_text("hello\n", encoding="utf-8")
    (root / ".pytest_cache").mkdir()
    (root / ".pytest_cache" / "state").write_text("x\n", encoding="utf-8")

    output = tmp_path / "artifact" / "repo.zip"
    build_source_zip(root, output)

    with ZipFile(output) as zf:
        names = set(zf.namelist())

    archive_root = default_source_zip_root_name(root)
    assert f"{archive_root}/README.md" in names
    assert f"{archive_root}/hyperflow/__main__.py" in names
    assert f"{archive_root}/.pytest_cache/state" not in names


def test_build_source_zip_does_not_embed_output_archive(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    (root / "hyperflow").mkdir(parents=True)
    (root / "hyperflow" / "__main__.py").write_text("print(\'ok\')\n", encoding="utf-8")
    (root / "README.md").write_text("hello\n", encoding="utf-8")

    output = root / default_source_zip_name(root)
    build_source_zip(root, output)

    with ZipFile(output) as zf:
        names = set(zf.namelist())

    archive_root = default_source_zip_root_name(root)
    assert f"{archive_root}/README.md" in names
    assert f"{archive_root}/hyperflow/__main__.py" in names
    assert default_source_zip_name(root) not in names
    assert f"{archive_root}/{default_source_zip_name(root)}" not in names


def test_default_source_zip_name_tracks_package_version() -> None:
    assert default_source_zip_name() == f"hyperflow-v{__version__}-source.zip"


def test_default_source_zip_root_name_tracks_package_version() -> None:
    assert default_source_zip_root_name() == f"hyperflow-v{__version__}"


def test_source_zip_version_can_be_read_from_target_root(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    (root / "hyperflow").mkdir(parents=True)
    (root / "hyperflow" / "version.py").write_text('__version__ = "9.9.9"\n', encoding="utf-8")

    assert get_version_from_root(root) == "9.9.9"
    assert default_source_zip_root_name(root) == "hyperflow-v9.9.9"
    assert default_source_zip_name(root) == "hyperflow-v9.9.9-source.zip"


def test_source_zip_excludes_prior_release_archives(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    (root / "hyperflow").mkdir(parents=True)
    (root / "hyperflow" / "__main__.py").write_text("print(\'ok\')\n", encoding="utf-8")
    (root / "README.md").write_text("hello\n", encoding="utf-8")
    (root / default_source_zip_name(root)).write_bytes(b"old zip")
    (root / "hyperflow-source.zip").write_bytes(b"legacy zip")

    output = tmp_path / "artifact" / "repo.zip"
    build_source_zip(root, output)

    with ZipFile(output) as zf:
        names = set(zf.namelist())

    archive_root = default_source_zip_root_name(root)
    assert f"{archive_root}/README.md" in names
    assert f"{archive_root}/hyperflow/__main__.py" in names
    assert default_source_zip_name(root) not in names
    assert f"{archive_root}/{default_source_zip_name(root)}" not in names
    assert "hyperflow-source.zip" not in names
    assert f"{archive_root}/hyperflow-source.zip" not in names
