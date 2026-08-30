# M3 preregistration-ready perturbation-design policy

Date: 2026-08-30

## Decision rule

Before a living run, freeze: (1) the candidate perturbation library, (2) phenotype-distance metric, (3) nominal tolerance `delta`, (4) measurement-error bound or calibrated noise model, (5) per-experiment biological burden, direct cost and operational failure probability, (6) total budget, and (7) any prior over candidate worlds. Then rerun the exact finite selector.

For the planned pilot, use a **prospective unknown-truth** rule. Do not choose a panel using a known simulator truth or a post-hoc biological outcome.

Primary lexicographic policy:
1. maximize worst-case truth-rooted connected elimination over all candidate truths, declared tolerance/noise scenarios, and loss of any one selected experiment;
2. maximize topology-free worst-case ambiguity elimination;
3. maximize robust Test-Cover/pair separation;
4. maximize robust expected ambiguity-class entropy under the declared primary prior;
5. maximize worst-scenario expected truth-rooted elimination under independent experiment failures;
6. minimize biological burden, then direct cost.

If the living topology assumption is not defensible, drop criterion 1 and use topology-free criteria 2-6. Never silently substitute the simulator topology for living biology.

## Current preserved-bundle result

With the explicitly synthetic planning proxies currently encoded in M3, the tight-budget recommendation is `0010 0100 1000` (cost 36 units, burden 15 units, three perturbations). It guarantees, across the four declared stress scenarios and any single selected-experiment failure in this finite simulator audit, at least 110/128 truth-rooted eliminations, at least 120/128 topology-free ambiguity eliminations, 7,535/8,128 separated pairs, and 6.625 bits of uniform-prior ambiguity-class entropy. These are simulator/planning numbers only.

The best known-truth retrospective panel for the frozen P06/0000 stress truth is different (`0100 0101 0110`), demonstrating why retrospective optimization must remain quarantined from prospective design.

## Solver policy

For <=16 candidate perturbations, exact enumeration is the certification path. Use subset DP for resource totals and pair-coverage unions, and independently cross-check coverage objectives by MILP where useful. Greedy may be reported as a heuristic comparison but is not the certification path for connected/minimax objectives because M2 already showed non-submodularity and arbitrarily bad greedy examples in general.

For larger libraries, first identify whether the objective is in a safe coverage/submodular regime. If yes, cost-aware submodular-cover/maximum-coverage approximations may be justified by the applicable theorem. Otherwise use MILP/branch-and-bound, dynamic programming on exploitable graph structure, or another exact/controlled-approximation method with an explicit optimality gap.

## Failure/noise treatment

M3 uses the conservative metric-error bound `delta_eff = delta + 2 eta` for bounded phenotype-coordinate error `eta`, following the target-relative distance perturbation bound already verified in M1. Robust selection takes the minimum over declared tolerance/noise scenarios and over no failure or loss of any one selected perturbation. A separate expected score assumes independent experiment failures with the declared per-context probabilities.

## Mandatory gate before biology

The current cost, burden and failure arrays are dimensionless stress-test proxies. Replace them with protocol-derived quantities and freeze them before experiment selection. If those values are not available, the correct status is design-policy ready / biological panel not yet certified.
