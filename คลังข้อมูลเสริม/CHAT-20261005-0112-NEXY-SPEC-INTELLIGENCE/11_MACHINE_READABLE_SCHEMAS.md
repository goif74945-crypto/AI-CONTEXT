# Machine-Readable Schemas

Requirement record:
```json
{"rid":"AREA-NNN","authority":"project_spec","modality":"MUST","scope":["component"],"trigger":"condition","behavior":"observable obligation","evidence_required":["test","artifact"],"dependencies":[],"conflicts":[],"mutability":"immutable","status":"unimplemented"}
```

Evidence record:
```json
{"eid":"E-NNN","rid":["AREA-NNN"],"method":"deterministic_check","result":"pass","artifact":"path-or-tool-reference","observed_at":"ISO-8601","limitations":[]}
```

Checkpoint record:
```json
{"chat_id":"CHAT-...","objective":"...","allowed_mutations":[],"forbidden_mutations":[],"completed":[],"in_progress":[],"blocked":[],"unknowns":[],"next_action":"...","verification_status":"..."}
```

Schemas are interfaces. Extend additively where possible; version semantic changes.