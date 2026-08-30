# T6 Theorems: Topological Measurement-Dimension Obstructions

Date: 2026-08-30
Status: mathematical development and synthesis; no priority claim.

## 1. Setup and three different complexity notions
Let `X` be a state space, `h:X->S` a declared present measurement, and `F:X->Y` a declared future-response map. A continuous Euclidean augmentation of dimension `k` is a continuous map `B:X->R^k` such that

`h(x)=h(x') and B(x)=B(x')  ==>  F(x)=F(x')`.

Equivalently, `F` factors set-theoretically through `(h,B)`. Define

`cdim_R(h,F) = min { k : such a continuous B:X->R^k exists }`.

This quantity is not the same as either:

1. the T5 set-theoretic branch-code cost `ceil(log2 m)` bits for `m` future-distinct component classes in a fiber; or
2. the Euclidean embedding dimension of `X`.

A real channel can encode arbitrarily many discrete labels when topology permits, while topology can also force many real channels even when each fiber has only two future-distinct states.

### Decoder continuity on compact domains
If `X` is compact, `(h,B)` is continuous into a Hausdorff space, and `F` is continuous and constant on fibers of `(h,B)`, then the induced decoder `G:(h,B)(X)->Y` is continuous whenever `Y` is Hausdorff. Indeed, the surjection `X->(h,B)(X)` is a quotient map because it is a continuous map from compact to Hausdorff. Thus the sphere examples below obstruct not only a continuous sensor with an arbitrary decoder, but also a continuous sensor with a continuous decoder on the realized measurement image.

## 2. Antipodal projective-space obstruction
Let

`h:S^n -> RP^n`, `h(x)=[x]`,

be the antipodal quotient, and let `F:S^n->R^(n+1)` be the identity inclusion `F(x)=x`.

For `n>=1`, `h` is a smooth two-sheeted covering map and a local diffeomorphism. Hence `Dh_x` is an isomorphism and

`ker Dh_x = {0} subset ker DF_x`

for every `x`. Thus the T4/T5 differential condition is maximally satisfied locally, while the two points of each fiber remain future-distinct under `F`.

### Theorem T6.1 (exact Euclidean completion dimension)
For every integer `n>=1`,

`cdim_R(h,F) = n+1`.

#### Proof
Suppose `B:S^n->R^k` is continuous and sufficient for `F`. Since `h(x)=h(-x)` but `F(x)!=F(-x)`, sufficiency forces

`B(x)!=B(-x)` for every `x in S^n`.

If `k<=n`, pad `B` with zero coordinates to obtain a continuous map `Btilde:S^n->R^n`. The Borsuk-Ulam theorem gives some `x` with

`Btilde(x)=Btilde(-x)`,

hence `B(x)=B(-x)`, contradiction. Therefore `k>=n+1`.

For achievability, take `B(x)=x in R^(n+1)`. Then `B(x)!=B(-x)` for all `x`, and indeed `F=B`; hence `(h,B)` is sufficient. Therefore the lower and upper bounds agree. QED.

### Edge case n=0
`S^0={-1,+1}` and `RP^0` is a point. A zero-dimensional Euclidean augmentation `R^0` is constant and cannot distinguish the two states, while `B(x)=x in R` does. Thus the same numerical formula holds:

`cdim_R(h,F)=1=n+1`.

Borsuk-Ulam is not needed for this zero-dimensional case.

### Corollary T6.1a (arbitrarily large gap from one branch bit)
Every fiber of `S^n->RP^n` has exactly two points, so T5's set-theoretic branch code needs only one bit. Nevertheless the minimum number of continuous real-valued channels is `n+1`, which is unbounded with `n`.

This is the central T6 obstruction: **binary latent branching does not imply one globally continuous real biomarker can complete the state.**

## 3. The circle double cover
Identify `S^1` with unit complex numbers. The map

`p:S^1->S^1`, `p(z)=z^2`,

is equivalent to `S^1->RP^1` after the standard homeomorphism `RP^1 ~= S^1`.

### Theorem T6.2 (one scalar fails, two channels suffice)
Let `F(z)=z` viewed in `R^2`. Then no continuous scalar `B:S^1->R` can make `(p,B)` sufficient for `F`, while `B(z)=(Re z, Im z)` does. Hence

`cdim_R(p,F)=2`.

#### Elementary scalar proof
Write `z=e^(i theta)` and define

`D(theta)=B(e^(i theta))-B(-e^(i theta))`.

