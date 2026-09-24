#!/usr/bin/env python3
"""Deterministic NEXY context-pack generator.

Reads only AI-CONTEXT registry files. It does not call network services and does
not infer PASS from implementation/test/evidence locations.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def file_hash(path: Path) -> str | None:
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def intersects(values: Iterable[str], selected: set[str]) -> bool:
    return bool(set(values) & selected)


def stable(items: Iterable[dict[str, Any]], key: str) -> list[dict[str, Any]]:
    return sorted(items, key=lambda x: str(x.get(key, "")))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="projects/NEXY.AI")
    ap.add_argument("--profile", choices=["BUILDER", "AUDITOR"], required=True)
    ap.add_argument("--task-type", required=True)
    ap.add_argument("--entity", action="append", default=[])
    ap.add_argument("--requirement", action="append", default=[])
    ap.add_argument("--expected-head")
    ap.add_argument("--max-dependency-depth", type=int, default=2)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    root = Path(args.root)
    routes_doc = load_json(root / "context-router/routes.json", {"routes": []})
    route = next((r for r in routes_doc["routes"] if r["task_type"] == args.task_type), None)
    if route is None:
        raise SystemExit(f"unknown task type: {args.task_type}")

    entities = load_jsonl(root / "ontology/entities.jsonl")
    relationships = load_jsonl(root / "ontology/relationships.jsonl")
    requirements = load_jsonl(root / "requirements/requirements.jsonl")
    contracts = load_jsonl(root / "contracts/contracts.jsonl")
    fsms = load_jsonl(root / "fsm/fsm-registry.jsonl")
    invariants = load_jsonl(root / "invariants/invariants.jsonl")
    implementation = load_jsonl(root / "implementation/system-to-code.jsonl")
    traces = load_jsonl(root / "traceability/requirement-trace.jsonl")
    failures = load_jsonl(root / "failures/failures.jsonl")
    events = load_jsonl(root / "events/events.jsonl")
    golden = load_jsonl(root / "examples/golden/examples.jsonl")
    negative = load_jsonl(root / "examples/negative/examples.jsonl")

    authority = load_json(root / "governance/authority-graph.json", {})
    supersession = load_json(root / "governance/supersession-graph.json", {})
    conflicts = load_jsonl(root / "governance/conflicts.jsonl")
    security = {
        "trust_boundaries": load_json(root / "security/trust-boundaries.json", {}),
        "permissions": load_json(root / "security/permission-matrix.json", {}),
        "threat_model": load_json(root / "security/threat-model.json", {}),
    }
    state = {
        "ownership": load_json(root / "state/state-ownership.json", {}),
        "persistence": load_json(root / "state/persistence-map.json", {}),
    }
    config = load_json(root / "config/config-registry.json", {})
    playbooks = load_json(root / "playbooks/registry.json", {"playbooks": []})

    entity_by_id = {e["id"]: e for e in entities}
    req_by_id = {r["requirement_id"]: r for r in requirements}
    selected_entities = set(route.get("seed_entities", [])) | set(args.entity)
    selected_requirements = set(args.requirement)

    for rid in list(selected_requirements):
        selected_entities.update(req_by_id.get(rid, {}).get("system_ids", []))

    # Resolve requirements for seed entities.
    for r in requirements:
        if intersects(r.get("system_ids", []), selected_entities):
            selected_requirements.add(r["requirement_id"])

    # Dependency closure. REQUIRES direction is dependent -> prerequisite.
    req_edges = [e for e in relationships if e.get("type") == "REQUIRES"]
    for _ in range(max(0, args.max_dependency_depth)):
        before = set(selected_entities)
        for e in req_edges:
            if e["from"] in selected_entities:
                selected_entities.add(e["to"])
            if "dependents" in route.get("include", []) and e["to"] in selected_entities:
                selected_entities.add(e["from"])
        if selected_entities == before:
            break

    # Re-resolve requirements after dependency expansion.
    for r in requirements:
        if intersects(r.get("system_ids", []), selected_entities):
            selected_requirements.add(r["requirement_id"])

    entity_rows = stable((entity_by_id[e] for e in selected_entities if e in entity_by_id), "id")
    req_rows = stable((req_by_id[r] for r in selected_requirements if r in req_by_id), "requirement_id")
    dep_rows = sorted(
        [e for e in relationships if e.get("from") in selected_entities and e.get("to") in selected_entities],
        key=lambda x: (x.get("from", ""), x.get("type", ""), x.get("to", "")),
    )

    contract_rows = stable(
        [c for c in contracts if c.get("contract_id") in selected_entities
         or c.get("owner_entity_id") in selected_entities
         or intersects(c.get("related_entity_ids", []), selected_entities)
         or intersects(c.get("requirement_ids", []), selected_requirements)],
        "contract_id",
    )
    fsm_rows = stable(
        [f for f in fsms if f.get("fsm_id") in selected_entities
         or intersects(f.get("requirement_ids", []), selected_requirements)],
        "fsm_id",
    )
    invariant_rows = stable(
        [i for i in invariants if intersects(i.get("governing_entity_ids", []), selected_entities)
         or intersects(i.get("requirement_ids", []), selected_requirements)],
        "invariant_id",
    )
    impl_rows = stable([m for m in implementation if m.get("entity_id") in selected_entities], "entity_id")
    trace_rows = stable([t for t in traces if t.get("requirement_id") in selected_requirements], "requirement_id")
    failure_rows = stable(
        [f for f in failures if intersects(f.get("affected_system_ids", []), selected_entities)],
        "failure_id",
    )
    event_rows = stable(
        [e for e in events if intersects(e.get("producer_ids", []), selected_entities)
         or intersects(e.get("consumer_ids", []), selected_entities)
         or ("FSM-EXECUTION" in selected_entities and e.get("namespace") == "DOC_C_EXECUTION")],
        "event_id",
    )

    config_entries = [
        e for e in config.get("entries", [])
        if e.get("owner") in selected_entities or e.get("source_requirement") in selected_requirements
    ]
    relevant_conflicts = [
        c for c in conflicts
        if intersects(c.get("affected_entities", []), selected_entities)
    ]

    example_pool = negative if args.profile == "AUDITOR" else golden + negative
    examples = sorted(
        [e for e in example_pool if intersects(e.get("requirements", []), selected_requirements)],
        key=lambda x: x.get("id", ""),
    )

    selected_playbooks = [
        p for p in playbooks.get("playbooks", [])
        if p.get("task_type") == route.get("playbook")
    ]

    test_refs: dict[str, dict[str, Any]] = {}
    evidence_refs: dict[str, dict[str, Any]] = {}
    for t in trace_rows:
        for x in t.get("test_refs", []):
            test_refs.setdefault(x["path"], x)
        for x in t.get("evidence_refs", []):
            evidence_refs.setdefault(x["path"], x)

    open_unknowns: list[str] = []
    for m in impl_rows:
        if m.get("mapping_status") == "UNMAPPED":
            open_unknowns.append(f"implementation unmapped: {m.get('entity_id')}")
        if m.get("mapping_status") == "CANDIDATE":
            open_unknowns.append(f"candidate implementation mapping requires inspection: {m.get('entity_id')}")
        if args.expected_head and m.get("head") != args.expected_head:
            open_unknowns.append(
                f"stale implementation head for {m.get('entity_id')}: {m.get('head')} != {args.expected_head}"
            )
    for t in trace_rows:
        if t.get("test_coverage") != "CANDIDATE_STATIC":
            open_unknowns.append(f"test coverage unresolved: {t.get('requirement_id')}")
        if t.get("verdict") != "NOT_EVALUATED":
            open_unknowns.append(f"unexpected pre-existing verdict requires review: {t.get('requirement_id')}")

    source_files = [
        root / "ontology/entities.jsonl",
        root / "ontology/relationships.jsonl",
        root / "requirements/requirements.jsonl",
        root / "governance/authority-graph.json",
        root / "governance/supersession-graph.json",
        root / "governance/conflicts.jsonl",
        root / "contracts/contracts.jsonl",
        root / "fsm/fsm-registry.jsonl",
        root / "invariants/invariants.jsonl",
        root / "implementation/system-to-code.jsonl",
        root / "traceability/requirement-trace.jsonl",
        root / "failures/failures.jsonl",
        root / "security/trust-boundaries.json",
        root / "state/state-ownership.json",
        root / "events/events.jsonl",
        root / "config/config-registry.json",
        root / "playbooks/registry.json",
    ]
    input_hashes = {str(p.relative_to(root)): file_hash(p) for p in source_files}
    identity = {
        "profile": args.profile,
        "task_type": args.task_type,
        "entities": sorted(selected_entities),
        "requirements": sorted(selected_requirements),
        "input_hashes": input_hashes,
    }
    pack_id = hashlib.sha256(
        json.dumps(identity, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()

    pack = {
        "pack_id": pack_id,
        "profile": args.profile,
        "task_type": args.task_type,
        "generated_from": {
            "router_schema_version": routes_doc.get("schema_version"),
            "input_hashes": input_hashes,
            "expected_head": args.expected_head,
        },
        "scope": {
            "route": route,
            "selected_entity_ids": sorted(selected_entities),
            "selected_requirement_ids": sorted(selected_requirements),
        },
        "entities": entity_rows,
        "requirements": req_rows,
        "dependencies": dep_rows,
        "authority": {
            "graph": authority,
            "supersession": supersession,
            "relevant_conflicts": relevant_conflicts,
        },
        "contracts": contract_rows,
        "fsms": fsm_rows,
        "invariants": invariant_rows,
        "implementation": impl_rows,
        "tests": [test_refs[k] for k in sorted(test_refs)],
        "evidence": [evidence_refs[k] for k in sorted(evidence_refs)],
        "failures": failure_rows,
        "security": security if "security" in route.get("include", []) else {},
        "state": state if "state" in route.get("include", []) else {},
        "events": event_rows if "events" in route.get("include", []) else [],
        "config": {"entries": config_entries} if "config" in route.get("include", []) else {},
        "playbooks": selected_playbooks,
        "examples": examples,
        "open_unknowns": sorted(set(open_unknowns)),
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(pack, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "pack_id": pack_id,
        "entities": len(entity_rows),
        "requirements": len(req_rows),
        "contracts": len(contract_rows),
        "fsms": len(fsm_rows),
        "invariants": len(invariant_rows),
        "implementation": len(impl_rows),
        "tests": len(test_refs),
        "evidence": len(evidence_refs),
        "failures": len(failure_rows),
        "open_unknowns": len(pack["open_unknowns"]),
        "output": str(out),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
