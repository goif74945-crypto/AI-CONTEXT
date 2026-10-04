from __future__ import annotations

from typing import Callable, Mapping

from .contracts import ConceptSpec, Evaluation, band, validate_inputs
from .q64 import HALF, ONE, Q64, max_q, min_q, ratio01, weighted_mean

Evaluator = Callable[[Mapping[str, Q64]], tuple[Q64, Q64, tuple[str, ...]]]


def _wm(*pairs: tuple[Q64, int]) -> Q64:
    return weighted_mean(tuple(pairs))


def _opportunity_cost(v: Mapping[str, Q64]):
    readiness = _wm((v["expected_value"], 4), (v["reversibility"], 2), (v["deadline_slack"], 2), (v["alternative_cost"].complement01(), 3))
    confidence = _wm((v["evidence_strength"], 3), (v["estimate_stability"], 2))
    return readiness, confidence, ("VALUE_VS_ALTERNATIVE", "REVERSIBILITY_WEIGHTED")


def _uncertainty_tomograph(v):
    concentrated_risk = max_q(v["model_uncertainty"], v["data_uncertainty"], v["policy_uncertainty"])
    coverage = min_q(v["observability"], v["counterexample_coverage"])
    readiness = _wm((concentrated_risk.complement01(), 4), (coverage, 4), (v["localizability"], 2))
    confidence = _wm((v["observability"], 3), (v["counterexample_coverage"], 3))
    return readiness, confidence, ("UNCERTAINTY_HOTSPOT", "COVERAGE_FLOOR")


def _voi_planner(v):
    info_gain = ratio01(v["uncertainty_reduction"], v["verification_cost"])
    timing = ratio01(v["decision_impact"], v["latency_penalty"])
    readiness = _wm((info_gain, 5), (timing, 3), (v["reusability"], 2))
    confidence = _wm((v["measurement_reliability"], 4), (v["decision_impact"], 1))
    return readiness, confidence, ("MARGINAL_INFORMATION_GAIN", "MEASUREMENT_RELIABILITY")


def _freeze_granularity(v):
    containment = ratio01(v["fault_locality"], v["blast_radius"])
    preservation = _wm((v["safe_progress_fraction"], 4), (v["rollback_precision"], 3), (containment, 3))
    confidence = _wm((v["fault_attribution"], 3), (v["rollback_precision"], 2))
    return preservation, confidence, ("MINIMUM_SAFE_FREEZE", "BLAST_RADIUS_AWARE")


def _decision_half_life(v):
    freshness = v["environment_stability"]
    durability = _wm((freshness, 3), (v["assumption_durability"], 3), (v["evidence_refreshability"], 2), (v["change_detection"], 2))
    confidence = _wm((v["change_detection"], 4), (v["evidence_refreshability"], 1))
    return durability, confidence, ("DECISION_TTL", "CHANGE_SENSITIVE")


def _tool_hedge(v):
    failover = min_q(v["provider_diversity"], v["semantic_equivalence"], v["state_portability"])
    economic = v["switch_cost"].complement01()
    readiness = _wm((failover, 5), (economic, 2), (v["health_observability"], 3))
    confidence = _wm((v["semantic_equivalence"], 3), (v["health_observability"], 2))
    return readiness, confidence, ("HEDGED_EXECUTION", "EQUIVALENCE_FLOOR")


def _interruption_merge(v):
    compatibility = v["new_intent_compatibility"]
    salvage = _wm((v["completed_work_reuse"], 3), (v["checkpoint_quality"], 3), (compatibility, 4))
    penalty = v["mutation_conflict"]
    readiness = _wm((salvage, 4), (penalty.complement01(), 3))
    confidence = _wm((v["checkpoint_quality"], 3), (v["intent_parse_confidence"], 3))
    return readiness, confidence, ("INTERRUPTION_SAFE_MERGE", "WORK_SALVAGE")


def _outcome_slo(v):
    service_margin = min_q(v["latency_margin"], v["quality_margin"], v["cost_margin"], v["reliability_margin"])
    readiness = _wm((service_margin, 6), (v["degradation_plan_quality"], 4))
    confidence = _wm((v["telemetry_quality"], 4), (v["degradation_plan_quality"], 1))
    return readiness, confidence, ("SLO_MIN_MARGIN", "DEGRADED_MODE_READY")


