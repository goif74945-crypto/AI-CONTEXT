# Architecture

## Design goals
- deterministic and provider/model independent;
- standard-library Python core;
- pure data transforms where practical;
- no network or subprocess in production package;
- explicit logical sequence instead of hidden time;
- canonical JSON + SHA-256 fingerprints;
- fail closed on malformed CLI input;
- privacy-aware outcome redaction.

## Modules
- `models.py`: typed signal/evidence/severity/delivery contracts.
- `canonical.py`: deterministic JSON and SHA-256 identity.
- `salience.py`: Salience Gate.
- `routing.py`: Interruption Governor.
- `compress.py`: Milestone Compressor.
- `delta.py`: Outcome Delta Compiler.
- `debt.py`: Acknowledgement Debt Ledger.
- `cli.py`: five machine-readable CLI operations.

## Trust boundary
Inputs are untrusted structured data. The package never executes content from a signal, never opens arbitrary files except the CLI input path chosen by the caller, and never performs network/model calls.

## Determinism boundary
Wall clock, randomness, environment variables, model output, filesystem ordering, and network state are excluded from decision semantics. Sequence/order must be explicit in input.

## Failure model
Malformed field/type/enum -> exception internally and CLI `FREEZE`.
Duplicate sequence or signal identity where uniqueness is required -> fail closed.
Future acknowledgement/signal -> fail closed.
Invalid redaction path -> fail closed.
Unknown state marker -> emitted as UNKNOWN delta, not inferred.

## Integration shape
Proposed adapters may map NEXY::PULSE/JUDGE/GUARD event envelopes into `OperatorSignal` without changing this core. Adapter mapping is outside the reference project's proof boundary.
