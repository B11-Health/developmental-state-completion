# R12 Domain-Balanced Calibration Checkpoint

Date: 2026-08-30
Decision: **CALIBRATION GEOMETRY MATTERS, BUT DOES NOT REACH THE FROZEN 80% SENSITIVITY STANDARD**

## Frozen reference
R10B, using the literal preregistered seed family `20260830+r` and the original pooled residualization/global-standardization geometry, produced 16/30 joint successes, with S-only adequacy preserved in 23/30 and Gate 2 detected in 19/30. The required promotion threshold was 24/30.

## Primary: domain-balanced scaling
R12 kept the same pooled outcome-blind residualizer but centered/scaled each residual separately within each acquisition before the same +0.30 pooled-target-SD injection. Result:
- S-only adequacy: 22/30
- Gate-2 detection: 19/30
- joint success: **16/30 (53.3%)**

The joint-success replicate set is exactly identical to R10B. Therefore simple equalization of residual mean/variance across acquisitions does not explain or rescue the corrected R10B calibration failure.

## Secondary: domainwise residualization
R12 then used the preregistered secondary diagnostic: fit the outcome-blind `S -> z` Ridge residualizer separately within each acquisition and center/scale the resulting residual within each acquisition before injection. Result:
- S-only adequacy: **30/30**
- Gate-2 detection: **18/30**
- joint success: **18/30 (60.0%)**

This geometry removes the adequacy-collapse component on these 30 seeds, but detection still fails in 12/30 and the joint rate remains below 24/30. It changes which directions succeed: four new successes appear relative to R10B and two R10B successes are lost.

## Interpretation
Within-acquisition centering/scaling of the pooled Ridge residual did not improve the 16/30 joint result or alter the R10B joint-success identities. The secondary acquisition-specific Ridge-residualized geometry changes the finite failure decomposition: S-only adequacy is 30/30, but Gate 2 still detects only 18/30 documented directions. This shows geometry sensitivity, not a unique causal explanation for the original failure.

R12 is post-hoc planning. It cannot reinterpret the near-zero observed history increment, cannot replace R10B, and cannot promote screening-off. The scientific estimand also changes: the primary construction is pooled Ridge-residualized against S, whereas the secondary construction is acquisition-specific Ridge-residualized against S using unlabeled S/H from each acquisition. Ridge residualization does not establish `E[Z|S]=0` or literal S-unpredictability. Both are transductive planning diagnostics, and the secondary is more strongly acquisition-conditioned. A future confirmatory protocol must choose that estimand prospectively.

R12_COMPLETE
