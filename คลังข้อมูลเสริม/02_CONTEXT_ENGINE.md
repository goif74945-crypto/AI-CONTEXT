# NEXY Context Engine — Retrieval Contract
Status: PROPOSAL

## Problem
Large repositories fail when retrieval returns “related text” instead of authoritative context. Context selection must preserve authority, freshness, scope and contradiction information.

## Retrieval unit schema
Each chunk SHOULD carry:
- id
- repository/path/ref/blob_sha
- semantic role
- authority_rank
- scope tags
- requirement ids
- valid_from / supersedes / superseded_by
- source_type
- content_hash
- trust label
- dependency links
- contradiction links
- generated_or_human
- verification state

## Ranking
Never rank by semantic similarity alone.
Suggested order:
1. explicit authoritative spec match
2. exact symbol/path/requirement match
3. current sealed project evidence
4. current implementation
5. tests/contracts
6. project docs
7. AI-CONTEXT advisory knowledge
8. external references
9. inference

Semantic relevance is a filter inside an authority tier, not a replacement for authority.

## Contradiction protocol
If two retrieved items disagree:
- preserve both
- identify authority and source identity
- do not blend them into a synthetic answer
- choose only when precedence is explicit
- otherwise emit CONFLICT/FREEZE

## Context budget allocation
PROPOSAL:
- 35% authority/spec
- 25% directly relevant implementation
- 20% tests/evidence
- 10% dependency/context neighborhood
- 10% counterevidence/known failures
Dynamic reallocation allowed, but authority cannot be starved.

## Query decomposition
For engineering questions retrieve independently:
A. requirement
B. implementation
C. tests
D. evidence
E. known failure/regression
F. dependency boundary
Then reconcile.

## Poisoning defense
Untrusted documents, web text, issues, comments and model-generated notes must never become instruction authority merely because retrieval surfaced them.
Store instruction/data distinction explicitly.

## Acceptance tests
- superseded spec is not selected over current spec
- advisory AI-CONTEXT cannot override project authority
- contradictory evidence produces conflict
- exact path/symbol queries remain stable
- retrieval result is reproducible for same index snapshot
- every returned claim can expose provenance
