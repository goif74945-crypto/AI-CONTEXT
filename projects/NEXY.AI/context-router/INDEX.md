# NEXY.AI Context Router

## Purpose
Route a task to the **smallest correct context slice** instead of loading the entire project.

## Input
- task text/type
- target repo/branch/HEAD
- scope
- authority
- requested claim class

## Output
- base compiled pack
- required registries
- conditional registries
- explicit default exclusions

## Algorithm
`TASK → CLASSIFY → GOVERNANCE CHECK → RESOLVE ENTITIES/REQS → IMPACT EXPANSION → LOAD REQUIRED CONTEXT → EXECUTE`

If multiple routes match, union only the required slices and deduplicate by canonical ID/path.

## Safety
Context Router reduces context size; it does not reduce evidence obligations.
