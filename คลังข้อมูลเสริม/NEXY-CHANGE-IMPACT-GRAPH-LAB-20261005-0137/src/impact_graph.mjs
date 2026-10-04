import { createHash } from 'node:crypto';

export const SCHEMA_VERSION = 'nexy.cige.v1';

export const NODE_KINDS = Object.freeze([
  'requirement',
  'contract',
  'module',
  'config',
  'artifact',
  'test',
  'evidence'
]);

export const EDGE_TYPES = Object.freeze([
  'depends_on',
  'implements',
  'verifies',
  'derived_from',
  'governed_by',
  'uses'
]);

export const DEFAULT_LIMITS = Object.freeze({
  maxNodes: 10000,
  maxEdges: 50000,
  maxImpactedNodes: 10000
});

const HARD_CYCLE_TYPES = new Set(['depends_on', 'derived_from', 'governed_by']);
const REVALIDATION_KINDS = new Set(['test', 'evidence']);

function compareText(a, b) {
  return a < b ? -1 : a > b ? 1 : 0;
}

function sortedUnique(values) {
  return [...new Set(values)].sort(compareText);
}

function normalizeNode(node) {
  return {
    id: node.id,
    kind: node.kind,
    critical: node.critical === true,
    ...(node.label === undefined ? {} : { label: String(node.label) }),
    ...(node.metadata === undefined ? {} : { metadata: canonicalize(node.metadata) })
  };
}

function normalizeEdge(edge) {
  return {
    from: edge.from,
    to: edge.to,
    type: edge.type
  };
}

export function canonicalize(value) {
  if (Array.isArray(value)) {
    return value.map(canonicalize);
  }
  if (value && typeof value === 'object') {
    const out = {};
    for (const key of Object.keys(value).sort(compareText)) {
      out[key] = canonicalize(value[key]);
    }
    return out;
  }
  return value;
}

export function stableStringify(value) {
  return JSON.stringify(canonicalize(value));
}

export function sha256Hex(value) {
  return createHash('sha256').update(value, 'utf8').digest('hex');
}

function freeze(reasonCode, details = {}) {
  return {
    status: 'FREEZE',
    reason_code: reasonCode,
    details: canonicalize(details)
  };
}

function assertPlainObject(value, name) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) {
    return `${name} must be an object`;
  }
  return null;
}

export function validateGraph(graph, limits = DEFAULT_LIMITS) {
  const objectError = assertPlainObject(graph, 'graph');
  if (objectError) return freeze('SCHEMA_VIOLATION', { errors: [objectError] });

  const errors = [];
  if (graph.schema_version !== SCHEMA_VERSION) {
    errors.push(`schema_version must equal ${SCHEMA_VERSION}`);
  }
  if (!Array.isArray(graph.nodes)) errors.push('nodes must be an array');
  if (!Array.isArray(graph.edges)) errors.push('edges must be an array');
  if (errors.length) return freeze('SCHEMA_VIOLATION', { errors: errors.sort(compareText) });

  if (!Number.isInteger(limits.maxNodes) || limits.maxNodes <= 0 ||
      !Number.isInteger(limits.maxEdges) || limits.maxEdges <= 0 ||
      !Number.isInteger(limits.maxImpactedNodes) || limits.maxImpactedNodes <= 0) {
    return freeze('INVALID_LIMITS', { limits });
  }

  if (graph.nodes.length > limits.maxNodes || graph.edges.length > limits.maxEdges) {
    return freeze('GRAPH_LIMIT_EXCEEDED', {
      node_count: graph.nodes.length,
      edge_count: graph.edges.length,
      limits
    });
  }

  const nodeIds = new Set();
  const nodeKinds = new Set(NODE_KINDS);
  for (const [index, node] of graph.nodes.entries()) {
    if (!node || typeof node !== 'object' || Array.isArray(node)) {
      errors.push(`nodes[${index}] must be an object`);
      continue;
    }
    if (typeof node.id !== 'string' || node.id.trim() === '') {
      errors.push(`nodes[${index}].id must be a non-empty string`);
    } else if (nodeIds.has(node.id)) {
      errors.push(`duplicate node id: ${node.id}`);
    } else {
      nodeIds.add(node.id);
    }
    if (!nodeKinds.has(node.kind)) {
      errors.push(`nodes[${index}].kind is unsupported: ${String(node.kind)}`);
    }
    if (node.critical !== undefined && typeof node.critical !== 'boolean') {
      errors.push(`nodes[${index}].critical must be boolean when present`);
    }
  }

  const edgeTypes = new Set(EDGE_TYPES);
  const edgeKeys = new Set();
  for (const [index, edge] of graph.edges.entries()) {
    if (!edge || typeof edge !== 'object' || Array.isArray(edge)) {
      errors.push(`edges[${index}] must be an object`);
      continue;
    }
    if (typeof edge.from !== 'string' || !nodeIds.has(edge.from)) {
      errors.push(`edges[${index}].from references unknown node: ${String(edge.from)}`);
    }
    if (typeof edge.to !== 'string' || !nodeIds.has(edge.to)) {
      errors.push(`edges[${index}].to references unknown node: ${String(edge.to)}`);
    }
    if (!edgeTypes.has(edge.type)) {
      errors.push(`edges[${index}].type is unsupported: ${String(edge.type)}`);
    }
    const key = `${edge.from}\u0000${edge.type}\u0000${edge.to}`;
    if (edgeKeys.has(key)) errors.push(`duplicate edge: ${edge.from} -[${edge.type}]-> ${edge.to}`);
    edgeKeys.add(key);
  }

  if (errors.length) return freeze('SCHEMA_VIOLATION', { errors: errors.sort(compareText) });

  const cycle = findHardDependencyCycle(graph);
  if (cycle) return freeze('DEPENDENCY_CYCLE', { cycle });

  return { status: 'PASS' };
}

