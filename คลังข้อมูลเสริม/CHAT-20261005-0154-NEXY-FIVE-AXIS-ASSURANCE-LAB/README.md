# NEXY Five-Axis Assurance Lab (FAAL)

**Status:** `EXPERIMENTAL / ADVISORY / AI-PROPOSED`  
**Authority:** none over NEXY.AI  
**Storage target:** AI-CONTEXT supplemental knowledge only  
**Protected target:** every repository whose name contains `NEXY.AI` remains read-only for this work.

FAAL is a standalone reference implementation of five complementary assurance primitives designed to be compatible with NEXY's evidence-first, fail-closed, deterministic architecture without modifying NEXY source.

## Why this lab exists

The inspected NEXY context already has strong work around evidence, privacy/context egress, pre-execution safety, operator contracts, intent integrity, proof capsules, directive epochs, localization, accessibility and other gates. This lab therefore does **not** create another generic firewall or preflight checker. It targets five different failure surfaces:

1. **Uncertainty Propagation Kernel (UPK)**  
   Prevent downstream claims from silently becoming more certain than their inputs. Any allowed uncertainty reduction needs an explicit bounded permit and new evidence.

2. **Change Impact Frontier (CIF)**  
   Convert a changed requirement/source/module into a deterministic downstream invalidation frontier: tests to rerun, evidence to stale and claims to revisit, with explanation paths.

3. **Swarm Independence Planner (SIP)**  
   Prevent "many agents" from masquerading as independent verification when they share provider, model family, context shard, tools or data sources. The score is a structural correlation index, **not** a probability.

4. **FSM Composition Guard (FCG)**  
   Preserve NEXY's rule that multiple state machines keep distinct semantics. Cross-machine bridges may emit events, but they never directly mutate a foreign machine state. Cyclic bridge compositions fail closed.

5. **Provenance-Preserving Context Compressor (PPCC)**  
   Reduce duplicated context only when equivalence is explicit and safe. Requirement coverage, provenance, unresolved truth states, dependencies and declared conflicts survive compression. Undeclared semantic disagreement freezes.

## Integrated advisory pipeline

```text
CHANGE
  -> Change Impact Frontier
  -> Uncertainty / release gate
  -> Swarm Independence Planner
  -> FSM Composition Guard
  -> Provenance-Preserving Context Compressor
  -> PASS or FREEZE advisory result
```

The bundle output is canonically serialized and SHA-256 identified. Equal canonical inputs produce an equal bundle identity under the tested conditions.

## Core invariants

- no network, subprocess, wall-clock, RNG or hidden environment reads in `nexy_faal/`;
- no floating-point literals in core assurance code;
- bounded integer uncertainty (`0..1,000,000 ppm`) and structural correlation (`0..100`);
- explicit `PASS`, `FREEZE` or input validation failure;
- deterministic sorting/canonicalization at set-like boundaries;
- canonical JSON + SHA-256 for advisory bundle identity;
- unresolved/conflicting context is never silently merged into resolved context;
- resource ceilings bound uncertainty fan-in, impact graph size, FSM composition, context records and swarm selection;
- all project code is isolated from the NEXY.AI implementation repositories.

## Repository layout

```text
01_DESIGN.md                  full architecture/design contract
02_REQUIREMENT_LEDGER.md      requirement -> implementation -> evidence map
03_THREAT_MODEL.md            attack/failure model
04_INTEGRATION_PROPOSAL.md    advisory-only NEXY integration concept
05_TEST_STRATEGY.md           red/green/audit strategy
nexy_faal/                    reference implementation
tests/                        71 unit + integration/resource-bound tests
scripts/                      independent verification utilities
evidence/                     raw verification outputs
PROJECT_MANIFEST.json         final payload inventory summary + SHA-256
FAAL_BUNDLE.tar.gz.b64        exact reproducible Design+Code+Test+Evidence bundle
00_SESSION_MEMORY.md          durable/resumable execution state
```

## Reproduce validation

After decoding/extracting the bundle:

```bash
PYTHONPATH=. python -m unittest discover -s tests -v
python -m compileall -q nexy_faal tests scripts
PYTHONPATH=. python scripts/verify_policy.py
PYTHONPATH=. python scripts/determinism_verify.py
PYTHONPATH=. python scripts/adversarial_verify.py
PYTHONPATH=. python scripts/mutation_sanity.py
```

## Evidence boundary

The tests prove behavior of this standalone reference implementation at the captured project bytes. They do **not** prove:

- NEXY.AI production integration;
- deployed runtime behavior;
- security of systems outside this lab;
- statistical independence of AI models;
- scientific calibration of uncertainty values;
- that no overlapping idea exists outside the inspected AI-CONTEXT scope.

Promotion into NEXY would require explicit user/project authorization plus mapping to current authoritative requirements and fresh integration/runtime evidence.
