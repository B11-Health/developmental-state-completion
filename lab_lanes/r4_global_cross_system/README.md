# R4 Global Cross-System Developmental-State Expansion

This lane expands the developmental-state-completion program across genuinely public plant and animal datasets while preserving the project's existing claim boundaries.

## Deliverables

- `DATASET_REGISTRY.md` — 21-unique-dataset ranked public registry with accessions, system/institution geography, modality/time/intervention structure, candidate H/S/Y constructions, and leakage risks.
- `ANALYSIS_PLAN.md` — five fully specified first-wave plans and common promotion rules.
- `r4_stomatal_proxy.py` — independent executable analysis of public Arabidopsis GSE167135 Smart-seq2/FACS data.
- `results/` — held-out predictions, fold metrics, multi-estimator summaries, incremental gains, permutation null, sensitivity calibration, and machine-readable result metadata.
- `CLAIM_BOUNDARIES.md` — explicit separation of predictive screening-off from mechanism and of cross-sectional trajectory proxies from literal future prediction.
- `NEXT_WAVE_QUEUE.md` — ranked follow-up queue with hard stop/downgrade rules.
- `SOURCE_PROVENANCE.md` — source URLs, downloaded file hashes, and access notes.

## Executed analysis status

The GSE167135 run is intentionally a **same-time measurement-sufficiency proxy**, not a developmental future test: H is seven FACS measurements, S is train-only transcriptomic PCs, and Y is TMMp-vs-ATML1p reporter enrichment. Adding H improves held-out performance across logistic, random-forest, and histogram-gradient-boosting models. That result argues against treating the selected transcriptomic representation as sufficient for this proxy target; it does not establish biological memory, mechanism, or global transcriptome insufficiency.

The initial tempting four-label leave-one-pool-out split was rejected before accepting results because each literal pool label is reporter-class-specific and therefore yields a single-class test fold. The frozen split holds out matched pool index (`pool_1` versus `pool_2`), with both reporter classes represented in each fold.

## Reproduce

From the repository root:

```text
python lab_lanes/r4_global_cross_system/r4_stomatal_proxy.py
```

The script uses fixed seed `20260830`; input SHA-256 hashes are frozen in `results/results.json`.
