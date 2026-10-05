from itertools import permutations
import pytest

from nexy_assurance_fivepack import (
    ActionRisk, AgentVote, Alert, AttentionGovernor, AttentionPolicy,
    CapabilityCandidate, EvidenceClaim, QuorumPolicy, TombstoneRegistry,
    analyze_evidence, evaluate_quorum, plan_assurance,
)

# IAQ

def test_iaq_correlated_replicas_collapse():
    votes = [
        AgentVote("a","PASS","p1","f1",frozenset({"s"}),"t"),
        AgentVote("b","PASS","p1","f1",frozenset({"s"}),"t"),
        AgentVote("c","PASS","p2","f2",frozenset({"x"}),"u"),
    ]
    r = evaluate_quorum(votes, QuorumPolicy(min_independent_clusters=2,min_support_ratio=1))
    assert r.verdict == "PASS" and r.independent_clusters == 2


def test_iaq_fake_quorum_freezes():
    votes=[AgentVote(str(i),"PASS","p","f",frozenset({"s"}),"t") for i in range(4)]
    assert evaluate_quorum(votes, QuorumPolicy(min_independent_clusters=2)).verdict == "FREEZE"


def test_iaq_independent_fail_blocks_default():
    votes=[
        AgentVote("a","PASS","p1","f1",frozenset({"a"}),"t1"),
        AgentVote("b","FAIL","p2","f2",frozenset({"b"}),"t2"),
        AgentVote("c","PASS","p3","f3",frozenset({"c"}),"t3"),
    ]
    assert "independent-failure-present" in evaluate_quorum(votes).reasons


def test_iaq_empty_freezes():
    assert evaluate_quorum([]).verdict == "FREEZE"


def test_iaq_duplicate_agent_rejected():
    v=AgentVote("a","PASS","p","f",frozenset({"s"}),"t")
    with pytest.raises(ValueError): evaluate_quorum([v,v])


@pytest.mark.parametrize(("field", "value"), [
    ("provider", ""),
    ("model_family", "  "),
    ("data_lineage", frozenset()),
    ("data_lineage", frozenset({""})),
    ("toolchain_fingerprint", ""),
])
def test_iaq_missing_independence_metadata_rejected(field, value):
    values = {
        "agent_id": "a",
        "verdict": "PASS",
        "provider": "p",
        "model_family": "f",
        "data_lineage": frozenset({"source"}),
        "toolchain_fingerprint": "t",
    }
    values[field] = value
    with pytest.raises(ValueError, match="independence metadata"):
        AgentVote(**values)


def test_iaq_order_invariant():
    votes=[
        AgentVote("a","PASS","p1","f1",frozenset({"a"}),"t1"),
        AgentVote("b","PASS","p2","f2",frozenset({"b"}),"t2"),
        AgentVote("c","PASS","p1","f1",frozenset({"a"}),"t1"),
    ]
    p=QuorumPolicy(min_independent_clusters=2,min_support_ratio=1)
    baseline=evaluate_quorum(votes,p)
    assert all(evaluate_quorum(x,p)==baseline for x in permutations(votes))

# ECG

def test_ecg_clean_independent_roots():
    c=EvidenceClaim("c",frozenset({"target"}),frozenset({"oracle"}),(("target","root:t"),("oracle","root:o")))
    assert analyze_evidence(c).status == "CLEAN"


def test_ecg_oracle_derived_from_target_contaminated():
    c=EvidenceClaim("c",frozenset({"target"}),frozenset({"oracle"}),(("oracle","target"),))
    assert "oracle-derived-from-target" in analyze_evidence(c).reasons


def test_ecg_shared_untrusted_root_contaminated():
    c=EvidenceClaim("c",frozenset({"target"}),frozenset({"oracle"}),(("target","root"),("oracle","root")))
    assert analyze_evidence(c).status == "CONTAMINATED"


def test_ecg_shared_trusted_root_clean():
    c=EvidenceClaim("c",frozenset({"target"}),frozenset({"oracle"}),(("target","spec"),("oracle","spec")),frozenset({"spec"}))
    assert analyze_evidence(c).status == "CLEAN"


def test_ecg_cycle_indeterminate():
    c=EvidenceClaim("c",frozenset({"target"}),frozenset({"oracle"}),(("target","x"),("x","target")))
    assert analyze_evidence(c).status == "INDETERMINATE"


def test_ecg_direct_overlap_contaminated():
    c=EvidenceClaim("c",frozenset({"same"}),frozenset({"same"}))
    assert "target-oracle-overlap" in analyze_evidence(c).reasons


def test_ecg_edge_order_invariant():
    edges=(("target","t"),("oracle","o"),("x","z"))
    baseline=analyze_evidence(EvidenceClaim("c",frozenset({"target"}),frozenset({"oracle"}),edges))
    assert all(analyze_evidence(EvidenceClaim("c",frozenset({"target"}),frozenset({"oracle"}),e))==baseline for e in permutations(edges))

# RAAS

def test_raas_low_risk_small_evidence():
    assert plan_assurance(ActionRisk(1,0,0,0)).required_evidence in {"E1","E2"}


def test_raas_high_production_promotes_e6():
    p=plan_assurance(ActionRisk(5,4,4,3,production=True))
    assert p.required_evidence == "E6" and p.explicit_confirmation_required and p.independent_quorum_required


def test_raas_irreversible_no_compensation_freezes():
    assert plan_assurance(ActionRisk(5,5,5,5,production=True,compensation_available=False)).disposition == "FREEZE"


