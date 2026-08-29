# LAB LANE M1 — theorem/counterexample checkpoint — 2026-08-29

## Status

**Falsification-first independent pass.** All code and outputs in this directory are local workspace artifacts. Nothing was pushed or published.

Primary executable: `lab_lanes/math/m1_math_verification.py`  
Machine-readable results: `lab_lanes/math/m1_results.json`

The original 224-world / Source640 simulator and its response matrix are **not present in the current public repository or its visible Git history**, and a workspace filename/content search did not locate a preserved Source640 artifact. I therefore did not invent or reconstruct that dataset. The finite tests below use:

1. the preserved 128-world x 16-context prospective two-context source bundle under `source_validation/two_context_2026-08-26/`; and
2. explicit adversarial finite constructions for theorem/counterexample tests.

The topology-sensitive source-bundle tests require a graph because the saved source bundle contains response data but no canonical world-space adjacency. I therefore declare the topology proxy rather than hide it: each law has a 4-cube over binary states, and equal states across laws are connected along a minimum spanning tree in the four-dimensional gain-vector space. Claims depending on this graph are labeled **proxy-dependent**.

---

## Executive verdict

At least one nontrivial positive result survives attempted counterexamples, and two useful sharpenings are stronger than the previous checkpoint.

### Surviving positive result A — finite **resolution** separation from compactness

Let `(X,d)` be a compact metric space of behaviorally distinct worlds. Let `{f_q : X -> Y_q}_{q in Q}` be a family of continuous experiments into metric spaces that separates points: for every `x != y`, some `q` has `rho_q(f_q(x),f_q(y)) > 0`.

For every fixed hidden-world resolution `epsilon > 0`, there exists a **finite** experiment panel `Q_epsilon` and a **uniform positive observation margin** `gamma_epsilon > 0` such that

`d(x,y) >= epsilon  =>  max_{q in Q_epsilon} rho_q(f_q(x),f_q(y)) >= gamma_epsilon`.

This is stronger and cleaner than the previous wording. Compactness is insufficient for one finite **exact** separator on all distinct pairs because `X x X \ Delta` need not be compact, but it is sufficient at every fixed positive resolution because

`K_epsilon = {(x,y): d(x,y) >= epsilon}`

is compact. The point-separating family gives an open cover of `K_epsilon`; compactness gives a finite subcover; the finite-panel maximum separation is a positive continuous function on a compact set, so it has a positive minimum.

**Status:** PROVED. This is standard compactness/continuity mathematics, not a novelty claim. It is nevertheless directly useful for the finite-resolution experimental program.

### Surviving positive result B — rooted-tree safe regime for topology-aware greedy design

For a finite rooted tree of candidate worlds with truth at the root, suppose each experiment deletes a fixed set of vertices not containing the truth. For any selected experiment set `Q`, define

`f(Q) = |V| - |C_Q(root)|`.

On a tree, deleting a vertex disconnects exactly its descendant subtree from the root. Therefore `f(Q)` is exactly the cardinality of the union of descendant sets cut by the selected experiments. It is a **coverage function**, hence monotone submodular.

Consequently, under a cardinality budget, ordinary greedy obtains the classical `(1 - 1/e)` approximation guarantee.

**Status:** PROVED for the stated deterministic rooted-tree deletion model. This does **not** imply adaptive submodularity for experiments with unknown stochastic outcomes; that requires separate assumptions on outcome-conditioned utilities and posteriors.

### Surviving negative result — connected-ambiguity greedy can be arbitrarily bad

The independent `n x n` grid construction reproduces exactly:

- `n=10`: greedy/optimal `0.30`
- `n=20`: `0.15`
- `n=40`: `0.075`
- `n=80`: `0.0375`
- `n=160`: `0.01875`

with ratio exactly `3/n -> 0`, while also satisfying an explicit increasing-marginal inequality. Thus no constant-factor guarantee exists for the connected-component objective without additional structure.

**Status:** REPRODUCED and algebraically verified.

---

# 1. Monotone refinement of connected causal ambiguity

For a panel `Q`, target `w*`, and product/sup experiment metric,

`D_Q(w,w*) = max_{q in Q} rho_q(f_q(w), f_q(w*))`,

