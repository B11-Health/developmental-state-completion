# Prior art and novelty matrix

Status: conservative mapping from primary literature and repository evidence. No priority claim.

| Concept | Primary prior art / established result | Relation to T4 | Novelty disposition |
|---|---|---|---|
| Causal states / predictive equivalence | Crutchfield & Young (1989), *Inferring Statistical Complexity*; Shalizi & Crutchfield (2001), *Computational Mechanics: Pattern and Prediction, Structure and Simplicity*, J. Stat. Phys. 104:817-879. Histories grouped by identical conditional future laws; causal states are minimal sufficient predictive statistics under their assumptions. | Direct precedent for quotienting histories by future distributions. | **Known.** Do not claim screening-off or predictive equivalence as new. |
| Predictive state representations | Littman, Sutton & Singh (2001), *Predictive Representations of State*, NeurIPS; Singh, James & Rudary (2004), *Predictive State Representations: A New Theory for Modeling Dynamical Systems*, UAI. | Direct precedent for state represented by predictions of future action-observation tests. | **Known.** Intervention/test-indexed predictive state is established. |
| Observable operator models | Jaeger (2000), *Observable Operator Models for Discrete Stochastic Time Series*, Neural Computation 12:1371-1398. | Closely related observable predictive realization. | **Known.** |
| Input-output computational mechanics | Barnett & Crutchfield, epsilon-transducer work (2015-era computational mechanics literature). | Controlled/input-conditioned causal-state analogue. | **Known / close precedent.** |
| Nonlinear observability | Hermann & Krener (1977), *Nonlinear Controllability and Observability*, IEEE TAC 22(5):728-740. | Kernel/rank conditions and local distinguishability sit in this lineage. | **Known mathematics.** T4's ker Dh subset ker DF is a factorization condition, not a new observability law. |
| Nonlinear realization | Classical realization theory (e.g. Sussmann and Isidori traditions) constructs state from input-output behavior under regularity/minimality assumptions. | Relevant to turning response families into a state realization. | **Known field.** |
| Bisimulation for MDPs | Givan, Dean & Greig (2003), *Equivalence notions and model minimization in Markov decision processes*; Ferns, Panangaden & Precup (2004), *Metrics for Finite Markov Decision Processes*. | Formal state abstraction by equal/near-equal rewards and transition behavior. | **Known.** Approximate predictive equivalence strongly overlaps bisimulation metrics. |
| Approximate simulation relations | Girard & Pappas (2007), *Approximation Metrics for Discrete and Continuous Systems*, IEEE TAC; related approximate bisimulation work. | Supports metric/tolerance notions and robustness of abstractions. | **Known.** T4's 2 eta sandwich is a simple finite response-map bound. |
| Sufficient dimension reduction | Li (1991), *Sliced Inverse Regression for Dimension Reduction*, JASA; Cook's SDR theory. | Predictive sufficiency with low-dimensional regressors. | **Known.** Decoder-relative PCA findings are empirical, not intrinsic state dimension. |
| Information bottleneck | Tishby, Pereira & Bialek (1999), *The Information Bottleneck Method*; predictive information bottleneck / causal-state connections by Still and collaborators. | Compression retaining predictive information. | **Known.** Loss/information tradeoffs should be framed as established information theory. |
| Causal representation learning | Locatello et al. and Schölkopf et al. modern causal-representation literature; intervention-based identifiability work. | Mechanism-oriented representations under intervention. | **Broad established area.** T4 should not equate predictive sufficiency with causal-variable identification. |
| Test Cover / separating systems | Classical Test Cover / minimum test collection literature; pair separation can be written as coverage over unordered hypothesis pairs. | Exactly matches finite noiseless experiment-family identification. | **Known.** M2 already freezes this correction. |
| Adaptive submodularity | Golovin & Krause (2011), *Adaptive Submodularity: Theory and Applications in Active Learning and Stochastic Optimization*, JAIR. | Relevant only when objective/observation model satisfies adaptive-submodularity assumptions. | **Known.** M2/M3 show connected ambiguity does not inherit this automatically. |
| Weak submodularity | Das & Kempe (2011), *Submodular meets Spectral* / submodularity-ratio framework. | M2 uses restricted ratio diagnostically. | **Known diagnostic.** No global certificate claimed. |
| Robust/minimax subset selection | Robust submodular optimization literature (e.g. Krause et al. robust observation selection traditions). | Pointwise minimum can destroy submodularity; exact certification is appropriate on the finite 16-context bundle. | **Known field + project-specific negative boundary.** |

## Search record
The isolated research browser on CDP 9444 was used on 2026-08-30. Google Scholar itself returned an unusual-traffic block, so the pass used ordinary Google results to reach primary/publisher or author-hosted records. Verified search hits included Shalizi & Crutchfield's causal-state paper on arXiv/Santa Fe Institute; Littman-Sutton-Singh's 2001 NeurIPS paper on the NeurIPS proceedings site; and the established Hermann-Krener observability citation. Search snippets were treated only as navigation/metadata, not as evidence for project claims.

## Potentially novel synthesis — phrased deliberately weakly
The defensible candidate contribution is **not a new state concept**. It is a cross-domain synthesis that combines:

1. calibrated residual-history value as an empirical *incompleteness diagnostic* for a declared developmental H/S/Y task;
2. intervention-family expansion as an explicit way to refine the predictive equivalence relation when old history reappears;
3. finite response-family identification linked to Test Cover while keeping a distinct topology-aware connected-ambiguity objective;
4. robustness margins for approximate response fibers, with explicit acknowledgment that connected-component topology can change discontinuously without a gap;
5. a biological workflow that separates task-relative predictive completion from mechanistic/causal completeness and from full-organism Markov claims.

Whether that *combination* is publishably novel requires a deeper systematic literature review; T4 makes no priority claim.

## Strong novelty claims that are prohibited
- 'We invented predictive state sufficiency.'
- 'We discovered causal states for biology.'
- 'Interventional future predictions as state are new.'
- 'The kernel condition is a new observability theorem.'
- 'Test Cover or pair-separation experiment design is new.'
- 'Connected ambiguity is generally submodular or greedy-approximable.'
- 'History screening-off proves mechanistic state completion.'
