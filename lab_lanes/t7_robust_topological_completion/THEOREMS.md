# T7 Theorems: Robust and Approximate Topological Completion

Date: 2026-08-30
Status: theorem/counterexample development; no priority claim.

## 1. Definitions
Let `X` be compact, `h:X->S` a present measurement, `F:X->Y` a future target in a metric space `(Y,d_Y)`, and `B:X->R^k` a continuous augmentation.

### Fiberwise sensor margin
For a declared set `D` of pairs that must be distinguished, define

`Delta_B(D) = inf { ||B(x)-B(x')||_2 : (x,x') in D }`.

For full deterministic completion, a natural choice is

`D_F = { (x,x') : h(x)=h(x'), F(x)!=F(x') }`.

For a finite cover `p:E->M` when every distinct sheet must be distinguished, use

`D_p = { (e,e') : p(e)=p(e'), e!=e' }`.

`Delta_B>0` is a robustness margin in sensor units. It is scale-dependent: replacing `B` by `cB` multiplies the margin by `|c|`. Comparisons therefore require fixed units, range, noise model, normalization, or regularity budget.

### Minimax epsilon-completion risk and dimension
For loss `ell:Y x Yhat -> [0,infinity)`, define

`R_k(h,F;ell) = inf_{B continuous X->R^k} inf_D sup_{x in X} ell(F(x), D(h(x),B(x)))`,

where, for metric prediction, `D` maps the realized measurement image `(h,B)(X)` into the prediction space `Y`; more generally one may specify a prediction space `Yhat` together with a loss on `Y x Yhat`. The decoder may be arbitrary unless continuity is explicitly imposed. Define

`cdim_epsilon(h,F;ell) = min { k>=0 : R_k <= epsilon }`.

For metric prediction we use `ell(y,yhat)=d_Y(y,yhat)`. This separates topological approximation error from statistical estimation error: `R_k` is a population/minimax representational quantity with the true maps known.

## 2. Sharp sphere lower bound
Let `h:S^n->RP^n` identify antipodes and `F(x)=x in R^(n+1)` with Euclidean loss.

### Theorem T7.1 (forced collision gives sharp error one)
For `n>=1` and every `k<=n`, every continuous `B:S^n->R^k` and every decoder `D` satisfy

`sup_x ||x-D(h(x),B(x))||_2 >= 1`.

Moreover the bound is sharp: `R_k=1` for every `0<=k<=n`.

#### Proof
Borsuk-Ulam gives an `x` with `B(x)=B(-x)`. Since `h(x)=h(-x)`, the decoder receives exactly the same input at `x` and `-x`; call its output `y`. By the triangle inequality,

`2 = ||x-(-x)|| <= ||x-y|| + ||y-(-x)||`,

so at least one error is at least `1`. This proves the lower bound.

For the upper bound, take any continuous `B` (including the zero-channel case) and use the constant decoder `D=0`. Every `x in S^n` has `||x||=1`, so the worst-case error is exactly `1`. QED.

### Edge case n=0
`S^0={-1,+1}` and `RP^0` is one point. With `k=0` the same two-point triangle argument gives minimax error `1`; with one real channel `B(x)=x`, zero error is possible. Thus the threshold statement below also holds for `n=0`.

### Corollary T7.1a (exact epsilon dimension)
For every `n>=0`,

- if `epsilon >= 1`, then `cdim_epsilon=0`;
- if `0 <= epsilon < 1`, then `cdim_epsilon=n+1`.

The upper bound for `epsilon<1` follows from `B(x)=x in R^(n+1)`, which permits exact decoding. T6 supplies the same `n+1` threshold for zero error; T7 shows that **no dimension reduction at all occurs until the allowed worst-case Euclidean error reaches the sphere radius**.

### Theorem T7.2 (n+1 channels give zero error and positive antipodal margin)
With `B(x)=x`,

`inf_x ||B(x)-B(-x)|| = 2`,

and decoder `D([x],B)=B` has zero error. More generally `B_c(x)=c x` has margin `2|c|` and zero noiseless prediction error for `c!=0`.

The arbitrary scaling is why a raw margin must not be advertised without a sensor scale/noise convention.

