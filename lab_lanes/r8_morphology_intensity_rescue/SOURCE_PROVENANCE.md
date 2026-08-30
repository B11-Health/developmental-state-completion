# R8 Source Provenance

Date: 2026-08-30

## Public sources
- Cell Tracking Challenge `Fluo-N3DL-DRO` training archive: public Drosophila developmental tracking data already used in R5/R7.
- Cell Tracking Challenge `Fluo-N3DL-TRIC` training archive: public Tribolium developmental tracking data already used in R6/R7.

## Selective retrieval
R8 did not download either full multi-GB archive. The existing remote ZIP central-directory/range method identified individual `t023.tif`, `t024.tif`, `t025.tif` raw entries and matching `GT/TRA/man_trackNNN.tif` label entries. Large raw entries were fetched as bounded compressed chunks into `raw_cache/`, reconstructed locally, and validated against ZIP metadata before use. Per-frame manifests record ZIP entry names, compressed/uncompressed sizes, CRC values, and SHA-256 of reconstructed uncompressed content.

## Annotation boundary
The dense `GT/TRA` volumes are tracking labels used as geometry proxies. They are **not claimed to be dense segmentation ground truth**. Drosophila `GT/SEG` contains only sparse single-object exemplars in the relevant neighborhood; Tribolium has no GT/SEG entries at frames 23-25.

## Analysis lineage
- Cohorts, frame25 anchor, frame40 outcomes, reciprocal sequence holdout, and R7 relational present features come from committed R7 artifacts.
- R8 adds only <=25 morphology/intensity features declared in `PREREGISTRATION.md`.
- `r8_analyze.py` was run once after all twelve frame-feature tables existed.
- Gate-1 outputs are in `results/gate1_fold_metrics.csv`, `results/adequacy_decisions.json`, and `results/results.json`.
- Because Gate 1 failed, no older-history fit or calibration/permutation output should exist as a promoted R8 result.
