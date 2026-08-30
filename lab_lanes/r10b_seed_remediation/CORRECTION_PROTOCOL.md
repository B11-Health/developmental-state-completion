# R10B Seed-Specification Remediation Protocol

Date: 2026-08-30
Status: FROZEN BEFORE REMEDIATION RUNS

## Trigger
Independent R11A audit found a reproducibility discrepancy in R10: `PREREGISTRATION.md` specifies synthetic residual-history direction seed `20260830 + r`, while committed `r10_history_calibration.py` uses `20260830 + 500000 + r`.

## Correction question
Does R10's calibration-limited decision survive when the +0.30 target-SD known-incomplete calibration is executed with the **documented preregistration seed family** exactly as written?

## Frozen correction
Change only the random-direction seed from `SEED + 500000 + rep` to `SEED + rep` for the 30 calibration directions. Preserve exactly:
- Tribolium future radial velocity only;
- R9 transductive within-acquisition percentile registration;
- same R8 99-feature present matrix and four H columns;
- same RF/ExtraTrees settings and reciprocal acquisition folds;
- same outcome-blind Ridge residualization of the random H combination against S;
- same +0.30 original-target-SD injection;
- same Gate 2 and S-only adequacy definitions;
- same success rule: Gate 2 AND S-only adequacy preserved;
- same threshold: >=24/30 successes required to pass calibration.

No other parameter may be changed after results are observed. The original implemented-seed result (10/30) remains part of the provenance record and must not be deleted.

## Decision
- If documented-seed success remains <24/30: R10's calibration-limited conclusion survives, with corrected provenance.
- If documented-seed success is >=24/30: R10's calibration interpretation must be reopened and downstream R11 language revised accordingly.

This lane is a reproducibility correction, not a new biological experiment.
