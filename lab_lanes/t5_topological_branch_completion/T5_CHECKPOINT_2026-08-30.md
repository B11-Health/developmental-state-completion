# T5 Topological Branch Completion Checkpoint

Date: 2026-08-30
Decision: **MATHEMATICALLY USEFUL SYNTHESIS / PROSPECTIVE BIOLOGICAL TEST REQUIRED**

## Result
T5 closes an explicit gap left by T4's connected-fiber theorem. When `ker Dh_x subset ker DF_x` holds everywhere but a measurement fiber is disconnected, the condition only forces the future map to be constant on each connected fiber component. The future therefore factors through the fiber-component (Reeb-space) quotient, not necessarily through `h` itself.

For a fixed measured value with `m` future-distinct component classes, any finite branch completion `B` satisfying `F=g(h,B)` needs at least `m` labels, giving a binary lower bound `ceil(log2 m)` bits. Enlarging the intervention family can only refine these future-response classes, so the required branch resolution cannot decrease.

## Frozen counterexample
`X=R\{0}`, `h(x)=x^2`, `F(x)=x` satisfies the local kernel condition everywhere but does not factor through `h`, because `+x` and `-x` are disconnected points in the same fiber with different futures. One sign bit completes the deterministic task.

## Executable history-proxy witness
In the frozen binary example, older history is a noisy proxy for the missing branch. At 15% proxy noise:
- `I(Y;H|Z) = 0.3901597` bits;
- `I(Y;H|Z,B) = 0`.

Thus residual history can disappear after adding a present branch coordinate even when the older measurement was genuinely predictive beforehand. This is an existence demonstration, not evidence that any current biological dataset has this exact structure.

## Prior-art boundary
Reeb/fiber-component quotients, local/global observability distinctions, predictive-state quotients, and Test Cover are established ideas. T5 does not claim those constructions or individual theorems as new. The potentially useful contribution is their synthesis into a falsifiable state-completion workflow.

## Empirical prediction
A candidate biological branch measurement earns support only if:
1. the present-state predictor is absolutely adequate on held-out biological groups;
2. older H has stable, calibrated incremental value;
3. a branch measurement chosen without future-label leakage is added;
4. adequate future prediction is maintained/improved while H increment collapses;
5. the result survives the declared intervention family.

If richer local/relational present features remove H without a discrete branch variable, the topological-branch explanation is unnecessary for that task. If H persists after strong present measurements and branch candidates, other explanations remain, including true path dependence.

## Program impact
T4 gave the connected-fiber sufficient condition. T5 identifies the global obstruction when connectedness fails and turns it into an experiment-design target: **measure or perturb to distinguish future-distinct components of the same current-measurement fiber.**

T5_COMPLETE
