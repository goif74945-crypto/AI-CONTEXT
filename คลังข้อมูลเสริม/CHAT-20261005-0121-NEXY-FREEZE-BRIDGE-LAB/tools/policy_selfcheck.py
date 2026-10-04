from __future__ import annotations

from freeze_bridge import ActionCode, Disclosure, FreezeStatus, Locale, ReasonCode, RecoveryOwner, compile_mapping
from freeze_bridge.policy import REASON_POLICIES


def main() -> int:
    checked = 0
    all_actions = [action.value for action in ActionCode]
    for reason in ReasonCode:
        policy = REASON_POLICIES[reason]
        for locale in Locale:
            for disclosure in Disclosure:
                for status in FreezeStatus:
                    payload = {
                        "protocol_version": "1.0",
                        "event_id": f"selfcheck-{checked}",
                        "reason_code": reason.value,
                        "status": status.value,
                        "blocking_layer": "SELF_CHECK",
                        "recovery_owner": RecoveryOwner.OPERATOR.value,
                        "disclosure": disclosure.value,
                        "locale": locale.value,
                        "retryable": True,
                        "missing_inputs": ["alpha", "beta"],
                        "evidence_refs": ["public:proof/1", "internal:trace/2", "secret:incident/3"],
                        "authorized_actions": all_actions,
                    }
                    first = compile_mapping(payload)
                    second = compile_mapping(payload)
                    if first != second:
                        raise AssertionError(f"non-deterministic output for {reason}/{locale}/{disclosure}/{status}")
                    emitted = {item["code"] for item in first["actions"]}
                    allowed = {action.value for action in policy.allowed_actions}
                    if not emitted.issubset(allowed):
                        raise AssertionError(f"unauthorized action leak for {reason}: {emitted - allowed}")
                    if reason is ReasonCode.SECURITY_INTEGRITY and disclosure is Disclosure.RESTRICTED:
                        if first["evidence_refs"]:
                            raise AssertionError("restricted security event leaked evidence refs")
                        if first["retryable"]:
                            raise AssertionError("restricted security event became retryable")
                    if reason is ReasonCode.UNKNOWN_REASON and first["retryable"]:
                        raise AssertionError("unknown reason became retryable")
                    checked += 1
    print(f"PASS policy_matrix_cases={checked}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
