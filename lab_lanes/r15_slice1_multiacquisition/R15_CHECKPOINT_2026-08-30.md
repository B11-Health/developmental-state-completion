# R15 SLICE-1 Multi-Embryo Preview Pilot Checkpoint

Date: 2026-08-30
Decision: **PROMISING CROSS-EMBRYO PRESENT-STATE ADEQUACY / HISTORY QUESTION UNRESOLVED**

## Frozen design
R15 uses the 2025 open SLICE-1 Tribolium light-sheet collection. DS0004 and DS0005 (Cytok8 #2) were development-only and used to freeze an eight-coordinate four-view image geometry state. Before validation previews were downloaded, the protocol fixed DS0007 (Cytok8 #3) as the primary unseen embryo and DS0035 (Lamin #4) as a cross-marker stress test.

Each released full-quality preview has 49 frames at 30-minute intervals. Nine windows use H=t-8, S=t, Y=t+8 for t={9,13,17,21,25,29,33,37,41}, so older history and future are each 4 hours from the present. Y is the full eight-feature future morphology vector, not a selected scalar outcome.

## Primary held-out embryo: DS0007
Training: DS0004 + DS0005 only.

S-only vector results:
- Ridge: R2_vector **-0.0136**, fails absolute adequacy.
- Random Forest: R2_vector **+0.0307**, passes.
- Extra Trees: R2_vector **+0.0567**, passes.

The frozen 2-of-3 Gate 1 therefore **passes**.

Because Gate 1 passed, the preregistered pilot also fit S+H. Delta R2_vector was negative for every estimator:
- Ridge: **-0.0540**
- Random Forest: **-0.0088**
- Extra Trees: **-0.0081**

## Secondary cross-marker stress test: DS0035
The exact same DS0004+DS0005 training fit, features, windows, preprocessing and models were applied to the predeclared Lamin #4 embryo.

S-only vector results:
- Ridge: R2_vector **+0.0371**
- Random Forest: R2_vector **+0.0378**
- Extra Trees: R2_vector **+0.0341**

All three pass absolute adequacy against the train-only mean baseline. Delta R2_vector after adding H was again negative for all three:
- Ridge: **-0.1127**
- Random Forest: **-0.0151**
- Extra Trees: **-0.0776**

## Interpretation
The eight-coordinate current image geometry state shows modest but positive held-out prediction of the full 4-hour-future geometry vector in two untouched embryos. The primary validation crosses to a new Cytok8 subline; the secondary test crosses to a Lamin-labeled embryo and still remains above the train-only baseline for all three models. This is a useful new cross-embryo adequacy result from an independent 2025 public resource.

The negative history increments are **not** evidence of screening-off. R15 has only two development embryos, one primary validation embryo, one secondary stress-test embryo, overlapping temporal windows within embryos, and no matched known-incomplete sensitivity calibration. The correct history status is unresolved.

## Next move
Use the SLICE-1 collection to define a larger fixed multi-embryo cohort before downloading/scoring it, preserve whole-embryo holdouts, then add matched null and known-incomplete calibration. The 50-dataset resource makes that expansion feasible without reusing the original two CTC acquisitions.

R15_PILOT_COMPLETE
