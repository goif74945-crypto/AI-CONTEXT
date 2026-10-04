import { ContractError, assertNonEmpty, assertSafeInt, canonicalize, type JsonValue } from "../../../src/canonical.js";

export type EffectState = "PREPARED" | "COMMITTED" | "EMITTED" | "CANCELLED";

export interface EffectRecord {
  readonly effectId: string;
  readonly payload: JsonValue;
  /** Exact canonical structural seal, not a lossy hash. */
  readonly payloadSeal: string;
  readonly state: EffectState;
  readonly preparedSeq: number;
  readonly committedSeq?: number;
  readonly emittedSeq?: number;
}

export type ReconcilePrepared =
  | { readonly verdict: "NEW"; readonly record: EffectRecord }
  | { readonly verdict: "REPLAY_PREPARED" | "REPLAY_COMMITTED" | "REPLAY_EMITTED"; readonly record: EffectRecord }
  | { readonly verdict: "FREEZE_CONFLICT"; readonly reason: "PAYLOAD_MISMATCH" }
  | { readonly verdict: "FREEZE_CANCELLED"; readonly reason: "EFFECT_ID_CANCELLED" };

export function prepareEffect(effectId: string, payload: JsonValue, seq: number): EffectRecord {
  assertNonEmpty(effectId, "effectId"); assertSafeInt(seq, "seq", 0);
  return { effectId, payload, payloadSeal: canonicalize(payload), state: "PREPARED", preparedSeq: seq };
}

export function reconcilePrepared(existing: EffectRecord | null, candidate: EffectRecord): ReconcilePrepared {
  if (!existing) return { verdict: "NEW", record: candidate };
  if (existing.effectId !== candidate.effectId) throw new ContractError("reconcilePrepared requires the same effectId");
  if (existing.payloadSeal !== candidate.payloadSeal) return { verdict: "FREEZE_CONFLICT", reason: "PAYLOAD_MISMATCH" };
  if (existing.state === "CANCELLED") return { verdict: "FREEZE_CANCELLED", reason: "EFFECT_ID_CANCELLED" };
  if (existing.state === "PREPARED") return { verdict: "REPLAY_PREPARED", record: existing };
  if (existing.state === "COMMITTED") return { verdict: "REPLAY_COMMITTED", record: existing };
  return { verdict: "REPLAY_EMITTED", record: existing };
}

export function commitEffect(record: EffectRecord, seq: number): EffectRecord {
  assertSafeInt(seq, "seq", 0);
  if (record.state === "COMMITTED" || record.state === "EMITTED") return record;
  if (record.state !== "PREPARED") throw new ContractError(`cannot commit effect from ${record.state}`);
  if (seq < record.preparedSeq) throw new ContractError("commit seq precedes prepare seq");
  return { ...record, state: "COMMITTED", committedSeq: seq };
}

export function emitEffect(record: EffectRecord, seq: number): { readonly verdict: "EMIT" | "ALREADY_EMITTED"; readonly record: EffectRecord } {
  assertSafeInt(seq, "seq", 0);
  if (record.state === "EMITTED") return { verdict: "ALREADY_EMITTED", record };
  if (record.state !== "COMMITTED" || record.committedSeq === undefined) throw new ContractError("effect must be COMMITTED before emission");
  if (seq < record.committedSeq) throw new ContractError("emit seq precedes commit seq");
  return { verdict: "EMIT", record: { ...record, state: "EMITTED", emittedSeq: seq } };
}

export function cancelPrepared(record: EffectRecord): EffectRecord {
  if (record.state === "CANCELLED") return record;
  if (record.state !== "PREPARED") throw new ContractError("only PREPARED effects can be cancelled without compensation");
  return { ...record, state: "CANCELLED" };
}

export function auditEffectRecord(record: EffectRecord): readonly string[] {
  const issues: string[] = [];
  if (record.payloadSeal !== canonicalize(record.payload)) issues.push("PAYLOAD_SEAL_MISMATCH");
  if ((record.state === "COMMITTED" || record.state === "EMITTED") && record.committedSeq === undefined) issues.push("MISSING_COMMIT_SEQ");
  if (record.state === "EMITTED" && record.emittedSeq === undefined) issues.push("MISSING_EMIT_SEQ");
  if (record.committedSeq !== undefined && record.committedSeq < record.preparedSeq) issues.push("COMMIT_BEFORE_PREPARE");
  if (record.emittedSeq !== undefined && (record.committedSeq === undefined || record.emittedSeq < record.committedSeq)) issues.push("EMIT_BEFORE_COMMIT");
  return issues.sort();
}
