# T6A Independent Adversarial Audit

Date: 2026-08-30
Branch base: local `main` at `d14951c48935d9237e7524fda6eb5ffbd33211ab`
Scope: independent verification of `lab_lanes/t6_topological_measurement_dimension`; no priority claim.

## Executive verdict

T6's main mathematical claims are correct. I found no counterexample to T6.1--T6.4 or the equivariant-map equivalence in T6.5. Two qualifications should be made before publication-level use:

1. **T6.3 is stronger than necessary in its hypotheses.** Connectedness of the base is not needed for the rank-order proof: a fiberwise-injective real scalar globally labels the sheets by rank over an arbitrary base, so the finite cover is trivial componentwise and in fact globally isomorphic to the product cover `M x {0,...,d-1}`.
2. **The Stiefel--Whitney obstruction needs ordinary vector-bundle hypotheses to be stated cleanly.** For a paracompact Hausdorff base (in particular a CW complex or manifold), the double cover defines the associated line bundle in the standard numerable-vector-bundle setting, a nowhere-zero section of `L^{oplus k}` forces `w_k=0`, and the Whitney product formula gives `w_k(L^{oplus k})=w_1(L)^k`. T6 currently omits this mild topological niceness assumption.

A separate novelty correction is important: the pre-existing **projected embedding / k-prem** literature studies exactly maps `f:N->M` for which some `g:N->R^k` makes `(f,g)` an embedding. For a finite covering and a future map that distinguishes every point in each fiber, this is essentially T6's full-sheet Euclidean completion problem. T6 should therefore be framed as a project-specific translation/synthesis, not as introducing the underlying topological problem.

## Audit matrix

