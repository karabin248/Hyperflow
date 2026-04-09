# Hyperflow Agent Runtime — Priority Tasks

## Current verified state
- baseline remains canonical
- canonical entrypoints do not import `hyperflow.agent_runtime`
- agent-runtime extension layer exists separately under `hyperflow/agent_runtime/`
- a minimal real runtime exists with roles, delegation, coordination, option generation, reporting handoff, fragment-shaped handoff objects, explicit worker time/failure contracts, explicit worker retry-policy descriptors, agent-only delegation-policy profiles, reversible multi-stage workflow presets, explicit promotion gates, baseline-output compatibility summaries, workflow-budget review summaries, and repeated-run stress summaries
- regression tests cover core agent-runtime behavior, worker failure/time budgets, retry behavior, fragment handoff, workflow-to-fragment compatibility review, framework-attached profile trace summaries, promotion-gate review status, compact worker-attempt rollups, workflow-budget evidence export, and repeated-run coordination/observer stress windows

## Next 5 priority tasks
1. **Add richer workflow retry-evidence coverage for terminal failure windows.**
   - classification: Baseline-safe extension candidate
2. **Add review-layer summaries for workflow budget-ceiling hits vs unused budget windows.**
   - classification: Baseline-safe extension candidate
3. **Add export-level counts for bounded vs unbounded workflow windows across wider review slices.**
   - classification: Baseline-safe extension candidate
4. **Add compact gate-level summaries for repeated-run failure windows beyond the latest comparison.**
   - classification: Baseline-safe extension candidate
5. **Add explicit framework-level trace summary coverage for failed attached agent nodes.**
   - classification: Baseline-safe extension candidate

## Best first execution task
Add richer workflow retry-evidence coverage for terminal failure windows so operator review can distinguish visible retry recovery from terminal retry exhaustion without changing baseline execution authority.
