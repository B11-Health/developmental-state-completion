# Prospective Validation Roadmap

## Objective

Move from retrospective and synthetic evidence to a prospective, blinded biological test of developmental state completion.

## Phase 1 — computational closure

1. Migrate and hash all frozen checkpoints.
2. Re-run every headline number in a fresh environment.
3. Publish negative results and calibration failures alongside positive results.
4. Freeze the candidate state-completion metric and intervention-selection rule before touching new biological outcomes.

## Phase 2 — living proof-of-principle

Select two or more plant backgrounds that are deliberately matched for baseline morphology but differ in a known or suspected developmental mechanism.

### Blinded protocol

1. Photograph and quantify baseline morphology.
2. Freeze the baseline classifier and expected chance-level discrimination.
3. Allow the algorithm to select a small perturbation panel from a preregistered safe set.
4. Apply perturbations under randomization and blinding.
5. Predict hidden background from the response trajectory.
6. Compare against random and equal-cost perturbation panels.
7. Unblind only after predictions and analysis code are frozen.

### Primary endpoint

Designed perturbations identify hidden biological background substantially better than baseline morphology alone and better than random/equal-cost perturbation selection.

### Secondary endpoint

A compact present-state representation makes older measured history add little out-of-sample predictive value across multiple future challenges, after calibration against finite-estimator bias.

## Phase 3 — recursive state completion

Introduce a new perturbation not used in fitting. If old history becomes predictive again, treat that as evidence that the current state representation is incomplete. Use the resulting residual to choose the next measurement or perturbation.

## Phase 4 — cross-system generalization

Test whether the same experimental logic transfers to systems where perturbations and lineage tracking are mature, for example Arabidopsis developmental transitions, organoids, or well-characterized cell-state differentiation systems.

## Success criteria

A strong result is not “the theory was right.” A strong result is a preregistered experiment in which:

- baseline appearance leaves a meaningful hidden-mechanism ambiguity;
- a designed perturbation collapses that ambiguity;
- the chosen current state predicts future response;
- old measured history becomes approximately redundant after conditioning on that state;
- the result replicates in an independent cohort or lab.

## Collaboration request

We are looking for collaborators with one or more of:

- longitudinal plant imaging;
- Arabidopsis/Cardamine developmental genetics;
- inducible perturbation systems;
- lineage-resolved molecular measurements;
- active experimental design;
- causal inference for dynamical systems;
- topological data analysis / Reeb-space methods.


## Current prospective protocol

The audited living-system design is maintained in [`LIVING_VALIDATION_PREREGISTRATION_DRAFT_2026-08-29.md`](LIVING_VALIDATION_PREREGISTRATION_DRAFT_2026-08-29.md). It supersedes informal sample-size, reagent, and threshold suggestions that were not source-verified.
