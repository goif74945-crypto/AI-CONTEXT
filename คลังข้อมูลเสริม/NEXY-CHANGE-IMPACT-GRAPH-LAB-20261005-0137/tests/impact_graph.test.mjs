import test from 'node:test';
import assert from 'node:assert/strict';
import {
  SCHEMA_VERSION,
  analyzeImpact,
  graphDigest,
  normalizeGraph,
  stableStringify,
  validateGraph
} from '../src/impact_graph.mjs';

function graph(nodes, edges) {
  return { schema_version: SCHEMA_VERSION, nodes, edges };
}

const baseGraph = graph(
  [
    { id: 'REQ-A', kind: 'requirement', critical: true },
    { id: 'CONTRACT-A', kind: 'contract' },
    { id: 'MODULE-A', kind: 'module' },
    { id: 'API-A', kind: 'artifact' },
    { id: 'TEST-A', kind: 'test' },
    { id: 'TEST-API', kind: 'test' },
    { id: 'EVIDENCE-A', kind: 'evidence' }
  ],
  [
    { from: 'CONTRACT-A', to: 'REQ-A', type: 'derived_from' },
    { from: 'MODULE-A', to: 'CONTRACT-A', type: 'implements' },
    { from: 'API-A', to: 'MODULE-A', type: 'depends_on' },
    { from: 'TEST-A', to: 'MODULE-A', type: 'verifies' },
    { from: 'TEST-API', to: 'API-A', type: 'verifies' },
    { from: 'EVIDENCE-A', to: 'TEST-A', type: 'derived_from' }
  ]
);

test('valid graph passes static validation', () => {
  assert.deepEqual(validateGraph(baseGraph), { status: 'PASS' });
});

test('changing a requirement deterministically propagates to consumers and verifiers', () => {
  const result = analyzeImpact(baseGraph, ['REQ-A']);
  assert.equal(result.status, 'PASS');
  assert.deepEqual(result.changed_nodes, ['REQ-A']);
  assert.deepEqual(result.impacted_nodes.map((x) => x.id), [
    'API-A', 'CONTRACT-A', 'EVIDENCE-A', 'MODULE-A', 'TEST-A', 'TEST-API'
  ]);
  assert.deepEqual(result.required_revalidation.map((x) => x.id), ['EVIDENCE-A', 'TEST-A', 'TEST-API']);
  assert.deepEqual(
    result.impacted_nodes.find((x) => x.id === 'TEST-API').cause_path,
    ['TEST-API', 'API-A', 'MODULE-A', 'CONTRACT-A', 'REQ-A']
  );
});

test('same semantic graph order produces identical digest and output', () => {
  const reordered = graph([...baseGraph.nodes].reverse(), [...baseGraph.edges].reverse());
  assert.equal(graphDigest(reordered), graphDigest(baseGraph));
  assert.equal(stableStringify(analyzeImpact(reordered, ['REQ-A'])), stableStringify(analyzeImpact(baseGraph, ['REQ-A'])));
});

test('unknown changed node freezes rather than guessing', () => {
  const result = analyzeImpact(baseGraph, ['REQ-NOT-THERE']);
  assert.equal(result.status, 'FREEZE');
  assert.equal(result.reason_code, 'UNKNOWN_CHANGED_NODE');
  assert.deepEqual(result.details.unknown_changed_nodes, ['REQ-NOT-THERE']);
});

test('critical changed node without test/evidence coverage freezes', () => {
  const uncovered = graph(
    [
      { id: 'REQ-X', kind: 'requirement', critical: true },
      { id: 'MODULE-X', kind: 'module' }
    ],
    [{ from: 'MODULE-X', to: 'REQ-X', type: 'implements' }]
  );
  const result = analyzeImpact(uncovered, ['REQ-X']);
  assert.equal(result.status, 'FREEZE');
  assert.equal(result.reason_code, 'EVIDENCE_MISSING');
  assert.deepEqual(result.critical_coverage_gaps, ['REQ-X']);
});

