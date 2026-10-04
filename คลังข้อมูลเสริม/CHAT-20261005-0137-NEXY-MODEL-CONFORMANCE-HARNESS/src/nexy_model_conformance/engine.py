from __future__ import annotations

from typing import Any, Iterable, Mapping

from .canonical import canonical_json, sha256_hex
from .errors import ContractError
from .jsonpath import resolve_path
from .model import CaseContract, Finding, Invariant, Observation, ProviderManifest, Report, Status

_SENSITIVE_KEYS = {
    "access_token", "api_key", "apikey", "client_secret", "authorization",
    "cookie", "password", "private_key", "refresh_token", "secret",
    "session_token", "token", "x_api_key",
}
_TYPE_NAMES: dict[str, tuple[type, ...]] = {
    "null": (type(None),), "string": (str,), "boolean": (bool,),
    "integer": (int,), "number": (int, float), "object": (dict,), "array": (list,),
}
_STATUS_PRIORITY = {
    Status.PASS: 0, Status.NOT_VERIFIED: 1, Status.PARTIAL: 2, Status.UNKNOWN: 3,
    Status.BLOCKED: 4, Status.FAIL: 5, Status.CONFLICT: 6,
}

class ConformanceEngine:
    """Provider-neutral, fail-closed conformance evaluator."""

    def __init__(self, *, max_observations: int = 64, max_document_bytes: int = 1_048_576) -> None:
        if max_observations < 1 or max_document_bytes < 1024:
            raise ValueError("invalid engine resource bounds")
        self.max_observations = max_observations
        self.max_document_bytes = max_document_bytes

    def verify(self, manifest: ProviderManifest, case: CaseContract, observations: Iterable[Observation]) -> Report:
        obs = tuple(observations)
        findings: list[Finding] = []
        if len(obs) > self.max_observations:
            findings.append(Finding("OBSERVATION_LIMIT_EXCEEDED", Status.FAIL, f"maximum {self.max_observations} observations allowed; got {len(obs)}"))
            obs = ()
        if self._encoded_size(case.request) > self.max_document_bytes:
            findings.append(Finding("REQUEST_SIZE_LIMIT_EXCEEDED", Status.FAIL, f"canonical request exceeds {self.max_document_bytes} bytes"))
            obs = ()
        missing_caps = sorted(case.required_capabilities - manifest.capabilities)
        if missing_caps:
            findings.append(Finding("CAPABILITY_MISSING", Status.FAIL, f"manifest lacks required capabilities: {', '.join(missing_caps)}"))

        request_hash = sha256_hex(case.request)
        relevant: list[Observation] = []
        seen_ids: set[str] = set()
        for item in obs:
            if item.observation_id in seen_ids:
                findings.append(Finding("DUPLICATE_OBSERVATION_ID", Status.FAIL, "observation_id must be unique", item.observation_id))
                continue
            seen_ids.add(item.observation_id)
            if item.case_id != case.case_id:
                findings.append(Finding("CASE_ID_MISMATCH", Status.FAIL, f"expected case_id {case.case_id!r}, got {item.case_id!r}", item.observation_id))
                continue
            if item.provider_ref != manifest.ref:
                findings.append(Finding("PROVIDER_REF_MISMATCH", Status.FAIL, f"expected provider_ref {manifest.ref!r}, got {item.provider_ref!r}", item.observation_id))
                continue
            if item.request_hash != request_hash:
                findings.append(Finding("REQUEST_HASH_MISMATCH", Status.FAIL, "observation is not bound to the case request", item.observation_id))
                continue
            payload = {"output": item.output, "evidence": list(item.evidence), "adapter_meta": dict(item.adapter_meta)}
            if self._encoded_size(payload) > self.max_document_bytes:
                findings.append(Finding("OBSERVATION_SIZE_LIMIT_EXCEEDED", Status.FAIL, f"canonical observation payload exceeds {self.max_document_bytes} bytes", item.observation_id))
                continue
            relevant.append(item)

        if len(relevant) < case.min_observations:
            findings.append(Finding("OBSERVATION_COUNT_INSUFFICIENT", Status.NOT_VERIFIED, f"need at least {case.min_observations}, observed {len(relevant)} valid observations"))
        for item in relevant:
            for invariant in case.invariants:
                finding = self._evaluate_invariant(invariant, item)
                if finding is not None:
                    findings.append(finding)
        findings.extend(self._verify_replay_stability(case, relevant))
        status = self._aggregate(findings)
        fingerprint_payload = {
            "case_id": case.case_id,
            "provider_ref": manifest.ref,
            "observation_hashes": [self._observation_hash(item) for item in relevant],
            "finding_codes": sorted((f.code, f.status.value, f.observation_id, f.path) for f in findings),
        }
        return Report(case.case_id, manifest.ref, status, tuple(findings), sha256_hex(fingerprint_payload), len(relevant))

    def compare_reports(self, case: CaseContract, observations_by_provider: Mapping[str, Iterable[Observation]]) -> tuple[Status, tuple[Finding, ...]]:
        findings: list[Finding] = []
        if not case.cross_provider_paths:
            return Status.NOT_VERIFIED, (Finding("NO_CROSS_PROVIDER_PATHS", Status.NOT_VERIFIED, "case declares no cross-provider equivalence paths"),)
        request_hash = sha256_hex(case.request)
        snapshots: dict[str, dict[str, Any]] = {}
        for provider_ref, observations in observations_by_provider.items():
            obs = tuple(observations)
            if len(obs) > self.max_observations:
                findings.append(Finding("OBSERVATION_LIMIT_EXCEEDED", Status.FAIL, f"{provider_ref} supplied {len(obs)} observations; limit is {self.max_observations}"))
                continue
            if not obs:
                findings.append(Finding("PROVIDER_OBSERVATION_MISSING", Status.NOT_VERIFIED, f"no observations for {provider_ref}"))
                continue
            valid: list[Observation] = []
            for item in obs:
                if item.provider_ref != provider_ref:
                    findings.append(Finding("PROVIDER_GROUP_MISMATCH", Status.FAIL, f"observation provider_ref does not match group {provider_ref}", item.observation_id))
                    continue
                if item.case_id != case.case_id:
                    findings.append(Finding("CASE_ID_MISMATCH", Status.FAIL, f"cross-provider observation is for {item.case_id!r}, expected {case.case_id!r}", item.observation_id))
                    continue
                if item.request_hash != request_hash:
                    findings.append(Finding("REQUEST_HASH_MISMATCH", Status.FAIL, "cross-provider observation is not bound to the case request", item.observation_id))
                    continue
                valid.append(item)
            if not valid:
                continue
            item = valid[0]
            values: dict[str, Any] = {}
            for path in case.cross_provider_paths:
                exists, value = resolve_path(item.output, path)
                if not exists:
                    findings.append(Finding("CROSS_PROVIDER_PATH_MISSING", Status.FAIL, f"required comparison path missing for {provider_ref}", item.observation_id, path))
                else:
                    values[path] = value
            snapshots[provider_ref] = values
        provider_refs = sorted(snapshots)
        if len(provider_refs) < 2:
            findings.append(Finding("CROSS_PROVIDER_SAMPLE_INSUFFICIENT", Status.NOT_VERIFIED, "cross-provider comparison requires at least two valid providers"))
        else:
            baseline_ref = provider_refs[0]
            baseline = snapshots[baseline_ref]
            for provider_ref in provider_refs[1:]:
                current = snapshots[provider_ref]
                for path in case.cross_provider_paths:
                    if path in baseline and path in current and baseline[path] != current[path]:
                        findings.append(Finding("CROSS_PROVIDER_CONFLICT", Status.CONFLICT, f"{provider_ref} differs from baseline {baseline_ref}", path=path))
        return self._aggregate(findings), tuple(findings)

    def _evaluate_invariant(self, invariant: Invariant, observation: Observation) -> Finding | None:
        if invariant.kind == "min_evidence":
            threshold = invariant.minimum
            if not isinstance(threshold, int) or isinstance(threshold, bool) or threshold < 0:
                raise ContractError("min_evidence.minimum must be a non-negative integer")
            if len(observation.evidence) < threshold:
                return Finding("EVIDENCE_MINIMUM_NOT_MET", Status.FAIL, f"requires >= {threshold} evidence records; got {len(observation.evidence)}", observation.observation_id)
            return None
        if invariant.kind == "no_sensitive_keys":
            sensitive = sorted(self._find_sensitive_keys(observation.output))
            if sensitive:
                return Finding("SENSITIVE_KEY_PRESENT", Status.FAIL, f"output contains forbidden sensitive-looking keys: {', '.join(sensitive)}", observation.observation_id)
            return None
        exists, value = resolve_path(observation.output, invariant.path)
        if invariant.kind == "exists":
            return None if exists else self._path_failure("PATH_MISSING", observation, invariant.path, "required path is missing")
        if not exists:
            return self._path_failure("PATH_MISSING", observation, invariant.path, "invariant target path is missing")
        if invariant.kind == "equals":
            return None if value == invariant.value else self._path_failure("VALUE_MISMATCH", observation, invariant.path, f"expected {invariant.value!r}, got {value!r}")
        if invariant.kind == "one_of":
            return None if value in invariant.values else self._path_failure("VALUE_OUTSIDE_ALLOWED_SET", observation, invariant.path, f"value {value!r} not in declared allowed set")
        if invariant.kind == "type":
            expected = invariant.value
            if not isinstance(expected, str) or expected not in _TYPE_NAMES:
                raise ContractError(f"unsupported invariant type name: {expected!r}")
            ok = False if isinstance(value, bool) and expected in {"integer", "number"} else isinstance(value, _TYPE_NAMES[expected])
            return None if ok else self._path_failure("TYPE_MISMATCH", observation, invariant.path, f"expected {expected}, got {type(value).__name__}")
        if invariant.kind == "range":
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                return self._path_failure("RANGE_TYPE_INVALID", observation, invariant.path, "range target is not numeric")
            if invariant.minimum is not None and value < invariant.minimum:
                return self._path_failure("RANGE_UNDERFLOW", observation, invariant.path, "value is below minimum")
            if invariant.maximum is not None and value > invariant.maximum:
                return self._path_failure("RANGE_OVERFLOW", observation, invariant.path, "value is above maximum")
            return None
        raise ContractError(f"unhandled invariant kind: {invariant.kind}")

    def _verify_replay_stability(self, case: CaseContract, observations: list[Observation]) -> list[Finding]:
        findings: list[Finding] = []
        if len(observations) < 2 or not case.deterministic_paths:
            return findings
        baseline = observations[0]
        for current in observations[1:]:
            for path in case.deterministic_paths:
                a_exists, a_value = resolve_path(baseline.output, path)
                b_exists, b_value = resolve_path(current.output, path)
                if a_exists != b_exists or (a_exists and a_value != b_value):
                    findings.append(Finding("DETERMINISTIC_REPLAY_CONFLICT", Status.CONFLICT, f"deterministic path diverged from baseline {baseline.observation_id}", current.observation_id, path))
        return findings

    @staticmethod
    def _encoded_size(value: Any) -> int:
        return len(canonical_json(value).encode("utf-8"))

    @staticmethod
    def _observation_hash(observation: Observation) -> str:
        return sha256_hex({
            "observation_id": observation.observation_id,
            "case_id": observation.case_id,
            "provider_ref": observation.provider_ref,
            "request_hash": observation.request_hash,
            "output": observation.output,
            "evidence": list(observation.evidence),
            "trace_id": observation.trace_id,
            "error_code": observation.error_code,
            "adapter_meta": dict(observation.adapter_meta),
        })

    @staticmethod
    def _path_failure(code: str, observation: Observation, path: str, message: str) -> Finding:
        return Finding(code, Status.FAIL, message, observation.observation_id, path)

    @classmethod
    def _find_sensitive_keys(cls, value: Any, prefix: str = "") -> set[str]:
        found: set[str] = set()
        if isinstance(value, dict):
            for key, item in value.items():
                normalized = key.lower().replace("-", "_")
                path = f"{prefix}.{key}" if prefix else key
                if normalized in _SENSITIVE_KEYS:
                    found.add(path)
                found.update(cls._find_sensitive_keys(item, path))
        elif isinstance(value, list):
            for index, item in enumerate(value):
                path = f"{prefix}.{index}" if prefix else str(index)
                found.update(cls._find_sensitive_keys(item, path))
        return found

    @staticmethod
    def _aggregate(findings: Iterable[Finding]) -> Status:
        findings = tuple(findings)
        if not findings:
            return Status.PASS
        return max((finding.status for finding in findings), key=lambda s: _STATUS_PRIORITY[s])
