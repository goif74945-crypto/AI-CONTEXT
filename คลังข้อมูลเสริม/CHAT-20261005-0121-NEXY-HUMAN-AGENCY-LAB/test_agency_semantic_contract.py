from __future__ import annotations

from dataclasses import replace
from itertools import product
import json
from pathlib import Path
import unittest

from agency_semantic_contract import (
    AuthorityBindingError,
    SemanticContractError,
    SemanticSource,
    StaleFrameError,
    SurfaceEvent,
    SurfaceMode,
    SurfaceResponse,
    apply_surface_event,
    audit_frames,
    compile_semantic_frame,
    reason_presentation,
    source_from_batch,
    source_from_decision,
)
from confirmation_coalescer import InteractionCandidate, coalesce_interactions
from human_agency_lab import AgencyDecisionEngine, Decision, ReasonCode, RequestProfile


ENGINE = AgencyDecisionEngine()
AUTHORITY = "authority-digest-A"
POLICY = "decision-policy-digest-A"
FIXTURE = Path(__file__).parent / "fixtures" / "semantic_scenarios.json"


def frame_for(action_id: str, **values: object):
    request = RequestProfile(action_id=action_id, **values)
    decision = ENGINE.evaluate(request)
    return compile_semantic_frame(
        source_from_decision(
            decision,
            authority_digest=AUTHORITY,
            decision_policy_digest=POLICY,
        )
    )


class ScenarioContractTests(unittest.TestCase):
    def test_reference_scenarios_match_modes_and_events(self) -> None:
        scenarios = json.loads(FIXTURE.read_text(encoding="utf-8"))
        frames = []
        for scenario in scenarios:
            with self.subTest(name=scenario["name"]):
                frame = frame_for(
                    scenario["request"]["action_id"],
                    **{
                        key: value
                        for key, value in scenario["request"].items()
                        if key != "action_id"
                    },
                )
                frames.append(frame)
                self.assertEqual(frame.mode.value, scenario["expected_mode"])
                self.assertEqual(
                    [control.event.value for control in frame.controls],
                    scenario["expected_events"],
                )
        audit = audit_frames(frames)
        self.assertEqual(audit.frames, 4)
        self.assertEqual(audit.modes, {mode.value: 1 for mode in SurfaceMode})
        self.assertEqual(audit.legal_events, 8)

    def test_scenario_audit_is_repeatable(self) -> None:
        frames = (
            frame_for("proceed"),
            frame_for("preview", ambiguity=0.4),
            frame_for("confirm", crosses_auth_boundary=True),
            frame_for(
                "freeze", destructive=True, rollback_available=False, reversibility=0.0
            ),
        )
        self.assertEqual(len({audit_frames(frames).digest for _ in range(100)}), 1)


class ProjectionTests(unittest.TestCase):
    def test_every_reason_code_has_stable_presentation(self) -> None:
        records = [reason_presentation(reason) for reason in ReasonCode]
        self.assertEqual(len(records), len(ReasonCode))
        self.assertEqual(len({record.code for record in records}), len(ReasonCode))
        self.assertTrue(all(record.label and record.summary for record in records))

    def test_unknown_reason_fails_closed(self) -> None:
        with self.assertRaises(SemanticContractError):
            reason_presentation("INVENTED_SUCCESS")

    def test_source_digest_is_exact_decision_digest(self) -> None:
        decision = ENGINE.evaluate(RequestProfile(action_id="preview", ambiguity=0.4))
        source = source_from_decision(
            decision,
            authority_digest=AUTHORITY,
            decision_policy_digest=POLICY,
        )
        self.assertEqual(source.source_digest, decision.digest())
        self.assertEqual(source.action_reasons[0].action_id, decision.action_id)

    def test_confirm_and_freeze_cannot_launder_hard_gate(self) -> None:
        for decision in (Decision.CONFIRM, Decision.FREEZE):
            with self.subTest(decision=decision), self.assertRaises(SemanticContractError):
                SemanticSource(
                    source_digest="source",
                    decision=decision,
                    hard_gate=False,
                    action_reasons=(
                        source_from_decision(
                            ENGINE.evaluate(
                                RequestProfile(action_id="x", ambiguity=0.4)
                            ),
                            authority_digest=AUTHORITY,
                            decision_policy_digest=POLICY,
                        ).action_reasons[0],
                    ),
                    authority_digest=AUTHORITY,
                    decision_policy_digest=POLICY,
                )

    def test_coalesced_batch_preserves_every_action_mapping(self) -> None:
        candidates = []
        for action_id, values in (
            ("a", {"ambiguity": 0.4}),
            ("b", {"confidence": 0.5}),
            ("c", {"scope_breadth": 0.8}),
        ):
            request = RequestProfile(action_id=action_id, **values)
            candidates.append(
                InteractionCandidate(
                    request=request,
                    decision=ENGINE.evaluate(request),
                    authority_digest=AUTHORITY,
                    decision_policy_digest=POLICY,
                    interaction_context="workspace-A",
                )
            )
        batch = coalesce_interactions(candidates).batches[0]
        frame = compile_semantic_frame(source_from_batch(batch))
        self.assertEqual(frame.mode, SurfaceMode.PREVIEW)
        self.assertEqual(
            tuple(item.action_id for item in frame.source.action_reasons),
            ("a", "b", "c"),
        )
        self.assertEqual(frame.source.source_digest, batch.digest())

    def test_frame_digest_changes_with_authority_or_policy(self) -> None:
        frame = frame_for("preview", ambiguity=0.4)
        authority_changed = replace(
            frame,
            source=replace(frame.source, authority_digest="authority-digest-B"),
        )
        policy_changed = replace(
            frame,
            source=replace(frame.source, decision_policy_digest="policy-digest-B"),
        )
        self.assertNotEqual(frame.digest(), authority_changed.digest())
        self.assertNotEqual(frame.digest(), policy_changed.digest())


