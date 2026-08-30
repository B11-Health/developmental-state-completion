# T7A Independent Adversarial Audit

Date: 2026-08-30
Base: 931dfc8 (after ef12c4c)
Verdict: PASS WITH QUALIFICATIONS. No central quantitative theorem failed, but several hypotheses/wordings must be tightened.

## Audit matrix

| Claim | Verdict | Independent finding | Required correction |
|---|---|---|---|
| Exact minimax risk 1 for `S^n -> RP^n`, `k<=n` | PASS | Borsuk-Ulam forces an antipodal completed-measurement collision; triangle inequality gives error >=1; constant zero decoder gives <=1. Works also for `n=0,k=0`. | Explicitly state decoder output lies in `R^{n+1}` for Euclidean loss. |
| Epsilon-dimension jump | PASS | For `epsilon<1`, all `k<=n` have risk 1 while `k=n+1` admits exact identity augmentation. For `epsilon>=1`, `k=0` suffices. | Same decoder-codomain clarification. |
| Positive antipodal margin at `n+1` | PASS | `B(x)=x` has pair margin exactly 2; scaling gives `2|c|`. | Keep scale-dependence warning. |
| Generic collision-to-risk lemma | PASS | Pure triangle inequality; no continuity assumption on decoder needed. | Define prediction codomain/loss consistently. |
| Probabilistic TV/Wasserstein collision bound | PASS | Any metric on laws gives pairwise lower bound `delta/2`. TV and `W_p` qualify under their standard domains. | For Wasserstein say ground space and measures satisfy conditions making `W_p` a metric (e.g. Polish metric space, finite pth moments). |
| TV midpoint sharpness | PASS | `M=(P+Q)/2` gives exact half-TV distance to both endpoints. | None. |
| `W_1` pairwise sharpness via mixture | PASS | Mixture coupling gives both endpoint distances <=delta/2; triangle inequality forces equality. | Optimal coupling existence is not needed if one argues with epsilon-optimal couplings; mention this for maximal generality. |
| `W_p,p>1` mixture estimate | PASS | Bound `2^{-1/p}delta` is valid symmetrically for both endpoints. T7 correctly avoids claiming universal midpoint sharpness. | None beyond standard `W_p` hypotheses. |
| Compact finite-cover positive global margin | NEEDS QUALIFICATION | The proof that `D_p` is compact silently needs the fiber product `{p(e)=p(e')}` to be closed in `E x E`, which follows if the base `M` is Hausdorff. Compact `E` alone is insufficient under completely general covering-space conventions. | State `M` Hausdorff (or another hypothesis guaranteeing the diagonal in `M x M` is closed). Then `D_p` is closed in compact `E x E` and the proof is valid. |
| Noncompact counterexample | PASS | Trivial double cover over `R` with separation `1/(1+|t|)` is continuous, fiber-injective, and has infimum 0. | None. |
| Bounded-noise sufficiency `2 eta < Delta` | PASS | Nearest-neighbor proof is exact when base point is known and the fiber codebook is known. | Replace vague phrase “future F constant on each sheet point” by: once the state within the known fiber is recovered, any declared `F:E->Y` can be evaluated/decoded in the population representation setting. |
| Impossibility at `2 eta >= Delta` | PASS WITH SCOPE | In the compact/min-attained setting, a closest pair has intersecting closed noise balls at equality, producing identical observations. This proves exact sheet-recovery impossibility. | Do not generalize equality-case sharpness to settings where `Delta` is only an unattained infimum. Future-prediction impossibility additionally requires the ambiguous pair to have distinct futures. |
| Dangerous-pair margin implies global epsilon decoder | PASS AS CAVEATED | T7 correctly says pairwise non-overlap alone need not construct a global epsilon-selector in an arbitrary target geometry. | Preserve this caveat; never upgrade it to a global decoder theorem without extra selection/geometry assumptions. |
| Decoder continuity discussion | PASS | Lower bounds hold for arbitrary deterministic decoders; continuous-selector existence is a separate upper-bound issue. | Make domain/codomain explicit: decoder on realized measurement image into prediction space, or define a general prediction space `Yhat` with loss on `Y x Yhat`. |

## Proof checks

