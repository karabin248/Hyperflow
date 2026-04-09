#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$ROOT_DIR"

if python3 -m pip install -e ".[api,test]"; then
  exit 0
fi

if [[ "${HYPERFLOW_STRICT_INSTALL:-0}" == "1" ]]; then
  echo "error: editable install failed and strict install is enabled" >&2
  exit 1
fi

echo "warning: editable install failed; falling back to source-checkout mode" >&2
if python3 -m hyperflow --version >/dev/null 2>&1; then
  echo "fallback check passed: hyperflow is runnable from source checkout"
  exit 0
fi

echo "error: fallback check failed; hyperflow cannot run from source checkout" >&2
exit 1
