import test from 'node:test';
import assert from 'node:assert/strict';
import { evaluateOutcomeClosure } from '../dist/outcome_closure.js';
import { summarizeProgress } from '../dist/progress_truth.js';
import { planReversibleProbes } from '../dist/reversible_probe.js';
import { judgeBenefitRegression } from '../dist/benefit_regression.js';
import { evaluateAdoptionReadiness } from '../dist/adoption_readiness.js';

const baseDossier = {
  proposalId: 'proposal-a',
  collisionScan: { checked: true, unresolvedOverlapIds: [] },
  compatibility: [{ id: 'c1', status: 'PASS' }],
  evidenceClassesPresent: ['E0', 'E1', 'E2'],
  requiredEvidenceClasses: ['E0', 'E1', 'E2'],
  rollback: { defined: true, verified: true },
  protectedScopeMutation: false,
  outcomeStatus: 'CLOSED',
  progressStatus: 'COMPLETE',
  benefitStatus: 'BENEFICIAL'
};

test('outcome contract freezes on duplicate required predicate IDs', () => {
  const result = evaluateOutcomeClosure(
    { id: 'dup', required: ['a', 'a'], forbidden: [], minEvidencePerRequired: 1 },
    [{ predicateId: 'a', status: 'SATISFIED', evidenceIds: ['e'] }]
  );
  assert.equal(result.status, 'FREEZE');
  assert.ok(result.reasons.includes('DUPLICATE_CONTRACT_PREDICATE'));
});

test('unknown forbidden predicate prevents closure without fabricating safety', () => {
  const result = evaluateOutcomeClosure(
    { id: 'unknown-forbidden', required: ['a'], forbidden: ['danger'], minEvidencePerRequired: 1 },
    [
      { predicateId: 'a', status: 'SATISFIED', evidenceIds: ['e1'] },
      { predicateId: 'danger', status: 'UNKNOWN', evidenceIds: [] }
    ]
  );
  assert.equal(result.status, 'OPEN');
  assert.deepEqual(result.unresolvedForbidden, ['danger']);
});

test('progress freezes duplicate obligation IDs instead of double-counting work', () => {
  const result = summarizeProgress([{ id: 'same', status: 'PASS' }, { id: 'same', status: 'PASS' }]);
  assert.equal(result.aggregate, 'FREEZE');
  assert.equal(result.completeClaimAllowed, false);
});

test('probe planner blocks owner-only evidence acquisition when only operator authority exists', () => {
  const result = planReversibleProbes({
    unknowns: [{ id: 'u', blocking: true }],
    availableAuthorities: ['OPERATOR'],
    probes: [{ id: 'owner-read', resolves: ['u'], effect: 'READ_ONLY', cost: 1, requiredAuthority: 'OWNER' }]
  });
  assert.equal(result.status, 'BLOCKED');
  assert.ok(result.rejectedProbes.some((x) => x.reason === 'MISSING_AUTHORITY'));
});

test('probe planner reports exact minimum safe cost when budget is too small', () => {
  const result = planReversibleProbes({
    unknowns: [{ id: 'u1', blocking: true }, { id: 'u2', blocking: true }],
    availableAuthorities: [],
    maxTotalCost: 1,
    probes: [
      { id: 'p1', resolves: ['u1'], effect: 'READ_ONLY', cost: 1, requiredAuthority: 'NONE' },
      { id: 'p2', resolves: ['u2'], effect: 'READ_ONLY', cost: 1, requiredAuthority: 'NONE' }
    ]
  });
  assert.equal(result.status, 'BLOCKED');
  assert.equal(result.minimumCost, 2);
  assert.ok(result.reasons.includes('COST_BUDGET_EXCEEDED'));
});

test('probe planner tie-breaks equal-cost equal-count covers by canonical probe IDs', () => {
  const result = planReversibleProbes({
    unknowns: [{ id: 'u', blocking: true }],
    availableAuthorities: [],
    probes: [
      { id: 'z-probe', resolves: ['u'], effect: 'READ_ONLY', cost: 1, requiredAuthority: 'NONE' },
      { id: 'a-probe', resolves: ['u'], effect: 'READ_ONLY', cost: 1, requiredAuthority: 'NONE' }
    ]
  });
  assert.equal(result.status, 'PROBE');
  assert.deepEqual(result.selectedProbeIds, ['a-probe']);
});

test('benefit judge freezes malformed axis thresholds', () => {
  const result = judgeBenefitRegression(
    [{ id: 'quality', direction: 'HIGHER', critical: true, minImprovement: 0, maxRegression: 0 }],
    { quality: 10 },
    { quality: 11 }
  );
  assert.equal(result.status, 'FREEZE');
  assert.ok(result.reasons.includes('INVALID_MIN_IMPROVEMENT:quality'));
});

test('benefit judge permits declared noncritical tradeoff only when a real improvement exists', () => {
  const result = judgeBenefitRegression(
    [
      { id: 'quality', direction: 'HIGHER', critical: true, minImprovement: 1, maxRegression: 0 },
      { id: 'cost', direction: 'LOWER', critical: false, minImprovement: 1, maxRegression: 0 }
    ],
    { quality: 10, cost: 5 },
    { quality: 12, cost: 6 }
  );
  assert.equal(result.status, 'BENEFICIAL');
  assert.deepEqual(result.improvedAxes, ['quality']);
  assert.deepEqual(result.regressedAxes, ['cost']);
});

test('adoption firewall freezes an explicit compatibility failure', () => {
  const result = evaluateAdoptionReadiness({ ...baseDossier, compatibility: [{ id: 'contract', status: 'FAIL' }] });
  assert.equal(result.status, 'FREEZE');
  assert.ok(result.reasons.includes('COMPATIBILITY_FAILURE'));
});

test('adoption firewall holds an unknown compatibility status', () => {
  const result = evaluateAdoptionReadiness({ ...baseDossier, compatibility: [{ id: 'contract', status: 'UNKNOWN' }] });
  assert.equal(result.status, 'HOLD');
  assert.ok(result.reasons.includes('COMPATIBILITY_UNKNOWN'));
});

test('adoption firewall holds when required evidence classes are missing', () => {
  const result = evaluateAdoptionReadiness({ ...baseDossier, evidenceClassesPresent: ['E0', 'E1'] });
  assert.equal(result.status, 'HOLD');
  assert.deepEqual(result.missingEvidenceClasses, ['E2']);
});

test('readiness fingerprint is invariant to compatibility and evidence input ordering', () => {
  const left = evaluateAdoptionReadiness({
    ...baseDossier,
    compatibility: [{ id: 'b', status: 'PASS' }, { id: 'a', status: 'PASS' }],
    evidenceClassesPresent: ['E2', 'E0', 'E1'],
    requiredEvidenceClasses: ['E1', 'E2', 'E0']
  });
  const right = evaluateAdoptionReadiness({
    ...baseDossier,
    compatibility: [{ id: 'a', status: 'PASS' }, { id: 'b', status: 'PASS' }],
    evidenceClassesPresent: ['E0', 'E1', 'E2'],
    requiredEvidenceClasses: ['E0', 'E1', 'E2']
  });
  assert.equal(left.fingerprint, right.fingerprint);
});
