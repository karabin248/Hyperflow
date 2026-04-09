from pathlib import Path
from zipfile import ZipFile

from hyperflow.release.source_zip import build_source_zip, default_source_zip_root_name


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_real_repo_source_zip_is_clean(tmp_path: Path) -> None:
    root = _repo_root()
    output = tmp_path / 'artifact' / 'repo.zip'

    build_source_zip(root, output)

    with ZipFile(output) as zf:
        names = set(zf.namelist())

    archive_root = default_source_zip_root_name(root)
    assert f"{archive_root}/README.md" in names
    assert f"{archive_root}/hyperflow/__main__.py" in names

    blocked_substrings = (
        '/hyperflow.egg-info/',
        '/__pycache__/',
        '/.pytest_cache/',
        '/build/',
        '/dist/',
        '/wheelhouse/',
        '/storage/',
    )
    for name in names:
        assert not any(blocked in name for blocked in blocked_substrings), name
