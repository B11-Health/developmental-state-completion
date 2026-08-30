# T8A Independent Adversarial Audit — T8 Calibration-Compatibility Envelope

Date: 2026-08-30
Base audited: local main `f73e49a215d87dfda9b1fad0031ca738e37e343d`
Audit branch: `lab-t8a-independent-audit-2026-08-30`
Overall verdict: **NEEDS QUALIFICATION**

## Executive verdict

T8's core calibration-envelope algebra is correct **after one missing oracle assumption is added**, but the theorem as currently stated is not exact under its own listed assumptions. The S-only curve is valid from `E[E|S]=0`, `E[Z|S]=0`, and `Cov(E,Z)=0`. The augmented `S+H` curve additionally requires that the augmented information reveal no residual conditional mean beyond the injected direction, for example

`E[E | S,H] = 0` almost surely,

with `Z` measurable from `(S,H)`.

Without that assumption, an `S+H` oracle may predict part or all of `E`. Then a positive predictor term is missing from `R2_{S+H}` and `Delta`, so the advertised iff condition and `Delta_max` are not exact for the broader model currently stated.

An exact finite counterexample satisfying every assumption written in T8 was constructed. It has `a=1/4`, `Var(M)=1`, `Var(E)=1/4`, `Var(Z)=1/2`, `r0=4/5`, `x=1/40`, `E[E|S]=0`, `E[Z|S]=0`, `Cov(E,Z)=0`, and `H=Z` so `S+H` reveals `Z` exactly. Yet `E=Z^2-1/2`, so `S+H` also reveals `E`. T8 predicts `R2_{S+H}=33/41` and `Delta=1/41`; the true population oracle values are `R2_{S+H}=1` and `Delta=9/41`. For `rho=3/4` and required `delta=1/10`, T8's iff says no compatible amplitude exists, while this nonzero amplitude satisfies both thresholds. Therefore the theorem as written is not an iff theorem under its stated assumptions.

With the strengthened condition `E[E|S,H]=0`, the original curves and envelope are recovered exactly. An independent exact-rational grid over 64 `(r0,rho,delta)` triples found no mismatch between the repaired interval condition and `r0 >= rho/(1-delta)`.

## 1. Exact oracle curves — NEEDS QUALIFICATION

Let `G = sigma(S,H)`, assume `Z` is `G`-measurable, and define

`g(S,H) = E[E | S,H]`.

From `E[E|S]=0` and `E[Z|S]=0`, the S-only oracle remains `M=m(S)`. Also `Cov(M,E)=0` and `Cov(M,Z)=0`. With `Cov(E,Z)=0`,

`Var(Y_a) = V_M + V_E + a^2 V_Z`.

Thus T8's S-only formula is correct:

`R2_S(a) = V_M / (V_M+V_E+a^2 V_Z) = r0/(1+x)`.

For the augmented oracle,

`E[Y_a | S,H] = M + aZ + g(S,H)`.

The residual is `E-g`. Because conditional expectation is an L2 projection,

`MSE_{S+H} = V_E - Var(g)`.

Also `Cov(g,Z)=E[gZ]=E[EZ]=0`, because `Z` is measurable in `(S,H)` and `Cov(E,Z)=0`. Therefore the exact generalized curve is

`R2_{S+H}(a) = [V_M + a^2 V_Z + Var(g)] / [V_M+V_E+a^2V_Z]`.

Writing

`q = Var(E[E|S,H]) / (V_M+V_E) >= 0`, 

this is

`R2_{S+H}(a) = (r0 + x + q)/(1+x)`

and

`Delta(a) = (x+q)/(1+x)`.

T8's displayed curves are the special case `q=0`, equivalently `E[E|S,H]=0` almost surely. Exact revelation of `Z` by `S+H` is not enough by itself.

### Exact counterexample

Take `S` independent Rademacher, `M=S`, and `Z` independent of `S` with probabilities `P(Z=-1)=1/4`, `P(Z=0)=1/2`, `P(Z=1)=1/4`. Let

`E = Z^2 - 1/2`, `H=Z`, and `a=1/4`.

