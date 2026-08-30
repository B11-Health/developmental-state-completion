# M2 Optimization Theory & Exact Perturbation Design Checkpoint

Date: 2026-08-29  
Branch: `lab-m2-optimization-2026-08-29`  
Base: current `origin/main` at lane start, `b7265faaa22065be0207922dc5f172152ea53dc5`  
Status: executable finite audit + theorem/counterexample checkpoint. No publication, email, or push.

## Executive result

M2 does **not** find a new general greedy guarantee. It finds a much narrower and more useful boundary:

1. On the preserved 128-world source bundle, greedy happens to equal the exact optimum for every audited truth, tolerance, topology, and cardinality budget 1-5.
2. That empirical success coexists with concrete non-submodularity on the source topology and with the frozen `3/n -> 0` greedy counterexample on grids. Therefore dataset-level greedy success is not evidence of a universal approximation theorem.
3. A structural sufficient condition broader than rooted trees survives: arbitrary cycles are allowed if the family of vertices that experiments can directly delete is **block-sparse** -- at most one potentially deletable vertex occurs in each biconnected block. In that regime, truth-rooted disconnection again reduces exactly to fixed-set coverage.
4. The pair-separation objective is classical Test Cover / coverage. The connected-component objective is closer to critical-node / nodal-interdiction optimization, but with experiment-induced deletion sets and a distinguished truth root. Information gain is a third, distinct objective and should not be conflated with either.

## 1. Frozen source bundle and exact enumeration

The audit uses the committed `source_validation/two_context_2026-08-26` bundle:

- 128 worlds = 8 laws x 16 four-bit states;
- 16 candidate perturbation contexts;
- 34 phenotype coordinates per context;
- target-relative discrepancy = maximum absolute phenotype-coordinate difference, exactly as in M1.

Audited tolerances:

`0, 1e-5, 2.5e-5, 3e-5, 3.2e-5, 1e-4, 1e-3, 1e-2, 5e-2`.

Audited cardinality budgets: `k=1,2,3,4,5`.

For each `k`, the exact optimum enumerates **all** `C(16,k)` panels (16, 120, 560, 1820, 4368 respectively; 6884 nonempty candidate panels across k=1..5). The source construction is exactly XOR-equivariant in the four-bit state. Code computes the eight law-specific state-`0000` utility tables, then maps every other truth state by the exact permutation `q -> q xor state`; greedy is still run with the actual state-specific context labels/tie breaking. Thus all 128 truths are included, not sampled.

### Declared topology choices

M2 intentionally treats topology as a modeling assumption and reports three choices:

- `complete_survivor`: complete graph on all worlds, so the truth component is the full surviving version space. This is a pure coverage control.
- `law_mst_x_q4`: the M1 proxy -- Q4 within each law plus same-state links across the gain-vector law MST.
- `law_clique_x_q4`: a denser sensitivity graph -- Q4 within each law plus same-state links across every pair of laws.

### Exact-vs-greedy result

Across 128 truths x 9 tolerances x 3 topologies x 5 budgets = **17,280 rows**:

| topology | rows | greedy suboptimal rows | minimum greedy/optimal | maximum additive gap |
|---|---:|---:|---:|---:|
| complete survivor | 5,760 | 0 | 1.0 | 0 |
| law-MST x Q4 | 5,760 | 0 | 1.0 | 0 |
| law-clique x Q4 | 5,760 | 0 | 1.0 | 0 |

This is an **instance result**, not a theorem. It freezes the stronger empirical statement: within this exact bundle/budget/tolerance audit, the lexicographic greedy rule never loses to exact cardinality optimization.

## 2. Non-submodularity survives the broader audit

For static known-outcome utility

`f(Q) = |V| - |C_Q(w*)|`,

M2 checks diminishing returns exhaustively for all conditioning panels of size at most 3 and all two-context augmentations, matching total selected size at most 5.

### Complete-survivor control

No diminishing-returns violation occurs. This is expected: deleted worlds are the union of fixed per-experiment inconsistent-world sets, so the objective is coverage.

The standard total curvature evaluates to 1 throughout these bundle instances because, once almost the whole redundant 16-context library is present, an individual context can have zero final marginal value despite positive singleton value. This makes the curvature bound formally valid but practically uninformative here.

### M1 law-MST x Q4

Only 2 of the 72 canonical law/tolerance instances show a violation, both at `delta=0.05`, but the violation is real:

