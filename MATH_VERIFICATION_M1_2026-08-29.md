# M1 Mathematics Verification Checkpoint — Robust Finite Resolution and Greedy Regimes

Date: 2026-08-29

Status: theorem/counterexample checkpoint plus finite computational audits. Classical mathematical ingredients are identified as precedent; simulator-specific statements are labeled computational evidence.

## 1. Monotone experimental refinement

Let `W` be a topological world space, `w* in W`, and each experiment `q` produce an observation `h_q(w)` in a metric space. For a finite panel `Q`, use the monotone product/sup discrepancy

`D_Q(w,w*) = max_{q in Q} d_q(h_q(w), h_q(w*))`.

Define

`K_Q^delta(w*) = {w : D_Q(w,w*) <= delta}`

and let `C_Q^delta(w*)` be the connected component of `K_Q^delta(w*)` containing `w*`.

### Theorem 1 — nested-panel refinement

If `Q subset Q'`, then

`K_Q'^delta(w*) subset K_Q^delta(w*)`

and therefore

`C_Q'^delta(w*) subset C_Q^delta(w*)`.

**Proof.** Adding coordinates to a maximum cannot decrease `D_Q`. Set inclusion follows. If `A subset B` and both contain `w*`, every connected subset of `A` containing `w*` is also a connected subset of `B`, so the target component is nested. QED.

This exact monotonicity is a property of the declared experiment metric. It is not guaranteed for arbitrary learned scores or non-monotone aggregations.

The M1 finite source-bundle audit found zero nested-panel monotonicity violations under the declared max-distance metric/topology proxy.

## 2. Bounded signature error gives a component sandwich

Suppose estimated target-relative panel discrepancies satisfy

`|Dtilde_Q(w,w*) - D_Q(w,w*)| <= kappa`

uniformly in `w`. Then for `delta >= kappa`,

`K_Q^(delta-kappa) subset Ktilde_Q^delta subset K_Q^(delta+kappa)`.

By Theorem 1's component argument,

`C_Q^(delta-kappa)(w*) subset Ctilde_Q^delta(w*) subset C_Q^(delta+kappa)(w*)`.

If each individual world response is perturbed by at most `eta` in the observation metric, a triangle inequality gives the common pairwise bound `kappa <= 2 eta`.

### What this does not say

Fixed-`delta` components need not vary Lipschitz-continuously as sets. A tiny distance perturbation can cross a merge saddle and cause a large component jump. The defensible statement is the **threshold sandwich**, not fixed-threshold set stability.

In the preserved source-derived 128-world audit, injected signature error `eta=1e-5` produced maximum target-relative distance error `1.90059e-5 <= 2e-5` and maximum sampled merge-threshold shift `1.90059e-5 <= 2e-5`.

## 3. Finite robust separation at any fixed positive world resolution

Bare exact finite separation of an infinite world space can fail even when the complete experiment family separates every pair. At a fixed scientifically meaningful world resolution, compactness changes the result.

### Theorem 2 — compact fixed-resolution finite panel

Let `(X,rho)` be a compact metric space. Let `{h_q : X -> Y_q}_{q in A}` be a family of continuous experiment maps into metric spaces. Assume the family is point-separating: for every `x != y`, some `q` satisfies

`d_q(h_q(x),h_q(y)) > 0`.

Then for every `epsilon > 0`, there exists a finite panel `Q_epsilon subset A` and a margin `gamma_epsilon > 0` such that

`rho(x,y) >= epsilon  =>  max_{q in Q_epsilon} d_q(h_q(x),h_q(y)) >= gamma_epsilon`.

### Proof

Consider the compact set

`P_epsilon = {(x,y) in X x X : rho(x,y) >= epsilon}`.

For every pair `(x,y)` in `P_epsilon`, point separation gives an experiment `q` with positive response distance. By continuity, that same experiment remains positively separating on an open neighborhood of `(x,y)` in `P_epsilon`. These neighborhoods form an open cover of the compact set `P_epsilon`; choose a finite subcover, involving finitely many experiments `Q_epsilon`.

Define

`g(x,y) = max_{q in Q_epsilon} d_q(h_q(x),h_q(y))`.

`g` is continuous and strictly positive on compact `P_epsilon`, hence attains a positive minimum `gamma_epsilon`. QED.

### Sharpness / why `epsilon > 0` matters

Take the infinite binary product `{0,1}^N` with metric `rho(x,y)=sum_j 2^{-j}|x_j-y_j|` and coordinate experiments. The full family separates points, but any finite coordinate panel misses two sequences differing only in a later coordinate. Thus no finite panel gives exact separation of all distinct worlds. Yet for each positive `epsilon`, finitely many leading coordinates suffice because the remaining metric tail can be made smaller than `epsilon`.

M1's finite Hilbert-cube analogue reproduces this distinction computationally.

### Scientific consequence

For living experiments, the useful question is not “can a finite panel reconstruct every infinitesimal world distinction?” It is:

> At the task-relevant world resolution `epsilon` and required measurement margin `gamma`, how many biologically admissible experiments are needed?

This is the robust/interface-constrained version of the working counterfactual embedding-dimension idea.

## 4. Finite candidate libraries: robust panel size can jump with tolerance

The preserved source-derived bundle contains:

- 128 candidate worlds;
- 16 available contexts;
- 34 phenotype coordinates per context.

Under exact pair separation:

- minimum panel size = **2**;
- one exact minimum panel is `{0000, 0111}`;
- there are **40** sufficient two-context panels;
- all 40 use contexts at Hamming distance 3 or 4 (32 at distance 3, 8 at distance 4);
- the best two-panel uniform pair-separation margin is about **3.19481e-5**, achieved by `{0111,1010}`.

