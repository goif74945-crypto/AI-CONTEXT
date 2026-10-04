# NNIK Threat Model

**Status:** AI_PROPOSED / SECURITY REVIEW AID

## Assets protected

- correctness of numeric accept/reject/freeze decisions;
- dimensional integrity;
- deterministic replay/conformance;
- bounded verifier resource usage;
- provenance of registry and normalized result identities.

## Trust boundaries

Raw contract and observation input are untrusted. The built-in unit registry is trusted only at its exact `registry_digest`. Future custom registries must be separately authorized/versioned.

## Threats and controls

| Threat | Failure mode | Control | Evidence |
|---|---|---|---|
| Binary float ingress | silent representation drift | Python `float` forbidden; CLI number tokens preserved as strings | E2 tests |
| Unit spoof/typo | wrong dimension/conversion | closed exact symbols; unknown unit freezes | E2 tests |
| Cross-dimension comparison | semantically invalid threshold | explicit dimension check | E2 tests |
| Affine-unit uncertainty bug | applying temperature offset to delta | separate scale-only `convert_delta` | E2 test |
| Hidden rounding | boundary decision changes | rounding only with explicit quantum+mode | E2 tests |
| Boundary uncertainty | false certainty near threshold | partial overlap => FREEZE | exhaustive E2 oracle test |
| Huge exponent/integer | exact-arithmetic resource exhaustion | numeric text/digit/exponent/bit limits | E2 tests |
| Huge CLI payload | JSON memory/CPU abuse | 1 MiB pre-parse file cap | E2 test |
| Dynamic code/network | injection/exfiltration | no eval/exec/network/subprocess imports in package | static AST audit |
| Fixed128 truncation | rational silently rounded into Core form | exact divisibility required | E2 tests |
| Fixed128 overflow | canonical wrap/saturation | range check => FREEZE | E2 tests |
| Registry drift | different conversions under same assumption | registry digest in result | E2/stability test |
| Cross-language drift | port disagrees with reference | golden vectors | E2 regeneration test |

## Residual risks

- No formal proof of arithmetic implementation correctness.
- Python big-integer/Fraction runtime itself is trusted.
- 1 MiB is a proposal-level safety default, not a canonical NEXY limit.
- Physical sensor uncertainty semantics are domain-specific and not modeled beyond an explicit absolute interval.
- Locale parsing is intentionally unsupported rather than inferred.
- Custom unit registries could be unsafe if future integration allows them without authority review.
