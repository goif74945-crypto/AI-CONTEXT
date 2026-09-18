from __future__ import annotations

import hashlib
import importlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

REPOSITORY = "goif74945-crypto/AI-CONTEXT"
BRANCH = "main"
RUNTIME_ROOT = "skills/nexy/runtime"
RUNTIME_VERSION = "1.1.0"
CANONICAL_REGISTRY_PATH = "skills/registry/registry.json"
PDF_SHA256 = "a2b07fcc9f792ac03331e60ffdfe1a87594788d7d65c75a361b463ea158e5a1c"
TARGET_IDS = ("GOV-001", "GOV-002", "CTX-001", "CTX-003", "REQ-001", "ARC-001", "ARC-004")
UNIVERSAL_REQUIRED = (
    "task", "authority", "scope", "repository", "branch", "head",
    "source_of_truth", "constraints", "expected_output", "validation_requirements",
)
UNIVERSAL_OUTPUT = (
    "status", "objective", "scope", "inputs", "actions", "changed_files",
    "unchanged_files", "validation", "evidence", "errors", "unknowns",
    "remaining", "next_action",
)
AUTHORITY_ORDER = {
    "CURRENT_USER_COMMAND": 1,
    "PROJECT_INSTRUCTIONS": 2,
    "MASTER_SPECIFICATION": 3,
    "PDF": 4,
    "REPOSITORY": 5,
    "VALIDATION_EVIDENCE": 6,
}


class RuntimeFault(Exception):
    def __init__(self, message: str, code: str, critical: bool = False):
        super().__init__(message)
        self.code = code
        self.critical = critical


class InvalidInput(RuntimeFault):
    def __init__(self, message: str):
        super().__init__(message, "INVALID_INPUT")


class Unauthorized(RuntimeFault):
    def __init__(self, message: str):
        super().__init__(message, "UNAUTHORIZED")


class SkillNotFound(RuntimeFault):
    def __init__(self, message: str):
        super().__init__(message, "INVALID_SKILL_ID")


class ScopeViolation(RuntimeFault):
    def __init__(self, message: str):
        super().__init__(message, "SCOPE_VIOLATION")


class RepositoryMismatch(RuntimeFault):
    def __init__(self, message: str):
        super().__init__(message, "REPOSITORY_MISMATCH")


class BranchMismatch(RuntimeFault):
    def __init__(self, message: str):
        super().__init__(message, "BRANCH_MISMATCH")


class IntegrityFailure(RuntimeFault):
    def __init__(self, message: str):
        super().__init__(message, "INTEGRITY_MISMATCH", True)


class AuthorityConflict(RuntimeFault):
    def __init__(self, message: str):
        super().__init__(message, "AUTHORITY_CONFLICT", True)


class ValidationFailure(RuntimeFault):
    def __init__(self, message: str, critical: bool = False):
        super().__init__(message, "VALIDATION_FAILURE", critical)


class MissingRequiredInput(RuntimeFault):
    def __init__(self, message: str):
        super().__init__(message, "MISSING_REQUIRED_INPUT", False)


class MissingSafetyCriticalInput(RuntimeFault):
    def __init__(self, message: str):
        super().__init__(message, "MISSING_SAFETY_CRITICAL_INPUT", False)


@dataclass(frozen=True)
class RegistryEntry:
    id: str
    name: str
    source_path: str
    runtime_entry: str
    permissions: tuple[str, ...]
    validator: str
    evidence_handler: str
    tests: tuple[str, ...]


@dataclass(frozen=True)
class AuthorizationToken:
    token_id: str
    execution_id: str
    skill_id: str
    action: str
    repository: str
    branch: str
    head: str
    scope_hash: str


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_hex(value: Any) -> str:
    raw = value if isinstance(value, bytes) else canonical_json(value).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def stable_id(prefix: str, value: Any) -> str:
    return f"{prefix}-{sha256_hex(value)[:16].upper()}"


def valid_head(head: Any) -> bool:
    if not isinstance(head, str) or len(head) != 40:
        return False
    try:
        int(head, 16)
        return True
    except ValueError:
        return False