def test_raas_permission_change_requires_control_gates():
    p=plan_assurance(ActionRisk(2,1,1,1,permission_change=True))
    assert p.explicit_confirmation_required and p.independent_quorum_required and p.negative_path_tests_required


def test_raas_invalid_scale_rejected():
    with pytest.raises(ValueError): ActionRisk(6,0,0,0)


def test_raas_pure():
    r=ActionRisk(3,2,1,4,production=True)
    first=plan_assurance(r)
    assert all(plan_assurance(r)==first for _ in range(1000))

# CTR

def test_ctr_retirement_blocks_stale_snapshot():
    r=TombstoneRegistry(); r.retire("alpha",10,"unsafe","beta")
    x=r.admit(CapabilityCandidate("alpha",9))
    assert not x.allowed and x.reason == "tombstoned" and x.replacement == "beta"


def test_ctr_newer_snapshot_still_cannot_bypass_active_retirement():
    r=TombstoneRegistry(); r.retire("alpha",10,"unsafe")
    assert not r.admit(CapabilityCandidate("alpha",999)).allowed


def test_ctr_restore_requires_new_epoch():
    r=TombstoneRegistry(); r.retire("alpha",10,"maint")
    with pytest.raises(ValueError): r.restore("alpha",10,"bad")
    r.restore("alpha",11,"reviewed")
    assert not r.admit(CapabilityCandidate("alpha",10)).allowed
    assert r.admit(CapabilityCandidate("alpha",11)).allowed


def test_ctr_replacement_admitted():
    r=TombstoneRegistry(); r.retire("alpha",10,"replaced","beta")
    assert r.admit(CapabilityCandidate("beta",10)).allowed


def test_ctr_self_replacement_rejected():
    r=TombstoneRegistry()
    with pytest.raises(ValueError): r.retire("x",1,"bad","x")


def test_ctr_digest_order_independent_for_unrelated_events():
    a=TombstoneRegistry(); b=TombstoneRegistry()
    a.retire("x",1,"r"); a.retire("y",2,"r")
    b.retire("y",2,"r"); b.retire("x",1,"r")
    assert a.digest()==b.digest()

# AIG

def test_aig_duplicate_low_suppressed():
    g=AttentionGovernor(AttentionPolicy(dedup_window_seconds=300))
    assert g.decide(Alert("k","LOW","e","s",1)).action=="DELIVER"
    assert g.decide(Alert("k","LOW","e","s",2)).action=="SUPPRESS"


def test_aig_changed_critical_state_never_suppressed():
    g=AttentionGovernor(AttentionPolicy(max_noncritical_per_window=0))
    assert g.decide(Alert("k","CRITICAL","e","s1",1)).action=="DELIVER"
    assert g.decide(Alert("k","CRITICAL","e","s2",2)).action=="DELIVER"


@pytest.mark.parametrize("prior_severity", ["LOW", "MEDIUM", "HIGH"])
def test_aig_escalation_to_critical_never_suppressed_as_duplicate(prior_severity):
    g=AttentionGovernor()
    assert g.decide(Alert("k",prior_severity,"e","s",1)).action=="DELIVER"
    decision=g.decide(Alert("k","CRITICAL","e","s",2))
    assert decision.action=="DELIVER"
    assert decision.reason=="critical-severity-escalated"


def test_aig_exact_critical_duplicate_may_suppress():
    g=AttentionGovernor()
    g.decide(Alert("k","CRITICAL","e","s",1))
    assert g.decide(Alert("k","CRITICAL","e","s",2)).action=="SUPPRESS"


def test_aig_budget_coalesces_noncritical_noise():
    g=AttentionGovernor(AttentionPolicy(max_noncritical_per_window=2,budget_window_seconds=60))
    assert g.decide(Alert("a","LOW","e1","s1",1)).action=="DELIVER"
    assert g.decide(Alert("b","MEDIUM","e2","s2",2)).action=="DELIVER"
    assert g.decide(Alert("c","LOW","e3","s3",3)).action=="COALESCE"


def test_aig_new_evidence_is_material():
    g=AttentionGovernor(AttentionPolicy(max_noncritical_per_window=5))
    g.decide(Alert("k","LOW","e1","s",1))
    assert g.decide(Alert("k","LOW","e2","s",2)).action=="DELIVER"


def test_aig_time_regression_rejected():
    g=AttentionGovernor(); g.decide(Alert("a","LOW","e","s",10))
    with pytest.raises(ValueError): g.decide(Alert("b","LOW","e","s",9))

# Cross-system reference flow

def test_integrated_high_risk_flow():
    assurance=plan_assurance(ActionRisk(5,4,4,3,production=True))
    assert assurance.required_evidence == "E6" and assurance.independent_quorum_required
    q=evaluate_quorum([
        AgentVote("a","PASS","p1","f1",frozenset({"a"}),"t1"),
        AgentVote("b","PASS","p2","f2",frozenset({"b"}),"t2"),
    ],QuorumPolicy(min_independent_clusters=2,min_support_ratio=1))
    assert q.verdict == "PASS"
    e=analyze_evidence(EvidenceClaim("deploy",frozenset({"runtime"}),frozenset({"spec"}),(("runtime","observed"),("spec","authority")),frozenset({"authority"})))
    assert e.status == "CLEAN"
    reg=TombstoneRegistry(); assert reg.admit(CapabilityCandidate("executor",42)).allowed
    assert AttentionGovernor().decide(Alert("deploy","HIGH","proof","state",100)).action == "DELIVER"
