"""Metamorphic Verification Forge (MVF).

Metamorphic verification is useful when an exact expected output (oracle) is
unavailable but a relation between outputs is knowable. The verifier records a
compact deterministic witness for every relation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, Iterable, TypeVar

I = TypeVar("I")
O = TypeVar("O")


@dataclass(frozen=True, slots=True)
class MetamorphicRelation(Generic[I, O]):
    relation_id: str
    transform: Callable[[I], I]
    holds: Callable[[I, I, O, O], bool]
    description: str = ""

    def __post_init__(self) -> None:
        if not self.relation_id.strip():
            raise ValueError("relation_id must be non-empty")


@dataclass(frozen=True, slots=True)
class RelationWitness:
    relation_id: str
    status: str
    detail: str


@dataclass(frozen=True, slots=True)
class MetamorphicResult:
    status: str
    witnesses: tuple[RelationWitness, ...]


def verify_metamorphic(
    system_under_test: Callable[[I], O],
    base_input: I,
    relations: Iterable[MetamorphicRelation[I, O]],
) -> MetamorphicResult:
    relation_list = tuple(sorted(relations, key=lambda relation: relation.relation_id))
    if not relation_list:
        raise ValueError("at least one metamorphic relation is required")
    if len({relation.relation_id for relation in relation_list}) != len(relation_list):
        raise ValueError("relation_id values must be unique")

    witnesses: list[RelationWitness] = []
    try:
        base_output = system_under_test(base_input)
    except Exception as exc:
        detail = f"base execution raised {type(exc).__name__}: {exc}"
        return MetamorphicResult(
            status="FAIL",
            witnesses=tuple(
                RelationWitness(relation.relation_id, "FAIL", detail)
                for relation in relation_list
            ),
        )

    for relation in relation_list:
        try:
            transformed_input = relation.transform(base_input)
            transformed_output = system_under_test(transformed_input)
            passed = bool(
                relation.holds(base_input, transformed_input, base_output, transformed_output)
            )
            witnesses.append(
                RelationWitness(
                    relation_id=relation.relation_id,
                    status="PASS" if passed else "FAIL",
                    detail=relation.description or "metamorphic relation evaluated",
                )
            )
        except Exception as exc:  # exception itself is decisive negative evidence
            witnesses.append(
                RelationWitness(
                    relation_id=relation.relation_id,
                    status="FAIL",
                    detail=f"relation raised {type(exc).__name__}: {exc}",
                )
            )

    overall = "PASS" if all(w.status == "PASS" for w in witnesses) else "FAIL"
    return MetamorphicResult(status=overall, witnesses=tuple(witnesses))
