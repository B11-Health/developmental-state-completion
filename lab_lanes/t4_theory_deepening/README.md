# T4 — Adversarial State-Sufficiency Theory Deepening

Date: 2026-08-30

This lane strengthens the theory by separating what is genuinely implied from what is only tempting rhetoric. The central result is a hierarchy of task-specific predictive sufficiency notions, a connected-fiber factorization theorem with the assumptions needed to make the local kernel condition global, and executable counterexamples showing why observational screening-off, finite horizon, local rank conditions, and robust submodularity cannot be overgeneralized.

## Files
- `THEORY_HIERARCHY.md` — exact/approximate, observational/interventional, finite/all-horizon, predictive/mechanistic hierarchy and implications.
- `THEOREMS_AND_COUNTEREXAMPLES.md` — proved statements and frozen non-implications.
- `PRIOR_ART_AND_NOVELTY_MATRIX.md` — primary-literature map and explicit no-priority boundaries.
- `FALSIFICATION_MAP.md` — what kills a scoped claim, an experimental-design claim, or the broader program.
- `REVIEWER_RED_TEAM.md` — strongest skeptical objections and required responses.
- `t4_counterexamples.py` / `t4_results.json` — dependency-free finite witnesses.
- `literature_search.py` / `literature_search_raw.json` — OpenAlex search across 16 prior-art areas.
- `literature_exact_search.py` / `literature_exact_search_raw.json` — targeted bibliographic search supplement.

## Frozen headline
The mathematically defensible object is a **task- and intervention-indexed predictive quotient**, not a universal biological state. A local condition `ker Dh_x subseteq ker DF_x` becomes a global factorization only with additional regularity such as connected fibers. Observational screening-off does not transfer to interventions: the exact finite witness changes `I(Y;H|S)` from 0 bits observationally to 1 bit under intervention.

## Scientific target
The highest-value empirical target is a closed loop: demonstrate calibrated residual history under a coarse present, prospectively choose extra measurement/perturbation from unresolved ambiguity, and show on held-out groups that the residual history increment falls under the richer present while strong baselines and burden controls fail to explain the improvement.

No universal Markovity, one-dimensional biology, mathematical priority, or completed living validation is claimed.
