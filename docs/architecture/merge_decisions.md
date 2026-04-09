# Merge Decisions

Status: confirmed
Confidence: high

## Accepted

1. Hyperflow MVP Runtime Baseline is explicitly scoped as MVP Core + Runtime Shell + Minimal Orchestration Layer.
2. The canonical cycle is `🌈💎🔥🧠🔀⚡`.
3. Legacy order may remain only as deprecated backward compatibility, never as canon.
4. The canonical runtime path is CLI / API entry → command construction → runtime kernel execution → output / persistence.
5. Public MVP API remains runtime-backed only: `/health`, `/v1/run`, `/v1/checkpoints*`, and `/v1/logs/recent`.
6. `/v1/agents` and `/v1/workflows` are deferred donor/product surface and are not mounted in the canonical MVP app.
7. Generated runtime artifacts and `hyperflow.egg-info/` are not baseline source truth and must not be committed.
8. Definition of done, canonical core, and runtime contract are locked as active docs under `docs/`.

## Rejected

1. A second parser, second CLI authority, or second orchestration spine.
2. Treating platform/product inventory routes as part of the MVP public API.
3. Treating committed traces, checkpoints, graph memory, or knowledge payloads as canonical source material.
4. Broad runtime redesign while baseline hardening is the main goal.

## Validation status

- code path smoke: required
- repo hygiene: required
- packaging integrity: required
- core runtime regression subset: required

## Change classification

This decision set is **canonical** for the current MVP Runtime Baseline stage.

## 2026-03-23 baseline hardening record

- what changed: added guard tests for exact mounted MVP API surface and shared CLI/API runtime authority.
- why it changed: to prevent drift into deferred donor routes or alternate entrypoint/runtime authority.
- classification: Core Runtime
- validation result: targeted hardening tests and integration surface passed locally.
- status labels: canonical runtime preserved, confirmed API surface, confirmed shared authority, deferred donor routes remain non-canonical.



## 2026-03-23 canonical cycle authority hardening record

- what changed: added regression guards that keep the reversed-tail full cycle `🌈💎🔥🧠⚡🔀` backward-compatible but explicitly non-canonical, and aligned docs assertions around that rule.
- why it changed: to stop accidental re-canonization of the deprecated legacy full-cycle alias while preserving compatibility.
- classification: Core Runtime
- validation result: targeted parser/docs regression tests passed locally along with the core runtime/integration guard set.
- status labels: canonical cycle preserved, legacy alias confirmed, non-canonical status confirmed, docs/runtime alignment strengthened.


## 2026-03-23 public api docs alignment hardening record

- what changed: aligned `docs/architecture/canonical_runtime.md` with the exact mounted MVP API surface and added regression guards that keep README, authority map, canonical runtime, and API contract docs in sync.
- why it changed: to prevent docs drift around the public API boundary and reinforce that archive/generated runtime material is reference/output only, not canonical source truth.
- classification: Core Runtime
- validation result: targeted docs, API-surface, packaging, and integration regression tests passed locally.
- status labels: API boundary confirmed, docs/runtime alignment strengthened, archive/reference-only rule confirmed.


## 2026-03-23 source tree hygiene hardening record

- what changed: removed committed `__pycache__/`, compiled Python artifacts, and `hyperflow.egg-info/` from the source tree, and added regression guards that fail if those generated artifacts return.
- why it changed: the uploaded v0.2.0 baseline summary states those artifacts were removed, but the shipped source zip still contained them, so the baseline package needed to match its own hygiene claims.
- classification: Core Runtime
- validation result: repo hygiene, packaging smoke, and targeted core/runtime integration checks passed locally after cleanup.
- status labels: source tree cleaned, hygiene contract strengthened, baseline package aligned with summary.


