# R2 cross-system state-sufficiency replication

This lane analyzes one additional public longitudinal developmental dataset distinct from the Refahi FM1 and Weinreb/Klein controls: Cell Tracking Challenge `Fluo-N3DH-CE` (*C. elegans* embryonic development).

## Reproduce
1. `python fetch_ctc_lineage_metadata.py`
2. Read `PREREGISTRATION.md`.
3. Run the deterministic batches with `run_batched.py` for `observed`, `strict`, `noemb`, `cal`, and `perm` as recorded in the checkpoint.
4. `python aggregate_results.py`

The original one-shot `analyze_ctc_ce_lineage.py` contains the complete analysis definitions; batching exists only to stay within shell execution windows. No external publication or push is performed by this lane.
