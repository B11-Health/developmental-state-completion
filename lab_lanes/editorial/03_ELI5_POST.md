# ELI5 post

## Public copy

### What does “developmental state completion” mean in plain English?

Imagine you are trying to predict what a growing plant cell will do next.

You can look at **what it looks like now**. You can also ask about **where it came from** - its earlier measurements, lineage, or history.

The basic test is simple:

**If knowing the present already lets us predict the future as well as we can, does the older measured history still add useful information?**

If the answer is no for a particular task, we say the present measurement behaves like a **sufficient state for that task**. That does **not** mean the plant has no memory. It does not mean biology is one-dimensional. It does not mean development is universally Markovian. It only means that, for the future we chose to predict and the measurements/models we tested, the older measured history did not add a stable material gain.

In one late-stage Arabidopsis flower-atlas task, that is roughly what we see: the current atlas state helps predict later growth, while adding the released older ancestor state gives little or no stable extra gain across the tested lineage-aware analyses. But in an earlier window, history looks more model-dependent. That is exactly why the claim has to stay narrow.

Now suppose two hidden biological mechanisms can look almost the same today. A baseline picture may not tell them apart. The next idea is to **poke the system in a carefully chosen way** and see whether they respond differently.

Think of two identical-looking locked boxes. Looking at the boxes tells you little. Pressing the right button may make one beep and the other flash. The response gives you information the static appearance did not.

We tested that logic in a restricted simulator, where designed contexts could recover a hidden signed state under a frozen prospective protocol. That is encouraging, but it is still a simulator result. The real biological test - using living Arabidopsis plants - has not been completed yet.

The bigger lesson is not “we found the secret state of life.” It is more modest and more testable:

**Measure the present. Check whether the past still predicts anything important. If it does, your state description is incomplete. Then choose the next perturbation to expose the missing difference.**

## Internal evidence-status block

| Evidence class | ELI5 translation | Status |
|---|---|---|
| OBSERVED-DATA REANALYSIS | Late-L1 FM1 task shows a narrow screening pattern; earlier L1 is more model/split sensitive. | Reproduced/narrowed |
| SIMULATOR EVIDENCE | Designed contexts recover hidden signed state in restricted frozen source simulator. | Reproducible simulator evidence |
| MATHEMATICAL RESULT | “Adding the right probe can reduce ambiguity” has precise assumptions; greedy is not universally safe. | Current theorem/counterexample work |
| HISTORICAL / PROVENANCE-INCOMPLETE | Do not use old 224-world or exact historical FM1 headline numbers to illustrate the ELI5 story. | Historical-only |
| PROSPECTIVE LIVING VALIDATION | The decisive plant perturbation test has not yet been run. | Future work |

## TikTok/short-video caption

Can the present “contain enough” of a cell’s past to predict what happens next? We test that by asking whether older measured history still improves future prediction after the current state is known. In one late Arabidopsis flower-atlas task, it mostly does not; in an earlier window, the answer is less stable. A simulator supports the idea of using perturbations to expose hidden differences, but living-plant validation is still ahead.