- strongest truth law: `P06`, canonical state `0000`;
- conditioning panel: `{0011}`;
- marginal of adding `0000`: 9;
- marginal of adding `0000` after also conditioning on `0010`: 19;
- diminishing-returns gap: **10**;
- restricted two-element submodularity-ratio diagnostic: **13/23 = 0.565217...**.

The ratio is explicitly **restricted** to conditioning size <=3 and two-element augmentations (total budget <=5). It is a finite diagnostic in the sense motivated by Das-Kempe, not a claimed global submodularity ratio for all set pairs.

### Denser law-clique x Q4

Again 2/72 canonical instances violate diminishing returns at `delta=0.05`. The largest gap falls to **3**, and the minimum restricted ratio rises to **15/17 = 0.882352...**. Thus adding redundant cross-law paths reduces, but does not eliminate, the complementarity created by connectivity cuts.

## 3. General counterexamples remain frozen

### Four-cycle: smallest clean synergy witness

Take cycle `0-1-2-3-0`, root at 0, and two experiments deleting vertices 1 and 3 respectively.

- `f(empty)=0`;
- `f({1})=1`;
- `f({3})=1`;
- `f({1,3})=3`.

The pair has positive synergy `3-1-1=1`, so even a single cycle is enough to destroy general submodularity.

### Arbitrarily bad greedy grid

M1's frozen n x n grid construction is re-executed unchanged. With budget two:

`f(greedy)/f(optimal)=3/n`.

For `n=10,20,40,80,160`, M2 again gets `0.30, 0.15, 0.075, 0.0375, 0.01875` exactly. Therefore no topology-free constant-factor guarantee for ordinary greedy is defensible.

## 4. New sufficient structural condition beyond rooted trees

### Theorem M2.1 -- block-sparse deletion coverage

Let `G=(V,E)` be a connected undirected graph with truth root `r`. Let `A subset V\{r}` be the set of vertices that can be directly deleted by at least one admissible experiment. Assume:

> Every biconnected block of `G` contains at most one vertex of `A`.

For an experiment `q`, let `D_q subset A` be its directly deleted vertices. Let

`L(a) = V \ C_{G-a}(r)`

be the vertices lost from the truth component when `a` alone is deleted. Then for every experiment panel `Q`,

`V \ C_{G - union_{q in Q} D_q}(r) = union_{q in Q} union_{a in D_q} L(a)`.

Consequently the weighted or unweighted disconnected-from-truth utility is a fixed-set coverage function and is monotone submodular. Under a cardinality budget, classical greedy has the usual `1-1/e` coverage guarantee.

### Proof sketch

Use the block-cut tree of `G`. A nontrivial biconnected block remains connected after removal of any single vertex. Because each block contains at most one potentially deletable vertex, a selected deletion set can never remove two different vertices from the same block and thereby create a genuinely cooperative cut inside that block. Any loss of reachability from `r` must therefore occur because a selected deletable articulation vertex on the unique root-to-block route in the block-cut tree is removed. That articulation alone already disconnects the downstream region. Hence every vertex lost under a multi-vertex deletion belongs to `L(a)` for at least one selected `a`; the reverse inclusion is monotonicity. Equality follows, giving union coverage.

This strictly generalizes the rooted-tree theorem: blocks may contain arbitrary cycles and dense 2-connected subgraphs, provided the admissible deletion family is sparse at block level.

### Executable witness

`m2_exact_optimization.py` includes a cyclic graph with two attached triangles and a block-sparse deletable set. All 8 subsets of the three deletable vertices match the fixed union-coverage prediction exactly.

### Boundary

The C4 counterexample violates the hypothesis because its one biconnected block contains both potentially deletable vertices. This is exactly the cooperative-cut mechanism the theorem excludes.

## 5. Objective comparison

### A. Robust pair separation = Test Cover / pair coverage

Threshold each experiment `q` into the world-pair set it distinguishes by more than `delta`. Maximizing distinguished pairs is ordinary maximum coverage; requiring all distinguishable pairs to be separated is Test Cover / Test Set. This objective ignores topology and a privileged truth root.

On the 128-world bundle there are 8,128 unordered pairs. Examples:

- `delta=0`: a two-context greedy panel already distinguishes all 8,128 pairs; exact optimum does too.
- `delta=3.2e-5`: budget 2 distinguishes 8,126 pairs; budget 4 reaches all 8,128.
- `delta=1e-4`: 8 pairs remain unresolved even with the full library, so no panel can cover them.
- `delta=0.05`: 224 pairs are intrinsically unresolved by the full library; budget 4 reaches the full feasible 7,904 distinguished pairs.

