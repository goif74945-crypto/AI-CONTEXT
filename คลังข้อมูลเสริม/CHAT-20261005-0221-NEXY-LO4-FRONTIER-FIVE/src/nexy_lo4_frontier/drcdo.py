from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping

from .common import FrontierInputError, canonicalize, require_text, stable_hash


@dataclass(frozen=True, slots=True)
class ReplayCapsule:
    capsule_id: str
    request: Mapping[str, Any]
    state: Mapping[str, Any]
    policy_hash: str
    tool_manifest: tuple[tuple[str, str], ...]
    deterministic_seed: int


@dataclass(frozen=True, slots=True)
class ReplayResult:
    executor_id: str
    status: str
    output_hash: str | None
    output: Any | None
    error_code: str | None


@dataclass(frozen=True, slots=True)
class DifferentialReport:
    status: str
    capsule_hash: str
    reference_executor: str | None
    divergent_executors: tuple[str, ...]
    results: tuple[ReplayResult, ...]
    fingerprint: str


def canonical_capsule(c: ReplayCapsule) -> ReplayCapsule:
    cid = require_text(c.capsule_id, "capsule_id")
    policy_hash = require_text(c.policy_hash, "policy_hash")
    if len(policy_hash) != 64 or any(ch not in "0123456789abcdef" for ch in policy_hash.lower()):
        raise FrontierInputError("POLICY_HASH_NOT_SHA256_HEX")
    if not isinstance(c.deterministic_seed, int) or c.deterministic_seed < 0:
        raise FrontierInputError("DETERMINISTIC_SEED_INVALID")
    manifest: dict[str, str] = {}
    for pair in c.tool_manifest:
        if not isinstance(pair, tuple) or len(pair) != 2:
            raise FrontierInputError("TOOL_MANIFEST_NOT_PAIR")
        name, version = require_text(pair[0], "tool_name"), require_text(pair[1], "tool_version")
        if name in manifest and manifest[name] != version:
            raise FrontierInputError(f"DUPLICATE_TOOL_VERSION:{name}")
        manifest[name] = version
    request = canonicalize(c.request)
    state = canonicalize(c.state)
    if not isinstance(request, dict) or not isinstance(state, dict):
        raise FrontierInputError("CAPSULE_REQUEST_STATE_MUST_BE_MAPPINGS")
    return ReplayCapsule(cid, request, state, policy_hash.lower(), tuple(sorted(manifest.items())), c.deterministic_seed)


def capsule_hash(c: ReplayCapsule) -> str:
    return stable_hash(canonical_capsule(c))


def run_replay(c: ReplayCapsule, executor_id: str, executor: Callable[[ReplayCapsule], Any]) -> ReplayResult:
    capsule = canonical_capsule(c)
    eid = require_text(executor_id, "executor_id")
    try:
        output = executor(capsule)
        canonical = canonicalize(output)
        return ReplayResult(eid, "PASS", stable_hash(canonical), canonical, None)
    except FrontierInputError:
        raise
    except Exception as exc:  # boundary intentionally converts executor faults into evidence
        return ReplayResult(eid, "FREEZE", None, None, f"EXECUTOR_EXCEPTION:{type(exc).__name__}")


def differential_oracle(c: ReplayCapsule, executors: Mapping[str, Callable[[ReplayCapsule], Any]]) -> DifferentialReport:
    if not executors:
        raise FrontierInputError("NO_EXECUTORS")
    normalized: list[ReplayResult] = []
    for eid in sorted(executors):
        normalized.append(run_replay(c, eid, executors[eid]))
    results = tuple(normalized)
    successful = [r for r in results if r.status == "PASS"]
    if not successful:
        ref = None
        divergent = tuple(r.executor_id for r in results)
        status = "FREEZE"
    else:
        ref = successful[0].executor_id
        ref_hash = successful[0].output_hash
        divergent = tuple(r.executor_id for r in results if r.status != "PASS" or r.output_hash != ref_hash)
        status = "PASS" if not divergent else "FREEZE"
    chash = capsule_hash(c)
    payload = {"status": status, "capsule_hash": chash, "reference": ref, "divergent": divergent, "results": results}
    return DifferentialReport(status, chash, ref, divergent, results, stable_hash(payload))
