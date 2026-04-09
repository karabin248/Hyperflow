# Agent Runtime Promotion Gates

## Purpose

This document defines the **promotion-gate contract** for the Hyperflow agent-runtime layer.

Promotion gates exist so agent-runtime features can approach baseline relevance only through an explicit, test-backed review. They are **not** a silent promotion path and they do **not** redefine the canonical Hyperflow baseline.

## Scope

Promotion gates are **agent-runtime layer only**.

They apply to extension features such as:
- handoff fragments
- worker execution contracts
- delegation-policy profiles
- workflow presets

They do **not** grant canonical status by themselves.

## Boundary rule

A promotion gate may record that a feature is ready for review, but it must still preserve:
- the canonical `🌈💎🔥🧠🔀⚡` cycle
- baseline `/v1/run` authority
- explicit separation between baseline and agent-runtime behavior

Promotion gates must never be treated as automatic promotion.

## Contract

Each gate declares:
- `target_kind`
- `target_id`
- `classification`
- `required_checks`
- `validated_checks`
- `min_observed_runs`
- `reversible`
- `relationship_to_baseline`
- `promotion_target`

## Review result

A promotion review returns:
- gate identity
- target kind/id
- current classification
- relationship to baseline
- current status
- missing checks
- observed runs
- minimum observed runs
- reversibility
- blockers

## Status model

Promotion reviews use the following statuses:
- `not_promoted`
- `needs_evidence`
- `ready_for_review`
- `blocked`

`ready_for_review` means the feature has met its declared gate conditions and can be considered in an explicit architecture review.

It does **not** mean the feature is baseline truth.

## Current built-in gates

The default agent runtime registers explicit gates for:
- `agent_runtime_handoff` fragments
- worker execution contracts
- delegation profiles
- workflow presets

These gates make promotion criteria durable and observable without routing canonical `/v1/run` through the agent runtime.


## Operator-facing gate snapshots

Promotion-review exports now include `gate_snapshots` for the current built-in gates.

Each snapshot reports:
- `gate_id`
- `target_kind`
- `target_id`
- `current_status`
- `required_checks`
- `validated_checks`
- `missing_checks`
- `observed_runs`
- `minimum_observed_runs`
- `profile_trace_summary_count`
- `recent_profile_task_trace_summaries`
- `worker_attempt_rollups`
- `mixed_status_repeated_run_summary`
- `reversible`
- `blockers`

These snapshots are review evidence only. They do **not** silently promote the target and they do **not** change canonical `/v1/run` authority.

Delegation-profile gate snapshots may also include `profile_trace_summary_count` and `recent_profile_task_trace_summaries` so operator review can inspect real framework-attached trace summaries instead of relying on doc-only profile claims.

Each profile trace summary may record:
- `task_id`
- `task_type`
- `delegation_profile_id`
- `delegation_mode`
- `option_roles_considered`
- `selected_role`
- `delegation_targets`
- `worker_attempts`
- `retries_scheduled`
- `failures_recorded`
- `trace_event_count`
- `event_type_counts`
- `audit_ready`
- `promotion_review_ready`

These fields are review evidence only. They are persisted above the canonical baseline path and do **not** create a second delegation controller.

Promotion-review exports may also include a `repeated_run_stress_summary` in the broader analysis surface so operators can inspect coordination drift and mixed observer windows across the full repeated-run window instead of trusting only the latest pairwise comparison.

Workflow-fragment compatibility summaries may also include a nested `workflow_budget_evidence_summary` so operator review can inspect bounded delegated workflow windows without treating workflow budget ceilings as baseline execution truth.

That budget summary may record:
- `budget_evidence_present`
- `bounded_run_count`
- `unbounded_run_count`
- `budget_ceiling_values`
- `latest_delegation_budget_ceiling`
- `latest_delegation_budget_used`
- `latest_delegation_budget_remaining`
- `latest_budget_usage_visible`
- `latest_budget_remaining_visible`
- `budget_window_visibility_complete`
- `budget_window_consistent`

These fields are review evidence only. They summarize persisted workflow-budget metadata already carried by the framework/agent-runtime attachment layer. They do **not** create a second workflow controller and they do **not** redefine canonical `/v1/run` authority.

That stress summary may record:
- `coordination_signature_count`
- `coordination_signatures`
- `coordination_drift_detected`
- `task_owner_windows`
- `mixed_observer_window_detected`
- `observer_status_windows`
- `mixed_observer_tasks`
- `stable_repeated_run_window`

These fields are review evidence only. They do **not** create a second coordination runtime and they do **not** redefine canonical Observer semantics.

## Promotion status

Current status: **not promoted**


Workflow-preset and multi-stage delegated-run reviews may also include a workflow-to-fragment compatibility summary so operator review can compare staged coordination against fragment contract expectations without promoting that behavior into baseline truth.

That compatibility summary may include a nested `retry_outcome_summary` so operators can see whether retry-shaped failure-policy actions produced visible recovered or terminal outcomes inside the workflow review surface. This remains evidence only and does not promote retry behavior into baseline canon.

Worker-contract gate snapshots may also include compact `worker_attempt_rollups` so operators can inspect repeated-run attempt pressure without treating those rollups as canonical runtime truth.

Each rollup records:
- `role_id`
- `task_ids`
- `observed_runs`
- `explicit_attempt_count`
- `inferred_min_attempt_count`
- `max_inferred_attempts_per_run`
- `retry_policy_hit_count`
- `terminal_failure_count`
- `attempt_counts_visible`
- `attempt_pressure`

These rollups are review evidence only. They are inferred from persisted agent-runtime traces, results, failures, and retry-shaped policy actions. They do **not** create a second worker runtime and they do **not** redefine baseline execution semantics.


Gate snapshots may also include a `mixed_status_repeated_run_summary` so operator review can distinguish repeated-run blockers that are still visible across the persisted window even when the latest pairwise comparison is already back to `completed`.

That summary may record:
- `status_sequence`
- `distinct_statuses`
- `latest_status`
- `completed_runs`
- `failed_runs`
- `blocking_statuses`
- `mixed_status_window_detected`
- `blocked`

These fields are review evidence only. They summarize persisted repeated-run status windows above the canonical baseline and do **not** create a second execution authority.
