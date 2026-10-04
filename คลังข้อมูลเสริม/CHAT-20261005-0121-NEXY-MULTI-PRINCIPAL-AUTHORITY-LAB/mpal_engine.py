#!/usr/bin/env python3
"""NEXY Multi-Principal Authority Lattice (MPAL) reference engine.

This is an experimental, standalone auxiliary prototype. It does not mutate NEXY,
replace NEXY RBAC, or establish current product requirements.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

DECISION_STATES = {"ALLOW", "DENY", "PENDING", "FREEZE"}
APPROVAL_DECISIONS = {"APPROVE", "DENY"}
DENY_MODES = {"ANY_ELIGIBLE_DENY", "VETO_ROLES_ONLY"}
HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{1,127}$")


@dataclass(frozen=True)
class Finding:
    code: str
    path: str
    message: str
    severity: str = "ERROR"


@dataclass(frozen=True)
class ValidationReport:
    ok: bool
    findings: tuple[Finding, ...]

    def to_dict(self) -> dict[str, Any]:
        return {"ok": self.ok, "findings": [asdict(f) for f in self.findings]}


@dataclass(frozen=True)
class Decision:
    state: str
    request_sha256: str
    policy_sha256: str
    rule_id: str | None
    reason_codes: tuple[str, ...]
    counted_approvals: tuple[tuple[str, tuple[str, ...]], ...]
    ignored_approvals: tuple[tuple[str, str], ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "state": self.state,
            "request_sha256": self.request_sha256,
            "policy_sha256": self.policy_sha256,
            "rule_id": self.rule_id,
            "reason_codes": list(self.reason_codes),
            "counted_approvals": {k: list(v) for k, v in self.counted_approvals},
            "ignored_approvals": [{"principal_id": p, "reason": r} for p, r in self.ignored_approvals],
        }


def _s(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _valid_id(value: Any) -> bool:
    return _s(value) and bool(ID_RE.fullmatch(value))


def _canonicalize(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {k: _canonicalize(value[k]) for k in sorted(value)}
    if isinstance(value, list):
        normalized = [_canonicalize(x) for x in value]
        if all(isinstance(x, Mapping) for x in normalized):
            for key in ("principal_id", "rule_id", "group_id"):
                if all(_s(x.get(key)) for x in normalized):
                    return sorted(normalized, key=lambda x: str(x[key]))
        if all(isinstance(x, str) for x in normalized):
            return sorted(normalized)
        return normalized
    return value


def _sha256_json(value: Any) -> str:
    payload = json.dumps(_canonicalize(value), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def policy_sha256(policy: Mapping[str, Any]) -> str:
    return _sha256_json(policy)


def request_sha256(request: Mapping[str, Any]) -> str:
    return _sha256_json(request)


def _dupes(values: Iterable[str]) -> set[str]:
    seen: set[str] = set()
    out: set[str] = set()
    for value in values:
        if value in seen:
            out.add(value)
        seen.add(value)
    return out


def validate_policy(policy: Any) -> ValidationReport:
    f: list[Finding] = []
    if not isinstance(policy, Mapping):
        return ValidationReport(False, (Finding("POLICY_NOT_OBJECT", "$", "Policy must be a JSON object."),))
    for key in ("policy_id", "version", "principals", "rules"):
        if key not in policy:
            f.append(Finding("MISSING_FIELD", f"$.{key}", "Required field missing."))
    if f:
        return ValidationReport(False, tuple(f))

    if not _valid_id(policy.get("policy_id")):
        f.append(Finding("INVALID_POLICY_ID", "$.policy_id", "Invalid policy id."))
    if not isinstance(policy.get("version"), int) or policy["version"] < 1:
        f.append(Finding("INVALID_VERSION", "$.version", "Version must be a positive integer."))

    principals = policy.get("principals")
    if not isinstance(principals, list) or not principals:
        f.append(Finding("PRINCIPALS_REQUIRED", "$.principals", "At least one principal is required."))
        principals = []
    principal_ids: list[str] = []
    active_by_role_domain: dict[tuple[str, str], set[str]] = {}
    for i, p in enumerate(principals):
        path = f"$.principals[{i}]"
        if not isinstance(p, Mapping):
            f.append(Finding("PRINCIPAL_NOT_OBJECT", path, "Principal must be an object."))
            continue
        for key in ("principal_id", "roles", "domains", "active"):
            if key not in p:
                f.append(Finding("MISSING_FIELD", f"{path}.{key}", "Required field missing."))
        pid = p.get("principal_id")
        if not _valid_id(pid):
            f.append(Finding("INVALID_PRINCIPAL_ID", f"{path}.principal_id", "Invalid principal id."))
        else:
            principal_ids.append(pid)
        roles = p.get("roles")
        domains = p.get("domains")
        if not isinstance(roles, list) or not roles or not all(_valid_id(x) for x in roles):
            f.append(Finding("INVALID_ROLES", f"{path}.roles", "roles must be a non-empty list of ids."))
            roles = []
        if isinstance(roles, list) and len(set(roles)) != len(roles):
            f.append(Finding("DUPLICATE_ROLE", f"{path}.roles", "roles must be unique."))
        if not isinstance(domains, list) or not domains or not all(_valid_id(x) for x in domains):
            f.append(Finding("INVALID_DOMAINS", f"{path}.domains", "domains must be a non-empty list of ids."))
            domains = []
        if isinstance(domains, list) and len(set(domains)) != len(domains):
            f.append(Finding("DUPLICATE_DOMAIN", f"{path}.domains", "domains must be unique."))
        if not isinstance(p.get("active"), bool):
            f.append(Finding("INVALID_ACTIVE", f"{path}.active", "active must be boolean."))
        if p.get("active") is True and _valid_id(pid) and isinstance(roles, list) and isinstance(domains, list):
            for role in roles:
                for domain in domains:
                    active_by_role_domain.setdefault((role, domain), set()).add(pid)
    for dup in sorted(_dupes(principal_ids)):
        f.append(Finding("DUPLICATE_PRINCIPAL_ID", "$.principals", f"Duplicate principal id: {dup}"))

    rules = policy.get("rules")
    if not isinstance(rules, list) or not rules:
        f.append(Finding("RULES_REQUIRED", "$.rules", "At least one rule is required."))
        rules = []
    rule_ids: list[str] = []
    selectors: list[tuple[str, str]] = []
    for i, rule in enumerate(rules):
        path = f"$.rules[{i}]"
        if not isinstance(rule, Mapping):
            f.append(Finding("RULE_NOT_OBJECT", path, "Rule must be an object."))
            continue
        required = (
            "rule_id", "domain", "action", "requester_roles", "approval_groups",
            "veto_roles", "deny_mode", "requester_may_approve", "min_distinct_approvers"
        )
        for key in required:
            if key not in rule:
                f.append(Finding("MISSING_FIELD", f"{path}.{key}", "Required field missing."))
        rid = rule.get("rule_id")
        if not _valid_id(rid):
            f.append(Finding("INVALID_RULE_ID", f"{path}.rule_id", "Invalid rule id."))
        else:
            rule_ids.append(rid)
        domain = rule.get("domain")
        action = rule.get("action")
        if not _valid_id(domain):
            f.append(Finding("INVALID_RULE_DOMAIN", f"{path}.domain", "Invalid domain id."))
        if not _valid_id(action):
            f.append(Finding("INVALID_RULE_ACTION", f"{path}.action", "Invalid action id."))
        if _valid_id(domain) and _valid_id(action):
            selectors.append((domain, action))

        requester_roles = rule.get("requester_roles")
        if not isinstance(requester_roles, list) or not requester_roles or not all(_valid_id(x) for x in requester_roles):
            f.append(Finding("INVALID_REQUESTER_ROLES", f"{path}.requester_roles", "requester_roles must be non-empty ids."))
            requester_roles = []
        veto_roles = rule.get("veto_roles")
        if not isinstance(veto_roles, list) or not all(_valid_id(x) for x in veto_roles):
            f.append(Finding("INVALID_VETO_ROLES", f"{path}.veto_roles", "veto_roles must be ids."))
            veto_roles = []
        if rule.get("deny_mode") not in DENY_MODES:
            f.append(Finding("INVALID_DENY_MODE", f"{path}.deny_mode", f"Expected one of {sorted(DENY_MODES)}."))
        if not isinstance(rule.get("requester_may_approve"), bool):
            f.append(Finding("INVALID_REQUESTER_APPROVAL_FLAG", f"{path}.requester_may_approve", "Must be boolean."))
        min_distinct = rule.get("min_distinct_approvers")
        if not isinstance(min_distinct, int) or min_distinct < 0:
            f.append(Finding("INVALID_MIN_DISTINCT", f"{path}.min_distinct_approvers", "Must be integer >= 0."))

        groups = rule.get("approval_groups")
        if not isinstance(groups, list) or not groups:
            f.append(Finding("APPROVAL_GROUPS_REQUIRED", f"{path}.approval_groups", "At least one approval group is required."))
            groups = []
        group_ids: list[str] = []
        eligible_union: set[str] = set()
        for j, group in enumerate(groups):
            gpath = f"{path}.approval_groups[{j}]"
            if not isinstance(group, Mapping):
                f.append(Finding("GROUP_NOT_OBJECT", gpath, "Approval group must be object."))
                continue
            for key in ("group_id", "eligible_roles", "threshold"):
                if key not in group:
                    f.append(Finding("MISSING_FIELD", f"{gpath}.{key}", "Required field missing."))
            gid = group.get("group_id")
            if not _valid_id(gid):
                f.append(Finding("INVALID_GROUP_ID", f"{gpath}.group_id", "Invalid group id."))
            else:
                group_ids.append(gid)
            eligible_roles = group.get("eligible_roles")
            if not isinstance(eligible_roles, list) or not eligible_roles or not all(_valid_id(x) for x in eligible_roles):
                f.append(Finding("INVALID_ELIGIBLE_ROLES", f"{gpath}.eligible_roles", "eligible_roles must be non-empty ids."))
                eligible_roles = []
            threshold = group.get("threshold")
            if not isinstance(threshold, int) or threshold < 1:
                f.append(Finding("INVALID_THRESHOLD", f"{gpath}.threshold", "threshold must be integer >= 1."))
            if _valid_id(domain) and isinstance(eligible_roles, list) and isinstance(threshold, int) and threshold >= 1:
                eligible: set[str] = set()
                for role in eligible_roles:
                    eligible.update(active_by_role_domain.get((role, domain), set()))
                eligible_union.update(eligible)
                if len(eligible) < threshold:
                    f.append(Finding(
                        "UNSATISFIABLE_GROUP",
                        gpath,
                        f"Threshold {threshold} exceeds active eligible principals {len(eligible)} for domain {domain}."
                    ))
        for dup in sorted(_dupes(group_ids)):
            f.append(Finding("DUPLICATE_GROUP_ID", f"{path}.approval_groups", f"Duplicate group id: {dup}"))
        if isinstance(min_distinct, int) and min_distinct > len(eligible_union):
            f.append(Finding("UNSATISFIABLE_MIN_DISTINCT", path, "min_distinct_approvers exceeds active eligible principals."))

    for dup in sorted(_dupes(rule_ids)):
        f.append(Finding("DUPLICATE_RULE_ID", "$.rules", f"Duplicate rule id: {dup}"))
    for dup in sorted(_dupes([f"{d}\0{a}" for d, a in selectors])):
        d, a = dup.split("\0", 1)
        f.append(Finding("AMBIGUOUS_RULE_SELECTOR", "$.rules", f"Multiple rules match domain={d} action={a}."))

    return ValidationReport(not any(x.severity == "ERROR" for x in f), tuple(f))


def validate_request(request: Any) -> ValidationReport:
    f: list[Finding] = []
    if not isinstance(request, Mapping):
        return ValidationReport(False, (Finding("REQUEST_NOT_OBJECT", "$", "Request must be an object."),))
    for key in ("request_id", "requester_id", "domain", "action", "target_id", "payload_sha256", "policy_version"):
        if key not in request:
            f.append(Finding("MISSING_FIELD", f"$.{key}", "Required field missing."))
    for key in ("request_id", "requester_id", "domain", "action", "target_id"):
        if key in request and not _valid_id(request.get(key)):
            f.append(Finding("INVALID_ID", f"$.{key}", "Invalid identifier."))
    if "payload_sha256" in request and (not isinstance(request.get("payload_sha256"), str) or not HEX64_RE.fullmatch(request["payload_sha256"])):
        f.append(Finding("INVALID_PAYLOAD_HASH", "$.payload_sha256", "payload_sha256 must be lowercase SHA-256 hex."))
    if "policy_version" in request and (not isinstance(request.get("policy_version"), int) or request["policy_version"] < 1):
        f.append(Finding("INVALID_POLICY_VERSION", "$.policy_version", "policy_version must be positive integer."))
    return ValidationReport(not f, tuple(f))


def _principal_map(policy: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {p["principal_id"]: p for p in policy["principals"] if isinstance(p, Mapping) and _s(p.get("principal_id"))}


def _find_rule(policy: Mapping[str, Any], request: Mapping[str, Any]) -> Mapping[str, Any] | None:
    matches = [r for r in policy["rules"] if r.get("domain") == request.get("domain") and r.get("action") == request.get("action")]
    if len(matches) == 1:
        return matches[0]
    return None


def _roles(principal: Mapping[str, Any]) -> set[str]:
    return set(principal.get("roles", []))


def _domain_allowed(principal: Mapping[str, Any], domain: str) -> bool:
    return domain in set(principal.get("domains", []))


def _freeze(policy: Mapping[str, Any], request: Mapping[str, Any], rule_id: str | None, codes: Iterable[str]) -> Decision:
    return Decision(
        state="FREEZE",
        request_sha256=request_sha256(request),
        policy_sha256=policy_sha256(policy),
        rule_id=rule_id,
        reason_codes=tuple(sorted(set(codes))),
        counted_approvals=tuple(),
        ignored_approvals=tuple(),
    )


def evaluate(
    policy: Mapping[str, Any],
    request: Mapping[str, Any],
    approvals: Sequence[Mapping[str, Any]],
    *,
    evaluation_tick: int,
) -> Decision:
    if not isinstance(evaluation_tick, int) or evaluation_tick < 0:
        raise ValueError("evaluation_tick must be an integer >= 0")

    policy_report = validate_policy(policy)
    if not policy_report.ok:
        return _freeze(policy, request, None, ["POLICY_INVALID"] + [x.code for x in policy_report.findings])
    request_report = validate_request(request)
    if not request_report.ok:
        return _freeze(policy, request, None, ["REQUEST_INVALID"] + [x.code for x in request_report.findings])
    if request["policy_version"] != policy["version"]:
        return _freeze(policy, request, None, ["REQUEST_POLICY_VERSION_MISMATCH"])

    principals = _principal_map(policy)
    requester = principals.get(request["requester_id"])
    if requester is None:
        return _freeze(policy, request, None, ["UNKNOWN_REQUESTER"])
    if not requester.get("active"):
        return Decision(
            "DENY", request_sha256(request), policy_sha256(policy), None,
            ("REQUESTER_INACTIVE",), tuple(), tuple()
        )
    if not _domain_allowed(requester, request["domain"]):
        return Decision(
            "DENY", request_sha256(request), policy_sha256(policy), None,
            ("REQUESTER_DOMAIN_DENIED",), tuple(), tuple()
        )

    selector_matches = [r for r in policy["rules"] if r.get("domain") == request["domain"] and r.get("action") == request["action"]]
    if not selector_matches:
        return Decision(
            "DENY", request_sha256(request), policy_sha256(policy), None,
            ("NO_AUTHORIZATION_RULE",), tuple(), tuple()
        )
    if len(selector_matches) != 1:
        return _freeze(policy, request, None, ["AMBIGUOUS_AUTHORIZATION_RULE"])
    rule = selector_matches[0]
    rule_id = rule["rule_id"]
    if not (_roles(requester) & set(rule["requester_roles"])):
        return Decision(
            "DENY", request_sha256(request), policy_sha256(policy), rule_id,
            ("REQUESTER_ROLE_DENIED",), tuple(), tuple()
        )

    req_hash = request_sha256(request)
    group_map = {g["group_id"]: g for g in rule["approval_groups"]}

    # Ensure this particular requester still leaves each group satisfiable when self-approval is forbidden.
    for gid, group in group_map.items():
        eligible: set[str] = set()
        for pid, principal in principals.items():
            if not principal.get("active") or not _domain_allowed(principal, request["domain"]):
                continue
            if not rule["requester_may_approve"] and pid == request["requester_id"]:
                continue
            if _roles(principal) & set(group["eligible_roles"]):
                eligible.add(pid)
        if len(eligible) < group["threshold"]:
            return _freeze(policy, request, rule_id, ["QUORUM_UNSATISFIABLE_FOR_REQUESTER", f"GROUP:{gid}"])

    seen: dict[str, tuple[str, str | None, str, int, int]] = {}
    counted: dict[str, set[str]] = {gid: set() for gid in group_map}
    ignored: list[tuple[str, str]] = []
    deny_seen = False
    veto_seen = False
    distinct_counted: set[str] = set()

    for index, approval in enumerate(approvals):
        if not isinstance(approval, Mapping):
            return _freeze(policy, request, rule_id, ["APPROVAL_NOT_OBJECT", f"INDEX:{index}"])
        required = ("principal_id", "decision", "group_id", "request_sha256", "policy_version", "valid_from_tick", "valid_until_tick")
        if any(k not in approval for k in required):
            return _freeze(policy, request, rule_id, ["APPROVAL_MALFORMED", f"INDEX:{index}"])
        pid = approval.get("principal_id")
        decision = approval.get("decision")
        group_id = approval.get("group_id")
        if not _valid_id(pid) or decision not in APPROVAL_DECISIONS or (group_id is not None and not _valid_id(group_id)):
            return _freeze(policy, request, rule_id, ["APPROVAL_MALFORMED", f"INDEX:{index}"])
        principal = principals.get(pid)
        if principal is None:
            return _freeze(policy, request, rule_id, ["UNKNOWN_APPROVER", f"PRINCIPAL:{pid}"])
        if approval.get("request_sha256") != req_hash:
            return _freeze(policy, request, rule_id, ["APPROVAL_REQUEST_HASH_MISMATCH", f"PRINCIPAL:{pid}"])
        if approval.get("policy_version") != policy["version"]:
            return _freeze(policy, request, rule_id, ["APPROVAL_POLICY_VERSION_MISMATCH", f"PRINCIPAL:{pid}"])
        vf = approval.get("valid_from_tick")
        vu = approval.get("valid_until_tick")
        if not isinstance(vf, int) or not isinstance(vu, int) or vf < 0 or vu < vf:
            return _freeze(policy, request, rule_id, ["APPROVAL_VALIDITY_INVALID", f"PRINCIPAL:{pid}"])

        signature = (decision, group_id, approval["request_sha256"], vf, vu)
        if pid in seen:
            if seen[pid] != signature:
                return _freeze(policy, request, rule_id, ["CONTRADICTORY_APPROVALS", f"PRINCIPAL:{pid}"])
            ignored.append((pid, "DUPLICATE_IDENTICAL_APPROVAL"))
            continue
        seen[pid] = signature

        if not principal.get("active"):
            ignored.append((pid, "APPROVER_INACTIVE"))
            continue
        if not _domain_allowed(principal, request["domain"]):
            return _freeze(policy, request, rule_id, ["APPROVER_DOMAIN_VIOLATION", f"PRINCIPAL:{pid}"])
        if evaluation_tick < vf:
            ignored.append((pid, "APPROVAL_NOT_YET_VALID"))
            continue
        if evaluation_tick > vu:
            ignored.append((pid, "APPROVAL_EXPIRED"))
            continue
        if not rule["requester_may_approve"] and pid == request["requester_id"]:
            ignored.append((pid, "REQUESTER_SELF_APPROVAL_FORBIDDEN"))
            continue

        roles = _roles(principal)
        if decision == "DENY":
            eligible_any_group = any(roles & set(g["eligible_roles"]) for g in group_map.values())
            has_veto = bool(roles & set(rule["veto_roles"]))
            if rule["deny_mode"] == "ANY_ELIGIBLE_DENY" and (eligible_any_group or has_veto):
                deny_seen = True
            elif rule["deny_mode"] == "VETO_ROLES_ONLY" and has_veto:
                veto_seen = True
            else:
                ignored.append((pid, "DENY_WITHOUT_POLICY_VETO_POWER"))
            continue

        if group_id not in group_map:
            return _freeze(policy, request, rule_id, ["UNKNOWN_APPROVAL_GROUP", f"PRINCIPAL:{pid}"])
        group = group_map[group_id]
        if not (roles & set(group["eligible_roles"])):
            return _freeze(policy, request, rule_id, ["APPROVER_ROLE_NOT_ELIGIBLE", f"PRINCIPAL:{pid}", f"GROUP:{group_id}"])
        counted[group_id].add(pid)
        distinct_counted.add(pid)

    if deny_seen:
        return Decision(
            "DENY", req_hash, policy_sha256(policy), rule_id,
            ("AUTHORIZED_DENY",),
            tuple((gid, tuple(sorted(ids))) for gid, ids in sorted(counted.items())),
            tuple(sorted(ignored)),
        )
    if veto_seen:
        return Decision(
            "DENY", req_hash, policy_sha256(policy), rule_id,
            ("AUTHORIZED_VETO",),
            tuple((gid, tuple(sorted(ids))) for gid, ids in sorted(counted.items())),
            tuple(sorted(ignored)),
        )

    missing: list[str] = []
    for gid, group in sorted(group_map.items()):
        if len(counted[gid]) < group["threshold"]:
            missing.append(f"GROUP_QUORUM_MISSING:{gid}:{len(counted[gid])}/{group['threshold']}")
    if len(distinct_counted) < rule["min_distinct_approvers"]:
        missing.append(f"DISTINCT_APPROVERS_MISSING:{len(distinct_counted)}/{rule['min_distinct_approvers']}")

    state = "PENDING" if missing else "ALLOW"
    reasons = tuple(sorted(missing)) if missing else ("ALL_AUTHORITY_GATES_SATISFIED",)
    return Decision(
        state=state,
        request_sha256=req_hash,
        policy_sha256=policy_sha256(policy),
        rule_id=rule_id,
        reason_codes=reasons,
        counted_approvals=tuple((gid, tuple(sorted(ids))) for gid, ids in sorted(counted.items())),
        ignored_approvals=tuple(sorted(ignored)),
    )


def approval_for(
    policy: Mapping[str, Any],
    request: Mapping[str, Any],
    principal_id: str,
    decision: str,
    group_id: str | None,
    *,
    valid_from_tick: int = 0,
    valid_until_tick: int = 10_000,
) -> dict[str, Any]:
    return {
        "principal_id": principal_id,
        "decision": decision,
        "group_id": group_id,
        "request_sha256": request_sha256(request),
        "policy_version": policy["version"],
        "valid_from_tick": valid_from_tick,
        "valid_until_tick": valid_until_tick,
    }


def _load(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _dump(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))


def cmd_validate(args: argparse.Namespace) -> int:
    report = validate_policy(_load(args.policy))
    _dump(report.to_dict())
    return 0 if report.ok else 2


def cmd_evaluate(args: argparse.Namespace) -> int:
    policy = _load(args.policy)
    request = _load(args.request)
    approvals = _load(args.approvals)
    if not isinstance(approvals, list):
        print("approvals file must contain a JSON array", file=sys.stderr)
        return 2
    decision = evaluate(policy, request, approvals, evaluation_tick=args.tick)
    _dump(decision.to_dict())
    return 0 if decision.state == "ALLOW" else 3


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Experimental NEXY Multi-Principal Authority Lattice reference engine")
    sub = p.add_subparsers(dest="command", required=True)
    v = sub.add_parser("validate-policy")
    v.add_argument("policy")
    v.set_defaults(func=cmd_validate)
    e = sub.add_parser("evaluate")
    e.add_argument("policy")
    e.add_argument("request")
    e.add_argument("approvals")
    e.add_argument("--tick", type=int, required=True)
    e.set_defaults(func=cmd_evaluate)
    return p


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
