# LAB LANE P1 - Provenance & Artifact Recovery

Generated: 2026-08-29T17:46:12.800285

## Bottom line

- The historical 224-world simulator/source/output bundle was **not recovered** from the authenticated Windows workspace.
- The two named historical frozen checkpoints were **not recovered as files**.
- `/root/plant_m2_deep/` was reported by the earliest public reproducibility manifest, but is not present in the visible Windows workspace or tested WSL paths.
- The later `source_validation/two_context_2026-08-26` bundle **is present** and was copied byte-for-byte into `staged_verified/`; it must not be mislabeled as the missing 224-world simulator.

## Missing historical artifacts / best provenance pointers

### INNOVATION_CLOSURE_STATE_COMPLETION_CHECKPOINT_2026-08-28.md
- Status: NOT PRESENT / NOT RECOVERED
- Supports: historical state-completion / 224-world reporting
- Best provenance pointer: REPRODUCIBILITY.md lines 7-14; historical ChatGPT research threads in browser history
- Historically reported SHA-256: `be709de7b39f2c6a4470ed7409e8ba7ef50c39cea075f5674f33b774f5cd72e8` (not revalidated because file is absent)

### STRATIFIED_CAUSAL_FIBER_AND_MECHANISM_PERSISTENCE_CHECKPOINT_2026-08-26.md
- Status: NOT PRESENT / NOT RECOVERED
- Supports: connected causal fibers, mechanism persistence, thresholds/perturbation ranking
- Best provenance pointer: REPRODUCIBILITY.md lines 11-14; reported original location /root/plant_m2_deep/

### /root/plant_m2_deep/
- Status: NOT PRESENT / NOT RECOVERED
- Supports: reported original workspace for historical simulator/checkpoint
- Best provenance pointer: REPRODUCIBILITY.md line 12; WSL probes //wsl$/Ubuntu/root/plant_m2_deep and //wsl.localhost/Ubuntu/root/plant_m2_deep were absent

### historical 224-world simulator/generator/output set
- Status: NOT PRESENT / NOT RECOVERED
- Supports: 14 architecture x 16 hidden-state grid, baseline/intervention outputs
- Best provenance pointer: REPRODUCIBILITY.md Test E lines 54-56; browser history: Reconstructing causal worlds, Verify checkpoint code, Develops experiment framework, Report experimental validation, Flower Research Checkpoint

### historical connected-causal-fiber threshold sweep outputs
- Status: NOT PRESENT / NOT RECOVERED
- Supports: connected components, accommodation and merge/access thresholds
- Best provenance pointer: REPRODUCIBILITY.md Test F lines 58-67; STRATIFIED checkpoint pointer

### historical perturbation-ranking outputs
- Status: NOT PRESENT / NOT RECOVERED
- Supports: connected-fiber contraction / topology-aware perturbation ranking
- Best provenance pointer: REPRODUCIBILITY.md Test G lines 69-71; STRATIFIED checkpoint pointer

## Verified staged artifacts

- Count: 149
- Full per-file original path, size, SHA-256, timestamps, type, and staged path: `chain_of_custody.json`.
- Staging is non-destructive; originals were not overwritten.

## Git chain of custody

- Earliest public checkpoint commit: `fb496cdf76153895c1443521f1d69aad528ce507` (already references missing historical artifacts in `REPRODUCIBILITY.md`).
- Later source-validation import commit: `34de67a9a7ed90854f85b7b5d2c6691084704e84` (adds the Aug-26 two-context bundle).

## Browser-accessible provenance pointers

- Reconstructing causal worlds: https://chatgpt.com/c/6a8f3fca-83ac-83ea-8184-3a6bbc250031
- Verify checkpoint code: https://chatgpt.com/c/6a8f408c-5be4-83e9-a5fa-80735286a12b
- Develops experiment framework: https://chatgpt.com/c/6a8db025-70bc-83ea-94ec-53c430082588
- Report experimental validation: https://chatgpt.com/c/6a8f9a87-87c4-83ea-a96d-5e78b2602a67
- Flower Research Checkpoint: https://chatgpt.com/c/6a909499-a598-83e9-b89e-80cf1009459b

## Custody rule

No artifact was recreated from prose. Missing items remain missing. Later validation artifacts are listed separately and are not used as substitutes for historical originals.
