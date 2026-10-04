import test from 'node:test';
import assert from 'node:assert/strict';
import { evaluateOutcomeClosure } from '../dist/outcome_closure.js';

test('closes only when every required predicate has enough evidence and no forbidden predicate fires', () => {
  const result = evaluateOutcomeClosure(
    { id: 'goal-1', required: ['artifact-exists', 'tests-pass'], forbidden: ['protected-repo-mutated'], minEvidencePerRequired: 1 },
    [
      { predicateId: 'tests-pass', status: 'SATISFIED', evidenceIds: ['e2'] },
      { predicateId: 'artifact-exists', status: 'SATISFIED', evidenceIds: ['e1'] },
      { predicateId: 'protected-repo-mutated', status: 'VIOLATED', evidenceIds: ['e3'] }
    ]
  );
  assert.equal(result.status, 'CLOSED');
  assert.deepEqual(result.openRequired, []);
});

test('stays open when evidence is missing', () => {
  const result = evaluateOutcomeClosure(
    { id: 'goal-2', required: ['tests-pass'], forbidden: [], minEvidencePerRequired: 2 },
    [{ predicateId: 'tests-pass', status: 'SATISFIED', evidenceIds: ['only-one'] }]
  );
  assert.equal(result.status, 'OPEN');
  assert.deepEqual(result.evidenceDeficits, ['tests-pass']);
});

test('freezes when a forbidden condition is satisfied', () => {
  const result = evaluateOutcomeClosure(
    { id: 'goal-3', required: ['done'], forbidden: ['protected-write'], minEvidencePerRequired: 1 },
    [
      { predicateId: 'done', status: 'SATISFIED', evidenceIds: ['e1'] },
      { predicateId: 'protected-write', status: 'SATISFIED', evidenceIds: ['e2'] }
    ]
  );
  assert.equal(result.status, 'FREEZE');
  assert.deepEqual(result.triggeredForbidden, ['protected-write']);
});

test('is deterministic across input ordering', () => {
  const contract = { id: 'goal-4', required: ['a', 'b'], forbidden: ['z'], minEvidencePerRequired: 1 };
  const a = evaluateOutcomeClosure(contract, [
    { predicateId: 'a', status: 'SATISFIED', evidenceIds: ['x'] },
    { predicateId: 'b', status: 'SATISFIED', evidenceIds: ['y'] },
    { predicateId: 'z', status: 'VIOLATED', evidenceIds: ['n'] }
  ]);
  const b = evaluateOutcomeClosure(contract, [
    { predicateId: 'z', status: 'VIOLATED', evidenceIds: ['n'] },
    { predicateId: 'b', status: 'SATISFIED', evidenceIds: ['y'] },
    { predicateId: 'a', status: 'SATISFIED', evidenceIds: ['x'] }
  ]);
  assert.equal(a.fingerprint, b.fingerprint);
});