When a required observation tolerance is imposed, the minimum panel changes:

| Required separation `delta` | Minimum panel | Full-library unresolved pairs | latent-L2 resolution floor |
|---:|---:|---:|---:|
| 0 | 2 | 0 | 0 |
| 1e-5 | 2 | 0 | 0 |
| 2.5e-5 | 2 | 0 | 0 |
| 3.0e-5 | 2 | 0 | 0 |
| 3.2e-5 | 4 | 0 | 0 |
| 1e-4 | infeasible | 8 | 0.002 |
| 1e-3 | infeasible | 56 | 0.014142 |
| 1e-2 | infeasible | 88 | 0.2 |

These are finite source-bundle results, not universal biological constants. They demonstrate why robust resolution and measurement margin belong in the definition.

## 5. Connected-ambiguity utility is not generally submodular

For a finite candidate graph with truth root `w*`, let experiments delete candidates inconsistent with the observed truth response. Define utility

`f(Q) = |V| - |C_Q(w*)|`,

where `C_Q(w*)` is the surviving connected component containing truth.

The previously frozen grid construction gives, for an `n x n` grid and budget two,

`f(greedy)/f(optimal) = 3/n -> 0`.

M1 re-executed the construction for `n=10,20,40,80,160`, obtaining ratios

`0.30, 0.15, 0.075, 0.0375, 0.01875`,

exactly matching `3/n`.

Thus connected-component ambiguity destruction has **no general constant-factor greedy guarantee** without extra structure.

## 6. The source-derived bundle is genuinely non-submodular, even though greedy happens to work there

M1 built an explicitly declared finite topology proxy for the preserved 128-world source bundle: a minimum-spanning tree over law-gain vectors, Cartesian-linked to the 4-cube state graph.

At truth `(P06,0000)` and `delta=0.05`, the connected-ambiguity utility has a concrete diminishing-returns violation:

- marginal value of experiment `0000` before conditioning: **9** removed vertices;
- marginal value after adding `0010`: **19**;
- submodularity gap: **10**.

So non-submodularity is not merely an adversarial-grid artifact under this proxy.

However, exhaustive comparison for budgets 1–5 found greedy utility equal to the optimum in this particular source-derived stress case. Therefore two claims must remain separate:

1. the objective is not generally submodular;
2. greedy is not necessarily poor on every dataset.

## 7. A precise static regime where greedy is safe

### Theorem 3 — rooted-tree known-outcome coverage regime

Let the candidate ambiguity graph be a rooted tree with the true world at the root. For each experiment `q`, after observing the truth-consistent outcome, let `D_q` be the set of vertices directly removed by that experiment. Define `A_q` as the union of the descendant subtrees rooted at vertices in `D_q`.

Then the number (or nonnegative total weight) of vertices disconnected from truth after a set of experiments `Q` is

`f(Q) = weight( union_{q in Q} A_q )`.

Hence `f` is a monotone submodular coverage function. Under a cardinality budget, ordinary greedy achieves the classical `(1-1/e)` approximation guarantee.

### Proof

On a tree there is a unique path from every vertex to the root. A surviving vertex is disconnected from the root exactly when that unique path contains at least one directly deleted vertex. Equivalently, the vertex lies in the descendant closure of at least one selected experiment's deletion set. Thus disconnected vertices are exactly the union of the fixed sets `A_q`. Weighted union coverage is monotone submodular. The classical greedy guarantee follows. QED.

M1 tested 40 random rooted-tree instances with arbitrary experiment deletion sets; no submodularity violation occurred and the minimum observed greedy/optimal ratio at budget 3 was **0.9333**.

### Important boundary

This is a **static, known-outcome** theorem. Tree topology alone does not imply adaptive submodularity when experiment outcomes are unknown and depend on the hidden truth. Adaptive guarantees require additional probabilistic/outcome structure.

## 8. Relation to established mathematics

These pieces are not individually new:

- compactness + finite-subcover arguments are classical topology;
- Reeb/Stein-type quotient ideas are established;
- observability and structural identifiability already formalize state/parameter distinguishability;
- predictive-state representations and causal-state/transducer constructions already formalize intervention/action-conditional predictive state;
- finite pair separation maps to Test Collection / Set Cover;
- weighted coverage submodularity and the `1-1/e` greedy bound are classical.

The project-specific contribution, if it survives prospective biology, is the **combination and experimental interpretation**: joint hidden state-law ambiguity in developmental systems, connected approximate inverse fibers under a declared biological metric, and recursive selection of admissible perturbations to complete a measurable current state for a specified future task.

## 9. Frozen rejections from M1

Do not revive these without explicit new assumptions:

- arbitrary experiment-score aggregation preserves refinement;
- fixed-delta connected components are Lipschitz-stable as sets;
- compactness alone gives one finite exact separator for an infinite world space;
- finite-library exact Euclidean embedding dimension is informative under arbitrary real projections;
- connected-ambiguity utility is generally submodular;
- tree topology alone implies adaptive submodularity under unknown outcomes.

## 10. Reproduction

Local lane artifacts:

- `lab_lanes/math/m1_math_verification.py`
- `lab_lanes/math/m1_results.json`

Running the script currently prints `M1 verification PASS` and reproduces the numerical checks above.

## Surviving mathematical program

The next mathematics should focus on **robust, admissible-measurement experiment complexity** rather than bare dimension:

1. characterize `kappa(epsilon,gamma)` for realistic perturbation libraries;
2. bound its sensitivity to measurement noise/model mismatch;
3. identify graph/metric structures beyond rooted trees that make connected-ambiguity utility submodular or approximately submodular;
4. compare pairwise robust separation versus connected-fiber destruction on the same biological objective;
5. extend static guarantees to adaptive policies only under explicitly verified outcome models.
