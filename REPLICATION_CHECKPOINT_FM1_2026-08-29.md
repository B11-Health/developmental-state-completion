# Independent FM1 replication checkpoint — 2026-08-29

## Status

**Observed-data reanalysis from the original authors' public repository.** This checkpoint independently reconstructs a narrower version of the developmental-state question from the released FM1 Arabidopsis flower atlas. It does not prove Markovianity and it is not a prospective biological validation.

## Upstream provenance

Primary paper: Refahi et al., *A multiscale analysis of early flower development in Arabidopsis provides an integrated view of molecular regulation and growth control* (Developmental Cell; PMCID PMC8519405).

Public data DOI: `10.17863/CAM.61991`

Authors' code: `https://gitlab.com/slcu/teamHJ/publications/refahi_etal_2020`

Frozen upstream commit used here: `95fde8b`

The released repository contains FM1 lineage/volume geometry, 25 binary regulatory-gene patterns at 96h, 120h and 132h, and the authors' lineage object.

### Windows reproducibility warning

`stateAnalysis/FM1_dtissue.tis` is an old text-protocol Python pickle. A normal Windows checkout can convert its LF newlines to CRLF and make it unreadable by Python 3. The replication script therefore loads the exact blob bytes with:

`git show HEAD:stateAnalysis/FM1_dtissue.tis`

rather than unpickling the working-tree copy.

## Question

For cells measured at 120h, how much does the present molecular state improve held-out prediction of subsequent lineage growth to 132h, and how much additional predictive information is supplied by the corresponding 96h ancestor state?

## Cohort construction

A 120h cell is included only when:

1. it has a released 25-gene binary state at 120h;
2. its 96h ancestor can be traced through the released lineage object and has a released 25-gene state;
3. released geometry exists at both 96h and 120h;
4. descendants can be traced to 132h with positive total volume.

Final cohort: **760 120h cells belonging to 233 distinct 96h ancestor groups.**

The future target is lineage log-volume expansion:

`Y = log(total descendant volume at 132h / cell volume at 120h)`.

## Leakage control

All descendants sharing a 96h ancestor are assigned to the same outer fold. Five-fold `GroupKFold` therefore prevents sibling/lineage leakage across training and test sets.

## Feature stacks

- **Current geometry:** log volume + 3D cell center at 120h.
- **Current state:** current geometry + 25 released binary regulatory-gene measurements at 120h.
- **Current + history:** current state + 96h ancestor log volume + 3D center + 25-gene state.

## Main held-out results

### Nested Ridge

Inner grouped model selection chooses ridge regularization only inside the training fold.

| Feature stack | Out-of-fold R2 | MAE |
|---|---:|---:|
| Current geometry | 0.0333 | 0.3410 |
| Current geometry + current 25-gene state | **0.2846** | 0.2673 |
| Current state + 96h history | **0.2928** | 0.2641 |

Increment from current molecular state over geometry: **+0.2513 R2**.

Increment from old history after current state: **+0.0082 R2**.

### Random-forest sensitivity analysis

| Feature stack | Out-of-fold R2 | MAE |
|---|---:|---:|
| Current geometry | 0.3002 | 0.2562 |
| Current geometry + current 25-gene state | **0.3524** | 0.2385 |
| Current state + 96h history | 0.3304 | 0.2425 |

The nonlinear sensitivity analysis agrees that the current molecular state adds predictive information, but old history does not provide a stable additional gain.

## Finite-sample calibration

Because adding 29 history variables can itself alter finite-sample generalization, the history-gain statistic was calibrated with a fixed-Ridge pipeline on synthetic controls preserving the real feature matrices and group structure.

Observed fixed-Ridge values:

- current-state R2: **0.2874**
- current + history R2: **0.2930**
- `Delta R2_history|current`: **+0.0056**

Known-Markov synthetic control (250 realizations):

- mean history gain: **-0.0125**
- 5th / median / 95th percentiles: **-0.0253 / -0.0132 / +0.0008**

Known-non-Markov control with a deliberately injected residual history term (250 realizations):

- mean history gain: **+0.0280**
- 5th / median / 95th percentiles: **+0.0059 / +0.0276 / +0.0531**
- power above the known-Markov 95th percentile: **0.976**

Group bootstrap of the biological history gain (5,000 resamples of 96h ancestor groups):

- median: **+0.0041**
- 95% interval: **[-0.0392, +0.0545]**

## Interpretation that survives

The released FM1 data independently support the narrower claim that **a current molecular measurement contains substantial future-growth information beyond current geometry**.

The old 96h state adds, at most, a small and model-sensitive amount of predictive information after the 120h state in this task. The confidence interval is too wide to claim exact screening-off or biological Markov closure.

A defensible statement is:

> In this FM1 task, much of the predictive information available from the measured lineage appears concentrated in the 120h molecular state; residual predictive value from the measured 96h ancestor state is small relative to the current-state gain and is not robustly resolved at this sample size.

## What this does not establish

- It does not prove `Y independent of H given S`.
- It does not establish a universal developmental state.
- It does not reproduce the earlier 24-window FM2–FM6 screening statistic because the public repository does not expose the same molecular measurements across those flowers.
- It does not show causality; this is observational lineage prediction.
- It does not replace the prospective perturbation experiment.

## Reproduction

Scripts:

- `analysis/refahi_fm1_state_completion.py`
- `analysis/refahi_fm1_calibration.py`

Clone the upstream repository and run from the repository workspace:

```bash
git clone https://gitlab.com/slcu/teamHJ/publications/refahi_etal_2020 refahi_diag
python developmental-state-completion/analysis/refahi_fm1_state_completion.py --upstream refahi_diag
python developmental-state-completion/analysis/refahi_fm1_calibration.py --upstream refahi_diag --reps 250 --bootstrap 5000
```

This checkpoint should be treated as **reproduced observational evidence**, not prospective biological validation.
