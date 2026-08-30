# R5 Drosophila Future-Trajectory Checkpoint

Date: 2026-08-30
Decision: **ADEQUACY-LIMITED / DO NOT PROMOTE A RESIDUAL-HISTORY CLAIM**

## Motivation
R4 broadened the global dataset registry but its first executed Arabidopsis analysis was deliberately a same-time measurement-sufficiency proxy. R5 sought a genuine separated future outcome in an independent organism using public release-native trajectories.

## Data recovery
The Cell Tracking Challenge `Fluo-N3DL-DRO` archive is ~6.22 GB and supports byte ranges. R5 parsed the remote ZIP64 central directory and fetched only selected gold tracking masks. This recovered 189 sequence-01 and 203 sequence-02 nervous-system tracking labels at frames 15,20,23,24,25,40, for 392 cells total.

No raw movie download was required.

## Frozen primary H/S/Y
Anchor time: frame 25.

- H = older frame15->20 velocity + speed + label-volume change.
- S0 = normalized frame-25 centroid position + label volume.
- S1 = S0 + frame24->25 velocity + recent volume change.
- S2 = S1 + recent acceleration from frames23/24/25.
- Y = average 3D future velocity over frame25->40.
- group split = hold out an entire acquisition sequence; two reciprocal folds.
- estimators = Ridge, Random Forest, Extra Trees.

## Primary result
All absolute cross-sequence mean held-out R2 values were below zero.

History increments at S2:

| Estimator | R2(S) | R2(S+H) | Delta R2 H |
|---|---:|---:|---:|
| Extra Trees | -1.801 | -1.879 | -0.079 |
| Random Forest | -2.175 | -1.964 | +0.211 |
| Ridge | -1.699 | -1.753 | -0.054 |

The apparent Random-Forest history rescue is not stable across estimators. The primary result therefore fails both absolute adequacy and increment-stability criteria.

## Secondary invariant sensitivity
Because raw global vectors can be sensitive to acquisition orientation, R5 explicitly labeled a post-primary sensitivity using rotation/translation-invariant scalar features and outcomes.

For **future radial velocity**, richer S produced positive H increments across all three models:

| S level | Extra Trees | Random Forest | Ridge |
|---|---:|---:|---:|
| S1 | +0.0908 | +0.0613 | +0.0510 |
| S2 | +0.0735 | +0.0810 | +0.0657 |

However, this is not a positive scientific result. Absolute S+H mean held-out R2 at S2 remained approximately -0.348, -0.362 and -0.606 respectively. A train-only acquisition-mean dummy predictor gave R2 about -0.003 in each held-out sequence. Thus all learned radial models were worse than the naive cross-sequence baseline.

Future-speed transfer was even poorer, with mean R2 roughly -7 to -9.

## New protocol result: absolute adequacy comes before Delta H
R5 demonstrates a failure mode that can generate seductive but meaningless residual-history increments. When the base and augmented models do not transfer to the held-out biological group, `Score(S+H)-Score(S)` can be positive even though `S+H` remains scientifically unusable.

**New promotion order:**
1. establish absolute held-out predictive adequacy against a train-only naive baseline;
2. then test stability/materiality of the H increment across prespecified estimators/groups;
3. then require known-complete/known-incomplete calibration before a state-sufficiency/history decision.

R5 stops at step 1. It would be inappropriate to spend more computation manufacturing a p-value for an increment in an inadequate predictor.

## Interpretation
R5 does **not** tell us whether Drosophila cells possess a path-dependent biological memory. It tells us that this deliberately inexpensive centroid/volume/kinematics representation does not support reliable cross-acquisition future prediction over the tested horizon. Sequence-level orientation and other domain differences are only part of the problem because even invariant scalar outcomes fail adequacy.

The correct next Drosophila design would require a richer present representation (local tissue coordinates, neighborhood geometry, morphology/intensity if released, developmental registration) and more independent acquisition groups before residual-history inference.

## Program impact
This negative result strengthens the larger program by adding a hard protection against false positives. R2 already showed that a large Delta history can be unpromotable because calibration power is weak. R5 now shows a second independent failure mode: a stable-looking Delta history can be unpromotable because **absolute predictive adequacy is weak**.

Together, future promotion requires both sensitivity **and** adequacy.

R5_COMPLETE
