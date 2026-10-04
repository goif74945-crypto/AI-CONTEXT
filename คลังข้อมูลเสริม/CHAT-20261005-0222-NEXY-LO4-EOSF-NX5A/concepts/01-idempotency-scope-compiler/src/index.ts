import { ContractError, assertNonEmpty, canonicalize, fingerprint, stableUnique, type JsonValue } from "../../../src/canonical.js";

export interface MutationIdentity {
  readonly route: string;
  readonly actorId: string;
  readonly projectId: string;
  readonly authorityEpoch: string;
  readonly payload: JsonValue;
  readonly userKey: string;
}

export interface IdempotencyPolicy {
  readonly scopeFields: readonly ("route" | "actorId" | "projectId" | "authorityEpoch" | "payload")[];
  readonly requirePayloadBinding: boolean;
  readonly requireAuthorityEpoch: boolean;
}

export interface CompiledIdempotency {
  readonly verdict: "PASS";
  readonly userKey: string;
  /** Non-security compact telemetry only. Never use this hash alone for authoritative equality. */
  readonly scopeFingerprint: string;
  /** Exact canonical structural identity. This is the authoritative equality key in this prototype. */
  readonly effectIdentity: string;
  readonly boundFields: readonly string[];
}

export function compileIdempotency(identity: MutationIdentity, policy: IdempotencyPolicy): CompiledIdempotency {
  assertNonEmpty(identity.route, "route");
  assertNonEmpty(identity.actorId, "actorId");
  assertNonEmpty(identity.projectId, "projectId");
  assertNonEmpty(identity.authorityEpoch, "authorityEpoch");
  assertNonEmpty(identity.userKey, "userKey");
  const fields = stableUnique(policy.scopeFields, "scopeFields") as readonly (keyof MutationIdentity)[];
  if (policy.requirePayloadBinding && !fields.includes("payload")) throw new ContractError("payload must be bound by idempotency scope");
  if (policy.requireAuthorityEpoch && !fields.includes("authorityEpoch")) throw new ContractError("authorityEpoch must be bound by idempotency scope");
  if (!fields.includes("route") || !fields.includes("projectId")) throw new ContractError("route and projectId are mandatory idempotency scope fields");
  const scope: Record<string, JsonValue> = {};
  for (const field of fields) scope[field] = identity[field] as JsonValue;
  return {
    verdict: "PASS",
    userKey: identity.userKey,
    scopeFingerprint: fingerprint(scope),
    effectIdentity: canonicalize({ userKey: identity.userKey, scope }),
    boundFields: fields,
  };
}

export type SeenExecutionState = "COMPLETED" | "IN_FLIGHT" | "FAILED_RETRYABLE";
export interface SeenMutation {
  readonly effectIdentity: string;
  /** Exact canonical structural seal, not a lossy hash. */
  readonly semanticSeal: string;
  readonly executionState: SeenExecutionState;
}

export type ReplayClassification =
  | { readonly verdict: "NEW"; readonly semanticSeal: string }
  | { readonly verdict: "REPLAY_COMPLETED"; readonly semanticSeal: string }
  | { readonly verdict: "REPLAY_IN_FLIGHT"; readonly semanticSeal: string }
  | { readonly verdict: "RETRY_SAME"; readonly semanticSeal: string }
  | { readonly verdict: "FREEZE_ALIAS"; readonly priorSeal: string; readonly semanticSeal: string };

export function classifyReplay(compiled: CompiledIdempotency, payload: JsonValue, seen: readonly SeenMutation[]): ReplayClassification {
  const semanticSeal = canonicalize({ payload, boundFields: compiled.boundFields as readonly JsonValue[] });
  const matches = seen.filter((entry) => entry.effectIdentity === compiled.effectIdentity);
  if (matches.length === 0) return { verdict: "NEW", semanticSeal };
  if (matches.length > 1) throw new ContractError("idempotency registry contains duplicate effect identity");
  const prior = matches[0]!;
  if (prior.semanticSeal !== semanticSeal) return { verdict: "FREEZE_ALIAS", priorSeal: prior.semanticSeal, semanticSeal };
  if (prior.executionState === "COMPLETED") return { verdict: "REPLAY_COMPLETED", semanticSeal };
  if (prior.executionState === "IN_FLIGHT") return { verdict: "REPLAY_IN_FLIGHT", semanticSeal };
  return { verdict: "RETRY_SAME", semanticSeal };
}