`K_Q^delta(w*) = {w : D_Q(w,w*) <= delta}`,

and `C_Q^delta(w*)` is the connected component of `K_Q^delta(w*)` containing `w*`.

## Theorem 1 — exact refinement

If `Q subset Q'`, then

`K_Q'^delta(w*) subset K_Q^delta(w*)`

and therefore

`C_Q'^delta(w*) subset C_Q^delta(w*)`.

The proof is immediate from monotonicity of the maximum under coordinate addition and maximality of the target component.

### Finite executable audit

On the preserved 128-world x 16-context source bundle, I reconstructed all 16 context-conditioned phenotype vectors. On the declared source-world graph proxy, I exhaustively enumerated all `2^16 = 65,536` experiment subsets for a nontrivial stress case and checked every one-experiment extension edge in the subset lattice. Number of component-inclusion violations: **0**.

**Status:** theorem verified; finite implementation audit PASS.

### Frozen rejection

Do not state refinement for normalized RMS/mean distances or any panel score whose value can decrease when a new experiment coordinate is added. The theorem belongs to monotone aggregators, especially max/sup.

---

# 2. Bounded signature error and component stability

Suppose every estimated experiment signature has uniform error at most `eta`:

`rho_q(f_q(w), ftilde_q(w)) <= eta`

for every `q,w`. Then target-relative pair distances satisfy

`|D_Q(w,w*) - Dtilde_Q(w,w*)| <= 2 eta`.

Hence

`K_Q^(delta-2eta) subset Ktilde_Q^delta subset K_Q^(delta+2eta)`

and, taking the component containing the target,

`C_Q^(delta-2eta) subset Ctilde_Q^delta subset C_Q^(delta+2eta)`.

## Stronger threshold statement

On a finite graph, define the component-entry / bottleneck threshold

`lambda_Q(v) = min_{paths w* -> v} max_{u on path} D_Q(u,w*)`.

Then

`v in C_Q^delta(w*)  iff  lambda_Q(v) <= delta`.

If `||D_Q - Dtilde_Q||_infinity <= kappa`, then every path bottleneck changes by at most `kappa`, so

`||lambda_Q - lambdatilde_Q||_infinity <= kappa`.

This gives a direct finite analogue of persistence/interleaving stability: **merge thresholds are stable even when a fixed-threshold component can jump discontinuously**.

### Executable source-bundle audit

With uniform coordinate perturbations `eta = 1e-5` on all saved source response vectors:

- observed maximum target-relative metric error: `1.9005903935109814e-05`
- theoretical bound `2 eta`: `2e-05`
- component-sandwich checks: PASS
- maximum bottleneck/merge-threshold error: `1.9005903935109814e-05 <= 2e-05`

**Status:** theorem verified; numerical stress test PASS.

### Frozen rejection

“Small measurement noise implies a small setwise change in the component at the same fixed delta” remains false. A tiny perturbation near a bottleneck can split/merge a large component. The stable object is the threshold-indexed family / merge thresholds, not necessarily a single threshold slice.

---

# 3. Finite separating perturbation conditions

The previous checkpoint mixed three different regimes. They should remain separate.

## 3.1 Exact separation on an infinite compact world space

Point separation by an infinite continuous family does **not** imply one finite exact separating subfamily.

Counterexample: the Hilbert cube `X=[0,1]^N`, with coordinate projections. The full countable family separates points, but any finite subfamily ignores infinitely many coordinates.

**Frozen rejection:** compactness alone does not give a finite exact separator for all `x != y`.

## 3.2 Positive-resolution separation on compact spaces

The compactness theorem in the executive verdict does hold for every `epsilon > 0` and even produces a uniform observation margin `gamma_epsilon > 0`.

This is the correct bridge from infinite point-separating experiment families to practical finite-resolution tomography.

## 3.3 Smooth finite-dimensional generic separation

For a compact smooth behavioral quotient `X` of dimension `d`, perturbations `u in U`, and an `r`-dimensional response `f(u,x)`, let an `m`-experiment tuple produce `F_u : X -> R^(mr)`. Under the collision-transversality hypothesis on

