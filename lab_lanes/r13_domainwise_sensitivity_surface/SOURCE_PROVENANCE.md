# R13 Source Provenance

R13 uses no new biological data. It inherits the public Tribolium trajectory task and R9/R10/R12 frozen preprocessing/model definitions already committed on main.

Chronology is repository-auditable: `PREREGISTRATION.md` was committed at `9487bf4`; execution code at `aff852a`; new 0.15/0.45/0.60 result files were generated only afterward. The 0.30 arm is read directly from committed R12 secondary decision files and the R13 runner refuses a new 0.30 fit.

The geometry is outcome-blind but transductive/acquisition-conditioned, using unlabeled S/H from each acquisition. Injection magnitude uses the inherited pooled original target SD.
