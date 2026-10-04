# ECPC-20 Traceability Catalog

Every C01-C20 has a DESIGN/CODE/TEST/EVIDENCE quartet inside the sealed archive. This remote catalog maps each concept to its tested source SHA-256.

| # | Concept | Source | SHA-256 |
|---:|---|---|---|
| 1 | Schema Fingerprint | `src/concepts/c01_schema_fingerprint.ts` | `74a12c5689cbf2225b3c64cafa15f590c2818b9449ccb68adf45275dd0d37d81` |
| 2 | Compatibility Lattice | `src/concepts/c02_compatibility_lattice.ts` | `ad06a98006e8fbd7d4cda031c3aec1b2ed07a0deade6a9b9be48df8d9f941f45` |
| 3 | Migration Witness | `src/concepts/c03_migration_witness.ts` | `035c02d479cf6ee7763c6d99acf88b538586708f72df5a95f0f94d3be4a976dc` |
| 4 | Codec Involution | `src/concepts/c04_codec_involution.ts` | `94b49313817039efc09b890ecace2bd7c669deba63417b8b5f651511642fc1c6` |
| 5 | Default Injection Guard | `src/concepts/c05_default_injection_guard.ts` | `ca5fffc24c561c5e15993442e004d8fd53bcc1322e2e2ebc1747a76d6091bead` |
| 6 | Enum Evolution Guard | `src/concepts/c06_enum_evolution_guard.ts` | `c6916fc4f37b195375d644e577fd71de3ce1820d309931730e88156427918e38` |
| 7 | Numeric Domain Guard | `src/concepts/c07_numeric_domain_guard.ts` | `56f522e0b5792d2c57fcbb88a01e1ea30789162d76f6067a5968118c16920753` |
| 8 | Nullability Guard | `src/concepts/c08_nullability_guard.ts` | `dc9c46471f5374f97b97468c456e45b5982085a28bff54a8faa27738da646366` |
| 9 | Authority Ownership Diff | `src/concepts/c09_authority_ownership_diff.ts` | `3ffb4e922eb335af337bf85b0c81543dd5a443bcae592a5d4cc21de638216eaa` |
| 10 | Ordering Semantics Guard | `src/concepts/c10_ordering_semantics_guard.ts` | `28b8aac5cee138df8245b484d51205ac2cba7fa1f5d4dd8a22e5bd9137181aa0` |
| 11 | Idempotency Contract Guard | `src/concepts/c11_idempotency_contract_guard.ts` | `77ed72c4011e97ef3d091765a0d6dbdf8c0282b6926093ae67d0a197f02e736a` |
| 12 | Unknown Field Retention | `src/concepts/c12_unknown_field_retention.ts` | `638b2204195bd2ef26066f1989cb8a9f1a535aa77e34c6abaaeb8423bce25294` |
| 13 | Version Handshake Solver | `src/concepts/c13_version_handshake_solver.ts` | `b3c06f7a699430b30d6c85d4013760495a2b9f13faf658784fc2d6450aa27e80` |
| 14 | Upgrade Path Planner | `src/concepts/c14_upgrade_path_planner.ts` | `6399e74846d983d8efa6a2309c0467e81f4fdef288bab4ea1a3a516385c012ef` |
| 15 | Rollback Proof | `src/concepts/c15_rollback_proof.ts` | `23065655c5539c1786925da51dc4d55abbeaf4a38b328fcc3a1b36b764ba50f6` |
| 16 | Replay Compatibility | `src/concepts/c16_replay_compatibility.ts` | `8b2a8817cd1cd0f834e659cedeee165f8841e1774116ef5de32050e438688da0` |
| 17 | Cross-Version Differential | `src/concepts/c17_cross_version_differential.ts` | `3f52e659cd6b7c2cbb827eb809e46af3ac3390c2228dac738fc20e5503113ad0` |
| 18 | Data Loss Budget | `src/concepts/c18_data_loss_budget.ts` | `a279c6d83e973592c7dc3f21a2db174992fb4e38ed3d422e88c800279f6fa2a6` |
| 19 | Contract Drift Merkle | `src/concepts/c19_contract_drift_merkle.ts` | `cc1bd3b8d7390e0c25b31c9bcf5d2305557cc3ea950453827bc54abe3b6e2802` |
| 20 | Promotion Pack | `src/concepts/c20_promotion_pack.ts` | `bbd5929adcd5882e0898e86fa73d3bc4aa884128b8b78bfb2ae73b4e60a24d4e` |

## Aggregate identities
- Engine: `src/engine.ts` SHA-256 `82b225f2f7fe7c4ac81eda5deadd1c66e29c450d400911deb8a9b88e8fb77527`
- EPC vote validator: `src/epc/vote.ts` SHA-256 `4ad99b1a68a53f239eaf6cabb05a565f7b96a92ef314283902c5989a7faea04b`
- EPC append-only ledger: `src/epc/ledger.ts` SHA-256 `a64f844a521abd2a27653c18517d57a8ecb91c18ee7eafb812ff3536a7968082`
- Tested-source manifest SHA-256: `1e615976b8ec5a9d4cdd9d089d9dbba1fd697ed05d35d72dd45f20b2b70ae826`
- Sealed archive SHA-256: `ef83a3ca988a4177b15f8a61910305bef7a5465a31d04f64aa5245ab1e9905be`
