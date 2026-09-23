# NEXY.AI AI Capability / Tool Registry

## Purpose
Prevent fake-tool/fake-execution behavior by separating:
1. technical capability;
2. repository/service permission;
3. task authorization;
4. evidence that the capability was actually observed.

## Files
- `tool-capabilities.json` — baseline/current observed project-relevant capabilities.
- `capability.schema.json`.
- `validation-report.md`.

## Critical distinction
**Technical permission != task authorization.**

Example:
the GitHub connector may technically report push permission to `NEXY.AI-`, but an AI must not mutate that repository unless the current user task explicitly authorizes it.

## Refresh rule
This registry is partly session/runtime dependent.
At the start of any high-impact task, rediscover capabilities whose state can change.

## Status vocabulary
Technical status:
AVAILABLE / READ_ONLY / BLOCKED / UNAVAILABLE / UNKNOWN.

Task authorization is a separate field and may be stricter.