## 2026-03-23 — shipped generated artifact cleanup + hygiene cutoff hardening
- classification: Core Runtime
- what changed: removed committed `__pycache__/`, `.pyc` / `.pyo`, and any `*.egg-info` from the v0.2.0 source tree; replaced the fragile time-minus-10-seconds hygiene cutoff with a test-session start marker.
- why it changed: the uploaded operational-hardened zip still contained shipped generated Python artifacts, and the hygiene guardrail needed to distinguish packaged debris from artifacts created during the current test session.
- validation: repo hygiene passes on the cleaned tree; broader canonical regression rerun after cleanup.
- status labels: hygiene mismatch fixed, source tree cleaned, regression guardrail strengthened.


## 2026-03-23 — future-layer package marker + authority-boundary hardening
- classification: Core Runtime
- what changed: added explicit non-canonical package markers to `hyperflow/framework` and `hyperflow/platform`, strengthened authority docs around archive/generated outputs and explicit promotion, and added regression tests for those rules.
- why it changed: the uploaded v0.2.0 hardened baseline still lacked package-level demotion markers and left authority-boundary wording weaker than the intended controlled-expansion policy.
- validation: targeted authority/docs/runtime guard subsets passed locally after the patch.
- status labels: single runtime spine preserved, future-layer demotion clarified, controlled expansion guardrails strengthened.


## 2026-03-23 — future-layer import-boundary guard hardening
- classification: Core Runtime
- what changed: added regression tests that block canonical entrypoints from importing `hyperflow.framework` or `hyperflow.platform`, and verified that CLI/API still share `runtime_kernel.run()` as the single runtime authority.
- why it changed: the v0.2.0 baseline still had future-layer code present in the repo but lacked an explicit anti-drift guard on canonical runtime imports.
- validation: targeted authority, docs, hygiene, runtime, and mounted API regression subsets passed locally after the patch.
- status labels: one runtime spine preserved, future-layer boundary enforced, controlled expansion guardrail strengthened.

## 2026-03-23 — Deferred surface boundary markers

- classification: Core Runtime
- change type: hardening / docs-runtime-tests alignment
- scope:
  - added explicit deferred-route markers to `hyperflow/api/routes_agents.py` and `hyperflow/api/routes_workflows.py`
  - tightened `hyperflow/platform/workers/__init__.py` so worker specs stay inventory-only metadata
  - strengthened `docs/architecture/platform_surface.md` to require an explicit promotion decision for deferred public routes
  - added regression coverage for deferred-surface markers
- why:
  - deferred donor/product surfaces were already unmounted, but the modules themselves were not marked strongly enough against quiet promotion
- validation:
  - targeted boundary subset passes
- status: accepted

## 2026-03-23 — Repo hygiene cleanup for committed egg-info

- classification: Core Runtime
- change type: repo hygiene / minimal-diff patch
- scope:
  - removed committed `hyperflow.egg-info` from the canonical baseline tree
  - validated that repo hygiene catches the condition and passes once cleaned
- why:
  - the guarded v0.2.0 zip still shipped generated packaging metadata, which violated the baseline repo-hygiene contract
- validation:
  - canonical hardening subset passes after removal
- status: accepted


## 2026-03-23 — agent runtime candidate attachment v1

- classification: Agent runtime candidate
- change type: next-layer architecture / minimal executable slice
- scope:
  - added `hyperflow/agent_runtime/*` with explicit contracts, registry, delegation planner, coordinator, and baseline-backed worker adapter
  - reused inventory-only worker metadata as role descriptors without promoting them into canonical runtime authority
  - added docs and tests that lock the agent layer above the baseline and block canonical entrypoints from importing it
- why:
  - the repo already contained framework and worker donor surfaces, but no real agent runtime attachment that executed delegated work through the canonical baseline path
- validation:
  - targeted framework, agent-runtime, boundary, and integration tests pass locally
- status labels: baseline preserved, agent-runtime candidate attached, no parallel canon, promotion deferred


## 2026-03-23 — agent runtime option-generation + guardrail hardening

- classification: Agent runtime candidate
- change type: next-layer architecture / validation hardening
- scope:
  - added explicit agent option contracts and option-set synthesis above delegated results
  - added delegation validation for duplicate task ids, missing dependencies, self-dependencies, and cycles
  - extended the agent-runtime track doc to state option generation and guardrail rules explicitly
