# DSMF-20 — Lo4 Deterministic Swarm Mechanism Fabric 20

Authority: `Lo4_AI_PROPOSAL_ONLY / EXPERIMENTAL / NON_CANON`

This folder contains a deterministic standalone reference project with 20 Q64.64 swarm-worker mechanisms designed for possible future NEXY::SWARM adaptation. It does not mutate or govern NEXY.AI and cannot override CORE/LAW/JUDGE.

## Durable bundle
The exact locally-tested Design + Code + Tests + Evidence + TypeScript adapter are sealed into eight base64 text parts:

`DSMF20_BUNDLE.tar.gz.b64.part-00` … `part-07`

Reconstruct:
```bash
cat DSMF20_BUNDLE.tar.gz.b64.part-* | base64 -d > DSMF20_BUNDLE.tar.gz
sha256sum DSMF20_BUNDLE.tar.gz
# expected: 1aa02bee8bb837b6fa4cbb0c68d933705a6d51d71327b01335f635d88c396f8f
tar -xzf DSMF20_BUNDLE.tar.gz
```

Verified standalone seal: 96/96 tests PASS, source branch coverage 99%, Python compileall PASS, TypeScript 5.8.3 adapter typecheck/self-test PASS, offline Python build/install/import PASS. NEXY exact-head integration/runtime/deployment remain NOT_VERIFIED.

Work code: `CHAT-20261005-0229-NEXY-LO4-DETERMINISTIC-SWARM-MECHANISM-FABRIC-20`.
Native UI chat ID is not exposed to the tool runtime.
