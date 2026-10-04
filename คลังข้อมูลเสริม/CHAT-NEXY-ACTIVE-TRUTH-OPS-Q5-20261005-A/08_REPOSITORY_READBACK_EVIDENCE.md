# Repository Readback Evidence

Observed after initial project commit.

Initial project commit:
8ba373602abfa9de91cad5018b5fa41405778163

Current main at readback:
c46dd364dd77e42a9fd8a4a9a7839ebecb1baf71

Ancestry compare:
status ahead
ahead_by 13
behind_by 0
merge_base 8ba373602abfa9de91cad5018b5fa41405778163

Root readback preserved both earlier durable state files and all project docs.

Exact bundle readback:
- part01: sha 8eee6238c3a87c29abefa29781fbc207c0fba068, 6000 bytes
- part02: sha a3901c8473d261a65a3fe589adb3012466890ff5, 6000 bytes
- part03: sha 176eb6690d90692569dc1896c8e5f6eb61ce6aa1, 6000 bytes
- part04: sha b3ea3dfc1e9aefb6e2c2d03dee4cfe72ce3fa666, 6000 bytes
- part05: sha 4303e1879f9b02033c407dd800fe08ded0d7af19, 448 bytes

Each part Git blob SHA was independently calculated from exact local text before attachment and matched GitHub create_blob return.

Local reconstruction of the same five logical parts produced archive SHA-256:
b3460fe3456288af7085aeb3a120bf8cef11416bc95695ccb3315a60ae6bea78

Limit:
This proves repository persistence/content identity. It does not prove NEXY runtime/deployment integration.
