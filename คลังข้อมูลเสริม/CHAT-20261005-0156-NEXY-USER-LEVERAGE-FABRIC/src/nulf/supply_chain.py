from __future__ import annotations

from dataclasses import dataclass
import re

from .common import Verdict, canonical_hash

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class Dependency:
    name: str
    version: str
    source: str
    sha256: str
    pinned: bool
    signature_state: str
    permissions: frozenset[str]
    network_domains: frozenset[str]


@dataclass(frozen=True)
class TrustPolicy:
    allowed_sources: frozenset[str]
    allowed_signature_states: frozenset[str]
    allowed_permissions: frozenset[str]
    allowed_network_domains: frozenset[str]
    require_pinned: bool = True
    require_sha256: bool = True


def audit(policy: TrustPolicy, dependencies: tuple[Dependency, ...]) -> dict:
    names = [d.name for d in dependencies]
    duplicate_names = sorted({name for name in names if names.count(name) > 1})
    issues: list[dict[str, str]] = []

    for dep in sorted(dependencies, key=lambda d: d.name):
        if not dep.name.strip() or not dep.version.strip():
            issues.append({"dependency": dep.name or "<blank>", "code": "INVALID_IDENTITY"})
            continue
        if dep.source not in policy.allowed_sources:
            issues.append({"dependency": dep.name, "code": "UNTRUSTED_SOURCE"})
        if policy.require_pinned and not dep.pinned:
            issues.append({"dependency": dep.name, "code": "UNPINNED_VERSION"})
        if policy.require_sha256 and not _SHA256_RE.fullmatch(dep.sha256.lower()):
            issues.append({"dependency": dep.name, "code": "INVALID_SHA256"})
        if dep.signature_state not in policy.allowed_signature_states:
            issues.append({"dependency": dep.name, "code": "UNACCEPTED_SIGNATURE_STATE"})
        for permission in sorted(dep.permissions - policy.allowed_permissions):
            issues.append({"dependency": dep.name, "code": f"PERMISSION_NOT_ALLOWED:{permission}"})
        for domain in sorted(dep.network_domains - policy.allowed_network_domains):
            issues.append({"dependency": dep.name, "code": f"NETWORK_DOMAIN_NOT_ALLOWED:{domain}"})

    if duplicate_names:
        issues.extend({"dependency": name, "code": "DUPLICATE_DEPENDENCY_NAME"} for name in duplicate_names)

    issues = sorted(issues, key=lambda x: (x["dependency"], x["code"]))
    result = {
        "verdict": Verdict.FREEZE.value if issues else Verdict.PASS.value,
        "reason_codes": sorted({issue["code"].split(":", 1)[0] for issue in issues}),
        "issues": issues,
        "dependencies_checked": len(dependencies),
    }
    result["fingerprint"] = canonical_hash({"policy": policy, "dependencies": sorted(dependencies, key=lambda d: d.name), "result": result})
    return result