## 3. Generic collision-to-risk lemma
### Theorem T7.3
Let `(Y,d)` be any metric space. If two states `x,x'` produce identical completed measurements `(h,B)` and their futures satisfy `d(F(x),F(x'))=delta`, then every decoder has worst-case error at least `delta/2` on `{x,x'}`.

Proof: for common decoder output `yhat`, triangle inequality gives `delta <= d(F(x),yhat)+d(yhat,F(x'))`. QED.

This requires no decoder continuity and no smoothness. The only topology enters when proving that a collision must exist.

## 4. Probabilistic future laws
Let the future target be a probability law `P_x` in a metric space of probability measures `(P(Y),d_P)`.

### Theorem T7.4 (probabilistic collision lower bound)
If `(h,B)` collides at `x,x'`, then any predicted law `Q` based only on `(h,B)` obeys

`max(d_P(P_x,Q), d_P(P_x',Q)) >= (1/2) d_P(P_x,P_x')`.

This is again the metric triangle inequality. Therefore any topologically forced collision whose two conditional future laws are separated by at least `delta` yields minimax probabilistic error at least `delta/2`.

The result applies directly to total variation and Wasserstein distances because both are metrics under their standard hypotheses; for `W_p`, take a standard metric ground space (for example Polish) and probability laws with finite p-th moment.

### Corollary T7.4a (sharp TV midpoint for a collided pair)
Under the convention `TV(P,Q)=sup_A |P(A)-Q(A)|`, let `M=(P+Q)/2`. Then

`TV(P,M)=TV(Q,M)=TV(P,Q)/2`.

Thus the `delta/2` pairwise lower bound is attained by the mixture midpoint.

### Corollary T7.4b (Wasserstein mixture midpoint)
For `W_p`, `p>=1`, and finite p-th moments, the mixture `M=(P+Q)/2` satisfies

`W_p(P,M) <= 2^(-1/p) W_p(P,Q)`

by coupling the shared half identically and the other half optimally. For `p=1` this gives `W_1(P,M)<=delta/2`, and the triangle lower bound forces equality for both endpoints. Hence the pairwise `W_1` lower bound `delta/2` is sharp.

For `p>1`, the generic triangle lower bound remains `delta/2`, but the simple mixture estimate is `2^(-1/p)delta`; T7 does not claim universal midpoint sharpness in arbitrary Wasserstein spaces.

### Deterministic laws as a special case
For `P_x=delta_x` on the unit sphere with ground Euclidean metric, `W_1(delta_x,delta_-x)=2`. Thus the forced antipodal collision gives worst-case `W_1` prediction error at least `1`, matching the deterministic theorem.

For total variation, `TV(delta_x,delta_-x)=1` for `x!=-x`, so the analogous lower bound is `1/2`, attained on the collided pair by the 50/50 mixture.

## 5. Compact finite covers: exact injectivity implies positive margin
Let `p:E->M` be a finite-sheeted covering, with `E` compact and `M` Hausdorff, and let `B:E->R^k` be continuous and injective on every fiber.

### Theorem T7.5 (positive global sheet-separation margin)
Then

`Delta_B = min { ||B(e)-B(e')|| : p(e)=p(e'), e!=e' } > 0`.

#### Proof
Because a finite cover is locally a finite disjoint union of sheets, the off-diagonal fiber-pair set

`D_p={(e,e'):p(e)=p(e'), e!=e'}`

is closed in `E x E`: near any diagonal point `(e,e)`, choose an evenly covered neighborhood and the sheet containing `e`; within the product of that sheet with itself, equality of basepoints forces equality of points. Thus the diagonal is relatively open inside the fiber product, so its complement `D_p` is relatively closed. Since `E x E` is compact, `D_p` is compact.

The continuous function `g(e,e')=||B(e)-B(e')||` is strictly positive on `D_p` by fiberwise injectivity, hence attains a strictly positive minimum. QED.

Compactness is essential for converting pointwise separation into a uniform positive margin.

