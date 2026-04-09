# Agent Runtime Workflow Presets Contract

Workflow presets are an **agent-runtime layer only** coordination surface above the canonical Hyperflow v0.2.0 baseline.

They exist to provide bounded multi-stage coordination shapes without routing canonical `/v1/run` through the agent runtime.

## Scope

Workflow presets may:
- sequence multiple agent-runtime task runs
- bind each stage to an explicit delegation profile
- carry forward prior stage output as bounded workflow context
- emit a workflow-scoped handoff fragment
- support explicit reversion of workflow-scoped active state

Workflow presets must not:
- redefine the canonical baseline cycle
- replace baseline MPS/EDDE authority
- create a second hidden runtime spine
- silently promote workflow behavior into baseline truth

## Required fields

Each workflow preset must declare:
- `id`
- `description`
- `stages`
- `reversible`
- `classification`
- `relationship_to_baseline`

Each stage must declare:
- `id`
- `delegation_profile_id`
- `description`

Optional workflow/run controls:
- `delegation_budget_ceiling`

Optional per-stage controls:
- `option_roles`
- `preferred_option_role`

## Runtime behavior

A workflow preset run returns:
- `workflow_run_id`
- `task_id`
- `baseline_authority`
- `workflow_preset`
- `stage_runs`
- `final_output`
- `workflow_fragment`
- `reverted`
- `delegation_budget_ceiling` when declared
- `delegation_budget_remaining` on stage outputs when bounded

The workflow fragment uses the same fragment standard as the agent-runtime handoff:
- `standard = hyperflow-fragment/v1`
- `kind = agent_runtime_workflow_handoff`

## Reversion model

Workflow preset reversion is bounded and explicit.

Reversion:
- marks the workflow run as reverted
- removes the active workflow fragment from workflow-scoped memory
- preserves stage-level traces and task results for audit

This keeps the layer reversible enough for controlled development without pretending the workflow layer is baseline canon.


## Operator review compatibility summary

Promotion-review exports now include a workflow-to-fragment compatibility summary under:
- `analysis.workflow_fragment_compatibility`

This summary is evidence only. It helps operators judge whether a coordinated multi-stage run still looks compatible with the fragment handoff contract and broader baseline-style output cues without claiming canonical `/v1/run` authority.

Current fields include:
- `fragment_standard`
- `fragment_kind`
- `stage_count`
- `completed_stage_count`
- `stage_task_ids`
- `preserves_canonical_cycle`
- `baseline_authority_preserved`
- `baseline_run_ids_present`
- `selected_option_present`
- `summary_present`
- `baseline_output_cues`
- `retry_outcome_summary`
- `workflow_budget_evidence_summary`
- `compatible_with_fragment_contract`
- `compatible_with_baseline_output_expectations`

The nested `retry_outcome_summary` is evidence only. It reports whether persisted workflow-fragment review data contains retry-shaped policy actions, which task ids they touched, and whether those retries ended in a visible recovered or terminal outcome. It does **not** create a second retry engine and it does **not** redefine canonical `/v1/run` semantics.

The nested `workflow_budget_evidence_summary` is also evidence only. It reports whether persisted workflow review windows contain bounded delegated runs, which budget ceilings were observed, whether the latest bounded run exposed `delegation_budget_used` / `delegation_budget_remaining`, and whether the bounded window stays internally consistent. It does **not** create a second coordination authority and it does **not** redefine canonical `/v1/run` semantics.

Current budget-evidence fields may include:
- `latest_delegation_budget_ceiling`
- `latest_delegation_budget_used`
- `latest_delegation_budget_remaining`
- `budget_window_visibility_complete`
- `budget_window_consistent`


## Delegation budget ceilings

Workflow-scoped coordination may declare an optional `delegation_budget_ceiling`.

Rules:
- the ceiling is a positive integer when present
- the ceiling is enforced by the agent-runtime attachment layer before each delegated stage
- the ceiling bounds only delegated agent stages inside the workflow run
- the ceiling does not redefine canonical baseline execution semantics
- exceeding the ceiling blocks the next delegated stage and leaves prior traces intact
