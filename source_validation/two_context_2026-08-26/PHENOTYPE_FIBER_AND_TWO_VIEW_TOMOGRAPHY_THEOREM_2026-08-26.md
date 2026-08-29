# Phenotype-fiber and two-view developmental tomography theorem — working note, 2026-08-26

## Setup
Let

\[
W_{n,G,c}=\{s\in[-c,c]^n:\|s\|_1=G\}
\]

be the signed fixed-budget causal world. For context q in (Z2)^n let R_q be the diagonal sign-reflection operator and define the rectified active signal

\[
u_q(s)=[-R_qs]_+.
\]

Let F:U->Y be the downstream developmental phenotype map, where U is the feasible rectified domain.

## Theorem 1 — exact baseline fiber before the downstream decoder
For baseline q=0, u=s_-=[-s]_+. Let A=supp(u) be the negative/active coordinates. Then

\[
R^{-1}(u)=\{s:\ s_A=-u_A,\ s_{A^c}=v,\ 0\le v_j\le c,\ \sum_{j\in A^c}v_j=G-\|u\|_1\}.
\]

Therefore the latent baseline fiber is a convex capped simplex in the inactive positive coordinates. In a relative interior stratum where all inactive coordinates can remain strictly between 0 and c, its dimension is

\[
\dim R^{-1}(u)=n-|A|-1.
\]

Caps can lower the dimension on boundary strata but cannot create nonconvexity.

### Feasible baseline quotient
For a fixed active support A of size k, the rectified coordinates obey

\[
0<u_j\le c\ (j\in A),\qquad
\max(0,G-(n-k)c)\le \sum_{j\in A}u_j\le \min(G,kc).
\]

The baseline quotient is the support-stratified union of these truncated positive simplices.

## Theorem 2 — phenotype fibers when F is injective
If F is injective on U, then equality of baseline phenotypes is equivalent to equality of u=s_-:

\[
F(s_-)=F(t_-)\iff s_-=t_-.
\]

Hence every baseline phenotype fiber in W is exactly the convex capped simplex above. The phenotype does not introduce additional global folds beyond the clipping ambiguity.

## Theorem 3 — complementary two-view tomography
For any q, let qbar=q xor (11...1). Then

\[
u_q=[-R_qs]_+,\qquad u_{\bar q}=[R_qs]_+,
\]

and coordinatewise

\[
R_qs=u_{\bar q}-u_q,\qquad |s|=u_{\bar q}+u_q.
\]

If F is injective, the two observed phenotypes F(u_q),F(u_qbar) uniquely determine the complete signed hidden world s. Thus any complementary phenotype pair is a global embedding of W into YxY.

## Theorem 4 — fixed-budget two-view masks of Hamming distance >=n-1
Suppose G is known. For two contexts q1,q2 whose Hamming distance is n, Theorem3 applies. If their Hamming distance is n-1, n-1 signed coordinates are recovered from opposite rectified halves. The magnitude of the one never-reflected coordinate is then fixed by the budget G; its sign is determined by whether its common rectified coordinate is active or zero (away from the exact zero seam). Therefore all masks at Hamming distance >=n-1 are globally sufficient at the latent signal level, and are phenotype-level sufficient whenever F is injective.

For n=4 relative to baseline, the five universal second masks are

\[
0111,1011,1101,1110,1111.
\]

## Theorem 5 — stability under a co-Lipschitz phenotype decoder
Assume

\[
\|F(u)-F(v)\|\ge m\|u-v\|
\]

on U. If observed/source phenotype y obeys \|y-F(u)\|<=eta and uhat is a constrained nearest point satisfying \|F(uhat)-y\|<=eta, then

\[
\|\hat u-u\|\le 2\eta/m.
\]

For a complementary pair,

\[
\|\hat s-s\|\le4\eta/m.
\]

Thus practical sign recovery for coordinate j is guaranteed whenever |s_j| is larger than the coordinate reconstruction error radius. Near causal collapse the algebra remains exact; finite precision controls the sign error probability.

## Executor evidence added 2026-08-26
### Seam-consistent phenotype decoder
A single degree-3 polynomial F(u) with u=max(-s,0), trained on new40/640 source contours, externally predicts source contours with worst Jaccard error about 2.24e-6 on old14, 2.13e-6 on near-seam12, and <=1.61e-6 on prospective/adversarial F-face tests.

### Constructive global univalence certificate for the frozen cubic
A rounded 4x34 projection A was found such that sym(A DF(u)) is uniformly positive on 0<=u_j<=1, sum u<=1.8. With A rounded to two decimals:
- ||A||_2 = 13.5298206962;
- 1,073,535-point grid minimum eigenvalue = 0.2435201785;
- explicit between-grid perturbation bound = 0.0307504796;
- certified floating-point margin mu >= 0.2127696988;
- resulting cubic co-Lipschitz lower bound mu/||A|| >= 0.01572598.

This is a constructive numerical certificate for the frozen polynomial, not yet a formal interval/rational proof for the source simulator.

### External phenotype-level two-view reconstruction
The cubic was trained new40 only and then inverted on unseen source contours:
- old14: 100% sign accuracy, median signed L2 2.31e-4, worst 6.86e-4;
- near-seam12 including gains down to .001: 100% sign accuracy, median 2.02e-4, worst 5.77e-4.
All five Hamming>=3 two-context masks gave 100% sign recovery on both external cohorts.

### Prospective post-hypothesis source validation
Frozen before rendering: TWO_PHENOTYPE_PROSPECTIVE_FROZEN_2026-08-26.json, SHA256 b5fdc0bd257dbb57874f107b3c7a12b6c9fe5ec9f89cb48de585743846341c3a.
Across 32 new complementary phenotype pairs, including four laws with a gain exactly .001:
- sign accuracy 100%;
- median signed L2 1.75175e-4;
- p95 4.28985e-4;
- maximum 5.14625e-4;
- every .001 weak-channel sign correct.
All preregistered thresholds passed.

### Exact baseline-fiber source example
Two fully interior laws gA=(.7,.05,.45,.6), gB=(.7,.45,.05,.6), state1001, have identical u=(.7,0,0,.6) and produced exactly coordinate-identical source baseline contours despite signed structural separation 0.565685. Counterfactual contexts that expose S/F separate them, with complementary q1111 source dIoU about .0128434.

## Scope / nonclaims
- The latent rectifier/fiber statements are exact for the restricted model.
- Global injectivity is certified for the frozen cubic surrogate up to numerical verification precision; source-continuum injectivity is supported prospectively but not formally certified.
- This is not yet evidence that living plant morphogenesis is exactly governed by this four-channel rectified architecture.
