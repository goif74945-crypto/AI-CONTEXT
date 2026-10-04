import test from 'node:test';
import assert from 'node:assert/strict';
import { planReversibleProbes } from '../dist/reversible_probe.js';

test('chooses the minimum-cost safe probe cover deterministically', () => {
  const result = planReversibleProbes({
    unknowns: [
      { id: 'u1', blocking: true },
      { id: 'u2', blocking: true }
    ],
    availableAuthorities: ['OPERATOR'],
    probes: [
      { id: 'p-both', resolves: ['u1', 'u2'], effect: 'READ_ONLY', cost: 3, requiredAuthority: 'NONE' },
      { id: 'p-u1', resolves: ['u1'], effect: 'READ_ONLY', cost: 1, requiredAuthority: 'NONE' },
      { id: 'p-u2', resolves: ['u2'], effect: 'REVERSIBLE_WRITE', cost: 1, requiredAuthority: 'OPERATOR', rollback: 'restore snapshot' }
    ]
  });
  assert.equal(result.status, 'PROBE');
  assert.deepEqual(result.selectedProbeIds, ['p-u1', 'p-u2']);
  assert.equal(result.totalCost, 2);
});

test('never selects irreversible probes', () => {
  const result = planReversibleProbes({
    unknowns: [{ id: 'u1', blocking: true }],
    availableAuthorities: ['OWNER'],
    probes: [
      { id: 'danger', resolves: ['u1'], effect: 'IRREVERSIBLE', cost: 1, requiredAuthority: 'OWNER' }
    ]
  });
  assert.equal(result.status, 'BLOCKED');
  assert.ok(result.rejectedProbes.some((x) => x.probeId === 'danger' && x.reason === 'IRREVERSIBLE_EFFECT'));
});

test('rejects reversible writes that have no rollback', () => {
  const result = planReversibleProbes({
    unknowns: [{ id: 'u1', blocking: true }],
    availableAuthorities: ['OPERATOR'],
    probes: [
      { id: 'unsafe-reversible', resolves: ['u1'], effect: 'REVERSIBLE_WRITE', cost: 1, requiredAuthority: 'OPERATOR' }
    ]
  });
  assert.equal(result.status, 'BLOCKED');
  assert.ok(result.rejectedProbes.some((x) => x.reason === 'MISSING_ROLLBACK'));
});

test('returns READY when no blocking unknown exists', () => {
  const result = planReversibleProbes({
    unknowns: [{ id: 'u1', blocking: false }],
    availableAuthorities: [],
    probes: []
  });
  assert.equal(result.status, 'READY');
  assert.deepEqual(result.selectedProbeIds, []);
});
