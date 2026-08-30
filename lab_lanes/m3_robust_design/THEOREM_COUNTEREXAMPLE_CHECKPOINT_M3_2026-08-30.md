# M3 theorem / counterexample checkpoint

Date: 2026-08-30

## What survives from M2

M2 established that the connected truth-rooted objective can be non-submodular even on a four-cycle, greedy can be arbitrarily poor without structural assumptions, and block-sparse deletions reduce the connected objective to fixed-set coverage. M3 does not weaken those warnings.

## M3.1 Robust-min counterexample

Even if every scenario objective is a modular/coverage function, pointwise robustification by minimum over scenarios need not be submodular. On ground set `{a,b}`, let `f1(Q)=1[a in Q]` and `f2(Q)=1[b in Q]`. Both are modular. Their robust value `g(Q)=min(f1(Q),f2(Q))` has `g({a})=g({b})=0`, `g({a,b})=1`, `g(empty)=0`, violating submodularity. Therefore a generic minimax wrapper does not inherit the coverage guarantee.

## M3.2 One-failure robustification counterexample

Let the base utility be cardinality coverage `f(Q)=|Q|`. Define one-failure robust utility as the minimum score after no failure or removal of one selected item. Then singletons have robust value 0 while `{a,b}` has robust value 1. Again, `0+0 < 1+0`, so worst-case dropout robustness is not generally submodular even when the base objective is modular.

This is why M3 certifies robust panels by exact enumeration on the 16-context bundle instead of transferring a greedy theorem through the robustification operator.

## M3.3 Independent-failure expectation boundary

For fixed independent item survival probabilities and a monotone submodular base set function, expectation over the random surviving subset preserves submodularity by linearity of expectation over submodular functions induced by each fixed survival realization. This observation supports expected-failure scoring for coverage-like objectives, but it does **not** rescue the truth-rooted connected objective when the base objective itself is non-submodular, nor the pointwise minimax operator above.

## M3.4 Noise/tolerance bound

If every phenotype coordinate for both candidate and target responses is perturbed by at most `eta`, target-relative sup-distance changes by at most `2 eta`. Thus using threshold `delta + 2 eta` is a conservative survivor-set stress test. This finite bound does not specify a stochastic phenotype model and should not be described as one.

## M3.5 Solver checkpoint

The candidate library has 16 contexts. Exact enumeration over feasible cost/burden/cardinality panels is therefore the primary certificate. Subset DP builds coverage unions/resources, and a sparse binary MILP independently matches the exact nominal costed pair-coverage optimum value. This solver agreement is an implementation check, not a new optimization theorem.

## Claims explicitly not made

- No mathematical priority claim for Test Cover, active diagnosis, adaptive experiment design, submodular cover with costs, robust submodular selection, critical-node optimization, or graph interdiction.
- No claim that the simulator law-MST x Q4 topology is living biological topology.
- No claim that the current synthetic cost/burden/failure numbers are experimentally measured.
- No claim that M2's greedy=exact result on 17,280 rows transfers to minimax/noisy/failure-aware objectives in general.