def repo_root_from_registry(path: str | Path) -> Path:
    registry = Path(path)
    return registry.parent.parent.parent


def load_registry(path: str | Path = CANONICAL_REGISTRY_PATH) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    validate_registry(data)
    return data


def validate_registry(data: dict[str, Any]) -> None:
    if data.get("registry_id") != "AI-CONTEXT-SKILL-REGISTRY":
        raise ValidationFailure("Canonical registry identity mismatch", True)
    if data.get("branch") != BRANCH:
        raise ValidationFailure("Canonical registry branch mismatch", True)
    skills = data.get("skills")
    if not isinstance(skills, list):
        raise ValidationFailure("Canonical registry skills must be a list", True)
    ids = [item.get("id") for item in skills if isinstance(item, dict)]
    if len(ids) != len(set(ids)):
        raise ValidationFailure("Canonical registry contains duplicate Skill IDs", True)
    target_entries = [item for item in skills if isinstance(item, dict) and item.get("id") in TARGET_IDS]
    if set(ids) & set(TARGET_IDS) != set(TARGET_IDS):
        raise ValidationFailure("Canonical registry is missing one or more target Skills", True)
    if len(target_entries) != len(TARGET_IDS):
        raise ValidationFailure("Canonical registry target Skill multiplicity mismatch", True)
    required = {
        "id", "name", "status", "implementation", "load_path", "locator",
        "permissions", "dependencies", "validation", "source_basis",
        "source_path", "validator", "evidence_handler", "tests",
    }
    for item in target_entries:
        if not required.issubset(item):
            missing = sorted(required - set(item))
            raise ValidationFailure(f"Registry entry {item.get('id')} missing fields: {missing}", True)
        if item["status"] == "BLOCKED":
            raise ValidationFailure(f"Target Skill {item['id']} is BLOCKED", True)
        if item["implementation"] != "PYTHON_RUNTIME":
            raise ValidationFailure(f"Target Skill {item['id']} is not bound to PYTHON_RUNTIME", True)
        if item["load_path"] != f"{RUNTIME_ROOT}/runtime.py":
            raise ValidationFailure(f"Target Skill {item['id']} load_path mismatch", True)
        if item["source_path"].split("/")[-1] != "SKILL.md":
            raise ValidationFailure(f"Target Skill {item['id']} source path mismatch", True)


def resolve_entry(registry: dict[str, Any], skill_id: str) -> RegistryEntry:
    for item in registry["skills"]:
        if item.get("id") == skill_id:
            if skill_id not in TARGET_IDS:
                raise SkillNotFound(f"Skill ID is not in scoped target set: {skill_id}")
            return RegistryEntry(
                id=item["id"],
                name=item["name"],
                source_path=item["source_path"],
                runtime_entry=item["locator"],
                permissions=tuple(item["permissions"]),
                validator=item["validator"],
                evidence_handler=item["evidence_handler"],
                tests=tuple(item["tests"]),
            )
    raise SkillNotFound(f"Unknown Skill ID: {skill_id}")


def load_callable(reference: str) -> Callable[..., Any]:
    if ":" not in reference:
        raise ValidationFailure(f"Invalid callable reference: {reference}", True)
    module, function = reference.split(":", 1)
    try:
        obj = getattr(importlib.import_module(module), function)
    except Exception as exc:
        raise ValidationFailure(f"Callable import failed: {reference}: {exc}", True) from exc
    if not callable(obj):
        raise ValidationFailure(f"Callable is not executable: {reference}", True)
    return obj