def _counterexample_reservoir(v):
    diversity = min_q(v["semantic_diversity"], v["boundary_diversity"], v["historical_diversity"])
    yield_score = ratio01(v["failure_discovery_rate"], v["maintenance_cost"])
    readiness = _wm((diversity, 4), (yield_score, 4), (v["replayability"], 2))
    confidence = _wm((v["replayability"], 3), (v["label_quality"], 3))
    return readiness, confidence, ("COUNTEREXAMPLE_DIVERSITY", "REPLAYABLE_FAILURE_MEMORY")


def _regret_bound(v):
    downside = max_q(v["irreversibility"], v["harm_severity"], v["uncertainty"])
    option_value = _wm((v["optionality"], 3), (v["learning_value"], 3), (v["delay_tolerance"], 2))
    readiness = _wm((downside.complement01(), 5), (option_value, 5))
    confidence = _wm((v["loss_bound_confidence"], 5), (v["uncertainty"].complement01(), 1))
    return readiness, confidence, ("BOUNDED_REGRET", "OPTION_VALUE")


def _cognitive_bandwidth(v):
    comprehension = min_q(v["information_clarity"], v["decision_salience"], v["attention_fit"])
    burden = max_q(v["notification_load"], v["choice_overload"])
    readiness = _wm((comprehension, 5), (burden.complement01(), 4), (v["progressive_disclosure"], 2))
    confidence = _wm((v["user_feedback_signal"], 3), (v["attention_fit"], 2))
    return readiness, confidence, ("COGNITIVE_LOAD_BOUND", "DECISION_SALIENCE")


def _proof_reuse(v):
    reuse = min_q(v["premise_match"], v["environment_match"], v["version_match"])
    savings = ratio01(v["verification_cost_saved"], v["reuse_validation_cost"])
    readiness = _wm((reuse, 5), (savings, 3), (v["lineage_integrity"], 4))
    confidence = _wm((v["lineage_integrity"], 5), (v["version_match"], 2))
    return readiness, confidence, ("PROOF_REUSE_ELIGIBILITY", "LINEAGE_GATED")


def _containment_radius(v):
    isolation = _wm((v["dependency_isolation"], 3), (v["state_partitioning"], 3), (v["rollback_scope_precision"], 3))
    propagation = max_q(v["side_effect_fanout"], v["shared_state_coupling"])
    readiness = _wm((isolation, 5), (propagation.complement01(), 4))
    confidence = _wm((v["dependency_map_quality"], 4), (v["rollback_scope_precision"], 2))
    return readiness, confidence, ("CONTAINMENT_RADIUS", "DEPENDENCY_AWARE")


def _intent_obsolescence(v):
    currentness = min_q(v["goal_stability"], v["constraint_freshness"], v["context_freshness"])
    contradiction_risk = v["new_signal_conflict"]
    readiness = _wm((currentness, 5), (contradiction_risk.complement01(), 4), (v["reconfirmation_ease"], 1))
    confidence = _wm((v["signal_provenance"], 4), (v["context_freshness"], 2))
    return readiness, confidence, ("INTENT_FRESHNESS", "OBSOLESCENCE_GUARD")


def _evidence_gain(v):
    novelty = ratio01(v["expected_information_gain"], v["evidence_redundancy"])
    efficiency = ratio01(v["decision_relevance"], v["acquisition_cost"])
    readiness = _wm((novelty, 4), (efficiency, 4), (v["acquisition_reliability"], 2))
    confidence = _wm((v["gain_estimate_quality"], 3), (v["acquisition_reliability"], 3))
    return readiness, confidence, ("EVIDENCE_MARGINAL_GAIN", "REDUNDANCY_PENALTY")


def _optionality(v):
    preservation = min_q(v["reversibility"], v["branch_preservation"], v["future_compatibility"])
    lockin = max_q(v["vendor_lockin"], v["schema_lockin"], v["state_lockin"])
    readiness = _wm((preservation, 5), (lockin.complement01(), 4), (v["migration_readiness"], 2))
    confidence = _wm((v["migration_readiness"], 3), (v["future_compatibility"], 2))
    return readiness, confidence, ("OPTIONALITY_PRESERVED", "LOCKIN_PENALTY")


