import { sha256Canonical, stableActionId } from './canonical.ts';
import type {
  DataEdge,
  DataGraph,
  DataNode,
  ErasureAction,
  ErasureActionKind,
  ErasurePlan,
  ErasureRequest,
  PlanBlocker,
  PlanStatus,
  RequiredEvidence,
} from './types.ts';

const RELATION_ORDER: Record<DataEdge['relation'], number> = {
  CONTAINS_BLOB: 10,
  DERIVES: 20,
  CACHES: 30,
  INDEXES: 40,
  EXPORTS: 50,
  AUDITS: 90,
};

const ACTION_ORDER: Record<ErasureActionKind, number> = {
  REVOKE_ACCESS: 10,
  RETAIN_UNDER_HOLD: 20,
  DESTROY_BLOB: 30,
  DELETE_DERIVED: 40,
  REBUILD_SHARED_DERIVED: 40,
  INVALIDATE_CACHE: 50,
  REMOVE_INDEX_ENTRY: 60,
  REQUEST_EXTERNAL_ERASURE: 70,
  APPEND_AUDIT_TOMBSTONE: 90,
  DELETE_IMMUTABLE_RECORD: 100,
};

const MUTATING_KINDS = new Set<ErasureActionKind>([
  'REVOKE_ACCESS',
  'DESTROY_BLOB',
  'DELETE_DERIVED',
  'INVALIDATE_CACHE',
  'REMOVE_INDEX_ENTRY',
  'REBUILD_SHARED_DERIVED',
]);

function compareEdges(a: DataEdge, b: DataEdge): number {
  return RELATION_ORDER[a.relation] - RELATION_ORDER[b.relation]
    || a.to.localeCompare(b.to)
    || a.from.localeCompare(b.from);
}

function compareBlockers(a: PlanBlocker, b: PlanBlocker): number {
  return a.code.localeCompare(b.code)
    || (a.nodeId ?? '').localeCompare(b.nodeId ?? '')
    || a.detail.localeCompare(b.detail);
}

function compareActions(a: ErasureAction, b: ErasureAction): number {
  return ACTION_ORDER[a.kind] - ACTION_ORDER[b.kind]
    || a.nodeId.localeCompare(b.nodeId)
    || a.actionId.localeCompare(b.actionId);
}

function held(node: DataNode, tick: bigint): boolean {
  return node.legalHold === true
    || (node.retentionUntilTick !== undefined && node.retentionUntilTick > tick);
}

function evidenceFor(kind: ErasureActionKind): RequiredEvidence {
  switch (kind) {
    case 'REVOKE_ACCESS': return 'ACCESS_REVOCATION_RECEIPT';
    case 'DESTROY_BLOB': return 'BLOB_DESTRUCTION_RECEIPT';
    case 'DELETE_DERIVED': return 'DERIVED_DELETE_RECEIPT';
    case 'INVALIDATE_CACHE': return 'CACHE_INVALIDATION_RECEIPT';
    case 'REMOVE_INDEX_ENTRY': return 'INDEX_REMOVAL_RECEIPT';
    case 'REBUILD_SHARED_DERIVED': return 'REBUILD_RECEIPT';
    case 'APPEND_AUDIT_TOMBSTONE': return 'AUDIT_TOMBSTONE_RECEIPT';
    case 'RETAIN_UNDER_HOLD': return 'HOLD_EVIDENCE';
    case 'REQUEST_EXTERNAL_ERASURE': return 'EXTERNAL_ERASURE_RECEIPT';
    case 'DELETE_IMMUTABLE_RECORD': return 'DERIVED_DELETE_RECEIPT';
  }
}

function makeAction(
  request: ErasureRequest,
  kind: ErasureActionKind,
  nodeId: string,
  reason: string,
  extra: Pick<ErasureAction, 'removeSourceNodeIds' | 'preserveSourceNodeIds'> = {},
): ErasureAction {
  const core = {
    requestId: request.requestId,
    mode: request.mode,
    kind,
    nodeId,
    removeSourceNodeIds: extra.removeSourceNodeIds?.slice().sort(),
    preserveSourceNodeIds: extra.preserveSourceNodeIds?.slice().sort(),
  };
  return {
    actionId: stableActionId(core),
    kind,
    nodeId,
    reason,
    requiredEvidence: evidenceFor(kind),
    ...(core.removeSourceNodeIds ? { removeSourceNodeIds: core.removeSourceNodeIds } : {}),
    ...(core.preserveSourceNodeIds ? { preserveSourceNodeIds: core.preserveSourceNodeIds } : {}),
  };
}