### 1. Sphere minimax theorem
For `k<=n`, zero-pad `B:S^n->R^k` to `R^n`. Borsuk-Ulam gives `B(x)=B(-x)`. Since `h(x)=h(-x)`, any deterministic decoder receives one common input and returns one `y in R^{n+1}`. Then `2=||x-(-x)|| <= ||x-y||+||y+x||`; hence one error is at least 1. The zero decoder has error exactly 1. No continuity of the decoder is used.

The `n=0` case is a two-point decision problem and gives the same threshold directly. Thus `cdim_epsilon=0` for `epsilon>=1` and `n+1` for `0<=epsilon<1`.

### 2. Probability-law claims
The lower bound is just the metric collision lemma applied in a space of probability laws. For total variation, linearity of signed measures yields `TV(P,(P+Q)/2)=TV(P,Q)/2`. For `W_p`, mix an approximately optimal `P-Q` coupling with the identity coupling on the shared half; taking the infimum gives `W_p(P,M)^p <= (1/2)W_p(P,Q)^p`, and similarly for `Q`. At `p=1`, the triangle inequality forces equality at both endpoints.

These are pairwise statements. They do not imply that a single midpoint prediction simultaneously solves a many-state minimax problem.

### 3. Compact-cover margin
Let `C=(p x p)^{-1}(Delta_M)`. If `M` is Hausdorff, `Delta_M` is closed, so `C` is closed in compact `E x E`. Covering local triviality makes the diagonal of `E x E` relatively open in `C`: near `(e,e)`, restrict both coordinates to the same local sheet, where equal basepoints force equal points. Therefore `D_p=C\Delta_E` is closed in `C`, hence compact. Continuous fiber-injective `B` gives a positive continuous distance function on compact `D_p`, so the minimum is positive.

Without a separation hypothesis on `M`, the step `C` closed is not automatic. This is the main theorem-hypothesis repair.

### 4. Bounded noise
If `2 eta < Delta_B`, the true codeword is within `eta` while any other fiber codeword is farther than `Delta_B-eta>eta`; unique nearest neighbor follows. If a minimum-distance pair exists and `2 eta>=Delta_B`, the midpoint of the pair belongs to both closed radius-`eta` balls, so the same observation can arise from two states. This establishes the exact universal threshold for compact/min-attained full sheet recovery.

For prediction rather than sheet identity, an ambiguity is harmful only to the extent that the corresponding futures are separated. T7 states this correctly via the collision-risk lemma.

## Assumption corrections to apply upstream

1. In the minimax definition, either set `D:(h,B)(X)->Y` for metric loss, or define a prediction space `Yhat` and a loss `ell:Y x Yhat->[0,infinity)`. The sphere theorem requires outputs in `R^{n+1}`.
2. In T7.5, add `M` Hausdorff (standard manifold/CW applications already satisfy this).
3. In Wasserstein statements, name the standard metric hypotheses instead of saying only “finite p-th moments.”
4. In T7.6, remove “F constant on each sheet point”; exact recovery of the point of the known finite fiber is enough to decode any fixed target map `F`.
5. State equality-case noise sharpness only where the margin is attained; compact T7.5 supplies attainment.
6. Preserve the distinction between pairwise dangerous-pair separation and existence of one global epsilon-accurate decoder.

## Novelty assessment
The mathematics underlying T7 is established. Classical Borsuk-Ulam supplies the collision, while the error-1 minimax value is an elementary metric-decision corollary. Bourgin-Yang/cohomological-index and sphere-waist literature provide stronger quantitative-topology context. Projected-embedding / `k`-prem literature already studies Euclidean vertical lifts `(p,B)` and therefore substantially overlaps the exact realization side. Urysohn-width/waist literature also studies continuous low-dimensional representations through fiber size/diameter, making broad “new quantitative topological dimension” claims unsafe.

Safe novelty statement:

> T7 does not introduce a new Borsuk-Ulam, covering-space, projected-embedding, Wasserstein, or robust-decoding theorem. Its defensible contribution is a project-specific synthesis: classical forced collisions are converted into task-relative minimax predictive risk, exact fiber separation is converted into a sensor-noise margin under explicit compact/Hausdorff assumptions, and these quantities are integrated with the developmental-state-completion framework.

## Final verdict
No material claim is false after the hypothesis repairs above. The strongest issue is the missing Hausdorff/separation hypothesis in the compact-margin proof; the next most important is the under-specified decoder codomain. All sharpness claims checked are valid within their stated or repaired scope.