- why:
  - the first candidate layer had real delegation and coordination, but it still lacked explicit cross-role option generation and stronger delegation guardrails required by the real agent-runtime track
- validation:
  - targeted agent-runtime, integration, framework, and authority-boundary tests pass locally after the patch
- status labels: baseline preserved, option generation attached, delegation guardrails strengthened, promotion deferred


## 2026-03-23 — Agent runtime trace and failure-policy hardening

- classification: agent runtime candidate
- baseline dependencies confirmed: canonical `build_command(...) -> runtime_kernel.run(...)` path remains the only execution authority
- change: added first-class agent task traces and failure-policy records; added delegated-vs-direct baseline comparison coverage
- why: delegation and coordination were already real, but failure handling and promotion evidence needed observable records above the baseline
- validation: targeted agent-runtime, integration, framework, hygiene, and packaging checks passed after the patch
- promotion status: deferred until traces, guardrails, and comparison behavior remain stable across broader validation


## 2026-03-24 — Agent runtime persistence and trace-store comparison

- classification: agent runtime candidate
- baseline dependencies confirmed: canonical `build_command(...) -> runtime_kernel.run(...)` path remains the only execution authority
- change: added agent-run persistence, file-backed agent-run snapshots, repeated-run comparison tooling, and persisted execution helpers above the baseline
- why: the candidate layer already had traces and failure-policy records, but promotion decisions still lacked a durable way to compare repeated delegated runs over time
- validation: targeted agent-runtime, persistence, integration, storage-policy, hygiene, packaging, and framework/boundary checks passed locally after the patch
- promotion status: deferred until persisted comparisons remain stable across broader validation and do not create authority drift


## 2026-03-24 — Agent runtime persistence-backed analysis and promotion evaluation

- classification: agent runtime candidate
- baseline dependency: canonical Hyperflow v0.2.0 runtime spine remains the only execution authority
- what changed: added persistence-backed analysis views and promotion-evaluation utilities above the agent-run store; extended the store with analysis and promotion-evaluation helpers; added tests and docs for evidence-backed review of repeated delegated runs
- why: repeated delegated runs could already be persisted and compared, but promotion review still depended on manual inspection rather than explicit evidence-backed utilities
- validation: agent-runtime store/integration/docs/hygiene/packaging subsets green in this pass
- promotion status: deferred until repeated-run evidence remains stable across broader validation and still shows no baseline authority drift

## 2026-03-24 — Agent runtime promotion-review exports and thresholds

- classification: agent runtime candidate
- baseline dependency: canonical Hyperflow v0.2.0 runtime spine remains the only execution authority
- what changed: added exportable promotion-review summaries, scoring thresholds, scorecards, store-backed review/export helpers, and tests for durable promotion-review artifacts above persisted delegated runs
- why: promotion evaluation utilities existed, but they still stopped short of durable review artifacts and explicit scoring thresholds for decision logging
- validation: focused agent-runtime/store/integration/framework/hygiene/packaging subsets green in this pass
- promotion status: deferred until export-backed review evidence remains stable across broader validation and still shows no baseline authority drift



## 2026-03-24 — Framework agent-node bridge to the baseline-backed agent runtime

- classification: agent runtime candidate
- baseline dependency: canonical `build_command(...) -> runtime_kernel.run(...)` path remains the only execution authority
- what changed: added a reversible framework-to-agent-runtime bridge so framework agent tasks and workflow agent nodes execute through the baseline-backed agent runtime adapter instead of returning stub-only placeholders; added role mapping, tests, and docs for the bridge boundary
- why: the framework package existed as donor/runtime material, but its agent nodes were still decorative stubs rather than real delegated execution above the baseline
- validation: targeted framework, agent-runtime, integration, hygiene, packaging, and core boundary subsets passed locally after the patch
- promotion status: deferred until the bridge remains stable across broader validation and still shows no baseline authority drift

- 2026-03-25: Routed framework agent bridge through persisted agent-runtime coordination so framework traces carry agent_run_id, delegation_plan_id, and selected_option_id without introducing a second runtime spine. Classification: agent runtime candidate. Validation: framework + agent-runtime + packaging guards green.


