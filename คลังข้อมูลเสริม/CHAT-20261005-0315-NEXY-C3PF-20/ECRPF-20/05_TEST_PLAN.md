# Verification Plan

Quality gates:

- strict TypeScript compilation;
- 20 mechanism surface exists in every successful evaluation;
- Q64.64 overflow/divide-by-zero fail closed;
- Q64 signed multiplication follows truncation-toward-zero reference behavior;
- zero/full rollout boundaries;
- canonical proof determinism across repeated runs;
- proof invariance under rule/entry reordering;
- unknown/missing/forbidden key rejection;
- integer/range rejection;
- plaintext and wrong-provider secret rejection, including lower-precedence injection;
- same-precedence ambiguity fail closed;
- dependency/conflict rejection;
- production fail-open rejection while explicit development-only mode remains representable;
- immutable build drift rejection;
- rollout direction/max-step/one-ULP boundary checks;
- rollback target closure;
- orphan dependency rejection;
- Q64 blast-radius behavior;
- non-authoritative handoff assertions;
- mutation matrices for fail-open and plaintext secret attacks;
- source audit for wall-clock/randomness/eval/network and binary floating-point decision arithmetic;
- exact SHA-256 manifest after final test bytes.