Then:

- `E[E|S]=0`;
- `E[Z|S]=0`;
- `Cov(E,Z)=0` by symmetry;
- `S+H` reveals `Z` exactly;
- all required second moments are finite;
- `Var(M)>0` and `Var(Z)>0`.

But `E` is also a deterministic function of `H=Z`. The exact results are:

- `r0=4/5`;
- `x=1/40`;
- `q=1/5`;
- `R2_S=32/41`, matching T8;
- true `R2_{S+H}=1`, versus T8 `33/41`;
- true `Delta=9/41`, versus T8 `1/41`.

This independently disproves the augmented curve under the current assumption list.

## 2. Compatibility iff — NEEDS QUALIFICATION

Under the repaired `q=0` model, T8's compatibility proof is exact:

`R2_S >= rho` iff `x <= r0/rho - 1`,

`Delta >= delta` iff `x >= delta/(1-delta)`.

A feasible `x>=0` exists iff

`delta/(1-delta) <= r0/rho - 1`,

which is equivalent to

`r0 >= rho/(1-delta)`.

Independent exact-rational enumeration over 64 threshold triples reproduced this equivalence with zero mismatches.

Under T8's currently stated broader assumptions, however, `Delta=(x+q)/(1+x)`, so the detection threshold is

`x >= (delta-q)/(1-delta)`

when the right-hand side is positive; if `q>=delta`, detection is already available at `x=0`. Therefore the simple iff is not valid without setting `q=0`.

The exact counterexample above makes the failure concrete: with `rho=3/4`, `delta=1/10`, and `r0=4/5`, T8's criterion gives

`4/5 < (3/4)/(9/10) = 5/6`,

so it declares incompatibility. But at `a=1/4`, the actual oracle has `R2_S=32/41 > 3/4` and `Delta=9/41 > 1/10`.

## 3. `Delta_max = 1-rho/r0` — NEEDS QUALIFICATION

For the repaired `q=0` model and `r0>=rho>0`, the maximum is attained at

`x_max = r0/rho - 1`,

and

`Delta_max = x_max/(1+x_max) = 1-rho/r0`.

So the displayed formula is correct in that model.

For the broader stated model with `q>0`,

`Delta(x)=(x+q)/(1+x)`.

Its derivative is `(1-q)/(1+x)^2`. Because `q=Var(E[E|S,H])/B <= V_E/B = 1-r0 < 1` when `V_M>0`, it is nondecreasing, and the adequacy-boundary value is

`Delta_max = 1 - rho/r0 + q*rho/r0`.

Thus T8's current `Delta_max` understates the possible augmented-oracle increment whenever `(S,H)` predicts any residual conditional mean.

If `r0<rho`, there is no adequacy-preserving amplitude because `R2_S(x)<=r0` for all `x>=0`. In that case `1-rho/r0` is negative and should not be presented as a meaningful maximum.

## 4. Amplitude interval — PASS only for repaired `q=0` model

When `q=0`, `V_Z>0`, `B>0`, `0<rho<1`, and `0<delta<1`, the squared normalized interval is exactly

`delta/(1-delta) <= x <= r0/rho - 1`.

Since `x=a^2 V_Z/B`, the magnitude interval is

`sqrt(B/V_Z)*sqrt(delta/(1-delta)) <= |a| <= sqrt(B/V_Z)*sqrt(r0/rho-1)`.

The interval is defined only when the upper endpoint is nonnegative and the compatibility condition holds.

For the generalized `q` model the lower bound becomes

`max(0,(delta-q)/(1-delta)) <= x`,

so the original amplitude interval is not exact unless `q=0`.

The interval is symmetric in the sign of `a` only because the stated orthogonality assumptions eliminate the linear cross-term. If `Cov(E,Z) != 0`, sign matters and neither `x=a^2V_Z/B` nor a sign-symmetric interval is sufficient.

## 5. Boundary cases

### `r0 < rho` — PASS

No feasible amplitude exists in the repaired model because `R2_S(a)=r0/(1+x) <= r0 < rho` for all `x>=0`.