- 2026-03-25: framework bridge plan ids stabilized across equivalent agent/task and workflow-node runs so persisted comparison and promotion review work from framework surfaces without changing baseline authority. Classification: Agent runtime candidate. Validation: framework + agent-runtime targeted suite green.


## 2026-03-25 — Validation spine hardening for CI workflows and generated-artifact discovery

- classification: agent-runtime mainline hardening
- baseline dependency: canonical Hyperflow v0.2.0 runtime spine remains the only execution authority
- what changed: aligned both GitHub workflows to the shared `scripts/test_suite.sh` regression entrypoint and added pytest discovery guards so generated `build/`, `dist/`, `wheelhouse/`, cache, and egg-info artifacts cannot become a second accidental test surface
- why: the mainline governance already depends on shared validation entrypoints, but one workflow still used raw `pytest -q` and the repo lacked an explicit guard against generated-artifact test discovery drift after packaging/build work
- validation: targeted CI/validation tests plus the shared regression suite and release verification green after the patch
- promotion status: deferred; baseline authority unchanged, validation discipline strengthened


## 2026-03-25 — Framework-to-agent trace linkage integrity completed

- classification: agent-runtime mainline hardening
- baseline dependency: canonical `build_command(...) -> runtime_kernel.run(...)` path remains the only execution authority
- what changed: preserved `framework_run_id` plus explicit baseline-run linkage in persisted agent-runtime trace records and snapshots so framework runs can be verified end to end across framework run, agent run, delegation plan, task traces, and baseline execution
- why: the bridge already exposed `framework_run_id` in framework output, but the persisted agent-runtime record did not preserve that identifier, leaving framework-to-agent trace linkage only partial
- validation: targeted framework + agent-runtime + integration linkage tests green after the patch
- promotion status: deferred; linkage integrity improved without changing baseline authority


## 2026-03-25 — Repo hygiene hardening for generated packaging artifacts

- classification: agent-runtime mainline hardening
- baseline dependency: canonical Hyperflow v0.2.0 runtime spine remains the only execution authority
- what changed: removed committed generated packaging/build artifacts from the mainline snapshot (`dist/`, `hyperflow.egg-info`, preexisting runtime `__pycache__` / `.pyc`, and `hyperflow-v0.2.0-source.zip`) and extended `scripts/clean_repo.sh` to remove versioned source-zip artifacts during cleanup
- why: the shared validation path already guarded against committed generated debris, but the validated snapshot still contained packaging residue that made repo-hygiene fail and left the local validation path fragile after source-zip generation
- validation: repo-hygiene, shared regression suite, and packaging smoke green after cleanup
- promotion status: deferred; baseline authority unchanged, validation honesty and repo hygiene strengthened


## 2026-03-25 — Workflow-to-fragment compatibility summaries for operator review

- classification: agent-runtime mainline hardening
- baseline dependency: canonical `build_command(...) -> runtime_kernel.run(...)` path remains the only execution authority
- what changed: added workflow-to-fragment compatibility summaries to agent-runtime analysis and promotion-review exports so multi-stage delegated runs now report fragment-standard cues, baseline-output cues, canonical-cycle preservation, and baseline-authority preservation as review evidence
- why: promotion-review exports already scored repeated delegated runs, but operators still lacked a compact summary showing whether coordinated multi-stage runs remained compatible with the fragment handoff contract and broader baseline-style output expectations
- validation: targeted agent-runtime store/framework/docs subsets plus the shared regression suite green after the patch
- promotion status: deferred; baseline authority unchanged, operator review evidence strengthened


## 2026-03-25 — Workflow delegation budget ceilings above the framework/agent bridge

- classification: delegation / coordination improvement
- baseline dependency: canonical `build_command(...) -> runtime_kernel.run(...)` path remains the only execution authority
- what changed: added optional `delegation_budget_ceiling` on workflow definitions and enforced it before each delegated agent node; exposed budget fields in workflow traces and bridge outputs for bounded coordination evidence
- why: multi-stage workflow runs were real and baseline-backed, but they still lacked an explicit workflow-scoped ceiling on delegated agent stages
- validation: focused framework/docs subsets plus the shared regression suite and packaging smoke passed after the patch
- promotion status: deferred; budget ceilings remain an agent-runtime attachment guardrail above the canonical baseline


