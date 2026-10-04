# Git Blob Identity Manifest

Execution: CHAT-20261005-0144-NEXY-INTERLEAVING-VERIFIER
Method: Git blob SHA from the tested local artifact compared against GitHub fetch_file blob SHA.
Result: 20/20 checked artifacts MATCH.

| Path | Git blob SHA |
|---|---|
| src/interleaving_verifier/model.py | 9c6456c3d7a8128c5f327664664b444e2a250f4e |
| src/interleaving_verifier/engine.py | 75e9d57af000f93665942871f422545e02f5008d |
| src/interleaving_verifier/cli.py | 5876eacedd4212ab885fa8d91579a0706333165d |
| src/interleaving_verifier/__init__.py | 4205c026756d951057bb052d1bf2c4c57fbebe65 |
| src/interleaving_verifier/__main__.py | eb53e2f31b2f703ad32ef64b8a41faa3e7d18e08 |
| tests/test_engine.py | 2a5be1463f03193a8b81e0bf38ce58b3853cd878 |
| tests/test_cli.py | 70db015080ffe4560a7911d88b0d13ae7c2d98b8 |
| tests/test_oracle.py | ca325ffc444427a34f71e2f15b76cf8173449bac |
| fixtures/confluent.json | 9dc75829bfeb73038e89142081fdc9ce5c92a589 |
| fixtures/divergent.json | d761fa8a70ce6a9a7d3eddae5ad4317aa13094eb |
| schemas/plan.schema.json | 2264f3c986e0004095ab7741ddd5f6cd4b1187e4 |
| schemas/report.schema.json | 439b0253177801f26d9952cba40ce607b01601ce |
| evidence/confluent-report.json | dcdeb2429cae45c68541cf6c981e47a52f77ab21 |
| evidence/divergent-report.json | f9c13944a02facb2f98c515efd27b806ab40e242 |
| README.md | 38fa35ada6850bdcb9fea8c666ccf094ece1cddc |
| 02_DESIGN.md | dabc0665372901f26359fc3ee95afdfe4785aa50 |
| 03_FAILURE_MODEL.md | 8115bc4fa81b2cf8c6f11515efcc8f4eb951b130 |
| 04_INTEGRATION_GUIDE.md | e8ac2ca9190878b6f3e3067109b60309268d5a4a |
| 05_AI_PROPOSED_EXTENSIONS.md | 7b4088b26e822db015bbeade7c652879930581cd |
| 06_TEST_MATRIX.md | 3af054de84707dea4fce72bac09e687a06496a69 |

This manifest binds the E1/E2 claims to the exact GitHub blobs checked after upload. It does not claim production NEXY integration.
