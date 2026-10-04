# Failure + Security Model

- Arithmetic overflow is fail-closed with `RangeError`.
- Division by zero is fail-closed.
- Hard safety gates reject instead of degrading silently.
- Ranking ties resolve by stable lexical identifiers, preventing host-dependent iteration order from changing decisions.
- No filesystem/network/process/env/secret access in decision modules.
- Q64 parser rejects exponent notation and malformed decimals to keep the input grammar narrow.
- This lab is not a security boundary by itself; callers must authenticate/authorize before invoking mutation-affecting decisions.
