# Architecture

The lab is intentionally five independent pure-function engines rather than a mini-platform. Their common contract is deterministic, JSON-compatible input/output and fail-closed validation.

```text
NEXY adapter (future, not implemented here)
       |
       +--> Minimal-Cut Failure Geometry ----> fragility cut sets
       +--> Liveness / Deadlock Sentinel ----> progress classification
       +--> Dependency Dominator Analyzer ---> chokepoints
       +--> Symmetry State-Space Reducer ----> equivalence key
       +--> Lo4 Mutation Tournament ----------> recommendation only

                     NO CANON WRITE PATH
```

## Integration law
- Each engine is advisory/analytical.
- NEXY remains final authority.
- A future adapter must validate schemas at the boundary and translate results into NEXY-native types.
- No result is a substitute for DOC-B/C/D/E requirements or runtime evidence.
- Tournament output explicitly contains `promotion_permitted: false` and `authority: EXPERIMENTAL_ONLY`.

## Why Python stdlib
The reference implementation is deliberately dependency-light and portable. Python is not proposed as the required NEXY runtime language. The algorithms expose language-neutral structures that can be independently ported to TypeScript/Rust and tested against golden vectors later.
