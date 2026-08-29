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
