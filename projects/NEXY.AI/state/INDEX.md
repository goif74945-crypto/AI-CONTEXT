# NEXY.AI State / Persistence Map

Files:
- `state-ownership.json` — authoritative owner, writers, readers, store, lifetime, recovery and audit per major state object.
- `persistence-map.json` — persistence tiers plus forbidden dependency/write patterns.

Key rule:
**state location ≠ state authority.**

The registry records declared owner separately from observed writer paths so authority inversion can be detected later.
