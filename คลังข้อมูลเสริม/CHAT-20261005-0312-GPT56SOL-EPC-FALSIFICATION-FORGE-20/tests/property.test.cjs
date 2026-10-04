const test = require('node:test');
const assert = require('node:assert/strict');
const forge = require('../dist/index.js');
const {Q64, ForgeError} = forge;
const q = Q64.parse;

function permutations3(a,b,c){ return [[a,b,c],[a,c,b],[b,a,c],[b,c,a],[c,a,b],[c,b,a]]; }

test('Q64 small-domain add/sub round-trip property', () => {
  for (let a = -32n; a <= 32n; a += 1n) {
    for (let b = -32n; b <= 32n; b += 1n) {
      const qa = Q64.fromInt(a);
      const qb = Q64.fromInt(b);
      assert.equal(qa.add(qb).sub(qb).raw, qa.raw);
      if (b !== 0n) assert.equal(qa.div(qb).mul(qb).sub(qa).abs().raw <= qb.abs().raw, true);
    }
  }
});

test('Q64 parser is canonical and deterministic over decimal corpus', () => {
  const corpus=['0','-0','1','-1','0.1','0.5','0.999999999','123456.125','-123456.125'];
  for(const text of corpus){
    const first=Q64.parse(text); const second=Q64.parse(text);
    assert.equal(first.raw,second.raw);
    assert.equal(first.toString(),second.toString());
  }
});

test('canonical planners are invariant to input order', () => {
  const faults=['timeout','corruption','dependency-loss'];
  const baseline=forge.faultInjectionExperimentPlanner(faults);
  for(const perm of permutations3(...faults)) assert.deepEqual(forge.faultInjectionExperimentPlanner(perm),baseline);

  const assumptions=[{id:'B',statement:'two'},{id:'A',statement:'one'},{id:'C',statement:'three'}];
  const expected=forge.assumptionKillExperimentPlanner(assumptions);
  for(const perm of permutations3(...assumptions)) assert.deepEqual(forge.assumptionKillExperimentPlanner(perm),expected);
});

test('dossier result is invariant to experiment result ordering', () => {
  const rows=[
    {id:'C',status:'PASS',evidence:['e3']},
    {id:'A',status:'PASS',evidence:['e1']},
    {id:'B',status:'NOT_VERIFIED',evidence:[]}
  ];
  const expected=forge.promotionExperimentDossierCompiler('CAND',rows);
  for(const perm of permutations3(...rows)) assert.deepEqual(forge.promotionExperimentDossierCompiler('CAND',perm),expected);
  assert.equal(expected.readiness,'INSUFFICIENT_EVIDENCE');
  assert.equal(expected.autoPromote,false);
});

test('information yield is monotonic across deterministic corpus', () => {
  let previous=Q64.ZERO;
  for(let numerator=0n;numerator<=10n;numerator+=1n){
    const current=forge.evidenceInformationYieldEstimator(numerator,10n,q('1'));
    assert.equal(current.compare(previous)>=0,true);
    previous=current;
  }
});

test('boundary and resource probes reject unrepresentable outside edges', () => {
  assert.throws(()=>forge.boundaryConditionProbePlanner('x',Q64.MIN,Q64.ZERO),ForgeError);
  assert.throws(()=>forge.boundaryConditionProbePlanner('x',Q64.ZERO,Q64.MAX),ForgeError);
  assert.throws(()=>forge.resourceEnvelopeProbe('x',Q64.ZERO,Q64.MAX),ForgeError);
});

test('reproducibility capsule is insensitive to metadata and list insertion order', () => {
  const expected=forge.reproducibilityCapsuleBuilder({b:'2',a:'1'},['z','a','m'],['linux','node']);
  const variants=[
    forge.reproducibilityCapsuleBuilder({a:'1',b:'2'},['a','m','z'],['node','linux']),
    forge.reproducibilityCapsuleBuilder({b:'2',a:'1'},['m','z','a'],['linux','node'])
  ];
  for(const variant of variants) assert.deepEqual(variant,expected);
});

test('falsification pipeline objects are frozen against accidental mutation', () => {
  const h=forge.requirementToHypothesis({id:'R',statement:'claim',invariants:['i'],evidenceRequired:['e']});
  assert.equal(Object.isFrozen(h),true);
  assert.equal(Object.isFrozen(h.falsifiers),true);
  const probes=forge.determinismProbeGenerator('R',2n);
  assert.equal(Object.isFrozen(probes),true);
  assert.equal(Object.isFrozen(probes[0]),true);
});
