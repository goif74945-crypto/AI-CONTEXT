const test = require('node:test');
const assert = require('node:assert/strict');
const {
  Q64,
  ForgeError,
  requirementToHypothesis,
  falsifiabilityGate,
  minimalFalsifierPlan,
  constraintNegationExperimentPlanner,
  boundaryConditionProbePlanner,
  faultInjectionExperimentPlanner,
  assumptionKillExperimentPlanner,
  discriminatingEvidenceSelector,
  oracleTriangulationPlanner,
  evidenceInformationYieldEstimator,
  sequentialEvidenceStopper,
  counterexampleDeltaMinimizer,
  environmentalSensitivityMatrix,
  determinismProbeGenerator,
  resourceEnvelopeProbe,
  crossVersionDifferentialExperiment,
  observabilityProbeContractCompiler,
  reproducibilityCapsuleBuilder,
  experimentIndependenceAuditor,
  promotionExperimentDossierCompiler,
  MECHANISM_IDS
} = require('../dist/index.js');

const q = (x) => Q64.parse(x);

test('forge exposes exactly 20 stable mechanisms', () => {
  assert.equal(MECHANISM_IDS.length, 20);
  assert.equal(new Set(MECHANISM_IDS).size, 20);
});

test('RHC compiles a requirement into a falsifiable hypothesis contract', () => {
  const out = requirementToHypothesis({
    id: 'REQ-1',
    statement: 'same input and state produces same structural result',
    invariants: ['output hash remains identical'],
    evidenceRequired: ['replay-hash']
  });
  assert.equal(out.id, 'HYP-REQ-1');
  assert.equal(out.authority, 'ADVISORY_ONLY');
  assert.deepEqual(out.falsifiers, ['violate:output hash remains identical']);
});

test('FG rejects hypotheses with no observable falsifier', () => {
  assert.throws(() => falsifiabilityGate({id:'H', claim:'always good', falsifiers:[], observables:[]}), ForgeError);
  const pass = falsifiabilityGate({id:'H', claim:'x', falsifiers:['x!=1'], observables:['x']});
  assert.equal(pass.status, 'PASS');
});

test('MFP picks minimum deterministic falsification cost then lexical id', () => {
  const out = minimalFalsifierPlan([
    {id:'B', cost:q('2'), falsifies:['H1']},
    {id:'A', cost:q('1'), falsifies:['H1']},
    {id:'C', cost:q('1'), falsifies:['H1']}
  ], ['H1']);
  assert.equal(out.selected[0].id, 'A');
});

test('CNEP creates one isolated negation per constraint', () => {
  const out = constraintNegationExperimentPlanner('H1', ['auth-boundary','evidence-fresh']);
  assert.deepEqual(out.map(x=>x.negatedConstraint), ['auth-boundary','evidence-fresh']);
});

test('BCPP creates raw-unit probes around both Q64 boundaries', () => {
  const out = boundaryConditionProbePlanner('latency', q('1'), q('2'));
  assert.equal(out.length, 6);
  assert.equal(out[0].value.raw, q('1').raw - 1n);
  assert.equal(out[5].value.raw, q('2').raw + 1n);
});

test('FIEP deterministically plans declared faults only', () => {
  const out = faultInjectionExperimentPlanner(['timeout','dependency-loss','corruption']);
  assert.deepEqual(out.map(x=>x.fault), ['corruption','dependency-loss','timeout']);
});

test('AKEP turns assumptions into direct kill experiments', () => {
  const out = assumptionKillExperimentPlanner([{id:'A2', statement:'clock is monotonic'},{id:'A1', statement:'source is independent'}]);
  assert.deepEqual(out.map(x=>x.assumptionId), ['A1','A2']);
  assert.equal(out[0].expectedIfAssumptionFalse, 'HYPOTHESIS_AT_RISK');
});

test('DES maximizes discrimination/cost without float math', () => {
  const out = discriminatingEvidenceSelector([
    {id:'E1', discrimination:q('0.8'), cost:q('0.4')},
    {id:'E2', discrimination:q('0.9'), cost:q('0.9')}
  ]);
  assert.equal(out.id, 'E1');
});

test('OTP requires independent oracles and emits disagreement probes', () => {
  assert.throws(() => oracleTriangulationPlanner([{id:'O1', root:'R'}]), ForgeError);
  const out = oracleTriangulationPlanner([{id:'O2', root:'B'},{id:'O1', root:'A'},{id:'O3', root:'A'}]);
  assert.equal(out.independentRoots, 2n);
  assert.equal(out.pairs.length, 2);
});

test('EIYE computes bounded Q64 information yield', () => {
  const out = evidenceInformationYieldEstimator(3n, 4n, q('0.5'));
  assert.equal(out.toString(), '0.375');
  assert.throws(()=>evidenceInformationYieldEstimator(5n,4n,q('0.5')), ForgeError);
});

test('SES is deterministic and non-promoting', () => {
  assert.equal(sequentialEvidenceStopper(q('0.2'), q('0.8'), q('0.7'), q('0.7')).verdict, 'FALSIFIED');
  assert.equal(sequentialEvidenceStopper(q('0.8'), q('0.1'), q('0.7'), q('0.7')).verdict, 'ENOUGH_FOR_REVIEW');
  assert.equal(sequentialEvidenceStopper(q('0.4'), q('0.4'), q('0.7'), q('0.7')).verdict, 'CONTINUE');
});