def validate_input_contract(envelope: dict[str, Any]) -> None:
    if not isinstance(envelope, dict):
        raise InvalidInput("Execution envelope must be an object")
    context = envelope.get("context")
    if not isinstance(context, dict):
        raise InvalidInput("context is required")
    missing = [field for field in UNIVERSAL_REQUIRED if field not in context]
    if missing:
        safety_missing = [field for field in missing if field in {
            "authority", "scope", "repository", "branch", "head",
            "source_of_truth", "constraints", "validation_requirements",
        }]
        if safety_missing:
            raise MissingSafetyCriticalInput(
                "Missing safety-critical input fields: " + ", ".join(safety_missing)
            )
        raise MissingRequiredInput("Missing required input fields: " + ", ".join(missing))
    if not isinstance(context["scope"], dict):
        raise InvalidInput("scope must be an object")
    if not isinstance(context["source_of_truth"], list) or not context["source_of_truth"]:
        raise InvalidInput("source_of_truth must be non-empty")
    if not isinstance(context["constraints"], list):
        raise InvalidInput("constraints must be a list")
    if not envelope.get("execution_id") or not envelope.get("action"):
        raise InvalidInput("execution_id and action are required")


def validate_output_contract(output: dict[str, Any]) -> None:
    if not isinstance(output, dict):
        raise ValidationFailure("Skill output must be an object", True)
    missing = [field for field in UNIVERSAL_OUTPUT if field not in output]
    if missing:
        raise ValidationFailure("Missing output fields: " + ", ".join(missing), True)


def validate_trace(trace: list[str]) -> None:
    expected = ["LOAD", "RESOLVE", "AUTHORIZE", "EXECUTE", "VALIDATE", "EVIDENCE", "RESULT"]
    if trace != expected:
        raise ValidationFailure(f"Execution chain mismatch: {trace}", True)


def authorize(entry: RegistryEntry, envelope: dict[str, Any]) -> AuthorizationToken:
    context = envelope["context"]
    action = envelope["action"]
    execution_id = envelope["execution_id"]
    if action not in entry.permissions:
        raise Unauthorized(f"Permission {action} is not allowed for {entry.id}")
    authority = context.get("authority", {})
    if (
        not isinstance(authority, dict)
        or authority.get("source_type") not in AUTHORITY_ORDER
        or not authority.get("source_id")
    ):
        raise Unauthorized("Invalid authority source")
    if authority.get("rank") != AUTHORITY_ORDER[authority["source_type"]]:
        raise Unauthorized("Authority rank mismatch")
    if context.get("repository") != REPOSITORY:
        raise RepositoryMismatch(f"Execution repository must be {REPOSITORY}")
    if context.get("branch") != BRANCH:
        raise BranchMismatch(f"Execution branch must be {BRANCH}")
    if not valid_head(context.get("head")):
        raise InvalidInput("HEAD must be a 40-character hexadecimal commit")
    if context.get("expected_head") is not None and context["head"] != context["expected_head"]:
        raise InvalidInput("HEAD does not match expected_head")
    scope = context.get("scope", {})
    if (
        entry.id in set(scope.get("out_of_scope_skill_ids", []))
        or entry.id not in scope.get("skill_ids", [])
        or action not in scope.get("allowed_actions", [])
    ):
        raise ScopeViolation(f"{entry.id}/{action} is outside authorized scope")
    scope_hash = sha256_hex({"skill_id": entry.id, "action": action, "scope": scope})
    return AuthorizationToken(
        token_id=stable_id("AUT", {"execution_id": execution_id, "skill_id": entry.id, "scope_hash": scope_hash}),
        execution_id=execution_id,
        skill_id=entry.id,
        action=action,
        repository=REPOSITORY,
        branch=BRANCH,
        head=context["head"],
        scope_hash=scope_hash,
    )


def evidence_bind(
    execution_id: str,
    skill_id: str,
    head: str,
    trace: list[str],
    input_envelope: dict[str, Any],
    output: dict[str, Any],
    result_id: str,
    status: str = "VERIFIED",
) -> dict[str, Any]:
    payload = {
        "execution_id": execution_id,
        "skill_id": skill_id,
        "head": head,
        "trace": trace,
        "input": input_envelope,
        "output": output,
        "result_id": result_id,
    }
    return {
        "id": stable_id("EVD", payload),
        "type": "EVIDENCE",
        "execution_id": execution_id,
        "skill_id": skill_id,
        "result_id": result_id,
        "handler_id": "EVIDENCE-HANDLER-NEXY-001",
        "source_head": head,
        "content_hash": sha256_hex(payload),
        "trace": trace,
        "status": status,
    }


