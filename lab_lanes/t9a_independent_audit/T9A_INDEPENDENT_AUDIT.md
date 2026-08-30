# T9A Independent Adversarial Audit — Fixed-Predictor Adequacy-Margin Identities

Date: 2026-08-30
Audit target: `lab-t9-fixed-predictor-margin-2026-08-30` at `bca2bac`
Audit base: local `main` at `0bd4a819961459582d6def89c32d3115a69d9b77`
Audit lane: `lab-t9a-independent-audit-2026-08-30`

## Decision

**NEEDS QUALIFICATION**

The central finite-sample fixed-predictor identity, the add-and-subtract refit/baseline decomposition, the train-only-naive baseline corollary under its stated centering assumptions, and the population oracle margin identity under `E[Z|S]=0` are correct. The main defect is the written R2-sign corollary: nonnegative alignment does **not** by itself imply sign invariance. A negative initial margin can cross zero and become positive for positive amplitude. In addition, any R2 statement must exclude amplitudes at which the target variance is zero, because ordinary R2 is then undefined/degenerate. These are theorem-statement qualifications, not failures of the core MSE-margin algebra.

## Repository / chronology check

- `bca2bac` has merge-base exactly `0bd4a819961459582d6def89c32d3115a69d9b77` with local `main`; therefore the audited T9 commit is directly based on the requested current-main floor.
- T9 adds only `lab_lanes/t9_fixed_predictor_margin/*` files.
- The independent T9A worktree was created from current main; the T9 source was inspected from the target commit rather than modified in place.

## 1. Fixed-predictor identity

T9 defines

`G(a;p,b) = MSE(b, y+a z) - MSE(p, y+a z)`

with normalized inner product `<u,v> = n^{-1} u^T v`. For fixed `p` and fixed `b`, direct expansion gives

`G(a;p,b) = G(0;p,b) + 2 a <z,p-b>`.

**Audit result: PASS.**

The `a^2 <z,z>` term is identical in the two squared errors and cancels exactly. The sign of the cross-term in T9 is correct. Independent random checks covered scalar constant baselines and vector baselines and obtained maximum absolute error `5.329e-15`.

### Vector/scalar baseline convention

The theorem is valid for any baseline vector `b` conformable with `y,p,z`. A scalar constant baseline is a special case via replication/broadcasting. T9's mathematical statement says vectors, while its code accepts scalar constants through NumPy broadcasting. There is no algebraic conflict, but downstream prose should distinguish:

- a **fixed arbitrary vector baseline**, for which T9.1 applies exactly;
- a **fixed scalar constant baseline**, likewise exact;
- a **mean baseline recomputed from `y_a`**, which is not fixed unless centering makes the mean unchanged.

## 2. Exact refit/baseline decomposition

T9 states

`G(a;p_a,b_a) = G(0;p,b) + 2a<z,p-b> + B_a + R_a`,

where

`B_a = MSE(b_a,y_a)-MSE(b,y_a)`

and

`R_a = MSE(p,y_a)-MSE(p_a,y_a)`.

**Audit result: PASS.**

This is a literal add-and-subtract identity. Independent checks with moving **vector-valued** `b_a` and changed `p_a` gave absolute residual `2.220e-16`. The labels “baseline movement” and “refit/changing-predictor effect” are descriptive accounting labels; neither term by itself establishes a causal mechanism.

### Required wording qualification

The sentence “if the injection is centered so the chosen baseline does not move” is safe only when the baseline rule is one whose value is actually frozen by that centering (for example, a domain mean baseline centered in that same domain). Centering does not generically freeze every possible baseline construction.

## 3. R2-sign corollary

For a test target with strictly positive sample variance and the ordinary test-mean denominator,

`R2(a) = 1 - MSE(p,y_a) / MSE(mean(y_a),y_a)`.

Whenever the denominator is positive, `sign(R2(a)) = sign(G(a;p,mean(y_a)))`.

If `mean(z)=0`, then `mean(y_a)=mean(y)`, so the baseline is fixed and T9.1 gives

`G(a) = G(0) + 2a <z,p-mean(y)>`.

**Audit result: NEEDS QUALIFICATION.**

The T9 text says: “if `<z,p-mean(y)> >= 0`, the sign of R2 is invariant under injection.” That is false without additional restrictions. Positive alignment makes the margin nondecreasing for `a>=0`; it does not prevent a negative margin from crossing zero.