`Psi(u,x,x') = F_u(x) - F_u(x')`

for `x != x'`, generic tuples are injective when `mr > 2d`.

This remains a standard parametric-transversality / Whitney-style corollary, **not new mathematics**. The biologically nontrivial issue is whether the admissible perturbation family is rich enough for the transversality assumption.

## 3.4 Finite candidate library = Test Cover / set cover on far pairs

For finite `W`, structural threshold `epsilon`, and observation threshold `delta`, define the universe of relevant pairs

`U_epsilon = {{i,j}: d_W(w_i,w_j) > epsilon}`.

Experiment `q` covers a pair when its response distance exceeds `delta`. A panel is identifying at `(epsilon,delta)` iff its cover sets cover `U_epsilon`. The minimum panel problem is therefore ordinary Test Cover/set cover on far pairs.

This yields classical logarithmic set-cover guarantees for greedy exact coverage and `(1-1/e)` guarantees for budgeted pair coverage. These guarantees do **not** transfer automatically to connected-component reduction.

---

# 4. Counterfactual embedding-dimension lower bounds

## Continuous exact embeddings

If a continuous exact counterfactual signature maps a behavioral quotient `X` into `R^(mr)`, then

`mr >= e(X)`,

where `e(X)` is the minimum Euclidean embedding dimension of `X`.

Hence `mr >= dim_top(X)` at minimum. For a compact `d`-manifold without boundary, embedding into `R^d` is impossible by invariance-of-domain/compactness, so `e(X) >= d+1`; topology can force a larger value.

Under rich generic smooth measurements, `mr > 2d` is a sufficient regime, not a necessary one.

## Finite libraries: exact dimension is the wrong quantity

For finitely many distinct response vectors, almost every arbitrary scalar linear projection is injective. Therefore a statement such as “the finite library requires `k` Euclidean coordinates” is meaningless unless the admissible measurement family and/or a robustness margin is constrained.

The right finite quantities are instead:

- minimum admissible experiments needed to cover all scientifically far pairs;
- resolution floor under a fixed observation tolerance;
- packing/information lower bounds under a required separation margin.

For `P` signatures in `[-R,R]^(mr)` separated by at least `Delta` in `l_infinity`, the counting/packing obstruction is

`P <= (1 + 2R/Delta)^(mr)`.

---

# 5. Source-bundle finite separation results

The saved prospective source bundle contains 8 laws x 16 binary states = **128 worlds**, with **16 intervention contexts** and 34 stored phenotype coordinates per context.

For a world `(law,state)` and relative intervention mask `q`, the source construction gives the phenotype corresponding to `(law, state xor q)`. This lets the complete 128 x 16 finite response matrix be reconstructed from the preserved source files without inventing missing Source640 data.

## Exact finite separation

Across all `8128` unordered world pairs:

- minimum exact panel size: **2**
- one exact panel: `0000 + 0111`
- exact two-context panels: **40 total**
- Hamming-distance 3 pairs: **32**
- Hamming-distance 4 pairs: **8**
- Hamming distance 0,1,2: **0** exact two-context separators

This exactly matches the restricted algebraic theorem that two masks are globally sufficient when their relative Hamming distance is at least `n-1=3` in the four-channel fixed-budget model.

The best exact two-panel **uniform phenotype-coordinate margin** over all world pairs is approximately

`3.1948089599609375e-05`.

The worst margin among exact sufficient two-panels is approximately `2.765655517578125e-05`.

These numbers are properties of the saved source renders and coordinate metric, not universal constants.

## Resolution/tolerance transition

Exhaustive all-pair Test-Cover results:

| phenotype tolerance `delta` | minimum exact all-pair panel | full-panel unresolved pairs | latent L2 resolution floor |
|---:|---:|---:|---:|
| 0 | 2 | 0 | 0 |
| 1e-5 | 2 | 0 | 0 |
| 2.5e-5 | 2 | 0 | 0 |
| 3e-5 | 2 | 0 | 0 |
| 3.2e-5 | 4 | 0 | 0 |
| 1e-4 | impossible | 8 | 0.002 |
| 1e-3 | impossible | 56 | 0.0141421 |
| 1e-2 | impossible | 88 | 0.2 |

