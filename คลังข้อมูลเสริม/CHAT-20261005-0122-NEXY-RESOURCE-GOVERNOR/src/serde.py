from __future__ import annotations

from typing import Any, Mapping

from .models import AgentProfile, DataClass, RiskTier, TaskProfile


def agent_from_mapping(data: Mapping[str, Any]) -> AgentProfile:
    return AgentProfile(
        agent_id=str(data["agent_id"]),
        provider_domain=str(data["provider_domain"]),
        roles=frozenset(str(item) for item in data["roles"]),
        capabilities=frozenset(str(item) for item in data.get("capabilities", [])),
        clearance=DataClass(str(data["clearance"])),
        max_context_tokens=int(data["max_context_tokens"]),
        input_cost_microunits_per_1k=int(data["input_cost_microunits_per_1k"]),
        output_cost_microunits_per_1k=int(data["output_cost_microunits_per_1k"]),
        estimated_latency_ms=int(data["estimated_latency_ms"]),
        quality_bps=int(data["quality_bps"]),
        max_evidence_class=int(data["max_evidence_class"]),
        active=bool(data.get("active", True)),
        quarantined=bool(data.get("quarantined", False)),
    )


def task_from_mapping(data: Mapping[str, Any]) -> TaskProfile:
    def optional_int(name: str) -> int | None:
        value = data.get(name)
        return None if value is None else int(value)

    return TaskProfile(
        task_id=str(data["task_id"]),
        required_capabilities=frozenset(str(item) for item in data.get("required_capabilities", [])),
        data_class=DataClass(str(data["data_class"])),
        risk_tier=RiskTier(str(data["risk_tier"])),
        required_evidence_class=int(data["required_evidence_class"]),
        worker_input_tokens=int(data["worker_input_tokens"]),
        worker_output_tokens=int(data["worker_output_tokens"]),
        verifier_input_tokens=int(data.get("verifier_input_tokens", 0)),
        verifier_output_tokens=int(data.get("verifier_output_tokens", 0)),
        require_independent_verifier=bool(data.get("require_independent_verifier", False)),
        min_quality_bps=int(data.get("min_quality_bps", 0)),
        max_total_tokens=optional_int("max_total_tokens"),
        max_cost_microunits=optional_int("max_cost_microunits"),
        max_latency_ms=optional_int("max_latency_ms"),
    )