class EventSafetyTests(unittest.TestCase):
    def test_stale_response_is_rejected(self) -> None:
        frame = frame_for("confirm", crosses_auth_boundary=True)
        with self.assertRaises(StaleFrameError):
            apply_surface_event(
                frame,
                SurfaceResponse("stale", SurfaceEvent.APPROVE, AUTHORITY),
            )

    def test_approval_authority_must_match(self) -> None:
        frame = frame_for("confirm", crosses_auth_boundary=True)
        with self.assertRaises(AuthorityBindingError):
            apply_surface_event(
                frame,
                SurfaceResponse(frame.digest(), SurfaceEvent.APPROVE, "other"),
            )

    def test_approval_is_request_not_execution_authority(self) -> None:
        frame = frame_for("confirm", crosses_auth_boundary=True)
        record = apply_surface_event(
            frame,
            SurfaceResponse(frame.digest(), SurfaceEvent.APPROVE, AUTHORITY),
        )
        self.assertTrue(record.backend_authorization_required)
        self.assertFalse(record.execution_authorized)
        self.assertEqual(record.source_digest, frame.source.source_digest)

    def test_remediation_request_is_bound_and_non_executing(self) -> None:
        frame = frame_for(
            "freeze", destructive=True, rollback_available=False, reversibility=0.0
        )
        record = apply_surface_event(
            frame,
            SurfaceResponse(
                frame.digest(), SurfaceEvent.REQUEST_REMEDIATION, AUTHORITY
            ),
        )
        self.assertTrue(record.backend_authorization_required)
        self.assertFalse(record.execution_authorized)

    def test_full_mode_event_grid_accepts_only_declared_controls(self) -> None:
        frames = {
            SurfaceMode.SILENT: frame_for("proceed"),
            SurfaceMode.PREVIEW: frame_for("preview", ambiguity=0.4),
            SurfaceMode.CONFIRM: frame_for("confirm", crosses_auth_boundary=True),
            SurfaceMode.FREEZE: frame_for(
                "freeze", destructive=True, rollback_available=False, reversibility=0.0
            ),
        }
        accepted = 0
        rejected = 0
        for mode, event in product(SurfaceMode, SurfaceEvent):
            frame = frames[mode]
            legal = event in {control.event for control in frame.controls}
            response = SurfaceResponse(frame.digest(), event, AUTHORITY)
            if legal:
                apply_surface_event(frame, response)
                accepted += 1
            else:
                with self.assertRaises(SemanticContractError):
                    apply_surface_event(frame, response)
                rejected += 1
        self.assertEqual(accepted, 8)
        self.assertEqual(rejected, 16)


class AbstractAccessibilityTests(unittest.TestCase):
    def test_controls_have_unique_keyboard_order_and_non_color_cues(self) -> None:
        frames = (
            frame_for("proceed"),
            frame_for("preview", ambiguity=0.4),
            frame_for("confirm", crosses_auth_boundary=True),
            frame_for(
                "freeze", destructive=True, rollback_available=False, reversibility=0.0
            ),
        )
        for frame in frames:
            with self.subTest(mode=frame.mode):
                events = tuple(control.event.value for control in frame.controls)
                self.assertEqual(frame.accessibility.keyboard_order, events)
                self.assertEqual(len(events), len(set(events)))
                self.assertIn("text", frame.accessibility.non_color_cues)
                self.assertTrue(frame.accessibility.surface_role)
                self.assertTrue(frame.accessibility.initial_focus)

    def test_freeze_has_no_approve_or_dismiss_semantics(self) -> None:
        frame = frame_for(
            "freeze", destructive=True, rollback_available=False, reversibility=0.0
        )
        events = {control.event for control in frame.controls}
        self.assertNotIn(SurfaceEvent.APPROVE, events)
        self.assertNotIn(SurfaceEvent.ACKNOWLEDGE, events)
        self.assertNotIn(SurfaceEvent.CANCEL, events)
        self.assertEqual(frame.accessibility.escape_behavior, "NO_DISMISS")


if __name__ == "__main__":
    unittest.main()
