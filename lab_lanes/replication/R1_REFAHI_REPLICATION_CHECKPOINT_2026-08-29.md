# LAB LANE R1 — Independent Refahi FM1 replication checkpoint

Date: 2026-08-29
Status: independent audit; no push/publication/email performed

## Frozen provenance

- Authors' repository: `refahi_diag`
- Authors' commit: `95fde8b3b9a0bd09d556ce765a2235093362306f`
- R1 isolated project base: `b9f21bbd969bf11c9ead40c6dc16669512ad5a84`
- R1 branch/worktree: `lab-r1-refahi-replication` / `dsc-r1-replication`
- R1 audit script: `lab_lanes/replication/r1_refahi_independent_audit.py`
- R1 audit script SHA256: `17aff171a2d0c9055119ca5735ac6bb5a28fedfb042f39043cd4da99fb55c29d`
- Fresh machine-readable output: `lab_lanes/replication/r1_fresh_audit.json`

### Source hashes used

| File | SHA256 |
|---|---|
| `refahi_diag/stateAnalysis/FM1_dtissue.tis` | `3e5bd64f3829f5ca2500eb3c11686eb10acf7157ae23e01e85685bdc233e749d` |
| `refahi_diag/data/geneExpression/t_96h.txt` | `8919a5097e819dcabb1ee84f3c1ac757d8373c9416b27a1b189046f0ad60cbd0` |
| `refahi_diag/data/geneExpression/t_120h.txt` | `f64e5c516c0b170c257287bcf5dc5b8b89b97e1cce49d65cd321837424588216` |
| `refahi_diag/common/common/L1L2_cells_ids.py` | `a1687a402692ad124f3a087617cf7d72b182e40a515a0868b585ecde5472b7e1` |
| `analysis/refahi_state_completion_replication.py` | `03f0dd0dcfabcd69587663ca97ce00d8c14d04e7433ef7218f85c09b83e7bb80` |
| `analysis/refahi_pc_completion_audit.py` | `b365e8cad55924883d7a8c3a1b27097c82cb9ef64cbc6035c415c6deb5b2c07d` |

## Historical 0.27 -> 0.64 molecular-gain claim

### Provenance finding

Repository-history search (`git log -S 0.64`, `git grep` at the initial public commit) finds the exact legacy numbers first as prose in commit `fb496cd`:

- trajectory/geometry R2 about `0.272`;
- + one unsupervised molecular PC R2 about `0.643`;
- + all 25 molecular variables about `0.633`;
- older molecular history about `+0.0095 R2`.

That commit contains only documentation (`CITATION.cff`, `CLAIMS_AND_EVIDENCE.md`, `PREPRINT.md`, `README.md`, `REPRODUCIBILITY.md`, `ROADMAP.md`) and no executable analysis artifact or frozen cohort/split/target definition capable of regenerating those four values. Later executable Refahi analyses were added in later commits and use explicitly different interfaces.

### Direct-source reconstruction result

The nearest traceable late-L1 direct-source setup is `96 -> 120 -> 132 h`, 256 eligible L1 cells, 86 independent 96h ancestor groups, 25 current atlas channels, future target `log(total 132h descendant volume / 120h cell volume)`, and grouped 5-fold CV.

Fresh fixed-partition results (PCA fit on training folds only):

| Decoder | geometry + PC1 R2 | geometry + all25 R2 |
|---|---:|---:|
| Ridge(alpha=10) | 0.4515 | 0.5991 |
| ExtraTrees | 0.6406 | 0.6304 |
| HistGradientBoosting | 0.6672 | 0.6597 |

These demonstrate that a value near 0.64 is reproducible for flexible nonlinear decoders on the late-L1 current-state task, but **the paired 0.272 baseline is not reproduced under the same traceable cohort/target/features/splits**. Ridge also does not support one-PC sufficiency.

**Frozen disposition:** the exact historical `0.272 -> 0.643` pair is **NOT REPRODUCED / provenance-incomplete**, not rescued by choosing a nearby modern analysis. It must not be cited as an independently replicated number.

## Late-L1 screening-off audit

Exact cohort: `96 -> 120 -> 132 h`, L1 only, `n=256`, `86` history-ancestor groups, no duplicate current cells.

Leakage checks:

- grouping variable is the 96h ancestor cell ID;
- maximum train/test ancestor-group overlap across every fresh grouped fold: **0**;
- maximum number of 120h descendants belonging to one ancestor group: 7, therefore ordinary row-wise CV would leak lineage families and is not acceptable;
- PC1 in the R1 fixed-split reconstruction is fit inside each training fold only.

Fresh repeated shuffled ancestor-group partitions:

