from __future__ import annotations

from pathlib import Path
import re
from zipfile import ZIP_DEFLATED, ZipFile

from hyperflow.version import get_version

_VERSION_RE = re.compile(r'__version__\s*=\s*["\']([^"\']+)["\']')

EXCLUDED_DIR_NAMES = {
    ".git",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "alerts",
    "artifacts",
    "build",
    "dist",
    "env",
    "hyperflow.egg-info",
    "storage",
    "venv",
    "wheelhouse",
}
EXCLUDED_FILE_NAMES = {
    ".DS_Store",
    "checkpoint_history.json",
    "graph.mmd",
    "graph.txt",
    "output.json",
    "status_report.json",
}
EXCLUDED_SUFFIXES = {".pyc", ".pyo", ".pyd", ".tmp", ".svg", ".png"}
EXCLUDED_GLOB_PATTERNS = {"hyperflow-source.zip", "hyperflow-v*-source.zip"}


def get_version_from_root(root: Path | None = None) -> str:
    if root is not None:
        version_py = root.resolve() / "hyperflow" / "version.py"
        if version_py.exists():
            match = _VERSION_RE.search(version_py.read_text(encoding="utf-8"))
            if match:
                return match.group(1)
    return get_version()


def default_source_zip_root_name(root: Path | None = None) -> str:
    return f"hyperflow-v{get_version_from_root(root)}"


def default_source_zip_name(root: Path | None = None) -> str:
    return f"{default_source_zip_root_name(root)}-source.zip"


def is_excluded(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    if any(part in EXCLUDED_DIR_NAMES for part in relative.parts[:-1]):
        return True
    if path.is_dir() and path.name in EXCLUDED_DIR_NAMES:
        return True
    if path.name in EXCLUDED_FILE_NAMES:
        return True
    if path.suffix in EXCLUDED_SUFFIXES:
        return True
    if any(relative.match(pattern) for pattern in EXCLUDED_GLOB_PATTERNS):
        return True
    return False


def iter_source_files(root: Path, extra_excluded: set[Path] | None = None):
    root = root.resolve()
    extra_excluded = {path.resolve() for path in (extra_excluded or set())}
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.resolve() in extra_excluded:
            continue
        if is_excluded(path, root):
            continue
        yield path


def build_source_zip(root: Path, output_zip: Path) -> Path:
    root = root.resolve()
    output_zip = output_zip.resolve()
    output_zip.parent.mkdir(parents=True, exist_ok=True)

    archive_root = default_source_zip_root_name(root)

    with ZipFile(output_zip, "w", compression=ZIP_DEFLATED) as zf:
        for path in iter_source_files(root, extra_excluded={output_zip}):
            relative = path.relative_to(root).as_posix()
            zf.write(path, arcname=f"{archive_root}/{relative}")
    return output_zip
