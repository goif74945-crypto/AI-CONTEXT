# LFCG Evidence
- Source: `src/index.ts`.
- Focused tests: 4 PASS.
- Negative paths: wrong/stale/future/revoked/expired lease behavior.
- Property: 500 sequential reacquisitions prove every stale fence is rejected.
- Stress: 20,000 allow/future-fence checks PASS.
- Production durable fencing remains NOT_VERIFIED.
