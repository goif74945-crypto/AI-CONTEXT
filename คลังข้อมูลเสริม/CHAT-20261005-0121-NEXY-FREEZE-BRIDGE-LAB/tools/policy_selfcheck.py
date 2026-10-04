from __future__ import annotations

from freeze_bridge import (
    Disclosure,
    FreezeStatus,
    Locale,
    ReasonCode,
    RecoveryIntent,
    RecoveryOwner,
    compile_mapping,
)
from freeze_bridge.policy import REASON_POLICIES


def main() -> int:
    checked = 0
    all_intents = [intent.value for intent in RecoveryIntent]
    for reason in ReasonCode:
        policy = REASON_POLICIES[reason]
        for locale in Locale:
            for disclosure in Disclosure:
                for status in FreezeStatus:
                    payload = {
                        "protocol_version": "1.1",
                        "event_id": f"selfcheck-{checked}",
                        "reason_code": reason.value,
                        "status": status.value,
                        "blocking_layer": "SELF_CHECK",
                        "recovery_owner": RecoveryOwner.OPERATOR.value,
                        "disclosure": disclosure.value,
                        "locale": locale.value,
                        "dependency_recheck_safe": True,
                        "missing_inputs": ["alpha", "beta"],
                        "evidence_refs": [
                            "public:proof/1",
                            "internal:trace/2",
                            "secret:incident/3",
                        ],
                        "authorized_recovery_intents": all_intents,
                    }
                    first = compile_mapping(payload)
                    second = compile_mapping(payload)
                    if first != second:
                        raise AssertionError(
                            f"non-deterministic output for {reason}/{locale}/{disclosure}/{status}"
                        )
                    emitted = set(first["eligible_recovery_intents"])
                    allowed = {intent.value for intent in policy.allowed_intents}
                    if not emitted.issubset(allowed):
                        raise AssertionError(f"unauthorized intent leak for {reason}: {emitted - allowed}")
                    if first["downstream_ui_authority_required"] is not True:
                        raise AssertionError("bridge unexpectedly claimed downstream UI authority")
                    forbidden_output_keys = {"role", "display_mode", "actions", "primary_action", "secondary_actions"}
                    if forbidden_output_keys.intersection(first):
                        raise AssertionError("Trust UX responsibility leaked into Freeze Bridge output")
                    if reason is ReasonCode.SECURITY_INTEGRITY and disclosure is Disclosure.RESTRICTED:
                        if first["evidence_refs"]:
                            raise AssertionError("restricted security event leaked evidence refs")
                        if first["dependency_recheck_safe"]:
                            raise AssertionError("restricted security event became dependency-recheck safe")
                    if reason is ReasonCode.UNKNOWN_REASON and first["dependency_recheck_safe"]:
                        raise AssertionError("unknown reason became dependency-recheck safe")
                    checked += 1
    print(f"PASS policy_matrix_cases={checked}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
