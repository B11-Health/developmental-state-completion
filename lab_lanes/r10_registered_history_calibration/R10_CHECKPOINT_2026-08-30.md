# R10 Registered-History Calibration Checkpoint

Date: 2026-08-30
Decision: **HISTORY INCREMENT NEAR ZERO, BUT CALIBRATION-LIMITED / DO NOT PROMOTE SCREENING-OFF**

## Eligibility
R10 is restricted to the single R9 primary Gate-1 pass: Tribolium future radial velocity with transductive within-acquisition percentile registration. No other organism, outcome, horizon or registration method was tested for history.

## Observed registered history increment
The adequate present representation remains adequate after adding H, but older history does not show a stable positive gain:

| Estimator | Held-out seq01 R2(S) | R2(S+H) | Delta R2 | Held-out seq02 R2(S) | R2(S+H) | Delta R2 | Mean Delta R2 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Random Forest | 0.08139 | 0.07388 | -0.00751 | 0.11426 | 0.11572 | +0.00146 | -0.00303 |
| Extra Trees | 0.11521 | 0.11148 | -0.00374 | 0.22404 | 0.21692 | -0.00712 | -0.00543 |

Gate 2 therefore **fails**: neither estimator has positive Delta R2 in both folds or mean Delta R2 >=+0.02.

## Matched no-increment null
Across 100 deterministic H-permutation replicates, **0/100** satisfy the full two-model Gate-2 rule. At this finite resolution, the matched false-positive rate is 0%. This shows the Gate-2 rule is not trivially firing under unrelated H in this sample/model stack.

## Known-incomplete +0.30-SD calibration
Thirty synthetic residual-history directions were injected at +0.30 times the original target SD using only the existing H coordinates and outcome-blind residualization against S.

- Gate 2 fires in 15/30 synthetic datasets regardless of S adequacy.
- The original two-model S-only adequacy prerequisite remains satisfied in 19/30 datasets.
- Both requirements are simultaneously met in only **10/30 (33.3%)** datasets.
- Conditional on S adequacy being preserved, detection is 10/19 (52.6%).
- Preregistered requirement: at least **24/30 (80%)** joint successes.

Calibration therefore **fails**.

## Interpretation
The observed increment is near zero and the matched null is clean, but the analysis does not have enough demonstrated sensitivity to promote a bounded screening-off conclusion at the preregistered +0.30-SD synthetic-history scale. The correct status is **calibration-limited / unresolved**.

This is a scientifically important distinction: R9 solved the absolute-prediction prerequisite for one task under a transductive deployment assumption, but that success does not automatically make residual-history inference well powered.

## What is supported
- Outcome-blind target-distribution registration materially rescues cross-acquisition present-state prediction for Tribolium radial velocity.
- In that adequate representation, the observed older-history increment is extremely small and not directionally stable.
- The current sample/model stack cannot reliably detect the preregistered +0.30-SD synthetic residual-history effect while preserving the same adequacy prerequisite.

## What is not supported
- Do not say older history is useless/redundant.
- Do not say Tribolium is Markov or memoryless.
- Do not reinterpret earlier R5/R6 history gains as biological memory.
- Do not generalize to Drosophila, speed, other horizons, other acquisitions or living systems.

## Next defensible move
Increase independent acquisition count and/or improve the registered present model so sensitivity can be demonstrated without losing absolute adequacy under injected history. A future history conclusion should be attempted only after a power design that meets the preregistered calibration threshold.

R10_COMPLETE
