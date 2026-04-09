# Hyperflow Agent Runtime — Profile Trace Summaries

Profile-to-task trace summaries are an **agent-runtime layer only** audit surface.

They exist to make delegation-profile behavior easier to compare for:
- promotion review
- runtime audits
- operator inspection

They do **not** redefine baseline MPS semantics. They must not redefine baseline MPS semantics.
They do **not** route canonical `/v1/run` through the agent runtime.

## Current summary fields

Each task run now stores a structured summary under `record.trace.profile_task_trace_summaries` and framework-attached agent outputs return the task-local copy as `profile_task_trace_summary`.

Current fields include:
- `run_id`
- `task_id`
- `task_type`
- `delegation_profile_id`
- `delegation_mode`
- `option_roles_considered`
- `selected_role`
- `next_owner`
- `delegation_targets`
- `worker_attempts`
- `retries_scheduled`
- `failures_recorded`
- `reporting_used`
- `research_used`
- `trace_event_count`
- `event_type_counts`
- `audit_ready`
- `promotion_review_ready`

## Purpose

These summaries are meant to answer:
- which delegation profile shaped the task
- which roles were actually used
- how many retries or failures occurred
- whether reporting/research happened
- whether the trace is usable for promotion review

## Promotion-review use

Delegation-profile promotion reviews now include:
- `trace_summary_count`
- `recent_trace_summaries`

This keeps profile audits explicit without promoting agent-runtime policy behavior into baseline authority.

## Current framework-attached defaults

For framework-attached agent nodes, the current runtime records:
- `delegation_profile_id = framework_agent_bridge`
- `delegation_mode = framework_attached`
- `task_type = framework_agent`

These defaults are audit labels above the baseline. They do **not** redefine baseline MPS or create a second framework runtime.
