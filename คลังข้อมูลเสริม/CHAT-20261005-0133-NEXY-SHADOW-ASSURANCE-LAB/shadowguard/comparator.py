from __future__ import annotations

from .models import DecisionRecord, Finding, Outcome, Severity


def compare_pair(stable: DecisionRecord, candidate: DecisionRecord) -> tuple[Finding, ...]:
    """Compare one stable/candidate decision pair.

    The comparator is deliberately conservative. It never executes either action.
    Any policy/input mismatch is treated as a non-comparable proof context rather
    than being hand-waved into a successful comparison.
    """
    if stable.case_id != candidate.case_id:
        raise ValueError("case_id mismatch")

    findings: list[Finding] = []
    case_id = stable.case_id

    if stable.input_fingerprint != candidate.input_fingerprint:
        findings.append(_f("INPUT_MISMATCH", case_id, "stable and candidate inputs differ"))
        return tuple(findings)

    if stable.policy_fingerprint != candidate.policy_fingerprint:
        findings.append(_f("POLICY_DRIFT", case_id, "policy fingerprint changed; a new authorized baseline is required"))

    if not _preserves_authority(stable.authority_chain, candidate.authority_chain):
        findings.append(_f("AUTHORITY_REGRESSION", case_id, "candidate removed, reordered, or replaced stable authority precedence"))

    stale = candidate.stale_evidence()
    if stale:
        findings.append(_f("STALE_EVIDENCE", case_id, f"candidate has {len(stale)} evidence item(s) bound to another revision"))

    candidate_classes = candidate.evidence_classes()
    missing_required = sorted(set(candidate.required_evidence_classes) - candidate_classes)
    if missing_required:
        findings.append(_f("MISSING_REQUIRED_EVIDENCE", case_id, "candidate is missing required evidence classes: " + ",".join(missing_required)))

    # Evidence-class substitution is forbidden. When the stable baseline required
    # a class for the same case, candidate cannot silently omit it.
    missing_stable_profile = sorted(set(stable.required_evidence_classes) - set(candidate.required_evidence_classes))
    if missing_stable_profile:
        findings.append(_f("EVIDENCE_PROFILE_DOWNGRADE", case_id, "candidate removed baseline evidence obligations: " + ",".join(missing_stable_profile)))

    if stable.outcome in {Outcome.FREEZE, Outcome.STOP} and candidate.outcome is Outcome.RELEASE:
        findings.append(_f("FREEZE_BYPASS", case_id, "candidate releases an action where stable baseline blocked execution"))
    elif stable.outcome is Outcome.RELEASE and candidate.outcome in {Outcome.FREEZE, Outcome.STOP}:
        findings.append(
            Finding(
                code="CONSERVATIVE_DIVERGENCE",
                severity=Severity.WARNING,
                case_id=case_id,
                message="candidate blocks a case that stable released; safe-side divergence requires usability review",
            )
        )
    elif stable.outcome is Outcome.RELEASE and candidate.outcome is Outcome.RELEASE and stable.action != candidate.action:
        findings.append(_f("ACTION_DIVERGENCE", case_id, "candidate released a different action than stable baseline"))

    removed_labels = sorted(set(stable.safety_labels) - set(candidate.safety_labels))
    if removed_labels:
        findings.append(_f("SAFETY_LABEL_REGRESSION", case_id, "candidate removed baseline safety labels: " + ",".join(removed_labels)))

    if not findings:
        findings.append(
            Finding(
                code="MATCH",
                severity=Severity.INFO,
                case_id=case_id,
                message="candidate preserves input, policy, authority, evidence obligations, safety labels, and release behavior",
            )
        )
    return tuple(findings)


def _preserves_authority(stable: tuple[str, ...], candidate: tuple[str, ...]) -> bool:
    """Stable authority chain must remain an exact prefix of candidate chain."""
    return len(candidate) >= len(stable) and candidate[: len(stable)] == stable


def _f(code: str, case_id: str, message: str) -> Finding:
    return Finding(code=code, severity=Severity.BLOCKING, case_id=case_id, message=message)
