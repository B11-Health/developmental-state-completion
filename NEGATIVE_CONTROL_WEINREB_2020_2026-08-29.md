# External state-incompleteness control — Weinreb et al. 2020

Date: 2026-08-29

## Purpose

A state-completion diagnostic is not credible if it only finds examples where old/lineage information looks redundant. It must also flag a measured state as **incomplete** in a system where independent lineage experiments demonstrate hidden fate information.

We therefore use the public data from Weinreb, Rodriguez-Fraticelli, Camargo & Klein, *Lineage tracing on transcriptional landscapes links state to fate during differentiation* (Science 2020, PMID 31974159, PMCID PMC7608074) as an external positive control for state incompleteness.

This is **not a new hematopoiesis discovery**. The original paper already showed that heritable fate properties can be hidden from scRNA-seq. Our goal is only to test whether a lightweight version of our screening-off logic recognizes that failure mode.

## Public release used

Repository README:
`https://github.com/AllonKleinLab/paper-data/tree/master/Lineage_tracing_on_transcriptional_landscapes_links_state_to_fate_during_differentiation`

Two small released files are sufficient for this control:

- `stateFate_inVitro_metadata.txt.gz` — cell time point, starting population, mature cell-type annotation, well, and SPRING x/y coordinates;
- `stateFate_inVitro_clone_matrix.mtx.gz` — binary clone membership.

The full normalized transcript matrix is approximately 2 GB compressed and is deliberately not required for this lightweight control. The present-state proxy here is therefore **mean day-2 SPRING position + starting population**, not the full transcriptome.

## Why this is a valid negative control

The original paper reports that transcriptional state predicts fate only partially and that separated sister cells retain highly concordant fate outcomes. It explicitly concludes that heritable cellular properties can influence fate while remaining undetected by scRNA-seq.

In the authors' split-well logic, a measured state would be functionally complete only if separated future sister outcomes were conditionally independent after conditioning on that state.

## Release-native cohort reconstruction

Using the public clone matrix literally:

- **677 clones** have day-6 cells in both well sets;
- **504 clones** have at least one mature fate represented in both wells;
- **217 clones** additionally have a sampled day-2 sister and descendants in both day-6 wells;
- after excluding tied/empty dominant-fate assignments, 158 remain;
- restricting prospectively to the three well-supported dominant fates `Neutrophil`, `Monocyte`, and `Baso` gives **133 clones**.

The paper reports different analysis counts (for example 408 clones in one split-well test and 502 in a late-prediction analysis), indicating additional filtering/analysis rules not encoded in the README. We therefore report our counts as a **release-native reconstruction**, not an exact reproduction of those figure cohorts.

## Test 1 — split-well fate-set concordance

Among the 504 clones with mature cells in both day-6 wells:

- exact mature-fate-set agreement between separated sister wells: **57.94%**;
- mean agreement after permuting well-2 clone identities: **17.40%**;
- permutation 95th percentile: **20.04%**;
- empirical `p = 0.0002` with 5,000 permutations.

This reproduces the **direction and magnitude class** of the original paper's sister-fate concordance result, but not its exact published 70% versus 22% numbers because the release-native filtering differs.

## Test 2 — does sister-lineage information improve prediction beyond day-2 state?

On the frozen 133-clone three-fate cohort, the target is the dominant mature fate in day-6 well 2.

Current-state proxy:

- mean day-2 SPRING x/y position for the clone;
- starting population (`Lin-Kit+Sca1+` or `Lin-Kit+Sca1-`).

Added lineage/fate information:

- dominant mature fate observed in the separated day-6 sister well 1.

Repeated five-fold stratified cross-validation (40 repeats in the high-precision run) with balanced multinomial logistic regression gave approximately:

| Model | Accuracy | Balanced accuracy | Log loss |
|---|---:|---:|---:|
| Day-2 state proxy | **0.606** | **0.618** | **0.938** |
| Day-2 state + separated sister fate | **0.820** | **0.827** | **0.559** |

Average paired gain from sister information:

- accuracy: **+0.213**;
- balanced accuracy: **+0.209**;
- log-loss reduction: **0.379**.

The held-out result therefore behaves exactly as an incompleteness control should: the measured day-2 state proxy does not screen off lineage-linked future information.

## Test 3 — conditional mutual information within day-2 state neighborhoods

To avoid relying on one classifier, day-2 state was coarsened into K-means neighborhoods using standardized SPRING x/y plus starting-population encoding. We then estimated

`I(F_well2 ; F_well1 | S_day2_bin)`

on the three-fate cohort and permuted well-1 fate labels **within the same current-state bins**.

| State bins | Observed CMI (bits) | Permutation null mean | Null 95th percentile | p (3,000 perms) |
|---:|---:|---:|---:|---:|
| 4 | 0.693 | 0.080 | 0.127 | 0.00033 |
| 6 | 0.650 | 0.143 | 0.201 | 0.00033 |
| 8 | 0.589 | 0.139 | 0.192 | 0.00033 |
| 10 | 0.583 | 0.149 | 0.217 | 0.00033 |

Residual dependence survives every tested state-resolution scale.

## Interpretation

This control supports a limited methodological claim:

> The same general state-sufficiency logic that finds little residual history in late FM1 can also identify strong residual lineage-linked information in a published system where the original investigators independently established hidden heritable fate properties.

That is evidence that the diagnostic is not structurally biased toward declaring every state complete.

## Important limitations

1. SPRING x/y is a low-dimensional visualization embedding of transcriptomic state, not the full scRNA-seq vector. This control is therefore easier than the original full-transcriptome prediction problem.
2. The added sister-well fate is **lineage-linked future information**, not literally an older historical measurement. This is a positive control for *state incompleteness / failure of screening-off*, not a direct copy of the FM1 history-gain statistic.
3. Our release-native clone counts differ from the paper's figure-specific counts, so exact numerical replication of Figure 3 is not claimed.
4. Cell types and fate combinations are observational labels supplied by the authors.
5. This result does not imply that the same hidden variables exist in plants.

## Consequence for developmental state completion

A useful state-completion framework must support both outcomes:

- **late FM1:** current released atlas state largely absorbs measured older-history information for a narrow future-growth task;
- **Weinreb/Klein control:** measured present-state proxy clearly fails to absorb lineage-linked information about future fate.

The scientific question is therefore not “is development Markov?” It is:

> For this organism, developmental stage, measurement stack, future task and intervention family, how much future-relevant information remains outside the current measured state?

## Reproduction

`analysis/weinreb_hidden_state_negative_control.py`

The script downloads only the two small public files above if they are absent.
