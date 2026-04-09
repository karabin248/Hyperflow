# Archive Policy

## Archive now

Move inactive or generated debris out of active paths when it is not import/runtime truth.

Examples for PR-01:

- generated package metadata (`hyperflow.egg-info`)
- stale workflow fragments after replacement
- seed-generated storage payload files already present in the archive copy
- caches such as `.pytest_cache`

## Keep active

Do not archive:

- runtime code
- active configs
- useful tests
- contracts still used by runtime or packaging
- anything referenced by imports or entrypoints

## Purpose

The archive is for retention, not active execution.
The live repo surface should reflect what the MVP actually runs.


## Applied cleanup
Legacy root docs and the previous `docs/master_hyperflow/` bundle were moved into `archive/docs/` to keep one active documentation path.
