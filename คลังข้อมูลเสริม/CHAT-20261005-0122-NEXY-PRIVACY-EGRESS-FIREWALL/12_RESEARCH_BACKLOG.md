# Research Backlog

Every item is **AI-PROPOSED**.

## P0 — Evidence-critical
- **R-01 Recursive minimization:** typed traversal for nested mappings, sequences, attachments, tables, and documents.
- **R-02 Derived-data taint:** track outputs derived from sensitive inputs even when raw values disappear.
- **R-03 Signed egress receipts:** bind request/payload hashes, policy/code/registry versions, recipient identity, decision time.
- **R-04 Bypass graph:** enumerate every network/export/tool path and prove protected context cannot reach them without a decision.
- **R-05 Revocation race model:** simulate queues, retries, duplicated dispatch, clock skew, and revocation between evaluation and send.

## P1 — Product integrity
- **R-06 Consent fatigue economics:** measure when repeated ASK prompts cause blind acceptance.
- **R-07 Explanation compiler:** map reason codes to useful explanations without leaking policy internals.
- **R-08 Privacy budget for identifiers:** measure re-identification risk through stable IDs, field names, timing, or rare reason patterns.
- **R-09 Purpose taxonomy governance:** prevent purpose drift/aliases from becoming catch-all authority.

## P2 — Advanced experiments
- **R-10 Information-flow control:** attach release constraints to derived objects/agent outputs.
- **R-11 Differential disclosure tests:** paired requests differing by one policy factor must have explainable output deltas.
- **R-12 Cross-provider retention contracts:** model retention/training/region/deletion as recipient capabilities without treating claims as runtime proof.
- **R-13 Confidential local preprocessing:** evaluate local redaction/classification before external model use.
- **R-14 Policy conflict solver:** produce minimal conflict proof and freeze rather than weaken conflicting rules.