def execute_with_token(
    token: AuthorizationToken,
    skill_fn: Callable[[dict[str, Any]], dict[str, Any]],
    envelope: dict[str, Any],
) -> dict[str, Any]:
    if token.execution_id != envelope.get("execution_id") or token.skill_id != envelope.get("skill_id"):
        raise Unauthorized("Authorization token does not match execution envelope")
    return skill_fn(envelope)


def base(envelope: dict[str, Any], objective: str) -> dict[str, Any]:
    return {
        "status": "SUCCESS",
        "objective": objective,
        "scope": envelope["context"]["scope"],
        "inputs": envelope["context"],
        "actions": [],
        "changed_files": [],
        "unchanged_files": [],
        "validation": {"status": "PASS"},
        "evidence": [],
        "errors": [],
        "unknowns": [],
        "remaining": [],
        "next_action": "NONE",
    }


def execute_gov_001(envelope: dict[str, Any]) -> dict[str, Any]:
    sources = envelope.get("data", {}).get("sources")
    if not isinstance(sources, list) or not sources:
        raise InvalidInput("GOV-001 requires non-empty sources")
    candidates = [
        source
        for source in sources
        if isinstance(source, dict)
        and source.get("status", "VERIFIED") != "UNKNOWN"
        and source.get("source_type") in AUTHORITY_ORDER
    ]
    if not candidates:
        output = base(envelope, "Identify which Source has authority over a decision.")
        output.update({
            "status": "BLOCKED",
            "authority_result": "UNKNOWN",
            "source": None,
            "confidence": 0.0,
            "conflicts": [],
            "decision": "BLOCKED",
            "unknowns": ["No verified authority source"],
            "next_action": "ACQUIRE_AUTHORITY_SOURCE",
        })
        return output
    if any(not isinstance(source.get("rank"), int) for source in candidates):
        raise InvalidInput("GOV-001 source rank is required")
    max_rank = max(source["rank"] for source in candidates)
    top = [source for source in candidates if source["rank"] == max_rank]
    if len({source["source_id"] for source in top}) > 1:
        raise AuthorityConflict("Multiple sources share the highest authority rank")
    output = base(envelope, "Identify which Source has authority over a decision.")
    output.update({
        "authority_result": "AUTHORITATIVE",
        "source": top[0]["source_id"],
        "confidence": 1.0,
        "conflicts": [],
        "decision": "CONTINUE",
        "actions": ["CLASSIFY_AUTHORITY"],
    })
    return output


def execute_gov_002(envelope: dict[str, Any]) -> dict[str, Any]:
    request = envelope.get("data", {}).get("request")
    if not isinstance(request, dict):
        raise InvalidInput("GOV-002 requires request")
    scope = envelope["context"]["scope"]
    if (
        envelope["skill_id"] in set(scope.get("out_of_scope_skill_ids", []))
        or request.get("target") not in scope.get("allowed_targets", [request.get("target")])
    ):
        raise ScopeViolation("Requested work is outside authorized scope")
    output = base(envelope, "Prevent work outside authorized scope.")
    output.update({"scope_result": "IN_SCOPE", "decision": "CONTINUE", "actions": ["CHECK_SCOPE"]})
    return output


def execute_ctx_001(envelope: dict[str, Any]) -> dict[str, Any]:
    context = envelope["context"]
    output = base(envelope, "Load required current context.")
    missing = [field for field in UNIVERSAL_REQUIRED if not context.get(field)]
    if missing:
        output.update({
            "status": "UNKNOWN",
            "context_result": "INCOMPLETE",
            "unknowns": missing,
            "next_action": "ACQUIRE_MISSING_CONTEXT",
        })
        return output
    output.update({"context_result": "CURRENT_CONTEXT_LOADED", "actions": ["LOAD_CURRENT_STATE"]})
    return output


