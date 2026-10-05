# F-CONTROL-WORKER-REF-NAMESPACE-001

STATUS: OPEN
SEVERITY: P0

The configured worker prefix `NEXY.AI-Test-AI/work/` cannot be created while the branch `NEXY.AI-Test-AI` exists. GitHub returned HTTP 422 when creation was attempted from integration SHA `608426cb30398b1f3461866f7079d2a435c96b96`.

SAFE_STATE:
- `NEXY.ai` unchanged.
- `NEXY.AI-Test-AI` unchanged.
- No worker branch created.

UNBLOCK:
The active worker branch naming rule must be changed to a Git-compatible non-descendant namespace, or direct integration-branch mutation must be explicitly authorized.