### `V_E = 0` — PASS with interpretation

Then `r0=1`. Under the repaired augmented assumption, compatibility reduces to

`1 >= rho/(1-delta)`, equivalently `rho+delta <= 1`.

At equality the compatible `x` is unique. If `E=0` almost surely, the strengthened condition is automatic.

### `delta -> 0` — PASS as a limit

The lower bound `delta/(1-delta)` tends to zero, and compatibility tends to the simple base-adequacy condition `r0>=rho`. At exactly `delta=0`, zero injection is admissible; T8 currently restricts to `0<delta<1`, so this is a limiting extension rather than part of the written theorem.

### `delta -> 1` — PASS as a limit

The lower bound diverges. For any fixed positive `rho`, no finite amplitude can preserve positive present adequacy while attain `Delta=1` in the repaired model. At exactly `delta=1`, the theorem's algebra using `1-delta` is undefined and should be handled separately.

### `rho -> 0` — NEEDS endpoint wording

For positive `rho`, the upper `x` bound grows without limit as `rho->0+`, and `Delta_max -> 1`. At exactly `rho=0`, present adequacy imposes no upper bound. For finite `a`, `Delta=x/(1+x)<1`; therefore `1` is a **supremum**, not a finite-amplitude maximum. T8 avoids this endpoint by assuming `0<rho<1`, but any boundary discussion should use supremum language.

### `rho -> 1` — PASS as a limit

For fixed `delta>0`, compatibility becomes impossible. At exactly `rho=1`, preserving `R2_S>=1` requires `r0=1` and `x=0`, which cannot produce positive injected-history `Delta` in the repaired model.

## 6. Cross-terms and predictor terms — NEEDS QUALIFICATION

T8 correctly excludes the variance cross-term `2a Cov(E,Z)` by explicitly assuming `Cov(E,Z)=0`.

It also correctly gets `Cov(M,E)=0` from `E[E|S]=0` and `Cov(M,Z)=0` from `E[Z|S]=0`, because `M=m(S)`.

The missing term is not a covariance cross-term. It is the augmented predictor contribution

`g(S,H)=E[E|S,H]`.

Its explained variance `Var(g)` belongs in the numerator of the augmented oracle `R2`. Pairwise zero covariance between `E` and `Z` does not imply `g=0`; nonlinear predictability can remain. The counterexample `E=Z^2-1/2` is exactly such a case.

A clean sufficient correction is:

> Assume `Z` is measurable with respect to `sigma(S,H)` and `E[E|S,H]=0` almost surely.

Then the augmented oracle predictor is exactly `M+aZ`, and all original T8 curves follow.

An equivalent formulation is to directly assume

`E[Y_a|S,H]=M+aZ`.

That statement is concise and exactly matches the proof step T8 currently uses without justification.

## 7. Relation to R10/R11 RF/ExtraTrees gates — PASS

T8 is appropriately separated from the empirical R10/R11 gate in its prose. That separation should be retained and, after this audit, strengthened rather than weakened.

R10/R11 differ from the idealized theorem in multiple material ways:

- they use finite-sample Random Forest and Extra Trees rather than population conditional-expectation oracles;
- they evaluate reciprocal whole-acquisition held-out `R2` and train-only-naive RMSE thresholds;
- the synthetic direction is only Ridge-residualized linearly against pooled registered `S`, which does not establish `E[Z|S]=0`;
- no condition establishes `Cov(E,Z)=0` relative to the unknown population oracle residual;
- the tree model sees the original history feature matrix `H`, not an oracle scalar `Z`; therefore `S+H` need not reveal the injected residual direction exactly in the functional sense needed by T8;
- conversely, `H` may carry finite-sample or nonlinear predictive information unrelated to the intended injected direction;
- finite-sample estimation error, domain shift, tree approximation, interactions, and changed target variance all affect the empirical gates.

Accordingly, T8 is **idealized design algebra only**. It is not a theorem about why a particular R10/R11 RF/ExtraTrees replicate passes or fails, and it cannot turn R10/R11's observed calibration plateau into a mathematically forced phenomenon.

