from __future__ import annotations

from .model import Action, Role

ROLE_SURFACE_CAPABILITIES: dict[Role, frozenset[Action]] = {
    Role.OWNER: frozenset({
        Action.VIEW_RESULT, Action.OPEN_TRACE, Action.SUBMIT_DIRECTIVE,
        Action.RECOVER_FREEZE, Action.EXPORT_ARTIFACT, Action.EXPORT_AUDIT,
        Action.CONFIG_CHANGE, Action.HARD_DELETE,
    }),
    Role.OPERATOR: frozenset({
        Action.VIEW_RESULT, Action.OPEN_TRACE, Action.SUBMIT_DIRECTIVE,
        Action.EXPORT_ARTIFACT,
    }),
    Role.AUDITOR: frozenset({
        Action.VIEW_RESULT, Action.OPEN_TRACE, Action.EXPORT_AUDIT,
    }),
    Role.SYSTEM: frozenset({Action.OPEN_TRACE, Action.EXPORT_AUDIT}),
    Role.PUBLIC_USER: frozenset({Action.VIEW_RESULT}),
}

MUTATING_ACTIONS = frozenset({
    Action.SUBMIT_DIRECTIVE,
    Action.RECOVER_FREEZE,
    Action.CONFIG_CHANGE,
    Action.HARD_DELETE,
})
