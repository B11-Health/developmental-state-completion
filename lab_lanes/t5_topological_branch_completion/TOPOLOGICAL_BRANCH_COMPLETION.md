# Topological Branch Completion of a Measured State

Date: 2026-08-30
Status: adversarial mathematical development; no priority claim.

## 1. Problem
Let `X` be a smooth latent-state manifold, `h:X->S` the present measurement, and `F:X->Y` a smooth future-response map for a declared task/intervention family. The repository's local differential condition

`ker Dh_x subset ker DF_x`

says that infinitesimal directions invisible to `h` are also invisible to `F`. T4 showed that if every fiber of `h` is connected, this condition upgrades to global factorization `F=g o h`. T5 asks what remains missing when fibers are disconnected.

The answer is topological: the differential condition forces `F` to be constant on each connected component of a measurement fiber, but it does not force different connected components with the same measured value to share a future. The minimal deterministic completion therefore lives on the quotient that remembers **which connected component of the fiber contains the state**.

## 2. Fiber-component quotient
Define `x ~_h x'` iff
1. `h(x)=h(x')`, and
2. `x,x'` lie in the same connected component of the fiber `h^{-1}(h(x))`.

Let `R_h = X / ~_h` and `q_h:X->R_h` be the quotient map. This is the Reeb-space construction associated with `h` in the standard topological sense; T5 does not claim that construction as new.

There is a natural map `bar_h:R_h->S` satisfying `h=bar_h o q_h`.

## 3. Theorem: branch-completion factorization
**Theorem T5.1.** Let `h:X->S` be a smooth submersion and `F:X->R^m` smooth. If `ker Dh_x subset ker DF_x` for every `x`, then `F` is constant on every connected component of every fiber of `h`. Hence there is a unique set map `G:R_h->R^m` such that

`F = G o q_h`.

### Proof
Each fiber `h^{-1}(s)` is a smooth embedded submanifold with tangent space `ker Dh`. A connected component of a manifold is path connected. For a smooth path `gamma` inside one component,

`d/dt F(gamma(t)) = DF_{gamma(t)} gamma'(t) = 0`

because `gamma'(t) in ker Dh`. Therefore `F` is constant along every such path and thus on the entire connected component. Define `G([x])=F(x)`; the preceding argument makes this well-defined and uniqueness follows from surjectivity of `q_h`. QED.

This is a deterministic task-level factorization statement. It does not imply stochastic causal completeness, biological Markovity, or that the quotient is experimentally measurable.

## 4. Why `h` alone can fail
Take `X=R\{0}`, `h(x)=x^2`, `F(x)=x`. Here `Dh=2x` is nonzero everywhere, so `ker Dh={0}` and the kernel-inclusion condition is vacuously true. Yet `h(-x)=h(x)` while `F(-x)!=F(x)`, so no `g` satisfies `F=g o h`.

The fiber of any `s>0` contains two disconnected points/components. Adding branch bit `B=1{x>0}` yields

`F = (2B-1)*sqrt(h)`.

The executable `t5_branch_tests.py` freezes this counterexample.

## 5. Minimal finite branch-code lower bound
Suppose that for a fixed measured value `s`, the fiber `h^{-1}(s)` has connected components `C_1,...,C_k`. By T5.1, `F` is constant on each component; write `y_i=F(C_i)`. Let `m_s` be the number of distinct values among `{y_i}`.

**Theorem T5.2.** Any discrete completion `B` satisfying `F=g(h,B)` must use at least `m_s` distinguishable branch labels on that fiber. Therefore a binary code needs at least

`ceil(log2 m_s)` bits

at measured value `s`.

### Proof
If two components with distinct future values receive the same `B` label while `h=s` for both, then `g(s,B)` would have to equal two different values, impossible. Thus each future-distinct component class needs a different codeword. A `b`-bit code has at most `2^b` codewords. QED.

The bound is achievable as a representational statement by assigning one label per **future-response equivalence class** of fiber components. That does not mean the optimal label is available as a biological measurement; discovering a feasible proxy is an experiment-design problem.

