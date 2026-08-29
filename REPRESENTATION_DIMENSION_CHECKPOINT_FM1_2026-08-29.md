# Representation-dimension checkpoint — late FM1 L1 atlas state

Date: 2026-08-29

Status: **post-hoc observed-data reanalysis; not prospective; not peer reviewed**

## Question

A legacy exploratory analysis suggested that one unsupervised molecular principal component could recover nearly all of the predictive gain of the released 25-channel FM1 flower atlas state. This checkpoint re-tests that claim directly from the authors' public FM1 release with leakage-safe lineage grouping.

Primary source:

- Refahi et al., *Developmental Cell* (2021), PMCID `PMC8519405`.
- Data DOI: `10.17863/CAM.61991`.
- Authors' GitLab commit used: `95fde8b3b9a0bd09d556ce765a2235093362306f`.

Critical caveat: the 25 channels are **binary atlas annotations integrated onto the FM1 reference**, not simultaneous longitudinal molecular measurements in each exact living cell.

## Cohort and target

Predefined late epidermal cohort from the direct-source replication:

- window: `96 -> 120 -> 132 h`;
- current cells: released L1 epidermal subset at 120 h whose 96 h ancestor is also L1;
- `n = 256` cells in `86` independent 96 h ancestor groups;
- future target: `log(total descendant volume at 132 h / current 120 h cell volume)`;
- geometry baseline: current log-volume and 3-D center;
- cross-validation: five-fold grouped by 96 h ancestor, so sibling descendants never cross train/test folds;
- PCA is fitted **inside each training fold** using the 25 current 120 h atlas channels, then applied to the held-out fold.

## Fixed-partition dimensionality audit

| Decoder | Geometry | + PC1 | + PC2 | + PC4 | + all 25 | Interpretation |
|---|---:|---:|---:|---:|---:|---|
| Ridge | 0.307 | 0.451 | 0.551 | **0.598** | **0.599** | linear decoder needs several PCs; PC1 alone is insufficient |
| ExtraTrees | 0.460 | **0.636** | 0.638 | 0.629 | 0.630 | PC1 alone matches/exceeds the full atlas block |
| HistGradientBoosting | 0.543 | **0.660** | 0.659 | 0.637 | 0.650 | PC1 alone matches/exceeds the full atlas block |

Training-fold PCA variance captured on average:

- PC1: **58.2%**;
- PC1–2: **81.3%**;
- PC1–4: **96.7%**.

For Ridge, the molecular gain above geometry is `0.599 - 0.307 = 0.292 R²`. PC1 recovers about **49.5%** of that gain, PC1–2 about **83.5%**, and PC1–4 about **99.6%**.

For the nonlinear decoders, PC1 alone recovers essentially all of the gain of the 25-channel block.

## Thirty-partition stability audit

To test whether nonlinear PC1 sufficiency is an accident of one ancestor-group split, we repeated five-fold grouped CV over 30 deterministic shuffled lineage partitions.

### ExtraTrees

- geometry mean R²: **0.494**;
- geometry + PC1 mean R²: **0.654**;
- geometry + all 25 mean R²: **0.638**;
- mean `PC1 - all25`: **+0.0156 R²**;
- PC1 >= all25 in **30/30 partitions**;
- median fraction of the full molecular gain recovered by PC1: about **110%**.

### HistGradientBoosting

- geometry mean R²: **0.604**;
- geometry + PC1 mean R²: **0.674**;
- geometry + all 25 mean R²: **0.671**;
- mean `PC1 - all25`: **+0.0034 R²**;
- PC1 >= all25 in **21/30 partitions**;
- median fraction of the full molecular gain recovered by PC1: about **105%**.

These split distributions are sensitivity analyses, not confidence intervals.

## Older history after the current representation

On the fixed grouped split:

- ExtraTrees: PC1 state `0.636`; PC1 + full 96 h history `0.640` (`+0.004 R²`).
- HistGradientBoosting: PC1 state `0.660`; PC1 + history `0.638` (negative gain).
- Ridge: all-25 current state `0.599`; + full history `0.599` (approximately zero).

Combined with the separate late-L1 200-partition history audit, there is no estimator-robust material positive history gain once the richer current state is included.

## Frozen correction

### Rejected wording

> “The developmental molecular state is one-dimensional.”

Rejected. The result depends on decoder class and on the exact task/interface.

### Also rejected

> “One PC is sufficient under any reasonable decoder.”

Rejected. Ridge requires roughly four PCs to recover the full predictive gain.

### Surviving statement

> In the predefined late-L1 FM1 cohort, a single unsupervised current atlas-expression coordinate captures essentially all of the **nonlinear** predictive value of the released 25-channel atlas block for subsequent lineage-volume expansion, while a linear decoder requires several coordinates. Thus the effective predictive representation dimension is decoder- and task-dependent.

This is a statement about an atlas-derived feature representation for one prediction target. It is **not** evidence that the biological organism has one intrinsic molecular state variable.

## Why this matters

The checkpoint separates three notions that had been conflated:

1. **variance dimension** — how many PCs explain the atlas-feature variance;
2. **linear predictive dimension** — how many coordinates a linear decoder needs;
3. **task-specific nonlinear predictive dimension** — how many coordinates a flexible decoder needs for the specified future target.

They are not the same quantity. Any future claim about a “minimal developmental state” must specify the decoder family, task, biological compartment, developmental time, and tolerated error.

## Reproduction files

- `analysis/refahi_pc_completion_audit.py`
- `analysis/refahi_pc_split_stability.py`
- `results/refahi_pc_completion_L1_ridge.json`
- `results/refahi_pc_completion_L1_extra_trees.json`
- `results/refahi_pc_completion_L1_histgb.json`
- `results/refahi_pc_split_stability_extra_trees_30.json`
- `results/refahi_pc_split_stability_histgb_30.json`

## Next falsification

The next decisive test is not another PCA variant. It is to measure a compact reporter/state vector **prospectively in living plants**, freeze the decoder before future outcomes are observed, and test whether the same compact representation remains sufficient under an enlarged intervention family.