### Explicit counterexample

Take

- `y=(-1,1)`, so `mean(y)=0`;
- `z=(-1,1)`, so `mean(z)=0`;
- fixed predictor `p=3y`.

Then `<z,p>=3>0`, but

- at `a=0`, `G=-3` and `R2=-3`;
- at `a=1`, `G=+3` and `R2=0.75`.

Thus the sign changes despite centered `z` and positive alignment.

### Corrected R2 statement

For amplitudes where `Var_test(y_a)>0`:

- exact orthogonality `<z,p-mean(y)>=0` **with equality** makes `G(a)` constant, hence the R2 sign is constant wherever R2 is defined;
- if `a>=0`, alignment `c=<z,p-mean(y)> > 0` makes `G(a)` nondecreasing. Therefore an initially nonnegative margin cannot collapse to negative, but an initially negative margin may cross to positive;
- if `a>=0`, `c<0` makes `G(a)` nonincreasing. Therefore an initially nonpositive margin cannot cross to positive, but an initially positive margin may collapse;
- for unrestricted signed amplitudes, only the exact affine formula determines crossings.

### Degenerate denominator

Even exact orthogonality does not guarantee that ordinary R2 remains defined for every amplitude. Independent construction:

- `y=(-1,-1,1,1)`;
- `z=-y` (centered);
- `p=(1,-1,1,-1)`;
- `<z,p>=0`.

The MSE margin is identical at `a=0` and `a=1`, but `y+z` is constant at `a=1`, so the ordinary R2 denominator is zero and R2 is undefined. T9 should say “sign invariant for all amplitudes **for which the R2 denominator is strictly positive**.”

The existing T9 test named `test_centered_r2_sign_margin` tests only an exact-orthogonality, initially-positive example; it does not test the stronger nonnegative-alignment sentence and therefore misses this counterexample.

## 4. Train-only-naive baseline corollary

Suppose the baseline is the scalar training-outcome mean and training-domain injection has zero mean. Then

`mean_train(Y_train + a Z_train) = mean_train(Y_train)`

for every `a`, so the scalar baseline is unchanged. On the held-out sample T9.1 applies to fixed `p` and this unchanged baseline. If the held-out direction is also orthogonal to `p-b`, the held-out MSE margin is invariant.

**Audit result: PASS, with explicit domain-centering qualification.**

The train and held-out conditions are logically distinct:

1. zero **training-domain** mean of `z` freezes the train-naive scalar baseline;
2. held-out orthogonality controls the fixed-predictor margin on the held-out domain.

Zero mean on one domain does not imply zero mean or orthogonality on the other. Independent checks confirm baseline movement immediately returns if train-domain centering fails.

## 5. Population oracle margin

Let `M=E[Y|S]`, `Y=M+E`, baseline `mu=E[Y]`, and define `Y_a=Y+aZ`. Since `M=E[Y|S]`, `E[E|S]=0`. Under `E[Z|S]=0`:

- `E[Z]=0`, hence `E[Y_a]=mu`;
- `E[(M-mu)E]=0`;
- `E[(M-mu)Z]=0`.

Therefore

`E[(Y_a-mu)^2] - E[(Y_a-M)^2] = E[(M-mu)^2] = Var(M)`.

Also `E[Y_a|S]=M`, so `M` remains the population squared-loss oracle given `S`.

**Audit result: PASS.**

No additional assumption such as `Cov(E,Z)=0` is needed for this *difference* identity: terms involving `E+aZ` that are common to both squared errors cancel, while the only cross-term with `M-mu` vanishes from the conditional-mean assumptions. An independent finite equiprobable construction reproduced the identity exactly for multiple positive and negative amplitudes.

### Assumption-failure counterexample

If `E[Z|S]=0` is dropped, the conclusion can fail. Let `Y=M=S` with `S in {-1,+1}` equiprobable and `Z=-M`. At `a=0.75`, the fixed predictor `M` has population baseline-relative margin `-0.5` and population R2 `-8`. This is not a counterexample to T9 because its key conditional-centering assumption is violated; it demonstrates why that assumption is essential.

## 6. Can quadratic injection variance alone force fixed-predictor adequacy collapse?

