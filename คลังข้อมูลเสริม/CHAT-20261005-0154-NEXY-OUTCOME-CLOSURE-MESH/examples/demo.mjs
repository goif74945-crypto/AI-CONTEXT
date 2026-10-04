import {
  evaluateOutcomeClosure,
  summarizeProgress,
  planReversibleProbes,
  judgeBenefitRegression,
  evaluateAdoptionReadiness
} from '../dist/index.js';

const probe = planReversibleProbes({
  unknowns: [{ id: 'fresh-runtime-proof', blocking: true }],
  availableAuthorities: [],
  probes: [{ id: 'read-ci', resolves: ['fresh-runtime-proof'], effect: 'READ_ONLY', cost: 1, requiredAuthority: 'NONE' }]
});

const outcome = evaluateOutcomeClosure(
  { id: 'nocm-demo', required: ['design', 'code', 'tests'], forbidden: ['protected-write'], minEvidencePerRequired: 1 },
  [
    { predicateId: 'design', status: 'SATISFIED', evidenceIds: ['spec'] },
    { predicateId: 'code', status: 'SATISFIED', evidenceIds: ['source'] },
    { predicateId: 'tests', status: 'SATISFIED', evidenceIds: ['runtime-test'] },
    { predicateId: 'protected-write', status: 'VIOLATED', evidenceIds: ['repo-diff-audit'] }
  ]
);

const progress = summarizeProgress([
  { id: 'design', status: 'PASS' },
  { id: 'code', status: 'PASS' },
  { id: 'tests', status: 'PASS' }
]);

const benefit = judgeBenefitRegression(
  [{ id: 'manual_checks', direction: 'LOWER', critical: false, minImprovement: 1, maxRegression: 0 }],
  { manual_checks: 5 },
  { manual_checks: 3 }
);

const adoption = evaluateAdoptionReadiness({
  proposalId: 'nocm-demo',
  collisionScan: { checked: true, unresolvedOverlapIds: [] },
  compatibility: [{ id: 'supplemental-adapter-boundary', status: 'PASS' }],
  evidenceClassesPresent: ['E0', 'E1', 'E2'],
  requiredEvidenceClasses: ['E0', 'E1', 'E2'],
  rollback: { defined: true, verified: true },
  protectedScopeMutation: false,
  outcomeStatus: outcome.status,
  progressStatus: progress.aggregate,
  benefitStatus: benefit.status
});

console.log(JSON.stringify({ probe, outcome, progress, benefit, adoption }, null, 2));