def execute_ctx_003(envelope: dict[str, Any]) -> dict[str, Any]:
    files = envelope.get("data", {}).get("files")
    if not isinstance(files, list) or not files:
        raise InvalidInput("CTX-003 requires files")
    inspected = []
    for file_entry in files:
        if (
            not isinstance(file_entry, dict)
            or not file_entry.get("path")
            or not file_entry.get("type")
            or not file_entry.get("content_hash")
        ):
            raise InvalidInput("CTX-003 file entries require path, type and content_hash")
        if "content" in file_entry:
            if not isinstance(file_entry["content"], str):
                raise InvalidInput("CTX-003 content must be text")
            expected = str(file_entry["content_hash"]).split(":", 1)[-1]
            if sha256_hex(file_entry["content"].encode("utf-8")) != expected:
                raise IntegrityFailure(f"Content hash mismatch for {file_entry['path']}")
        inspected.append({
            "id": stable_id("FILE", {"path": file_entry["path"], "content_hash": file_entry["content_hash"]}),
            "path": file_entry["path"],
            "type": file_entry["type"],
            "content_hash": file_entry["content_hash"],
            "dependencies": file_entry.get("dependencies", []),
            "callers": file_entry.get("callers", []),
            "callees": file_entry.get("callees", []),
            "contracts": file_entry.get("contracts", []),
            "tests": file_entry.get("tests", []),
        })
    output = base(envelope, "Inspect actual source before deciding.")
    output.update({"inspected_files": inspected, "actions": ["INSPECT_SOURCE"]})
    return output


def execute_req_001(envelope: dict[str, Any]) -> dict[str, Any]:
    requirement = envelope.get("data", {}).get("requirement")
    if not isinstance(requirement, dict):
        raise InvalidInput("REQ-001 requires requirement object")
    required = ["objective", "in_scope", "out_scope", "input", "output", "constraint", "acceptance", "validation"]
    missing = [field for field in required if field not in requirement]
    output = base(envelope, "Translate a command into an explicit requirement contract.")
    if missing:
        output.update({
            "status": "UNKNOWN",
            "requirement_result": "INCOMPLETE",
            "unknowns": missing,
            "next_action": "ACQUIRE_AUTHORITATIVE_DETAIL",
        })
        return output
    output.update({
        "requirement_result": "COMPLETE",
        "requirement": requirement,
        "actions": ["TRANSLATE_COMMAND"],
    })
    return output


def execute_arc_001(envelope: dict[str, Any]) -> dict[str, Any]:
    architecture = envelope.get("data", {}).get("architecture")
    if not isinstance(architecture, dict):
        raise InvalidInput("ARC-001 requires architecture facts")
    missing = [field for field in ("layers", "authority_flow", "boundaries") if field not in architecture]
    output = base(envelope, "Understand actual NEXY architecture before changes.")
    if missing:
        output.update({
            "status": "UNKNOWN",
            "architecture_result": "INCOMPLETE",
            "unknowns": missing,
            "next_action": "INSPECT_MISSING_ARCHITECTURE",
        })
        return output
    output.update({"architecture_result": "INSPECTED", "architecture": architecture, "actions": ["INSPECT_ARCHITECTURE"]})
    return output


def execute_arc_004(envelope: dict[str, Any]) -> dict[str, Any]:
    impact = envelope.get("data", {}).get("impact")
    if not isinstance(impact, dict):
        raise InvalidInput("ARC-004 requires impact facts")
    required = [
        "affected_modules", "affected_contracts", "affected_state",
        "affected_tests", "affected_security", "affected_release",
    ]
    missing = [field for field in required if field not in impact]
    output = base(envelope, "Determine what an architectural change affects.")
    if missing:
        output.update({
            "status": "BLOCKED",
            "unknowns": missing,
            "next_action": "INSPECT_CRITICAL_IMPACT",
        })
        return output
    output.update({
        "AFFECTED_MODULES": impact["affected_modules"],
        "AFFECTED_CONTRACTS": impact["affected_contracts"],
        "AFFECTED_STATE": impact["affected_state"],
        "AFFECTED_TESTS": impact["affected_tests"],
        "AFFECTED_SECURITY": impact["affected_security"],
        "AFFECTED_RELEASE": impact["affected_release"],
        "actions": ["ANALYZE_ARCHITECTURE_IMPACT"],
    })
    return output