test('hard dependency cycle freezes with deterministic cycle evidence', () => {
  const cyclic = graph(
    [
      { id: 'A', kind: 'module' },
      { id: 'B', kind: 'module' },
      { id: 'C', kind: 'module' }
    ],
    [
      { from: 'A', to: 'B', type: 'depends_on' },
      { from: 'B', to: 'C', type: 'depends_on' },
      { from: 'C', to: 'A', type: 'depends_on' }
    ]
  );
  const result = validateGraph(cyclic);
  assert.equal(result.status, 'FREEZE');
  assert.equal(result.reason_code, 'DEPENDENCY_CYCLE');
  assert.deepEqual(result.details.cycle, ['A', 'B', 'C', 'A']);
});

test('duplicate node, bad edge and unsupported kind freeze as schema violation', () => {
  const invalid = graph(
    [
      { id: 'A', kind: 'module' },
      { id: 'A', kind: 'unknown-kind' }
    ],
    [{ from: 'A', to: 'MISSING', type: 'magic' }]
  );
  const result = validateGraph(invalid);
  assert.equal(result.status, 'FREEZE');
  assert.equal(result.reason_code, 'SCHEMA_VIOLATION');
  assert.ok(result.details.errors.length >= 3);
});

test('graph size limits freeze before traversal', () => {
  const result = validateGraph(baseGraph, { maxNodes: 2, maxEdges: 2, maxImpactedNodes: 2 });
  assert.equal(result.status, 'FREEZE');
  assert.equal(result.reason_code, 'GRAPH_LIMIT_EXCEEDED');
});

test('impact traversal limit freezes instead of truncating output', () => {
  const result = analyzeImpact(baseGraph, ['REQ-A'], {
    limits: { maxNodes: 100, maxEdges: 100, maxImpactedNodes: 3 }
  });
  assert.equal(result.status, 'FREEZE');
  assert.equal(result.reason_code, 'IMPACT_LIMIT_EXCEEDED');
});

test('normalization strips irrelevant property order but retains canonical metadata', () => {
  const g = graph(
    [{ id: 'A', kind: 'module', metadata: { z: 1, a: { y: 2, x: 3 } } }],
    []
  );
  const normalized = normalizeGraph(g);
  assert.equal(stableStringify(normalized.nodes[0].metadata), '{"a":{"x":3,"y":2},"z":1}');
});

test('multiple changed nodes collapse duplicate impact deterministically', () => {
  const result = analyzeImpact(baseGraph, ['MODULE-A', 'REQ-A', 'MODULE-A']);
  assert.equal(result.status, 'PASS');
  assert.deepEqual(result.changed_nodes, ['MODULE-A', 'REQ-A']);
  assert.deepEqual(result.impacted_nodes.map((x) => x.id), ['API-A', 'CONTRACT-A', 'EVIDENCE-A', 'TEST-A', 'TEST-API']);
});

test('noncritical uncovered change may pass while still reporting zero revalidation', () => {
  const isolated = graph([{ id: 'DOC-X', kind: 'artifact', critical: false }], []);
  const result = analyzeImpact(isolated, ['DOC-X']);
  assert.equal(result.status, 'PASS');
  assert.equal(result.summary.impacted_count, 0);
  assert.equal(result.summary.revalidation_count, 0);
});

test('invalid limits freeze explicitly', () => {
  const result = analyzeImpact(baseGraph, ['REQ-A'], {
    limits: { maxNodes: 0, maxEdges: 100, maxImpactedNodes: 100 }
  });
  assert.equal(result.status, 'FREEZE');
  assert.equal(result.reason_code, 'INVALID_LIMITS');
});

test('change set digest is independent of duplicate and input order', () => {
  const a = analyzeImpact(baseGraph, ['REQ-A', 'MODULE-A']);
  const b = analyzeImpact(baseGraph, ['MODULE-A', 'REQ-A', 'REQ-A']);
  assert.equal(a.change_set_digest, b.change_set_digest);
});
