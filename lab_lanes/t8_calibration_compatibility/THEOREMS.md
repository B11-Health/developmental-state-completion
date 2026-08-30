# T8 Calibration Compatibility Envelope — Audited Form

Date: 2026-08-30
Status: corrected after independent T8A audit; elementary idealized calibration algebra; no novelty or priority claim.

## 1. Setup
Let `Y=M+E`, with `M=m(S)` and `E[E|S]=0`. Let `Z` be a synthetic omitted-history direction with `E[Z|S]=0`, finite second moments, and define `Y_a=M+E+aZ`.

For the **simple envelope theorem**, assume additionally:
1. `Z` is measurable with respect to `(S,H)`;
2. `E[E|S,H]=0` almost surely, equivalently the augmented information contains no conditional-mean information about the base residual beyond `M+aZ`;
3. `Cov(E,Z)=0` (this is implied by 1–2 but retained explicitly for the variance decomposition);
4. `V_M=Var(M)>0`, `V_Z=Var(Z)>0`, and all relevant second moments are finite.

Write `V_E=Var(E)`, `B=V_M+V_E`, `r0=V_M/B`, and `x=a^2 V_Z/B`. These are population squared-error oracle quantities, not finite-sample RF/ExtraTrees gates.

## 2. Exact simple-envelope curves
Under the assumptions above,

`R2_S(a)=r0/(1+x)`,

`R2_{S+H}(a)=(r0+x)/(1+x)`,

and

`Delta(a)=R2_{S+H}-R2_S=x/(1+x)`.

### Proof
`E[E|S]=0` and `E[Z|S]=0` imply `E[Y_a|S]=M`. The S-only residual is `E+aZ`, whose variance is `V_E+a^2V_Z`. By measurability of `Z` and `E[E|S,H]=0`, `E[Y_a|S,H]=M+aZ`; the augmented residual is exactly `E`, with variance `V_E`. The total variance is `V_M+V_E+a^2V_Z`. Substitution into `R2=1-MSE/Var(Y_a)` gives the three formulas.

## 3. Compatibility theorem
Fix `0<rho<1` and `0<delta<1`. An injection amplitude satisfying both

`R2_S(a)>=rho` and `Delta(a)>=delta`

exists **iff**

`r0 >= rho/(1-delta)`.

Equivalently, if `r0>=rho`, the largest oracle incremental R2 compatible with the present-only threshold is

`Delta_max = 1-rho/r0`.

### Proof
Adequacy gives `x <= r0/rho-1`; detection gives `x >= delta/(1-delta)`. The interval is nonempty iff `delta/(1-delta) <= r0/rho-1`, equivalent to the displayed condition. At `x_max=r0/rho-1`, `Delta=x/(1+x)=1-rho/r0`.

## 4. Compatible amplitude interval
When the condition holds,

`delta/(1-delta) <= x <= r0/rho-1`.

Because `x=a^2V_Z/B`,

`sqrt(B/V_Z)*sqrt(delta/(1-delta)) <= |a| <= sqrt(B/V_Z)*sqrt(r0/rho-1)`.

This is a calibration-design range, not a biological effect-size range.

## 5. Generalized augmented-information form
T8A showed that exact revelation of `Z` does **not** by itself imply the simple augmented curve. Let

`g(S,H)=E[E|S,H]` and `q=Var(g)/B`.

If `Z` is measurable from `(S,H)` and `Cov(E,Z)=0`, then the exact augmented oracle is

`R2_{S+H}(a)=(r0+x+q)/(1+x)`

and

`Delta(a)=(x+q)/(1+x)`.

The simple T8 envelope is exactly the special case `q=0`, i.e. `E[E|S,H]=0`. For `q>0`, the detection lower bound becomes

`x >= max(0,(delta-q)/(1-delta))`,

while the adequacy upper bound remains `x <= r0/rho-1`. When `r0>=rho`, the adequacy-boundary increment is

`Delta_max(q)=1-rho/r0 + q*rho/r0`.

This generalized form prevents hidden augmented predictability of the base residual from being misattributed to the injected history direction.

## 6. Boundary consequences
- If `r0<rho`, no amplitude can preserve the present threshold because `R2_S(a)<=r0`.
- If `V_E=0`, then `r0=1`; in the simple envelope compatibility reduces to `rho+delta<=1`.
- As `delta->0+`, compatibility approaches `r0>=rho`; at `delta=0`, zero injection is allowed.
- As `delta->1-`, the required lower injection diverges for any positive `rho`.
- As `rho->0+`, the upper bound diverges and `Delta` approaches 1 only as a supremum for finite amplitudes.
- At `rho=1`, positive injected history cannot coexist with `R2_S>=1`.

## 7. Relation to R10/R11/R12
The theorem is deliberately more idealized than the empirical pipeline. R10–R12 use finite-sample RF/ExtraTrees, reciprocal held-out acquisitions, positive held-out R2 plus train-only-naive RMSE, linearly residualized synthetic directions, and a history feature matrix rather than an oracle scalar `Z`. None of those empirical lanes establishes the conditional-expectation assumptions required above.

Therefore T8 is a calibration-design envelope only. It cannot prove why a particular R10/R11/R12 replicate passes or fails, cannot turn an empirical plateau into a theorem, and cannot establish biological screening-off. In particular, if one maps only the empirical positive-R2 condition to `rho=0`, the simple oracle curve remains positive for every finite `x`; therefore the negative held-out R2/naive-baseline failures seen empirically must come from finite-sample estimation, refitting, domain shift, baseline mismatch, or other effects not represented by the simple T8 model.

## 8. Safe methodological takeaway
Before requiring a synthetic calibration to both preserve present-state adequacy and detect omitted history, declare what the augmented information is allowed to predict. If `(S,H)` predicts base residual structure in addition to the injected direction, use the generalized `q` form; if the intended stress test isolates the injected direction, enforce or assume `E[E|S,H]=0`. Only then does the simple compatibility envelope apply.
