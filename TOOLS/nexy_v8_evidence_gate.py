#!/usr/bin/env python3
"""NEXY V8 local evidence consistency gate (stdlib only).

This tool validates evidence record structure and internal consistency.
It CANNOT verify GitHub access, original DOCX bytes, runtime logs, external
provider state, identity/signatures, or approval authenticity. Those require
independent exact-HEAD readback by the executing Codex/auditor.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

REPO = "goif74945-crypto/NEXY.AI-"
BRANCH = "NEXY.ai"
SPEC_SHA = "b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7"
EVIDENCE_IDS = {f"E{i}" for i in range(1, 13)}
ACCEPTED_ATOMS = {"VERIFIED_COMPLIANT", "FIXED_AND_VERIFIED"}
ALL_ATOMS = ACCEPTED_ATOMS | {"NOT_VERIFIED", "FAILED", "BLOCKED", "EXCLUDED"}
HEX40 = re.compile(r"^[a-f0-9]{40}$", re.I)
HEX64 = re.compile(r"^[a-f0-9]{64}$", re.I)
PAR = re.compile(r"^P[0-9]{4,5}(?::[A-Za-z0-9._-]+)?$")


def is_hex40(value: Any) -> bool:
    return isinstance(value, str) and bool(HEX40.fullmatch(value))


def is_hex64(value: Any) -> bool:
    return isinstance(value, str) and bool(HEX64.fullmatch(value))


def is_nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def count_value(value: Any) -> bool:
    return type(value) is int and value >= 0


def inspect_record(data: Any) -> tuple[list[str], bool, dict[str, Any]]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["root must be a JSON object"], False, {}
    if not is_nonempty(data.get("run_id")):
        errors.append("run_id is empty")
    if data.get("product") != REPO or data.get("branch") != BRANCH:
        errors.append("wrong product or branch")
    head = data.get("product_head")
    if not is_hex40(head):
        errors.append("product_head must be 40 hex characters")
    if data.get("spec_sha256") != SPEC_SHA:
        errors.append("actual original-spec SHA is not the required authority SHA")

    inv = data.get("source_inventory")
    if not isinstance(inv, dict):
        inv = {}
        errors.append("source_inventory missing")
    for name in ("tracked_files", "eligible_text_files", "full_text_reads",
                 "semantic_reviews", "unread_or_error_files"):
        if not count_value(inv.get(name)):
            errors.append(f"source_inventory.{name} must be a nonnegative integer")
    if all(count_value(inv.get(k)) for k in ("tracked_files", "eligible_text_files",
                                            "full_text_reads", "semantic_reviews")):
        if not (inv["semantic_reviews"] <= inv["full_text_reads"]
                <= inv["eligible_text_files"] <= inv["tracked_files"]):
            errors.append("source_inventory counts violate semantic<=read<=eligible<=tracked")

    spec = data.get("spec_inventory")
    if not isinstance(spec, dict):
        spec = {}
        errors.append("spec_inventory missing")
    for name in ("normalized_atomic_count", "in_scope_atomic_count",
                 "excluded_atomic_count", "unresolved_authority_conflicts"):
        if not count_value(spec.get(name)):
            errors.append(f"spec_inventory.{name} must be a nonnegative integer")
    if type(spec.get("all_clauses_enumerated")) is not bool:
        errors.append("spec_inventory.all_clauses_enumerated must be boolean")
    if not is_hex64(spec.get("source_register_sha256")):
        errors.append("spec_inventory.source_register_sha256 requires a real digest format")

    atoms = data.get("atoms")
    if not isinstance(atoms, list) or not atoms:
        atoms = []
        errors.append("atoms must be nonempty list")
    seen: set[str] = set()
    applicable = excluded = 0
    accepted_atoms = 0
    for idx, atom in enumerate(atoms):
        prefix = f"atoms[{idx}]"
        if not isinstance(atom, dict):
            errors.append(f"{prefix} must be an object")
            continue
        atom_id = atom.get("id")
        if not is_nonempty(atom_id):
            errors.append(f"{prefix}.id missing")
        elif atom_id in seen:
            errors.append(f"duplicate atomic ID {atom_id}")
        else:
            seen.add(atom_id)
        if not isinstance(atom.get("spec_locator"), str) or not PAR.fullmatch(atom["spec_locator"]):
            errors.append(f"{prefix}.spec_locator invalid")
        applicability = atom.get("applicability")
        verdict = atom.get("verdict")
        if applicability == "APPLICABLE":
            applicable += 1
        elif applicability == "EXCLUDED":
            excluded += 1
        elif applicability != "AMBIGUOUS":
            errors.append(f"{prefix}.applicability invalid")
        if verdict not in ALL_ATOMS:
            errors.append(f"{prefix}.verdict invalid")
        if verdict == "EXCLUDED" and (
            applicability != "EXCLUDED" or not is_nonempty(atom.get("finding"))
        ):
            errors.append(f"{prefix}: exclusion requires spec-backed finding")
        sources = atom.get("source_refs", [])
        proofs = atom.get("runtime_proofs", [])
        if not isinstance(sources, list) or not isinstance(proofs, list):
            errors.append(f"{prefix}: source_refs/runtime_proofs must be lists")
            continue
        if verdict in ACCEPTED_ATOMS:
            accepted_atoms += 1
            if applicability != "APPLICABLE":
                errors.append(f"{prefix}: verified verdict requires APPLICABLE")
            if not sources:
                errors.append(f"{prefix}: accepted atom has no source refs")
            else:
                for s in sources:
                    if (not isinstance(s, dict) or not is_nonempty(s.get("path"))
                            or not is_hex40(s.get("git_blob_sha"))
                            or s.get("review_status") != "SEMANTICALLY_REVIEWED"):
                        errors.append(f"{prefix}: accepted source must be fully semantically reviewed")
            kinds: set[str] = set()
            for p in proofs:
                if not isinstance(p, dict):
                    errors.append(f"{prefix}: proof must be object")
                    continue
                kinds.add(str(p.get("kind", "")))
                if (not is_nonempty(p.get("command_or_test")) or type(p.get("exit_code")) is not int
                        or p.get("exit_code") != 0 or not is_hex64(p.get("log_sha256"))
                        or p.get("source_head") != head or not is_nonempty(p.get("environment"))
                        or not is_nonempty(p.get("artifact_locator"))):
                    errors.append(f"{prefix}: proof lacks exact-HEAD passing command/log/environment/artifact")
            if "POSITIVE" not in kinds or not kinds.intersection(
                {"NEGATIVE", "ADVERSARIAL", "PROPERTY", "MODEL"}
            ):
                errors.append(f"{prefix}: positive + negative/adversarial proofs required")
            if verdict == "FIXED_AND_VERIFIED":
                if atom.get("commit_sha") != head or not is_hex40(atom.get("remote_readback_sha")):
                    errors.append(f"{prefix}: fixed atom needs final product HEAD commit + readback SHA")
    if count_value(spec.get("normalized_atomic_count")) and spec["normalized_atomic_count"] != len(atoms):
        errors.append("normalized_atomic_count differs from atomic rows supplied")
    if count_value(spec.get("in_scope_atomic_count")) and spec["in_scope_atomic_count"] != applicable:
        errors.append("in_scope_atomic_count differs from APPLICABLE rows")
    if count_value(spec.get("excluded_atomic_count")) and spec["excluded_atomic_count"] != excluded:
        errors.append("excluded_atomic_count differs from EXCLUDED rows")

    doc_e = data.get("doc_e")
    if not isinstance(doc_e, list):
        doc_e = []
        errors.append("doc_e must be list")
    doc_ids: list[str] = []
    release_count = 0
    for i, e in enumerate(doc_e):
        if not isinstance(e, dict):
            errors.append(f"doc_e[{i}] must be object")
            continue
        doc_ids.append(str(e.get("id")))
        if e.get("source_head") != head:
            errors.append(f"doc_e[{i}]: stale proof HEAD")
        status = e.get("status")
        if status not in {"NOT_VERIFIED", "PASSED", "FAILED", "BLOCKED"}:
            errors.append(f"doc_e[{i}]: invalid status")
        if status == "PASSED":
            release_count += 1
            if not is_hex64(e.get("proof_sha256")) or not is_nonempty(e.get("artifact_locator")):
                errors.append(f"doc_e[{i}]: passed gate lacks proof digest and location")
            if e.get("id") == "E11" and not is_nonempty(e.get("approval_ref")):
                errors.append("E11: signed owner approval evidence is required")
    if len(doc_ids) != 12 or set(doc_ids) != EVIDENCE_IDS:
        errors.append("doc_e requires unique E1..E12, each exactly once")
    approval = data.get("approval", {})
    if approval is not None and not isinstance(approval, dict):
        errors.append("approval must be object")
        approval = {}
    status = data.get("overall_status")
    if status not in {"PARTIAL", "BLOCKED", "FAILED", "ACCEPTED"}:
        errors.append("overall_status invalid")
    structurally_ready = (
        bool(atoms)
        and spec.get("all_clauses_enumerated") is True
        and spec.get("unresolved_authority_conflicts") == 0
        and count_value(spec.get("in_scope_atomic_count"))
        and applicable == accepted_atoms == spec.get("in_scope_atomic_count")
        and count_value(inv.get("eligible_text_files"))
        and inv.get("full_text_reads") == inv.get("eligible_text_files")
        and inv.get("semantic_reviews") == inv.get("eligible_text_files")
        and inv.get("unread_or_error_files") == 0
        and release_count == 12
        and isinstance(approval, dict)
        and approval.get("status") == "VERIFIED"
        and is_nonempty(approval.get("evidence_locator"))
    )
    if status == "ACCEPTED" and not structurally_ready:
        errors.append("ACCEPTED is false: missing coverage, spec, verified atoms, E1-E12 or signoff")
    summary = {
        "atomic_rows": len(atoms),
        "applicable_rows": applicable,
        "accepted_atoms_structural": accepted_atoms,
        "doc_e_passed_structural": release_count,
        "structurally_ready_for_independent_verification": structurally_ready,
        "overall_status_reported": status,
        "warning": "Format and cross-field consistency only; actual proof/log/source/auth/signoff readback REQUIRED.",
    }
    return errors, structurally_ready and not errors, summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path, help="JSON evidence record from Codex")
    parser.add_argument("--allow-incomplete", action="store_true",
                        help="exit 0 for structurally sound PARTIAL/BLOCKED records, not for release")
    args = parser.parse_args()
    try:
        data = json.loads(args.record.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "INVALID", "errors": [str(exc)]}, ensure_ascii=False))
        return 3
    errors, ready, summary = inspect_record(data)
    if errors:
        print(json.dumps({"status": "INVALID", "errors": errors, "summary": summary}, indent=2))
        return 3
    if not ready or data.get("overall_status") != "ACCEPTED":
        print(json.dumps({"status": "NOT_ACCEPTED", "summary": summary}, indent=2))
        return 0 if args.allow_incomplete else 2
    print(json.dumps({"status": "FORMAT_GATE_PASSED_ONLY", "summary": summary}, indent=2))
    print("IMPORTANT: A separate auditor MUST validate actual logs, original DOCX, Git blobs and approvals.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
