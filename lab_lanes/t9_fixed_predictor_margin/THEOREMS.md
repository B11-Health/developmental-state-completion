# T9 Fixed-Predictor Adequacy-Margin Identities

Date: 2026-08-30
Status: exact finite-sample squared-error algebra; design interpretation only; no novelty or priority claim.

## 1. Deterministic setup
For vectors `y,p,b,z` on the same finite test set, define `y_a=y+a z` and `MSE(u,v)=n^{-1}||u-v||^2`. Let the predictor-vs-baseline adequacy margin be

`G(a;p,b)=MSE(b,y_a)-MSE(p,y_a)`.

Positive `G` means the predictor beats that baseline in squared error.

## 2. Exact fixed-predictor identity
**Theorem T9.1.** If `p` and `b` are held fixed as `a` changes,

`G(a;p,b)=G(0;p,b)+2a <z,p-b>`,

where `<u,v>=n^{-1}u^T v`.

### Proof
Expand both squared errors. The common `a^2||z||^2/n` term cancels exactly, leaving the displayed linear cross-term.

### Consequences
- If `<z,p-b>=0`, the baseline-relative MSE margin is exactly invariant for every injection amplitude.
- Synthetic variance alone does not mechanically force a fixed predictor to lose against a fixed baseline.
- If the alignment is nonzero, any margin crossing is linear in `a`; the direction/sign of alignment determines whether injection helps or hurts the margin.

## 3. Refit/baseline decomposition
Let `p_a` and `b_a` be the predictor and baseline actually used after injection. Then

`G(a;p_a,b_a) = G(0;p,b) + 2a<z,p-b> + B_a + R_a`,

where

`B_a = MSE(b_a,y_a)-MSE(b,y_a)`

and

`R_a = MSE(p,y_a)-MSE(p_a,y_a)`.

This is an exact add-and-subtract identity. `B_a` isolates baseline movement; `R_a` isolates the effect of refitting/changing the predictor relative to keeping `p` fixed.

Therefore, if the injection is centered so the chosen baseline does not move and it is orthogonal to `p-b`, any change in the adequacy margin is entirely the predictor-refit/generalization term `R_a`.

## 4. R2 sign corollary
On a fixed test sample, for amplitudes at which the target variance is strictly positive, ordinary R2 has the same sign as the predictor-vs-test-mean MSE margin. If `mean(z)=0`, then the test-mean baseline is fixed and

`G(a)=G(0)+2a<z,p-mean(y)>`.

Exact orthogonality makes this margin constant, so its sign is invariant wherever R2 is defined. For `a>=0`, positive alignment makes the margin nondecreasing: an initially nonnegative margin cannot collapse to negative, but an initially negative margin may cross to positive. Negative alignment gives the reverse one-sided statement. Therefore nonnegative alignment alone does **not** imply sign invariance. If an amplitude makes `Var(y_a)=0`, ordinary R2 is undefined and no sign claim applies.

## 5. Train-only-naive baseline corollary
Suppose a cross-domain fold uses a constant baseline equal to the training-outcome mean. If the injected direction has zero mean in the training domain, that baseline value is unchanged by injection. On the held-out domain, the exact T9.1 margin identity then applies to a fixed predictor and that unchanged constant baseline. If the held-out injection is also orthogonal to `p-b`, the predictor-vs-train-naive squared-error ordering cannot change solely because `a^2 Var(z)` increased.

## 6. Population oracle corollary
Let `Y=M+E` with `M=E[Y|S]`, and let the baseline be `E[Y]`. If `E[Z|S]=0`, then `E[Z]=0` and `E[Z(M-E[Y])]=0`. Holding the oracle present predictor `M` fixed while defining `Y_a=Y+aZ`, the squared-error advantage of `M` over the mean baseline is exactly `Var(M)` for every `a`.

This does **not** say the numerical R2 is constant; the denominator can change. It says the sign of population oracle R2 cannot become negative from an S-orthogonal injection alone.

## 7. Relation to R10–R12
R10–R12 refit RF/ExtraTrees after each injected outcome and use cross-acquisition evaluation. Therefore T9 does not predict their pass/fail outcomes directly. It instead identifies what must be responsible when adequacy changes: baseline shift, alignment of the injected direction with the held-out prediction contrast, predictor refitting/generalization, or combinations of those effects.

R12's domainwise construction centers the synthetic direction within each acquisition, which removes one baseline-shift route. Its 30/30 S-adequacy result is consistent with a more stable calibration geometry, but T9 does not prove causality because the nonlinear predictors are refit.

## 8. Safe takeaway
When diagnosing calibration-induced adequacy collapse, do not blame the added synthetic variance by itself. For fixed predictions and baselines the quadratic variance term cancels from the predictor-vs-baseline MSE margin. Inspect alignment, baseline movement, and refit/domain-generalization effects separately.
