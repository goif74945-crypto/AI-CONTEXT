# Proposed Integration Architecture — AI-PROPOSED ONLY

```text
External / Model / Tool Inputs
        |
        v
[Context Taint Firewall]
        |
        v
[Semantic Capability ABI Compiler] <--- provider declarations
        |
        +----> [Model Drift Sentinel] <--- probe observations/baseline
        |
        v
NEXY authority / judge decision  (existing concept; NOT modified here)
        |
        v
[Scoped Authority Lease Engine]
        |
        v
[Effect Transaction Coordinator]
        |
        v
External tool side effects
```

The five systems are deliberately complementary: CTF guards information trust, SCAC guards semantic adapter compatibility, MDS guards temporal provider behavior, SALE guards delegated authority, and ETC guards multi-step external mutation integrity.

No existing NEXY.AI implementation file was changed.
