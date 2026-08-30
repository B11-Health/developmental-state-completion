# R5 — Drosophila Cross-Sequence Future-Trajectory Stress Test

Date: 2026-08-30
Status: **COMPLETE NEGATIVE / ADEQUACY-LIMITED RESULT**

## Question
Can an older kinematic segment `H` improve prediction of a later 3D developmental cell trajectory after a declared present representation `S`, and does that increment disappear as `S` is enriched?

## Public source
Cell Tracking Challenge `Fluo-N3DL-DRO`: developing *Drosophila melanogaster* embryo, SIMView light-sheet microscopy, 0.406 x 0.406 x 2.03 um voxels, 30-second time step. The challenge states that the gold tracking annotations used for evaluation correspond to cells forming the developing nervous system.

The training ZIP is about 6.22 GB. R5 did **not** download the raw movie. A ZIP64 HTTP range reader recovered only selected public gold `TRA` label volumes and `man_track.txt` metadata, validated entry size and CRC, and derived 3D centroids. This yielded 189 cells in sequence 01 and 203 in sequence 02 at all six frozen frames, 392 cells total.

## Frozen primary task
Frames: 15, 20, 23, 24, 25, 40.

- `H`: older motion from frames 15->20, older speed, and older volume change.
- `S0`: current frame-25 normalized position + volume.
- `S1`: S0 + recent frame-24->25 velocity + recent volume change.
- `S2`: S1 + recent acceleration from frames 23/24/25.
- `Y`: average future 3D velocity from frame 25->40.
- split: leave one complete CTC acquisition sequence out. No cell from the held-out acquisition is used for model fitting.
- estimators: Ridge, Random Forest, Extra Trees.

At a 30-second frame interval, H spans an older 2.5-minute motion segment, the recent velocity spans 30 seconds, and Y spans the next 7.5 minutes.

## Result
The raw-vector task failed absolute cross-sequence predictive adequacy. Mean held-out R2 was negative for every estimator and every S level. The richest S2 history increments were mixed:

- Extra Trees: Delta R2 = -0.079
- Random Forest: Delta R2 = +0.211
- Ridge: Delta R2 = -0.054

A secondary translation/rotation-invariant sensitivity for future radial velocity produced positive H increments at S2 across all three estimators (+0.0735, +0.0810, +0.0657), but the absolute models still had negative held-out R2 and were worse than the train-sequence-mean dummy predictor. Therefore those positive increments are **not promoted** as evidence that history is future-predictive.

## New methodological finding
R5 exposes a failure mode that should become a program-wide promotion rule: **an incremental history gain is not scientifically interpretable if the augmented predictor itself lacks out-of-group predictive adequacy.** A delta can become positive inside a model that is still worse than a naive cross-group baseline.

See `ADEQUACY_GATE.md` and the checkpoint for the proposed hard gate.

## Reproduce
- `fetch_dro_centroids_part.py` selectively derives public gold-mask centroids through HTTP byte ranges.
- `r5_primary.py` runs the frozen vector task.
- `r5_invariant.py` runs the explicitly secondary invariant sensitivity.
- `r5_dummy_baseline.py` evaluates train-only naive baselines.

No biological-memory, universal-state, or organism-level Markov claim is supported by R5.
