from __future__ import annotations

import re
from collections.abc import Iterable
from types import MappingProxyType

from .model import (
    ImpactClass,
    PreferenceDefinition,
    RegistryError,
    ScopeKind,
)

_KEY_PATTERN = re.compile(r"^[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)+$")
_PROTECTED_PREFIXES = (
    "auth.",
    "core.",
    "evidence.",
    "law.",
    "permission.",
    "rbac.",
    "release.",
    "safety.",
    "security.",
)
_MAX_EXECUTION_SENSITIVE_TTL_SECONDS = 24 * 60 * 60


class PreferenceRegistry:
    """Immutable allowlist of preference keys and their safety contracts."""

    def __init__(self, definitions: Iterable[PreferenceDefinition]) -> None:
        indexed: dict[str, PreferenceDefinition] = {}
        for definition in definitions:
            self._validate_definition(definition)
            if definition.key in indexed:
                raise RegistryError(f"duplicate preference definition: {definition.key}")
            indexed[definition.key] = definition
        if not indexed:
            raise RegistryError("registry must contain at least one preference definition")
        self._definitions = MappingProxyType(dict(sorted(indexed.items())))

    @staticmethod
    def _validate_definition(definition: PreferenceDefinition) -> None:
        if not _KEY_PATTERN.fullmatch(definition.key):
            raise RegistryError(f"invalid preference key syntax: {definition.key}")
        if definition.key.startswith(_PROTECTED_PREFIXES):
            raise RegistryError(f"protected authority domain cannot be personalized: {definition.key}")

        if definition.impact is ImpactClass.EXECUTION_SENSITIVE:
            if not definition.requires_expiry:
                raise RegistryError(
                    f"{definition.key}: execution-sensitive definitions must require expiry"
                )
            if not definition.requires_consent_receipt:
                raise RegistryError(
                    f"{definition.key}: execution-sensitive definitions require consent receipt"
                )
            if definition.max_ttl_seconds > _MAX_EXECUTION_SENSITIVE_TTL_SECONDS:
                raise RegistryError(
                    f"{definition.key}: execution-sensitive TTL exceeds 24-hour lab ceiling"
                )
            forbidden = definition.allowed_scopes.difference(
                {ScopeKind.SESSION, ScopeKind.TASK}
            )
            if forbidden:
                raise RegistryError(
                    f"{definition.key}: execution-sensitive preferences are session/task scoped only"
                )

    def get(self, key: str) -> PreferenceDefinition:
        try:
            return self._definitions[key]
        except KeyError as exc:
            raise RegistryError(f"unregistered preference key: {key}") from exc

    def keys(self) -> tuple[str, ...]:
        return tuple(self._definitions)

    def definitions(self) -> tuple[PreferenceDefinition, ...]:
        return tuple(self._definitions.values())


def default_registry() -> PreferenceRegistry:
    common_scopes = frozenset(
        {ScopeKind.USER, ScopeKind.PROJECT, ScopeKind.SESSION, ScopeKind.TASK}
    )
    return PreferenceRegistry(
        [
            PreferenceDefinition(
                key="presentation.verbosity",
                allowed_values=("concise", "balanced", "detailed"),
                default="balanced",
                impact=ImpactClass.PRESENTATION,
                allowed_scopes=common_scopes,
                description="Preferred amount of explanatory detail.",
            ),
            PreferenceDefinition(
                key="presentation.explanation_depth",
                allowed_values=("brief", "standard", "deep"),
                default="standard",
                impact=ImpactClass.PRESENTATION,
                allowed_scopes=common_scopes,
                description="Preferred explanation depth without changing truth or evidence gates.",
            ),
            PreferenceDefinition(
                key="interaction.confirmation_density",
                allowed_values=("minimal", "standard", "explicit"),
                default="standard",
                impact=ImpactClass.PRESENTATION,
                allowed_scopes=common_scopes,
                description="Presentation density for non-authoritative confirmations.",
            ),
            PreferenceDefinition(
                key="workflow.auto_show_evidence",
                allowed_values=(False, True),
                default=True,
                impact=ImpactClass.WORKFLOW_CONVENIENCE,
                allowed_scopes=common_scopes,
                description="Whether evidence summaries are shown automatically when available.",
            ),
            PreferenceDefinition(
                key="workflow.result_structure",
                allowed_values=("prose", "table", "checklist"),
                default="prose",
                impact=ImpactClass.WORKFLOW_CONVENIENCE,
                allowed_scopes=common_scopes,
                description="Preferred result presentation structure.",
            ),
        ]
    )
