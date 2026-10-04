# Possible NEXY Integration Map

**AI-PROPOSED only. No integration has been performed.**

Potential future placements:

1. **Model/provider hot-swap gate**: mirror normalized cases through old/new provider adapters; compare outcome semantics before rollout.
2. **Policy migration gate**: establish an explicitly authorized new baseline, then run shadow comparison on regression corpus.
3. **Refactor assurance**: compare old/new JUDGE or routing outputs on immutable fixtures.
4. **Release evidence input**: attach report hash and exact revisions to a release evidence record. It cannot replace required E4/E5/E6 evidence.
5. **Incident replay**: replay an incident corpus through patched logic and prove that unsafe releases became freezes while unaffected cases remain stable.

## Required adapter contract before adoption
An integration adapter must prove normalized inputs are semantically equivalent, policy/revision identities are exact, raw secret/user content is excluded unless explicitly authorized, and decision records cannot trigger actions from the shadow path.

## Non-authority clause
The comparator may recommend only `PASS / FAIL / NOT_VERIFIED`. It must not override USER LAW, NEXY LAW, JUDGE, RSEL/Safety Kernel, deployment approvals or human irreversible-action approval.
