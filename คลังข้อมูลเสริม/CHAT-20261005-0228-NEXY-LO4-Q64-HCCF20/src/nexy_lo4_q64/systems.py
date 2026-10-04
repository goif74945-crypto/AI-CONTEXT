from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence

from .q64 import Q64, Q64Error

ZERO = Q64.zero()
ONE = Q64.one()


def _q(v: Q64 | int | str) -> Q64:
    return Q64.coerce(v)


def _nonneg(v: Q64, name: str) -> Q64:
    if v.raw < 0:
        raise Q64Error(f"{name} must be non-negative")
    return v


def _unit(v: Q64, name: str) -> Q64:
    if v.raw < 0 or v.raw > ONE.raw:
        raise Q64Error(f"{name} must be in [0,1]")
    return v


def _mean(values: Sequence[Q64]) -> Q64:
    if not values:
        raise Q64Error("empty sequence")
    total = ZERO
    for v in values:
        total = total + v
    return total / Q64.from_int(len(values))


def _weighted_mean(items: Sequence[tuple[Q64, Q64]]) -> Q64:
    if not items:
        raise Q64Error("empty weighted sequence")
    numerator = ZERO
    denominator = ZERO
    for value, weight in items:
        _nonneg(weight, "weight")
        numerator = numerator + value * weight
        denominator = denominator + weight
    if denominator.raw == 0:
        raise Q64Error("zero total weight")
    return numerator / denominator


@dataclass(frozen=True, slots=True)
class Ranked:
    key: str
    score: Q64
    reason: str


def attention_budget(urgency: Q64, impact: Q64, uncertainty: Q64, interruption_cost: Q64) -> Q64:
    """01 DAB: deterministic attention budget in [0,1]."""
    u, i, x, c = map(lambda z: _unit(z[0], z[1]), [(urgency,"urgency"),(impact,"impact"),(uncertainty,"uncertainty"),(interruption_cost,"interruption_cost")])
    return _weighted_mean([(u,Q64.from_int(35)),(i,Q64.from_int(35)),(x,Q64.from_int(20)),(ONE-c,Q64.from_int(10))]).clamp(ZERO, ONE)


def context_entropy(concentrations: Sequence[Q64]) -> Q64:
    """02 CEG: dispersion proxy without logs; 0 focused, approaches 1 dispersed."""
    if not concentrations:
        raise Q64Error("no concentrations")
    total = ZERO
    sq = ZERO
    for p in concentrations:
        _unit(p, "concentration")
        total = total + p
        sq = sq + p*p
    if total.raw != ONE.raw:
        raise Q64Error("concentrations must sum exactly to 1.0 Q64")
    return (ONE - sq).clamp(ZERO, ONE)


def semantic_drift(reference: Sequence[Q64], current: Sequence[Q64]) -> Q64:
    """03 SDI: normalized L1 drift."""
    if len(reference) != len(current) or not reference:
        raise Q64Error("vector shape mismatch")
    acc = ZERO
    for a,b in zip(reference,current):
        acc = acc + (a-b).abs()
    return (acc / Q64.from_int(len(reference))).clamp(ZERO, ONE)


def compression_priority(information: Q64, redundancy: Q64, retrieval_cost: Q64) -> Q64:
    """04 ICP: priority to compress while preserving high-information low-redundancy items."""
    return (_unit(redundancy,"redundancy") * _unit(retrieval_cost,"retrieval_cost") * (ONE - _unit(information,"information"))).clamp(ZERO,ONE)


def friction_score(steps: int, reversals: int, ambiguity: Q64, latency: Q64) -> Q64:
    """05 UFF: interaction friction field score."""
    if steps < 0 or reversals < 0:
        raise Q64Error("counts must be non-negative")
    structural = (Q64.from_int(steps + 2*reversals) / Q64.from_int(max(1, steps + 2*reversals + 8))).clamp(ZERO,ONE)
    return _weighted_mean([(structural,Q64.from_int(40)),(_unit(ambiguity,"ambiguity"),Q64.from_int(35)),(_unit(latency,"latency"),Q64.from_int(25))]).clamp(ZERO,ONE)


