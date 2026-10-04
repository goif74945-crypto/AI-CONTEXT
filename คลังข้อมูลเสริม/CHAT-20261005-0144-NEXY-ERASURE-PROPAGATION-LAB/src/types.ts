export type DataNodeKind =
  | 'CANONICAL_ARTIFACT'
  | 'BLOB'
  | 'DERIVED'
  | 'SHARED_DERIVED'
  | 'CACHE'
  | 'INDEX'
  | 'AUDIT_LOG'
  | 'EXTERNAL_EXPORT';

export type DataRelation =
  | 'CONTAINS_BLOB'
  | 'DERIVES'
  | 'CACHES'
  | 'INDEXES'
  | 'AUDITS'
  | 'EXPORTS';

export interface DataNode {
  id: string;
  kind: DataNodeKind;
  ownerId: string;
  mutable: boolean;
  retentionUntilTick?: bigint;
  legalHold?: boolean;
  externalSystem?: string;
}

export interface DataEdge {
  from: string;
  to: string;
  relation: DataRelation;
}

export interface DataGraph {
  nodes: DataNode[];
  edges: DataEdge[];
}

export type ErasureMode = 'SOFT_DELETE' | 'HARD_ERASURE';

export interface ErasureRequest {
  requestId: string;
  subjectOwnerId: string;
  targetNodeId: string;
  requestedAtTick: bigint;
  mode: ErasureMode;
}

export type PlanStatus =
  | 'READY'
  | 'PARTIAL_HOLD'
  | 'PENDING_EXTERNAL'
  | 'FREEZE';

export type BlockerCode =
  | 'TARGET_NOT_FOUND'
  | 'TARGET_OWNER_MISMATCH'
  | 'DUPLICATE_NODE_ID'
  | 'DANGLING_EDGE'
  | 'CROSS_OWNER_MUTATION'
  | 'PROPAGATION_CYCLE'
  | 'IMMUTABLE_MUTATION'
  | 'MISSING_EXTERNAL_ADAPTER'
  | 'SHARED_PROVENANCE_INCOMPLETE';

export interface PlanBlocker {
  code: BlockerCode;
  nodeId?: string;
  detail: string;
}

export type ErasureActionKind =
  | 'REVOKE_ACCESS'
  | 'DESTROY_BLOB'
  | 'DELETE_DERIVED'
  | 'INVALIDATE_CACHE'
  | 'REMOVE_INDEX_ENTRY'
  | 'REBUILD_SHARED_DERIVED'
  | 'APPEND_AUDIT_TOMBSTONE'
  | 'RETAIN_UNDER_HOLD'
  | 'REQUEST_EXTERNAL_ERASURE'
  | 'DELETE_IMMUTABLE_RECORD';

export type RequiredEvidence =
  | 'ACCESS_REVOCATION_RECEIPT'
  | 'BLOB_DESTRUCTION_RECEIPT'
  | 'DERIVED_DELETE_RECEIPT'
  | 'CACHE_INVALIDATION_RECEIPT'
  | 'INDEX_REMOVAL_RECEIPT'
  | 'REBUILD_RECEIPT'
  | 'AUDIT_TOMBSTONE_RECEIPT'
  | 'HOLD_EVIDENCE'
  | 'EXTERNAL_ERASURE_RECEIPT';

export interface ErasureAction {
  actionId: string;
  kind: ErasureActionKind;
  nodeId: string;
  reason: string;
  requiredEvidence: RequiredEvidence;
  removeSourceNodeIds?: string[];
  preserveSourceNodeIds?: string[];
}

export interface ErasurePlan {
  schemaVersion: 'NEXY_ERASURE_PLAN_V1';
  request: ErasureRequest;
  status: PlanStatus;
  executionAuthorized: boolean;
  actions: ErasureAction[];
  blockers: PlanBlocker[];
  planHash: string;
}

export interface ErasureReceipt {
  actionId: string;
  planHash: string;
  nodeId: string;
  outcome: 'APPLIED' | 'NOOP' | 'RETAINED';
  evidenceHash: string;
}

export interface ReceiptVerification {
  status: 'PASS' | 'FAIL' | 'NOT_VERIFIED';
  missingActionIds: string[];
  invalidReceiptActionIds: string[];
}
