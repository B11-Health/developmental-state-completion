# Evidence-safe research update

## Public copy

### What survived our latest internal audit

We have been testing a narrow question in developmental biology: **when does a measurement of the present contain enough information for a specified future task, and when does older measured history still add something important?**

The latest audit made the project smaller in some places and stronger in others.

In a direct-source reanalysis of the released Arabidopsis FM1 flower atlas, the clearest result is a **late L1 epidermal growth task**. In that predefined window, current geometry plus the released 25-channel atlas state predicts future lineage growth strongly, while adding the released 96-hour ancestor state gives no stable material improvement across the lineage-grouped analyses we tested. That is a task-, stage-, representation-, decoder-, loss-, and finite-sample-specific screening pattern. It is **not** proof that flower development is Markovian, that the plant "forgets" its past, or that all relevant biological memory has disappeared.

The earlier L1 window is an important counterweight: residual history value is much more split- and estimator-dependent there. That disagreement is useful. It tells us not to force a universal "state completion" story onto the data.

We also tested the diagnostic on a published mammalian lineage system where hidden heritable fate information is known to matter. The method flags the reduced present-state proxy as incomplete there. That gives us a positive control: the procedure is capable of saying "the present measurement is not enough."

On the computational side, a **separate, prospectively frozen source-simulator experiment** showed that two designed phenotype contexts could recover a hidden signed state in a restricted four-channel model with the preregistered decoder and thresholds. That is a simulator validation of the experimental logic, not living-plant validation.

The mathematics also became more disciplined. Adding experiments refines the target ambiguity under a monotone experiment metric, and finite-resolution separation can be guaranteed under standard compactness/continuity assumptions. But the topology-sensitive connected-ambiguity objective is not generally submodular: we have an explicit construction where greedy experiment selection becomes arbitrarily bad, with greedy/optimal ratio `3/n -> 0`. Under additional structure, such as the deterministic rooted-tree coverage regime, classical greedy guarantees return. None of the surrounding ideas - predictive states, observability, Reeb/Stein fiber topology, set cover, or submodularity - are being claimed as inventions of this project.

A separate provenance audit also forced corrections. The original artifact bundle behind the historical 224-world report was not recovered, and the exact old `0.272 -> 0.643` FM1 headline pair cannot be regenerated from an executable artifact chain that existed with the original prose. Those numbers now stay labeled historical/provenance-incomplete rather than being blended into the reproducible results above.

So the current claim is deliberately narrow:

**We are developing a falsifiable workflow for testing whether a physically measurable present developmental state is predictively sufficient for a specified task, and - when it is not - for choosing perturbations against the specific joint state-law ambiguity that remains.** The ingredients have strong precedents. The candidate contribution is the integration and the prospective biological test.

The decisive next step is still ahead of us: a living Arabidopsis perturbation experiment, with a frozen decoder, blinded evaluation, a complete baseline-only comparator, and - if a biologically legitimate burden-matched perturbation can be validated - an equal-cost/random comparator. Until that experiment is run, we will call it what it is: a prospective validation plan.

## Internal evidence-status block - do not delete when adapting

| Evidence class | What this post says | Current status | Primary grounding |
|---|---|---|---|
| OBSERVED-DATA REANALYSIS | Late-L1 FM1 current state is strongly predictive; older released history has no stable material gain under tested grouped analyses. Earlier L1 is estimator/split sensitive. Weinreb/Klein serves as an incompleteness control. | Reproduced/narrowed | `CLAIMS_AND_EVIDENCE.md` C1, C13-C15; `lab_lanes/replication/R1_REFAHI_REPLICATION_CHECKPOINT_2026-08-29.md` |
| SIMULATOR EVIDENCE | Frozen two-context source-simulator recovery supports the probe logic in a restricted model. | Reproducible simulator result | `CLAIMS_AND_EVIDENCE.md` C17; `source_validation/two_context_2026-08-26/` |
| MATHEMATICAL RESULT | Monotone refinement under a monotone metric; finite-resolution separation; greedy can be arbitrarily bad; rooted-tree safe regime. | Proved/reproduced with stated assumptions | `lab_lanes/math/THEOREM_COUNTEREXAMPLE_CHECKPOINT_2026-08-29.md` |
| HISTORICAL / PROVENANCE-INCOMPLETE | Historical 224-world bundle and exact old `0.272 -> 0.643` pair are not currently independently recoverable. | Downgraded; do not use as reproduced evidence | `lab_lanes/provenance/P1_PROVENANCE_RECOVERY.md`; R1 checkpoint |
| PROSPECTIVE LIVING VALIDATION | Proposed Arabidopsis perturbation validation with frozen/blinded comparisons. | Not yet performed | `lab_lanes/biology/B1_CHECKPOINT_2026-08-29.md`; `PREREGISTRATION_READY_MINIMAL_DESIGN.md` |

## Safe short caption

Current evidence is observational, computational, and mathematical - not yet living-plant validation. A late-L1 Arabidopsis reanalysis shows a strong task-specific screening pattern; an earlier window is model-sensitive; a frozen simulator test supports the perturbation logic; and our math shows why greedy experiment choice can fail for connected ambiguity. We also downgraded historical numbers whose original artifact chains cannot currently be recovered. Next: a blinded prospective plant test.