test('CDM chooses smallest counterexample delta deterministically', () => {
  const out = counterexampleDeltaMinimizer([
    {id:'C2', delta:q('0.25'), witness:'b'},
    {id:'C1', delta:q('0.25'), witness:'a'},
    {id:'C3', delta:q('0.5'), witness:'c'}
  ]);
  assert.equal(out.id, 'C1');
});

test('ESM measures per-metric environment span', () => {
  const out = environmentalSensitivityMatrix([
    {environment:'B', metrics:{latency:q('3'),quality:q('0.8')}},
    {environment:'A', metrics:{latency:q('1'),quality:q('0.9')}}
  ]);
  assert.equal(out.latency.span.toString(), '2');
  assert.equal(out.quality.span.toString(), '0.1');
});

test('DPG generates stable replay probes without seeds or wall clock', () => {
  const out = determinismProbeGenerator('CASE-1', 3n);
  assert.deepEqual(out.map(x=>x.id), ['DET-CASE-1-000001','DET-CASE-1-000002','DET-CASE-1-000003']);
  assert.ok(out.every(x=>x.inputId === 'CASE-1'));
});

test('REP probes below/min/max/above resource envelope', () => {
  const out = resourceEnvelopeProbe('memory', q('4'), q('8'));
  assert.deepEqual(out.map(x=>x.position), ['BELOW_MIN','AT_MIN','AT_MAX','ABOVE_MAX']);
});

test('CVDE emits only semantic differences in canonical key order', () => {
  const out = crossVersionDifferentialExperiment(
    {a:'same',b:'old',c:'only-old'},
    {a:'same',b:'new',d:'only-new'}
  );
  assert.deepEqual(out.map(x=>x.key), ['b','c','d']);
});

test('OPCC fails closed if a falsifier has no observable signal', () => {
  assert.throws(()=>observabilityProbeContractCompiler(['f1','f2'], {f1:'signal-1'}), ForgeError);
  const out=observabilityProbeContractCompiler(['f2','f1'], {f1:'signal-1',f2:'signal-2'});
  assert.deepEqual(out.map(x=>x.falsifier), ['f1','f2']);
});

test('RCB canonicalizes order and produces replay-stable checksum', () => {
  const a=reproducibilityCapsuleBuilder({z:'2',a:'1'}, ['cmd-b','cmd-a'], ['env-b','env-a']);
  const b=reproducibilityCapsuleBuilder({a:'1',z:'2'}, ['cmd-a','cmd-b'], ['env-a','env-b']);
  assert.deepEqual(a,b);
  assert.match(a.checksum, /^[0-9a-f]{16}$/);
});

test('EIA detects common roots and computes independence ratio', () => {
  const out=experimentIndependenceAuditor([
    {id:'E1', roots:['R1']},
    {id:'E2', roots:['R2']},
    {id:'E3', roots:['R1']}
  ]);
  assert.equal(out.independentExperiments, 2n);
  assert.equal(out.totalExperiments, 3n);
  assert.equal(out.ratio.toString().slice(0,6),'0.6666');
  assert.deepEqual(out.sharedRoots, ['R1']);
});

test('PEDC remains advisory and cannot auto-promote', () => {
  const out=promotionExperimentDossierCompiler('CAND-1', [
    {id:'E2', status:'PASS', evidence:['x']},
    {id:'E1', status:'FALSIFIED', evidence:['y']}
  ]);
  assert.equal(out.authority,'ADVISORY_ONLY');
  assert.equal(out.autoPromote,false);
  assert.equal(out.readiness,'BLOCKED_BY_FALSIFICATION');
  assert.deepEqual(out.experiments.map(x=>x.id),['E1','E2']);
});

test('critical invalid input paths fail closed', () => {
  assert.throws(()=>minimalFalsifierPlan([],['H1']), ForgeError);
  assert.throws(()=>boundaryConditionProbePlanner('x',q('2'),q('1')), ForgeError);
  assert.throws(()=>determinismProbeGenerator('',1n), ForgeError);
  assert.throws(()=>resourceEnvelopeProbe('cpu',q('-1'),q('1')), ForgeError);
  assert.throws(()=>experimentIndependenceAuditor([]), ForgeError);
});

test('MFP solves total-cost coverage instead of per-hypothesis greedy selection', () => {
  const out=minimalFalsifierPlan([
    {id:'ONE',cost:q('1.5'),falsifies:['H1','H2']},
    {id:'H1-CHEAP',cost:q('1'),falsifies:['H1']},
    {id:'H2-CHEAP',cost:q('1'),falsifies:['H2']}
  ],['H1','H2']);
  assert.deepEqual(out.selected.map(x=>x.id),['ONE']);
  assert.deepEqual(out.uncovered,[]);
});

test('MFP fails closed when full falsification coverage is impossible', () => {
  assert.throws(()=>minimalFalsifierPlan([{id:'A',cost:q('1'),falsifies:['H1']}],['H1','H2']),ForgeError);
});
