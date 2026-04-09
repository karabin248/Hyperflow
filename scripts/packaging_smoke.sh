#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$ROOT_DIR"

HEAVY_TIMEOUT_SECONDS=${HEAVY_TIMEOUT_SECONDS:-180}
export PYTEST_DISABLE_PLUGIN_AUTOLOAD=${PYTEST_DISABLE_PLUGIN_AUTOLOAD:-1}

run_smoke() {
  local label="$1"
  local test_path="$2"

  echo "== packaging smoke: ${label} =="
  if [[ "${HF_PACKAGING_USE_TIMEOUT:-0}" == "1" ]] && command -v timeout >/dev/null 2>&1; then
    timeout --foreground "${HEAVY_TIMEOUT_SECONDS}"s python -m pytest -vv -s "$test_path"
  else
    python -m pytest -vv -s "$test_path"
  fi
  bash scripts/clean_repo.sh --deep >/dev/null 2>&1 || true
}

if [[ "${1:-}" == "--clean" ]]; then
  bash scripts/clean_repo.sh --deep
fi

echo "== packaging smoke: build artifacts =="
BUILD_LOG=$(mktemp)
if ! python -m build --sdist --wheel >"$BUILD_LOG" 2>&1; then
  cat "$BUILD_LOG"
  rm -f "$BUILD_LOG"
  exit 1
fi
rm -f "$BUILD_LOG"

run_smoke "sdist" "hyperflow/tests/test_built_sdist_smoke.py"
run_smoke "wheel" "hyperflow/tests/test_built_wheel_smoke.py"

if find . -type d -name '*.egg-info' -print -quit | grep -q .; then
  echo "packaging smoke failed: stray egg-info left in repo"
  exit 1
fi

echo "packaging smoke: PASS"
