# Execution 011 CROSS
Product NEXY.ai HEAD 44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08
DOCX SHA-256 verified this turn: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7.
DOC-C paragraph indices zero-based P9885 (BUILD SPEC) and P9915 (release.quorum_min=2) / P9916 (evidence_min=2).
LAW initial source Git blob f0ae1b06774e11cb2c0f417bc36c0d398347b036; isolated patched source 696acae9428a347e91eb32a26b692f6d913f1bf0.
LAW patch blob d9247cf4f91c624683d21c3a4225510cd32b0822; LAW test blob 417f3932f3eaf649eb11e56963838727f3537f67.

CASE1: candidate quorumCount=2, agentIds=[agent-01] must fail schema and release. CASE2: quorumCount=10, agentIds 2 must fail. CASE3: exact quorum2 and agentIds2 remains PASS. CASE4: quorumCount1 with agentIds2 retains CONSENSUS_FAILED. CASE5: duplicate agentIds still rejected. Before patch 2 failures; after patch all five and related 53 tests passed. This tests LAW predicate, not live Worker/PG production transaction. JUDGE normal path derives counts from votes, reachability of inconsistent normal payload unproven.