function findCycle(
  reachable: Set<string>,
  outgoing: Map<string, DataEdge[]>,
): string[] | null {
  const visiting = new Set<string>();
  const visited = new Set<string>();
  const stack: string[] = [];

  const dfs = (id: string): string[] | null => {
    if (visiting.has(id)) {
      const start = stack.indexOf(id);
      return [...stack.slice(start), id];
    }
    if (visited.has(id)) return null;

    visiting.add(id);
    stack.push(id);
    for (const edge of (outgoing.get(id) ?? []).filter(e => e.relation !== 'AUDITS').sort(compareEdges)) {
      if (!reachable.has(edge.to)) continue;
      const cycle = dfs(edge.to);
      if (cycle) return cycle;
    }
    stack.pop();
    visiting.delete(id);
    visited.add(id);
    return null;
  };

  for (const id of [...reachable].sort()) {
    const cycle = dfs(id);
    if (cycle) return cycle;
  }
  return null;
}

export function buildErasurePlan(graph: DataGraph, request: ErasureRequest): ErasurePlan {
  const blockers: PlanBlocker[] = [];
  const nodeById = new Map<string, DataNode>();
  const duplicateIds = new Set<string>();

  for (const node of graph.nodes) {
    if (nodeById.has(node.id)) duplicateIds.add(node.id);
    else nodeById.set(node.id, node);
  }
  for (const id of [...duplicateIds].sort()) {
    blockers.push({ code: 'DUPLICATE_NODE_ID', nodeId: id, detail: `Duplicate graph node id: ${id}` });
  }

  const target = nodeById.get(request.targetNodeId);
  if (!target) {
    blockers.push({ code: 'TARGET_NOT_FOUND', nodeId: request.targetNodeId, detail: 'Erasure target is absent from the provenance graph' });
    return finalize(request, [], blockers, false, false);
  }
  if (target.ownerId !== request.subjectOwnerId) {
    blockers.push({ code: 'TARGET_OWNER_MISMATCH', nodeId: target.id, detail: `Target owner ${target.ownerId} does not match erasure subject ${request.subjectOwnerId}` });
  }

  const outgoing = new Map<string, DataEdge[]>();
  const incoming = new Map<string, DataEdge[]>();
  for (const edge of graph.edges) {
    const out = outgoing.get(edge.from) ?? [];
    out.push(edge);
    outgoing.set(edge.from, out);
    const inc = incoming.get(edge.to) ?? [];
    inc.push(edge);
    incoming.set(edge.to, inc);
  }

  const reachable = new Set<string>();
  const queue = [target.id];
  while (queue.length > 0) {
    const id = queue.shift()!;
    if (reachable.has(id)) continue;
    reachable.add(id);

    for (const edge of (outgoing.get(id) ?? []).slice().sort(compareEdges)) {
      if (!nodeById.has(edge.to)) {
        blockers.push({ code: 'DANGLING_EDGE', nodeId: edge.to, detail: `Reachable ${edge.relation} edge ${edge.from} -> ${edge.to} has no target node` });
        continue;
      }
      if (!reachable.has(edge.to)) queue.push(edge.to);
    }
  }

  const cycle = findCycle(reachable, outgoing);
  if (cycle) {
    blockers.push({ code: 'PROPAGATION_CYCLE', nodeId: cycle[0]!, detail: `Erasure propagation cycle: ${cycle.join(' -> ')}` });
  }

  const actions: ErasureAction[] = [];
  let hasHold = false;
  let hasExternal = false;

  for (const id of [...reachable].sort()) {
    const node = nodeById.get(id)!;

    const ownerAllowed = node.ownerId === request.subjectOwnerId
      || node.kind === 'AUDIT_LOG'
      || node.kind === 'SHARED_DERIVED';
    if (!ownerAllowed) {
      blockers.push({ code: 'CROSS_OWNER_MUTATION', nodeId: node.id, detail: `Refusing automatic mutation of ${node.kind} owned by ${node.ownerId}` });
      continue;
    }

    const isHeld = held(node, request.requestedAtTick);

    if (node.kind === 'CANONICAL_ARTIFACT') {
      actions.push(makeAction(request, 'REVOKE_ACCESS', node.id, 'Sever user-facing access before any downstream erasure action'));
      if (isHeld) {
        hasHold = true;
        actions.push(makeAction(request, 'RETAIN_UNDER_HOLD', node.id, 'Artifact metadata is retained under active legal/retention hold'));
      }
      continue;
    }

    if (node.kind === 'AUDIT_LOG') {
      actions.push(makeAction(request, 'APPEND_AUDIT_TOMBSTONE', node.id, 'Preserve immutable audit history and append a non-secret erasure tombstone instead of mutating prior log records'));
      continue;
    }

    if (isHeld) {
      hasHold = true;
      actions.push(makeAction(request, 'RETAIN_UNDER_HOLD', node.id, 'Active legal/retention hold blocks destructive mutation while preserving erasure intent'));
      continue;
    }

    if (node.kind === 'SHARED_DERIVED') {
      const sourceEdges = (incoming.get(node.id) ?? []).filter(e => e.relation === 'DERIVES');
      const missingSources = sourceEdges.filter(e => !nodeById.has(e.from));
      if (missingSources.length > 0) {
        blockers.push({ code: 'SHARED_PROVENANCE_INCOMPLETE', nodeId: node.id, detail: 'Shared derivative cannot be safely rebuilt because at least one provenance source node is missing' });
        continue;
      }
      const removeSourceNodeIds = sourceEdges.map(e => e.from).filter(sourceId => reachable.has(sourceId)).sort();
      const preserveSourceNodeIds = sourceEdges.map(e => e.from).filter(sourceId => !reachable.has(sourceId)).sort();
      if (removeSourceNodeIds.length === 0) {
        blockers.push({ code: 'SHARED_PROVENANCE_INCOMPLETE', nodeId: node.id, detail: 'Shared derivative is reachable but no removable provenance source can be established' });
        continue;
      }
      actions.push(makeAction(
        request,
        'REBUILD_SHARED_DERIVED',
        node.id,
        'Recompute shared derivative without the erased source while preserving unrelated principals data',
        { removeSourceNodeIds, preserveSourceNodeIds },
      ));
      continue;
    }

    let actionKind: ErasureActionKind;
    let reason: string;
    switch (node.kind) {
      case 'BLOB':
        actionKind = request.mode === 'HARD_ERASURE' ? 'DESTROY_BLOB' : 'REVOKE_ACCESS';
        reason = request.mode === 'HARD_ERASURE'
          ? 'Destroy content-bearing blob after access revocation'
          : 'Soft deletion revokes blob access without claiming physical destruction';
        break;
      case 'DERIVED':
        actionKind = request.mode === 'HARD_ERASURE' ? 'DELETE_DERIVED' : 'REVOKE_ACCESS';
        reason = request.mode === 'HARD_ERASURE'
          ? 'Delete exclusively-owned derivative that depends on the erased source'
          : 'Soft deletion revokes access to derivative without claiming physical erasure';
        break;
      case 'CACHE':
        actionKind = 'INVALIDATE_CACHE';
        reason = 'Invalidate cached copy derived from erased source';
        break;
      case 'INDEX':
        actionKind = 'REMOVE_INDEX_ENTRY';
        reason = 'Remove discoverability/index projection that points to erased source';
        break;
      case 'EXTERNAL_EXPORT':
        if (!node.externalSystem) {
          blockers.push({ code: 'MISSING_EXTERNAL_ADAPTER', nodeId: node.id, detail: 'External export lacks an external system identifier/adapter target' });
          continue;
        }
        hasExternal = true;
        actionKind = 'REQUEST_EXTERNAL_ERASURE';
        reason = `Request erasure from external system ${node.externalSystem}; local deletion is not proof of external deletion`;
        break;
      default:
        continue;
    }

    if (MUTATING_KINDS.has(actionKind) && !node.mutable && node.kind !== 'BLOB') {
      blockers.push({ code: 'IMMUTABLE_MUTATION', nodeId: node.id, detail: `${node.kind} is immutable but planned action ${actionKind} requires mutation` });
      continue;
    }
    actions.push(makeAction(request, actionKind, node.id, reason));
  }

  return finalize(request, actions, blockers, hasHold, hasExternal);
}

function finalize(
  request: ErasureRequest,
  actions: ErasureAction[],
  blockers: PlanBlocker[],
  hasHold: boolean,
  hasExternal: boolean,
): ErasurePlan {
  const sortedActions = actions.slice().sort(compareActions);
  const sortedBlockers = blockers.slice().sort(compareBlockers);
  const status: PlanStatus = sortedBlockers.length > 0
    ? 'FREEZE'
    : hasExternal
      ? 'PENDING_EXTERNAL'
      : hasHold
        ? 'PARTIAL_HOLD'
        : 'READY';

  const body = {
    schemaVersion: 'NEXY_ERASURE_PLAN_V1' as const,
    request,
    status,
    executionAuthorized: status !== 'FREEZE',
    actions: sortedActions,
    blockers: sortedBlockers,
  };

  return { ...body, planHash: sha256Canonical(body) };
}
