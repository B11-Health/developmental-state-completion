# LAB LANE B1 — Minimum Collaboration / Material Questions for the Tsiantis Group

Purpose: exact questions needed to convert the source-supported design into a runnable Phase-0 pilot. These are questions to ask later; **no contact has been made**.

## A. RCOg-V suppressor material

1. Do you currently have viable seed for homozygous `RCOg-V`, `cuc2-4;RCOg-V`, `cuc2-5;RCOg-V`, `cyp71-3;RCOg-V`, `nop2a-5;RCOg-V`, and `nop2a-6;RCOg-V`?
2. For each available line, what is the exact genotype/zygosity of the suppressor allele and the RCOg-V transgene in the seed stock you would provide?
3. Are any of these lines deposited in a public stock center? If yes, what are the accession numbers? If not, can they be shared directly for academic collaboration?
4. Are there MTA, redistribution, attribution, or third-party restrictions on any of these lines or on the RCOg-V construct?
5. Are there known fertility, vigor, germination, or propagation issues for the exact stocks beyond those reported in Wang et al.?
6. Are there linked background mutations or backcross-generation details we should treat as material confounders in a blinded genotype-decoding study?
7. Do you recommend `cyp71-3` or `nop2a-5` as the cleaner post-initiation suppressor for a small prospective live-imaging pilot, based on stock quality and phenotype penetrance rather than on our desired result?

## B. PIN1:GFP and inducible ChCUC1 material

8. Do you currently have the *A. thaliana* `PIN1p::PIN1:GFP` line used with the Hu dex-inducible ChCUC1 system?
9. Do you currently have either of the two representative `ChCUC1p::LhG4:GR; Op::ChCUC1:tdTomato; PIN1p::PIN1:GFP` lines used for the published dex experiment?
10. Can those lines/constructs be shared, or do any components require permission from another lab or separate MTA?
11. What selectable markers are carried by RCOg-V, PIN1:GFP, and the inducible ChCUC1 construct, and do any marker combinations make the proposed crosses impractical?
12. Are there known linkage relationships or transgene-silencing issues that would materially complicate combining these reporters with `cuc2-4`, `cyp71-3`, or `nop2a-5`?
13. Has anyone in the group already combined RCOg-V with PIN1:GFP and/or the dex-inducible ChCUC1 system in any suppressor background, even if unpublished? If yes, what was observed and what can be treated as preliminary rather than published evidence?
14. Does adding the inducible ChCUC1 system produce an obvious phenotype before dex exposure in any relevant background?

## C. Exact dex/mock transfer

15. For the published *A. thaliana* leaf-4 assay, should we reproduce the SI condition exactly as the Phase-0 starting point: 10 µM dexamethasone + 0.01% Triton X-100 spray, DMSO-matched mock, treatment when leaf 3 is visible, imaging leaf 4 24 h later?
16. Is there any unpublished handling detail critical to reproducing that assay—spray volume, number of sprays, time of day, humidity, recovery conditions, dissection timing, or leaf-length window—that is not explicit in the SI?
17. In your experience, is leaf length still the best operational staging variable for the PIN1 polarity readout in these backgrounds, or should another developmental marker be frozen instead?
18. What leaf-4 length window would you use for a feasibility cohort before any genotype-decoding analysis?
19. Would you expect the same dex condition to be biologically tolerable in `cuc2-4`, `cyp71-3`, and `nop2a-5`, or should Phase 0 explicitly test a small dose-response before selecting the confirmatory condition?
20. What objective criterion would you use to call a specimen “successfully induced” without using genotype-separation performance?

## D. Imaging and readout feasibility

21. Can RCO-VENUS, PIN1:GFP, and ChCUC1:tdTomato be imaged in the same living specimen with acceptable spectral separation on your current confocal setup?
22. If not, which two channels would you prioritize for the smallest defensible pilot?
23. Is repeated imaging of the same developing leaf before treatment and 24 h later technically realistic without causing enough handling/dissection burden to confound growth?
24. If repeated imaging is not realistic, would you recommend paired sibling/cohort baselines rather than pretending we have within-leaf change measurements?
25. Can the published PIN1 polarity classes and reversal-distance measurement be scored reliably in `cuc2-4` leaves that may have smoother margins and altered RCO expression pattern?
26. Would you retain manual polarity scoring by two blinded readers, or is there a validated automated/semi-automated pipeline you would trust enough to freeze prospectively?
27. What acquisition failure modes should be preregistered—poor membrane signal, saturation, segmentation failure, wrong developmental stage, tissue damage, or others?

## E. Physiological burden / interpretability

28. What is the smallest burden panel you consider sufficient to distinguish a developmental response from gross treatment injury over the 24-h assay window?
29. Is short-window leaf area/length growth versus mock feasible in the same specimens, or would imaging manipulation make that measure misleading?
30. Do you recommend any validated stress or cell-death readout already present in your workflow, or should the pilot stay with visible injury/survival plus growth/developmental delay?
31. What level/pattern of tissue damage would make you reject a dex condition as uninterpretable before looking at decoding performance?

## F. Equal-cost/random perturbation comparator

32. What alternative perturbation would you consider biologically legitimate as a comparator that is not designed specifically around the ChCUC1→PIN1 margin-patterning mechanism?
33. Can that comparator be applied at the same leaf stage and scored over a comparable response window?
34. What burden measure would you trust for matching the comparator to the active ChCUC1 perturbation prospectively?
35. Does the comparator require a different vehicle or procedure-specific mock?
36. Is there any reason the comparator would directly perturb PIN1 polarity or RCO expression and therefore fail as a nominally non-targeted comparator?
37. If no defensible equal-cost comparator exists, do you agree the first experiment should be framed only as “response adds information beyond baseline,” with no claim of optimal/targeted intervention superiority?

## G. Future outcome and propagation

38. Which later outcome can be measured from the same treated leaf with the least additional intervention: mature leaf margin complexity, a fixed shape-space coordinate, lobe count, or another quantitative trait?
39. At what age/stage should that outcome be acquired to minimize stage ambiguity?
40. Can treated/imaged plants be returned to growth reliably enough to obtain that future outcome from the same leaf?
41. Would the imaging/dissection itself alter the later morphology enough to require a no-imaging handling control?

## H. Cross-allele validation

42. If the primary CUC2 result is positive, is `cuc2-5;RCOg-V` the best available independent-allele replication despite its reported weaker/variable initiation phenotype?
43. If NOP2A is used, are `nop2a-5` and `nop2a-6` sufficiently independent stocks/backgrounds for an allele-transfer test after the necessary backcross/genotyping controls?
44. Are there any cleaner independent alleles already in hand that would be preferable but were not part of the Wang suppressor paper?

## Minimum collaboration/material package

The smallest transfer/collaboration package needed for a Phase-0 pilot is:

- one verified RCOg-V stock;
- `cuc2-4;RCOg-V`;
- one post-initiation suppressor (`cyp71-3;RCOg-V` or `nop2a-5;RCOg-V`, chosen by material quality/feasibility);
- a functional `PIN1p::PIN1:GFP` source;
- one published representative `ChCUC1p::LhG4:GR; Op::ChCUC1:tdTomato` line or the exact construct/source needed to recreate it;
- genotype/marker information sufficient to design crosses;
- permission/terms needed to transfer those materials;
- access to a confocal workflow capable of the published GFP/VENUS/tdTomato assay;
- collaborator nomination of a biologically legitimate equal-cost comparator, if the stronger intervention-selection claim is to be tested.

No request should be sent until the project lead reviews this list.