def _mincut_repair(v):
    cut_quality = ratio01(v["conflict_removed"], v["semantic_surface_changed"])
    preservation = min_q(v["invariant_preservation"], v["backward_compatibility"])
    readiness = _wm((cut_quality, 5), (preservation, 4), (v["repair_replayability"], 2))
    confidence = _wm((v["conflict_localization"], 4), (v["repair_replayability"], 2))
    return readiness, confidence, ("MINIMUM_SEMANTIC_CUT", "INVARIANT_PRESERVATION")


def _progress_velocity(v):
    verified = ratio01(v["verified_delta"], v["churn"])
    convergence = v["acceptance_distance_reduction"]
    readiness = _wm((verified, 4), (convergence, 4), (v["rework_avoidance"], 2))
    confidence = _wm((v["measurement_coverage"], 4), (v["acceptance_traceability"], 2))
    return readiness, confidence, ("VERIFIED_PROGRESS_RATE", "CHURN_DISCOUNTED")


def _value_density(v):
    usefulness = min_q(v["user_value"], v["decision_relevance"], v["actionability"])
    density = ratio01(usefulness, v["surface_complexity"])
    readiness = _wm((density, 5), (v["information_preservation"], 3), (v["discoverability"], 2))
    confidence = _wm((v["user_validation"], 4), (v["information_preservation"], 2))
    return readiness, confidence, ("VALUE_PER_SURFACE", "LOSS_BOUNDED_COMPACTION")


def _recovery_diversity(v):
    diversity = min_q(v["independent_recovery_paths"], v["state_reconstructability"], v["provider_independence"])
    drill = v["recovery_drill_success"]
    readiness = _wm((diversity, 5), (drill, 4), (v["time_to_recover_margin"], 3))
    confidence = _wm((v["recovery_drill_success"], 4), (v["state_reconstructability"], 2))
    return readiness, confidence, ("RECOVERY_PATH_DIVERSITY", "DRILL_EVIDENCE_GATED")


