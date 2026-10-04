from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .collision import WorkManifest
from .models import Proposal, ProposalValidationError


def load_json(path: str | Path) -> Any:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_proposal(path: str | Path) -> Proposal:
    return Proposal.from_dict(load_json(path))


def load_catalog(path: str | Path | None) -> tuple[Proposal, ...]:
    if path is None:
        return ()
    data = load_json(path)
    if not isinstance(data, list):
        raise ProposalValidationError(["catalog: required JSON array"])
    proposals: list[Proposal] = []
    errors: list[str] = []
    seen_ids: set[str] = set()
    for index, item in enumerate(data):
        try:
            proposal = Proposal.from_dict(item)
        except ProposalValidationError as exc:
            errors.extend(f"catalog[{index}].{message}" for message in exc.errors)
            continue
        if proposal.proposal_id in seen_ids:
            errors.append(f"catalog[{index}].proposal_id: duplicate id {proposal.proposal_id!r}")
            continue
        seen_ids.add(proposal.proposal_id)
        proposals.append(proposal)
    if errors:
        raise ProposalValidationError(errors)
    return tuple(proposals)


def load_work_manifest(path: str | Path) -> WorkManifest:
    return WorkManifest.from_dict(load_json(path))


def load_work_manifest_catalog(path: str | Path) -> tuple[WorkManifest, ...]:
    data = load_json(path)
    if not isinstance(data, list):
        raise ProposalValidationError(["work manifest catalog: required JSON array"])
    manifests: list[WorkManifest] = []
    errors: list[str] = []
    seen: set[str] = set()
    for index, item in enumerate(data):
        try:
            manifest = WorkManifest.from_dict(item)
        except ProposalValidationError as exc:
            errors.extend(f"work_catalog[{index}].{message}" for message in exc.errors)
            continue
        if manifest.execution_id in seen:
            errors.append(f"work_catalog[{index}].execution_id: duplicate id {manifest.execution_id!r}")
            continue
        seen.add(manifest.execution_id)
        manifests.append(manifest)
    if errors:
        raise ProposalValidationError(errors)
    return tuple(manifests)
