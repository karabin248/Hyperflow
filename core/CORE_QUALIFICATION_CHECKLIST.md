# Core Module Qualification Checklist

Complete this checklist **before** marking a module as `core`.

- [ ] **Explicit input contract**
  - [ ] Defined input format (types, required fields, constraints)
  - [ ] Defined edge cases and input validation
- [ ] **Explicit output contract**
  - [ ] Defined output format (types, field semantics)
  - [ ] Defined compatibility guarantees (for example, versioning)
- [ ] **Operational metrics**
  - [ ] Quality metrics (for example, correctness, completeness)
  - [ ] Performance metrics (for example, latency, throughput)
  - [ ] Reliability metrics (for example, error rate)
- [ ] **Failure modes**
  - [ ] List of expected failure modes
  - [ ] For each failure mode: detection, degradation, error message
- [ ] **Safety thresholds**
  - [ ] Defined safety limits (for example, timeout, max cost, max size)
  - [ ] Defined actions after threshold breaches
- [ ] **Dependencies**
  - [ ] Explicit list of internal and external dependencies
  - [ ] Dependency classification: critical / optional
- [ ] **Rollback criterion**
  - [ ] Measurable rollback trigger
  - [ ] Described rollback procedure and return point

## Classification rule
If any checklist item is missing, the module **does not qualify for `core/`** and must remain in `boost/` or `experimental/`.
