# NEXY Shadow Assurance Lab

**Status:** AI-PROPOSED / STANDALONE PROTOTYPE / NOT NEXY AUTHORITY  
**Location:** AI-CONTEXT supplemental knowledge only  
**Mutation boundary:** This project must not write to any repository whose name contains `NEXY.AI`.

## Purpose

Provide a safe pre-integration mechanism for comparing a stable NEXY-style decision stream against a candidate model, policy, refactor, provider, or subsystem in **shadow mode**. The candidate is evaluated but never granted execution authority by this prototype.

The core question is not "did the new model look smart?" It is: **did the candidate preserve authority, evidence obligations, safety/freeze behavior, and deterministic structure for the same proof context?** Humans do enjoy upgrading things and discovering three weeks later that the upgrade quietly removed the brakes. This lab exists to make that harder.

## What the prototype detects

- input mismatch / incomparable proof context;
- policy drift that requires a new authorized baseline;
- authority-chain removal, replacement, or reordering;
- stale evidence bound to the wrong revision;
- missing required evidence classes;
- evidence-obligation downgrade;
- stable `FREEZE`/`STOP` becoming candidate `RELEASE`;
- changed released action;
- removed safety labels;
- missing candidate coverage;
- unbaselined candidate cases;
- repeated identical candidate output;
- structurally different duplicate candidate output (nondeterminism signal).

## Non-goals

This prototype does **not** execute actions, deploy anything, claim production safety, validate all 837 current NEXY normalized requirements, or replace NEXY LAW/JUDGE/Safety Kernel. It does not treat a higher-numbered evidence class as an automatic substitute for another class.

## Quick run

```bash
python -m unittest discover -s tests -v
python -m shadowguard.cli fixtures/stable.jsonl fixtures/candidate_pass.jsonl --pretty
python -m shadowguard.cli fixtures/stable.jsonl fixtures/candidate_fail.jsonl --pretty
```

Expected CLI exit codes: `0=PASS`, `1=FAIL`, `2=input/tooling error`, `3=NOT_VERIFIED`.

## Integration shape

```text
stable decision records ─┐
                         ├─> Shadow Assurance Comparator -> Promotion Gate -> report only
candidate shadow records ┘                                  │
                                                            └─ no execution authority
```

NEXY may later choose to consume this report as one evidence input. Adoption requires an explicit NEXY integration decision and exact-revision verification. Nothing in this lab self-promotes into NEXY.
