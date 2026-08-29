# Evidence desk addendum — Refahi replication reconciliation

Date: 2026-08-29

NotebookLM was given the new direct-source FM1 replication results and asked to reconcile them against its 18-source notebook. The synthesis generated several useful design implications, but also produced new overclaims. This addendum records what the lab accepts and rejects.

## Accepted from the reconciliation

1. **The broad screening-off language must be retired.** Completion is indexed by developmental time, biological compartment, future target, measurement interface, model class and finite-sample resolution.
2. **Atlas imputation/mapping is a material confound.** The released FM1 expression channels are manually integrated spatial annotations, not repeated 25-gene measurements in the exact same cells. A prospective study should directly measure its primary state channels in the same specimen.
3. **Pooling heterogeneous cell strata can manufacture residual history.** The late pooled Ridge signal is not reproduced within stable L1/L2/deeper strata; compartment-specific analysis should be primary.
4. **Estimator disagreement must be disclosed.** Ridge and ExtraTrees disagree in pooled cases. This is evidence that the state/estimator pair is unresolved, not a reason to select whichever model supports the preferred narrative.
5. **Null calibration is insufficient without power calibration.** A no-history conclusion is only meaningful relative to a known-incomplete alternative of biologically meaningful magnitude.
6. **NSF framing should emphasize operational, information-bounded state mapping and falsification**, not a universal hidden biological state or a new definition of Markovity.

## Rejected / downgraded NotebookLM interpretations

### “Early flower development is structurally non-Markovian” — rejected

The early pooled Ridge history gain establishes that **the tested current representation + Ridge model is incomplete for the future-growth task**. It does not establish intrinsic non-Markov biology. Missing current variables, spatial mixture, measurement error or model misspecification can all generate residual history.

### “Late L1 demonstrates complete predictive screening-off” — too strong

The result supports **no detectable added value from the tested older atlas state under the tested models and calibration**. It cannot exclude weaker history effects, unmeasured history variables, different future targets, or new intervention families.

### “Late L1 is explained by canalization/manifold collapse” — hypothesis only

Canalization is biologically plausible and consistent with developmental literature, but the replication did not directly measure a manifold-rank collapse or a causal canalization mechanism. It should be proposed as a testable explanation, not reported as the result.

### “The observation stack spans the future-growth Jacobian row space” — not established

That is a local mathematical sufficiency condition, not something measured by the Refahi regression. No Jacobian/rank certificate was computed in this audit.

### “99% power proves the late-L1 result is real” — rejected wording

The matched calibration shows 99% power **for the particular simulated 0.20-target-SD direct history effect**. It strengthens the interpretation relative to that effect size; it is not proof that all biologically meaningful memory is absent.

## Public-language rule after reconciliation

Use:

> In the late FM1 L1 epidermal growth task, current geometry plus the released atlas expression state predicts descendant growth well, while the tested older atlas state adds no reproducible predictive value under Ridge and ExtraTrees. The conclusion is task-, compartment-, measurement- and estimator-specific and is not a proof of biological Markovity.

Do not use:

- “plants become Markovian”;
- “we proved the past no longer matters”;
- “late development has no memory”;
- “the 25-gene state is the true biological state”;
- “the result proves canalization”;
- “the atlas state completely determines the future.”

## Preregistration consequences

The RCOg-V preregistration now requires:

- prospectively fixed tissue/stage strata;
- same-specimen current-state measurements for primary molecular channels;
- prespecified linear and nonlinear estimator classes;
- estimator-disagreement classified as unresolved;
- matched known-complete and known-incomplete calibration before unblinding;
- no claim of completion when power for the preregistered residual-history effect is inadequate.
