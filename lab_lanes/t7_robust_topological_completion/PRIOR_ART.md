# T7 Prior Art and Novelty Boundary

Date: 2026-08-30
Status: literature-grounded boundary; no priority claim.

## Established mathematical ingredients

| Ingredient | Prior art / source recovered in isolated browser | T7 use | Novelty posture |
|---|---|---|---|
| Antipodal coincidence obstruction | Karol Borsuk, "Drei Sätze über die n-dimensionale euklidische Sphäre," Fundamenta Mathematicae 20 (1933), 177-190, DOI 10.4064/fm-20-1-177-190 | Forces a collision for every continuous `S^n->R^k`, `k<=n` after zero-padding | Established theorem |
| Coincidence-set / Bourgin-Yang extensions | C.-T. Yang's 1954/1955 Borsuk-Ulam generalizations; later Bourgin-Yang literature; Fadell-Husseini equivariant index theory | Context for stronger statements about coincidence sets and equivariant obstructions | Established research area; T7 does not import unproved quantitative claims |
| Ideal-valued equivariant index | E. Fadell and S. Husseini, "An ideal-valued cohomological index theory with applications to Borsuk-Ulam and Bourgin-Yang theorems," Ergodic Theory Dynam. Systems 8 (1988), 73-85, DOI 10.1017/S0143385700009342 | Context for robust/equivariant obstruction language inherited from T6 | Established theory |
| Waist / large-fiber results | M. Gromov, "Isoperimetry of waists and concentration of maps," GAFA 13 (2003), 178-215, DOI 10.1007/s000390300004; Y. Memarian, "On Gromov's Waist of the Sphere Theorem," J. Topol. Anal. 3 (2011), 7-36, arXiv:0911.3972 | Shows that quantitative topology can control more than existence of one coincidence, but T7 does not claim a waist theorem for the present predictive loss | Established results, contextual only |
| Fiberwise/projected embedding | S. A. Melikhov, "Transverse fundamental group and projected embeddings," Proc. Steklov Inst. Math. 290 (2015), 155-165; related projected/near-projected embedding literature | Context for lifting a map to an embedding by added Euclidean coordinates | Established field |
| Covering spaces / monodromy / configuration spaces | Standard covering-space theory; Fadell-Neuwirth configuration-space machinery; T6's configuration-space pullback criterion | Gives the exact-realizability backdrop for the margin question | Established topology |
| Robust sensor placement under noise | Broad engineering literature on sensor placement and noisy recovery, including recent robust sparse sensor-placement work | Context for practical normalization/noise issues | Established applied area; not used as a theorem source |

## What T7 actually proves without needing stronger quantitative topology
The sharp sphere minimax result does **not** require a quantitative strengthening of Borsuk-Ulam. Classical Borsuk-Ulam gives one exact antipodal collision. Because the corresponding futures `x` and `-x` are Euclidean distance `2`, a two-point triangle argument immediately yields worst-case prediction error at least `1`. A zero decoder attains `1`. Thus the project-specific quantitative statement follows by composing two established elementary facts.

This is important for claim discipline: T7 should not describe the error-1 theorem as a new "quantitative Borsuk-Ulam theorem." It is a predictive-risk corollary of classical Borsuk-Ulam.

## Quantitative topology search outcome
The browser search recovered relevant stronger traditions:

1. Bourgin-Yang results estimate dimensions/sizes of coincidence sets under equivariant hypotheses.
2. Gromov's waist theorem controls the size of a fiber of maps from spheres to lower-dimensional Euclidean spaces.
3. Equivariant cohomological-index methods formalize obstruction strength.
4. Projected-embedding / k-prem work studies when extra Euclidean coordinates lift a map to an embedding.

These are mathematically adjacent but are not necessary to prove T7's principal minimax statements. No claim is made that T7's exact definitions of robust predictive margin or epsilon-completion dimension are absent from these literatures.

## Project-specific synthesis
The potentially useful synthesis is the chain

`topologically forced measurement collision -> metric separation of future targets -> minimax predictive lower bound -> positive sheet margin when exact separation exists -> explicit noise budget`.

For developmental-state-completion this makes T6 operational: the obstruction is not merely "exact decoding impossible." Under a declared future metric, it can impose a nonzero approximation floor; once enough channels exist, the achieved fiberwise separation margin can be compared directly with sensor noise.

## Explicit novelty boundary
Do not claim priority for:
- Borsuk-Ulam or Bourgin-Yang theorems;
- sphere waist results;
- equivariant index/cohomology;
- covering-space monodromy;
- configuration spaces;
- projected/fiberwise embeddings;
- generic robust sensor placement;
- triangle-inequality minimax lower bounds.

Safe phrasing:

> We use established topological collision theorems and elementary metric decision bounds to define a task-specific robust-completion diagnostic. The mathematical ingredients are classical; the contribution sought here is their explicit integration into an intervention-indexed predictive-state measurement workflow.
