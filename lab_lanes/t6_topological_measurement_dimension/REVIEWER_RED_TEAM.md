# T6 Reviewer Red Team

Date: 2026-08-30

## Claim 1: "Two branch states require one bit, so one continuous scalar should suffice."
**Failure:** bit count is set-theoretic; a continuous scalar imposes a global order on every finite fiber. Nontrivial monodromy prevents that order from being globally consistent. The antipodal sphere family makes the gap arbitrarily large: one bit versus `n+1` real channels.

## Claim 2: "Borsuk-Ulam only says maps to R^n collide; perhaps R^k with k<n avoids it."
**Failure:** append zero coordinates to map `R^k` into `R^n`. A collision in the padded map is a collision in the original map. Thus every `k<=n` is ruled out.

## Claim 3: "Maybe the lower bound is n, not n+1."
**Failure:** Borsuk-Ulam rules out `k=n`; `B(x)=x` provides an explicit solution in `R^(n+1)`. Therefore the minimum is exactly `n+1`.

## Claim 4: "The result starts only at n>=1, so S^0 is an exception."
**Resolution:** the formula still holds at `n=0`: the base is a point, `R^0` cannot distinguish two points, and one real coordinate can. State this separately rather than invoking Borsuk-Ulam unnecessarily.

## Claim 5: "One-dimensional sensors always fail on the circle double cover."
**Overstatement:** one **real-valued** scalar fails. A circle-valued sensor `B(z)=z` works. The theorem is codomain-sensitive.

## Claim 6: "No scalar can separate a nontrivial finite cover because the total space is connected."
**Incomplete reasoning:** connectedness alone only rules out continuous maps into a discrete label set. A real-valued scalar has connected codomain and needs the stronger fiber-order argument. The proof in THEOREMS.md uses locally constant rank and shows such a scalar would trivialize the cover.

## Claim 7: "Nontrivial monodromy forces at least two real channels for every finite cover, and two always suffice."
**First half:** for full sheet separation, yes: T6.3 rules out one scalar on any nontrivial connected finite cover.
**Second half:** not established in arbitrary bases. Circle covers embed fiberwise in the plane, but general finite covers can have additional configuration-space or characteristic-class obstructions. T6 makes no universal two-channel theorem.

## Claim 8: "w1(L)^k=0 is equivalent to existence of k channels for a double cover."
**Too strong:** nonvanishing gives a valid obstruction; vanishing of the top Stiefel-Whitney class is not claimed sufficient for arbitrary bases. The exact condition used is existence of a `Z2`-equivariant map to `S^(k-1)`.

## Claim 9: "The augmentation must embed the whole latent manifold."
**False:** it only needs to separate collisions of `h` that are future-distinct. If `h` is already sufficient, zero extra dimensions are needed even for a high-dimensional state manifold.

## Claim 10: "ker Dh=0 means h is globally sufficient."
**False:** it means h is locally immersive/local-diffeomorphic in the covering examples. Global sheet collisions survive. `S^n->RP^n` is the clean counterexample.

## Claim 11: "The numerical tests prove Borsuk-Ulam."
**False:** the scripts are witnesses and regression tests only. Exact proofs live in THEOREMS.md and depend on established topology.

## Claim 12: "This proves biology has nontrivial monodromy."
**False:** the topology is conditional on the modeled state/measurement geometry. Empirical work would need to establish a robust loop/branch structure and adequate prediction first. The correct scientific conclusion is a design warning, not a biological diagnosis.

## Claim 13: "History residuals imply a topological branch."
**False:** residual history can come from model inadequacy, noise, batch effects, missing continuous state, or genuine path dependence. T6 only says topology is one possible obstruction to a globally continuous present-state completion.

## Claim 14: "The T6 synthesis is mathematically novel."
**Unsupported:** Borsuk-Ulam, monodromy, configuration spaces, characteristic classes, Reeb quotients, and local/global observability are established. No priority claim is made. Any publication should describe the novelty, if any, as application/synthesis unless a deeper specialist search establishes otherwise.
