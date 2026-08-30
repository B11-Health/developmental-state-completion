# R10 Methods — Registered History Increment and Calibration

## Observed analysis
R10 uses only the R9-primary adequate task: Tribolium future radial velocity under transductive within-acquisition percentile registration. The committed R8 99-feature present matrix is percentile-ranked separately within each acquisition. The four inherited older-history columns are percentile-ranked the same way when added to S. Only Random Forest and Extra Trees determine the history gate because only those estimators passed R9 Gate 1.

For each reciprocal held-out acquisition, the same model is fit with S and with S+H. Delta R2 is computed on identical held-out rows. Gate 2 requires positive delta R2 in both folds and mean delta R2 >=0.02 for both models, with S+H remaining absolutely adequate.

## Matched null
One hundred deterministic permutations independently scramble H row assignments in source and target domains while preserving S, Y and H marginal distributions. Each replicate refits S+H and applies the full Gate-2 rule. This is a matched finite-sample no-increment control, not a proof of conditional independence.

## Known-incomplete calibration
Thirty deterministic residual-history directions are generated from random unit combinations of the four registered H columns. Each direction is residualized against registered S using Ridge(alpha=1) with no Y, standardized, and injected into the actual outcome at 0.30 times the original target SD. The same RF/ExtraTrees S and S+H models are refit under both reciprocal holds.

A calibration replicate counts as successful only if the injected dataset preserves the two-model S-only adequacy prerequisite and the same Gate-2 rule detects the injected history effect. The preregistered requirement is >=24/30 successes.

## Execution
Observed analysis was run once. The 100 permutation replicates were serialized in five 20-replicate jobs; the 30 calibration replicates were serialized in three 10-replicate jobs to stay within the shell execution window. The scientific configuration did not change between jobs.
