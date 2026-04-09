#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$ROOT_DIR"

BUILD_ARTIFACTS=false
if [[ "${1:-}" == "--build" ]]; then
  BUILD_ARTIFACTS=true
fi

echo "== preflight cleanup =="
bash scripts/clean_repo.sh --deep

echo "== install editable package + extras =="
if ! python3 -m pip install -e ".[api,test]"; then
  echo "WARNING: editable install failed; continuing with in-repo module checks."
  echo "WARNING: this is usually caused by offline/proxy-restricted environments."
fi

echo "== entrypoints =="
if command -v hyperflow >/dev/null 2>&1; then
  hyperflow --version
else
  echo "WARNING: 'hyperflow' console script not found; skipping CLI entrypoint binary check."
fi
python3 -m hyperflow --version
python3 -m hyperflow.interface.cli --version

echo "== canonical smoke =="
if command -v hyperflow >/dev/null 2>&1; then
  hyperflow --pretty "🌈💎🔥🧠🔀⚡ runtime contract health check"
else
  python3 -m hyperflow.interface.cli --pretty "🌈💎🔥🧠🔀⚡ runtime contract health check"
fi

echo "== status report =="
if command -v hyperflow >/dev/null 2>&1; then
  hyperflow --status-report
else
  python3 -m hyperflow.interface.cli --status-report
fi

echo "== release verify =="
python3 -m hyperflow.release_verify --pretty

echo "== compile =="
python3 -m compileall -q hyperflow

echo "== regression tests =="
bash scripts/test_suite.sh

echo "== packaging smoke =="
bash scripts/packaging_smoke.sh

if [[ "$BUILD_ARTIFACTS" == true ]]; then
  echo "== build =="
  python3 -m build
  echo "== source zip =="
  python3 scripts/make_source_zip.py
fi
