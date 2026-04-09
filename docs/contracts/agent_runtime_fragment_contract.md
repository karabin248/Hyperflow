# Agent Runtime Fragment Handoff Contract

This document defines the **fragment-shaped handoff object** emitted by the agent-runtime layer.

It is an extension-layer contract. It does **not** replace the canonical baseline output contract and it does **not** route canonical `/v1/run` through the agent runtime.

## Purpose

The handoff fragment gives the agent-runtime layer a stable, baseline-aligned structured output object for:
- selected option handoff
- reporting output handoff
- traceable runtime result storage
- future reversible integration with broader fragment-oriented runtime outputs

## Standard

- `standard`: `hyperflow-fragment/v1`
- `kind`: `agent_runtime_handoff`

## Required fields

- `standard`
- `kind`
- `run_id`
- `task_id`
- `baseline_authority`
- `canonical_cycle`
- `coordinator_role`
- `selected_role`
- `next_owner`
- `options_considered`
- `summary`
- `payload`
- `metadata`

## Boundary rules

- `baseline_authority` must remain the canonical Hyperflow baseline
- `canonical_cycle` remains `🌈💎🔥🧠🔀⚡`
- the fragment is a **handoff object above baseline**, not a new canonical runtime output path
- canonical CLI/API entrypoints must remain free of `hyperflow.agent_runtime` imports unless explicitly promoted

## Metadata expectations

The current agent-runtime handoff metadata includes:
- `task_type`
- `preferred_option_role`
- `reporting_role`
- `selected_worker_id`
- `classification`
- `attaches_above_baseline`
- `delegation_profile_id`
- `delegation_mode`

## Current status

- classification: **Baseline-safe extension candidate**
- promotion status: **not promoted**
- validation status: **test-backed in `hyperflow/tests/test_agent_runtime.py`**


## Compatibility summary

The runtime now records a fragment compatibility summary for each handoff fragment under:
- `agent_runtime.fragment_compatibility`

This summary is intentionally modest. It proves that the agent-runtime fragment preserves broader baseline output cues without claiming to be a canonical `/v1/run` result.

Current checks include:
- `standard_matches_declared_fragment_standard`
- `preserves_canonical_cycle`
- `required_fragment_fields_present`
- `baseline_output_cues` for `kind`, `summary`, and `run_id`
- `payload_summary_matches_fragment_summary`
- `compatible_with_baseline_output_expectations`
