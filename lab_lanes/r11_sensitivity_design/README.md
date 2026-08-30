# R11 Sensitivity Design — Qualified After Independent Audit

R11 decomposes the **original implemented-seed** R10 calibration into S-only adequacy and history-detection components, then evaluates the same first 20 directions at 0.15/0.30/0.45/0.60 target SD.

**Aggregate planning result:** detection rises 0%→75% while S-only adequacy falls 85%→45%; joint success is 0%, 30%, 30%, 30%. R11A independently reproduced the counts and selected refits, but required qualification: individual detection is not monotone, the 30% joint sets change with scale, and the original R10 implementation seed family differed from the literal preregistration.

R10B later executed the documented seed family and obtained 16/30 joint successes, still below 24/30. R11 therefore remains a planning diagnostic, not the controlling calibration result.

The executable now rejects duplicate/missing replicate IDs during aggregation.
