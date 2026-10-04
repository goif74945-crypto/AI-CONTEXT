# Threat Model

## Assets protected
- correctness of gate result;
- authority ordering supplied by the caller;
- evidence freshness semantics;
- deterministic replay identity;
- isolation from NEXY mutation.

## Threats and controls

| Threat | Control | Residual limitation |
|---|---|---|
| Stale evidence reused after code/state change | revision + optional content digest binding | exporter must provide trustworthy identity |
| Conflicting rules silently merged | same-highest-authority conflict freezes | semantic keys must be normalized by exporter |
| Stronger-looking evidence class substituted incorrectly | exact accepted class list | requirement contract must name acceptable classes correctly |
| Input-order nondeterminism | canonical JSON + deterministic sorting | semantic equivalence beyond JSON equality is not inferred |
| Orphan proof attached to deleted requirement | orphan evidence blocks | deleted evidence outside snapshot is invisible |
| Dependency corruption | missing dependency and cycle detection | dependencies omitted by exporter cannot be reconstructed |
| Tool compromises NEXY | no NEXY mutation capability required | caller must actually deploy with least privilege |
| Malformed JSON exploits parser ambiguity | standard JSON parser + strict typed validation | resource-exhaustion limits are not implemented in v0.1 |

## Trust boundary
REFLEX trusts only the bytes it receives enough to parse them. It does not treat provenance strings as proof. A provenance field is descriptive metadata, not a cryptographic attestation.

## Security status
- No network access in core engine: **DESIGN FACT**.
- No secrets required by core engine: **DESIGN FACT**.
- Resistance to maliciously huge input: **NOT_VERIFIED / NOT IMPLEMENTED**.
- Sandboxing in a target deployment: **NOT_VERIFIED**.
- Cryptographic signer verification: **NOT IMPLEMENTED**.
