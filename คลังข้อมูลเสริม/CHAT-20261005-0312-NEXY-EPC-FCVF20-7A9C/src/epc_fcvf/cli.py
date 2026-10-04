from __future__ import annotations

import json

from .canonical import canonical_hash
from .engine import initial_state
from .fixtures import evidence_events, keep_event, pins, ready_event
from .modelcheck import execute_trace, explore
from .systems import evaluate_all


def main() -> int:
    state = initial_state(
        chat_id="CHAT-20261005-0312-NEXY-EPC-FCVF20-7A9C",
        candidate_id="EPC-FCVF20",
        candidate_path="คลังข้อมูลเสริม/CHAT-20261005-0312-NEXY-EPC-FCVF20-7A9C",
        pins=pins(),
    )
    trace = (*evidence_events(), ready_event(), keep_event())
    final, results = execute_trace(state, trace)
    findings = evaluate_all(final)
    payload = {
        "accepted": all(r.accepted for r in results),
        "findings_pass": all(f.passed for f in findings),
        "systems": len(findings),
        "state_hash": canonical_hash(final),
        "vote_count": len(final.votes),
        "evidence_coverage_q64_raw": str(final.evidence_coverage_q64().raw),
    }
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0 if payload["accepted"] and payload["findings_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
