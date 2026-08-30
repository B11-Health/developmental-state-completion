# Absolute Predictive Adequacy Gate

Date: 2026-08-30
Status: methodological rule proposed from R5 failure analysis.

## Problem
The program often reports the incremental value of older information after a declared present representation, e.g.

`Delta_H = Score(S + H) - Score(S)`.

R5 shows that `Delta_H > 0` can be misleading when both `S` and `S+H` are poor predictors under the scientifically relevant group shift. In the Drosophila radial-velocity sensitivity, all three estimators showed positive H increments at richer S, yet every augmented model had negative leave-one-sequence-out R2 and was worse than a train-sequence-mean dummy baseline.

An improvement inside a failed predictor is not evidence of a stable future-relevant historical signal.

## Proposed program-wide gate
Before interpreting or promoting a residual-history increment, require all three layers:

1. **Absolute adequacy.** The augmented predictor must beat a simple train-only naive baseline under the same held-out groups and metric. For continuous outcomes, positive held-out R2 is a strong default check when meaningful; proper-score improvement over a train-only dummy is also required. For classification, use proper scores and discrimination/calibration against a train-only prevalence baseline.
2. **Increment stability.** The H increment must have the same material direction across prespecified estimators and held-out groups, not merely a favorable average driven by one model or group.
3. **Sensitivity calibration.** The pipeline must demonstrate power/sensitivity to a prespecified known-incomplete alternative and appropriate behavior on a known-complete/null control.

If layer 1 fails, classify the result **ADEQUACY-LIMITED** and stop before mechanistic interpretation. If layer 1 passes but layers 2 or 3 fail, classify **UNRESOLVED**.

## R5 application
### Raw future vector
Absolute R2 was negative for every model. At S2 the history gain ranged from -0.079 to +0.211 across estimators. Fails layers 1 and 2.

### Future radial velocity sensitivity
At S2, H gains were positive across Extra Trees, Random Forest and Ridge (+0.0735, +0.0810, +0.0657). However, the train-mean dummy achieved approximately R2=-0.003 on each held-out acquisition, while all learned S+H models were substantially worse (mean R2 roughly -0.35 to -0.61). Fails layer 1 decisively.

Therefore R5 is not a positive residual-history result.

## Why this matters beyond R5
The gate prevents three common errors:

- celebrating a relative improvement when domain shift has destroyed absolute prediction;
- treating estimator-specific rescue as biological evidence;
- interpreting a history coefficient/effect before verifying the model can predict the declared future in new biological groups.

This gate should be incorporated into future R2/R3-style preregistrations and any living-system analysis before promotion.