_SPECS: tuple[tuple[ConceptSpec, Evaluator], ...] = (
    (ConceptSpec("L4Q64-01", "Opportunity Cost Router", ("expected_value","reversibility","deadline_slack","alternative_cost","evidence_strength","estimate_stability"), "Routes work using value, reversibility and opportunity cost rather than raw priority."), _opportunity_cost),
    (ConceptSpec("L4Q64-02", "Uncertainty Surface Tomograph", ("model_uncertainty","data_uncertainty","policy_uncertainty","observability","counterexample_coverage","localizability"), "Finds uncertainty hotspots and blocks action when uncertainty cannot be localized."), _uncertainty_tomograph),
    (ConceptSpec("L4Q64-03", "Evidence Value-of-Information Planner", ("uncertainty_reduction","verification_cost","decision_impact","latency_penalty","reusability","measurement_reliability"), "Schedules evidence acquisition by marginal decision value."), _voi_planner),
    (ConceptSpec("L4Q64-04", "Freeze Granularity Optimizer", ("fault_locality","blast_radius","safe_progress_fraction","rollback_precision","fault_attribution"), "Freezes the smallest safe scope instead of indiscriminately stopping the whole system."), _freeze_granularity),
    (ConceptSpec("L4Q64-05", "Decision Half-Life Estimator", ("environment_stability","assumption_durability","evidence_refreshability","change_detection"), "Scores how long a decision can remain trusted before mandatory refresh."), _decision_half_life),
    (ConceptSpec("L4Q64-06", "Tool Hedge Portfolio", ("provider_diversity","semantic_equivalence","state_portability","switch_cost","health_observability"), "Builds provider/tool fallback readiness without assuming interchangeable behavior."), _tool_hedge),
    (ConceptSpec("L4Q64-07", "Interruption Merge Compiler", ("new_intent_compatibility","completed_work_reuse","checkpoint_quality","mutation_conflict","intent_parse_confidence"), "Safely merges mid-flight user direction changes while salvaging verified work."), _interruption_merge),
    (ConceptSpec("L4Q64-08", "Outcome SLO Budgeter", ("latency_margin","quality_margin","cost_margin","reliability_margin","degradation_plan_quality","telemetry_quality"), "Treats outcome quality, latency, reliability and cost as one deterministic release budget."), _outcome_slo),
    (ConceptSpec("L4Q64-09", "Counterexample Reservoir", ("semantic_diversity","boundary_diversity","historical_diversity","failure_discovery_rate","maintenance_cost","replayability","label_quality"), "Maintains a replayable, diversity-scored bank of failure examples."), _counterexample_reservoir),
    (ConceptSpec("L4Q64-10", "Regret-Bound Planner", ("irreversibility","harm_severity","uncertainty","optionality","learning_value","delay_tolerance","loss_bound_confidence"), "Selects actions that limit worst-case regret while preserving learning value."), _regret_bound),
    (ConceptSpec("L4Q64-11", "Human Cognitive Bandwidth Governor", ("information_clarity","decision_salience","attention_fit","notification_load","choice_overload","progressive_disclosure","user_feedback_signal"), "Constrains UI/agent output to the operator's decision bandwidth."), _cognitive_bandwidth),
    (ConceptSpec("L4Q64-12", "Proof Reuse Graph Optimizer", ("premise_match","environment_match","version_match","verification_cost_saved","reuse_validation_cost","lineage_integrity"), "Reuses prior verification only when premise, environment, version and lineage still match."), _proof_reuse),
    (ConceptSpec("L4Q64-13", "Failure Containment Radius Estimator", ("dependency_isolation","state_partitioning","rollback_scope_precision","side_effect_fanout","shared_state_coupling","dependency_map_quality"), "Estimates how far a fault can propagate before approving execution."), _containment_radius),
    (ConceptSpec("L4Q64-14", "Intent Obsolescence Detector", ("goal_stability","constraint_freshness","context_freshness","new_signal_conflict","reconfirmation_ease","signal_provenance"), "Detects when an old user instruction has become unsafe or stale under new context."), _intent_obsolescence),
    (ConceptSpec("L4Q64-15", "Marginal Evidence Gain Scheduler", ("expected_information_gain","evidence_redundancy","decision_relevance","acquisition_cost","acquisition_reliability","gain_estimate_quality"), "Stops gathering redundant evidence and targets the next highest-value proof."), _evidence_gain),
    (ConceptSpec("L4Q64-16", "Task Optionality Preserver", ("reversibility","branch_preservation","future_compatibility","vendor_lockin","schema_lockin","state_lockin","migration_readiness"), "Penalizes plans that prematurely destroy future choices."), _optionality),
    (ConceptSpec("L4Q64-17", "Consistency Repair Min-Cut Engine", ("conflict_removed","semantic_surface_changed","invariant_preservation","backward_compatibility","repair_replayability","conflict_localization"), "Chooses the smallest semantic repair that removes a contradiction while preserving invariants."), _mincut_repair),
    (ConceptSpec("L4Q64-18", "Semantic Progress Velocity Meter", ("verified_delta","churn","acceptance_distance_reduction","rework_avoidance","measurement_coverage","acceptance_traceability"), "Measures verified convergence, not file count or activity volume."), _progress_velocity),
    (ConceptSpec("L4Q64-19", "Value Density Compactor", ("user_value","decision_relevance","actionability","surface_complexity","information_preservation","discoverability","user_validation"), "Compresses control surfaces while proving useful information was preserved."), _value_density),
    (ConceptSpec("L4Q64-20", "Recovery Path Diversity Planner", ("independent_recovery_paths","state_reconstructability","provider_independence","recovery_drill_success","time_to_recover_margin"), "Requires multiple independent recovery paths rather than a single optimistic rollback story."), _recovery_diversity),
)

SPECS = {spec.concept_id: spec for spec, _ in _SPECS}
EVALUATORS = {spec.concept_id: fn for spec, fn in _SPECS}


def evaluate(concept_id: str, values: Mapping[str, Q64]) -> Evaluation:
    try:
        spec = SPECS[concept_id]
        evaluator = EVALUATORS[concept_id]
    except KeyError as exc:
        raise KeyError(f"unknown concept_id: {concept_id}") from exc
    validate_inputs(spec, values)
    readiness, confidence, codes = evaluator(values)
    return Evaluation(spec.concept_id, readiness, confidence, band(readiness, confidence), codes)