Greedy equals exact optimum for every audited pair-coverage budget/tolerance row, consistent with a highly redundant easy instance; this should not be generalized beyond the bundle.

### B. Connected truth-component reduction = response-induced critical-node/interdiction objective

Here the panel first induces a union of inconsistent worlds, then utility counts all vertices absent from the root component after those deletions. A single directly deleted world can disconnect many other surviving worlds. Conversely, two experiments can cooperate to form a cut even when neither does alone. This places the graph operation near critical-node and nodal-interdiction literature, but the decision variables are experiments with structured deletion sets rather than independently purchasable graph vertices.

The literature already contains hardness and special-structure algorithms for established critical-node/connectivity objectives, including bounded-treewidth and series-parallel cases. M2 therefore makes **no priority claim** for graph deletion optimization or tractability from graph structure.

### C. Uniform-prior exact-signature information gain

For comparison, M2 also maximizes Shannon entropy of the exact joint experiment signature under a uniform prior over the 128 worlds. One context yields `6.57016` bits; two contexts achieve the full `log2(128)=7` bits. Greedy equals exact optimum for budgets 1-5.

This objective answers a different question: how much uncertainty about the entire world identity is removed on average under a prior? It does not directly optimize the worst-case truth component or topology-aware ambiguity. An experiment can be excellent in entropy and poor for a particular truth/rooted connected fiber, or vice versa.

## 6. Literature / priority red-team

The machine-readable `literature_map.json` freezes the closest established categories and DOIs. The main precedents are:

- de Bontridder et al. (2003), Test Cover: pairwise item distinction by tests;
- Das & Kempe (2011), submodularity ratio as a weak-submodularity diagnostic;
- Golovin & Krause (2011), adaptive submodularity for uncertain sequential outcomes;
- Addis, Di Summa & Grosso (2013), critical-node deletion and bounded-treewidth algorithms;
- Shen & Smith (2012), critical-node objectives on trees and series-parallel graphs;
- Kennedy et al. (2011), direct nodal interdiction.

The defensible project-specific statement is narrow: **we are combining a response-induced experiment library with truth-rooted connected approximate inverse fibers and auditing exact perturbation design on the preserved developmental simulator/source bundle.** M2 does not establish priority for Test Cover, information gain, submodularity diagnostics, graph interdiction, critical-node objectives, or adaptive diagnosis.

## 7. Frozen false conjectures / claims not to revive

1. **False:** connected-component reduction is submodular on arbitrary undirected graphs. C4 already refutes it.
2. **False:** series-parallel, planar, bounded-treewidth, or low-cycle topology alone is enough for submodularity. C4 is planar, series-parallel, and treewidth 2.
3. **False:** strong greedy performance on the 128-world source bundle implies a constant-factor general guarantee. The grid ratio tends to zero.
4. **False:** denser topology restores submodularity in the source bundle. It reduces the worst observed gap but leaves violations.
5. **Unsupported:** the restricted finite-budget submodularity ratio is a global approximation certificate. It is reported only as a diagnostic.
6. **Unsupported:** static known-truth results imply adaptive-submodular guarantees under unknown outcomes. They do not.
7. **Unsupported priority:** the graph objective/counterexample is mathematically unprecedented. It sits inside established graph deletion/interdiction territory; no novelty claim is made absent a much deeper equivalence search.

## 8. Reproduction and artifacts

Run from the repository root or workspace:

`python lab_lanes/m2_optimization/m2_exact_optimization.py`

Artifacts:

- `m2_exact_optimization.py` -- executable source audit and synthetic theorem/counterexample checks;
- `m2_results.json` -- compact machine-readable summary, topology declarations, comparison objectives, synthetic witnesses;
- `exact_vs_greedy_all_truths.csv` -- all 17,280 exact-vs-greedy rows;
- `submodularity_diagnostics.json` -- 216 canonical topology/law/tolerance diagnostic records;
- `pair_coverage_exact_vs_greedy.csv` -- Test-Cover/maximum-coverage comparison;
- `exact_entropy_exact_vs_greedy.csv` -- exact-signature Shannon-information comparison;
- `literature_map.json` -- precedent/overlap/difference ledger;
- this checkpoint.

The script ends with `M2 exact optimization PASS` and rechecks the C4 and `3/n` counterexamples every run.
