# Skill Compiler — Design

STATUS: PROPOSED_BY_AI / STANDALONE PROTOTYPE

## Objective
Compile repeated verified execution records into a portable skill manifest while blocking inconsistent, weakly evidenced or secret-bearing traces.

## Promotion gates
- same objective pattern;
- at least `min_passes` successful records;
- pass ratio at or above threshold;
- minimum evidence class met by every promoted record;
- canonical step sequence identical across promoted records;
- no secret-like literals in steps/input/output names.

## Output
A deterministic `SkillManifest` containing normalized steps, observed environments, provenance record IDs and measured pass ratio.

## Security
This prototype applies conservative secret-pattern scanning for common API key/token/password forms. It freezes rather than redacts because silent redaction may change workflow semantics.

## Evidence target
E2 tests cover successful compilation, step drift rejection, weak evidence rejection and secret rejection.
