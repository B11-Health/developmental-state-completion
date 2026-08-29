# Claim-language style guide

## Core newsroom rule

**Name the evidence class before choosing the verb.** The same sentence structure must not be used for observed-data reanalysis, simulator evidence, mathematics, historical reports, and future living validation.

## Required evidence labels and verbs

### 1. OBSERVED-DATA REANALYSIS

Use verbs such as:

- “reanalysis supports”
- “we observe in the released dataset”
- “is consistent with”
- “shows no stable material gain under the tested analyses”
- “is estimator/split sensitive”

Avoid:

- “proves biology is…”
- “demonstrates universal…”
- “establishes exact conditional independence”

Required qualifier for FM1:

> task-, stage-, compartment-, representation-, loss-, decoder-, and finite-sample-relative

Required measurement caveat:

> the 25 FM1 channels are integrated binary atlas annotations, not 25 simultaneous longitudinal molecular measurements in the exact same living cells

### 2. SIMULATOR EVIDENCE

Use verbs such as:

- “the simulator reproduces”
- “the frozen source-simulator test supports”
- “within this restricted model”
- “passed the preregistered simulator thresholds”

Avoid:

- “validated in biology”
- “proves this works in plants”
- “shows two perturbations are universally sufficient”

Required phrase for C17:

> prospective source-simulator validation, not living-plant validation

### 3. MATHEMATICAL RESULT

Separate three kinds of statements:

**Established mathematics / identity:** say “standard,” “classical,” or “strongly precedented.”

**Project-specific theorem/counterexample:** say “we proved for the stated assumptions” or “we constructed/reproduced a counterexample for this exact objective.”

**Proxy-dependent computation:** name the proxy explicitly and do not convert it into a theorem about the biological world space.

Never claim priority for:

- predictive states / causal states / PSRs
- input-output computational mechanics
- observability or structural identifiability
- Reeb spaces / Stein factorization
- set cover / Test Cover
- submodularity or adaptive submodularity
- generic finite-dimensional embedding/transversality arguments

### 4. HISTORICAL / PROVENANCE-INCOMPLETE

Mandatory verbs:

- “historically reported”
- “provenance-incomplete”
- “not independently recovered”
- “not currently reproducible from the recovered artifact chain”

Never write:

- “our experiment showed” if the original source/output bundle is missing
- “replicated” for the exact `0.272 -> 0.643` pair
- “the 224-world experiment is reproducible”
- any historical topology threshold or ranking number as a current measured result

If a newer experiment is nearby, explicitly state that it is **separate** rather than using it to repair the old claim.

### 5. PROSPECTIVE LIVING VALIDATION

Use future/proposal verbs:

- “we plan to test”
- “the preregistered design proposes”
- “is gated by”
- “would count as a falsifier”

Never write:

- “validated in living plants”
- “confirmed in Arabidopsis”
- “designed perturbations outperform random controls” before the comparator exists and is run
- “materials are available” unless transfer/stock availability is actually confirmed

## Novelty language

Preferred:

> The candidate contribution is not a new definition of state or a new topology, but a falsifiable experimental workflow for measuring when a developmental state is predictively sufficient and for choosing perturbations against the specific mechanism ambiguity that remains.

Allowed:

- “candidate contribution”
- “task-specific integration”
- “we did not identify a single paper combining these exact pieces in this developmental setting in the current red-team pass”

Forbidden without a dedicated priority review:

- first ever
- unprecedented
- completely new
- rewrites biology
- solves development
- new mathematical field
- invented predictive state
- invented connected-fiber topology

## Universal statements to ban

Do not publish:

- “development is Markovian”
- “the plant forgets its past”
- “history is useless once the present is measured”
- “one molecular dimension controls flower development”
- “our simulations prove a biological law”
- “our algorithm finds the optimal experiment”
- “identical phenotypes hiding different mechanisms is our discovery”

## Numerical style

1. Give cohort and task before a performance number.
2. Distinguish fixed split, repeated split, bootstrap interval, and partition quantiles.
3. Never call partition quantiles confidence intervals.
4. If estimator families disagree, report the disagreement; do not average it away.
5. Do not quote historical numbers without the label “historically reported / provenance-incomplete.”
6. For very specific simulator metrics, say “within the restricted source simulator.”
7. Do not turn “no material incremental gain under tested decoders” into “zero information.”

## Platform compression rules

### LinkedIn / GitHub / press page

May include full qualification and evidence classes.

### YouTube description

First three sentences should state: what was tested, strongest surviving result, and what has **not** been validated.

### TikTok / short social caption

Never shorten away both of these points:

1. the result is task-specific/reanalysis or simulator-based; and
2. living-plant validation is still prospective.

If character pressure is high, delete numerical detail before deleting qualifiers.

## Headline test

Before approving a headline, ask:

> Could a reasonable reader infer living validation, universal biology, exact causal closure, or mathematical priority from this headline alone?

If yes, rewrite it.

## Five evidence badges for internal drafting

Use these exact tags in working drafts when useful:

`[OBSERVED-DATA REANALYSIS]`
`[SIMULATOR EVIDENCE]`
`[MATHEMATICAL RESULT]`
`[HISTORICAL / PROVENANCE-INCOMPLETE]`
`[PROSPECTIVE LIVING VALIDATION]`
