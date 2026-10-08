# CASES 008
TASK_ID: 20261008-NEXY-NORMAL-CHAT-EXECUTION-008-CROSS
PRODUCT HEAD: 44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08
CONTROL MAIN PREWRITE: 8e787a81e11fc00f2bd7d5ca68474f0b774085c1
SPEC SHA-256: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7 (recomputed from mounted DOCX 2026-10-08)
SOURCE BLOBS: dispatch.ts 002eef253ce836e2cd0e200f5d15cb5042cdeb29; cage.ts 5afd464ed39470381ef1df643a630e1f431817dc; vnext-config.ts a3141a649be7e40ec79f417f53bba9b73081232b; matrix historical f18b4874b875ca713dd007c7feddffba13d0f380

QUEUE-CANCEL-RACE-006: Current dispatchSource unconditionally uses update({where:{id}}) after await enqueue. Candidate replaces entire dispatchDirective() with CAS updateMany WHERE (id,status,attempts,lastError), with conflict re-read and narrow error catch. Ten source-importing Vitest tests authored, NOT_RUN. At least four are expected RED on original implementation; no false pass claimed. Redis publish before cancellation, worker claim of PENDING, and terminal preservation covered at mock boundary only.
CAGE-ISOLATION-006: Current cage source supports Linux bwrap=false direct spawn and labels result linux-cgroup-seccomp. DOCX P04137-P04149 calls for namespace/syscall/memory isolation. Candidate throw CageError(SPAWN_FAILED,CAGE_OS_ISOLATION_UNAVAILABLE) before direct spawn; NOT_RUN. Preexisting tests/integration/lo3-cage-command.spec.ts first comments expect insecure fallback, so must revise tests, not just flip source. Even bwrap available does not prove seccomp JSON applied or cgroup active.
