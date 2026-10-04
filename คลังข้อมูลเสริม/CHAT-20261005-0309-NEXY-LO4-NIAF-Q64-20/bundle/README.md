# NIAF-20 Sealed Bundle

This bundle preserves the full Design + Code + Test + Evidence tree.

- Archive SHA-256: `24e9ffd24bd61fa20adcbda10d36075bb76a784cc006e5dfe6bb3ec9c5d4c5b5`
- Internal manifest SHA-256: `2101721117a13bb7be05bbef3ddb34926de1a75cabb9af3267d4f997410eac6d`

Reconstruct on a trusted machine:

```bash
base64 -d NIAF-20-sealed.tar.gz.b64 > NIAF-20-sealed.tar.gz
printf '%s  %s\n' 24e9ffd24bd61fa20adcbda10d36075bb76a784cc006e5dfe6bb3ec9c5d4c5b5 NIAF-20-sealed.tar.gz | sha256sum -c -
tar -xzf NIAF-20-sealed.tar.gz
cd NIAF-20
sha256sum -c MANIFEST.sha256
./scripts/verify.sh
```

The bundle is Lo4 proposal-only. Reconstruction does not constitute NEXY integration or promotion.
