# Stage-dependence checkpoint — FM1 Arabidopsis atlas

Date: 2026-08-29

## Purpose

Test whether the incremental predictive value of older lineage history changes across developmental windows when the same analysis logic is applied to the original Refahi et al. FM1 public release.

This checkpoint is observational and uses an integrated/template gene-expression atlas. It does **not** prove biological memory, Markov closure, or causal state completion.

## Data provenance

Upstream repository: `https://gitlab.com/slcu/teamHJ/publications/refahi_etal_2020`  
Frozen upstream commit: `95fde8b`  
Primary paper: Refahi et al., Developmental Cell (2021), PMCID `PMC8519405`.

The paper states that gene-expression patterns were integrated into the FM1 4-D template by manually annotating individual cells from published information plus new RNA in-situ/live-imaging data. The 25 channels used here are therefore **atlas annotations**, not simultaneous molecular assays in every exact live cell.

## Common analysis

For each window `history -> current -> future`:

- target: log descendant-volume expansion from current to future;
- current state: current log volume + 3-D center + current 25-gene atlas annotation;
- history: ancestor log volume + 3-D center + older 25-gene atlas annotation;
- five-fold outer GroupKFold, grouping all descendants of the same history-time ancestor together;
- nested grouped Ridge is the linear decoder;
- random forest is the nonlinear sensitivity decoder.

## All eligible cells

| Window | N / history groups | Ridge current | Ridge + history | Delta | RF current | RF + history | Delta |
|---|---:|---:|---:|---:|---:|---:|---:|
| 10 -> 40 -> 96h | 129 / 96 | 0.3654 | 0.3923 | +0.0269 | 0.3315 | 0.3497 | +0.0182 |
| 40 -> 96 -> 120h | 262 / 84 | 0.1218 | 0.1425 | +0.0207 | 0.1431 | 0.1038 | -0.0393 |
| 96 -> 120 -> 132h | 760 / 233 | 0.2846 | 0.2928 | +0.0082 | 0.3478 | 0.3249 | -0.0229 |

There is no estimator-robust large history effect across the pooled-cell windows. Ridge shows modest positive history gains that diminish in the latest window; the nonlinear decoder does not reproduce those gains after the first window.

## Predefined L1 epidermal cells

L1 membership comes directly from the authors' `common/common/L1L2_cells_ids.py`, independent of our outcome target.

| Window | N / history groups | Ridge current | Ridge + history | Delta | RF current | RF + history | Delta |
|---|---:|---:|---:|---:|---:|---:|---:|
| 10 -> 40 -> 96h | 50 / 40 | 0.4670 | 0.4730 | +0.0061 | 0.3920 | 0.4131 | +0.0211 |
| 40 -> 96 -> 120h | 100 / 30 | 0.1449 | 0.3642 | **+0.2193** | 0.2182 | 0.2356 | +0.0174 |
| 96 -> 120 -> 132h | 256 / 86 | **0.5947** | **0.5956** | **+0.0008** | **0.6695** | **0.6674** | **-0.0021** |

## Why the middle L1 window matters

The 40 -> 96 -> 120h L1 interval contains a large linear-decoder history gain but only a small nonlinear-decoder gain. Decomposing history shows:

| Feature stack | Nested Ridge R2 | RF R2 | ExtraTrees R2 |
|---|---:|---:|---:|
| Current state | 0.1449 | 0.2182 | 0.2365 |
| + old geometry only | 0.0833 | 0.2361 | 0.2579 |
| + old atlas only | **0.3386** | 0.2229 | 0.2309 |
| + full history | **0.3642** | 0.2356 | 0.2570 |

Thus the large Ridge gain comes primarily from the old 40h atlas annotation, not old geometry. Nonlinear tree estimators extract little or no comparable gain from that old atlas block.

A fixed-Ridge group-preserving permutation test of the old atlas block gave:

- observed Delta R2: **+0.1522**;
- permutation null 95th percentile: about **+0.024**;
- empirical `p` about **0.005** with 200 permutations in the reproducibility harness (a 1,000-permutation direct run gave approximately `p=0.002`).

This establishes that the old atlas annotation contains real incremental linear predictive structure. It does **not** establish physical memory, because nonlinear current-state models largely absorb the same predictive structure without the old atlas.

## Late L1 screening-off result

In the 96 -> 120 -> 132h L1 window, both the linear and nonlinear decoders agree that adding 96h history changes held-out performance by approximately zero. This is the strongest reproduced screening-off pattern in the released atlas.

However, finite-sample calibration shows limited sensitivity to subtle effects. Under the fixed-Ridge synthetic calibration, approximate power to detect residualized history effects of 0.10, 0.15, 0.20, 0.25, 0.30, 0.35 and 0.40 target-SD was about 0.16, 0.37, 0.73, 0.88, 0.98, 1.00 and 1.00, respectively.

Therefore the data can argue against **moderate-to-large** residual history effects under this calibration, but cannot rule out small ones.

## Frozen rejection

> “Early flower development is structurally non-Markovian, while late flower development becomes Markovian.”

**Rejected.** The public FM1 atlas does not justify this statement. History gain is decoder-dependent in the middle window, the molecular channels are integrated atlas annotations, and the late cohort lacks power to exclude subtle residual effects.

## Surviving interpretation

The strongest defensible statement is:

> Predictive sufficiency is developmental-stage-, observation-, task-, and decoder-dependent at finite sample size. In the predefined late-L1 FM1 cohort, the released current geometry + atlas state predicts subsequent lineage growth well and older released history adds essentially no incremental predictive value across both linear and nonlinear decoders; in a middle L1 window, older atlas state adds substantial signal to a linear decoder but little to nonlinear tree decoders.

This makes **state-completion testing an estimator-calibrated empirical procedure**, not a declaration of an intrinsic Markov state.

## Consequences for prospective biology

A living-system validation should pre-register:

1. a sharply stage/layer-matched cohort;
2. directly measured current reporters rather than a manually integrated atlas;
3. at least one linear and one flexible nonlinear decoder;
4. known-complete and known-incomplete simulation calibration at the planned sample size;
5. a smallest residual-history effect the study is powered to exclude;
6. no “state complete” wording unless the conclusion is robust to the pre-specified decoder family and calibration.

## Reproduction

- `analysis/refahi_fm1_state_completion.py`
- `analysis/refahi_fm1_calibration.py`
- `analysis/refahi_fm1_l1_test.py`
- `analysis/refahi_fm1_stage_sweep.py`
