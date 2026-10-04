import test from 'node:test';
import assert from 'node:assert/strict';
import { buildErasurePlan, verifyErasureReceipts, type DataGraph, type ErasureRequest } from '../src/index.ts';

const req: ErasureRequest = { requestId:'persist-001', subjectOwnerId:'u1', targetNodeId:'a', requestedAtTick:100n, mode:'HARD_ERASURE' };
const g = (nodes: DataGraph['nodes'], edges: DataGraph['edges'] = []): DataGraph => ({ nodes, edges });
const artifact = { id:'a', kind:'CANONICAL_ARTIFACT' as const, ownerId:'u1', mutable:true };

test('hard erasure destroys owned blob but tombstones immutable audit', () => {
  const plan = buildErasurePlan(g([
    artifact,
    { id:'b', kind:'BLOB', ownerId:'u1', mutable:true },
    { id:'log', kind:'AUDIT_LOG', ownerId:'system', mutable:false },
  ], [
    { from:'a', to:'b', relation:'CONTAINS_BLOB' },
    { from:'a', to:'log', relation:'AUDITS' },
  ]), req);
  assert.equal(plan.status, 'READY');
  assert.ok(plan.actions.some(x => x.kind === 'DESTROY_BLOB' && x.nodeId === 'b'));
  assert.ok(plan.actions.some(x => x.kind === 'APPEND_AUDIT_TOMBSTONE' && x.nodeId === 'log'));
  assert.ok(!plan.actions.some(x => x.kind === 'DELETE_IMMUTABLE_RECORD'));
});

test('soft delete never claims physical blob destruction', () => {
  const plan = buildErasurePlan(g([artifact,{ id:'b', kind:'BLOB', ownerId:'u1', mutable:true }],[{ from:'a', to:'b', relation:'CONTAINS_BLOB' }]), { ...req, mode:'SOFT_DELETE' });
  assert.equal(plan.status, 'READY');
  assert.ok(plan.actions.some(x => x.kind === 'REVOKE_ACCESS' && x.nodeId === 'b'));
  assert.ok(!plan.actions.some(x => x.kind === 'DESTROY_BLOB'));
});

test('retention hold produces PARTIAL_HOLD and blocks destruction', () => {
  const plan = buildErasurePlan(g([artifact,{ id:'b', kind:'BLOB', ownerId:'u1', mutable:true, retentionUntilTick:200n }],[{ from:'a', to:'b', relation:'CONTAINS_BLOB' }]), req);
  assert.equal(plan.status, 'PARTIAL_HOLD');
  assert.ok(plan.actions.some(x => x.kind === 'RETAIN_UNDER_HOLD' && x.nodeId === 'b'));
  assert.ok(!plan.actions.some(x => x.kind === 'DESTROY_BLOB'));
});

test('shared derivative rebuild preserves unrelated owners', () => {
  const plan = buildErasurePlan(g([
    artifact,
    { id:'other', kind:'CANONICAL_ARTIFACT', ownerId:'u2', mutable:true },
    { id:'shared', kind:'SHARED_DERIVED', ownerId:'system', mutable:true },
  ], [
    { from:'a', to:'shared', relation:'DERIVES' },
    { from:'other', to:'shared', relation:'DERIVES' },
  ]), req);
  const action = plan.actions.find(x => x.nodeId === 'shared');
  assert.equal(plan.status, 'READY');
  assert.equal(action?.kind, 'REBUILD_SHARED_DERIVED');
  assert.deepEqual(action?.removeSourceNodeIds, ['a']);
  assert.deepEqual(action?.preserveSourceNodeIds, ['other']);
});

test('cross-owner exclusive derivative freezes and denies execution', () => {
  const plan = buildErasurePlan(g([artifact,{ id:'foreign', kind:'DERIVED', ownerId:'u2', mutable:true }],[{ from:'a', to:'foreign', relation:'DERIVES' }]), req);
  assert.equal(plan.status, 'FREEZE');
  assert.equal(plan.executionAuthorized, false);
  assert.ok(plan.blockers.some(x => x.code === 'CROSS_OWNER_MUTATION'));
});

