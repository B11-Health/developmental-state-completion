# R15B Independent Source-Level Replication

Date: 2026-08-30
Verdict: **PASS**

## Source identity
- DS0004 Zenodo record 17391047: 63858868 bytes; SHA-256 `0cf8690d0174770f82826e0a9810fc82957c2cc14b37e2e9310a7b389468aa2d`; exact match to R15 provenance: **YES**.
- DS0005 Zenodo record 17391052: 56385544 bytes; SHA-256 `53407d593139fcee9448c3d8006db33997a7664bc3c9a6194cc783095db87a96`; exact match to R15 provenance: **YES**.
- DS0007 Zenodo record 17391061: 64939950 bytes; SHA-256 `345beebef2bd5ba74fe4ef8dad3d135b203bff1c54fbdd2cb3cc3f4f198bc1d9`; exact match to R15 provenance: **YES**.
- DS0035 Zenodo record 17391295: 74069986 bytes; SHA-256 `b9760d3777006c8ae0f6b1db21eff1e8ca095bb685a6be8ebe96b6de1c8a56eb`; exact match to R15 provenance: **YES**.

## Independent feature extraction
A fresh R15B extractor was applied directly to the four redownloaded `Movie-FQ.TIF` files. It did not read or import the committed R15 feature CSVs during extraction. Each TIFF yielded 49 frames and a 49-column table (time index plus the frozen four-view panel and aggregate geometry features).
- DS0004: 49/49 rows, column order match, time indices match, max absolute numeric difference = 0.0e+00, nonzero numeric cells = 0.
- DS0005: 49/49 rows, column order match, time indices match, max absolute numeric difference = 0.0e+00, nonzero numeric cells = 0.
- DS0007: 49/49 rows, column order match, time indices match, max absolute numeric difference = 0.0e+00, nonzero numeric cells = 0.
- DS0035: 49/49 rows, column order match, time indices match, max absolute numeric difference = 0.0e+00, nonzero numeric cells = 0.

## Metric replication
- Primary DS0007 Gate 1: **PASS**, identical to R15. S-only R2: Ridge -0.01361825759942703; Random Forest 0.03068882877615342; Extra Trees 0.05665991553710925.
- Primary history deltas: Ridge -0.05399771243432694; Random Forest -0.008833647186484828; Extra Trees -0.008086432794827902.
- Secondary DS0035 Gate 1: **PASS**, identical to R15. S-only R2: Ridge 0.037072068378419254; Random Forest 0.03780146920728478; Extra Trees 0.03405586516999415.
- Secondary history deltas: Ridge -0.11269413584576948; Random Forest -0.015074103170071962; Extra Trees -0.0775617681208719.
- Maximum absolute primary metric discrepancy: 0.
- Maximum absolute secondary metric discrepancy: 2.2204460492503131e-16 (floating-point roundoff only).

## Discrepancies
No source-byte, SHA-256, feature-table, gate-decision, or substantive metric discrepancy was found. The only nonzero metric difference was 2.220446049250313e-16 in a secondary Extra Trees floating-point value, consistent with machine precision.

## Scope
This source-level replication closes the exact gap identified by R15A: it independently redownloaded the four released preview TIFFs, verified raw identity, regenerated the derived feature tables, and reproduced the frozen primary and secondary analyses. The scientific qualifications from R15/R15A remain unchanged: this is a small cross-embryo whole-image adequacy pilot and does not establish screening-off or history redundancy.

R15B_COMPLETE
