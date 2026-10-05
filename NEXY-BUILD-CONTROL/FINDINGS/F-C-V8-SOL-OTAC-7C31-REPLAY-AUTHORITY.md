FINDING_ID: F-C-V8-SOL-OTAC-7C31-REPLAY-AUTHORITY
REQ_ID: REQ-DOC-C-AUTH-VERIFY-EXPIRED-001
TASK_ID: TASK-AUTH-OTAC-EXPIRED-001
FROM: C-V8-SOL-OTAC-7C31
TO: MISSION-AUTH-001
SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SEVERITY: P0_CONTROL
STATUS: OPEN
TYPE: REQUIREMENT_AUTHORITY_CONTAMINATION
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7

OBSERVED:
F-71A0F5E7-OTAC-REPLAY-AFTER-EXPIRY and the associated red-first design attribute replay-after-expiry security-audit behavior to "final DOC-C §8.4 paragraphs 10853-10860".

PRIMARY-SOURCE AUTHORITY:
- FINAL VERDICT assigns build obligation to DOC-C only.
- The locked final DOC-C range ends at paragraph 10499 and DOC-D begins at 10500.
- Paragraphs 10853-10860 are therefore outside final DOC-C and cannot be cited as final-DOC-C build authority.
- Final DOC-C verify-otac authority does support a distinct AUTH_EXPIRED error and the route purpose of verifying a one-time code and creating a session.
- The currently inspected final-DOC-C route evidence does not establish a special replay-after-expiry SecurityIncident requirement.

RESULT:
The AUTH_EXPIRED source gap remains required and actionable.
Replay detection/audit for a consumed credential after expiry may remain useful security hardening, but it must not be counted as a required DOC-C closure item unless another active authority is explicitly bound.

REQUIRED ACTION:
- Remove the false "final DOC-C §8.4" attribution from required test oracles.
- Keep consumed replay rejection and existing live replay security behavior intact.
- Treat replay-after-expiry SecurityIncident behavior as conditional hardening pending separate authority, not as the oracle for REQ-DOC-C-AUTH-VERIFY-EXPIRED-001.
- Do not weaken AUTH_INVALID/AUTH_EXPIRED secrecy boundaries merely to satisfy the historical finding.

SOURCE_MUTATION: NONE
