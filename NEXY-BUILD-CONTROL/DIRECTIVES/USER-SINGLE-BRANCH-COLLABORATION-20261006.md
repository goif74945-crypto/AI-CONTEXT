# USER DIRECTIVE — SINGLE-BRANCH MULTI-CHAT COLLABORATION

AUTHORITY: CURRENT_EXPLICIT_USER_OPERATIONAL_DIRECTIVE
STATUS: EXECUTE_NOW
TARGET_REPOSITORY: goif74945-crypto/NEXY.AI-
PROTECTED_UPSTREAM: NEXY.ai
ONLY_SHARED_PRODUCT_BRANCH: NEXY.AI-Test-AI
CONTROL_REPOSITORY: goif74945-crypto/AI-CONTEXT

This directive supersedes every prior instruction that requires or permits creation of worker, validation, CI, oracle, review, temporary, or per-chat product branches.

## Absolute branch law

The product repository is converging to exactly two branches:
1. NEXY.ai — read-only/protected upstream.
2. NEXY.AI-Test-AI — the only branch on which collaborative product work may be integrated.

Effective immediately:
- DO NOT CREATE ANY NEW PRODUCT BRANCH.
- DO NOT CONTINUE WRITING TO EXISTING NONCANONICAL PRODUCT BRANCHES.
- DO NOT FORCE-PUSH OR DELETE NEXY.ai.
- Existing extra branches are FROZEN_FOR_MIGRATION.
- Do not delete an extra branch until its useful information has been exported, reviewed, and either integrated or explicitly rejected with evidence.
- After migration is complete, delete all noncanonical product branches so only NEXY.ai and NEXY.AI-Test-AI remain.

## Per-chat migration

Every active Chat that owns or used a noncanonical branch must export what it created into AI-CONTEXT before abandoning that branch.

Canonical proposal path:
NEXY-BUILD-CONTROL/PRODUCT-PROPOSALS/<SYSTEM_KEY>/<CHAT_ID>/<PROPOSAL_ID>.json

Each proposal must include:
CHAT_ID
SYSTEM_KEY
PROPOSAL_ID
SOURCE_BRANCH
SOURCE_HEAD_SHA
BASE_TARGET_SHA
SPEC_REQUIREMENTS
CHANGED_FILES
IMPLEMENTATION_SUMMARY
PATCH_OR_CANONICAL_CHANGE_DESCRIPTION
TESTS_RUN
TEST_EVIDENCE
KNOWN_LIMITATIONS
CONFLICTS
STATUS

If code/diff content is required to preserve the work, store the patch or exact relevant content in AI-CONTEXT under the same proposal directory.

After export:
- stop writing to the old branch;
- participate in discussion/review;
- continue useful work through AI-CONTEXT proposals and the shared target process.

## Discussion

Chats working on the same system must compare proposals against the authoritative specification and real evidence.

Discussion path:
NEXY-BUILD-CONTROL/PRODUCT-DISCUSSIONS/<SYSTEM_KEY>/<ROUND_ID>/

Discussion must focus on:
- specification fidelity;
- correctness;
- runtime/test evidence;
- compatibility with already integrated product state;
- regression risk;
- deterministic behavior where required;
- completeness.

Popularity cannot override the authoritative specification.

A proposal proven incompatible with the authoritative spec is ineligible even if it receives votes.

## Voting

Exactly one Chat has exactly one valid vote per SYSTEM_KEY per ROUND_ID.

Canonical ballot path:
NEXY-BUILD-CONTROL/PRODUCT-VOTES/<SYSTEM_KEY>/<ROUND_ID>/<CHAT_ID>.json

Required ballot fields:
CHAT_ID
SYSTEM_KEY
ROUND_ID
SELECTED_PROPOSAL_ID
SPEC_FIDELITY_REASON
EVIDENCE_REFERENCES
CAST_AT_CONTROL_HEAD

Rules:
- one CHAT_ID = one vote per system per round;
- duplicate ballots from the same CHAT_ID in the same round are invalid after the first valid ballot;
- fake/synthetic peers or votes are forbidden;
- a Chat cannot cast multiple identities;
- votes choose between eligible implementations, not between different meanings of the specification;
- the eligible proposal with the greatest number of unique valid Chat votes wins;
- a tie creates a new tie-break review round containing only the tied eligible proposals;
- USER directive may override the vote.

## Applying the winner

No simultaneous blind writes to NEXY.AI-Test-AI.

Before applying a winning implementation, one Chat must obtain the current shared TARGET_WRITE_LEASE recorded in AI-CONTEXT and bind:
CHAT_ID
SYSTEM_KEY
ROUND_ID
WINNING_PROPOSAL_ID
EXPECTED_TARGET_HEAD_SHA

The writer must re-read NEXY.AI-Test-AI, apply/rebase the winning change onto the current head, run required real tests, then move the branch only with expected-head/CAS semantics.

After the write, publish result/evidence to AI-CONTEXT and release the write lease.

Other Chats continue discussion, testing, review, gap discovery, or preparation while the writer is integrating.

## No-stop rule

Receiving this directive does not end a Chat's mission.

After branch migration, every Chat continues working.
A completed proposal, review, vote, test, or integration does not mean the Chat is finished.
If its current work becomes obsolete, blocked, or loses a vote, it immediately selects another useful task.

## ACK and sleeping Chats

Every active Chat must ACK this directive before its next product mutation.

ACK path:
NEXY-BUILD-CONTROL/ACKS/SINGLE-BRANCH-MIGRATION/<CHAT_ID>.json

If a contacted Chat produces neither an ACK nor any new control/product activity for 600 seconds after this directive is observed, classify it as ASLEEP/INACTIVE for coordination purposes.

ASLEEP/INACTIVE Chats:
- do not block discussion;
- do not block voting;
- do not count toward vote participation;
- may rejoin later by reading current state and writing a fresh ACK.

## Immediate priorities

1. Stop creating branches.
2. Freeze all existing extra branches.
3. Inventory their branch heads.
4. Export branch-owned work to AI-CONTEXT proposals.
5. Group proposals by SYSTEM_KEY.
6. Discuss and test competing implementations.
7. Vote with one CHAT_ID = one vote.
8. Apply only the winning eligible implementation to NEXY.AI-Test-AI through one serialized target writer.
9. Prune migrated/rejected extra branches only after preservation is proven.
10. Continue until NEXY.AI-Test-AI matches the authoritative specification as closely and completely as real evidence can establish.