For a finite family of fibers, a global fixed-width code requires at least `ceil(log2 max_s m_s)` bits. Infinite/continuous quotients require more careful topological or information-theoretic notions and are not reduced to a finite-bit slogan.

## 6. Intervention-indexed refinement
For an intervention family `Pi`, stack the declared response maps into `F_Pi`. Two fiber components are future-equivalent if their full response signatures agree across `Pi`.

**Theorem T5.3.** If `Pi subset Pi'`, then future-response equivalence under `Pi'` refines (or equals) equivalence under `Pi`. Consequently `m_s(Pi') >= m_s(Pi)` and the finite branch-code lower bound cannot decrease when the intervention family is enlarged.

Proof: equality of a larger response vector implies equality of every subvector; adding coordinates can split existing equivalence classes but cannot merge classes already distinguished by the smaller vector. QED.

This formalizes an important experimental principle: a state can be sufficient for a narrow intervention family and become incomplete when new interventions distinguish previously hidden branches.

## 7. Connection to Test Cover
Once fiber components are quotiented by full future-response equivalence, choosing a finite intervention panel that distinguishes the remaining classes is a separating-system/Test-Cover problem. T5's six-component finite example has four full response classes and needs at least two of three candidate experiments to separate all four classes. This is not a new Test-Cover theorem; the new value for this project is the decomposition:

`measurement fiber -> connected components -> future-response quotient -> separating intervention panel`.

It tells us *what* a perturbation panel should distinguish after local differential sufficiency has already been exhausted.

## 8. History as a proxy for missing branch state
Let `Z=h(X)` be measured present, `B` the hidden fiber-component/future-equivalence branch, `H` older measured history, and `Y` future. If

`Y independent H | (Z,B)`

but `H` is informative about `B` given `Z`, then `I(Y;H|Z)` may be positive while `I(Y;H|Z,B)=0`.

This gives a concrete interpretation of residual history that does not require a separate mystical memory variable: older measurements can act as a proxy for a presently unmeasured branch coordinate. The executable binary example gives `I(Y;H|Z)=0.3901597` bits at 15% proxy noise and exactly zero after `B` is added.

This is one possible explanation, not a universal claim. Residual history can also arise from model inadequacy, leakage, nonstationarity, measurement error, or true path-dependent mechanisms.

## 9. Approximate branch completion
For tolerance `epsilon` in a metric on future signatures, exact response classes may be compressed by grouping components whose within-group future diameter is <= `epsilon`. Let `N_epsilon(s)` be the minimum number of such groups needed to partition the fiber-component response set at `s`. Any deterministic epsilon-accurate finite branch code needs at least `ceil(log2 N_epsilon(s))` bits on that fiber.

T5's scalar example `[0,.03,.08,.51,.55,1.2]` at diameter tolerance `.1` has three groups and therefore needs at least two bits. In higher-dimensional response spaces, computing the minimum diameter-bounded partition can itself be combinatorial; T5 makes no generic efficient-algorithm claim.

## 10. What would make this scientifically useful
A biological application requires more than observing residual history. It requires a candidate present measurement `B_hat` motivated independently of the outcome, followed by a frozen test:
1. establish adequate held-out prediction from the present representation;
2. measure stable residual history beyond that present;
3. add `B_hat` without using future labels to define it;
4. test whether residual history collapses while future prediction is preserved/improved;
5. test the same representation across the declared intervention family.

If a branch candidate only works because it was constructed from future labels, it is a descriptive quotient, not a prospective state measurement.

## 11. Claim boundary
The mathematical takeaway is not "development has a hidden branch bit." It is:

> Under the differential kernel condition, disconnected components of a measurement fiber are the exact topological obstruction to upgrading local invisibility into global deterministic factorization. A sufficient completion may therefore require branch information that identifies future-distinct fiber components.

The Reeb-space/fiber-component quotient and separating-system ingredients are established mathematical ideas. The potentially useful contribution is their explicit synthesis into the intervention-indexed predictive-state-completion workflow and a falsifiable experimental design rule. Priority is not claimed.
