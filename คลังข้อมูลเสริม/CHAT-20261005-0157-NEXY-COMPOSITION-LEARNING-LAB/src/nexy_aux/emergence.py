from __future__ import annotations

from typing import Any

from .canonical import sha256

_ALLOWED_TAINTS = {"SECRET", "PRIVATE", "UNTRUSTED", "LOW_TRUST_AUTHORITY", "VERIFIED"}
_ALLOWED_CAPABILITIES = {
    "EXTERNAL_EGRESS",
    "PUBLIC_WRITE",
    "EXECUTE_CODE",
    "MUTATE_PROTECTED",
    "REDACT_SECRET",
    "REDACT_PRIVATE",
    "VALIDATE_UNTRUSTED",
    "VALIDATE_AUTHORITY",
}


def _finish(result: dict[str, Any]) -> dict[str, Any]:
    result["fingerprint"] = sha256(result)
    return result


def _string_list(value: Any, field: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or any(not isinstance(x, str) or not x for x in value):
        raise ValueError(f"{field} must be a list of non-empty strings")
    if len(value) != len(set(value)):
        raise ValueError(f"{field} must not contain duplicates")
    return value


def analyze_plan(plan: dict[str, Any]) -> dict[str, Any]:
    """Propagate taints through a multi-step tool plan and detect emergent hazards.

    Capability labels are declarative inputs. A production caller must bind them to
    independently verified tool contracts; this analyzer does not prove that a tool
    actually performs the validation/redaction its contract claims.
    """
    if not isinstance(plan, dict):
        raise ValueError("plan must be an object")
    initial = plan.get("artifacts", {})
    steps = plan.get("steps", [])
    if not isinstance(initial, dict):
        raise ValueError("artifacts must be an object")
    if not isinstance(steps, list):
        raise ValueError("steps must be a list")

    artifacts: dict[str, set[str]] = {}
    for name, taints_raw in sorted(initial.items(), key=lambda item: str(item[0])):
        if not isinstance(name, str) or not name:
            raise ValueError("artifact names must be non-empty strings")
        taints = set(_string_list(taints_raw, f"artifacts.{name}"))
        unknown = taints - _ALLOWED_TAINTS
        if unknown:
            raise ValueError(f"unknown taints for {name}: {sorted(unknown)}")
        artifacts[name] = taints

    seen_steps: set[str] = set()
    findings: list[dict[str, Any]] = []
    trace: list[dict[str, Any]] = []

    for index, raw in enumerate(steps):
        if not isinstance(raw, dict):
            raise ValueError("each step must be an object")
        sid = raw.get("id")
        if not isinstance(sid, str) or not sid:
            raise ValueError("step.id must be a non-empty string")
        if sid in seen_steps:
            raise ValueError(f"duplicate step id: {sid}")
        seen_steps.add(sid)

        consumes = _string_list(raw.get("consumes", []), f"{sid}.consumes")
        produces = _string_list(raw.get("produces", []), f"{sid}.produces")
        capabilities = set(_string_list(raw.get("capabilities", []), f"{sid}.capabilities"))
        unknown_caps = capabilities - _ALLOWED_CAPABILITIES
        if unknown_caps:
            raise ValueError(f"unknown capabilities for {sid}: {sorted(unknown_caps)}")

        missing = sorted(name for name in consumes if name not in artifacts)
        if missing:
            return _finish({
                "status": "FREEZE",
                "reason": "MISSING_ARTIFACT",
                "step_id": sid,
                "missing_artifacts": missing,
                "findings": findings,
                "trace": trace,
            })

        duplicate_outputs = sorted(name for name in produces if name in artifacts)
        if duplicate_outputs:
            return _finish({
                "status": "FREEZE",
                "reason": "ARTIFACT_OVERWRITE_FORBIDDEN",
                "step_id": sid,
                "artifacts": duplicate_outputs,
                "findings": findings,
                "trace": trace,
            })

        taints: set[str] = set()
        for name in consumes:
            taints.update(artifacts[name])

        before = sorted(taints)
        if "REDACT_SECRET" in capabilities:
            taints.discard("SECRET")
        if "REDACT_PRIVATE" in capabilities:
            taints.discard("PRIVATE")
        if "VALIDATE_UNTRUSTED" in capabilities:
            taints.discard("UNTRUSTED")
            taints.add("VERIFIED")
        if "VALIDATE_AUTHORITY" in capabilities:
            taints.discard("LOW_TRUST_AUTHORITY")
            taints.add("VERIFIED")

        step_findings: list[dict[str, str]] = []

        def add(code: str, detail: str) -> None:
            item = {"code": code, "step_id": sid, "detail": detail}
            findings.append(item)
            step_findings.append(item)

        if "EXTERNAL_EGRESS" in capabilities and "SECRET" in taints:
            add("E_SECRET_EGRESS", "secret-tainted data reaches external egress")
        if "PUBLIC_WRITE" in capabilities and ({"PRIVATE", "SECRET"} & taints):
            add("E_PRIVATE_PUBLICATION", "private/secret-tainted data reaches a public write")
        if "EXECUTE_CODE" in capabilities and "UNTRUSTED" in taints:
            add("E_UNTRUSTED_EXECUTION", "untrusted data reaches code execution without validation")
        if "MUTATE_PROTECTED" in capabilities and "UNTRUSTED" in taints:
            add("E_UNTRUSTED_PROTECTED_MUTATION", "untrusted data reaches a protected mutation")
        if "MUTATE_PROTECTED" in capabilities and "LOW_TRUST_AUTHORITY" in taints:
            add("E_CONFUSED_DEPUTY", "low-trust authority influences a protected mutation without authority validation")

        for name in produces:
            artifacts[name] = set(taints)

        trace.append({
            "index": index,
            "step_id": sid,
            "input_taints": before,
            "output_taints": sorted(taints),
            "capabilities": sorted(capabilities),
            "findings": sorted(step_findings, key=lambda x: (x["code"], x["step_id"])),
        })

    findings = sorted(findings, key=lambda x: (x["step_id"], x["code"], x["detail"]))
    return _finish({
        "status": "FREEZE" if findings else "PASS",
        "reason": "EMERGENT_RISK" if findings else "NO_POLICY_VIOLATION_OBSERVED",
        "findings": findings,
        "trace": trace,
        "artifacts": {k: sorted(v) for k, v in sorted(artifacts.items())},
    })
