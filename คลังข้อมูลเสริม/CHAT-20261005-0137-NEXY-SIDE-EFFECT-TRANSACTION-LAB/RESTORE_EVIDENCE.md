# Restore Raw Evidence

Raw evidence is preserved as `evidence/EVIDENCE_ARCHIVE.b64`.

Expected decoded gzip archive SHA-256:

`a0374e2dee6063bfb19291bf9bc87bd3b688ac09ba04edbba8a82d2105faf52a`

Expected base64-text SHA-256:

`f309eef243dbf74dddf9569de979b7e5dabdf6d944314614e757b7042c2a4e51`

```bash
base64 -d evidence/EVIDENCE_ARCHIVE.b64 > evidence.tar.gz
sha256sum evidence.tar.gz
mkdir evidence-restored
tar -xzf evidence.tar.gz -C evidence-restored
```

The archive contains `EVIDENCE.md` plus raw verification log, benchmark log, environment record, static audit, source observations, test inventory and file inventory from this session.