function findHardDependencyCycle(graph) {
  const adjacency = new Map(graph.nodes.map((node) => [node.id, []]));
  for (const edge of graph.edges) {
    if (HARD_CYCLE_TYPES.has(edge.type)) adjacency.get(edge.from).push(edge.to);
  }
  for (const list of adjacency.values()) list.sort(compareText);

  const state = new Map();
  const stack = [];
  const stackIndex = new Map();

  const visit = (nodeId) => {
    state.set(nodeId, 1);
    stackIndex.set(nodeId, stack.length);
    stack.push(nodeId);

    for (const next of adjacency.get(nodeId)) {
      const nextState = state.get(next) ?? 0;
      if (nextState === 0) {
        const found = visit(next);
        if (found) return found;
      } else if (nextState === 1) {
        const start = stackIndex.get(next);
        return [...stack.slice(start), next];
      }
    }

    stack.pop();
    stackIndex.delete(nodeId);
    state.set(nodeId, 2);
    return null;
  };

  for (const nodeId of [...adjacency.keys()].sort(compareText)) {
    if ((state.get(nodeId) ?? 0) === 0) {
      const found = visit(nodeId);
      if (found) return found;
    }
  }
  return null;
}

export function normalizeGraph(graph) {
  return {
    schema_version: SCHEMA_VERSION,
    nodes: graph.nodes
      .map(normalizeNode)
      .sort((a, b) => compareText(a.id, b.id) || compareText(a.kind, b.kind)),
    edges: graph.edges
      .map(normalizeEdge)
      .sort((a, b) => compareText(a.from, b.from) || compareText(a.type, b.type) || compareText(a.to, b.to))
  };
}

export function graphDigest(graph) {
  return sha256Hex(stableStringify(normalizeGraph(graph)));
}

function buildReverseAdjacency(graph) {
  const reverse = new Map(graph.nodes.map((node) => [node.id, []]));
  for (const edge of graph.edges) {
    reverse.get(edge.to).push({ consumer: edge.from, type: edge.type });
  }
  for (const list of reverse.values()) {
    list.sort((a, b) => compareText(a.consumer, b.consumer) || compareText(a.type, b.type));
  }
  return reverse;
}

