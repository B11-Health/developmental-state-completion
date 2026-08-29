# Technical post for scientists

## Public copy

### A narrower formulation of developmental-state completion after replication, provenance, and theorem audits

We have substantially narrowed the project’s public claim after independent replication, provenance recovery, and mathematical red-team work.

For a predefined developmental task and intervention family, let `H` denote older measured history, `S` a candidate present-state representation, and `Y^pi` a future outcome under intervention/policy `pi`. The empirical diagnostic is residual history value after conditioning on `S`, evaluated out of sample and calibrated against known-complete and known-history-dependent controls.

Under Bayes-optimal log loss, the population value of adding `H` is conditional mutual information, `I(Y;H|S)`; under squared loss, zero incremental value only establishes conditional-mean screening-off. We therefore avoid treating “no predictive gain” as model-free conditional independence.

In the released Arabidopsis FM1 atlas, the strongest surviving biological result is the predefined `96 -> 120 -> 132 h` L1 growth task. Current geometry plus the released 25-channel integrated atlas state predicts future lineage growth strongly. Adding the released 96 h ancestor representation provides no material incremental gain in the late-L1 repeated lineage-grouped analyses across the tested decoder families. The earlier L1 window is materially more split- and estimator-dependent, which argues against a universal monotone “completion” narrative. The atlas channels are integrated binary annotations on the reference, not simultaneous longitudinal molecular measurements in every tracked living cell.

As an external incompleteness control, a reanalysis of the public Weinreb/Klein split-well lineage data shows substantial residual sister-well fate information after conditioning on a reduced day-2 state proxy. We use that directionally: the diagnostic can reject an inadequate present-state proxy in a system where hidden heritable fate information is independently established.

The inverse-problem side is also narrower. For a target world `w*`, experiment panel `Q`, and coordinatewise monotone/sup response metric, define a finite-resolution compatible set and its target-connected component `C_Q^delta(w*)`. Adding experiment coordinates monotonically refines this component. Under uniform signature error `eta`, target-relative distances shift by at most `2 eta`, yielding the corresponding tolerance sandwich; in finite graphs, bottleneck/merge thresholds are stable under that perturbation bound even when a single fixed-delta component can jump.

At fixed positive hidden-world resolution, a continuous point-separating experiment family on a compact world space admits a finite uniformly separating panel by a standard compactness argument. This is not presented as new mathematics. For finite candidate libraries, global pair separation reduces to Test Cover/set cover on structurally relevant pairs.

Crucially, target-connected ambiguity reduction is not generally submodular. An explicit grid construction gives greedy/optimal ratio `3/n -> 0`. A source-derived topology-proxy stress test also exhibits increasing marginal gains, although greedy still matches the exact optimum for budgets 1-5 in that particular finite instance. Under a deterministic rooted-tree deletion model, the objective reduces to a coverage function and classical `(1-1/e)` greedy guarantees return.

The novelty boundary is therefore explicit: predictive states, causal-state equivalence, augmented-state observability/identifiability, connected fiber topology/Reeb-style constructions, active intervention design, set cover, and submodularity are established precedents. The candidate contribution is the **task-specific integration** of calibrated residual-history sufficiency, finite-resolution joint state-law ambiguity, and ambiguity-targeted perturbation design into a prospective developmental-biology workflow.

A frozen two-context source-simulator experiment provides prospective computational evidence for that workflow in a restricted four-channel model. It is not living-plant validation. The biological confirmatory experiment remains prospective and is currently gated by material/cross feasibility, reporter compatibility, perturbation-burden controls, and a valid equal-cost/random comparator.

One further correction: the exact historical `0.272 -> 0.643` FM1 tuple and the original 224-world/topology/ranking artifacts are provenance-incomplete in the current workspace. We do not use them as independently reproduced evidence.

## Internal evidence-status block

| Evidence class | Technical claim | Status |
|---|---|---|
| OBSERVED-DATA REANALYSIS | FM1 late-L1 screening pattern; earlier-window dependence; Weinreb/Klein incompleteness control. | Reproduced/narrowed |
| SIMULATOR EVIDENCE | Frozen two-context source-simulator recovery in restricted model. | Reproducible |
| MATHEMATICAL RESULT | Loss-aware screening identities; refinement; tolerance sandwich; finite-resolution separator; greedy impossibility; rooted-tree safe regime. | Mix of established identities and project-specific theorem/counterexample work; novelty boundaries mandatory |
| HISTORICAL / PROVENANCE-INCOMPLETE | Exact legacy FM1 tuple; 224-world bundle; historical topology/ranking values. | Do not use as replicated quantitative evidence |
| PROSPECTIVE LIVING VALIDATION | Blinded RCOg-V/suppressor perturbation workflow and comparators. | Not yet performed |

## Suggested scientist-facing title variants

- “Predictive sufficiency in development: what survived a replication and theorem audit”
- “From residual history to perturbation design: a narrowed developmental-state workflow”
- “Why our connected-ambiguity objective breaks greedy guarantees”
