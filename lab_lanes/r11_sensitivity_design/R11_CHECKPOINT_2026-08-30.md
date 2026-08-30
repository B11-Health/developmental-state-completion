# R11 Calibration-Failure Decomposition and Sensitivity-Surface Checkpoint

Date: 2026-08-30
Decision: **AGGREGATE ADEQUACY–DETECTABILITY TRADEOFF ON TESTED GRID / PLANNING ONLY**

## Scope and provenance
R11 is a planning-only follow-up to the original R10 implementation. It does not reinterpret the observed near-zero history increment. It evaluates the first 20 **implemented R10 seed-family** residual directions (`20260830+500000+r`) at 0.15, 0.30, 0.45, and 0.60 target SD. The 0.30 arm is inherited and was not refit.

Independent R11A audit later found that R10's literal preregistration had written `20260830+r`; R10B subsequently remediated that discrepancy and obtained 16/30 joint successes at +0.30 SD, still below 24/30. Thus R11 is retained as a planning diagnostic of the original implemented-seed family, not as the controlling corrected R10 calibration.

## Main aggregate result
| Injected history scale | S-only adequacy A | Gate-2 detection D | Joint J | D conditional on A |
|---:|---:|---:|---:|---:|
| 0.15 SD | 17/20 = 85% | 0/20 = 0% | 0/20 = 0% | 0/17 = 0% |
| 0.30 SD | 14/20 = 70% | 9/20 = 45% | 6/20 = 30% | 6/14 = 42.9% |
| 0.45 SD | 11/20 = 55% | 12/20 = 60% | 6/20 = 30% | 6/11 = 54.5% |
| 0.60 SD | 9/20 = 45% | 15/20 = 75% | 6/20 = 30% | 6/9 = 66.7% |

Across these four grid points, aggregate Gate-2 detection increases while aggregate S-only adequacy decreases. The aggregate joint rate is 30% at 0.30, 0.45, and 0.60 SD. This is a **grid-level aggregate plateau**, not a replicate-wise monotonic law: R11A found at least one direction whose Gate-2 pass status reverses between 0.45 and 0.60, and the identities of the six joint-success directions change across scales.

## Original R10 implemented-seed decomposition
Across all 30 original implemented-seed calibration directions: 10 joint pass, 9 adequacy-only, 5 detection-only, and 6 neither. This shows that the original 10/30 failure mixed under-detection with loss of S-only adequacy. R10B's documented-seed remediation later changed the joint count to 16/30 while preserving the calibration-fail decision.

## Protocol consequence
Future calibration should separately freeze and report `A(a)` (S adequacy), `D(a)` (history detection), `J(a)` (joint success), and `D|A(a)`. A single generic "power" percentage can hide opposing failure modes. On this tested original-seed grid, merely increasing injection magnitude did not raise the strict joint rate above 30%. This does not rule out behavior outside the tested grid and is not a universal nonmonotonicity theorem.

## Reproducibility/audit
R11A independently verified exact replicate coverage, zero metric-to-decision mismatches, the committed summary, and selected deterministic refits. It also identified the R10 seed mismatch and a code-hardening issue: aggregation should explicitly reject duplicate or missing replicate IDs. The R11 executable has now been hardened to require the exact unique set `0..19` for every summarized scale.

## Claim boundary
R11 does not establish history redundancy, biological memory, Markovity, non-Markovity, or a biological effect-size threshold. R10B controls the corrected preregistration-seed sensitivity conclusion: 16/30 < 24/30, calibration-limited/unresolved.

R11_COMPLETE_QUALIFIED
