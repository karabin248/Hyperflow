from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_android_shell_is_imported_as_files_only() -> None:
    android_root = REPO_ROOT / 'apps' / 'android'
    assert (android_root / 'README.md').exists()
    assert (android_root / 'build.gradle.kts').exists()
    assert (android_root / 'settings.gradle.kts').exists()
    assert (android_root / 'app' / 'build.gradle.kts').exists()
    assert (android_root / 'app' / 'src' / 'main' / 'java' / 'com' / 'hyperflow' / 'app' / 'MainActivity.kt').exists()
    assert not (REPO_ROOT / 'hyperflow_platform').exists()
