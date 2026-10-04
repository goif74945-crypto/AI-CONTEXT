from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import re
import unicodedata
from typing import Any, Iterable, Mapping, Sequence

DECISIONS = ("PROCEED", "COEXIST", "DECONFLICT", "FREEZE")
STATUSES = ("DRAFT", "ACTIVE", "COMPLETED", "CANCELLED")
KINDS = ("FILE", "TREE")
TOKEN_RE = re.compile(r"\w+", re.UNICODE)
FORBIDDEN_PATH = set("*?[]{}")

DEFAULT_POLICY = {
    "schema_version": "1.0",
    "coexist_threshold_bps": 4000,
    "deconflict_threshold_bps": 7600,
    "max_lease_seconds": 86400,
    "domain_weight": 35,
    "capability_weight": 25,
    "deliverable_weight": 25,
    "objective_weight": 15,
}

REQUIRED = {
    "schema_version", "mission_id", "objective", "domains", "capabilities",
    "deliverables", "write_claims", "protected_claims", "exclusive_resources",
    "exclusive_authorities", "started_at", "lease_expires_at", "status",
}

class ValidationError(ValueError):
    pass

def parse_time(value: str) -> datetime:
    if not isinstance(value, str):
        raise ValidationError("TIMESTAMP_NOT_STRING")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValidationError("INVALID_TIMESTAMP") from exc
    if parsed.tzinfo is None:
        raise ValidationError("TIMESTAMP_REQUIRES_TIMEZONE")
    return parsed.astimezone(timezone.utc)

def norm_atom(value: str, field: str) -> str:
    if not isinstance(value, str):
        raise ValidationError(field + ":NOT_STRING")
    out = unicodedata.normalize("NFKC", value).strip().casefold()
    if not out:
        raise ValidationError(field + ":EMPTY")
    return out

def norm_set(values: Sequence[str], field: str, required: bool = True) -> list[str]:
    if not isinstance(values, (list, tuple)):
        raise ValidationError(field + ":NOT_ARRAY")
    out = sorted({norm_atom(x, field) for x in values})
    if required and not out:
        raise ValidationError(field + ":EMPTY_SET")
    return out

def norm_path(path: str) -> str:
    if not isinstance(path, str):
        raise ValidationError("PATH_NOT_STRING")
    out = unicodedata.normalize("NFKC", path).strip().replace("\\", "/")
    while "//" in out:
        out = out.replace("//", "/")
    out = out.strip("/")
    if not out:
        raise ValidationError("PATH_EMPTY")
    if any(part in ("", ".", "..") for part in out.split("/")):
        raise ValidationError("PATH_AMBIGUOUS_SEGMENT")
    if any(ch in out for ch in FORBIDDEN_PATH):
        raise ValidationError("PATH_GLOB_FORBIDDEN")
    return out

def canon_claim(raw: Mapping[str, Any]) -> dict[str, str]:
    if not isinstance(raw, Mapping) or set(raw) != {"path", "kind"}:
        raise ValidationError("MALFORMED_PATH_CLAIM")
    if raw["kind"] not in KINDS:
        raise ValidationError("UNKNOWN_PATH_CLAIM_KIND")
    return {"path": norm_path(raw["path"]), "kind": raw["kind"]}

def claims_intersect(left: Mapping[str, str], right: Mapping[str, str]) -> bool:
    a, b = canon_claim(left), canon_claim(right)
    if a["kind"] == b["kind"] == "FILE":
        return a["path"] == b["path"]
    if a["kind"] == b["kind"] == "TREE":
        return (
            a["path"] == b["path"]
            or a["path"].startswith(b["path"] + "/")
            or b["path"].startswith(a["path"] + "/")
        )
    tree, file = (a, b) if a["kind"] == "TREE" else (b, a)
    return file["path"] == tree["path"] or file["path"].startswith(tree["path"] + "/")

def objective_tokens(text: str) -> list[str]:
    if not isinstance(text, str) or not text.strip():
        raise ValidationError("objective:EMPTY")
    tokens = sorted(set(TOKEN_RE.findall(unicodedata.normalize("NFKC", text).casefold())))
    if not tokens:
        raise ValidationError("OBJECTIVE_HAS_NO_TOKENS")
    return tokens

