import assert from "node:assert/strict";
import { NEXY_BASELINE, cloneBaseline } from "../src/baseline.mjs";
import { evaluateAll } from "../src/gates.mjs";

const malformed=[
  null, {}, {states:null}, {transitions:"not-array"}, {release:{}},
  {rbac:{manage_roles:"OWNER"}}, {numericScopes:{CORE_L9:{format:"Q64.64"}}},
  {envelope:{requiredFields:null,statuses:[],states:[]}},
  {adapter:{requiredFields:[],requiredMethods:null}},
  {evidence:{requiredFields:[],hashHexLength:"64",confidenceMinQ64:0n,confidenceMaxQ64:1n}}
];
let cases=0;
for(const candidate of malformed){
  const report=evaluateAll(NEXY_BASELINE,candidate);
  assert.ok(["DEFER","REJECT"].includes(report.composite.verdict));
  assert.notEqual(report.composite.verdict,"KEEP_CANDIDATE");
  assert.ok(report.gates.some(g=>g.status==="NOT_VERIFIED" || g.status==="FAIL"));
  cases++;
}
for(const key of Object.keys(NEXY_BASELINE).filter(k=>!["identity","provenance"].includes(k))){
  const c=cloneBaseline(); delete c[key];
  const report=evaluateAll(NEXY_BASELINE,c);
  assert.notEqual(report.composite.verdict,"KEEP_CANDIDATE");
  cases++;
}
console.log(JSON.stringify({status:"PASS",suite:"cvrc20-malformed",cases}));
