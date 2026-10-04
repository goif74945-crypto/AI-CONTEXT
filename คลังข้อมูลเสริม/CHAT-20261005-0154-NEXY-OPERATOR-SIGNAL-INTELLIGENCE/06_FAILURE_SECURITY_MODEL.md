# Failure & Security Model

## Protected guarantees
1. Critical/freeze/security signals cannot be silently suppressed.
2. Unverified/unknown state cannot be displayed as an ordinary verified delta.
3. Redacted fields cannot leak their before/after values through delta entries.
4. Acknowledgements cannot precede or refer to nonexistent ack-required signals.
5. Duplicate identities/sequences are rejected where ambiguity would make output unreliable.

## Threats and response
- **Noisy event flood:** compressor deduplicates routine semantic repeats; critical routes remain immediate.
- **Quiet-mode abuse:** critical/freeze/security routing override quiet mode.
- **Fake acknowledgement:** unknown/pre-signal/future acknowledgement is rejected.
- **Sensitive delta exposure:** exact subtree or whole-root redaction replaces values with `[REDACTED]`.
- **Clock manipulation:** deadlines use caller-declared logical sequence, not local time.
- **Instruction injection in message strings:** messages are data only; no eval/exec/model/tool dispatch exists.
- **Nondeterministic ordering:** compressor sorts by explicit sequence and rejects duplicate sequence numbers.

## Known limits
This is not an authentication system, notification transport, persistence database, accessibility renderer, or production NEXY adapter. Those require separate evidence.