def canonical_mission(raw: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(raw, Mapping):
        raise ValidationError("MISSION_NOT_OBJECT")
    missing = sorted(REQUIRED - set(raw))
    unknown = sorted(set(raw) - REQUIRED)
    if missing:
        raise ValidationError("MISSING_FIELDS:" + ",".join(missing))
    if unknown:
        raise ValidationError("UNKNOWN_FIELDS:" + ",".join(unknown))
    if raw["status"] not in STATUSES:
        raise ValidationError("UNKNOWN_MISSION_STATUS")
    writes = sorted((canon_claim(x) for x in raw["write_claims"]), key=lambda x: (x["path"], x["kind"]))
    protected = sorted((canon_claim(x) for x in raw["protected_claims"]), key=lambda x: (x["path"], x["kind"]))
    if not writes:
        raise ValidationError("write_claims:EMPTY")
    start, end = parse_time(raw["started_at"]), parse_time(raw["lease_expires_at"])
    if end <= start:
        raise ValidationError("LEASE_NOT_AFTER_START")
    objective = unicodedata.normalize("NFKC", raw["objective"]).strip()
    return {
        "schema_version": norm_atom(raw["schema_version"], "schema_version"),
        "mission_id": norm_atom(raw["mission_id"], "mission_id"),
        "objective": objective,
        "objective_tokens": objective_tokens(objective),
        "domains": norm_set(raw["domains"], "domains"),
        "capabilities": norm_set(raw["capabilities"], "capabilities"),
        "deliverables": norm_set(raw["deliverables"], "deliverables"),
        "write_claims": writes,
        "protected_claims": protected,
        "exclusive_resources": norm_set(raw["exclusive_resources"], "exclusive_resources", False),
        "exclusive_authorities": norm_set(raw["exclusive_authorities"], "exclusive_authorities", False),
        "started_at": start.isoformat().replace("+00:00", "Z"),
        "lease_expires_at": end.isoformat().replace("+00:00", "Z"),
        "status": raw["status"],
    }

def validate_policy(policy: Mapping[str, Any]) -> dict[str, Any]:
    if set(policy) != set(DEFAULT_POLICY):
        raise ValidationError("INVALID_POLICY_FIELDS")
    p = dict(policy)
    if not (0 <= p["coexist_threshold_bps"] < p["deconflict_threshold_bps"] <= 10000):
        raise ValidationError("INVALID_OVERLAP_THRESHOLDS")
    if p["max_lease_seconds"] <= 0:
        raise ValidationError("INVALID_MAX_LEASE_SECONDS")
    weights = [p["domain_weight"], p["capability_weight"], p["deliverable_weight"], p["objective_weight"]]
    if any((not isinstance(x, int) or x < 0) for x in weights) or sum(weights) != 100:
        raise ValidationError("INVALID_WEIGHT_VECTOR")
    return p

def jaccard_bps(left: Iterable[str], right: Iterable[str]) -> int:
    a, b = set(left), set(right)
    union = a | b
    return 0 if not union else len(a & b) * 10000 // len(union)

def active_at(mission: Mapping[str, Any], now: datetime) -> bool:
    return mission["status"] == "ACTIVE" and parse_time(mission["started_at"]) <= now < parse_time(mission["lease_expires_at"])

def validate_lease(mission: Mapping[str, Any], policy: Mapping[str, Any]) -> None:
    seconds = (parse_time(mission["lease_expires_at"]) - parse_time(mission["started_at"])).total_seconds()
    if seconds > policy["max_lease_seconds"]:
        raise ValidationError("LEASE_EXCEEDS_POLICY_MAX")

def hard_reasons(candidate: Mapping[str, Any], incumbent: Mapping[str, Any]) -> list[str]:
    reasons: set[str] = set()
    if candidate["mission_id"] == incumbent["mission_id"] and candidate != incumbent:
        reasons.add("MISSION_ID_COLLISION")
    if any(claims_intersect(a, b) for a in candidate["write_claims"] for b in incumbent["write_claims"]):
        reasons.add("WRITE_SCOPE_COLLISION")
    if any(claims_intersect(a, b) for a in candidate["write_claims"] for b in incumbent["protected_claims"]):
        reasons.add("CANDIDATE_WRITE_HITS_INCUMBENT_PROTECTED_SCOPE")
    if any(claims_intersect(a, b) for a in incumbent["write_claims"] for b in candidate["protected_claims"]):
        reasons.add("INCUMBENT_WRITE_HITS_CANDIDATE_PROTECTED_SCOPE")
    if set(candidate["exclusive_resources"]) & set(incumbent["exclusive_resources"]):
        reasons.add("EXCLUSIVE_RESOURCE_COLLISION")
    if set(candidate["exclusive_authorities"]) & set(incumbent["exclusive_authorities"]):
        reasons.add("EXCLUSIVE_AUTHORITY_COLLISION")
    return sorted(reasons)

def overlap_bps(candidate: Mapping[str, Any], incumbent: Mapping[str, Any], policy: Mapping[str, Any]) -> int:
    weighted = (
        policy["domain_weight"] * jaccard_bps(candidate["domains"], incumbent["domains"])
        + policy["capability_weight"] * jaccard_bps(candidate["capabilities"], incumbent["capabilities"])
        + policy["deliverable_weight"] * jaccard_bps(candidate["deliverables"], incumbent["deliverables"])
        + policy["objective_weight"] * jaccard_bps(candidate["objective_tokens"], incumbent["objective_tokens"])
    )
    return weighted // 100

def compare(candidate: Mapping[str, Any], incumbent: Mapping[str, Any], now: datetime, policy: Mapping[str, Any]) -> dict[str, Any]:
    if not active_at(incumbent, now):
        return {"incumbent_id": incumbent["mission_id"], "decision": "PROCEED", "overlap_bps": 0, "reason_codes": ["INCUMBENT_INACTIVE_OR_LEASE_EXPIRED"], "active": False}
    hard = hard_reasons(candidate, incumbent)
    score = overlap_bps(candidate, incumbent, policy)
    if hard:
        decision, reasons = "FREEZE", hard
    elif score >= policy["deconflict_threshold_bps"] and jaccard_bps(candidate["deliverables"], incumbent["deliverables"]) > 0:
        decision, reasons = "DECONFLICT", ["HIGH_DECLARED_MISSION_OVERLAP"]
    elif score >= policy["coexist_threshold_bps"]:
        decision, reasons = "COEXIST", ["MODERATE_DECLARED_MISSION_OVERLAP"]
    else:
        decision, reasons = "PROCEED", ["LOW_DECLARED_MISSION_OVERLAP"]
    return {"incumbent_id": incumbent["mission_id"], "decision": decision, "overlap_bps": score, "reason_codes": reasons, "active": True}

def evaluate(candidate_raw: Mapping[str, Any], incumbents_raw: Sequence[Mapping[str, Any]], *, now: str, policy: Mapping[str, Any] | None = None) -> dict[str, Any]:
    p = validate_policy(DEFAULT_POLICY if policy is None else policy)
    now_dt = parse_time(now)
    candidate = canonical_mission(candidate_raw)
    validate_lease(candidate, p)
    if candidate["status"] not in ("DRAFT", "ACTIVE"):
        raise ValidationError("CANDIDATE_STATUS_NOT_ADMISSIBLE")
    if parse_time(candidate["started_at"]) > now_dt:
        raise ValidationError("CANDIDATE_STARTS_IN_FUTURE")
    if parse_time(candidate["lease_expires_at"]) <= now_dt:
        raise ValidationError("CANDIDATE_LEASE_ALREADY_EXPIRED")

    incumbents = [canonical_mission(x) for x in incumbents_raw]
    incumbent_ids = [x["mission_id"] for x in incumbents]
    if len(incumbent_ids) != len(set(incumbent_ids)):
        raise ValidationError("DUPLICATE_REGISTRY_MISSION_ID")
    for incumbent in incumbents:
        validate_lease(incumbent, p)
    incumbents.sort(key=lambda x: x["mission_id"])
    comparisons = [compare(candidate, incumbent, now_dt, p) for incumbent in incumbents]

    rank = {"PROCEED": 0, "COEXIST": 1, "DECONFLICT": 2, "FREEZE": 3}
    decision = max((x["decision"] for x in comparisons), key=rank.get, default="PROCEED")
    reasons = sorted({r for x in comparisons if x["decision"] == decision for r in x["reason_codes"]})
    if not comparisons:
        reasons = ["NO_ACTIVE_REGISTRY_CONFLICTS"]

    payload = {
        "candidate": candidate,
        "incumbents": incumbents,
        "now": now_dt.isoformat().replace("+00:00", "Z"),
        "policy": p,
        "decision": decision,
        "reason_codes": reasons,
        "comparisons": comparisons,
    }
    packed = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return {"decision": decision, "reason_codes": reasons, "comparisons": comparisons, "decision_hash": hashlib.sha256(packed).hexdigest()}
