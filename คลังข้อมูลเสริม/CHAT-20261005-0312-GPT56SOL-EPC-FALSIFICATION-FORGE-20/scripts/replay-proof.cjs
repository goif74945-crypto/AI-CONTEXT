const assert = require('node:assert/strict');
const forge = require('../dist/index.js');
const q = forge.Q64.parse;
function execute(){
  const hypothesis=forge.requirementToHypothesis({
    id:'NEXY-DETERMINISM', statement:'same relevant input and state yields same structural result',
    invariants:['canonical output remains identical'], evidenceRequired:['replay-checksum']
  });
  const constraints=forge.constraintNegationExperimentPlanner(hypothesis.id,['authority-boundary','evidence-validity','stable-order']);
  const faults=forge.faultInjectionExperimentPlanner(['dependency-loss','malformed-evidence','timeout']);
  const probes=forge.determinismProbeGenerator('NEXY-DETERMINISM',8n);
  const yieldQ64=forge.evidenceInformationYieldEstimator(7n,8n,q('0.875'));
  return forge.reproducibilityCapsuleBuilder(
    {hypothesis:hypothesis.id,informationYield:yieldQ64.toString(),authority:hypothesis.authority},
    [...constraints.map(x=>x.id),...faults.map(x=>x.id),...probes.map(x=>x.id)],
    ['node-22','typescript-5.8','q64.64-trunc-zero']
  );
}
const first=execute();
for(let i=0;i<1000;i+=1) assert.deepEqual(execute(),first);
console.log(`REPLAY_PROOF_PASS iterations=1000 checksum=${first.checksum} algorithm=${first.checksumAlgorithm}`);