**Audit result: PASS for the narrowly stated fixed-`p`, fixed-`b`, squared-error margin claim.**

For fixed `p,b`, the quadratic injection term cancels identically. Consequently the standalone magnitude `a^2 <z,z>` cannot itself change the predictor-vs-baseline MSE ordering. Any change in `G(a)` comes through the linear alignment `2a<z,p-b>`.

This claim must not be broadened to either of the following:

- **moving baselines**: if the baseline is recomputed from `y_a` and centering does not freeze it, extra amplitude dependence appears through `B_a`;
- **refit predictors**: RF/ExtraTrees or any other model refit after outcome injection changes `p_a`, represented by `R_a`, and can show nonlinear or nonmonotone empirical behavior.

### Moving-baseline counterexample

With `y=(-1,1)`, fixed `p=y`, and noncentered `z=(0,2)`, at `a=3`:

- against the original fixed baseline `b=0`, the margin is `+7`;
- against the recomputed test-mean baseline, the margin is `-2`.

Thus cancellation of the fixed-baseline quadratic term must not be read as a theorem about an outcome-dependent baseline.

## 7. Relation to R10–R12 RF/ExtraTrees

**Audit result: PASS.**

T9 explicitly says R10–R12 refit RF/ExtraTrees after each injected outcome and that T9 does not predict those empirical pass/fail outcomes directly. This boundary is essential and should remain prominent. T9 can provide an exact accounting decomposition for comparison with a chosen fixed reference predictor/baseline, but it does not establish that observed adequacy changes in refit nonlinear models are caused by one particular term.

The checkpoint phrase “clarifies why finite-sample adequacy collapse in R10–R12 cannot be attributed to synthetic variance alone” is acceptable only if read as the algebraic diagnostic point above, not as a direct mechanistic theorem about the refitted estimators. Safer wording is “shows that the common quadratic target-injection term is not, by itself, sufficient to change a **fixed-predictor/fixed-baseline** MSE margin.”

## 8. Code/test audit

Target tests pass (`T9_TESTS_PASS`). Independent T9A checks pass (`T9A_CHECKS_PASS`). No sign error was found in `t9_margin.py`; the exact identity and decomposition implementation are correct.

Coverage gap: the target suite does not test

- a positive-alignment / negative-initial-margin R2 sign crossing;
- zero target-variance R2 degeneracy;
- a moving outcome-dependent baseline;
- failure of the population result when `E[Z|S]=0` is violated.

T9A adds independent executable examples for all four boundaries.

## Exact corrections requested

1. Replace the R2 sentence

   `if <z,p-mean(y)> >= 0, the sign of R2 is invariant under injection`

   with a monotonicity statement conditioned on amplitude direction and initial margin, or restrict sign invariance to exact orthogonality.

2. Add the denominator condition `Var_test(y_a)>0` to all ordinary-R2 sign statements.

3. Clarify that centering freezes a mean-derived baseline only when centering is performed in the same domain/sample used to construct that baseline.

4. Keep the RF/ExtraTrees boundary explicit: T9 is fixed-predictor/fixed-baseline squared-error algebra plus an exact accounting decomposition, not a theorem that refit nonlinear predictors must preserve adequacy.

## Safe statement

For squared error on a fixed evaluation sample, if both predictor `p` and baseline `b` are fixed while the target is changed from `y` to `y+a z`, then

`G(a)=MSE(b,y+a z)-MSE(p,y+a z)=G(0)+2a<z,p-b>`.

Hence the common quadratic injection term cancels exactly. Under exact orthogonality to `p-b`, the fixed predictor-vs-baseline MSE margin is invariant with amplitude. If either predictor or baseline changes, the exact additional terms are baseline movement and predictor-change/refit terms. For an ordinary test-mean R2, centered `z` freezes the mean baseline, but R2-sign invariance follows from exact orthogonality only at amplitudes where the target variance is nonzero; nonzero alignment gives an affine/monotone margin and may permit a zero crossing. At population level, if `M=E[Y|S]` and `E[Z|S]=0`, the fixed oracle `M` remains the conditional-mean predictor for `Y+aZ`, and its mean-baseline squared-error advantage is exactly `Var(M)`. None of these identities directly predicts the behavior of refit RF/ExtraTrees models.

T9A_COMPLETE