Thus the algebraic exact-identifiability statement and the finite-precision source-render statement are importantly different. At `delta=3.2e-5`, exact pair separation still exists but needs four contexts. By `delta=1e-4`, even all 16 saved contexts leave eight pairs unresolved.

---

# 6. Greedy connected-ambiguity counterexample

Let `G` be an even `n x n` grid and truth lie on the left. Let `q1` and `q2` delete complementary alternating cells of the middle column. Each alone leaves passages and has utility `n/2`; together they form a full wall and produce utility `n^2/2`. Let decoy `q0` delete the far-right boundary column, giving one-step utility `n`.

Greedy therefore picks `q0` first, then one of `q1,q2`, yielding `3n/2`, while optimum picks `q1,q2`, yielding `n^2/2`.

The ratio is exactly

`(3n/2)/(n^2/2) = 3/n -> 0`.

This simultaneously gives a direct submodularity violation because the marginal value of `q2` is much larger after `q1` than at the empty set.

**Status:** independently executable and reproduced through `n=160`.

---

# 7. A safe greedy regime, and what is still unproved

## Theorem 7 — rooted-tree coverage equivalence

Let candidate worlds form a rooted tree `T=(V,E)` with truth `r`. Each experiment `q` deterministically removes a vertex set `D_q` with `r notin D_q`. Let

`A_q = union_{v in D_q} Desc(v)`

be the union of descendant subtrees rooted at deleted vertices.

Then for every selected panel `Q`,

`V \ C_Q(r) = union_{q in Q} A_q`.

Therefore

`f(Q) = |union_{q in Q} A_q|`.

So `f` is a monotone coverage function and hence submodular.

### Executable stress test

Forty random rooted-tree instances were generated with seven random deletion experiments each. For every instance:

- exact equality between connected-component reduction and descendant coverage was exhaustively checked for all experiment subsets;
- exhaustive submodularity violations: **0**;
- cardinality-budget-3 greedy was compared to exact optimum;
- minimum observed greedy/optimal ratio: **0.933333...**, above the theorem’s general `1-1/e` floor.

The observed ratio is only a test statistic; the guarantee comes from the coverage proof.

## What this does not prove

Tree topology is **not** by itself enough for adaptive submodularity when experiment outcomes are unknown. Adaptive-submodular guarantees require a distribution over realizations plus a diminishing-conditional-expected-benefit property. No such property has been proved here for developmental perturbations.

---

# 8. Source-derived connected-component stress test

Using the declared law-MST x state-4-cube topology proxy, truth `P06/0000`, and phenotype tolerance `delta=0.05`, I exhaustively evaluated all `65,536` experiment subsets.

A genuine submodularity violation appears:

- base panel: `{0011}`
- candidate experiment: `0000`
- conditioning experiment: `0010`
- marginal gain of `0000` before conditioning: **9** vertices
- marginal gain after adding `0010`: **19** vertices
- increasing-marginal gap: **10**

So complementarity is not merely a synthetic grid pathology; it can arise in a finite graph built from the saved source-world data.

However, for this particular stress case greedy still reaches the exact optimum for budgets 1 through 5. Therefore the correct statement is:

> The source-derived proxy utility is non-submodular, but this finite instance does not exhibit a greedy performance loss at the tested budgets.

Do not convert “non-submodular” into “greedy failed here.”

---

# 9. Relation to established mathematics — novelty boundary

| Project object/claim | Closest established precedent | Verdict |
|---|---|---|
| Connected components of exact inverse fibers | Reeb spaces / Stein factorization | Established; not ours |
| Components of inverse images of finite neighborhoods | Reeb-space approximations, Mapper / Joint Contour style neighborhood constructions | Strong precedent |
| Joint state + law `w=(theta,x)` | augmented-state observability and structural identifiability | Established |
| States indistinguishable under all allowed inputs | nonlinear observability / input-output behavioral equivalence | Established |
| Approximate finite-experiment similarity | not automatically bisimulation | Keep distinct |
| Full branching transition matching | bisimulation / approximate bisimulation | Established, stronger condition |
| Histories grouped by identical predictive futures | causal states / computational mechanics | Established |
| Controlled predictive state from action-conditioned tests | Predictive State Representations (PSRs) | Established, very close |
| Input-output causal-state construction | epsilon-transducers / input-output computational mechanics | Established |
| Greedy set/pair coverage | set cover / maximum coverage | Established guarantees |
| Greedy with stochastic sequential observations | adaptive submodularity, when hypotheses hold | Established conditional guarantees |
| Generic finite-dimensional separation | Whitney/Takens/parametric transversality family of arguments | Established |

