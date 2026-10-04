from __future__ import annotations

from dataclasses import dataclass

from .common import Verdict, canonical_hash


@dataclass(frozen=True)
class SkillNode:
    skill_id: str
    prerequisites: tuple[str, ...]
    action: str
    evidence: str


@dataclass(frozen=True)
class MasteryRequest:
    goal_skill: str
    declared_known_skills: frozenset[str]
    max_steps: int = 20


def compile_path(request: MasteryRequest, nodes: tuple[SkillNode, ...]) -> dict:
    if not request.goal_skill.strip() or request.max_steps < 0:
        return {"verdict": Verdict.FREEZE.value, "reason_codes": ["INVALID_REQUEST"], "steps": []}
    node_map = {n.skill_id: n for n in nodes}
    if len(node_map) != len(nodes):
        return {"verdict": Verdict.FREEZE.value, "reason_codes": ["DUPLICATE_SKILL_ID"], "steps": []}
    if request.goal_skill not in node_map and request.goal_skill not in request.declared_known_skills:
        return {"verdict": Verdict.FREEZE.value, "reason_codes": ["UNKNOWN_GOAL_SKILL"], "steps": []}

    unknown_known = sorted(request.declared_known_skills - set(node_map))
    if unknown_known:
        return {
            "verdict": Verdict.FREEZE.value,
            "reason_codes": ["UNKNOWN_DECLARED_KNOWLEDGE"],
            "unknown_skills": unknown_known,
            "steps": [],
        }

    ordered: list[str] = []
    visiting: list[str] = []
    visited: set[str] = set(request.declared_known_skills)
    missing_refs: set[str] = set()
    cycle: list[str] = []

    def visit(skill: str) -> None:
        nonlocal cycle
        if cycle or skill in visited:
            return
        if skill in visiting:
            idx = visiting.index(skill)
            cycle = visiting[idx:] + [skill]
            return
        node = node_map.get(skill)
        if node is None:
            missing_refs.add(skill)
            return
        visiting.append(skill)
        for prereq in sorted(node.prerequisites):
            visit(prereq)
        visiting.pop()
        if not cycle and skill not in visited:
            visited.add(skill)
            ordered.append(skill)

    visit(request.goal_skill)
    reasons: list[str] = []
    if missing_refs:
        reasons.append("MISSING_PREREQUISITE_DEFINITION")
    if cycle:
        reasons.append("PREREQUISITE_CYCLE")
    if len(ordered) > request.max_steps:
        reasons.append("STEP_BUDGET_EXCEEDED")

    steps = [
        {
            "skill_id": skill,
            "action": node_map[skill].action,
            "evidence": node_map[skill].evidence,
        }
        for skill in ordered[: request.max_steps]
    ] if not reasons else []

    result = {
        "verdict": Verdict.FREEZE.value if reasons else Verdict.PASS.value,
        "reason_codes": sorted(reasons),
        "steps": steps,
        "missing_prerequisites": sorted(missing_refs),
        "cycle": cycle,
        "declared_known_skills": sorted(request.declared_known_skills),
    }
    result["fingerprint"] = canonical_hash({"request": request, "nodes": sorted(nodes, key=lambda n: n.skill_id), "result": result})
    return result
