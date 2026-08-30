# T6 Prior Art and Novelty Boundary

Date: 2026-08-30
Status: literature-grounded synthesis; no priority claim.

## Established mathematical ingredients

| Topic | Established result/connection | T6 use | Novelty posture |
|---|---|---|---|
| Borsuk-Ulam | Karol Borsuk, 1933, *Drei Saetze ueber die n-dimensionale euklidische Sphaere*, Fundamenta Mathematicae 20, 177-190, DOI 10.4064/fm-20-1-177-190 | Exact lower bound for continuous antipodal separation `S^n -> R^k` when `k<=n` | **Classical theorem** |
| Finite covering spaces and monodromy | Standard covering-space theory: loop transport acts by permutations of the fiber; connected covers correspond to transitive actions under standard hypotheses | Explains why local sheet labels can fail to glue globally | **Classical topology** |
| Configuration spaces | Fadell & Neuwirth, 1962, *Configuration Spaces*, Mathematica Scandinavica 10, 111-118, DOI 10.7146/math.scand.a-10517 | Realizing a finite cover by `R^k`-valued sheet coordinates is formulated via pullback from unordered configuration space | **Classical framework** |
| Cohomological Borsuk-Ulam machinery | Fadell & Husseini, 1988, *An ideal-valued cohomological index theory with applications to Borsuk-Ulam and Bourgin-Yang theorems*, Ergodic Theory and Dynamical Systems 8* | Places antipodal separation in general equivariant-obstruction language | **Established machinery** |
| Characteristic classes | Milnor & Stasheff, 1974, *Characteristic Classes* | A double cover defines a line bundle; `w_1(L)^k != 0` obstructs a nonzero section of `L^{\oplus k}` and therefore `k` separating channels | **Standard bundle theory** |
| Reeb/fiber-component quotient | Reeb 1946 and modern Reeb-space literature | T5 quotient by connected fiber components | **Established construction** |
| Local vs global observability | Hermann & Krener, 1977, *Nonlinear Controllability and Observability*, IEEE TAC 22(5), 728-740 | Reinforces that local differential conditions do not guarantee global distinguishability | **Established warning** |
| Euclidean embedding | Whitney 1936 and later embedding theory | Used only to distinguish whole-state embedding dimension from task-relative completion dimension | **Classical theorem family** |

## Literature verification notes from the isolated browser
The isolated browser recovered the following bibliographic facts directly from publisher/index pages or primary-paper search records:

- Borsuk's 1933 paper is listed in *Fundamenta Mathematicae* 20(1), pages 177-190; DOI `10.4064/FM-20-1-177-190`.
- Fadell & Neuwirth's *Configuration Spaces* is listed in *Mathematica Scandinavica* 10 (1962), pages 111-118; DOI `10.7146/math.scand.a-10517`.
- Fadell & Husseini's ideal-valued cohomological index paper is listed in *Ergodic Theory and Dynamical Systems* 8 (1988) and explicitly advertises applications to Borsuk-Ulam/Bourgin-Yang theorems.
- Hermann & Krener's 1977 paper is listed in *IEEE Transactions on Automatic Control* 22(5), pages 728-740.
- Georges Reeb's 1946 paper is cited as *Sur les points singuliers d'une forme de Pfaff completement integrable ou d'une fonction numerique*, C. R. Acad. Sci. Paris 222, 847-849.
- Whitney's 1936 *Differentiable Manifolds* is indexed in *Annals of Mathematics* and is a foundational source for Euclidean manifold embedding.

T6 intentionally avoids claiming that any one of these results is new.

## What T6 adds for this repository
The potentially useful synthesis is the chain

`local kernel condition -> fiber components -> set-theoretic branch classes -> continuous realizability problem -> monodromy/equivariant obstruction -> lower bound on measurement channels`.

The mathematical ingredients are classical. The repository-specific value is to expose a hidden assumption in T5: a branch class that can be named with a few bits need not be realizable as a few globally continuous biological measurement channels.

## Especially important distinctions

### 1. Bit complexity is not Euclidean measurement dimension
For `S^n->RP^n`, only two future-distinct points occur per fiber, so the branch bit cost is one bit, while the minimum continuous Euclidean augmentation dimension is `n+1`.

For the degree-8 circle cover, full set-theoretic sheet coding needs three bits, yet two real channels suffice continuously by embedding the circle in the plane.

Neither quantity monotonically bounds the other without extra assumptions.

### 2. Euclidean channel count is codomain-dependent
One real scalar cannot separate the antipodal points of `S^1`, but one circle-valued channel can. Therefore a statement like "one biomarker is impossible" must mean a one-dimensional real-valued globally continuous readout, not every conceivable one-dimensional topological observable.

### 3. Monodromy is decisive for one real channel but not by itself a complete higher-dimensional invariant
A scalar imposes an order on the fiber, so any nontrivial monodromy is impossible. For `R^2` and above, points can braid around one another without collision, and higher-dimensional/topological obstructions can remain. Configuration spaces and equivariant/cohomological methods are the correct broader language.

## What is safe to say
> Established topology implies that finite local branch structure does not guarantee a low-dimensional globally continuous Euclidean sensor. T6 applies covering monodromy, Borsuk-Ulam, configuration spaces, and characteristic-class reasoning to the developmental-state-completion measurement problem.

## What is not safe to say
- "We discovered a new Borsuk-Ulam theorem."
- "We proved a new classification of finite covers."
- "Topology proves biological state completion needs n+1 biomarkers."
- "Every binary hidden state needs multiple biomarkers."
- "The branch is a real biological variable rather than a task-relative quotient class."

## Publication-level literature work still needed
Before any formal mathematical novelty statement, a topology specialist should search specifically for:
- fiberwise embeddings of covering spaces into trivial Euclidean bundles;
- Euclidean dimension / embedding dimension of covers and associated bundles;
- Schwarz genus / sectional category and equivariant index connections;
- deleted-product and configuration-space criteria for fiberwise embeddings;
- sensor-placement / observer-design literature that explicitly treats global topology and sheet monodromy.

Until then, frame T6 as a rigorous application/synthesis of established mathematics, not as a priority claim.
