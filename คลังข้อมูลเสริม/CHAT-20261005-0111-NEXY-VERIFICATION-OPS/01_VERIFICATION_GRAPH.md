# Verification Graph for NEXY-class Systems

## Purpose
A claim is releasable only when its required evidence graph is closed. “Code exists” is not equivalent to “behavior works”.

## Graph model
Each requirement R maps to one or more claims C. Each claim maps to an evidence class E and freshness boundary F.

R → C → E → validator → result → artifact → provenance → release decision

A missing edge yields NOT_VERIFIED, not PASS.

## Evidence classes
| Claim | Minimum evidence |
|---|---|
| syntax/type correctness | parser/compiler/typechecker |
| pure logic | focused deterministic tests |
| persistence behavior | integration test against real test datastore |
| provider integration | controlled integration evidence |
| UI interaction | browser/E2E evidence |
| authorization | negative + positive auth tests |
| concurrency | concurrent execution/replay test |
| recovery | induced failure + recovery proof |
| deployment | exact deployment/environment observation |
| performance | measured workload with declared environment |
| security property | threat-specific test/review evidence |
| physical safety | independent physical/HIL evidence |

## Closure rules
1. Evidence must identify exact target version/commit/config.
2. Stale evidence cannot prove a changed target.
3. A lower evidence class cannot substitute for a higher one.
4. Negative-path evidence is mandatory for freeze/fail-closed claims.
5. Any critical UNKNOWN keeps the dependent claim open.
6. PASS requires reproducible evidence location and validator outcome.

## Anti-patterns
- screenshot proves backend correctness
- unit test proves deployment
- design document proves implementation
- one happy-path test proves safety
- model confidence proves anything at all

## Release invariant
No critical output crosses the trusted boundary while any required critical evidence node is FAIL, UNKNOWN, CONFLICT, or NOT_VERIFIED.
