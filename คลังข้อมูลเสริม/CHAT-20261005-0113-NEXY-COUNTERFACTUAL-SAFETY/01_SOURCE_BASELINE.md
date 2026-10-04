# Source Baseline and Truth Boundary

Status: SOURCE-GROUNDED BASELINE
Chat: CHAT-20261005-0113-NEXY-COUNTERFACTUAL-SAFETY

## Purpose
Freeze the source assumptions used by this supplemental pack so future readers can distinguish NEXY source truth from AI-proposed engineering.

## SOURCE_FACT
- The current normalized NEXY source matrix contains 837 requirement rows.
- 773 rows are in Current Build: 12 CURRENT_GOVERNING_LAW + 547 CURRENT_BUILD + 127 CURRENT_BUILD_SUPPLEMENT + 87 SUPPORTED_PRODUCT_DESIGN.
- 52 DEPLOYMENT_EVIDENCE rows are proof obligations rather than implementation proof.
- 8 rows are EXCLUDED_CURRENT and 4 DEFERRED_FUTURE.
- DOC-B governs current system law.
- DOC-C is current build authority.
- DOC-D controls product/UI only where DOC-C supports it.
- DOC-E controls deployment evidence/approval and is not implementation proof.
- Historical 215 registry is DEPRECATED_UNRELIABLE_DO_NOT_USE for current counting or completeness.
- The matrix itself explicitly says implementation audit was not performed and defaults implementation status to NOT_VERIFIED.

## Derived engineering consequence
Any change-safety system must preserve four independent coordinates:
1. source obligation,
2. implementation state,
3. runtime evidence,
4. deployment evidence.

A transition in one coordinate MUST NOT silently update another.

## Provenance
Source paths:
- projects/NEXY.AI/overview.md
- projects/NEXY.AI/deep/INDEX.md
- projects/NEXY.AI/source-normalization/CURRENT-SYSTEM-FEATURE-BUILD-MATRIX.md
- rules/VERIFICATION.md

## Non-claim
This file does not establish the current code state of NEXY.AI.
