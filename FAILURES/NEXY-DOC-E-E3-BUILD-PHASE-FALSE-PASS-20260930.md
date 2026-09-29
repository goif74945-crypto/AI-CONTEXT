# NEXY-DOC-E-E3-BUILD-PHASE-FALSE-PASS-20260930

FAILURE_ID: NEXY-DOC-E-E3-BUILD-PHASE-FALSE-PASS-20260930
context: DOC-E E3 migration roundtrip on Railway
cause:
- private Railway DNS is unavailable during build phase
- direct psql cannot consume Prisma-style DATABASE_URL query parameter schema=public
- nested E3 harness inherited set +e and could continue after database commands failed
failed_approach: run full DB roundtrip inside Railpack build phase
recovery:
- move migration roundtrip to Railway pre-deploy command (private network available)
- use separate psql URL without schema query
- enforce set -e at E3 command start
- use isolated temporary database and trap cleanup
verified_recovery:
- deployment 64d41f28-7377-4363-aa2e-3e9bc0aae5e0
- exact SHA 941dd80a37d85e44e075658cee8e59e1103a1fbf
- DOC_E_E3_ROUNDTRIP=PASS
- log sha256 3ac26fff3300eb6f1b2129b1334032bb830046deba94b15fda91175bd693b01f
boundary: proof is historical exact-head mechanism evidence only after branch drift
prevention: never accept a PASS marker unless upstream commands are fail-fast and the execution plane has required networking
