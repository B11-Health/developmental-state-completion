# R13 Domainwise Sensitivity Surface Checkpoint

Date: 2026-08-30
Decision: **BEST TESTED SCALE 22/30; FROZEN 24/30 STANDARD NOT REACHED**

## Frozen design
R13 prospectively evaluated the already-audited R12 secondary acquisition-specific Ridge-residualized geometry on the same documented 30 directions, same R9-qualified Tribolium radial task, same RF/ExtraTrees models, reciprocal acquisition folds, exact R10 Gate 2, and the fixed scale grid 0.15/0.30/0.45/0.60 target SD. The 0.30 arm is inherited from R12 and was not refit.

## Result
| scale | S-only adequacy | Gate-2 detection | joint success |
|---:|---:|---:|---:|
| 0.15 | 30/30 | 1/30 | **1/30 (3.3%)** |
| 0.30 | 30/30 | 18/30 | **18/30 (60.0%)** |
| 0.45 | 27/30 | 23/30 | **22/30 (73.3%)** |
| 0.60 | 27/30 | 22/30 | **20/30 (66.7%)** |

The best tested joint rate is 22/30 at 0.45 SD, two successes below the historical 24/30 planning reference. Increasing to 0.60 SD does not rescue the criterion and reduces joint success to 20/30.

## Interpretation
The acquisition-specific residualization geometry substantially improves the sensitivity surface relative to the earlier pooled geometry, but it still does not reach the frozen 80% standard on the preregistered grid. The surface is non-monotone at the aggregate level after 0.45 SD: stronger injection does not guarantee better joint success because adequacy and detection remain coupled.

This is a post-R12 planning result on the same transductive two-acquisition task and seed family. It does not replace R10B, does not validate screening-off, and does not justify selecting 0.45 SD as a new confirmatory threshold after seeing the result. A future confirmatory protocol must choose geometry and amplitude prospectively on new data/independent acquisitions.

R13_COMPLETE
