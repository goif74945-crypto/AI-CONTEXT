# Source / Test Bundle

The human-readable design/evidence documents are published directly. The complete executable implementation, tests, stress harness, concept-specific designs, raw evidence, and manifest are preserved as a base64-split `tar.gz` source bundle because the connected GitHub writer cannot ingest the assistant's local directory as a file tree.

Reconstructed archive SHA-256:
`9af0a004884662fb62396869f83f35fa5b96a57f738cd72dd6b8026c76cc93ae`

Published parts:
`NEXY-LO4-REALITY-FIVE-SOURCE.tar.gz.b64.part01` through `part07`.

Reconstruct, verify, and run:

```bash
cat NEXY-LO4-REALITY-FIVE-SOURCE.tar.gz.b64.part* | base64 -d > NEXY-LO4-REALITY-FIVE-SOURCE.tar.gz
sha256sum NEXY-LO4-REALITY-FIVE-SOURCE.tar.gz
mkdir source && tar -xzf NEXY-LO4-REALITY-FIVE-SOURCE.tar.gz -C source
cd source
sha256sum -c MANIFEST.sha256
python verify.py
python stress_verify.py
```

The reconstructed archive contains the modular `reality_five/` package, compatibility facade, split `tests/`, verification scripts, concept-specific designs, raw test evidence, and `MANIFEST.sha256`.

This split is a transport adaptation only. It does not reduce the tested artifact set or alter code behavior.

Classification: `Lo4_AI_PROPOSAL_ONLY`. This is not NEXY Canon and not proof of runtime integration.
