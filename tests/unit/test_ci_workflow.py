from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
CI_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "ci.yml"
PACKAGE_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "python-package.yml"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_ci_workflows_use_packaged_install_path() -> None:
    for workflow in (CI_WORKFLOW, PACKAGE_WORKFLOW):
        text = _read(workflow)
        assert 'python -m pip install -e ".[api,test]"' in text


def test_ci_workflows_use_shared_regression_entrypoint() -> None:
    for workflow in (CI_WORKFLOW, PACKAGE_WORKFLOW):
        text = _read(workflow)
        assert 'bash scripts/test_suite.sh' in text
        assert 'pytest -q' not in text


def test_ci_workflow_install_path_matches_packaged_runtime() -> None:
    for workflow in (CI_WORKFLOW, PACKAGE_WORKFLOW):
        text = _read(workflow)
        assert "environment.yml" not in text
        assert "conda env update" not in text
        assert "conda install pytest" not in text
