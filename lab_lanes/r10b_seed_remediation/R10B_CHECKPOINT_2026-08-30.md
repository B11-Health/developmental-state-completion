# R10B Seed-Specification Remediation Checkpoint

Date: 2026-08-30
Decision: **R10 CALIBRATION-LIMITED CONCLUSION SURVIVES; NUMERIC SENSITIVITY ESTIMATE CORRECTED**

## Trigger
Independent audit found that R10's preregistration specified random residual-history direction seed `20260830 + r`, while the committed R10 implementation used `20260830 + 500000 + r`.

R10B executed the written seed family exactly, changing no other scientific setting.

## Corrected calibration result
Thirty +0.30 target-SD residual-history calibration replicates using seed `20260830 + replicate` produced:
- S-only adequacy preserved: **23/30**;
- Gate 2 detected the injected history effect: **19/30**;
- both requirements jointly satisfied: **16/30 = 53.3%**;
- preregistered requirement: **24/30 = 80%**.

Therefore calibration still **fails** under the documented seed family.

## Comparison with original implementation
The original R10 implemented-seed family (`20260830 + 500000 + r`) yielded 10/30 joint successes. The corrected documented-seed family yields 16/30. This shows the finite 30-direction sensitivity estimate is materially seed-family dependent.

However, both estimates remain well below the preregistered 24/30 threshold. Thus the decision-level conclusion is robust to this correction even though the reported numeric sensitivity is not.

## Scientific consequence
The observed R10 history increment remains near zero, but the corrected calibration still does not demonstrate enough sensitivity to interpret that near-zero increment as screening-off. Status remains **calibration-limited / unresolved**.

R10B does not change the observed history metrics, the 0/100 matched permutation result, R9 adequacy, or any biological task. It only repairs the synthetic calibration seed provenance.

## Required upstream correction
Future summaries should distinguish:
1. original implemented-seed calibration: 10/30;
2. documented-preregistration-seed remediation: 16/30;
3. frozen threshold: 24/30.

The safest current headline is: **the exact sensitivity estimate changed after seed-specification remediation, but calibration still failed decisively enough that screening-off remains unpromoted.**

R10B_COMPLETE
