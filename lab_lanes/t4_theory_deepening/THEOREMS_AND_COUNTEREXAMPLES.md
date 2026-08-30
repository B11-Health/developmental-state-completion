# Theorems and counterexamples

Status: small provable statements + explicit falsifiers. No priority claim.

## T1. Log-loss identity
Assume regular conditional distributions. For any intervention a,
V_log(H|S,a)=R*(S,a)-R*(S,H,a)=I(Y^a;H|S).
Proof: Bayes log risk is conditional entropy. Subtract H(Y^a|S,H) from H(Y^a|S).
Corollary: exact distributional screening-off iff log-loss history value is zero.

## C1. One loss can miss dependence
Let H be a fair bit and Y=H. Under squared loss for target Z=Y-1/2 with a decoder class forced to constants, H has zero admissible value even though Y and H are dependent. Thus decoder-restricted loss sufficiency is not distributional sufficiency.

## T2. Observational sufficiency does not transfer across interventions
There exists a structural system with Y independent of H observationally given S, but dependent after intervention.
Construction: H,U iid fair bits, S=0. Observationally set A=H and Y=H xor A=0, so Y is constant and H is screened off. Under do(A=0), Y=H, hence I(Y;H|S,do(A=0))=1 bit.
Therefore observational screening-off alone cannot certify intervention-indexed state completeness.

## T3. Finite-horizon does not imply longer-horizon
Let S be constant, H fair, and Y_t=0 for t<=T while Y_{T+1}=H. Then H is screened off for Y_{0:T} but not for Y_{0:T+1}. No finite-horizon claim upgrades without assumptions on dynamics or all horizons.

## T4. Finite experiment family identifies finite predictive equivalence classes iff it separates them
Let W be finite candidate worlds and tests q in Q with noiseless response r_q(w). Define w~w' iff all q in Q give equal responses. A chosen panel P subset Q identifies equivalence classes exactly iff for every w not~ w' there exists q in P with r_q(w) != r_q(w'). Proof is immediate from equality of response signatures. This is the Test-Cover/separating-system criterion, not a new theorem.

## T5. Bounded response error gives a tolerance sandwich
If ||Fhat(w)-F(w)||_inf <= eta for all w, then for every pair w,w', | ||Fhat(w)-Fhat(w')||_inf - ||F(w)-F(w')||_inf | <= 2eta. Thus true delta-close pairs are estimated (delta+2eta)-close, and estimated (delta-2eta)-close pairs are truly delta-close.
Proof: triangle inequality twice.

## C2. Connected fibers can be topologically unstable without a margin
Three worlds on a line have true response coordinates 0,1,2 and threshold delta=1. With edges defined by <=delta, the graph is connected. Perturb the middle response from 1 to 1+epsilon and the first edge disappears for every epsilon>0. Therefore arbitrarily small error can split a connected component when a critical edge sits exactly at threshold. Stability requires a separation margin from threshold, not merely small norm error.

## T6. Local-to-global deterministic factorization under connected fibers
Let X,S be smooth manifolds, h:X->S a surjective submersion with connected fibers, and F:X->R^m smooth. If ker Dh_x subset ker DF_x for every x, then F is constant on each fiber. Hence there is a unique g:S->R^m with F=g o h; locally g is smooth, and under the quotient topology induced by a submersion it is smooth globally.
Proof: tangent vectors to a fiber lie in ker Dh, hence DF annihilates them. Along any piecewise smooth path in a connected fiber, d/dt F(gamma(t))=0, so F is constant. Define g(s)=F(x) for x in h^{-1}(s). Submersion charts provide local smoothness.

## C3. Kernel inclusion alone is not enough globally
Let X be the disjoint union of two copies of R, h(x,branch)=x, and F(x,branch)=branch in {0,1}. Then Dh is full rank and ker Dh={0}, so ker Dh subset ker DF vacuously everywhere, yet no single g satisfies F=g o h because the two disconnected points in each fiber have different F. Connected fibers (or explicit fiber constancy) are essential.

## C4. Predictive equivalence is weaker than mechanistic identity
World 1: latent mechanism M=0 always; World 2: M=1 always. For every allowed intervention in Pi, both emit the same Y distribution. They are predictively equivalent on Pi but mechanistically distinct. Enlarging Pi may or may not separate them. Therefore predictive-state completeness is quotient completeness, not ontology recovery.

## T7. Robust-min does not preserve submodularity
Let f1(Q)=1[a in Q], f2(Q)=1[b in Q]. Both are modular. g(Q)=min(f1(Q),f2(Q)) has g({a})=g({b})=0 and g({a,b})=1, violating submodularity. This re-derives M3.1.

## T8. Expected independent survival preserves submodularity
For a monotone submodular f and independently surviving selected items, g(Q)=E[f(R_Q)] is submodular. Couple survival with fixed Bernoulli labels for the entire ground set; each realization maps Q to Q intersect R and preserves submodularity. Expectation preserves the inequality. Independence is sufficient, not necessary; the key is a selection-independent coupling.

## C5. History screening-off does not imply a complete measured state
Take latent X=(S,Z), history H=Z, and future task Y=S. Then Y is screened off from H given S perfectly, but S omits latent Z and is incomplete for any future/intervention depending on Z. Screening-off establishes only task-relative sufficiency.

## C6. Adding present variables can unmask history
H,Z iid fair, Y=H xor Z. Then I(Y;H)=0 but I(Y;H|Z)=1 bit. Residual-history information is not monotone decreasing as measurements are added.

## Reviewer-facing boundary
None of T1-T8 proves living-system state completion. The strongest theorem-level statement available here is conditional factorization/refinement under explicit assumptions. Biological claims require calibrated tests of the declared H/S/Y/intervention family.
