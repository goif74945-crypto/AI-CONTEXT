# NEXY Lo4 Equitable Control Integrity64

**Status:** AI-proposed supplemental reference implementation. **NOT NEXY CANON. NOT CURRENT BUILD REQUIREMENT.**

Work trace ID: `CHAT-20261005-0224-NEXY-LO4-EQUITABLE-CONTROL-INTEGRITY64`

The platform-native ChatGPT conversation ID is not exposed to the available tools, so the trace ID above is used rather than fabricating one.

## Five new systems
1. **FREEZE_EQ64** — compares FREEZE-rate burden across supplied cohorts.
2. **VERIFY_TAX64** — compares average verification/evidence burden.
3. **UNNECESSARY_FREEZE64** — compares retrospectively verified avoidable-freeze rates.
4. **RECOVERY_EQ64** — compares recovery success and recovery time.
5. **THRESHOLD_FRAGILITY64** — compares concentration near policy boundaries.

## Privacy posture
The library accepts opaque cohort IDs and aggregate counters/totals. It does not infer cohort membership or sensitive attributes from user data.

## Run
```bash
node --test tests/*.test.mjs
node verify.mjs
```

No third-party dependencies are required.

## Evidence boundary
Passing this package's local tests proves only the standalone reference code at the tested bytes. It does not prove NEXY.AI integration, production fairness, causality, legal compliance, deployment, or Canon promotion.
