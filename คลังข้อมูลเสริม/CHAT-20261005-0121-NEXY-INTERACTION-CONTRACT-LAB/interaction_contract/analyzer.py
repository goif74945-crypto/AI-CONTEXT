from __future__ import annotations

from collections import defaultdict
from typing import Any

from .canonical import canonical_sha256
from .model import Contract, Directive, Event, parse_contract


_CRITICALITY_WEIGHT = {"critical": 20, "high": 12, "normal": 6, "low": 3}


def _finding(code: str, severity: str, message: str, **details: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "code": code,
        "severity": severity,
        "message": message,
    }
    if details:
        payload["details"] = details
    return payload


def _directive_outcomes(contract: Contract) -> dict[str, list[Event]]:
    by_directive: dict[str, list[Event]] = defaultdict(list)
    for event in contract.events:
        if event.type != "evidence":
            continue
        for directive_id in event.directive_ids:
            by_directive[directive_id].append(event)
    return by_directive


def _effective_outcome(events: list[Event]) -> str | None:
    if not events:
        return None
    return events[-1].outcome


def _detect_conflicts(contract: Contract) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    directives = {d.id: d for d in contract.directives}
    for directive in contract.directives:
        for target_id in directive.conflicts_with:
            pair = tuple(sorted((directive.id, target_id)))
            if pair in seen:
                continue
            seen.add(pair)
            target = directives[target_id]
            if directive.resolved and target.resolved:
                findings.append(
                    _finding(
                        "EXPLICIT_DIRECTIVE_CONFLICT",
                        "critical",
                        f"Active directives {pair[0]} and {pair[1]} explicitly conflict.",
                        directive_ids=list(pair),
                    )
                )
    return findings


def _detect_scope_violations(contract: Contract) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    authorized = set(contract.authorized_scopes)
    protected = set(contract.protected_scopes)
    for event in contract.events:
        if event.type != "action":
            continue
        for scope in event.scopes:
            if scope in protected:
                findings.append(
                    _finding(
                        "PROTECTED_SCOPE_TOUCHED",
                        "critical",
                        f"Action event {event.seq} touches protected scope {scope}.",
                        seq=event.seq,
                        scope=scope,
                    )
                )
            elif scope not in authorized:
                findings.append(
                    _finding(
                        "UNAUTHORIZED_SCOPE_EXPANSION",
                        "critical",
                        f"Action event {event.seq} uses scope {scope} without authorization.",
                        seq=event.seq,
                        scope=scope,
                    )
                )
    return findings


def _detect_clarification_debt(contract: Contract) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    directive_map = {d.id: d for d in contract.directives}
    for event in contract.events:
        if event.type != "clarification":
            continue
        for directive_id in event.directive_ids:
            directive = directive_map[directive_id]
            if directive.resolved:
                findings.append(
                    _finding(
                        "REDUNDANT_CLARIFICATION",
                        "normal",
                        f"Clarification event {event.seq} re-asks resolved directive {directive_id}.",
                        seq=event.seq,
                        directive_id=directive_id,
                    )
                )
    return findings


def _detect_assumption_pressure(contract: Contract) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for event in contract.events:
        if event.type != "action" or not event.assumptions:
            continue
        findings.append(
            _finding(
                "ACTION_WITH_ASSUMPTION",
                "high",
                f"Action event {event.seq} depends on explicit assumptions and requires review.",
                seq=event.seq,
                assumptions=list(event.assumptions),
            )
        )
    return findings


def _detect_directive_coverage(contract: Contract) -> tuple[list[dict[str, Any]], dict[str, str | None]]:
    findings: list[dict[str, Any]] = []
    outcomes = _directive_outcomes(contract)
    effective: dict[str, str | None] = {}
    for directive in contract.directives:
        outcome = _effective_outcome(outcomes.get(directive.id, []))
        effective[directive.id] = outcome
        if outcome is None:
            findings.append(
                _finding(
                    "DIRECTIVE_UNEVIDENCED",
                    directive.criticality,
                    f"Directive {directive.id} has no evidence event.",
                    directive_id=directive.id,
                    criticality=directive.criticality,
                )
            )
        elif outcome in {"fail", "unknown", "not_verified"}:
            findings.append(
                _finding(
                    "DIRECTIVE_NOT_SATISFIED",
                    directive.criticality,
                    f"Directive {directive.id} effective outcome is {outcome}.",
                    directive_id=directive.id,
                    outcome=outcome,
                )
            )
        elif outcome == "pass":
            latest = outcomes[directive.id][-1]
            if not latest.evidence_ref:
                findings.append(
                    _finding(
                        "PASS_WITHOUT_EVIDENCE_REF",
                        "high",
                        f"Directive {directive.id} is marked pass without evidence_ref.",
                        directive_id=directive.id,
                        seq=latest.seq,
                    )
                )
    return findings, effective


