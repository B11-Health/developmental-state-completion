# R11 Theory Note — Why Known-Incomplete Calibration Can Trade Detectability Against Adequacy

Consider the idealized population model `Y=m(S)+e` with `E[e|S]=0`, and define a synthetic omitted-history direction `Z` with `E[Z|S]=0`. Let `Y_a=Y+aZ`. Assume finite second moments, nonzero `Var(Y_a)`, and `Cov(e,Z)=0`. Independence of `e` and `Z` is sufficient but stronger than necessary.

Under these assumptions the oracle squared-error predictor from S remains `m(S)`, `Cov(m(S),e)=0`, and `Cov(m(S),Z)=0`. Therefore

`MSE_S(a)=Var(e)+a^2 Var(Z)`,

`Var(Y_a)=Var(m(S))+Var(e)+a^2 Var(Z)`,

and the population oracle coefficient of determination is

`R2_S(a)=Var(m(S)) / [Var(m(S))+Var(e)+a^2 Var(Z)]`.

For `Var(Z)>0`, this oracle S-only R2 decreases with `|a|`. A larger omitted-history component can therefore become easier for an S+H procedure to detect while making an absolute S-only adequacy prerequisite harder to satisfy. A joint criterion requiring both properties need not improve as injection magnitude grows.

This is an idealized explanatory model, not a theorem about the finite-sample R10/R11 Random Forest/Extra Trees pipeline. The actual construction residualizes Z **linearly** against pooled S; it does not establish `E[Z|S]=0`, `Cov(e,Z)=0`, or population-oracle conditions. It also scales injection using pooled outcome dispersion. Accordingly, R11's empirical result is stated only at the aggregate level for its tested task, directions, models, samples, and scale grid.
