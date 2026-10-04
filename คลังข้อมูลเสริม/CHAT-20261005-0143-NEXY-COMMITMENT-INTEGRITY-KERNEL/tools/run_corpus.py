from __future__ import annotations

import json
import pathlib
from dataclasses import replace

from ncik.engine import evaluate_commitment
from ncik.model import (
    AuthorityState, BindingType, CapabilityManifest, Commitment, EffectClass,
    EvidenceClass, ExecutionBinding, TemporalMode,
)

ROOT = pathlib.Path(__file__).resolve().parents[1]


def base_commitment() -> Commitment:
    return Commitment(
        commitment_id="C-ADV",
        revision=1,
        issuer="NEXY",
        beneficiary="user",
        objective="Deliver verified artifact",
        deliverable="Verified artifact",
        scope=("project:alpha",),
        protected_scope=("project:omega",),
        temporal_mode=TemporalMode.IMMEDIATE,
        effect=EffectClass.READ_ONLY,
        authority_state=AuthorityState.RESOLVED,
        authority_refs=("user:directive:1",),
        required_evidence=(EvidenceClass.E2_UNIT,),
        binding=ExecutionBinding(BindingType.INLINE_SESSION, "session:adv", False, "proof:inline"),
        metadata={"fixture":"adversarial"},
    )


def base_caps() -> CapabilityManifest:
    return CapabilityManifest(frozenset(BindingType), frozenset(EffectClass), frozenset(EvidenceClass))


def scenario(name: str):
    c, cp = base_commitment(), base_caps()
    if name == "valid_immediate": pass
    elif name == "authority_conflict": c = replace(c, authority_state=AuthorityState.CONFLICT)
    elif name == "authority_unresolved": c = replace(c, authority_state=AuthorityState.UNRESOLVED)
    elif name == "empty_id": c = replace(c, commitment_id=" ")
    elif name == "invalid_revision": c = replace(c, revision=0)
    elif name == "missing_issuer": c = replace(c, issuer="")
    elif name == "missing_beneficiary": c = replace(c, beneficiary="")
    elif name == "missing_objective": c = replace(c, objective="")
    elif name == "missing_deliverable": c = replace(c, deliverable="")
    elif name == "empty_scope": c = replace(c, scope=())
    elif name == "protected_collision": c = replace(c, scope=("project:omega",))
    elif name == "protected_collision_casefold": c = replace(c, scope=("PROJECT:OMEGA",))
    elif name == "missing_authority_refs": c = replace(c, authority_refs=())
    elif name == "missing_binding_ref": c = replace(c, binding=replace(c.binding, binding_ref=""))
    elif name == "missing_capability_proof": c = replace(c, binding=replace(c.binding, capability_proof_ref=""))
    elif name == "scheduled_wrong_binding": c = replace(c, temporal_mode=TemporalMode.SCHEDULED, deadline_spec="2026-10-06T09:00+07:00")
    elif name == "scheduled_not_durable": c = replace(c, temporal_mode=TemporalMode.SCHEDULED, deadline_spec="2026-10-06T09:00+07:00", binding=ExecutionBinding(BindingType.SCHEDULED_TASK,"task:1",False,"proof:scheduler"))
    elif name == "scheduled_missing_spec": c = replace(c, temporal_mode=TemporalMode.SCHEDULED, binding=ExecutionBinding(BindingType.SCHEDULED_TASK,"task:1",True,"proof:scheduler"))
    elif name == "scheduled_valid": c = replace(c, temporal_mode=TemporalMode.SCHEDULED, deadline_spec="2026-10-06T09:00+07:00", binding=ExecutionBinding(BindingType.SCHEDULED_TASK,"task:1",True,"proof:scheduler"))
    elif name == "conditional_wrong_binding": c = replace(c, temporal_mode=TemporalMode.CONDITIONAL, trigger_spec="on:reply")
    elif name == "conditional_missing_trigger": c = replace(c, temporal_mode=TemporalMode.CONDITIONAL, binding=ExecutionBinding(BindingType.CONDITION_WATCH,"watch:1",True,"proof:watch"))
    elif name == "conditional_valid": c = replace(c, temporal_mode=TemporalMode.CONDITIONAL, trigger_spec="on:reply", binding=ExecutionBinding(BindingType.CONDITION_WATCH,"watch:1",True,"proof:watch"))
    elif name == "recurring_not_durable": c = replace(c, temporal_mode=TemporalMode.RECURRING, trigger_spec="daily@08:00", binding=ExecutionBinding(BindingType.RECURRING_TASK,"rec:1",False,"proof:rec"))
    elif name == "recurring_missing_trigger": c = replace(c, temporal_mode=TemporalMode.RECURRING, binding=ExecutionBinding(BindingType.RECURRING_TASK,"rec:1",True,"proof:rec"))
    elif name == "recurring_valid": c = replace(c, temporal_mode=TemporalMode.RECURRING, trigger_spec="daily@08:00", binding=ExecutionBinding(BindingType.RECURRING_TASK,"rec:1",True,"proof:rec"))
    elif name == "binding_capability_missing": cp = replace(cp, supported_bindings=frozenset())
    elif name == "effect_capability_missing": cp = replace(cp, supported_effects=frozenset())
    elif name == "evidence_capability_missing": cp = replace(cp, evidence_classes=frozenset({EvidenceClass.E0_PRESENCE}))
    elif name == "duplicate_scope_semantics": c = replace(c, scope=("project:alpha","project:alpha"))
    elif name == "whitespace_semantics": c = replace(c, objective=" Deliver   verified\n artifact ")
    else: raise ValueError(f"unknown scenario {name}")
    return c, cp


def main() -> int:
    data = json.loads((ROOT / "fixtures" / "adversarial_cases.json").read_text(encoding="utf-8"))
    failures = []
    for case in data["cases"]:
        c, cp = scenario(case["scenario"])
        result = evaluate_commitment(c, cp)
        ok = result.decision.value == case["expected_decision"] and case["expected_reason"] in result.reason_codes
        print(f"{case['id']} {'PASS' if ok else 'FAIL'} {result.decision.value} {','.join(result.reason_codes)}")
        if not ok:
            failures.append(case["id"])
    print(f"CORPUS total={len(data['cases'])} failed={len(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
