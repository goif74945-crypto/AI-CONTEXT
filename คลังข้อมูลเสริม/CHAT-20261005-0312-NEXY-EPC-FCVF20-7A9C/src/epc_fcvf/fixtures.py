from __future__ import annotations

import hashlib

from .model import CourtPins, Disposition, EvidenceKind, EvidenceRef, Event, EventKind, WorkStatus


SPEC_HASH = "b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7"
NEXY_SHA = "9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43"
AI_CONTEXT_SHA = "718a88fb1e252c22f338e39c5d15edb92a264f93"


def h(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def pins() -> CourtPins:
    return CourtPins(
        spec_id="แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx",
        spec_hash=SPEC_HASH,
        nexy_repo="goif74945-crypto/NEXY.AI-",
        nexy_branch="NEXY.ai",
        nexy_commit_sha=NEXY_SHA,
        ai_context_commit_sha=AI_CONTEXT_SHA,
    )


def evidence_events() -> tuple[Event, ...]:
    return (
        Event(EventKind.ATTACH_EVIDENCE, evidence=EvidenceRef(EvidenceKind.SPEC, "spec:02838,05798-05804", h("spec"))),
        Event(EventKind.ATTACH_EVIDENCE, evidence=EvidenceRef(EvidenceKind.CODE, "nexy:vnext-state-matrix,trinity,fixed128", h("code"), NEXY_SHA)),
        Event(EventKind.ATTACH_EVIDENCE, evidence=EvidenceRef(EvidenceKind.AI_CONTEXT, "AI-EXECUTION-KERNEL+rules", h("context"), AI_CONTEXT_SHA)),
        Event(EventKind.ATTACH_EVIDENCE, evidence=EvidenceRef(EvidenceKind.TEST, "local:unittest+modelcheck", h("test"))),
    )


def ready_event() -> Event:
    return Event(EventKind.SET_STATUS, status=WorkStatus.READY)


def keep_event(idx: int = 1) -> Event:
    return Event(
        EventKind.KEEP,
        vote_id=f"VOTE-KEEP-{idx}",
        timestamp=f"2026-10-05T03:{20+idx:02d}:00+07:00",
        reason="Verified constitutional candidate should remain active for further formal promotion review.",
        counterargument="Formal model is bounded and does not prove unmodeled production behavior.",
        final_justification="Keep is advisory only; evidence is complete for this reference package and no authority escalation is granted.",
    )


def cut_event(idx: int = 1) -> Event:
    return Event(
        EventKind.CUT,
        vote_id=f"VOTE-CUT-{idx}",
        timestamp=f"2026-10-05T03:{30+idx:02d}:00+07:00",
        reason="Evidence-backed candidate is superseded within the active proposal set.",
        counterargument="Archival may lose future utility if assumptions change.",
        final_justification="CUT is non-destructive and preserves the artifact as superseded evidence.",
        requested_disposition=Disposition.SUPERSEDED,
    )
