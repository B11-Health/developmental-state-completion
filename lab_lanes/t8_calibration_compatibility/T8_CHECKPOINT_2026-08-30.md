# T8 Calibration Compatibility Checkpoint — Corrected After T8A

Date: 2026-08-30
Decision: **NEEDS-QUALIFICATION AUDIT INCORPORATED / CORRECTED IDEALIZED ENVELOPE**

T8A independently found that the original T8 setup omitted a necessary augmented-oracle assumption. Revealing the injected direction `Z` from `(S,H)` does not prevent `(S,H)` from also predicting some of the base residual `E`. A finite counterexample satisfied every original written assumption while falsifying the original augmented R2 curve and iff statement.

The corrected simple theorem now requires `E[E|S,H]=0` (equivalently `E[Y_a|S,H]=M+aZ`) in addition to the original S-orthogonality assumptions. Under that repaired model, all original formulas, the iff condition `r0>=rho/(1-delta)`, `Delta_max=1-rho/r0`, and the amplitude interval are exact and independently verified by T8A.

T8 now also records the generalized case `q=Var(E[E|S,H])/B`, where `R2_{S+H}=(r0+x+q)/(1+x)` and `Delta=(x+q)/(1+x)`.

This remains elementary design algebra only. It is not a theorem about R10/R11/R12 finite-sample gates and carries no biological or priority claim.

T8_CORRECTED_COMPLETE
