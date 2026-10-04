# Requirement / Evidence Ledger

| ID | Requirement | Implementation | Evidence target | Current status |
|---|---|---|---|---|
| LII-001 | superseded directive invalidates old work | `interrupt_epoch.py` | unit + adversarial | PASS locally |
| LII-002 | action changes after prepare freeze | `interrupt_epoch.py` | unit | PASS locally |
| LII-003 | action lease single-use | `interrupt_epoch.py` | unit | PASS locally |
| LII-004 | cache isolation by user/project/policy/model/tool/schema/input | `cache_provenance.py` | unit + adversarial | PASS locally |
| LII-005 | cache tamper detection | `cache_provenance.py` | adversarial | PASS locally |
| LII-006 | cross-modality critical fields equal | `multimodal_intent.py` | unit + adversarial | PASS locally |
| LII-007 | missing required modality freezes | `multimodal_intent.py` | unit | PASS locally |
| LII-008 | output stream sequence is contiguous and identity-consistent | `completion_boundary.py` | unit + adversarial | PASS locally |
| LII-009 | exactly one final marker exists at stream tail and binds full payload hash | `completion_boundary.py` | unit + adversarial | PASS locally |
| LII-010 | EOF/truncation, chunk gap, mixed contract/run or final digest mismatch freeze | `completion_boundary.py` | unit + adversarial | PASS locally |
| LII-011 | required inputs must exist uniquely and match kind/trust/digest | `input_cohesion.py` | unit + adversarial | PASS locally |
| LII-012 | unreferenced inputs are quarantined | `input_cohesion.py` | unit | PASS locally |
| LII-013 | passing intent+input+epoch compile to one deterministic snapshot | `coordinator.py` | integration + determinism | PASS locally |
| LII-014 | hash-seed-independent reference fingerprints | canonical serialization + probe | subprocess probe seeds 1/2/777 | PASS locally |
| LII-015 | Python source parses/compiles | package | `compileall` | PASS locally |
| LII-016 | NEXY.AI repo untouched | mutation boundary | connector write audit | PASS — all mutation tool targets were AI-CONTEXT |
| LII-017 | committed code bytes equal locally tested bytes | manifest Git blob SHA | post-write fetch | PASS — 19/19 Git blobs matched |
| LII-018 | production NEXY integration | OUT OF SCOPE | E3/E4/E5 in actual NEXY | NOT_VERIFIED |
