# R2 Cross-System State-Sufficiency Replication Checkpoint — 2026-08-29

## Status
**Complete as a conservative cross-system replication. The preregistered positive residual-history decision rule is NOT met because calibration power is inadequate, despite large observed nonlinear history gains.**

This lane does not alter the project evidence ledger and makes no publication claim.

## Why this dataset
A plant-first search identified the 2026 Arabidopsis multiscale growth atlas, but its immediately accessible material was meta-analytic/aggregate and the SI download path was browser-challenge protected. I did not reconstruct individual H/S/Y trajectories from plots.

The strongest directly recoverable developmental fallback was the public Cell Tracking Challenge `Fluo-N3DH-CE` dataset: two longitudinal 3D microscopy sequences of a developing *C. elegans* embryo with explicit lineage ground truth. It is distinct from Refahi FM1 and Weinreb/Klein. The CTC page attributes it to the Waterston Lab and links Murray et al. (2008), *Nature Methods*, DOI `10.1038/nmeth.1228`. See `SOURCE_PROVENANCE.md`.

## Frozen task
The task was preregistered in `PREREGISTRATION.md` before biological model fitting. For focal tracks with an observed binary division and complete parent/grandparent history:

- **Y:** focal cell-cycle duration in frames (`end - start + 1`).
- **S:** focal birth/start frame, lineage depth, embryo indicator.
- **H:** parent cycle duration, grandparent cycle duration, parent-minus-grandparent duration.

The question is narrow: **does older lineage timing add held-out predictive value for focal division timing after this coarse candidate present state?** This is not a test of full molecular state completion or organismal Markovity.

## Cohort and leakage controls
- 701 eligible dividing focal tracks: 346 from embryo 01, 355 from embryo 02.
- 24 primary groups defined by embryo + depth-2 ancestor.
- 12 stricter groups defined by embryo + depth-1 ancestor.
- 100 repeated GroupShuffleSplit partitions, 25% of groups held out.
- Maximum train/test group overlap: **0**.
- Track IDs, focal end frame, descendants, child timing, and future image measurements were forbidden as predictors.
- A 30-split permuted-target sanity control produced nonpositive median history gain for all estimators.

## Primary held-out results

| Estimator | median R2(S) | median R2(S+H) | median delta R2 | positive splits | delta R2 2.5–97.5% |
|---|---:|---:|---:|---:|---:|
| HistGradientBoosting | 0.533 | 0.727 | **+0.171** | 96% | -0.022 to +0.427 |
| Random forest | 0.550 | 0.736 | **+0.134** | 93% | -0.024 to +0.564 |
| Ridge | 0.676 | 0.711 | +0.045 | 66% | -0.060 to +0.245 |

The nonlinear estimators show large, repeated held-out gains from ancestral timing. Ridge is positive in median but split-unstable.

## Known-complete / known-incomplete calibration
Matched synthetic outcomes were generated on the same rows, groups, and feature matrices. The known-complete outcome depends on S plus Gaussian noise matched to the empirical S-only residual scale. The known-incomplete outcome adds a parent-duration residual component of **0.30 target SD**, as frozen in the preregistration. There were 200 simulations.

| Estimator | known-complete 95th percentile delta R2 | observed median above cutoff? | power for +0.30 SD incomplete control |
|---|---:|---:|---:|
| HistGradientBoosting | +0.041 | yes | **17.5%** |
| Random forest | +0.058 | yes | **21.0%** |
| Ridge | +0.016 | yes | **39.0%** |

Thus the observed median gain exceeds the matched complete-state null cutoff for all three estimators, but the pipeline has poor power for the preregistered moderate incomplete-state effect. The preregistered rule required >=80% calibration power for at least two estimators. **No estimator meets that condition.**

## Preregistered decision
The preregistered positive rule required at least two estimators to satisfy all four conditions:
1. median delta R2 > +0.02;
2. positive delta R2 on >=80% of grouped splits;
3. observed median above the known-complete 95th-percentile cutoff;
4. >=80% power for the +0.30 target-SD known-incomplete control.

HistGradientBoosting and random forest satisfy conditions 1–3 but fail condition 4. Ridge also fails split stability and power. Therefore:

> **R2 does not promote a positive stable-residual-history claim under its preregistered rule.**

This is a calibration-limited result, not a null result. The raw biological prediction pattern is consistent with residual lineage-history information beyond this coarse S, but the analysis as preregistered cannot establish the requested stable-history criterion at its own declared sensitivity standard.

## Sensitivities
### Stricter depth-1 clade grouping
- HistGradientBoosting median delta R2 **+0.172**, 89% positive.
- Random forest **+0.188**, 94% positive.
- Ridge **+0.065**, 67% positive.

The nonlinear signal does not disappear when larger related subtrees are held together.

### Remove embryo indicator from S
- HistGradientBoosting median delta R2 **+0.178**, 98% positive.
- Random forest **+0.155**, 97% positive.
- Ridge **+0.068**, 78% positive.

The nonlinear history gain is not explained by simply encoding embryo identity in S.

### Permuted-target leakage sanity check
Median delta R2 is -0.077 (HistGradientBoosting), -0.046 (random forest), and -0.002 (Ridge). This argues against a trivial pipeline artifact that mechanically rewards the larger H feature block.

## Interpretation allowed
For this public *C. elegans* embryonic lineage-timing task, ancestral division timing carries substantial held-out predictive information for nonlinear decoders beyond a deliberately coarse present representation consisting of developmental time, depth, and embryo identity. The effect persists under stricter genealogical grouping and removal of embryo identity.

## Interpretation not allowed
- Do not claim that *C. elegans* development is non-Markov in its true biological state.
- Do not claim molecular memory or hidden epigenetic state from lineage timing alone.
- Do not claim that the preregistered stable-history criterion was met; it was not.
- Do not treat S as a complete cell state; it is intentionally coarse.
- Do not generalize this result to Arabidopsis or to the Refahi FM1 task.

## Falsification outcome
The lane was designed so that a positive biological pattern could still fail promotion if the calibration could not support the declared sensitivity. That is exactly what happened. The observed nonlinear signal survived the main leakage/sensitivity attacks, but the predeclared +0.30-SD calibration had only 17.5–39% power, so the stronger conclusion is frozen as **unresolved** rather than rescued post hoc.

## Artifacts
- `PREREGISTRATION.md`
- `SOURCE_PROVENANCE.md`
- `fetch_ctc_lineage_metadata.py`
- `analyze_ctc_ce_lineage.py`
- `run_batched.py`
- `aggregate_results.py`
- `source_data/manifest.json` and two hashed lineage tables
- `results/grouped_split_results.csv`
- `results/summary.csv`
- `results/calibration_split_results.csv`
- `results/calibration_summary.csv`
- `results/decision_table.csv`
- `results/depth1_group_summary.csv`
- `results/no_embryo_indicator_summary.csv`
- `results/permutation_summary.csv`
- `results/run_metadata.json`

## Reproducibility note
The original one-shot analysis exceeded the Authenticated Shell command window after writing the cohort table, so the exact same deterministic estimator/split definitions were executed in batches. Batch files are retained in `results/`; `aggregate_results.py` reconstructs the final tables. No external data were altered, no publication/send action occurred, and no remote push was performed.
