from __future__ import annotations

from dataclasses import dataclass

from .common import canonical_digest, require_digest, require_nonempty
from .input_cohesion import CohesionResult
from .interrupt_epoch import EpochToken, InterruptEpochGate
from .multimodal_intent import IntentEquivalenceResult


@dataclass(frozen=True, slots=True)
class InteractionSnapshot:
    session_id: str
    directive_id: str
    epoch: int
    directive_digest: str
    intent_fingerprint: str
    input_binding_fingerprint: str
    policy_hash: str
    snapshot_digest: str


def build_interaction_snapshot(
    epoch_gate: InterruptEpochGate,
    token: EpochToken,
    intent: IntentEquivalenceResult,
    inputs: CohesionResult,
    *,
    policy_hash: str,
) -> InteractionSnapshot:
    epoch_decision = epoch_gate.validate_token(token)
    if not epoch_decision.allowed:
        raise RuntimeError(epoch_decision.code)
    if not intent.allowed:
        raise RuntimeError("INTENT_NOT_APPROVED")
    if not inputs.allowed:
        raise RuntimeError("INPUTS_NOT_APPROVED")
    policy_hash = require_digest("policy_hash", policy_hash)
    require_nonempty("session_id", token.session_id)
    material = {
        "session_id": token.session_id,
        "directive_id": token.directive_id,
        "epoch": token.epoch,
        "directive_digest": token.directive_digest,
        "intent_fingerprint": intent.fingerprint,
        "input_binding_fingerprint": inputs.binding_fingerprint,
        "policy_hash": policy_hash,
    }
    digest = canonical_digest(material)
    return InteractionSnapshot(snapshot_digest=digest, **material)