function verifierCoverageForCriticalChanged(changedId, reverse, nodeById) {
  const queue = [changedId];
  const visited = new Set([changedId]);
  const verifiers = [];

  for (let index = 0; index < queue.length; index += 1) {
    const current = queue[index];
    for (const incoming of reverse.get(current)) {
      if (visited.has(incoming.consumer)) continue;
      visited.add(incoming.consumer);
      queue.push(incoming.consumer);
      const node = nodeById.get(incoming.consumer);
      if (REVALIDATION_KINDS.has(node.kind)) verifiers.push(node.id);
    }
  }
  return sortedUnique(verifiers);
}

export function analyzeImpact(graph, changedIds, options = {}) {
  const limits = { ...DEFAULT_LIMITS, ...(options.limits ?? {}) };
  const validation = validateGraph(graph, limits);
  if (validation.status !== 'PASS') return validation;

  if (!Array.isArray(changedIds) || changedIds.length === 0 || changedIds.some((id) => typeof id !== 'string' || id.trim() === '')) {
    return freeze('INVALID_CHANGE_SET', { changed_ids: changedIds });
  }

  const nodeById = new Map(graph.nodes.map((node) => [node.id, node]));
  const changed = sortedUnique(changedIds);
  const unknownChanged = changed.filter((id) => !nodeById.has(id));
  if (unknownChanged.length) return freeze('UNKNOWN_CHANGED_NODE', { unknown_changed_nodes: unknownChanged });

  const reverse = buildReverseAdjacency(graph);
  const queue = changed.map((id) => ({ id, distance: 0 }));
  const visited = new Set(changed);
  const distance = new Map(changed.map((id) => [id, 0]));
  const cause = new Map();
  const causeEdge = new Map();

  for (let index = 0; index < queue.length; index += 1) {
    const current = queue[index];
    for (const incoming of reverse.get(current.id)) {
      if (visited.has(incoming.consumer)) continue;
      if (visited.size >= limits.maxImpactedNodes) {
        return freeze('IMPACT_LIMIT_EXCEEDED', {
          limit: limits.maxImpactedNodes,
          observed_minimum: visited.size + 1
        });
      }
      visited.add(incoming.consumer);
      distance.set(incoming.consumer, current.distance + 1);
      cause.set(incoming.consumer, current.id);
      causeEdge.set(incoming.consumer, incoming.type);
      queue.push({ id: incoming.consumer, distance: current.distance + 1 });
    }
  }

  const impactedIds = [...visited].filter((id) => !changed.includes(id)).sort(compareText);
  const impacted = impactedIds.map((id) => ({
    id,
    kind: nodeById.get(id).kind,
    distance: distance.get(id),
    via_edge_type: causeEdge.get(id),
    cause_path: buildCausePath(id, cause)
  }));

  const requiredRevalidation = impacted
    .filter((entry) => REVALIDATION_KINDS.has(entry.kind))
    .map((entry) => ({ id: entry.id, kind: entry.kind, cause_path: entry.cause_path }));

  const criticalCoverageGaps = [];
  for (const id of changed) {
    const node = nodeById.get(id);
    if (!node.critical) continue;
    const verifiers = verifierCoverageForCriticalChanged(id, reverse, nodeById);
    if (verifiers.length === 0) criticalCoverageGaps.push(id);
  }

  const normalized = normalizeGraph(graph);
  const output = {
    status: criticalCoverageGaps.length ? 'FREEZE' : 'PASS',
    schema_version: SCHEMA_VERSION,
    graph_digest: sha256Hex(stableStringify(normalized)),
    change_set_digest: sha256Hex(stableStringify(changed)),
    changed_nodes: changed,
    impacted_nodes: impacted,
    required_revalidation: requiredRevalidation,
    critical_coverage_gaps: criticalCoverageGaps,
    summary: {
      node_count: graph.nodes.length,
      edge_count: graph.edges.length,
      changed_count: changed.length,
      impacted_count: impacted.length,
      revalidation_count: requiredRevalidation.length
    }
  };

  if (criticalCoverageGaps.length) {
    output.reason_code = 'EVIDENCE_MISSING';
  }
  return output;
}

function buildCausePath(start, cause) {
  const path = [start];
  let current = start;
  while (cause.has(current)) {
    current = cause.get(current);
    path.push(current);
  }
  return path;
}
