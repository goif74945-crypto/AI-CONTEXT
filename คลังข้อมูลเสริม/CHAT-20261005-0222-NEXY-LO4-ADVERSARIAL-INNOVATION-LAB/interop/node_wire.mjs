import fs from "node:fs";
import {
  analyzeContractDrift,
  EvidenceValue,
  evaluateAbstention,
  evaluateConstraints,
  InfluenceGraph,
} from "../typescript/dist/index.js";

const fixture = JSON.parse(fs.readFileSync(new URL("./fixture.json", import.meta.url), "utf8"));
const a = fixture.aurora;
const aurora = evaluateAbstention(
  a.cases.map((x) => ({
    caseId: x.case_id,
    answerable: x.answerable,
    action: x.action,
    ...(x.correct === undefined ? {} : { correct: x.correct }),
    ...(x.confidence === undefined ? {} : { confidence: x.confidence }),
    ...(x.risk_weight === undefined ? {} : { riskWeight: x.risk_weight }),
  })),
  {
    wrongAnswerCost: 4,
    unanswerableAnswerCost: 8,
    needlessAbstainCost: 1,
    maxUnsafeAnswerRate: a.policy.max_unsafe_answer_rate,
    minReliabilityScore: a.policy.min_reliability_score,
    maxBrierScore: a.policy.max_brier_score,
  },
);
const margin = evaluateConstraints(fixture.margin.constraints.map((x) => ({
  name: x.name, actual: x.actual, operator: x.operator, limit: x.limit,
  scale: x.scale, requiredMargin: x.required_margin,
})));
const u = fixture.upa;
const upa = new EvidenceValue(u.left.state, u.left.provenance).knowledgeJoin(new EvidenceValue(u.right.state, u.right.provenance));
const t = fixture.traceweight;
const graph = new InfluenceGraph(t.nodes.map((x) => ({
  nodeId: x.node_id, parents: x.parents, isAgentSource: x.is_agent_source, verified: x.verified,
})));
const trace = graph.analyze(t.target);
const d = fixture.contract_drift;
const drift = analyzeContractDrift(
  {
    authorizedScope: d.before.authorized_scope,
    successInvariants: d.before.success_invariants,
    forbiddenActions: d.before.forbidden_actions,
    assumptions: d.before.assumptions,
    requiredEvidence: d.before.required_evidence,
  },
  {
    authorizedScope: d.after.authorized_scope,
    successInvariants: d.after.success_invariants,
    forbiddenActions: d.after.forbidden_actions,
    assumptions: d.after.assumptions,
    requiredEvidence: d.after.required_evidence,
  },
);
const out = {
  aurora: { status: aurora.status, unsafe_answer_rate: Number(aurora.unsafeAnswerRate.toFixed(12)) },
  margin: { release_status: margin.releaseStatus, minimum_margin: Number(margin.minimumMargin.toFixed(12)) },
  upa: { state: upa.state, releaseable: upa.releaseable },
  traceweight: { status: trace.status, dominant_source: trace.dominantSource, dominance_ratio: Number(trace.dominanceRatio.toFixed(12)) },
  contract_drift: { status: drift.status, total_cost: drift.totalCost },
};
function stable(value) {
  if (Array.isArray(value)) return `[${value.map(stable).join(",")}]`;
  if (value !== null && typeof value === "object") {
    return `{${Object.keys(value).sort().map((k) => `${JSON.stringify(k)}:${stable(value[k])}`).join(",")}}`;
  }
  return JSON.stringify(value);
}
console.log(stable(out));
