# T6 Checkpoint — 2026-08-30

Status: COMPLETE LOCALLY; NO PUSH; NO PUBLICATION.

## Starting point
- Parent branch/worktree: local `main`.
- Starting commit: `ea00b47` (`Complete R7 relational adequacy rescue`).
- T6 branch: `lab-t6-topological-measurement-dimension-2026-08-30`.
- Isolated worktree: `C:/Users/codeg/mcp-shell-auth/workspace/developmental-state-completion-t6`.

## What was established
1. **Exact antipodal dimension theorem.** For `h:S^n->RP^n`, `F(x)=x`, the minimum continuous Euclidean augmentation dimension is exactly `n+1`. Borsuk-Ulam excludes all `k<=n`; `B(x)=x` achieves `n+1`. The `n=0` edge case also gives `1` by direct inspection.
2. **Circle double-cover theorem.** For `z->z^2`, one real scalar cannot separate all antipodal pairs, while two real channels `(Re z, Im z)` can. Local discrete sheet labels exist but cannot be globally continuous on connected `S^1`.
3. **General finite-cover scalar obstruction.** A real-valued map injective on each fiber of a finite cover globally orders the sheets. The fiberwise rank is locally constant, producing global sections and forcing the cover to be trivial. Thus every nontrivial connected finite cover needs at least two real channels for full sheet separation.
4. **Configuration-space criterion.** Fiberwise `R^k` sheet coordinates are equivalent to realizing the cover as a pullback of the canonical marked-point cover over unordered configurations in `R^k`.
5. **Double-cover equivariant formulation.** Pair separation in `R^k` is equivalent to a `Z2`-equivariant map to `S^(k-1)`. A nonzero `w_1(L)^k` is therefore a characteristic-class obstruction. For the antipodal projective cover this recovers the `k<=n` impossibility.
6. **Complexity separation.** Set-theoretic branch bits, continuous Euclidean measurement dimension, arbitrary-codomain topological dimension, and whole-state embedding dimension are explicitly distinguished.

## Strong counterexamples / comparisons
- `S^n->RP^n`: one set-theoretic bit versus `n+1` continuous real channels, an unbounded gap.
- Degree-8 circle cover: three set-theoretic bits for full sheet identity versus two continuous real channels, so bit count can also exceed Euclidean channel count.
- `S^1` double cover: one real scalar fails, but one circle-valued observable succeeds, proving codomain sensitivity.

## Prior-art boundary
The lane treats the following as established mathematics, not discoveries:
- Borsuk-Ulam (Borsuk 1933);
- covering-space monodromy;
- configuration spaces (Fadell-Neuwirth 1962);
- equivariant/cohomological Borsuk-Ulam machinery (Fadell-Husseini 1988);
- characteristic classes (Milnor-Stasheff);
- Reeb/fiber-component quotients;
- local/global nonlinear observability distinctions (Hermann-Krener 1977);
- Euclidean embedding theory (Whitney).

The project-specific contribution is the synthesis of these ideas with T4/T5's predictive-state-completion framework. No priority claim is made.

## Executable verification
`test_t6_topology.py` passed all four regression checks:
- sampled scalar antipodal sign-change witnesses;
- exact planar antipodal margin `2`;
- degree-2 monodromy sheet swap;
- degree-8 comparison: 3 bits versus 2 continuous real channels.

These computations illustrate the theorems; they do not replace the exact proofs.

## Empirical implication
A binary latent branch does **not** imply that one continuous biomarker can globally complete state. The appropriate experimental alternatives include multi-channel present measurements, local/charted biomarkers, explicitly discontinuous branch classifiers, non-Euclidean observables, or perturbation-assisted disambiguation.

## Completion gate
Before completion, T6 requires:
- executable tests passing;
- reviewer red-team present;
- prior-art and empirical-implication documents present;
- local commit created;
- `git status` clean;
- HEAD moved from `ea00b47`.
