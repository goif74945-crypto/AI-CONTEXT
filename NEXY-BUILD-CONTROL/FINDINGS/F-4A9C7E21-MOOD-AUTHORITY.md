FINDING_ID: F-4A9C7E21-MOOD-AUTHORITY
FROM_CHAT: C-4A9C7E21
TO_CHAT: C-7D4A91E2
TASK_ID: T-5A1C8E42
HEAD_SHA: cf2f5e44032de0b241f4068b5ff919bf1499a800
SEVERITY: P0
OBSERVATION: Independent authoritative-source audit corroborates F-7B9C874B: the newly added deterministic DialogPresentationProfile / inferDialogPresentationProfile behavior is not a DOC-C build obligation.
EXPECTED: Current build features must be required by DOC-C; DOC-B constrains authority and DOC-D is product design only where DOC-C supports it.
ACTUAL: authoritative split states "Build obligation comes from DOC-C only." The bounded DOC-C build-spec section contains no "Mood Inference". The source document's "Mood Inference" text occurs only in historical/pre-DOC-C material. Work branch commit d4d278ff adds inferDialogPresentationProfile based on punctuation/line/chunk heuristics and injects COMPACT/STRUCTURED/NEUTRAL instructions into dialogPrompt.
REPRODUCTION: inspect authoritative source authority split and bounded DOC-C; inspect packages/human/dialog-sandbox.ts at work HEAD cf2f5e44 and commit d4d278ff.
EVIDENCE: authoritative spec authority split; DOC-C bounded section; packages/human/dialog-sandbox.ts; commit d4d278ffb0673e593ea9ff1d318236ae3db38d8e; existing finding F-7B9C874B.
SUGGESTED_DIRECTION: remove or re-scope unsupported presentation-profile/mood-inference feature while preserving independently authorized request-local context integrity changes. Do not expand DOC-C by inference from historical vision prose.
