from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Iterable, Mapping


class SchemaInputError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class FieldSpec:
    name: str
    type_name: str
    required: bool = False
    enum_values: tuple[str, ...] = ()
    has_default: bool = False


@dataclass(frozen=True, slots=True)
class ContractSchema:
    version: str
    fields: tuple[FieldSpec, ...]
    additional_properties: bool = False


@dataclass(frozen=True, slots=True)
class Change:
    code: str
    field: str
    severity: str
    detail: str


@dataclass(frozen=True, slots=True)
class EvolutionPlan:
    classification: str
    recommended_semver_bump: str
    changes: tuple[Change, ...]
    migration_steps: tuple[str, ...]
    rollback_possible: bool
    reason_codes: tuple[str, ...]
    fingerprint: str


def _clean(value: str, field: str) -> str:
    if not isinstance(value, str):
        raise SchemaInputError(f"{field}:NOT_STRING")
    value = value.strip()
    if not value:
        raise SchemaInputError(f"{field}:EMPTY")
    return value


def _normalize_field(field: FieldSpec) -> FieldSpec:
    name = _clean(field.name, "field.name")
    type_name = _clean(field.type_name, f"{name}.type")
    enum_values = tuple(sorted({_clean(v, f"{name}.enum") for v in field.enum_values}))
    if enum_values and type_name not in {"string", "integer", "number"}:
        raise SchemaInputError(f"{name}:ENUM_UNSUPPORTED_FOR_TYPE")
    return FieldSpec(name, type_name, bool(field.required), enum_values, bool(field.has_default))


def _normalize_schema(schema: ContractSchema) -> ContractSchema:
    version = _clean(schema.version, "version")
    fields = tuple(sorted((_normalize_field(f) for f in schema.fields), key=lambda f: f.name))
    names = [f.name for f in fields]
    if len(names) != len(set(names)):
        raise SchemaInputError("DUPLICATE_FIELD")
    return ContractSchema(version, fields, bool(schema.additional_properties))


def _type_relation(old: str, new: str) -> str:
    if old == new:
        return "SAME"
    if old == "integer" and new == "number":
        return "WIDENING"
    return "BREAKING"


def _map_fields(schema: ContractSchema) -> dict[str, FieldSpec]:
    return {f.name: f for f in schema.fields}


