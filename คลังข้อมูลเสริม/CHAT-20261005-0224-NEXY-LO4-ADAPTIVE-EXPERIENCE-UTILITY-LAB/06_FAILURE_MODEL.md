# Failure Model

## Fail-closed conditions

### Numeric core
- signed 128-bit overflow;
- division by zero;
- malformed decimal text;
- invalid unit-interval value.

### IURS
- empty/duplicate proposals;
- objective-set mismatch;
- protected objective without a weight;
- every proposal violates protected minima.

### COMET
- candidate already selected;
- missing pairwise overlap evidence;
- conflicting duplicate overlap evidence.

### SCTE
- duplicate surface ID;
- invalid/zero touch weight;
- invalid weight sum;
- surface/total complexity limit exceeded.

### DCPX
- duplicate candidate ID;
- unknown dependency/conflict;
- incomplete overlap matrix;
- reference exact-enumeration limit exceeded;
- no feasible portfolio.

### RIVP
- irreversible effect class;
- insufficient information gain;
- excessive risk/blast/sample budget;
- weak rollback confidence;
- option value below threshold;
- no control holdout.

## Important distinction
`FREEZE` means contract/evidence integrity is insufficient to make the decision. `HOLD` means inputs are valid but expected value/feasibility is insufficient. `REJECT` means an explicit safety/complexity/collision gate is violated.

## Recovery law
Correct the smallest failing input/contract/code defect, rerun the focused test, then rerun the complete suite and deterministic replay. Never convert missing evidence to a favorable default merely to make a proposal selectable.