def deferred_value(value: Q64, decay: Q64, delay_ticks: int, dependency_gain: Q64) -> Q64:
    """06 DVS: deterministic deferred-work value with rational decay approximation."""
    if delay_ticks < 0:
        raise Q64Error("delay_ticks must be non-negative")
    v = _nonneg(value,"value")
    d = _unit(decay,"decay")
    gain = _nonneg(dependency_gain,"dependency_gain")
    factor = ONE / (ONE + d * Q64.from_int(delay_ticks))
    return v * factor + gain


def information_gain(unknown_mass: Q64, resolvable_mass: Q64, cost: Q64) -> Q64:
    """07 IGR: route actions by expected resolvable unknown per cost."""
    u = _unit(unknown_mass,"unknown_mass")
    r = _unit(resolvable_mass,"resolvable_mass")
    c = _nonneg(cost,"cost")
    if c.raw == 0:
        raise Q64Error("cost must be > 0")
    return (u*r)/c


def tool_efficiency(success: Q64, evidence_gain: Q64, latency_cost: Q64, mutation_risk: Q64) -> Q64:
    """08 TICS: tool invocation composite score."""
    s,e,l,m = (_unit(success,"success"),_unit(evidence_gain,"evidence_gain"),_unit(latency_cost,"latency_cost"),_unit(mutation_risk,"mutation_risk"))
    return _weighted_mean([(s,Q64.from_int(40)),(e,Q64.from_int(40)),(ONE-l,Q64.from_int(10)),(ONE-m,Q64.from_int(10))]).clamp(ZERO,ONE)


def explanation_density(useful_claims: int, tokens: int, unresolved_ratio: Q64) -> Q64:
    """09 EDC: useful verified claim density, penalized by unresolved ratio."""
    if useful_claims < 0 or tokens <= 0 or useful_claims > tokens:
        raise Q64Error("invalid counts")
    density = Q64.from_ratio(useful_claims,tokens)
    return density*(ONE-_unit(unresolved_ratio,"unresolved_ratio"))


def recovery_priority(blast_radius: Q64, reversibility: Q64, user_impact: Q64, evidence_quality: Q64) -> Q64:
    """10 RPO: recovery ordering score."""
    b,r,u,e = (_unit(blast_radius,"blast_radius"),_unit(reversibility,"reversibility"),_unit(user_impact,"user_impact"),_unit(evidence_quality,"evidence_quality"))
    return _weighted_mean([(b,Q64.from_int(35)),(u,Q64.from_int(35)),(ONE-r,Q64.from_int(20)),(ONE-e,Q64.from_int(10))]).clamp(ZERO,ONE)


def horizon_utility(immediate: Q64, near: Q64, long: Q64, irreversible_penalty: Q64) -> Q64:
    """11 MHUI: multi-horizon utility that discounts irreversible downside."""
    p = _unit(irreversible_penalty,"irreversible_penalty")
    score = _weighted_mean([(immediate,Q64.from_int(50)),(near,Q64.from_int(30)),(long,Q64.from_int(20))])
    return score*(ONE-p)


def capability_saturation(demand: Q64, capacity: Q64, queue_pressure: Q64) -> Q64:
    """12 CSM: saturation with pressure coupling."""
    d,c = (_nonneg(demand,"demand"),_nonneg(capacity,"capacity"))
    if c.raw == 0:
        raise Q64Error("capacity must be > 0")
    utilization = (d/c).clamp(ZERO,ONE)
    return _weighted_mean([(utilization,Q64.from_int(75)),(_unit(queue_pressure,"queue_pressure"),Q64.from_int(25))]).clamp(ZERO,ONE)


def rhythm_pressure(message_rate: Q64, correction_rate: Q64, idle_ratio: Q64) -> Q64:
    """13 IRR: interaction rhythm pressure for pacing adapters."""
    return _weighted_mean([(_unit(message_rate,"message_rate"),Q64.from_int(45)),(_unit(correction_rate,"correction_rate"),Q64.from_int(40)),(ONE-_unit(idle_ratio,"idle_ratio"),Q64.from_int(15))]).clamp(ZERO,ONE)


def reversibility_score(rollback_coverage: Q64, state_capture: Q64, external_side_effect: Q64) -> Q64:
    """14 DRM: decision reversibility meter."""
    return _weighted_mean([(_unit(rollback_coverage,"rollback_coverage"),Q64.from_int(45)),(_unit(state_capture,"state_capture"),Q64.from_int(35)),(ONE-_unit(external_side_effect,"external_side_effect"),Q64.from_int(20))]).clamp(ZERO,ONE)


