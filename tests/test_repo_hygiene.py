from __future__ import annotations

from pathlib import Path


def test_repo_hygiene_lock() -> None:
    root = Path(__file__).resolve().parents[1]
    banned_names = {'archive', '.pytest_cache', 'build', 'dist', 'tmp', 'legacy'}
    offenders: list[str] = []

    for path in root.rglob('*'):
        rel = path.relative_to(root).as_posix()
        if rel.startswith('.tmp_'):
            continue
        if '__pycache__' in rel or '.egg-info' in rel:
            continue
        if any(part in banned_names for part in path.parts):
            offenders.append(rel)
            continue
        if rel.endswith(('.pyc', '.pyo', '.zip')):
            offenders.append(rel)
            continue
        if path.is_file() and path.stat().st_size > 1_000_000 and not rel.endswith('.json'):
            offenders.append(rel)

    assert offenders == []
