import type { Q64 } from "./q64.js";

export type CandidateStatus =
  | "WIP"
  | "DEFER"
  | "INSUFFICIENT_EVIDENCE"
  | "ACTIVE"
  | "ARCHIVED"
  | "REJECTED"
  | "SUPERSEDED";

export interface Candidate {
  readonly candidateId: string;
  readonly ownerChatId: string;
  readonly lineageRootId: string;
  readonly declaredParentIds: readonly string[];
  readonly declaredMerge: boolean;
  readonly semanticAtoms: readonly string[];
  readonly evidenceIds: readonly string[];
  readonly scopeDimensions: readonly string[];
  readonly createdTick: bigint;
  readonly status: CandidateStatus;
}

export interface Revision {
  readonly candidateId: string;
  readonly revisionId: string;
  readonly parentRevisionId: string | null;
  readonly tick: bigint;
  readonly semanticAtoms: readonly string[];
  readonly evidenceIds: readonly string[];
  readonly scopeDimensions: readonly string[];
  readonly status: CandidateStatus;
}

export type VoteRound = "KEEP" | "CUT";

export interface CourtVote {
  readonly voteId: string;
  readonly chatId: string;
  readonly candidateId: string;
  readonly candidateOwnerChatId: string;
  readonly revisionId: string;
  readonly round: VoteRound;
  readonly tick: bigint;
  readonly provenanceCluster: string | null;
  readonly argumentEvidenceIds: readonly string[];
  readonly counterargumentEvidenceIds: readonly string[];
  readonly reason: string;
  readonly counterargument: string;
  readonly finalJustification: string;
}

export interface RankEntry {
  readonly candidateId: string;
  readonly rank: bigint;
}

export interface StatusObservation {
  readonly status: CandidateStatus;
  readonly evidenceDigest: string;
  readonly evidenceCount: bigint;
  readonly tick: bigint;
}

export interface EvidenceItem {
  readonly evidenceId: string;
  readonly stance: "SUPPORT" | "OPPOSE" | "NEUTRAL";
}

export type MechanismId =
  | "SPLIT64" | "MERGE64" | "LAUNDER64" | "FRONT64" | "CLONE64"
  | "IIA64" | "CLONEINV64" | "ORDER64" | "EVIDORDER64" | "TIE64"
  | "OSC64" | "DEFERCHURN64" | "SCOPE64" | "APPEAL64" | "COALITION64"
  | "RECIPROCITY64" | "BURST64" | "COUNTERARG64" | "DISSENT64" | "MANIPGATE64";

export type FindingState = "CLEAR" | "FLAGGED" | "UNKNOWN";

export interface Finding {
  readonly mechanism: MechanismId;
  readonly state: FindingState;
  readonly hardBlock: boolean;
  readonly severityQ64: Q64;
  readonly reason: string;
  readonly relatedIds: readonly string[];
}