## 2026-03-25 — Operator-facing promotion gate snapshots for built-in agent-runtime gates

- classification: promotion-readiness work
- baseline dependency: canonical `build_command(...) -> runtime_kernel.run(...)` path remains the only execution authority
- what changed: added built-in promotion gate snapshots to agent-runtime promotion-review summaries and exports so operator review now records gate status, required checks, validated checks, missing checks, observed-run counts, reversibility, and blockers for handoff fragments, worker execution contracts, delegation profiles, and workflow presets
- why: promotion gates already existed in contract form, but the review/export surface still lacked a durable operator-facing snapshot showing which built-in gates were actually review-ready versus merely declared
- validation: targeted agent-runtime store/docs subsets plus the shared regression suite and packaging smoke passed after the patch
- promotion status: deferred; the patch strengthens review evidence only and does not silently promote any target into baseline truth


## 2026-03-25 — Workflow retry-outcome summaries in fragment review exports

- classification: promotion-readiness work
- baseline dependency: canonical `build_command(...) -> runtime_kernel.run(...)` path remains the only execution authority
- what changed: added a nested retry-outcome summary to workflow-to-fragment compatibility analysis and markdown/json promotion-review exports so operators can see when persisted workflow review data contains retry-shaped policy actions, which task ids they touched, and whether those retries ended in visible recovered or terminal outcomes
- why: workflow-fragment review already exposed fragment and baseline-output compatibility cues, but it still lacked an explicit place to surface retry evidence without pretending the agent-runtime layer had a separate retry engine or baseline authority
- validation: targeted agent-runtime store/docs subsets plus the shared regression suite and packaging smoke passed after the patch
- promotion status: deferred; the patch adds review evidence only and does not promote retry behavior into baseline truth


## 2026-03-25 — Compact worker-attempt rollups in promotion gate snapshots

- classification: promotion-readiness work
- baseline dependency: canonical `build_command(...) -> runtime_kernel.run(...)` path remains the only execution authority
- what changed: added compact worker-attempt rollups to promotion-gate snapshots and markdown/json review exports so worker-contract reviews now surface repeated-run attempt pressure, retry-shaped evidence, and visible multi-attempt windows without inventing a second worker runtime
- why: operator review already showed gate status and retry-shaped workflow evidence, but it still lacked a compact worker-level summary of repeated attempt pressure across persisted delegated runs
- validation: targeted agent-runtime store/docs subsets plus the shared regression suite and packaging smoke passed after the patch
- promotion status: deferred; the patch adds review evidence only and does not promote worker execution behavior into baseline truth



## 2026-03-26 — Repeated-run stress summaries for coordination drift and mixed observer windows

- classification: promotion-readiness work
- baseline dependency: canonical `build_command(...) -> runtime_kernel.run(...)` path remains the only execution authority
- what changed: added repeated-run stress summaries to agent-runtime analysis and markdown/json promotion-review exports so persisted review windows now report coordination signatures, task-owner windows, mixed observer windows, and stable-window status across the full repeated-run slice instead of relying only on the latest pairwise comparison
- why: repeated-run promotion checks already compared the latest two runs, but they could still miss coordination drift or mixed observer windows that only became visible when looking across the broader persisted run window
- validation: targeted agent-runtime store/docs subsets, framework/integration subsets, and the shared regression suite plus packaging smoke passed after the patch
- promotion status: deferred; the patch strengthens review evidence and repeated-run validation above the canonical baseline without changing baseline authority


## 2026-03-26 — Workflow-budget evidence summaries in promotion review exports

