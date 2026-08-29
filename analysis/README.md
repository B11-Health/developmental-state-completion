# Independently Rerunnable Analyses

These scripts are deliberately small and dependency-light. They are separate from the raw ChatGPT/NotebookLM research logs and are used to promote a claim from **reported** to **reproduced computationally**.

## 1. Greedy connected-ambiguity counterexample

Run:

```bash
python analysis/greedy_component_counterexample.py
```

Artifacts:
- `greedy_component_counterexample.py`
- `greedy_component_counterexample_results.csv`

Checks an `n x n` grid construction in which complementary half-wall experiments jointly split the candidate-world graph while a boundary-column decoy fools a budget-two greedy policy. The script asserts the exact ratio

`greedy / optimal = 3/n`,

which tends to zero. This verifies that connected-component ambiguity reduction is not generally submodular and that greedy selection has no generic constant-factor guarantee.

## 2. Finite-sample state-completion CMI calibration

Run:

```bash
python analysis/state_completion_cmi_calibration.py
```

Artifacts:
- `state_completion_cmi_calibration.py`
- `state_completion_cmi_calibration_results.csv`

Simulates a known first-order Markov binary system and a deliberately second-order/history-dependent alternative. It estimates plug-in conditional mutual information `I(Y;H | S,A)` over 1,000 Monte Carlo trajectories at each sample size.

The test is not intended to define a universal threshold. It demonstrates why an empirical state-completion analysis must calibrate both:

- **false-positive behavior** under a process known to be complete/Markov under the measured state; and
- **power** under a process with known residual history dependence.

## Reproducibility rule

If a future mathematical/statistical claim originates in a research-agent output, it should not be labeled `REPRODUCED COMPUTATIONALLY` until a separate, checked script or derivation in this directory reproduces the relevant result without depending on the agent's cached numerical output.


## 3. Refahi Arabidopsis flower-atlas state-completion audit

Primary checkpoint: `../REPLICATION_CHECKPOINT_2026-08-29.md`.

### External source

The analysis does **not** redistribute the authors' cell-level source data. Clone the public source repository as a sibling of this repository:

```bash
git clone https://gitlab.com/slcu/teamHJ/publications/refahi_etal_2020.git refahi_diag
git -C refahi_diag checkout 95fde8b3b9a0bd09d556ce765a2235093362306f
```

The full microscopy/segmentation archive is cited by the primary paper at DOI `10.17863/CAM.61991`; the textual FM1 geometry, lineage pickle and atlas gene-state files needed for this audit are present in the cited GitLab commit.

### Python dependencies

```bash
python -m pip install numpy pandas scipy scikit-learn
```

The scripts auto-discover a sibling directory named `refahi_diag`. An explicit checkout can instead be supplied through environment variable `REFAHI_ROOT`.

### Frozen primary cases

Run each case separately (the 100-permutation primary null plus nonlinear robustness can be computationally heavier when all four are batched):

```bash
python analysis/refahi_state_completion_replication.py --hist 40 --cur 96 --fut 120 --subset all
python analysis/refahi_state_completion_replication.py --hist 40 --cur 96 --fut 120 --subset L1
python analysis/refahi_state_completion_replication.py --hist 96 --cur 120 --fut 132 --subset all
python analysis/refahi_state_completion_replication.py --hist 96 --cur 120 --fut 132 --subset L1
```

Outputs are written to `results/refahi_<history>_<current>_<future>_<subset>.json`.

### Matched known-complete / known-incomplete calibration

Example:

```bash
python analysis/refahi_calibrate_history_delta.py 96 120 132 L1 --sims 100
```

Repeat with the four primary cases. The known-complete generator makes future outcome depend only on current features; the known-incomplete generator adds a residualized older-history direction of 0.20 target SD. The calibration is intentionally tied to the exact Ridge ΔR² statistic used in the checkpoint.

### Post-hoc sensitivity analyses

These were specified **after** the primary four-case results and must not be presented as preregistered tests:

```bash
python analysis/refahi_posthoc_layer_sensitivity.py
python analysis/refahi_posthoc_layer_subsets.py
python analysis/refahi_posthoc_ridge_sensitivity.py
python analysis/refahi_posthoc_combinatorial_state.py
python analysis/refahi_posthoc_split_sensitivity.py
```

### Measurement limitation

The 25 released expression channels in this audit are binary domains manually integrated into the FM1 reference atlas from literature, RNA in-situ hybridization and some live imaging. They are not repeated 25-gene measurements made longitudinally in the exact same living cells. This limitation is part of the result, not a footnote to be removed from public communication.
