# R15 Model Freeze

Date: 2026-08-30
Status: FROZEN BEFORE FIRST DS0007 SCORE

Training embryos: DS0004, DS0005. Primary held-out embryo: DS0007.

Models:
- Ridge(alpha=10.0)
- RandomForestRegressor(n_estimators=500, min_samples_leaf=2, max_features=0.8, random_state=20260830, n_jobs=-1)
- ExtraTreesRegressor(n_estimators=500, min_samples_leaf=2, max_features=0.9, random_state=20260830, n_jobs=-1)

S, H and Y are standardized using training rows only. The vector score is `1 - SSE_model/SSE_trainmean` over all held-out windows and all eight standardized future-state coordinates. Gate 1 requires positive vector R2 and RMSE below the train-only mean baseline for at least two of the three estimators on DS0007. If Gate 1 fails, history fitting is prohibited.