- classification: promotion-readiness work
- baseline dependency: canonical `build_command(...) -> runtime_kernel.run(...)` path remains the only execution authority
- what changed: persisted framework-attached agent traces now retain workflow delegation-budget metadata, and promotion-review analysis/markdown/json exports now surface a nested `workflow_budget_evidence_summary` so operators can inspect bounded delegated workflow windows, observed budget ceilings, latest budget usage visibility, and bounded-window consistency
- why: workflow delegation ceilings already existed at the framework/agent-runtime attachment boundary, but promotion-review exports still lacked durable evidence showing whether bounded workflow runs actually carried reviewable budget metadata across the persisted run window
- validation: targeted agent-runtime store/docs subsets, framework/integration subsets, and the shared regression suite plus packaging smoke passed after the patch
- promotion status: deferred; the patch strengthens workflow-budget review evidence above the canonical baseline without changing baseline authority


## 2026-03-26 — Gate snapshot coverage for blocked mixed-status repeated runs

- classification: promotion-readiness work
- baseline dependency: canonical `build_command(...) -> runtime_kernel.run(...)` path remains the only execution authority
- what changed: added a nested `mixed_status_repeated_run_summary` to promotion-gate snapshots and promoted mixed non-completed repeated-run windows into explicit gate blockers so operator review can see blocked status windows even when the latest pairwise comparison has already returned to `completed`
- why: repeated-run stress summaries already exposed broader window drift, but the gate layer could still collapse mixed completed/failed windows into generic missing evidence instead of an explicit blocked state
- validation: targeted agent-runtime store/docs subsets plus the shared regression suite and packaging smoke passed after the patch
- promotion status: deferred; the patch strengthens operator review evidence only and does not change baseline authority


## 2026-03-26 — framework-attached profile trace summaries persisted and surfaced

- what changed
  - persisted `profile_task_trace_summaries` in agent-runtime trace records
  - returned `profile_task_trace_summary` from framework agent bridge outputs
  - promoted delegation-profile gate evidence from doc-only claims to persisted review objects
- why it changed
  - the contracts already described profile trace summaries, but the framework-attached execution path did not actually export or validate them
  - this closes that gap above the baseline spine without changing canonical execution authority
- classification
  - Docs / Contracts Alignment
  - Promotion-Readiness Work
- validation result
  - focused framework/store/docs validation passed
  - shared regression validation passed
- status
  - baseline-safe
  - agent-runtime
  - promotion still deferred


## 2026-03-26 — Baseline qualification gate and canonical authority hardening
- what changed: removed the canonical EDDE schema validator dependency on `hyperflow.framework.errors`, added a baseline-owned schema validation error, introduced `core/BASELINE_QUALIFICATION_GATE.md` plus `scripts/baseline_qualification.sh` / `make baseline-qualify`, and tightened canonical authority docs/tests around runtime shell, reasoning authority, control authority, and the rule that no new canonical behavior may emerge outside the baseline qualification gate
- why: baseline qualification still had a real future-layer dependency in a canonical contract path and lacked a single explicit gate that future merges must satisfy before claiming new canonical behavior
- classification: Boundary Protection; Docs / Contracts Alignment
- validation: focused boundary/docs/contract checks, the new baseline qualification gate, and the shared regression suite passed after the patch
- status: baseline-safe; promotion deferred

## 2026-03-26 — baseline qualification expanded for core trace / checkpoint authority
- what changed: expanded `make baseline-qualify` / `scripts/baseline_qualification.sh` to cover trace persistence, trace contract capture, checkpoint history, runtime storage policy, observability routes, and checkpoint identity; added boundary tests that keep canonical trace/checkpoint modules and routes future-layer free; tightened baseline docs so core trace / core checkpoint truth is explicitly baseline-owned
- why: the prior baseline gate named trace/checkpoint authority but still treated it mostly as implied behavior instead of an explicit qualification surface with direct regression coverage
- classification: boundary protection; docs/contracts alignment
- validation: focused baseline boundary/docs checks, the expanded baseline qualification gate, the shared regression suite, packaging smoke, and post-build hygiene all passed
- status: baseline-safe; promotion deferred

