# C2 Evidence

Standalone evidence achieved: **E1 + E2**.

Executed cases include:
- multi-step secret egress;
- secret redaction breaking the taint chain;
- untrusted code execution;
- validation breaking untrusted taint;
- low-trust authority influencing protected mutation;
- missing artifact freeze;
- artifact overwrite freeze;
- duplicate-output rejection;
- 50 seeded irrelevant-step cases preserving secret-egress detection;
- C2→C5 minimal reproducer integration.

This proves only behavior of the prototype's explicit abstract taint model. It does not prove real providers/tools are correctly labeled or that all real-world hazards are represented.
