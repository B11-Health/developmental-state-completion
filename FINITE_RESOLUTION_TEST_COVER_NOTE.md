# Finite-resolution reconstruction as test cover

Date: 2026-08-29

## Novelty boundary

The finite candidate-world problem below is **not a new combinatorial problem**. For binary tests and exact pairwise distinction it is the classical **Minimum Test Collection / separating-system** problem. The value for this project is the mapping between that established mathematics and finite-resolution developmental experiment design, and the contrast with connected-component ambiguity objectives where classical coverage guarantees can fail.

Classical references include Rényi-style separating systems and Halldórsson, Halldórsson & Ravi (2001), *On the Approximability of the Minimum Test Collection Problem*, DOI `10.1007/3-540-44676-1_13`.

## 1. Finite developmental world library

Let `W={w_1,...,w_N}` be a finite set of candidate state-law worlds with structural metric `d_W`. Let `Q_full` be a finite library of admissible experiments. Experiment `q` returns phenotype/response `h_q(w)` in metric space `(Y_q,d_q)`.

For a panel `Q subset Q_full`, define the panel discrepancy

`D_Q(w_i,w_j) = max_{q in Q} d_q(h_q(w_i),h_q(w_j))`.

Fix:

- hidden-world resolution `epsilon >= 0`;
- phenotype distinguishability threshold `delta >= 0`.

A panel is **(epsilon,delta)-identifying** when

`D_Q(w_i,w_j) <= delta  =>  d_W(w_i,w_j) <= epsilon`

for every pair. Equivalently, every pair farther than `epsilon` in hidden-world space is separated by at least one chosen experiment by more than `delta`.

Define

`kappa(epsilon,delta) = min{|Q| : Q is (epsilon,delta)-identifying}`,

with `kappa=infinity` if no subpanel of the admissible library can satisfy the requirement.

## 2. Exact reduction to pair cover

Define the universe of structurally relevant pairs

`U_epsilon = {{i,j}: i<j and d_W(w_i,w_j) > epsilon}`.

Each experiment covers the pairs it separates:

`S_q(epsilon,delta) = {{i,j} in U_epsilon : d_q(h_q(w_i),h_q(w_j)) > delta}`.

### Proposition 1 — Test-cover equivalence

A panel `Q` is `(epsilon,delta)`-identifying if and only if

`union_{q in Q} S_q(epsilon,delta) = U_epsilon`.

Therefore `kappa(epsilon,delta)` is exactly the minimum set cover of the far-pair universe by experiment-separation sets. For binary experiments at `epsilon=delta=0`, this is the classical Minimum Test Collection problem.

### Consequences

1. Exact finite-world panel selection is combinatorial even when the underlying biology is continuous.
2. Exhaustive search or integer programming is appropriate for small experiment libraries.
3. Greedy pair separation inherits classical set-cover guarantees; this guarantee does **not** transfer automatically to connected-component ambiguity destruction.

## 3. Greedy guarantees for pairwise separation

Let `M=|U_epsilon|`. The standard greedy algorithm repeatedly chooses the experiment covering the largest number (or total weight) of currently uncovered far pairs.

For minimum exact coverage, generic set-cover analysis gives an approximation factor at most `H_M <= 1+ln M`; because `M <= N(N-1)/2`, this is at most approximately `1+2 ln N`. This is consistent with the classical Minimum Test Collection approximation literature.

For a fixed budget `B`, define pair-coverage utility

`F(Q)=| union_{q in Q} S_q |`

(or a nonnegative weighted version). This is a monotone submodular coverage function. Classical greedy therefore achieves at least `1-(1-1/B)^B >= 1-1/e` of the optimal budget-`B` pair coverage.

### Critical distinction

Our already-published connected-ambiguity objective is different. It scores how a panel changes the **connected component containing a target world**, not merely how many world pairs receive distinct signatures. The repository contains a separate counterexample in which greedy connected-component splitting has approximation ratio `3/n -> 0`.

Thus:

> Pairwise separation has classical coverage structure; connected causal-fiber destruction can lose that structure completely.

This distinction should replace any blanket statement that “greedy tomography” is good or bad. The answer depends on the objective.

## 4. Irreducible resolution floor

For the full experiment library, define

`epsilon_floor(delta) = max{ d_W(w_i,w_j) : D_Qfull(w_i,w_j) <= delta }`,

with maximum zero if no distinct pair remains compatible.

### Proposition 2 — Impossibility below the full-panel floor

If `epsilon < epsilon_floor(delta)`, then

`kappa(epsilon,delta)=infinity`.

Proof: a pair exists with structural distance greater than `epsilon` but full-panel discrepancy at most `delta`. Every subpanel has discrepancy no larger than the full panel, so no subpanel can separate that pair.

