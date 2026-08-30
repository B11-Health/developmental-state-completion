# R12 Source Provenance

R12 uses only committed R10/R10B inputs already derived from the public Tribolium Cell Tracking Challenge trajectory task. No new biological data are fetched.

Frozen inheritance: R9 transductive percentile representation, R10 RF/ExtraTrees models and Gate 2, R10B documented seed family `20260830+r`, 30 replicates, and +0.30 pooled original target-SD injection magnitude. R12 changes only the outcome-blind residual-history construction declared in `PREREGISTRATION.md`.

The primary transform uses pooled `S -> z` residualization followed by within-acquisition centering/scaling. The secondary transform fits `S -> z` separately within each acquisition and then centers/scales within acquisition. Neither transform uses Y except the inherited pooled target SD used to set injection magnitude.

Both geometries are outcome-blind but transductive with respect to target-domain covariates. The secondary geometry explicitly fits its Ridge residualizer inside each acquisition, including the acquisition later held out for prediction; this is permitted only for the declared planning diagnostic and must not be presented as target-free deployment.

R12A independently showed that Ridge residualization does not establish literal S-unpredictability; same-family in-sample R2 remains nonzero for some residualized directions.
