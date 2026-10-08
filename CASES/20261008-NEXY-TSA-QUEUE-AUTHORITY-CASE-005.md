# CASE — Scope of TSA Authority for Canonical Queue TTL

CASE_ID: 20261008-NEXY-TSA-QUEUE-AUTHORITY-CASE-005
TASK_ID: 20261008-NEXY-DOCB-DOCC-TSA-QUEUE-TTL-005
CATEGORY: SOURCE_AUTHORITY / SEMANTIC_DEPENDENCY
STATUS: OPEN_FOR_IMPLEMENTATION_DEPENDENCY_REVIEW

CAUSE: Current canonical queue source depends on currentTsaBatchTimeMs(), while final DOC-C queue defaults specify TTL=900000 but do not explicitly state that queue expiry must verify TSA signatures.
EVIDENCE: Hash-matched DOCX P09844, P09886-P09948, plus broader time P04003-P04009 and P05151-P05158, earlier queue law P09435-P09459.
IMPACT: Removing TSA blindly could violate Core time law; demanding TSA blindly may impose an implementation dependency not expressly stated in DOC-C.
REMEDY: Trace source call graph and isolate applicable trust boundary, separately classify normative obligation, available authority providers, and runtime behavior.
DO_NOT_DO: No arbitrary clock substitution, fake TSA signatures, test skipping or release signoff promotion.
NEXT: Codex continues bounded TSA-path audit and independent sandbox repair.