| Claim | Verdict | Independent adversarial result | Required correction / qualification |
|---|---|---|---|
| T6 definition of `cdim_R(h,F)` | PASS | Well-defined as a task-relative minimum over nonnegative integers when a finite-dimensional augmentation exists; examples used all have explicit upper bounds. | If used for arbitrary spaces, allow value `+infinity` when no finite `k` exists. |
| (1) `cdim_R(S^n->RP^n,F=id)=n+1`, `n>=1` | PASS | Sufficiency forces antipodal separation. If `k<=n`, compose `B:S^n->R^k` with the coordinate inclusion `R^k -> R^n`; Borsuk--Ulam gives an antipodal collision. Identity inclusion into `R^(n+1)` attains the bound. | Say “pad with `n-k` zero coordinates” rather than merely “pad with zero coordinates” for maximal precision. |
| (1) edge case `n=0` | PASS | `S^0` has two points over the single point `RP^0`; `R^0` is a singleton and cannot separate them, while `x |-> x in R` does. | None. |
| (2) one real channel impossible for `z|->z^2` | PASS | For continuous `B:S^1->R`, `D(z)=B(z)-B(-z)` is continuous and odd. On any antipodal half-turn, `D(-z)=-D(z)`, so IVT forces a zero unless already zero. | None. This is the `n=1` Borsuk--Ulam case but the elementary proof is sound. |
| (2) two real channels suffice | PASS | `B(z)=(Re z,Im z)` is injective on the whole circle, hence certainly on each two-point fiber. | None. |
| Local branch labels need not globalize | PASS | A connected total space admits no nonconstant map to a discrete two-point set. For the circle double cover the nontrivial monodromy swaps sheets. | Keep wording tied to connected `E`; a disconnected trivial double cover does admit a global discrete label. |
| (3) fiber-injective scalar trivializes finite cover | PASS | Rank of `B` within each finite fiber is locally constant in every evenly-covered neighborhood. Rank strata are open, disjoint, exhaust `E`, meet each fiber once, and each restriction is a bijective local homeomorphism over `M`, hence a homeomorphism. | **Connectedness of `M` is unnecessary.** The theorem can be strengthened. No Hausdorff, path-connected, semilocally simply-connected, or monodromy-classification hypothesis is needed for this direct proof. |
| Monodromy explanation for (3) | NEEDS QUALIFICATION | Correct intuition on path-connected components under standard covering-space monodromy language. | Do not make monodromy classification carry the proof unless standard local path-connectedness hypotheses are stated. The rank proof is hypothesis-minimal and should remain primary. |
| Degree-`d` circle cover has full-sheet `cdim_R=2` for `d>=2` | PASS | Scalar impossible by T6.3 because the cover is connected/nontrivial; planar identity coordinate separates all roots in every fiber. | “Connected/nontrivial” can be justified directly; no issue with large `d`. |
| (4) configuration-space pullback iff criterion | PASS | A fiberwise-injective `B` gives the unordered configuration `Phi(m)=B(p^{-1}(m))`; in an evenly-covered neighborhood this is the quotient of `d` continuous distinct branches, proving continuity. Conversely the marked point in the pulled-back configuration is the required `B`. The canonical identification is a local homeomorphism/bijection over the base. | Define `UConf_d(R^k)=F_d(R^k)/Sigma_d` with quotient topology. For `k=0,d>1` it is empty, correctly implying nonexistence. |
| `k=1` configuration consequence | PASS | Every unordered configuration of `d` real points has a canonical increasing ordering, so the marked-point cover splits into rank sheets. | None. |
| `k=2` braid statement | PASS | Standard: unordered planar configuration spaces support nontrivial braids/permutations without collisions. | It is explanatory, not needed for theorem proof. |
| `k>=3` “monodromy alone not complete” warning | PASS | Safe and conservative. Higher obstruction data can matter for maps from higher-dimensional bases even when fundamental-group behavior is simple. | Avoid implying a specific complete obstruction theory unless cited. |
| (5) pair separation iff `Z2`-equivariant `E->S^(k-1)` | PASS | From `B`, odd difference `D(e)=B(e)-B(tau e)` is nonzero and normalizes equivariantly. Conversely an equivariant sphere map itself is a separating `R^k`-valued `B`. | For `k=0`, `S^{-1}` convention is awkward; state theorem for `k>=1`. |
| Equivalence with nowhere-zero section of `L^{oplus k}` | PASS | Standard associated-bundle correspondence between equivariant maps to the sign representation and sections. | State base in the standard vector-bundle category (e.g. paracompact Hausdorff) if characteristic classes are invoked next. |
| `w_1(L)^k` necessary obstruction | NEEDS QUALIFICATION | Under standard bundle hypotheses, a nowhere-zero section of a rank-`k` bundle forces top Stiefel--Whitney class to vanish; Whitney product gives `w(L^{oplus k})=(1+w_1(L))^k`, so top term is `w_1(L)^k`. | Add a niceness assumption such as paracompact Hausdorff/CW/manifold. Continue to state vanishing as necessary, not sufficient. |
| Projective-space characteristic-class recovery | PASS | For tautological line bundle over `RP^n`, `H^*(RP^n;F_2)=F_2[a]/(a^{n+1})`, `a=w_1(L)`, so `a^k !=0` for `1<=k<=n`; `k=n+1` is achieved explicitly. | None beyond the preceding bundle-category qualification. |
| (6) one branch bit vs `n+1` real channels | PASS | Two future-distinct states per fiber need one fixed-length binary bit set-theoretically, but continuous Euclidean realization can require `n+1` coordinates. | Make explicit that “bit cost” assumes discrete exact labels; it is not information capacity of a finite-precision real sensor. |
| (6) degree 8: 3 bits vs 2 real channels | PASS | Eight exact discrete labels need `ceil(log2 8)=3` bits while the circle embeds in `R^2`, separating all 8 points per fiber. | This demonstrates incomparability of these accounting notions, not that two reals contain “less information” than three bits. |
| Decoder continuity on compact domain | PASS | Continuous surjection from compact `X` to the Hausdorff image `(h,B)(X)` is quotient; a fiber-constant continuous `F` descends continuously. | `Y` need not be Hausdorff for the quotient-factor continuity argument; T6's stated hypothesis is stronger than necessary but harmless. |

## Independent proofs and edge-case checks

### A. Exact projective-space completion dimension

Let `q:S^n->RP^n` and `F(x)=x`. If `(q,B)` is sufficient, then for every `x`, the two points `x,-x` share the same `q`-value but have distinct `F`-values, so `B(x)!=B(-x)`.

