# NEXY.AI Golden + Negative Corpus

Machine-readable examples:
- `golden/examples.jsonl`
- `negative/examples.jsonl`

Golden examples show behavior that preserves NEXY authority/invariants.

Negative examples are deliberately plausible-looking mistakes:
- fake success;
- stale evidence;
- authority inversion;
- invalid FSM;
- scope creep;
- UI masking;
- hidden fallback;
- nondeterministic mutation;
- destructive learning rewrite;
- test-file-as-PASS;
- orphan FREEZE;
- physical claims from code only.

AI should query negative patterns before finalizing a patch/audit verdict.
