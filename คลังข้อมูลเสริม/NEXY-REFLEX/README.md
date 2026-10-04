# NEXY-REFLEX

**Requirement & Evidence Freshness, Lineage, Exception eXaminer**

Standalone deterministic shadow verification lab designed to work *alongside* NEXY without entering or mutating the NEXY.AI repository.

## What it does
- resolves explicit authority precedence without guessing;
- freezes on conflicting highest-authority values;
- rejects stale evidence bound to another target revision/digest;
- requires explicitly accepted evidence classes;
- validates requirement dependency integrity;
- calculates transitive evidence invalidation after changes;
- emits canonical, replayable SHA-256 decision digests.

## What it does not do
- modify NEXY;
- become NEXY::JUDGE;
- infer implementation state from design documents;
- treat the 837 normalized NEXY source rows as implementation proof;
- use AI output as authority.

## Quick start

```bash
cd คลังข้อมูลเสริม/NEXY-REFLEX
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m nexy_reflex.cli evaluate examples/pass.snapshot.json
```

A successful gate returns exit code `0`. Any valid non-PASS gate result returns exit code `2`. Input errors return `4`.

## Files
- `docs/00-MISSION.md` — scope and immutable mission contract.
- `docs/01-DESIGN.md` — architecture and semantics.
- `docs/02-INTEGRATION-CONTRACT.md` — read-only NEXY compatibility boundary.
- `docs/03-THREAT-MODEL.md` — threats and limitations.
- `docs/04-AI-PROPOSALS.md` — future ideas, explicitly concept-only.
- `contracts/` — input/output JSON Schema contracts.
- `src/nexy_reflex/` — implementation.
- `tests/` — unit/regression suite.
- `examples/` — deterministic PASS and conflict examples.
- `state/WORKING-MEMORY.md` — resumable execution state.
- `evidence/` — executed verification record.

## Truth boundary
This project can prove properties of the exported snapshot it receives and of its own deterministic evaluation logic. It cannot, by itself, prove NEXY runtime, deployment, security, UI, or physical-system behavior.
