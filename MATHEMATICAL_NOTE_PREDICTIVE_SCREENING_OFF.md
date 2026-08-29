# Mathematical note: predictive screening-off, loss functions, and decoder dependence

Date: 2026-08-29

## Scope

This note formalizes the statistical object underlying **developmental state completion**. The mathematics below is not claimed as new information theory. The contribution of the research program, if it survives, is biological/experimental: use calibrated prediction and intervention design to determine which present measurements are sufficient for specified developmental futures.

## 1. Population value of older history

Let

- `H` = older measured history;
- `S` = present measured state;
- `Y` = specified future outcome;
- `L(y,a)` = prediction loss.

For any information set `Z`, define the Bayes risk

\[
R_L^*(Y\mid Z)=\inf_f\;\mathbb E[L(Y,f(Z))],
\]

where the infimum is over all measurable predictors for which the risk exists.

Define the **population history value**

\[
\boxed{V_L(H\to Y\mid S)
=R_L^*(Y\mid S)-R_L^*(Y\mid S,H).}
\]

Because a predictor with access to `(S,H)` can ignore `H`,

\[
V_L(H\to Y\mid S)\ge 0.
\]

This is the population quantity that finite-sample cross-validation is trying to estimate. Negative held-out gains are therefore not “negative information”; they reflect estimation variance, regularization, model-class mismatch, or optimization error.

---

## 2. The log-loss identity

### Theorem 1 — Log-loss history value equals conditional mutual information

Assume regular conditional distributions exist and the relevant entropies are finite. Under logarithmic loss,

\[
L_{\log}(y,q)=-\log q(y),
\]

where `q` is a predictive conditional distribution, the Bayes-optimal predictor is the true conditional law. Hence

\[
R_{\log}^*(Y\mid S)=H(Y\mid S),
\]

and

\[
R_{\log}^*(Y\mid S,H)=H(Y\mid S,H).
\]

Therefore

\[
\boxed{V_{\log}(H\to Y\mid S)=I(Y;H\mid S).}
\]

### Corollary 1

Under the same assumptions,

\[
V_{\log}(H\to Y\mid S)=0
\]

if and only if

\[
Y\perp H\mid S
\]

(up to the usual almost-sure qualifications).

### Consequence

If the scientific claim is genuinely **distributional screening-off**, calibrated out-of-sample log loss is the natural target. R² is not an equivalent substitute.

---

## 3. Squared loss is weaker

### Theorem 2 — Squared-loss history value

Assume `Y` is square-integrable. Under squared-error loss,

\[
L_2(y,a)=(y-a)^2,
\]

the Bayes predictor is the conditional mean. Let

\[
m_S=\mathbb E[Y\mid S],\qquad
m_{SH}=\mathbb E[Y\mid S,H].
\]

Then the Pythagorean property of conditional expectation gives

\[
\boxed{V_2(H\to Y\mid S)
=\mathbb E[(m_{SH}-m_S)^2].}
\]

### Corollary 2

`V_2=0` if and only if

\[
\mathbb E[Y\mid S,H]=\mathbb E[Y\mid S]
\]

almost surely.

That is only **conditional-mean screening-off**. It does **not** imply

\[
Y\perp H\mid S.
\]

History may change variance, tails, multimodality, or other aspects of the future distribution while leaving the conditional mean unchanged.

### Example

Let `H` be a fair sign and let

\[
Y\mid H \sim \mathcal N(0,\sigma_H^2)
\]

with different variances for the two values of `H`. With no `S`, squared-loss history value is zero because both conditional means are zero, while log-loss history value is positive because the conditional distributions differ.

---

## 4. Decoder-limited state sufficiency

Real experiments do not optimize over all measurable predictors. Let `F_S` and `F_{SH}` be preregistered decoder classes, with `F_S` embedded in `F_{SH}` by allowing the larger model to ignore history.

Define

\[
V_{L,F}(H\to Y\mid S)
=\inf_{f\in F_S}R_L(f)
-\inf_{g\in F_{SH}}R_L(g).
\]

At population level this remains nonnegative for nested classes. But a finite-sample estimator

\[
\widehat V_{L,F}
\]

can be negative on held-out data because the larger model pays an estimation penalty.

