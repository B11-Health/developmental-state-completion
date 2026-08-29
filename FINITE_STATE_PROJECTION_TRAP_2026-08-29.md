# Finite-state projection trap — why exact 1-D separation is not a biological dimension result

Date: 2026-08-29

## Proposition

Let `S = {x_1, ..., x_N}` be a finite set of distinct vectors in `R^p`, with `N >= 2`. For a projection vector `v in R^p`, define the scalar observable

`f_v(x) = v^T x`.

Then for Lebesgue-almost-every `v`, `f_v` is injective on `S`.

### Proof

For a fixed pair `i != j`, a collision occurs exactly when

`v^T x_i = v^T x_j`,

or equivalently

`v^T (x_i - x_j) = 0`.

Because `x_i != x_j`, this condition defines a proper hyperplane in `R^p`, which has Lebesgue measure zero. There are only finitely many pairs, so the union of all collision hyperplanes also has measure zero. Every `v` outside that finite union assigns a distinct scalar value to every element of `S`. QED.

## Consequence

For a **finite** candidate-state library, exact injective scalar coding does not imply that the underlying biological state is one-dimensional. If arbitrary real-valued linear observables are allowed and no robustness constraint is imposed, one scalar is generically enough to label every finite state exactly.

Therefore an exact finite-set “embedding dimension” is scientifically weak unless at least one of the following is specified:

1. a restricted admissible measurement family;
2. continuity/topology on a non-finite world space;
3. bounded measurement norm or cost;
4. a minimum separation margin relative to noise;
5. transfer to unseen states/worlds;
6. a decoder restriction or task loss.

## Robust replacement

For a normalized scalar projection `||v||=1`, define its finite-state separation margin

`gamma(v;S) = min_{i != j} |v^T(x_i - x_j)|`.

A robust one-dimensional code requires `gamma` to exceed the effective measurement/noise scale. More generally, for an admissible measurement family `A`, a useful robust embedding quantity should minimize the number of measurement coordinates subject to a required pair-separation margin.

One possible working definition is

`cedim_{epsilon,gamma,A}(W) = min |Q|`

such that every pair of worlds farther than `epsilon` in the scientific world metric is separated by at least `gamma` in the experiment-signature metric using experiments `Q subset A`.

For a finite library this becomes the already-identified far-pair Test-Cover problem. For a continuous world space, topological/embedding constraints re-enter and the scalar finite-set shortcut disappears.

## FM1 late-L1 example

The direct-source FM1 late-L1 cohort contains only **8 distinct 25-channel atlas-expression patterns** across 256 cells.

- Full-data PC1 is injective on all 8 patterns.
- PC1 explains about **58.2%** of atlas-expression variance.
- Its minimum raw inter-state scalar separation is about **0.01567**.
- 30/30 target-independent Gaussian random 1-D projections tested were also injective on all 8 states, as the proposition predicts.

Thus exact scalar separability of these eight states is not special.

### What is special about PC1?

PC1 is more useful for the future-growth task than a typical random scalar code:

- ExtraTrees, fixed grouped split: PC1 R2 about **0.633**; median of 30 random scalar projections about **0.600**.
- HistGradientBoosting: PC1 R2 about **0.664**; median random projection about **0.630**.
- Only roughly 17–20% of the tested random projections matched or exceeded PC1 under those decoders.

However, PC1 is **not unusually robust as a code**:

- among 10,000 random unit projections, its raw minimum separation margin is near the **50th percentile**;
- after standardizing by code spread, its margin is only around the **14th percentile**.

Its ordering of the eight states is somewhat better aligned with their mean future growth (absolute state-level Spearman about `0.643`, roughly the 74th percentile of random projections). Across the 30 random ExtraTrees codes, predictive R2 correlates more with target-order alignment than with minimum separation margin.

## Frozen correction

### Rejected

> “A one-dimensional projection that separates all finite observed states establishes a one-dimensional developmental state.”

False.

### Surviving interpretation

> A compact scalar representation may be highly useful for a specified prediction task, but its scientific meaning must be judged by robustness, admissible measurement constraints, transfer beyond the finite training-state library, and performance under a pre-specified decoder—not by exact finite-state injectivity alone.

## Relevance to counterfactual developmental tomography

This sharpens the program's use of “counterfactual embedding dimension.” The quantity of interest cannot be bare Euclidean dimension on a finite simulator library. It must be **robust and interface-constrained**: how many biologically admissible measurements/perturbations are required to separate scientifically distinct worlds by a margin large enough to survive noise and transfer to new states?