For a **finite** experiment library, if `epsilon >= epsilon_floor(delta)`, the full panel is `(epsilon,delta)`-identifying and hence `kappa <= |Q_full|`.

### Monotonicity

For the finite library:

- `epsilon_floor(delta)` is nondecreasing in `delta`;
- `kappa(epsilon,delta)` is nonincreasing in `epsilon`;
- `kappa(epsilon,delta)` is nondecreasing in `delta`.

These are exact finite-library statements.

## 5. Robust separation under measurement/model error

Assume each response is perturbed by at most `eta` in its experiment metric:

`d_q(h_q(w), htilde_q(w)) <= eta`.

Then for every pair, triangle inequality gives

`| d_q(htilde_q(w_i),htilde_q(w_j)) - d_q(h_q(w_i),h_q(w_j)) | <= 2 eta`.

Therefore:

- true separation `> delta + 2 eta` guarantees observed separation `> delta`;
- true separation `< delta - 2 eta` guarantees observed nonseparation `< delta`;
- only the `4 eta` gray band around the threshold is intrinsically unstable under this bound.

A robust test-cover instance should therefore cover far pairs using a margin, not tests that barely cross `delta`.

## 6. Information/packing lower bounds

### Discrete-outcome bound

If a set of `P` candidate worlds is pairwise farther than `epsilon` and every selected experiment has at most `K` possible outcomes, unique signatures require

`K^m >= P`,

so

`m >= ceil(log(P)/log(K))`.

For binary tests this is `m >= ceil(log2 P)`. Restricted experiment libraries can require many more tests.

### Bounded continuous-response packing bound

Suppose each experiment contributes `r` real coordinates, the total signature lies in `[-R,R]^(mr)`, and every pair in a `P`-world structural packing must be separated by at least `Delta` in `l_infinity` signature distance. Disjoint `l_infinity` balls of radius `Delta/2` imply

`P <= (1 + 2R/Delta)^(mr)`.

Thus

`mr >= log(P) / log(1+2R/Delta)`

and

`m >= ceil( log(P) / (r log(1+2R/Delta)) )`.

This is only a geometric sanity bound; it does not account for restrictions on which signatures biological experiments can realize.

## 7. Random-panel upper bound

Suppose experiments are sampled independently from a distribution over the admissible library and every far pair is separated with probability at least `p>0`. Let `M=|U_epsilon|`. Then after `m` independent experiments,

`Pr(any far pair remains unseparated) <= M (1-p)^m <= M exp(-pm)`.

Therefore it is sufficient to take

`m >= log(M/beta)/p`

to obtain complete pairwise separation with probability at least `1-beta`.

This is a simple union-bound guarantee, not a claim that realistic perturbation libraries have favorable `p`. Estimating the worst-pair separation probability is itself an experimental-design problem.

## 8. Archived Source640 phase results

The recovered simulator checkpoint reported the following **finite-sample Source640** phase behavior:

- `delta=.001`: `epsilon<=.25` impossible; `epsilon=.5 -> kappa=2`; `epsilon=1 -> kappa=1`.
- `delta=.00155`: `epsilon<=.25` impossible; `epsilon=.5 -> kappa=2`; `epsilon=1 -> kappa=1`.
- `delta=.0028`: `epsilon<=.75` impossible; `epsilon=1 -> kappa=3`.
- `delta=.0035`: `epsilon<=1` impossible; `epsilon≈1.25–1.5 -> sampled kappa around 3`.

These numbers have **not yet been independently rerun from a migrated Source640 response matrix in this public checkout**. They remain archived finite-sample findings, not theorem statements.

The same checkpoint reported an operational resolution-floor approximation dominated by the weak NORMAL state-flip channel, with model-specific singleton salience slopes approximately:

- C: `0.00647034`;
- S: `0.02257782`;
- F: `0.00931728`;
- N: `0.00554426`.

It proposed `epsilon_floor(delta) ~ (2/c_N) delta ~ 360.7 delta` in that restricted executor while NORMAL aliases dominate. This scaling is model-specific and must not be presented as universal biology.

## 9. What remains scientifically distinctive

The combinatorics are established. The candidate scientific contribution is the **coupling** of three different ambiguity objects:

1. global finite-resolution identification `kappa(epsilon,delta)` — a test-cover problem with classical pair-coverage guarantees;
2. target-local path blocking `kappa_nav` — a labeled-cut / hypergraph-transversal problem;
3. connected causal-fiber contraction — a topology-sensitive objective where greedy can be arbitrarily bad.

A developmental experiment can be easy under one objective and hard under another. Making that objective dependence explicit, then testing which objective predicts experimental efficiency in a living system, is the nontrivial research program.