| Cohort / decoder | partitions | mean delta R2 history | median | split q2.5-q97.5 | positive fraction | > +0.05 fraction |
|---|---:|---:|---:|---:|---:|---:|
| middle L1 Ridge | 8 | +0.1117 | +0.1201 | [-0.0391, +0.2213] | 0.875 | 0.750 |
| late L1 Ridge | 8 | -0.0179 | **-0.0154** | [-0.0381, -0.0034] | 0.000 | **0.000** |
| middle L1 ExtraTrees | 2 | +0.0052 | +0.0052 | [-0.0120, +0.0224] | 0.500 | 0.000 |
| late L1 ExtraTrees | 2 | +0.0091 | +0.0091 | [+0.0004, +0.0179] | 0.500 | **0.000** |
| middle L1 HistGB | 2 | -0.0522 | -0.0522 | [-0.0637, -0.0408] | 0.000 | 0.000 |
| late L1 HistGB | 2 | -0.0126 | -0.0126 | [-0.0209, -0.0043] | 0.000 | **0.000** |

These fresh runs agree with the larger committed stability audit in `STAGE_DEPENDENCE_CHECKPOINT_FM1_2026-08-29.md`: middle-L1 history value is split- and decoder-sensitive, whereas late L1 is much more stably near zero/non-positive and did not show a material >+0.05 gain in the prior 200-Ridge/15-ExtraTrees stability analyses.

## Calibration

Fresh calibration preserved the real late-L1 feature matrix and ancestor grouping, generated a known-complete target from current state only, and a known-incomplete target by adding a residualized history direction of 0.30 target-SD. With 20 fresh Monte-Carlo realizations (small independent smoke calibration):

- known-complete mean delta R2: `-0.0109`;
- known-complete 95th percentile: `-0.0038`;
- known-incomplete mean delta R2: `+0.0525`;
- power against the fresh null threshold: `1.00`.

Because 20 realizations are deliberately small, they are not used for precise power claims. The established project calibration with hundreds of simulations remains the appropriate quantitative reference. R1 uses this fresh run only to verify directionality: the statistic can distinguish a deliberately incomplete state at moderate effect size while the biological late-L1 history gain remains near zero.

## Discrepancy diagnosis

1. **Legacy provenance gap:** the original 0.272/0.643/0.633/+0.0095 numbers were documented before executable analysis artifacts were committed. Exact cohort, target, split seed, estimator and trajectory feature stack are not recoverable from that original commit.
2. **Observation-interface drift:** later analyses use either current 120h geometry only, a richer 96h->120h trajectory stack, or explicit L1 restrictions. These interfaces materially change baseline R2.
3. **Estimator dependence:** in late L1, PC1 approximately matches all 25 channels for flexible nonlinear decoders, but not Ridge. Therefore “one molecular dimension” is decoder-specific and cannot be used to reverse-engineer the old claim.
4. **Split dependence in small middle-L1 cohort:** only 30 ancestor groups exist; single GroupKFold assignments can move Ridge history gain dramatically. Repeated grouped partitions are mandatory.
5. **Atlas measurement caveat:** the 25 channels are integrated binary atlas annotations, not simultaneous longitudinal molecular assays in the same living cells. Screening-off is predictive with respect to this released representation, not proof of biological Markov closure.

## Strongest surviving claim

> In the predefined late-L1 FM1 cohort (96h history -> 120h current state -> 132h growth), current geometry plus the released 25-channel atlas state predicts future lineage growth strongly, and adding the released 96h ancestor state provides no material incremental predictive gain across lineage-grouped repeated splits and multiple tested decoder families. This is a finite-sample, task- and representation-specific predictive screening-off result, not proof of exact conditional independence or an intrinsic biological Markov state.

## Rejected / frozen claims

- **REJECTED:** “The exact historical 0.272 -> 0.643 molecular-gain result has been independently reproduced.” No executable provenance supports that exact pair.
- **REJECTED:** “One molecular PC is generally sufficient.” It is sufficient for tested nonlinear decoders on late L1, but not Ridge; the finite atlas has only a small number of distinct binary states.
- **REJECTED:** “Early flower development is non-Markovian and late development becomes Markovian.” Middle-L1 history gain is decoder/split dependent; late-L1 power cannot exclude subtle residual dependence.
- **REJECTED:** “Late L1 proves Y independent of H given S.” Near-zero held-out gain is evidence against moderate residual predictive value under tested decoders, not a proof of conditional independence.

## Exact executable paths checked

- `analysis/refahi_state_completion_replication.py`
- `analysis/refahi_fm1_state_completion.py`
- `analysis/refahi_fm1_l1_test.py`
- `analysis/refahi_fm1_stage_sweep.py`
- `analysis/fm1_split_stability.py`
- `analysis/refahi_fm1_calibration.py`
- `analysis/refahi_pc_completion_audit.py`
- `analysis/refahi_pc_split_stability.py`
- `analysis/validate_refahi_checkpoint.py`
- `reproduction/reproduce_fm1_grouped.py`
- R1: `lab_lanes/replication/r1_refahi_independent_audit.py`

`analysis/validate_refahi_checkpoint.py` was rerun successfully and returned `REFAHI_CHECKPOINT_VALIDATED` for the committed numerical checkpoint values.

## R1 disposition

**PASS, NARROWED:** late-L1 predictive screening-off survives independent leakage-safe replication at the level of “no material incremental history gain under tested decoders.”

**FAIL / FREEZE:** exact legacy 0.272 -> 0.643 pair is not independently reproducible from recoverable executable provenance.
