import test from 'node:test';
import assert from 'node:assert/strict';
import { evaluateAdoptionReadiness } from '../dist/adoption_readiness.js';

const readyDossier = {
  proposalId: 'proposal-1',
  collisionScan: { checked: true, unresolvedOverlapIds: [] },
  compatibility: [
    { id: 'directive-shape', status: 'PASS' },
    { id: 'evidence-shape', status: 'PASS' }
  ],
  evidenceClassesPresent: ['E0', 'E1', 'E2'],
  requiredEvidenceClasses: ['E0', 'E1', 'E2'],
  rollback: { defined: true, verified: true },
  protectedScopeMutation: false,
  outcomeStatus: 'CLOSED',
  progressStatus: 'COMPLETE',
  benefitStatus: 'BENEFICIAL'
};

test('can only become READY_FOR_HUMAN_REVIEW, never auto-approved', () => {
  const result = evaluateAdoptionReadiness(readyDossier);
  assert.equal(result.status, 'READY_FOR_HUMAN_REVIEW');
  assert.equal(result.automaticApproval, false);
});

test('freezes on protected-scope mutation', () => {
  const result = evaluateAdoptionReadiness({ ...readyDossier, protectedScopeMutation: true });
  assert.equal(result.status, 'FREEZE');
  assert.ok(result.reasons.includes('PROTECTED_SCOPE_MUTATION'));
});

test('holds when overlap remains unresolved', () => {
  const result = evaluateAdoptionReadiness({
    ...readyDossier,
    collisionScan: { checked: true, unresolvedOverlapIds: ['existing-project'] }
  });
  assert.equal(result.status, 'HOLD');
  assert.ok(result.reasons.includes('UNRESOLVED_OVERLAP'));
});

test('holds when rollback proof is absent', () => {
  const result = evaluateAdoptionReadiness({
    ...readyDossier,
    rollback: { defined: true, verified: false }
  });
  assert.equal(result.status, 'HOLD');
  assert.ok(result.reasons.includes('ROLLBACK_NOT_VERIFIED'));
});
