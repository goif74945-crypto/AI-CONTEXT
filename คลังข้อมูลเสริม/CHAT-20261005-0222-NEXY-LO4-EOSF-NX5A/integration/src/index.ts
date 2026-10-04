import { compileIdempotency, classifyReplay, type IdempotencyPolicy, type MutationIdentity, type SeenMutation } from "../../concepts/01-idempotency-scope-compiler/src/index.js";
import { analyzeRetryAmplification, type RetryNode } from "../../concepts/02-retry-amplification-bounder/src/index.js";
import { authorizeCommit, type CommitAttempt, type LeaseState } from "../../concepts/03-lease-fencing-commit-gate/src/index.js";
import { prepareEffect, reconcilePrepared, type EffectRecord } from "../../concepts/04-outbox-effect-seal/src/index.js";
import { certifyCancellationClosure, type JobNode } from "../../concepts/05-cancellation-closure-certifier/src/index.js";

export interface EffectSafetyInput {
  readonly mutation: MutationIdentity;
  readonly idempotencyPolicy: IdempotencyPolicy;
  readonly seenMutations: readonly SeenMutation[];
  readonly retryRootId: string;
  readonly retryNodes: readonly RetryNode[];
  readonly retryBudget: bigint;
  readonly lease: LeaseState;
  readonly commitAttempt: CommitAttempt;
  readonly existingEffect: EffectRecord | null;
  readonly effectSeq: number;
  readonly cancellationRootId: string;
  readonly jobs: readonly JobNode[];
}

export type EffectSafetyResult =
  | { readonly verdict: "READY"; readonly effectIdentity: string; readonly effectRecord: EffectRecord; readonly resumeFrom: "PREPARED" | "COMMITTED"; readonly retryWorstCase: string; readonly cancellations: readonly string[] }
  | { readonly verdict: "SUPPRESS_REPLAY"; readonly effectIdentity: string; readonly evidence: "REGISTRY_COMPLETED" | "OUTBOX_EMITTED" }
  | { readonly verdict: "FREEZE"; readonly blockers: readonly string[] };

export function preflightExternalEffect(input: EffectSafetyInput): EffectSafetyResult {
  const blockers: string[] = [];
  const compiled = compileIdempotency(input.mutation, input.idempotencyPolicy);
  const replay = classifyReplay(compiled, input.mutation.payload, input.seenMutations);
  if (replay.verdict === "FREEZE_ALIAS") blockers.push("IDEMPOTENCY_ALIAS");

  const retry = analyzeRetryAmplification(input.retryRootId, input.retryNodes, input.retryBudget);
  if (retry.verdict === "FREEZE") blockers.push(...retry.reasonCodes.map((r) => `RETRY:${r}`));
  if (replay.verdict === "RETRY_SAME" && retry.verdict !== "PASS") blockers.push("IDEMPOTENCY_RETRY_NOT_PROVEN_SAFE");

  const fence = authorizeCommit(input.lease, input.commitAttempt);
  if (fence.verdict === "FREEZE") blockers.push(`FENCE:${fence.reason}`);

  const prepared = prepareEffect(compiled.effectIdentity, input.mutation.payload, input.effectSeq);
  const reconciled = reconcilePrepared(input.existingEffect, prepared);
  if (reconciled.verdict === "FREEZE_CONFLICT") blockers.push("OUTBOX:PAYLOAD_MISMATCH");
  if (reconciled.verdict === "FREEZE_CANCELLED") blockers.push("OUTBOX:EFFECT_ID_CANCELLED");

  const outboxState = "record" in reconciled ? reconciled.record.state : null;
  if (replay.verdict === "REPLAY_IN_FLIGHT") {
    if (outboxState === "EMITTED") blockers.push("REGISTRY_OUTBOX_STATE_CONFLICT");
    else blockers.push("IDEMPOTENCY_IN_FLIGHT");
  }
  if (replay.verdict === "REPLAY_COMPLETED" && input.existingEffect !== null && outboxState !== "EMITTED") {
    blockers.push("REGISTRY_OUTBOX_STATE_CONFLICT");
  }
  if (replay.verdict === "RETRY_SAME" && outboxState === "EMITTED") {
    blockers.push("REGISTRY_OUTBOX_STATE_CONFLICT");
  }

  const cancellation = certifyCancellationClosure(input.cancellationRootId, input.jobs);
  if (cancellation.verdict === "FREEZE") blockers.push(...cancellation.blockers.map((b) => `CANCEL:${b}`));
  if (blockers.length) return { verdict: "FREEZE", blockers: [...new Set(blockers)].sort() };

  if (replay.verdict === "REPLAY_COMPLETED") return { verdict: "SUPPRESS_REPLAY", effectIdentity: compiled.effectIdentity, evidence: "REGISTRY_COMPLETED" };
  if (reconciled.verdict === "REPLAY_EMITTED") return { verdict: "SUPPRESS_REPLAY", effectIdentity: compiled.effectIdentity, evidence: "OUTBOX_EMITTED" };

  const effectRecord = "record" in reconciled ? reconciled.record : prepared;
  const resumeFrom = effectRecord.state === "COMMITTED" ? "COMMITTED" : "PREPARED";
  return { verdict: "READY", effectIdentity: compiled.effectIdentity, effectRecord, resumeFrom, retryWorstCase: retry.worstCaseEffectAttempts, cancellations: cancellation.cancelNow };
}