test('dangling edge freezes instead of guessing deletion coverage', () => {
  const plan = buildErasurePlan(g([artifact],[{ from:'a', to:'missing', relation:'DERIVES' }]), req);
  assert.equal(plan.status, 'FREEZE');
  assert.ok(plan.blockers.some(x => x.code === 'DANGLING_EDGE'));
});

test('cycle freezes instead of inventing unsafe order', () => {
  const plan = buildErasurePlan(g([artifact,{ id:'d', kind:'DERIVED', ownerId:'u1', mutable:true }],[
    { from:'a', to:'d', relation:'DERIVES' },
    { from:'d', to:'a', relation:'DERIVES' },
  ]), req);
  assert.equal(plan.status, 'FREEZE');
  assert.ok(plan.blockers.some(x => x.code === 'PROPAGATION_CYCLE'));
});

test('external export requires adapter and external evidence', () => {
  const plan = buildErasurePlan(g([artifact,{ id:'e', kind:'EXTERNAL_EXPORT', ownerId:'u1', mutable:true, externalSystem:'provider-x' }],[{ from:'a', to:'e', relation:'EXPORTS' }]), req);
  assert.equal(plan.status, 'PENDING_EXTERNAL');
  const action = plan.actions.find(x => x.nodeId === 'e');
  assert.equal(action?.kind, 'REQUEST_EXTERNAL_ERASURE');
  assert.equal(action?.requiredEvidence, 'EXTERNAL_ERASURE_RECEIPT');
});

test('plan identity is deterministic across graph ordering', () => {
  const nodes: DataGraph['nodes'] = [artifact,{ id:'b', kind:'BLOB', ownerId:'u1', mutable:true },{ id:'c', kind:'CACHE', ownerId:'u1', mutable:true }];
  const edges: DataGraph['edges'] = [{ from:'a', to:'b', relation:'CONTAINS_BLOB' },{ from:'a', to:'c', relation:'CACHES' }];
  const p1 = buildErasurePlan(g(nodes,edges), req);
  const p2 = buildErasurePlan(g([...nodes].reverse(),[...edges].reverse()), req);
  assert.equal(p1.planHash, p2.planHash);
  assert.deepEqual(p1.actions, p2.actions);
});

test('receipt verification is NOT_VERIFIED when evidence is incomplete', () => {
  const plan = buildErasurePlan(g([artifact,{ id:'b', kind:'BLOB', ownerId:'u1', mutable:true }],[{ from:'a', to:'b', relation:'CONTAINS_BLOB' }]), req);
  const action = plan.actions[0]!;
  const result = verifyErasureReceipts(plan,[{ actionId:action.actionId, planHash:plan.planHash, nodeId:action.nodeId, outcome:'APPLIED', evidenceHash:'a'.repeat(64) }]);
  assert.equal(result.status, 'NOT_VERIFIED');
});

test('receipt verification rejects stale plan hash', () => {
  const plan = buildErasurePlan(g([artifact]), req);
  const action = plan.actions[0]!;
  const result = verifyErasureReceipts(plan,[{ actionId:action.actionId, planHash:'f'.repeat(64), nodeId:action.nodeId, outcome:'APPLIED', evidenceHash:'a'.repeat(64) }]);
  assert.equal(result.status, 'FAIL');
});

test('all plan-bound receipts are required for PASS', () => {
  const plan = buildErasurePlan(g([artifact,{ id:'b', kind:'BLOB', ownerId:'u1', mutable:true }],[{ from:'a', to:'b', relation:'CONTAINS_BLOB' }]), req);
  const receipts = plan.actions.map((x,i) => ({ actionId:x.actionId, planHash:plan.planHash, nodeId:x.nodeId, outcome:'APPLIED' as const, evidenceHash:String(i+1).padStart(64,'0') }));
  assert.equal(verifyErasureReceipts(plan,receipts).status, 'PASS');
});
