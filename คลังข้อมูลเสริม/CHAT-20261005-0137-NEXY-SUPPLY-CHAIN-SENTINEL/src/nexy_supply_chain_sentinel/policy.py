from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from typing import Any, Mapping


class PolicyError(ValueError):
    pass


@dataclass(frozen=True)
class Policy:
    require_integrity: bool = True
    allowed_npm_hosts: tuple[str, ...] = ("registry.npmjs.org",)
    allow_additions: bool = False
    allow_removals: bool = False
    allow_version_changes: bool = False
    allow_source_changes: bool = False
    allow_integrity_changes: bool = False
    max_packages: int = 100_000
    max_input_bytes: int = 64 * 1024 * 1024

    def __post_init__(self) -> None:
        if not isinstance(self.max_packages, int) or isinstance(self.max_packages, bool) or self.max_packages < 1:
            raise PolicyError("max_packages must be a positive integer")
        if not isinstance(self.max_input_bytes, int) or isinstance(self.max_input_bytes, bool) or self.max_input_bytes < 1:
            raise PolicyError("max_input_bytes must be a positive integer")
        hosts = self.allowed_npm_hosts
        if not isinstance(hosts, tuple) or not hosts or any(not isinstance(h, str) or not h.strip() for h in hosts):
            raise PolicyError("allowed_npm_hosts must be a non-empty tuple of host names")
        normalized = tuple(sorted({h.strip().lower() for h in hosts}))
        object.__setattr__(self, "allowed_npm_hosts", normalized)

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "Policy":
        if not isinstance(value, Mapping):
            raise PolicyError("policy must be a JSON object")
        allowed = {f.name for f in fields(cls)}
        unknown = sorted(set(value) - allowed)
        if unknown:
            raise PolicyError(f"unknown policy fields: {', '.join(unknown)}")
        kwargs = dict(value)
        if "allowed_npm_hosts" in kwargs:
            hosts = kwargs["allowed_npm_hosts"]
            if not isinstance(hosts, list):
                raise PolicyError("allowed_npm_hosts must be a JSON array")
            kwargs["allowed_npm_hosts"] = tuple(hosts)
        bool_fields = {
            "require_integrity",
            "allow_additions",
            "allow_removals",
            "allow_version_changes",
            "allow_source_changes",
            "allow_integrity_changes",
        }
        for name in bool_fields:
            if name in kwargs and not isinstance(kwargs[name], bool):
                raise PolicyError(f"{name} must be boolean")
        return cls(**kwargs)

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["allowed_npm_hosts"] = list(self.allowed_npm_hosts)
        return value
