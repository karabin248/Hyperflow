# Android shell

This directory contains the imported Android UI shell from the platform donor.

Current intent:
- preserve the mobile skeleton in the canonical MVP repo
- keep backend ownership under the `hyperflow` Python package
- avoid introducing a second backend runtime or a parallel contract namespace

Current non-goals:
- no live auth wiring
- no worker execution wiring
- no backend scheduler coupling
- no parallel `hyperflow_platform` backend package
- no Android-driven contract fork

Expected next move:
- keep the shell file-complete
- wire it to the canonical `/health`, `/v1/agents`, `/v1/workflows`, `/v1/checkpoints`, and `/v1/logs/recent` surface only after contract review