Important conceptual distinction:

- **trace/predictive equivalence** says future observable laws match under allowed interventions;
- **bisimulation** additionally constrains matching transition/branching structure;
- **finite connected ambiguity components** are inverse-problem objects around a target under a chosen experiment panel and tolerance.

They should not be used as synonyms.

---

# 10. Developmental state completion and PSR/causal-state precedent

For history `h` and future policy `pi`, define

`K_h^pi = P(future observations | h, do(pi))`.

Define

`h ~_Pi h' iff K_h^pi = K_h'^pi for all pi in Pi`.

The quotient by `~_Pi` is the coarsest interventional predictive state for the chosen future family. A measured present state `S=s(H)` is complete exactly when its value determines that quotient.

This is a predictive-sufficiency statement. It is tightly precedented by causal states, controlled predictive-state representations, and input-output computational mechanics.

**Frozen novelty rejection:** “present biological state screens off older history” is not a new mathematical definition of state.

**Still scientifically live:** whether a biologically measurable instantaneous developmental representation approximates the minimal interventionally predictive quotient for a meaningful developmental task family.

---

# 11. Frozen conjectures / rejected overclaims

The following are frozen as false or unsupported unless assumptions are explicitly changed:

1. **Adding experiments always shrinks ambiguity under any score.** False; needs a monotone panel metric.
2. **Fixed-delta connected components are setwise stable under small signature noise.** False; only threshold interleaving / merge-threshold stability is guaranteed.
3. **Compactness gives a finite exact separator from any point-separating infinite family.** False. Correct only at fixed positive resolution, or with stronger finite-dimensional/richness assumptions.
4. **Finite candidate libraries have a meaningful exact Euclidean embedding dimension under arbitrary real projections.** False/trivialized by generic scalar projection.
5. **Connected ambiguity reduction is generally submodular.** False; grid counterexample and source-proxy violation.
6. **Greedy connected-ambiguity design is generally near-optimal.** False; ratio can tend to zero.
7. **Tree topology alone gives adaptive-submodular sequential design.** Not proved; deterministic tree coverage gives ordinary submodularity only.
8. **Finite-resolution connected fibers are approximate bisimulation classes.** False without transition-compatibility conditions.
9. **Joint hidden-state/parameter inference is a new observability concept.** False; augmented-state identifiability precedent.
10. **Predictive screening-off / finite action-conditioned prediction vectors are unprecedented state ideas.** False; causal states, PSRs, epsilon-transducers.

---

# 12. What is strongest now

The strongest mathematically defensible formulation is narrower than the original rhetoric:

> For a monotone experiment metric, adding perturbations monotonically refines the connected ambiguity around a target world. Under bounded signature error, the entire threshold-indexed component family is interleaved, with finite-graph merge thresholds moving by at most the metric error. At any fixed positive hidden-world resolution, a continuous point-separating experiment family on a compact world space admits a finite uniformly separating panel. Yet topology-sensitive component reduction is not generally submodular and greedy can be arbitrarily bad; greedy regains classical guarantees only under additional structure such as the rooted-tree coverage regime.

None of the surrounding mathematical ingredients — Reeb constructions, observability/identifiability, causal states, PSRs, bisimulation, set cover, submodular or adaptive-submodular design — should be claimed as invented here.

The live project contribution remains a **biological/computational synthesis and empirical question**, not a new branch of pure mathematics.

---

# 13. Reproduction

From repository root:

`python lab_lanes/math/m1_math_verification.py`

Expected terminal sentinel:

`M1 verification PASS`

The script writes `lab_lanes/math/m1_results.json` and asserts all theorem-level finite invariants used in this checkpoint.