Then `D(theta+pi)=-D(theta)`. If `D(theta0)>0`, then `D(theta0+pi)<0`; if it is negative the signs reverse. By the intermediate value theorem, some `theta` has `D(theta)=0`, so `B(z)=B(-z)`. If `D` is ever zero already, the conclusion is immediate. Thus one scalar fails.

Two channels suffice by the standard embedding `z -> (Re z, Im z)`, whose antipodal values differ by Euclidean distance `2`.

### Local branch labels versus global branch labels
Every covering is locally trivial. On a sufficiently small arc `U` in the base, `p^-1(U)` splits into two disjoint sheets, and one may assign locally constant labels `0` and `1` to the two sheets. But `S^1` is connected, so every globally continuous map `S^1->{0,1}` into a discrete two-point space is constant. The local labels cannot be glued globally without a cut/discontinuity. This is the simplest monodromy manifestation.

### Codomain warning
The statement is specifically about **real Euclidean channels**. A single circle-valued channel `B:S^1->S^1`, for example `B(z)=z`, separates antipodes. Thus `cdim_R=2` does not mean every one-dimensional topological sensor codomain fails. Euclidean channel count, covering dimension of an arbitrary codomain, and bit count must not be conflated.

## 4. Scalar obstruction for every nontrivial finite cover
The circle phenomenon is not special to antipodes.

### Theorem T6.3 (a fiber-separating real scalar trivializes a finite cover)
Let `p:E->M` be a `d`-sheeted covering with `d>=2`, where `M` is connected. Suppose there is a continuous map `B:E->R` that is injective on every fiber `p^-1(m)`. Then the covering is trivial: `E` is the disjoint union of `d` open-and-closed subspaces, each mapped homeomorphically onto `M` by `p`.

Consequently, if `E` is connected and `d>=2`, no such scalar `B` exists.

#### Proof
For `e in E`, define its fiberwise rank

`r(e) = # { e' in p^-1(p(e)) : B(e') < B(e) }`,

so `r(e)` lies in `{0,...,d-1}`. Because the `d` values of `B` on each fiber are distinct, and because a covering has local sheet trivializations, their strict order cannot change under a sufficiently small movement in the base without two values becoming equal. Therefore `r` is locally constant on `E`.

For each rank `j`, let `E_j={e:r(e)=j}`. The sets `E_j` are open and closed, each fiber contains exactly one point of each rank, and `p|E_j:E_j->M` is a one-sheeted covering, hence a homeomorphism. Thus `E` is the disjoint union of `d` global sections and the cover is trivial. QED.

### Monodromy interpretation
A scalar imposes a total order on every fiber. Continuous transport around a loop cannot change that order without a collision. Therefore the monodromy permutation around every loop must preserve every rank, hence must be the identity. Nontrivial monodromy is a global obstruction to a one-real-channel sheet code.

### Corollary T6.3a (connected circle covers)
For the connected degree-`d` circle cover `p_d:S^1->S^1`, `p_d(z)=z^d`, `d>=2`, any future map that distinguishes all `d` points in each fiber cannot be completed by one real scalar. Two real channels suffice using `B(z)=(Re z,Im z)`. Hence its full sheet-separation Euclidean completion dimension is exactly `2`, independent of `d`.

This also shows that numerical bit count and Euclidean dimension are not ordered quantities: for `d=8`, a set-theoretic code needs at least three bits, yet two continuous real channels suffice.

## 5. Configuration-space characterization of finite-cover realizability
Let `UConf_d(R^k)` be the unordered configuration space of `d` distinct points in `R^k`, and let

`T_d(R^k) = { (Q,q) : Q in UConf_d(R^k), q in Q } -> UConf_d(R^k)`

be the canonical `d`-sheeted cover that marks one point of a configuration.

### Theorem T6.4 (configuration-space pullback criterion)
A `d`-sheeted covering `p:E->M` admits a continuous `B:E->R^k` that is injective on every fiber if and only if `p` is isomorphic, as a covering over `M`, to the pullback of `T_d(R^k)` along some continuous map

`Phi:M->UConf_d(R^k)`.

#### Proof
If `B` is fiberwise injective, define

`Phi(m) = { B(e) : e in p^-1(m) }`.

Local covering trivializations and continuity of `B` make `Phi` continuous into the unordered configuration space. The map

`e -> (p(e), Phi(p(e)), B(e))`

identifies `E` with the pullback of the marked-point cover.

Conversely, in a pullback point `(m,Q,q)`, define `B(m,Q,q)=q`. This is continuous and takes distinct values on the `d` points over each `m`. QED.

