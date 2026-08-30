# R7 Relational Adequacy Rescue

This lane tests whether richer release-native relational present-state features rescue whole-acquisition future prediction in the R5 Drosophila and R6 Tribolium datasets before any older-history interpretation.

## Reproduce
Run:

`python lab_lanes/r7_relational_adequacy_rescue/r7_relational_rescue.py`

The script uses only committed R5/R6 source-derived files and writes deterministic result tables under `results/` with seed `20260830`.

## Outcome
All four preregistered organism×outcome adequacy tests fail Gate 1. The code therefore writes zero history-fit rows and zero permutation rows by design. See `R7_RELATIONAL_ADEQUACY_CHECKPOINT_2026-08-30.md` for the scientific decision.
