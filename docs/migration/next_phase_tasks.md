# Hyperflow MVP — Next Phase Task Pack

## Current verified state
Completed and verified:
- single active package root: `hyperflow`
- canonical `/v1/run` path preserved
- observability surface added:
  - `GET /v1/checkpoints`
  - `GET /v1/logs/recent`
- inventory routes remain deferred donor/product surface:
  - `GET /v1/agents`
  - `GET /v1/workflows`
- env-first config lookup added
- focused validation passed: 35 tests

## Purpose of this pack
This pack turns the current MVP state into the next executable task sequence.
The goal is to continue safely without re-opening core runtime convergence.

## Priority order
1. Android shell import
2. Worker surface absorption as metadata/stubs only
3. Checkpoint identity convergence
4. Archive/docs cleanup
5. Release hardening

---

## PR-04 — Android Shell Import

### Goal
Import the Android shell from the platform donor into `apps/android/` without coupling it to a second backend runtime.

### Scope
- create `apps/android/`
- copy Android project skeleton from `hyperflow-platform-canonical-1`
- rewrite package references only if required for build hygiene
- add a minimal README describing current non-goals
- do not wire live backend auth, workers, or parallel contracts yet

### Touched areas
- `apps/android/**`
- `docs/migration/donor_matrix.md`
- `docs/contracts/mobile_contract.md`

### Acceptance criteria
- Android shell exists under `apps/android/`
- no top-level `hyperflow_platform` backend package is introduced
- backend tests remain green
- no backend runtime behavior changes

### Tests
- file integrity / project tree smoke
- if Gradle wrapper exists: basic project parse task only
- backend focused regression subset still passes

### Rollback
Remove `apps/android/` and related docs only.

---

## PR-05 — Worker Surface Absorption (Metadata/Stubs)

### Goal
Absorb worker concepts into the canonical repo without introducing a second orchestrator or live worker execution system.

### Scope
- create `hyperflow/platform/workers/`
- port worker metadata or stub definitions only:
  - `research_worker`
  - `reasoning_worker`
  - `reporting_worker`
  - `tools_worker`
- expose workers only through inventory/metadata if useful
- do not connect workers into `/v1/run`
- do not create a scheduler, queue, or new planner

### Touched areas
- `hyperflow/platform/workers/**`
- `hyperflow/platform/inventory.py`
- optional new tests under `tests/integration/`

### Acceptance criteria
- workers exist as canonical metadata/stubs
- inventory remains singular and repo-owned
- no second execution path appears
- `/v1/run` remains unchanged

### Tests
- import smoke for worker modules
- inventory response regression
- `/v1/run` parity regression

### Rollback
Remove `hyperflow/platform/workers/` and worker inventory entries only.

---

## PR-06 — Checkpoint Identity Convergence

### Goal
Converge checkpoint lookup from file-name identity toward a stable runtime-linked identity model.

### Why
Current checkpoint detail lookup is intentionally file-based. That is safe for MVP but weak for future workflow/history APIs.

### Scope
- inspect current checkpoint persistence flow
- add an internal mapping layer from `run_id` to checkpoint identity where possible
- keep backward compatibility with existing file-based lookup
- do not redesign storage wholesale

### Touched areas
- `hyperflow/checkpoint/history.py`
- `hyperflow/checkpoint/snapshot.py`
- `hyperflow/memory/traces.py`
- `hyperflow/api/routes_checkpoints.py`
- tests for run/checkpoint association

### Acceptance criteria
- a run-generated checkpoint can be referenced by stable logical identity
- existing list endpoints still work
- no storage migration is required for current seed artifacts

### Tests
- run -> checkpoint association regression
- checkpoint listing compatibility
- recent logs/checkpoints parity

### Rollback
Disable the mapping layer and fall back to file-name identity.

---

## PR-07 — Archive and Docs Cleanup

### Goal
Reduce cognitive noise without touching runtime behavior.

### Scope
- classify remaining docs into:
  - active runtime docs
  - migration docs
  - archive-only docs
- move narrative or duplicate overlays out of active docs paths when safe
- keep executable truth docs visible
- do not delete evidence; archive it

### Touched areas
- `docs/**`
- `archive/**`
- `README.md`

### Acceptance criteria
- one clear active documentation path exists
- migration history remains preserved
- runtime commands in README still match reality

### Tests
- README command smoke
- repo hygiene tests if applicable

### Rollback
Restore moved docs from archive.

---

## PR-08 — Release Hardening

### Goal
Make the repo easier to ship without broad architectural change.

### Scope
- verify wheel/sdist smoke continuously in CI
- ensure packaged resources cover contract golden and configs required at runtime
- review test extras and build metadata for completeness
- optionally add a simple release checklist doc

### Touched areas
- `pyproject.toml`
- `MANIFEST.in`
- `.github/workflows/ci.yml`
- `docs/architecture/authority_map.md`

### Acceptance criteria
- sdist/wheel smoke remains green
- packaged resource assumptions are explicit and tested
- no hidden dependency gap remains for API-focused tests

### Tests
- build wheel
- build sdist
- install built artifacts
- smoke import + version + selected API tests

### Rollback
Revert packaging-only changes.

---

## Suggested execution order
- PR-04 Android shell import
- PR-05 worker metadata/stubs
- PR-06 checkpoint identity convergence
- PR-07 archive/docs cleanup
- PR-08 release hardening

## Stop conditions
Pause and reassess if any of these happens:
- `/v1/run` output shape changes unexpectedly
- a second runtime path appears
- inventory starts depending on worker execution
- Android import drags backend contracts into a second namespace
- checkpoint changes require destructive storage migration
