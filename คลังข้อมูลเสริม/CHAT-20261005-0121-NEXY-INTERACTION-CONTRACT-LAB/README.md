# NEXY Interaction Contract Lab

Status: **AI-PROPOSED / ADVISORY / IMPLEMENTED IN AI-CONTEXT ONLY**

This lab explores a missing control surface for future NEXY work: deterministic measurement of whether a user’s explicit directives survive the path from request → clarification → action → evidence → completion.

It does **not** infer intent from prose. It analyzes a structured interaction contract. That limitation is intentional: a detector that guesses what the user “probably meant” would violate the project’s zero-guess direction while pretending to protect it. Humans remain impressively capable of inventing contradictions without machine assistance.

## What it detects

- explicit directive conflicts;
- protected-scope access attempts;
- unauthorized scope expansion;
- redundant clarification of already-resolved directives;
- actions that depend on explicit assumptions;
- directives with missing/failed/unknown evidence;
- PASS claims with no evidence reference;
- premature COMPLETE claims.

## Outputs

The analyzer emits deterministic JSON with:

- `interaction_loss_score` (0 best, 100 worst);
- `retention_score` (100 best);
- effective outcome per directive;
- normalized findings;
- `completion_gate` = `PASS` or `BLOCK`.

## Run

```bash
python -m unittest discover -s tests -v
python -m interaction_contract.cli examples/good_session.json --pretty --fail-on-block
python -m interaction_contract.cli examples/bad_session.json --pretty --fail-on-block
```

No third-party dependencies are required.

## Boundary

This is an advisory research artifact stored in `AI-CONTEXT/คลังข้อมูลเสริม`. It is **not** an authoritative NEXY.AI requirement, and it does not modify the NEXY.AI repository.
