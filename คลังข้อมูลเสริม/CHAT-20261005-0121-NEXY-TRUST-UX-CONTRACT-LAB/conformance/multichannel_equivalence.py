from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping

_THIS = Path(__file__).resolve().parent
_CHECKER_PATH = _THIS / "truth_surface_checker.py"
_SPEC = importlib.util.spec_from_file_location("truth_surface_checker", _CHECKER_PATH)
assert _SPEC and _SPEC.loader
checker = importlib.util.module_from_spec(_SPEC)
sys.modules.setdefault("truth_surface_checker", checker)
_SPEC.loader.exec_module(checker)


@dataclass(frozen=True)
class ChannelViolation:
    code: str
    channel: str
    path: str
    message: str


@dataclass(frozen=True)
class MultiChannelReport:
    schema_version: str
    conformant: bool
    channels: tuple[str, ...]
    per_channel_reports: Mapping[str, Mapping[str, Any]]
    cross_channel_violations: tuple[ChannelViolation, ...]
    certificate_fingerprint: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "conformant": self.conformant,
            "channels": list(self.channels),
            "per_channel_reports": dict(self.per_channel_reports),
            "cross_channel_violations": [asdict(v) for v in self.cross_channel_violations],
            "certificate_fingerprint": self.certificate_fingerprint,
        }


def _action_signature(surface: Mapping[str, Any]) -> tuple[tuple[str, str], ...]:
    raw = surface.get("actions", [])
    if not isinstance(raw, list):
        return tuple()
    sig = []
    for action in raw:
        if isinstance(action, Mapping):
            aid = action.get("id")
            kind = action.get("kind")
            if isinstance(aid, str) and isinstance(kind, str):
                sig.append((aid, kind))
    return tuple(sorted(sig))


def audit_channels(
    backend: Mapping[str, Any],
    surfaces: Mapping[str, Mapping[str, Any]],
    role: str,
) -> MultiChannelReport:
    if not isinstance(surfaces, Mapping) or not surfaces:
        raise checker.ConformanceInputError("surfaces must be a non-empty channel mapping")

    names = tuple(sorted(surfaces))
    reports: dict[str, Mapping[str, Any]] = {}
    cross: list[ChannelViolation] = []

    for name in names:
        if not isinstance(name, str) or not name.strip():
            raise checker.ConformanceInputError("channel name must be non-empty text")
        report = checker.audit_surface(backend, surfaces[name], role)
        reports[name] = report.to_dict()

    baseline_name = names[0]
    baseline = surfaces[baseline_name]
    baseline_fields = {
        "displayed_status": baseline.get("displayed_status"),
        "displayed_state": baseline.get("displayed_state"),
        "result_visible": baseline.get("result_visible"),
        "request_id": baseline.get("request_id"),
        "trace_id": baseline.get("trace_id"),
    }
    baseline_actions = _action_signature(baseline)

    for name in names[1:]:
        surface = surfaces[name]
        for field, expected in baseline_fields.items():
            if surface.get(field) != expected:
                cross.append(ChannelViolation(
                    code=f"CHANNEL_{field.upper()}_DIVERGENCE",
                    channel=name,
                    path=f"surfaces.{name}.{field}",
                    message=f"Channel {name} differs from baseline channel {baseline_name} for {field}.",
                ))
        if _action_signature(surface) != baseline_actions:
            cross.append(ChannelViolation(
                code="CHANNEL_ACTION_DIVERGENCE",
                channel=name,
                path=f"surfaces.{name}.actions",
                message=f"Channel {name} exposes a different action set from baseline channel {baseline_name}.",
            ))

    channel_conformant = all(report["conformant"] is True for report in reports.values())
    conformant = channel_conformant and not cross
    normalized = {
        "schema_version": "1.0.0-proposal",
        "channels": list(names),
        "per_channel_reports": reports,
        "cross_channel_violations": [asdict(v) for v in cross],
    }
    fp = hashlib.sha256(json.dumps(normalized, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    return MultiChannelReport(
        schema_version="1.0.0-proposal",
        conformant=conformant,
        channels=names,
        per_channel_reports=reports,
        cross_channel_violations=tuple(cross),
        certificate_fingerprint=fp,
    )
