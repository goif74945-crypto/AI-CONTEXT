# Lo4 Orthogonal Pentaforge — Engineering Design

**Classification:** AI-PROPOSED / Lo4 / EXPERIMENTAL / NOT CANON

## Architecture

```text
Authorized immutable inputs
          |
          +--> SQX  symmetry quotient --------------------+
          +--> CEFG causal explanation gate --------------+
          +--> RSEK robotics envelope --------------------+--> advisory reports
          +--> FPSA schedulability analysis --------------+         |
          +--> OEWC observational equivalence ------------+         v
                                                               future explicit adapter
                                                                        |
                                                                        v
                                                           existing NEXY authority/judge
```

The package is intentionally pure-data. It has no network, clock, randomness, filesystem mutation, subprocess, credentials, provider SDK, or NEXY implementation dependency.

## Numeric substrate: signed Q64.64

All continuous quantities and scores use `Q64`.

### Representation
`real_value = raw / 2^64`, with raw constrained to the signed 128-bit interval.

### Arithmetic law
- add/subtract: exact raw integer operations followed by signed-128 range check;
- multiply: `(a.raw * b.raw) / 2^64`, truncating toward zero;
- divide: `(a.raw * 2^64) / b.raw`, truncating toward zero;
- decimal parse: exact base-10 integer ratio, then Q64 conversion;
- no binary floating-point conversion is used.

### Failure law
Division by zero, malformed decimal input, invalid raw type, or signed-128 result overflow raises explicitly.

## SQX — Symmetry Quotient Explorer

### Purpose
Reduce duplicate finite states caused only by permutations of explicitly interchangeable entities.

### Input
- global state;
- entities with explicit `group` and canonicalizable attributes.

### Algorithm
1. canonicalize each entity attributes object;
2. group by explicit symmetry-group identifier;
3. sort member encodings inside each group;
4. canonicalize global state + grouped members;
5. bucket original input states by canonical key;
6. emit one representative per bucket.

### Invariants
- groups are explicit, never inferred;
- entities in different groups never collapse merely because attributes match;
- canonical key is order invariant inside a declared group;
- original indices are retained;
- `orbit_upper_bound` is deliberately an upper bound, not an exact orbit-size theorem.

### Complexity
For `n` states each containing `m` entities, dominated by canonical sorting inside groups, approximately O(n * m log m) plus serialization.

### Failure
Empty state set or empty symmetry-group name fails explicitly.

## CEFG — Causal Explanation Faithfulness Gate

### Purpose
Ensure an explanation references the explicit causal trace rather than unrelated, unknown, or post-hoc facts.

### Inputs
- causal fact IDs;
- mandatory explanation fact IDs;
- explicitly known noncausal fact IDs;
- explanation referenced fact IDs;
- Q64.64 minimum causal coverage.

### Outputs
- Q64.64 precision;
- Q64.64 causal coverage;
- unknown/noncausal/missing-mandatory sets;
- deterministic reason codes.

### Invariants
- mandatory IDs must be causal;
- an ID cannot be both causal and noncausal;
- unknown references fail;
- known noncausal references fail;
- missing mandatory causes fail;
- insufficient coverage fails.

### Limitation
The gate validates faithfulness against a supplied causal trace. It does not prove the supplied trace itself is causally correct.

## RSEK — Robotics Safety Envelope Kernel

### Purpose
Provide a deterministic pre-actuation motion-envelope calculation that is useful as an advisory gate but cannot become the sole physical safety mechanism.

### Formulae
- reaction distance = `speed * reaction_time`
- braking distance = `speed^2 / (2 * max_deceleration)`
- stopping distance = reaction + braking
- available distance = obstacle distance - safety margin
- clearance = available - stopping
- clearance ratio = available / stopping when stopping > 0

All formula quantities are Q64.64.

### Failure/reason codes
- `SPEED_LIMIT_EXCEEDED`
- `MARGIN_EXCEEDS_OBSTACLE_DISTANCE`
- `INSUFFICIENT_STOPPING_DISTANCE`

Negative physical quantities or nonpositive maximum deceleration are rejected.

### Safety boundary
No physical safety claim is permitted from this module alone. Real adoption requires controller-specific dynamics, uncertainty margins, actuator/brake behavior, sensor latency, HIL/physical evidence, and independent safety controls.

## FPSA — Fixed-Priority Schedulability Analyzer

### Purpose
Bound periodic task response times under fixed-priority interference.

### Priority convention
Smaller integer priority value means higher priority. Priority values themselves are discrete integers. Period, WCET, deadlines, interference, response time, and utilization are Q64.64.

### Response-time recurrence
For task i:

`R_next = C_i + sum(ceil(R / T_h) * C_h)` for all higher-priority tasks h.

The iteration converges when `R_next == R`, proves a deadline miss when `R > D`, or terminates with `ITERATION_LIMIT` when the configured proof budget is exhausted.

### Truth invariant
Iteration budget exhaustion is not relabeled as a deadline miss unless the computed response actually exceeds the deadline.

### Limitation
Reference model assumes the supplied periodic fixed-priority task abstraction. It does not model arbitrary blocking, jitter, multicore interference, cache effects, nonpreemptive sections, or distributed clocks.

## OEWC — Observational Equivalence Witness Compiler

### Purpose
Compare bounded traces only on contract-declared observable fields, allowing internal IDs or implementation details to vary without contaminating the equivalence claim.

### Algorithm
1. validate observable-field contract;
2. project every event onto included fields;
3. canonicalize projected values;
4. digest projected traces;
5. compare overlapping cells;
6. count length mismatch as unmatched observable cells;
7. emit Q64.64 match ratio and detailed mismatches.

### Invariants
- observable fields are explicit, unique, and required on every event;
- field order is deterministic;
- object insertion order does not affect canonical values;
- bounded equality does not imply universal semantic equivalence.

## Composition law

`PentaforgeSnapshot.advisory_pass` is true only when CEFG, RSEK, FPSA, and OEWC pass. SQX is a state-space reduction report rather than a legality verdict, so it is carried as evidence but does not itself promote or reject an action.

No composite result grants authority. An integrating NEXY boundary remains responsible for authorization, evidence-class requirements, and final FREEZE/PASS behavior.

## Security/trust boundary

All external data must be validated before it is treated as trusted input. The reference package contains no secret handling and no external execution. If future adapters add I/O, their trust boundary must be specified and separately tested.

## Version/evolution law

Any semantic change to Q64 rounding, canonicalization, observable projection, priority convention, robotics equations, or causal reason codes invalidates previous behavioral evidence and requires rerunning the full verification suite.
