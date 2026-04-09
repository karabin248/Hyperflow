#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$ROOT_DIR"

export PYTEST_DISABLE_PLUGIN_AUTOLOAD=${PYTEST_DISABLE_PLUGIN_AUTOLOAD:-1}
export PYTHONDONTWRITEBYTECODE=${PYTHONDONTWRITEBYTECODE:-1}

bash scripts/clean_repo.sh >/dev/null 2>&1 || true

python -m pytest -q hyperflow/tests \
  --ignore=hyperflow/tests/test_built_sdist_smoke.py \
  --ignore=hyperflow/tests/test_built_wheel_smoke.py

python -m pytest -q tests