def compile_evolution(
    old_schema: ContractSchema,
    new_schema: ContractSchema,
    *,
    explicit_renames: Mapping[str, str] | None = None,
) -> EvolutionPlan:
    old_schema = _normalize_schema(old_schema)
    new_schema = _normalize_schema(new_schema)
    explicit_renames = dict(explicit_renames or {})

    old = _map_fields(old_schema)
    new = _map_fields(new_schema)
    renames: dict[str, str] = {}
    for src, dst in sorted(explicit_renames.items()):
        src, dst = _clean(src, "rename.source"), _clean(dst, "rename.target")
        if src not in old or dst not in new:
            raise SchemaInputError(f"INVALID_RENAME:{src}->{dst}")
        if src == dst:
            raise SchemaInputError(f"REDUNDANT_RENAME:{src}")
        if dst in renames.values():
            raise SchemaInputError(f"DUPLICATE_RENAME_TARGET:{dst}")
        renames[src] = dst

    effective_targets: dict[str, str] = {}
    for old_name in sorted(old):
        target = renames.get(old_name, old_name)
        previous = effective_targets.get(target)
        if previous is not None and previous != old_name:
            raise SchemaInputError(f"AMBIGUOUS_TARGET:{previous},{old_name}->{target}")
        effective_targets[target] = old_name

    changes: list[Change] = []
    migration_steps: list[str] = []
    reason_codes: set[str] = set()
    consumed_new: set[str] = set()

    for old_name, old_field in sorted(old.items()):
        target_name = renames.get(old_name, old_name)
        new_field = new.get(target_name)
        if old_name in renames:
            consumed_new.add(target_name)
            changes.append(Change("FIELD_RENAMED", old_name, "MIGRATION", f"{old_name}->{target_name}"))
            migration_steps.append(f"COPY {old_name} TO {target_name}; retain compatibility bridge until consumers migrate")
            reason_codes.add("EXPLICIT_RENAME_REQUIRES_MIGRATION")
        if new_field is None:
            changes.append(Change("FIELD_REMOVED", old_name, "BREAKING", "existing consumer-visible field removed"))
            reason_codes.add("FIELD_REMOVAL")
            continue

        relation = _type_relation(old_field.type_name, new_field.type_name)
        if relation == "BREAKING":
            changes.append(Change("TYPE_CHANGED", old_name, "BREAKING", f"{old_field.type_name}->{new_field.type_name}"))
            reason_codes.add("TYPE_BREAK")
        elif relation == "WIDENING":
            changes.append(Change("TYPE_WIDENED", old_name, "ADDITIVE", f"{old_field.type_name}->{new_field.type_name}"))

        if old_field.required and not new_field.required:
            changes.append(Change("REQUIRED_TO_OPTIONAL", old_name, "ADDITIVE", "consumer requirement relaxed"))
        elif not old_field.required and new_field.required:
            if new_field.has_default:
                changes.append(Change("OPTIONAL_TO_REQUIRED_WITH_DEFAULT", old_name, "MIGRATION", "backfill/default required"))
                migration_steps.append(f"BACKFILL {target_name} USING DECLARED DEFAULT before enforcing required")
                reason_codes.add("REQUIREDNESS_MIGRATION")
            else:
                changes.append(Change("OPTIONAL_TO_REQUIRED", old_name, "BREAKING", "old payloads may omit field"))
                reason_codes.add("REQUIREDNESS_BREAK")

        old_enum, new_enum = set(old_field.enum_values), set(new_field.enum_values)
        if old_enum or new_enum:
            if old_enum and not new_enum:
                changes.append(Change("ENUM_CONSTRAINT_REMOVED", old_name, "ADDITIVE", "accepted value set widened to unconstrained type"))
            elif not old_enum and new_enum:
                changes.append(Change("ENUM_CONSTRAINT_ADDED", old_name, "BREAKING", "previous arbitrary values may now be rejected"))
                reason_codes.add("ENUM_NARROWING")
            elif not old_enum.issubset(new_enum):
                removed = sorted(old_enum - new_enum)
                changes.append(Change("ENUM_VALUES_REMOVED", old_name, "BREAKING", f"removed={removed}"))
                reason_codes.add("ENUM_NARROWING")
            elif new_enum != old_enum:
                added = sorted(new_enum - old_enum)
                changes.append(Change("ENUM_VALUES_ADDED", old_name, "ADDITIVE", f"added={added}"))

    for new_name, new_field in sorted(new.items()):
        if new_name in old or new_name in consumed_new:
            continue
        if new_field.required and not new_field.has_default:
            changes.append(Change("REQUIRED_FIELD_ADDED", new_name, "BREAKING", "old payloads cannot satisfy new requirement"))
            reason_codes.add("REQUIRED_ADDITION")
        elif new_field.required and new_field.has_default:
            changes.append(Change("REQUIRED_FIELD_ADDED_WITH_DEFAULT", new_name, "MIGRATION", "requires deterministic default/backfill"))
            migration_steps.append(f"ADD {new_name} WITH DECLARED DEFAULT; BACKFILL {new_name} BEFORE STRICT ENFORCEMENT")
            reason_codes.add("ADDITION_MIGRATION")
        else:
            changes.append(Change("OPTIONAL_FIELD_ADDED", new_name, "ADDITIVE", "backward-readable additive field"))

    if old_schema.additional_properties and not new_schema.additional_properties:
        changes.append(Change("ADDITIONAL_PROPERTIES_DISABLED", "*", "BREAKING", "previous unknown properties may be rejected"))
        reason_codes.add("OPEN_TO_CLOSED_SCHEMA")
    elif not old_schema.additional_properties and new_schema.additional_properties:
        changes.append(Change("ADDITIONAL_PROPERTIES_ENABLED", "*", "ADDITIVE", "schema accepts additional properties"))

    severities = {c.severity for c in changes}
    if "BREAKING" in severities:
        classification = "BREAKING"
        bump = "MAJOR"
    elif "MIGRATION" in severities:
        classification = "MIGRATION_REQUIRED"
        bump = "MAJOR"
    elif "ADDITIVE" in severities:
        classification = "ADDITIVE_COMPATIBLE"
        bump = "MINOR"
    else:
        classification = "NO_STRUCTURAL_CHANGE"
        bump = "PATCH"

    rollback_possible = "BREAKING" not in severities and all("DROP" not in step for step in migration_steps)
    payload = {
        "old_version": old_schema.version,
        "new_version": new_schema.version,
        "classification": classification,
        "recommended_semver_bump": bump,
        "changes": [
            {"code": c.code, "field": c.field, "severity": c.severity, "detail": c.detail}
            for c in changes
        ],
        "migration_steps": migration_steps,
        "rollback_possible": rollback_possible,
        "reason_codes": sorted(reason_codes),
    }
    fingerprint = sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return EvolutionPlan(
        classification,
        bump,
        tuple(changes),
        tuple(migration_steps),
        rollback_possible,
        tuple(sorted(reason_codes)),
        fingerprint,
    )