For `1<=k<=n`, let `i:R^k->R^n` be `i(y)=(y,0,...,0)`. Borsuk--Ulam applied to `i o B:S^n->R^n` yields `x` with `iB(x)=iB(-x)`. Since `i` is injective, `B(x)=B(-x)`, contradiction. Thus `k>=n+1`. Taking `B(x)=x` gives `k=n+1`.

For `n=0`, the argument is finite: `R^0` is one point and cannot separate the two points of `S^0`; `R` can. Thus the formula is exactly `n+1` for all `n>=0`.

No smoothness is needed for this dimension statement; continuity alone suffices. The local-differential observation for `n>=1` is separately correct because the quotient is a local diffeomorphism.

### B. Circle scalar obstruction

For `p(z)=z^2`, each fiber is `{z,-z}`. If `B:S^1->R` separated every fiber, define `D(z)=B(z)-B(-z)`. Then `D(-z)=-D(z)`. Choose any `z`. If `D(z)=0`, separation already fails. Otherwise `D(z)` and `D(-z)` have opposite signs. Along either semicircular path from `z` to `-z`, continuity and IVT force a zero. Contradiction.

The planar map `z|->(Re z,Im z)` is injective, so two coordinates suffice. Hence exact dimension `2`.

### C. Scalar order trivializes any finite cover

Let `p:E->M` be a finite `d`-sheet cover and `B:E->R` be fiberwise injective. For each `e`, set

`r(e)=#{e' in p^{-1}(p(e)): B(e')<B(e)}`.

Take an evenly covered neighborhood `U` of `m=p(e)` with sheets `s_1,...,s_d:U->E`. The functions `b_i=B o s_i` are continuous and pairwise unequal at every point of `U`. Around a given point, all finitely many signs `b_i-b_j` remain unchanged after shrinking `U`, so the rank of each branch is constant there. Therefore `r:E->{0,...,d-1}` is locally constant.

For each `j`, `E_j=r^{-1}(j)` is open (and its complement, a finite union of other rank strata, is open), so it is also closed. Every fiber contains exactly one point of rank `j`, hence `p|E_j:E_j->M` is bijective. It is a local homeomorphism because it is the restriction of a covering map to one local sheet. A bijective local homeomorphism is a homeomorphism. Thus

`E = disjoint union_j E_j ~= M x {0,...,d-1}`

over `M`.

This proof uses only the covering local-triviality axiom, finiteness of the fiber, continuity of `B`, and the linear order on `R`. **Connectedness is not used.**

### D. Configuration-space pullback criterion

Let `F_d(R^k)={(x_1,...,x_d):x_i!=x_j}` and `UConf_d(R^k)=F_d(R^k)/Sigma_d`. The marked-point cover is

`T_d={(Q,q):Q in UConf_d(R^k), q in Q}->UConf_d(R^k)`.

If `B:E->R^k` is fiberwise injective, define `Phi(m)=B(p^{-1}(m))`. In an evenly-covered neighborhood `U`, choose local sections `s_i`. Then `u|->(B(s_1(u)),...,B(s_d(u)))` is a continuous map to ordered configuration space; composing with the finite permutation quotient proves local, hence global, continuity of `Phi`. Map

`e |-> (p(e), (Phi(p(e)),B(e)))`

into the pullback. Locally this identifies each covering sheet with the corresponding marked branch; hence it is a covering isomorphism.

Conversely, on the pullback define `B(m,Q,q)=q`. Distinct marked points over the same `(m,Q)` have distinct Euclidean coordinates. This proves the iff criterion without classification theory.

### E. Double covers and characteristic classes

For a double cover with involution `tau`, separation by `B:E->R^k` gives the nonzero odd vector

`D(e)=B(e)-B(tau e)`.

Normalization gives an equivariant `v:E->S^{k-1}`. Conversely `B=v` separates because `v(tau e)=-v(e)` and a unit vector never equals its negative. This equivalence is exact for `k>=1`.

For a sufficiently nice base, an equivariant map to the sign representation sphere is the same as a nowhere-zero section of `L^{oplus k}`. A nonzero section splits off a trivial line subbundle after choosing a bundle metric; therefore the top Stiefel--Whitney class vanishes. The Whitney product formula gives

