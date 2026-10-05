# GHOSTEDGE Controlled Campaign Sufficiency — Design

**Classification: AI-PROPOSED / EXPERIMENTAL / NOT CANON / NOT NEXY.AI IMPLEMENTATION**

## Verified gap

Fresh execution showed the original experimental GHOSTEDGE returning `CLEAN`
for zero experiments. It also emitted a dependency candidate from two failing
interventions without any sham/control observation, so the same evidence could
not distinguish intervention-specific failure from baseline failure.

This continuation deepens GHOSTEDGE; it does not add a sixth mission concept.

## Objective

Admit a hidden-dependency conclusion only after a complete bounded campaign:

1. every declared perturbation source receives a minimum intervention count;
2. a minimum sham/control count exists;
3. every intervention observes exactly the contract-declared targets;
4. every sham observes the union of campaign targets;
5. failures are a subset of observed targets;
6. identifiers and observation entries are unique;
7. declared-dependency input is structurally valid;
8. intervention failure rate meets hit and ratio thresholds; and
9. intervention rate exceeds sham rate by a declared integer lift threshold.

Insufficient campaign evidence returns `FREEZE`, not `CLEAN`.

## Contracts

- `PerturbationCampaignContract`: exact source/target matrix and evidence floors.
- `CampaignExperiment`: `INTERVENTION` or `SHAM` observation.
- `ControlledCampaignDetector`: coverage gate plus controlled dependency signal.
- `GhostedgeCampaignAssurance`: integration adapter comparing the original
  detector with the controlled result. An uncontrolled candidate rejected by
  sham evidence freezes as a disagreement rather than being silently erased.

## Determinism

All inputs are normalized by identifiers and names. Ratios use integer
thousandths only. Gaps, candidates, and hashes have stable ordering.

## Non-duplication boundary

Repository-wide keyword inspection found broad causal, confounder, and
negative-control research, but no existing artifact combining GHOSTEDGE's
hidden dependency detector with an exact observation matrix, fail-closed empty
campaign handling, sham baseline, and minimum failure-rate lift. This artifact
owns only that narrow GHOSTEDGE evidence-sufficiency gap.

## Limits

- Sham balance reduces one confounding class; it does not prove causality.
- Experiment assignment, environment equivalence, and observation authenticity
  are caller obligations and remain unverified.
- Integer rate thresholds are bounded descriptive checks, not statistical
  confidence claims.
- No canonical, production, deployment, or NEXY.AI implementation claim is
  made.
