# LEDGER-NEXY-DOC-E-2026-09-30-EFC680A

| id | source | claim | proof | deps | risk | status | confidence | freshness |
|---|---|---|---|---|---|---|---|---|
| L1 | GitHub NEXY.ai branch | canonical HEAD is efc680a5846dcd6a49ad5e49bc53ec6e8cdd4e98 | branch/ref + commit created by fast-forward | GitHub connector | low | VERIFIED | 1.00 | current |
| L2 | GitHub source fetch | DOC-E contract corruption existed at prior HEAD 541421ab | malformed bytes inside TypeScript expression | repository file content | S4 | VERIFIED | 1.00 | current-at-fix |
| L3 | GitHub commit | corruption/test contradiction repaired | commit bd817650267acea64f21aa631d49076c5e7d201a | Git object | medium | VERIFIED_SOURCE_CHANGE | 1.00 | current |
| L4 | GitHub Actions | CI jobs instantiate | run 36602718686 lists 11 jobs | Actions API | medium | VERIFIED | 1.00 | current |
| L5 | GitHub Actions | runner-smoke never reached step execution | run 36602881913, job 109524417528, steps=null, logs_url=null | Actions API | S4 | VERIFIED | 1.00 | current |
| L6 | external tools | no alternate runner currently available | Opera disconnected; desktop offline; Termalin hosts=[] | plugin state | medium | VERIFIED | 1.00 | current |
| L7 | DOC-E release law | release is not authorized | E1-E12 not executed on exact HEAD; E11 not externally signed | design authority + current evidence | S4 | VERIFIED | 1.00 | current |