def freshness(initial: Q64, age_ticks: int, half_pressure: Q64) -> Q64:
    """15 SFDE: deterministic rational freshness decay."""
    if age_ticks < 0:
        raise Q64Error("age_ticks must be non-negative")
    i = _unit(initial,"initial")
    h = _nonneg(half_pressure,"half_pressure")
    return i / (ONE + h*Q64.from_int(age_ticks))


def evidence_sampling_priority(materiality: Q64, uncertainty: Q64, sample_cost: Q64, coverage: Q64) -> Q64:
    """16 BESA: budget-aware evidence sampling priority."""
    c = _nonneg(sample_cost,"sample_cost")
    if c.raw == 0:
        raise Q64Error("sample_cost must be > 0")
    return (_unit(materiality,"materiality")*_unit(uncertainty,"uncertainty")*(ONE-_unit(coverage,"coverage")))/c


def calibration_mix(estimates: Sequence[tuple[Q64,Q64]]) -> Q64:
    """17 CCM: cross-model calibration mixer; confidence weights are explicit and non-negative."""
    for estimate, confidence in estimates:
        _unit(estimate,"estimate")
        _unit(confidence,"confidence")
    return _weighted_mean(list(estimates)).clamp(ZERO,ONE)


def change_wavefront(direct_impact: Q64, fanout: int, coupling: Q64, test_gap: Q64) -> Q64:
    """18 SCIW: spec-change impact wavefront score."""
    if fanout < 0:
        raise Q64Error("fanout must be non-negative")
    fan = Q64.from_ratio(fanout, fanout+4) if fanout else ZERO
    return _weighted_mean([(_unit(direct_impact,"direct_impact"),Q64.from_int(35)),(fan,Q64.from_int(25)),(_unit(coupling,"coupling"),Q64.from_int(25)),(_unit(test_gap,"test_gap"),Q64.from_int(15))]).clamp(ZERO,ONE)


def handoff_continuity(state_coverage: Q64, decision_provenance: Q64, blocker_clarity: Q64, evidence_links: Q64) -> Q64:
    """19 DHCE: deterministic handoff continuity estimator."""
    vals=[_unit(state_coverage,"state_coverage"),_unit(decision_provenance,"decision_provenance"),_unit(blocker_clarity,"blocker_clarity"),_unit(evidence_links,"evidence_links")]
    return _mean(vals)


def user_value_frontier(usefulness: Q64, correctness: Q64, latency: Q64, cognitive_load: Q64, lock_in: Q64) -> Q64:
    """20 UVFE: user-value frontier score with correctness dominant."""
    u,c,l,g,k = (_unit(usefulness,"usefulness"),_unit(correctness,"correctness"),_unit(latency,"latency"),_unit(cognitive_load,"cognitive_load"),_unit(lock_in,"lock_in"))
    return _weighted_mean([(c,Q64.from_int(40)),(u,Q64.from_int(30)),(ONE-l,Q64.from_int(10)),(ONE-g,Q64.from_int(10)),(ONE-k,Q64.from_int(10))]).clamp(ZERO,ONE)


SYSTEMS = {
    "DAB": attention_budget,
    "CEG": context_entropy,
    "SDI": semantic_drift,
    "ICP": compression_priority,
    "UFF": friction_score,
    "DVS": deferred_value,
    "IGR": information_gain,
    "TICS": tool_efficiency,
    "EDC": explanation_density,
    "RPO": recovery_priority,
    "MHUI": horizon_utility,
    "CSM": capability_saturation,
    "IRR": rhythm_pressure,
    "DRM": reversibility_score,
    "SFDE": freshness,
    "BESA": evidence_sampling_priority,
    "CCM": calibration_mix,
    "SCIW": change_wavefront,
    "DHCE": handoff_continuity,
    "UVFE": user_value_frontier,
}


def rank(candidates: Mapping[str,Q64]) -> list[Ranked]:
    """Stable deterministic rank: score descending, then UTF-8 byte lexical key."""
    if not candidates:
        raise Q64Error("no candidates")
    ordered = sorted(candidates.items(), key=lambda kv: (-kv[1].raw, kv[0].encode("utf-8")))
    return [Ranked(key, score, "score_desc_then_utf8_key") for key,score in ordered]