class SkillRuntime:
    def __init__(self, registry_path: str | Path = CANONICAL_REGISTRY_PATH):
        self.registry_path = Path(registry_path)
        self.registry = load_registry(self.registry_path)

    def run(self, skill_id: str, envelope: dict[str, Any]) -> dict[str, Any]:
        trace: list[str] = []
        execution_id = envelope.get("execution_id", "UNKNOWN-EXECUTION")
        head = envelope.get("context", {}).get("head", "UNKNOWN")
        entry: RegistryEntry | None = None
        try:
            trace.append("LOAD")
            entry = resolve_entry(self.registry, skill_id)
            envelope = {**envelope, "skill_id": skill_id}

            trace.append("RESOLVE")
            skill_fn = load_callable(entry.runtime_entry)
            validator = load_callable(entry.validator)
            evidence_handler = load_callable(entry.evidence_handler)
            validate_input_contract(envelope)

            trace.append("AUTHORIZE")
            token = authorize(entry, envelope)

            trace.append("EXECUTE")
            output = execute_with_token(token, skill_fn, envelope)

            trace.append("VALIDATE")
            validator(output)
            status = output.get("status", "SUCCESS")
            if status not in {"SUCCESS", "UNKNOWN", "BLOCKED", "FAILURE", "FREEZE"}:
                raise ValidationFailure(f"Unsupported skill status: {status}", True)

            result_id = stable_id(
                "RES",
                {"execution_id": execution_id, "skill_id": skill_id, "head": head, "output": output},
            )

            trace_for_evidence = trace + ["EVIDENCE", "RESULT"]
            validate_trace(trace_for_evidence)
            trace.append("EVIDENCE")
            evidence = evidence_handler(
                execution_id, skill_id, head, trace_for_evidence, envelope, output, result_id, "VERIFIED"
            )
            output = {**output, "evidence": [evidence]}

            trace.append("RESULT")
            validate_trace(trace)
            return self._success(skill_id, execution_id, head, status, output, trace, result_id, evidence)

        except RuntimeFault as fault:
            if fault.code == "MISSING_REQUIRED_INPUT":
                status = "UNKNOWN"
            elif fault.code == "MISSING_SAFETY_CRITICAL_INPUT":
                status = "BLOCKED"
            else:
                status = "FREEZE" if fault.critical else "FAILURE"
            return self._failure(skill_id, execution_id, head, status, fault, trace, entry)
        except Exception as exc:
            unexpected = RuntimeFault(str(exc), "UNEXPECTED_RUNTIME_ERROR", True)
            return self._failure(skill_id, execution_id, head, "FREEZE", unexpected, trace, entry)

    def _success(
        self,
        skill_id: str,
        execution_id: str,
        head: str,
        status: str,
        output: dict[str, Any],
        trace: list[str],
        result_id: str,
        evidence: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "id": result_id,
            "type": "RESULT",
            "status": status,
            "skill_id": skill_id,
            "execution_id": execution_id,
            "source_head": head,
            "runtime_root": RUNTIME_ROOT,
            "runtime_version": RUNTIME_VERSION,
            "repository": REPOSITORY,
            "branch": BRANCH,
            "chain": trace,
            "skill_output": output,
            "evidence_id": evidence["id"],
            "checkpoint": {
                "id": stable_id("CHK", execution_id),
                "expected": 1,
                "processed": 1,
                "verified": 1 if status == "SUCCESS" else 0,
                "failed": 0,
                "skipped": 0,
                "blocked": 1 if status in {"BLOCKED", "FREEZE"} else 0,
                "remaining": 0,
                "current_item": skill_id,
                "resume_point": "NONE" if status == "SUCCESS" else "REVALIDATE",
                "last_verified_source": output.get("inputs", {}).get("source_of_truth", []),
                "last_verified_head": head,
            },
        }

    def _failure(
        self,
        skill_id: str,
        execution_id: str,
        head: str,
        status: str,
        fault: RuntimeFault,
        trace: list[str],
        entry: RegistryEntry | None,
    ) -> dict[str, Any]:
        error_id = stable_id(
            "ERR",
            {
                "execution_id": execution_id,
                "skill_id": skill_id,
                "head": head,
                "code": fault.code,
                "message": str(fault),
            },
        )
        result_id = stable_id(
            "RES",
            {"execution_id": execution_id, "skill_id": skill_id, "status": status, "error": error_id},
        )
        failure = {"id": error_id, "code": fault.code, "message": str(fault)}

        evidence_function: Callable[..., Any] = evidence_bind
        if entry is not None:
            try:
                evidence_function = load_callable(entry.evidence_handler)
            except RuntimeFault:
                evidence_function = evidence_bind

        evidence = evidence_function(
            execution_id,
            skill_id,
            head,
            trace,
            {"execution_id": execution_id, "skill_id": skill_id},
            {"status": status, "failure": failure},
            result_id,
            "VERIFIED",
        )
        return {
            "id": result_id,
            "type": "RESULT",
            "status": status,
            "skill_id": skill_id,
            "execution_id": execution_id,
            "source_head": head,
            "runtime_root": RUNTIME_ROOT,
            "runtime_version": RUNTIME_VERSION,
            "repository": REPOSITORY,
            "branch": BRANCH,
            "chain": trace,
            "failure": failure,
            "evidence_id": evidence["id"],
            "evidence": evidence,
            "checkpoint": {
                "id": stable_id("CHK", execution_id),
                "expected": 1,
                "processed": 1 if trace else 0,
                "verified": 0,
                "failed": 1 if status == "FAILURE" else 0,
                "skipped": 0,
                "blocked": 1 if status == "FREEZE" else 0,
                "remaining": 0,
                "current_item": skill_id,
                "resume_point": "RETRY_AFTER_REVALIDATION" if status == "FREEZE" else "FIX_FAILURE",
                "last_verified_source": [],
                "last_verified_head": head,
            },
        }

    @staticmethod
    def freeze(reason: str, execution_id: str, skill_id: str, head: str) -> dict[str, Any]:
        fault = IntegrityFailure(reason)
        error_id = stable_id(
            "ERR",
            {
                "execution_id": execution_id,
                "skill_id": skill_id,
                "head": head,
                "code": fault.code,
                "message": str(fault),
            },
        )
        result_id = stable_id(
            "RES",
            {"execution_id": execution_id, "skill_id": skill_id, "status": "FREEZE", "error": error_id},
        )
        evidence = evidence_bind(
            execution_id,
            skill_id,
            head,
            ["FREEZE"],
            {"execution_id": execution_id, "skill_id": skill_id},
            {"status": "FREEZE", "failure": {"id": error_id, "code": fault.code, "message": str(fault)}},
            result_id,
            "VERIFIED",
        )
        return {
            "id": result_id,
            "type": "RESULT",
            "status": "FREEZE",
            "skill_id": skill_id,
            "execution_id": execution_id,
            "source_head": head,
            "runtime_root": RUNTIME_ROOT,
            "runtime_version": RUNTIME_VERSION,
            "repository": REPOSITORY,
            "branch": BRANCH,
            "chain": ["FREEZE"],
            "failure": {"id": error_id, "code": fault.code, "message": str(fault)},
            "evidence_id": evidence["id"],
            "evidence": evidence,
            "checkpoint": {
                "id": stable_id("CHK", execution_id),
                "expected": 1,
                "processed": 1,
                "verified": 0,
                "failed": 0,
                "skipped": 0,
                "blocked": 1,
                "remaining": 0,
                "current_item": skill_id,
                "resume_point": "REVALIDATE_SOURCE_AND_HEAD",
                "last_verified_source": [],
                "last_verified_head": head,
            },
        }