### Consequences
- For `k=1`, unordered configurations have a unique increasing order; the canonical marked-point cover splits into `d` rank components. T6.3 follows.
- For `k=2`, loops in configuration space are governed by braid phenomena; nontrivial sheet permutations can occur without point collisions.
- For `k>=3`, ordered configuration spaces of Euclidean space are much less constrained at the fundamental-group level, but finite-`k` realizability over higher-dimensional bases can still involve higher topological obstructions. Monodromy alone should therefore be treated as a necessary organizing invariant, not automatically as a complete finite-dimensional criterion in all bases.

This theorem is a repackaging of standard covering/configuration-space machinery, not a new topology theorem.

## 6. Double covers, equivariant maps, and characteristic-class obstruction
Let `p:E->M` be a double cover with deck involution `tau`, and let `L=E x_{Z2} R_sign` be its associated real line bundle.

### Theorem T6.5 (pair separation equals an equivariant sphere map)
There exists a continuous `B:E->R^k` with

`B(e) != B(tau e)` for every `e`

if and only if there exists a `Z2`-equivariant map

`v:E->S^(k-1)`, with `v(tau e)=-v(e)`.

#### Proof
Given `B`, define the odd difference

`D(e)=B(e)-B(tau e)`.

Pair separation makes `D` nonzero. Normalize: `v(e)=D(e)/||D(e)||`. Then `v(tau e)=-v(e)`.

Conversely, given such `v`, take `B=v` as a map into `R^k`; antipodal outputs are distinct. QED.

Equivalently, such a `v` is a nowhere-zero section of the rank-`k` bundle `L^(direct sum k)`.

### Corollary T6.5a (Stiefel-Whitney necessary condition)
If a separating `B:E->R^k` exists, then

`w_k(L^(direct sum k)) = w_1(L)^k = 0 in H^k(M;Z2)`.

Thus a nonzero power `w_1(L)^k` forbids `k` real channels. This is a standard characteristic-class obstruction.

### Recovery of the projective-space bound
For `S^n->RP^n`, `L` is the tautological line bundle and

`H*(RP^n;Z2) = Z2[a]/(a^(n+1))`, `a=w_1(L)`.

Hence `a^k != 0` for every `1<=k<=n`, ruling out `k<=n`. The explicit map `x->x in R^(n+1)` gives the matching upper bound. This cohomological calculation is consistent with, and can be viewed as a characteristic-class route to, the Borsuk-Ulam obstruction in this case.

The vanishing of `w_1(L)^k` is only a necessary condition in general; T6 does not claim it is sufficient for arbitrary bases.

## 7. Relation to T5's fiber-component theorem
T5 proved that under `ker Dh subset ker DF`, `F` is constant on connected components of measurement fibers, so a set-theoretic branch code can label future-distinct components. T6 adds a second question:

> Can that branch code be realized by a globally continuous sensor with a specified codomain such as `R^k`?

The answer can be no even when each fiber consists of only two isolated points and `ker Dh=0` everywhere. Local differential adequacy and finite fiber cardinality therefore do not control global continuous realizability.

## 8. Distinguishing completion dimension from embedding dimension
`cdim_R(h,F)` asks only for enough extra coordinates to separate **future-distinct collisions that remain after `h`**. It does not ask `B` itself to embed `X`.

Examples:
- If `h` is already sufficient, `cdim_R(h,F)=0` even when `X` has large embedding dimension.
- For a trivial `d`-sheet cover `M x {1,...,d}->M`, one scalar assigning distinct constants to the sheets suffices for full sheet separation, regardless of the dimension of `M`.
- For `S^n->RP^n` with `F(x)=x`, `cdim_R=n+1`; here the standard sphere embedding attains the bound, but equality with an embedding dimension is special to this example and should not be generalized.

## 9. Safe mathematical conclusion
The established topology supports the following project-level statement:

> A finite branch label guaranteed set-theoretically by fiber-component analysis need not admit a low-dimensional globally continuous Euclidean realization. Covering monodromy, Borsuk-Ulam/equivariant obstructions, and characteristic classes can force multiple continuous measurement channels or the use of local/discontinuous charts.

No priority claim is made for Borsuk-Ulam, covering-space monodromy, configuration-space classification, equivariant index theory, characteristic classes, or Reeb/fiber-component quotients. The project-specific contribution is the way these established obstructions are composed with T4/T5's predictive-state-completion question.
