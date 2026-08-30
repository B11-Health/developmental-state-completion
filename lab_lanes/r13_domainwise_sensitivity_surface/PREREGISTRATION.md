# R13 Preregistration — Domainwise Calibration Sensitivity Surface

Date: 2026-08-30
Status: FROZEN AND COMMITTED BEFORE ANY NEW R13 SCALE EVALUATION

## Motivation
R12A independently verified the R12 secondary planning geometry: acquisition-specific Ridge residualization against S, followed by within-acquisition centering/scaling, preserves S-only adequacy in 30/30 documented +0.30-SD calibration directions but detects only 18/30, below the frozen 24/30 criterion. R13 prospectively maps scale sensitivity for this already-audited geometry. It cannot reinterpret observed biology.

## Frozen inheritance
- Task: the single R9-qualified Tribolium future-radial-velocity task.
- Representation: R9 transductive percentile S/H representation.
- Models: exact R10 Random Forest and Extra Trees.
- Folds: reciprocal whole-acquisition 01/02.
- Gate 2: exact R10 rule.
- Seeds: documented family `20260830 + replicate`, replicates 0..29.
- Synthetic direction geometry: exact R12 secondary `domainwise_residualizer`: for each acquisition separately fit `Ridge(alpha=1)` S->z, residualize, then center/scale residual to mean 0 / SD 1 within that acquisition.
- Injection magnitude unit: pooled original target SD, identical to R10B/R12.
- The geometry is outcome-blind but transductive/acquisition-conditioned; it does not establish `E[Z|S]=0`.

## Frozen scale surface
Evaluate the same 30 documented directions at scales 0.15, 0.30, 0.45, and 0.60 target SD.

- **0.30 is inherited from committed R12 secondary results and must not be refit.**
- New outcome evaluations are only 0.15, 0.45, and 0.60.

For each scale report:
1. S-only adequacy count/rate;
2. Gate-2 detection count/rate;
3. joint success count/rate;
4. detection conditional on adequacy;
5. exact success replicate identities and paired transitions across scales.

## Decision rule
The historical 24/30 criterion is retained as a planning reference. R13 does not create a new confirmatory threshold. A scale reaching >=24/30 would mean only that this post-hoc planning geometry can achieve the old numerical sensitivity target on these same data/seeds; it would **not** validate screening-off or retroactively replace R10B.

## Prohibited changes
No changes after results to seeds, geometry, folds, models, Gate 2, outcome, history coordinates, target-SD convention, or scale grid. Do not add intermediate/favorable scales.

## Claim boundary
R13 is a paired planning surface on a transductive synthetic calibration. It is not biological evidence, not a deployment result, and not an oracle conditional-independence test.
