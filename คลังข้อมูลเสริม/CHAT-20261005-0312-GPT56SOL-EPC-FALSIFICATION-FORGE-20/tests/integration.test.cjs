const test = require('node:test');
const assert = require('node:assert/strict');
const forge = require('../dist/index.js');
const q = forge.Q64.parse;

test('proposal-to-experiment dossier is replay-identical and never promotes', () => {
  const req={id:'R-DETERMINISM',statement:'same state => same output',invariants:['stable output hash'],evidenceRequired:['hash']};
  function run(){
    const h=forge.requirementToHypothesis(req);
    forge.falsifiabilityGate({id:h.id,claim:h.claim,falsifiers:h.falsifiers,observables:['output-hash']});
    const boundaries=forge.boundaryConditionProbePlanner('load',q('0'),q('1'));
    const det=forge.determinismProbeGenerator('R-DETERMINISM',4n);
    const info=forge.evidenceInformationYieldEstimator(3n,4n,q('0.75'));
    const capsule=forge.reproducibilityCapsuleBuilder(
      {candidate:'C-1',hypothesis:h.id,informationYield:info.toString()},
      [...boundaries.map(x=>x.id),...det.map(x=>x.id)],
      ['node22','q64.64']
    );
    return forge.promotionExperimentDossierCompiler('C-1',[
      {id:'EXP-BOUNDARY',status:'PASS',evidence:[capsule.checksum]},
      {id:'EXP-REPLAY',status:'PASS',evidence:[capsule.checksum]}
    ]);
  }
  const a=run(); const b=run();
  assert.deepEqual(a,b);
  assert.equal(a.autoPromote,false);
  assert.equal(a.readiness,'READY_FOR_EXTERNAL_REVIEW');
});
