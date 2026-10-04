import test from 'node:test';
import assert from 'node:assert/strict';
import { evaluateOutcomeClosure } from '../dist/outcome_closure.js';
import { summarizeProgress } from '../dist/progress_truth.js';
import { planReversibleProbes } from '../dist/reversible_probe.js';
import { judgeBenefitRegression } from '../dist/benefit_regression.js';
import { evaluateAdoptionReadiness } from '../dist/adoption_readiness.js';

test('end-to-end mesh moves from unresolved work to human-review-ready without auto-promotion', () => {
  const probe = planReversibleProbes({
    unknowns: [{ id: 'runtime-evidence', blocking: true }],
    availableAuthorities: [],
    probes: [{ id: 'read-ci-result', resolves: ['runtime-evidence'], effect: 'READ_ONLY', cost: 1, requiredAuthority: 'NONE' }]
  });
  assert.equal(probe.status, 'PROBE');

  const outcome = evaluateOutcomeClosure(
    { id: 'closure', required: ['design', 'code', 'tests'], forbidden: ['nexy-write'], minEvidencePerRequired: 1 },
    [
      { predicateId: 'design', status: 'SATISFIED', evidenceIds: ['spec'] },
      { predicateId: 'code', status: 'SATISFIED', evidenceIds: ['commit'] },
      { predicateId: 'tests', status: 'SATISFIED', evidenceIds: ['test-run'] },
      { predicateId: 'nexy-write', status: 'VIOLATED', evidenceIds: ['repo-audit'] }
    ]
  );
  assert.equal(outcome.status, 'CLOSED');

  const progress = summarizeProgress([
    { id: 'design', status: 'PASS' },
    { id: 'code', status: 'PASS' },
    { id: 'tests', status: 'PASS' }
  ]);
  assert.equal(progress.aggregate, 'COMPLETE');

  const benefit = judgeBenefitRegression(
    [{ id: 'manual_checks', direction: 'LOWER', critical: false, minImprovement: 1, maxRegression: 0 }],
    { manual_checks: 5 },
    { manual_checks: 3 }
  );
  assert.equal(benefit.status, 'BENEFICIAL');

  const readiness = evaluateAdoptionReadiness({
    proposalId: 'nocm',
    collisionScan: { checked: true, unresolvedOverlapIds: [] },
    compatibility: [{ id: 'nexy-contract-boundary', status: 'PASS' }],
    evidenceClassesPresent: ['E0', 'E1', 'E2'],
    requiredEvidenceClasses: ['E0', 'E1', 'E2'],
    rollback: { defined: true, verified: true },
    protectedScopeMutation: false,
    outcomeStatus: outcome.status,
    progressStatus: progress.aggregate,
    benefitStatus: benefit.status
  });

  assert.equal(readiness.status, 'READY_FOR_HUMAN_REVIEW');
  assert.equal(readiness.automaticApproval, false);
});