## 8. Test audit — NEEDS QUALIFICATION

The original `test_t8_compatibility.py` passes, but its coverage can produce false confidence about the theorem's assumptions.

The tests call the same closed-form helper functions that encode the theorem and check identities among those outputs. For example, `test_identity` verifies that the programmed `r2_sh-r2_s` equals the programmed `delta`; it does not construct a joint distribution and independently compute population oracle conditional expectations. Likewise, the compatibility-boundary test checks algebra internal to the same formulas. These are useful regression tests for implementation arithmetic but not assumption-validation tests.

T8A adds independent finite-distribution checks in `audit_t8a.py` and `test_t8a_independent.py`:

1. an exact counterexample satisfying every written T8 assumption but falsifying the augmented curve and iff;
2. an exact `q=0` construction with `E[E|S,H]=0` that reproduces all original curves;
3. an exact-rational 64-triple envelope grid checking the repaired iff independently of T8's implementation helpers;
4. endpoint sanity checks for `r0<rho`, `V_E=0`, and threshold limits.

All T8A independent tests pass.

## 9. Exact correction

The minimum correction to preserve T8's intended theorem is to change the setup from

> Assume the augmented information `S+H` reveals `Z` exactly.

to something equivalent to

> Assume `Z` is measurable with respect to `(S,H)` and the augmented information contains no additional conditional-mean information about the base residual: `E[E|S,H]=0` almost surely. Equivalently, `E[Y_a|S,H]=M+aZ`.

Then retain `E[E|S]=0`, `E[Z|S]=0`, `Cov(E,Z)=0`, finite second moments, `V_M>0`, and `V_Z>0`.

Under that corrected setup:

- `R2_S(a)=r0/(1+x)` — **PASS**;
- `R2_{S+H}(a)=(r0+x)/(1+x)` — **PASS**;
- `Delta=x/(1+x)` — **PASS**;
- compatible amplitude exists iff `r0>=rho/(1-delta)` — **PASS**;
- `Delta_max=1-rho/r0` for `r0>=rho` — **PASS**;
- the magnitude interval in T8 — **PASS**;
- interpretation as an idealized calibration-design envelope, not an RF/ExtraTrees theorem — **PASS**.

Without that correction, the theorem-level claims about the augmented oracle, iff envelope, `Delta_max`, and amplitude lower bound are **FAIL as exact claims**, although the S-only curve and the underlying `q=0` algebra remain correct.

## 10. Safe statement

**Safe T8 statement:**

> In an idealized population squared-error model `Y=M+E`, `M=m(S)`, suppose `E[E|S]=0`, an injected direction `Z` satisfies `E[Z|S]=0` and `Cov(E,Z)=0`, and `(S,H)` reveals `Z` while providing no additional conditional-mean information about `E` (`E[E|S,H]=0`). Writing `r0=Var(M)/(Var(M)+Var(E))` and `x=a^2Var(Z)/(Var(M)+Var(E))`, the oracle curves are `R2_S=r0/(1+x)` and `Delta=x/(1+x)`. For `0<rho,delta<1`, an amplitude satisfying both `R2_S>=rho` and `Delta>=delta` exists iff `r0>=rho/(1-delta)`, with compatible `x` interval `delta/(1-delta) <= x <= r0/rho-1` and, when `r0>=rho`, `Delta_max=1-rho/r0`. This is elementary idealized design algebra only; it is not a theorem about the finite-sample R10/R11 RF/ExtraTrees gates.

If the no-extra-residual-information assumption is not imposed, use the generalized term `q=Var(E[E|S,H])/(Var(M)+Var(E))`, giving `R2_{S+H}=(r0+x+q)/(1+x)` and `Delta=(x+q)/(1+x)` instead of T8's simpler augmented curve.

## Audit artifacts

- `audit_t8a.py` — exact finite-distribution counterexample, repaired-model checks, exact-rational envelope grid, boundary checks.
- `audit_results.json` — machine-readable independent results.
- `test_t8a_independent.py` — independent assertions that the written assumptions admit the counterexample and that the strengthened model recovers T8.

T8A_COMPLETE