def _detect_premature_completion(
    contract: Contract,
    effective_outcomes: dict[str, str | None],
) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    complete_events = [
        event for event in contract.events if event.type == "completion" and event.completion_status == "complete"
    ]
    if not complete_events:
        return findings

    blocking_directives = [
        directive.id
        for directive in contract.directives
        if directive.kind != "preference" and effective_outcomes.get(directive.id) != "pass"
    ]
    if blocking_directives:
        for event in complete_events:
            findings.append(
                _finding(
                    "PREMATURE_COMPLETION_CLAIM",
                    "critical",
                    f"Completion event {event.seq} claims complete while mandatory directives lack PASS.",
                    seq=event.seq,
                    blocking_directive_ids=blocking_directives,
                )
            )
    return findings


def _score(contract: Contract, findings: list[dict[str, Any]]) -> dict[str, Any]:
    penalty = 0
    per_code: dict[str, int] = defaultdict(int)
    directive_map = {d.id: d for d in contract.directives}

    for finding in findings:
        code = finding["code"]
        per_code[code] += 1
        if code in {"PROTECTED_SCOPE_TOUCHED", "UNAUTHORIZED_SCOPE_EXPANSION"}:
            penalty += 25
        elif code in {"PREMATURE_COMPLETION_CLAIM", "EXPLICIT_DIRECTIVE_CONFLICT"}:
            penalty += 30
        elif code == "PASS_WITHOUT_EVIDENCE_REF":
            penalty += 12
        elif code == "ACTION_WITH_ASSUMPTION":
            penalty += 10
        elif code == "REDUNDANT_CLARIFICATION":
            penalty += 4
        elif code in {"DIRECTIVE_UNEVIDENCED", "DIRECTIVE_NOT_SATISFIED"}:
            did = finding.get("details", {}).get("directive_id")
            criticality = directive_map[did].criticality if did in directive_map else "normal"
            penalty += _CRITICALITY_WEIGHT[criticality]
        else:
            penalty += 5

    loss_score = min(100, penalty)
    return {
        "interaction_loss_score": loss_score,
        "retention_score": max(0, 100 - loss_score),
        "penalty_total_before_cap": penalty,
        "finding_counts": dict(sorted(per_code.items())),
    }


def analyze_contract(raw: dict[str, Any]) -> dict[str, Any]:
    """Analyze a structured interaction contract deterministically.

    This function deliberately does not infer semantics from natural language. All conflict,
    scope, and directive relationships must be explicitly encoded in the input contract.
    """
    contract = parse_contract(raw)

    findings: list[dict[str, Any]] = []
    findings.extend(_detect_conflicts(contract))
    findings.extend(_detect_scope_violations(contract))
    findings.extend(_detect_clarification_debt(contract))
    findings.extend(_detect_assumption_pressure(contract))
    coverage_findings, effective_outcomes = _detect_directive_coverage(contract)
    findings.extend(coverage_findings)
    findings.extend(_detect_premature_completion(contract, effective_outcomes))

    severity_order = {"critical": 0, "high": 1, "normal": 2, "low": 3}
    findings.sort(
        key=lambda item: (
            severity_order.get(item["severity"], 99),
            item["code"],
            str(item.get("details", {})),
        )
    )

    score = _score(contract, findings)
    mandatory = [d.id for d in contract.directives if d.kind != "preference"]
    passed = [did for did in mandatory if effective_outcomes.get(did) == "pass"]

    completion_gate = "PASS" if len(passed) == len(mandatory) and not any(
        f["severity"] == "critical" for f in findings
    ) else "BLOCK"

    return {
        "schema_version": "interaction-contract-report/v0.1",
        "contract_id": contract.contract_id,
        "input_fingerprint_sha256": canonical_sha256(raw),
        "deterministic": True,
        "semantic_inference_used": False,
        "metrics": {
            **score,
            "mandatory_directives": len(mandatory),
            "mandatory_passed": len(passed),
            "mandatory_pass_ratio": (len(passed) / len(mandatory)) if mandatory else 1.0,
        },
        "effective_outcomes": dict(sorted(effective_outcomes.items())),
        "findings": findings,
        "completion_gate": completion_gate,
    }