- what changed: expanded the baseline qualification gate and authority docs/tests to explicitly freeze parser/control, MPS, and output-contract authority inside the canonical baseline, and added boundary assertions that these baseline-owned modules stay future-layer free.
- why it changed: semantic hardening for the canonical baseline needed stronger explicit proof that parser/control, MPS, and output-contract behavior qualify only through the baseline gate rather than by implication.
- classification: Boundary Protection; Docs / Contracts Alignment.
- validation result: baseline docs/alignment and runtime-authority boundary tests passed along with the baseline qualification gate, shared suite, packaging smoke, and post-build repo hygiene checks.
- status labels: baseline-safe, canonical authority freeze tightened, promotion still deferred.


- date: 2026-03-26
- classification: Boundary Protection
- what changed: moved emoji action routing and action registry helpers used by canonical parser/control and EDDE execution into baseline-owned `hyperflow.language.action_router` and `hyperflow.engine.action_registry`, leaving `hyperflow.extensions.*` as compatibility wrappers only; tightened baseline boundary tests/docs so canonical modules may not import `hyperflow.extensions` and baseline qualification now treats action routing/execution as baseline-owned semantics.
- why it changed: the canonical command-builder and EDDE execution path still depended on `hyperflow.extensions/*`, which left baseline behavior emerging from outside the declared canonical spine even after the qualification gate was introduced.
- validation: `python -m pytest -q hyperflow/tests/test_runtime_authority_boundaries.py hyperflow/tests/test_baseline_docs_alignment.py hyperflow/tests/test_emoji_action_router.py`; `bash scripts/baseline_qualification.sh`; `bash scripts/test_suite.sh`
- status labels: baseline-safe, canonical dependency boundary tightened, semantic freeze closer to closure, promotion still deferred.


## 2026-03-26 — Canonical cycle semantic drift fix for 🌈💎🔥🧠🔀⚡

- classification: Boundary Protection
- change type: baseline semantic hardening / minimal-diff patch
- scope:
  - aligned `canonical_signature` with the canonical combo registry for `🌈💎🔥🧠🔀⚡`
  - stopped `canonical_signature` from silently overriding combo-registry parser semantics when the same emoji already exists in the canonical combo registry
  - refreshed the runtime contract golden and added direct parser/run-trace regression coverage for the canonical cycle order
- why:
  - the repo had a real semantic drift where the canonical combo declared `remix -> deliver`, but `canonical_signature`, parser output, and the contract golden were preserving `deliver -> remix`
- validation:
  - targeted parser/config/trace/runtime guard subset green; baseline qualification and shared suite rerun after the fix
- status labels: canonical cycle semantics aligned, parser source-of-truth hardened, golden contract corrected

## 2026-03-26 — Canonical signature removed from parser sequence resolution

- what changed
  - removed `canonical_signature` from `get_emoji_parser_sequences()` so parser resolution now derives combo semantics only from `combo_registry`
  - removed `canonical_signature` from combo-sequence audit classification
  - added a config-layer regression proving `canonical_signature` does not participate in parser sequences
  - added a runtime-level regression proving `🌈💎🔥🧠🔀⚡` preserves `scan -> extract -> build -> reason -> remix -> deliver` through command build and EDDE contract output
- why it changed
  - the semantic drift root cause was not just mismatched data; it was allowing `canonical_signature` to exist on the parser sequence path at all
  - the baseline canon should keep `canonical_signature` as a descriptive marker, not a second parser metadata source
- classification
  - Boundary Protection
  - Docs / Contracts Alignment
- validation result
  - `python -m pytest -q hyperflow/tests/test_config_layer.py hyperflow/tests/test_emoji_parser.py hyperflow/tests/test_runtime_kernel.py hyperflow/tests/test_run_trace_golden.py` → 38 passed
  - `bash scripts/baseline_qualification.sh` → 103 passed, 1 skipped
  - `bash scripts/test_suite.sh` → 216 passed, 1 skipped, plus tests/ phase 16 passed
  - `python -m pytest -q hyperflow/tests/test_built_sdist_smoke.py hyperflow/tests/test_built_wheel_smoke.py` → 2 passed
  - `python -m pytest -q hyperflow/tests/test_repo_hygiene.py` → 11 passed
- status
  - baseline-safe