This is the correct interpretation of the FM1 random-forest values where `current + history` can score slightly worse than `current`: the data do not contain “negative history information.” The fitted model simply fails to convert the extra variables into improved held-out risk.

### Operational rule

A biological state should never be called “complete” without specifying at least:

1. future task `Y`;
2. loss `L`;
3. current measurement stack `S`;
4. history `H` being tested;
5. decoder family `F`;
6. finite-sample calibration and detectable effect size;
7. developmental stage / compartment;
8. intervention family, if the claim is counterfactual.

---

## 5. A rejected monotonicity conjecture

A tempting conjecture is:

> If we add more present-state measurements, older history must become less useful.

This is false for conditional mutual information.

### Counterexample — XOR unmasking

Let `H` and `Z` be independent fair bits and define

\[
Y=H\oplus Z.
\]

With no current measurement,

\[
I(Y;H)=0,
\]

because `Y` is marginally independent of `H`.

Now add `Z` to the present state. Then

\[
Y\oplus Z=H,
\]

so

\[
\boxed{I(Y;H\mid Z)=1\ \text{bit}.}
\]

Adding the present measurement **increases** the detectable residual history from zero to one bit.

### Frozen rejection

> “Residual history information must decrease monotonically as the current measurement stack grows.”

**Rejected.** Conditioning can reveal dependencies that were marginally hidden.

### What remains monotone

This should not be confused with the separate causal-fiber result. If an experimental panel `Q_1` is contained in `Q_2`, then the set of worlds consistent with all observations in `Q_2` is a subset of the set consistent with `Q_1` (for the same tolerance convention). **Inverse-fiber refinement is monotone; conditional mutual information under added conditioning variables is not.**

---

## 6. Distributional state completion

For one future task, define exact distributional completion by

\[
\boxed{Y\perp H\mid S.}
\]

For a family of interventions `\Pi`, with counterfactual/policy-indexed futures `Y^\pi`, define task-family completion by

\[
\boxed{Y^\pi\perp H\mid S\quad\forall\pi\in\Pi.}
\]

Equivalently under Bayes-optimal log loss,

\[
I(Y^\pi;H\mid S)=0\quad\forall\pi\in\Pi.
\]

For approximate finite-sample work, the operational target is not zero but a preregistered tolerance:

\[
I(Y^\pi;H\mid S)\le \varepsilon_\pi
\]

or its calibrated predictive-risk analogue, together with demonstrated power to detect a biologically meaningful residual effect.

---

## 7. Relation to statistical sufficiency and Blackwell comparison

This framework is narrower than classical statistical sufficiency and Blackwell informativeness.

- Classical sufficiency is defined relative to an unknown parameter and a sampling model.
- Blackwell comparison asks whether one experiment is at least as informative as another across **all** decision problems.
- Developmental state completion asks whether a particular present measurement stack makes specified older history redundant for a **specified family of future developmental decisions/predictions**.

The correct novelty claim is therefore not a new definition of information or sufficiency. The candidate contribution is an experimental program that repeatedly **measures, perturbs, tests residual history, and expands the state only when a specified future task remains unresolved**.

---

## 8. Consequences for the current evidence

### FM1 late-L1

The reproduced near-zero R² history gain is evidence for weak **conditional-mean** residual history under the tested decoders, not proof of conditional independence. The stronger publication target should include probabilistic prediction and log-loss calibration.

### FM1 middle-L1

The large Ridge history gain but small tree-model gain shows decoder dependence. The state is therefore unresolved under the current operational definition.

### Weinreb/Klein control

The strong sister-fate gain and conditional dependence after coarse state conditioning behave as a positive control for **state incompleteness**. The current reduced state proxy clearly fails screening-off.

---

## 9. Next decisive analysis

For each public benchmark and the prospective living-plant study:

1. define a probabilistic future outcome;
2. fit preregistered probabilistic decoders;
3. report held-out log-loss improvement from history;
4. calibrate the same estimator on known-complete and known-incomplete simulators;
5. report a detectable residual-information threshold;
6. only then use “screening-off” language.

This replaces an informal R² threshold with a loss-aware, task-aware, calibration-aware criterion.