`w(L^{oplus k})=w(L)^k=(1+a)^k`, `a=w_1(L)`,

whose degree-`k` term is `a^k`. Hence `a^k!=0` forbids separation by `k` real coordinates.

For `RP^n`, `a^k` is nonzero exactly through degree `n`, recovering the Borsuk--Ulam lower bound.

## Search for pre-existing equivalents / novelty boundary

The audit searched the isolated research browser for classical and modern formulations. The strongest overlap found is the projected-embedding literature:

- P. M. Akhmetiev and S. A. Melikhov, **Projected and near-projected embeddings** (arXiv:1711.03520; later published). Their terminology calls `f:N->M` a `k`-prem when there is a map `g:N->R^k` such that `(f,g):N->M x R^k` is an embedding.
- S. A. Melikhov, **Transverse fundamental group and projected embeddings** (arXiv:1505.00505), explicitly treats covering maps among the motivating cases.

For a finite covering `p:E->M`, if `B` is injective on every fiber then `(p,B)` is injective; because `p` is locally a homeomorphism, `(p,B)` is locally an embedding, and in standard Hausdorff settings this is exactly the vertical/fiberwise embedding viewpoint. Therefore the full-sheet version of T6's minimization is not a newly discovered topology problem.

Classical ingredients independently located:

- Karol Borsuk, *Drei Saetze ueber die n-dimensionale euklidische Sphaere*, Fundamenta Mathematicae 20 (1933), 177--190, DOI 10.4064/fm-20-1-177-190.
- Edward Fadell and Lee Neuwirth, *Configuration Spaces*, Mathematica Scandinavica 10 (1962), 111--118, DOI 10.7146/math.scand.a-10517. Publisher record located through Mathematical Sciences Publishers / journal index.
- Allen Hatcher, *Algebraic Topology*, covering-space chapters: standard source for covering maps, lifting, and monodromy/classification under the usual hypotheses.
- John Milnor and James Stasheff, *Characteristic Classes* (1974), and standard vector-bundle texts such as Hatcher's *Vector Bundles and K-Theory*, for Whitney product and Stiefel--Whitney obstruction machinery.
- Edward Fadell and Sufian Husseini, *An ideal-valued cohomological index theory with applications to Borsuk-Ulam and Bourgin-Yang theorems* (1988), for broader equivariant/cohomological obstruction language.

I did **not** find evidence supporting a priority claim for the configuration pullback criterion, the scalar-order obstruction, the equivariant normalization trick, or the projective-space dimension computation. All should be presented as standard or straightforward consequences of established topology.

## Safe novelty statement

> The topology in T6 is an application and synthesis of established covering-space, configuration-space, Borsuk--Ulam/equivariant, characteristic-class, and projected-embedding ideas. The repository-specific contribution is to formulate the **task-relative continuous state-completion question** after T4/T5: a small set-theoretic branch code for future-distinct fiber components need not admit a globally continuous low-dimensional Euclidean measurement realization. No claim is made that the underlying topological obstructions, fiberwise-embedding problem, or Euclidean lift dimension are new.

## Recommended edits to T6 before external use

1. Extend `cdim_R` to `N union {+infinity}` for arbitrary inputs, or explicitly restrict to cases with a finite-dimensional witness.
2. Strengthen T6.3 by deleting “where `M` is connected”; retain connectedness only in the corollary “if `E` is connected and `d>=2`, no scalar exists.”
3. State T6.5 for `k>=1`.
4. Before the Stiefel--Whitney corollary, assume `M` is paracompact Hausdorff (or simply a CW complex/manifold in project applications).
5. Add projected-embedding / `k`-prem literature to PRIOR_ART and explicitly say that full-sheet `cdim_R` for covers is a task-relative variant of a known vertical embedding problem.
6. Clarify that the bit comparisons concern exact discrete labels, not finite-precision information capacity of real-valued sensors.
7. Optionally remove the unnecessary “`Y` Hausdorff” assumption from the compact-domain quotient decoder paragraph.

## Final audit decision

**PASS WITH QUALIFICATIONS.** No central theorem failed. The corrections are hypothesis/novelty-boundary tightening, not reversals of the main T6 conclusion.
