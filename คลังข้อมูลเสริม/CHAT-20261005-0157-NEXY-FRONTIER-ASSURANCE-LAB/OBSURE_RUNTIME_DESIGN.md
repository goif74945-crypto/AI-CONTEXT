# OBSURE Runtime Witness Certification — Design

**Classification: AI-PROPOSED / EXPERIMENTAL / NOT CANON / NOT NEXY.AI IMPLEMENTATION**

## Gap being deepened

The original OBSURE gate proves that a telemetry *specification* declares the
phases and fields required for an effect. It explicitly does not prove that a
runtime emitted those events. This continuation deepens OBSURE without adding
a sixth mission concept.

## Objective

Certify a bounded, completed runtime witness only when:

1. the original OBSURE specification gate passes;
2. every observed event resolves to one admitted event specification;
3. required field values are present and non-empty;
4. `trace_id`, `action_id`, and `effect_id` remain correlated;
5. lifecycle sequence numbers are unique, non-negative integers;
6. the lifecycle is exactly `INTENT -> START -> SUCCESS|FAILURE`;
7. the terminal phase matches the declared run expectation; and
8. compensation is present, ordered, and legal exactly when declared.

Any violation returns `FREEZE`; it never repairs, reorders, or invents events.

## Explicit contracts

- `RuntimeEvent`: event name, effect ID, sequence, and actual field values.
- `EffectRunExpectation`: expected terminal phase plus whether compensation is
  required for this run.
- `RuntimeWitnessCertifier.certify`: runtime-only witness validation.
- `ObsureRuntimeAssurance.assess`: integration adapter that runs the original
  OBSURE specification gate before witness certification.

## Failure semantics

The result contains deterministic, sorted issue records and a SHA-256 result
hash. Empty input, duplicate IDs/names/sequences, unknown events/effects,
unsupported values, incomplete traces, terminal ambiguity, illegal
compensation, correlation drift, and ordering defects fail closed.

## Non-duplication boundary

Repository-wide inspection found the original OBSURE specification gate and a
separate human-interaction trace conformance lab. No prior artifact was found
that certifies actual side-effect telemetry against OBSURE event schemas. This
work is restricted to machine side-effect lifecycle witnesses; it does not
evaluate human interaction friction, consent, or presentation behavior.

## Limits

- Input is an already-collected bounded event set; collection authenticity is
  not proven.
- Sequence numbers are logical order supplied by the caller, not trusted wall
  clock time.
- Hashing proves deterministic content identity, not signer identity.
- No production, deployment, NEXY.AI adoption, or live integration claim is
  made.
