# R12 Preregistration — Domain-Balanced Known-Incomplete Calibration

Date: 2026-08-30
Status: DECLARED FROZEN BEFORE R12 OUTCOME EVALUATION

Post-audit provenance note: R12A verified the committed design/results but found that Git history first adds the preregistration, implementation, results, tests, and checkpoint in the same commit. The session record states the design was written before execution, but repository chronology alone does not independently prove the pre-outcome freeze.

## Motivation
R10B corrected the R10 seed specification and obtained 16/30 joint successes at +0.30 pooled target-SD, below the frozen 24/30 threshold. A post-R10B diagnostic found that the pooled residual-history directions have unequal standard deviations across the two acquisitions. R12 tests whether that calibration geometry itself contributes to adequacy loss. R12 cannot upgrade the biological history conclusion.

## Frozen task
Use exactly the R10/R10B Tribolium future-radial-velocity task, R9 transductive percentile S/H representation, cohorts, reciprocal acquisition holds, Random Forest/Extra Trees models, Gate 2, and documented residual-direction seed family `20260830 + replicate`, for replicates 0..29. Use only +0.30 times the same pooled original target SD.

## Primary calibration geometry: domain-balanced residual
For each documented seed, construct `z=H w` and fit the same pooled outcome-blind `Ridge(alpha=1)` residualizer `S -> z`. Then, instead of globally standardizing the residual, center and scale it separately within each acquisition to mean zero and standard deviation one. Inject `0.30 * pooled_SD(Y) * h_balanced` into Y. This uses S/H and acquisition labels but no Y in the balancing transform; the pooled Y SD is inherited unchanged from R10/R10B.

## Secondary diagnostic: domainwise residualizer
As a secondary planning-only diagnostic, fit `Ridge(alpha=1)` from S to z separately within each acquisition, residualize within acquisition, and center/scale each residual to mean zero/unit SD before the same +0.30 pooled-target-SD injection.

## Outputs
For each geometry report S-only adequacy preservation, Gate-2 detection, joint success, and four-way decomposition. The R10B documented-seed result 16/30 is the fixed reference and is not refit.

## Interpretation rules
- R12 is post-hoc calibration design, not confirmatory biology.
- Even if a geometry reaches 24/30, do not reinterpret the observed near-zero history result as screening-off.
- A higher joint rate would support only that calibration geometry/domain balancing materially affects sensitivity.
- A lower or unchanged rate would argue against variance imbalance being the main bottleneck.
- Do not change scale, seeds, models, gate, folds, or add geometries after seeing results.
