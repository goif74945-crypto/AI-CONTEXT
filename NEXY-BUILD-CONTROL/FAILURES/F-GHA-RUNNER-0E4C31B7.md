FAILURE_ID: F-GHA-RUNNER-0E4C31B7
REPORTER_CHAT_ID: C-5A9E7C41
TASK_ID: T-8F3C2A91
STATUS: NEEDS_HELP
SEVERITY: P1
NEXY_BRANCH: NEXY.AI-Test-AI
SOURCE_SHA: 311474744b2644229ccef26850440f02090ca97b
TITLE: GitHub Actions hosted jobs fail before runner allocation

FACT:
- Upstream exact SHA 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43 had four push workflows fail.
- Required jobs in NEXY CI / Deploy Gate run 37222997743 had runner_id=0 and steps=0; downstream DOC-C / attestation / deploy jobs were skipped.
- Exact HEAD run 37222997798, Layer8 Cargo lock run 37222997736, and Six-system run 37222997784 also failed with runner_id=0 and steps=0.
- Rerun of cargo-lock produced attempt-2 job 111540344741; it again failed with runner_id=0 and steps=0.
- After enabling work-branch push trigger, exact work SHA 311474744b2644229ccef26850440f02090ca97b created push run 37238120592.
- All nine executable jobs in run 37238120592 again failed before any step with runner_id=0 and steps=0.

ASSUMPTION:
- None used to classify the observed runner-allocation failure.

UNKNOWN:
- Exact GitHub-side cause (billing/quota/service/account/repository policy/other infrastructure) is not exposed by available job evidence.

AFFECTED:
- GitHub-hosted E1-E5 verification and deploy-gate execution.
- Fresh exact-head CI proof.

INDEPENDENT_WORK_NOT_BLOCKED:
- Static/source inspection.
- Work-branch source repair with non-GitHub execution evidence where available.
- Control-plane review/testing/coordination.

NEXT_ACTION:
- Independent chat/account-side investigation of hosted-runner availability.
- Do not treat these zero-step jobs as proof that application tests/builds fail.

EVIDENCE_REFS:
- runs 37222997743, 37222997798, 37222997736, 37222997784
- rerun job 111540344741
- work-branch run 37238120592
