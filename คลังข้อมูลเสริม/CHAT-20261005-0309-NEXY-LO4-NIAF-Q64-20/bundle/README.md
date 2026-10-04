# NIAF-20 Sealed Bundle

This bundle preserves the full Design + Code + Test + Evidence tree.

- Archive SHA-256: `24e9ffd24bd61fa20adcbda10d36075bb76a784cc006e5dfe6bb3ec9c5d4c5b5`
- Internal manifest SHA-256: `2101721117a13bb7be05bbef3ddb34926de1a75cabb9af3267d4f997410eac6d`
- Base64 transport is split into four parts to keep publication operations bounded.

Reconstruct on a trusted machine:

```bash
cat NIAF-20-sealed.tar.gz.b64.part00 \
    NIAF-20-sealed.tar.gz.b64.part01 \
    NIAF-20-sealed.tar.gz.b64.part02 \
    NIAF-20-sealed.tar.gz.b64.part03 \
  | tr -d '\n' | base64 -d > NIAF-20-sealed.tar.gz

printf '%s  %s\n' 24e9ffd24bd61fa20adcbda10d36075bb76a784cc006e5dfe6bb3ec9c5d4c5b5 NIAF-20-sealed.tar.gz | sha256sum -c -
tar -xzf NIAF-20-sealed.tar.gz
cd NIAF-20
sha256sum -c MANIFEST.sha256
./scripts/verify.sh
```

Expected transport-part Git blob SHAs after publication:

- part00: `04b98277ae28d35d84e4ab7e9b3b357efc6f4305`
- part01: `4e07cf1e153719113e424b6d805e64dbaa868bdf`
- part02: `8987dc43ba80d0d56efc9a0dd1661fce14bc3c54`
- part03: `ebd08652cf55c0470ff7d6102a6d2ee21cab3d3c`

The bundle is Lo4 proposal-only. Reconstruction does not constitute NEXY integration or promotion.
