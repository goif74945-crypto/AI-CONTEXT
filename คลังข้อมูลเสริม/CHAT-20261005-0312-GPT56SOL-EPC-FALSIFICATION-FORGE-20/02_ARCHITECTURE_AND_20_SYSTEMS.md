# Architecture and Twenty Lo4 Systems

## Architecture

The forge is a pure advisory library. It accepts normalized proposal/requirement material and emits immutable experiment contracts or advisory evidence records. It has no repository writer, database client, network client, clock, random source, provider adapter or state-transition API.

### Layers

1. **Q64 substrate** — checked signed Q64.64 (`src/q64.ts`).
2. **Hypothesis compiler** — turns requirements into falsifiable contracts.
3. **Experiment planners** — produce canonical counterexample/boundary/fault/assumption/replay probes.
4. **Evidence selectors and metrics** — Q64 deterministic information/cost/independence calculations.
5. **Reproducibility layer** — canonical capsule construction and deterministic non-security checksum.
6. **Advisory dossier** — packages results; never promotes or changes NEXY state.

All collection outputs are canonicalized before decision use. Critical malformed inputs throw `ForgeError` or `Q64Error` rather than falling back.

## Twenty mechanisms

| # | ID | System | Objective | Inputs | Outputs | Fail-closed behavior | Future NEXY integration surface |
|---:|---|---|---|---|---|---|---|
| 1 | RHC | Requirement-to-Hypothesis Compiler | Convert a requirement into an explicit claim plus falsifiers | requirement ID, statement, invariants, evidence obligations | immutable hypothesis contract | empty requirement/invariant/evidence rejected | consume normalized requirement rows before Lo4 evaluation |
| 2 | FG | Falsifiability Gate | Reject claims that cannot be disproven observably | claim, falsifiers, observables | PASS contract only | no falsifier/observable => exception | pre-screen proposal experiments before verification allocation |
| 3 | MFP | Minimal Falsifier Planner | Find exact minimum-total-Q64-cost experiment set covering required hypotheses | candidate falsifiers, Q64 costs, hypothesis coverage | exact deterministic selected set | uncovered hypothesis, cost overflow, >128 bounded exact problem => exception | optimize expensive verification campaigns without changing verdict authority |
| 4 | CNEP | Constraint-Negation Experiment Planner | Test one constraint violation at a time | hypothesis + constraints | isolated negation experiments | empty constraints rejected | derive negative tests from LAW/constraint contracts |
| 5 | BCPP | Boundary Condition Probe Planner | Probe just outside/on/inside declared Q64 limits | metric, min, max | 6 canonical Q64 probes | inverted/unrepresentable edge rejected | augment fixed-point boundary suites |
| 6 | FIEP | Fault Injection Experiment Planner | Turn declared dependency faults into explicit containment tests | fault identifiers | canonical injection plans | no faults rejected | verification fixture source for timeout/dependency/corruption paths |
| 7 | AKEP | Assumption-Kill Experiment Planner | Attack every stated proposal assumption directly | assumption ID + statement | assumption violation experiments | duplicate/empty assumptions rejected | make hidden assumptions visible before promotion review |
| 8 | DES | Discriminating Evidence Selector | Prefer evidence that distinguishes competing outcomes per cost | discrimination Q64, cost Q64 | best deterministic evidence choice | invalid unit metric / non-positive cost rejected | prioritize verification work under bounded resources |
| 9 | OTP | Oracle Triangulation Planner | Compare independent evidence roots instead of one oracle monoculture | oracle IDs + roots | cross-root disagreement pairs | <2 independent roots rejected | schedule independent verifier/tool/provider evidence checks |
| 10 | EIYE | Evidence Information-Yield Estimator | Quantify discriminating outcome coverage adjusted by source independence | outcome counts + Q64 independence | Q64 yield | invalid counts/range rejected | advisory verification-efficiency metric only |
| 11 | SES | Sequential Evidence Stopper | Stop experimentation conservatively on strong refutation or enough evidence for external review | support/refutation + thresholds Q64 | FALSIFIED / ENOUGH_FOR_REVIEW / CONTINUE | out-of-unit inputs rejected | reduce unnecessary experiments; cannot promote |
| 12 | CDM | Counterexample Delta Minimizer | Prefer the smallest reproducible counterexample | counterexample IDs, Q64 deltas, witnesses | minimal counterexample | empty/negative delta rejected | shrink regression reproductions before handoff |
| 13 | ESM | Environmental Sensitivity Matrix | Measure outcome variation across environments | environment metric maps | per-metric min/max/Q64 span | inconsistent metric sets rejected | expose OS/runtime/provider sensitivity before adoption |
| 14 | DPG | Determinism Probe Generator | Require byte-identical repeated execution for same input | stable input ID + repetition bigint | stable replay probe set | zero/excess repetition rejected | generate replay obligations for deterministic paths |
| 15 | REP | Resource Envelope Probe | Probe below/at/above resource constraints | resource min/max Q64 | boundary resource tests | negative min / edge overflow rejected | test memory/latency/CPU policy envelopes without runtime authority |
| 16 | CVDE | Cross-Version Differential Experiment | Generate only semantic key differences between two observed versions | before/after maps | canonical changed-key experiments | no guessing for absent values; absence represented explicitly | regression testing across candidate revisions |
| 17 | OPCC | Observability Probe Contract Compiler | Require each falsifier to have a measurable signal | falsifiers + signal map | observability obligations | any missing signal rejects whole contract | enforce evidence observability before running costly tests |
| 18 | RCB | Reproducibility Capsule Builder | Canonicalize metadata/commands/environment for replay | metadata + command IDs + environment descriptors | canonical payload + deterministic checksum | empty critical fields / non-ASCII internal hash input rejected | attach replay capsule to evidence; checksum is non-security only |
| 19 | EIA | Experiment Independence Auditor | Build deterministic root-disjoint experiment subset and expose shared roots | experiments + causal/source roots | Q64 independence ratio, shared roots, selected independent IDs | empty/duplicate experiment rejected | detect false confidence from correlated evidence sources |
| 20 | PEDC | Promotion Experiment Dossier Compiler | Package experimental results for external Judge/human review | candidate + experiment evidence | readiness dossier | missing evidence blocks readiness; falsification blocks candidate | handoff only; hard-coded `ADVISORY_ONLY`, `autoPromote=false` |

## Authority model

The package has no method that can call a NEXY transition, alter a repository, or emit an accepted Canon state. Its strongest positive conclusion is `READY_FOR_EXTERNAL_REVIEW`. This is intentionally weaker than NEXY `accepted` and cannot be interpreted as that event.

## Deterministic ordering

Where input order could alter a result, identifiers/keys are normalized to canonical lexical order. MFP uses exact dynamic programming with deterministic tie-breaks: total Q64 cost, then fewer experiments, then canonical ID sequence. EIA builds a conservative canonical root-disjoint subset.

## Failure semantics

No silent fallback is used for:
- Q64 overflow;
- divide by zero;
- malformed decimal text;
- missing critical evidence;
- missing observability mapping;
- un-falsifiable required hypotheses;
- non-independent oracle sets;
- impossible outside-boundary probe at signed-128 edge;
- duplicate experiment identities.

The caller must convert these explicit errors into the appropriate NEXY freeze/error contract if integrated later.
