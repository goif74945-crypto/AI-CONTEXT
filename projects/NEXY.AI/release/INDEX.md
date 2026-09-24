# NEXY.AI Release Gate Matrix

Canonical:
- `gates.json`

Stages:
DEV → TEST → STAGING → CANARY → PROD

Current observed status:
**BLOCKED / NON_DEPLOYABLE for HEAD 9c9befd9fe255b0f9271e6e2b8c4bb2443a08089**

Reason:
DOC-E E1–E12 artifacts are not bound to current HEAD and several are explicitly BLOCKED/BLOCKED_EXTERNAL.

No automatic promotion is allowed from source/code presence.