### Counterexample T7.C1 (noncompact injectivity need not give a positive margin)
Take the trivial two-sheet cover `E=R x {0,1}->R` and define `B(t,0)=0`, `B(t,1)=1/(1+|t|)`. The map is fiberwise injective for every finite `t`, but the global margin has infimum `0` as `|t|->infinity`.

## 6. Additive sensor noise
Assume the base measurement `p(e)` is known exactly and the augmentation is observed as

`Z=B(e)+xi`, with `||xi||<=eta`.

### Theorem T7.6 (bounded-noise robust decoding)
If a compact finite cover has fiberwise margin `Delta_B>0` and

`2 eta < Delta_B`,

then the true sheet is uniquely recoverable from `(p(e),Z)` by nearest-neighbor decoding among the finite set `{B(e'):p(e')=p(e)}`. Hence the exact point in the known finite fiber is recovered, so any fixed declared target map `F:E->Y` can be decoded exactly in this population representation setting.

#### Proof
For the true point, `||Z-B(e)||<=eta`. Every other sheet point `e'` has

`||Z-B(e')|| >= ||B(e)-B(e')||-eta >= Delta_B-eta > eta`.

So the true sheet is the unique nearest point. QED.

### Sharpness of the universal threshold
If `2 eta >= Delta_B` and the margin is attained—as it is under the compact/Hausdorff hypotheses of T7.5—choose a pair attaining the margin. Their closed radius-`eta` balls intersect when `2 eta>=Delta_B`. At an intersection observation, an adversary can produce the same noisy sensor value from either sheet. Therefore no decoder can guarantee exact sheet recovery uniformly over all bounded noises. If their futures are distance `delta`, Theorem T7.3 forces worst-case future error at least `delta/2` at that ambiguous observation.

This is a worst-case bounded-noise statement. Gaussian or other stochastic noise requires error probabilities/Bayes risk rather than a hard threshold.

## 7. Approximate margins tied to future tolerance
Exact sheet injectivity can be stronger than necessary. For predictive tolerance `epsilon`, define the set of future-dangerous pairs

`D_epsilon = {(x,x'): h(x)=h(x'), d_Y(F(x),F(x'))>2epsilon}`

and robust predictive margin

`Delta_B^(epsilon) = inf_{D_epsilon} ||B(x)-B(x')||`.

Any exact collision on `D_epsilon` makes worst-case error `>epsilon` impossible by T7.3. Under bounded sensor noise, a positive `Delta_B^(epsilon)>2eta` guarantees that noise balls for all pairs whose futures are more than `2epsilon` apart do not overlap. Turning that separation condition into a global epsilon-accurate decoder can require additional geometry of the future sets; T7 does not claim pairwise separation alone is sufficient in arbitrary metric targets.

## 8. Decoder continuity versus arbitrary decoders
The lower bounds T7.1, T7.3, and T7.4 do **not** assume decoder continuity. They are stronger: identical measurements force identical decoder outputs for any deterministic function.

Upper bounds can differ if continuity is required. In the compact exact-completion setting of T6, a continuous injective-enough measurement induces a continuous decoder on the realized measurement image under standard compact-to-Hausdorff quotient conditions. Under approximate prediction, existence of an arbitrary minimax selector need not imply existence of a continuous selector. T7 keeps these notions separate.

## 9. What topology does and does not lower-bound
Topology provides a representational floor only under declared assumptions:

- the augmentation `B` is continuous;
- the observation codomain is fixed, here Euclidean `R^k`;
- the loss and future metric are fixed;
- the minimax domain includes all relevant states;
- sensor noise is modeled explicitly.

It does **not** include finite-sample estimation, misspecified decoder classes, calibration error, distribution shift, measurement preprocessing, or biological stochasticity unless those are separately incorporated. An empirical error above the topological lower bound is not evidence that topology caused the excess error.

## 10. Main T7 conclusion
For the antipodal projective-space example, the exact topological obstruction has a sharp approximate form: with at most `n` continuous real channels, minimax worst-case Euclidean future error is exactly `1`; only at `n+1` channels can the error drop below `1`, in fact to zero. For compact finite covers, exact fiberwise continuous separation automatically has a positive global margin, and bounded additive noise consumes that margin at the sharp universal factor `2 eta < Delta_B`.
