import { ContractError, assertNonEmpty, stableUnique } from "../../../src/canonical.js";

export type JobState = "QUEUED" | "RUNNING" | "SUCCEEDED" | "FAILED" | "CANCELLED" | "EXPIRED";
export interface JobNode {
  readonly id: string;
  readonly parentId: string | null;
  readonly state: JobState;
  /** True only when a real external effect is already materialized, regardless of job terminal state. */
  readonly hasExternalEffect: boolean;
  readonly compensationId: string | null;
}

export interface CancellationPlan {
  readonly verdict: "PASS" | "FREEZE";
  readonly rootId: string;
  readonly cancelNow: readonly string[];
  readonly jobsWithMaterializedEffects: readonly string[];
  readonly requiredCompensations: readonly string[];
  readonly blockers: readonly string[];
}

export function certifyCancellationClosure(rootId: string, jobs: readonly JobNode[]): CancellationPlan {
  assertNonEmpty(rootId, "rootId");
  const map = new Map<string, JobNode>();
  for (const job of jobs) {
    assertNonEmpty(job.id, "job.id");
    if (map.has(job.id)) throw new ContractError(`duplicate job ${job.id}`);
    if (job.parentId !== null) assertNonEmpty(job.parentId, `${job.id}.parentId`);
    if (job.compensationId !== null) assertNonEmpty(job.compensationId, `${job.id}.compensationId`);
    map.set(job.id, job);
  }
  if (!map.has(rootId)) throw new ContractError("cancellation root does not exist");
  const children = new Map<string, string[]>();
  for (const job of jobs) {
    if (job.parentId !== null) {
      if (!map.has(job.parentId)) throw new ContractError(`unknown parent ${job.parentId}`);
      const list = children.get(job.parentId) ?? [];
      list.push(job.id);
      children.set(job.parentId, list);
    }
  }
  const seen = new Set<string>();
  const stack = new Set<string>();
  function walk(id: string, closure: string[]): void {
    if (stack.has(id)) throw new ContractError(`job graph cycle at ${id}`);
    if (seen.has(id)) return;
    stack.add(id); seen.add(id); closure.push(id);
    for (const child of (children.get(id) ?? []).sort()) walk(child, closure);
    stack.delete(id);
  }
  const closure: string[] = [];
  walk(rootId, closure);
  const cancelNow: string[] = [];
  const jobsWithEffects: string[] = [];
  const compensations: string[] = [];
  const blockers: string[] = [];
  for (const id of closure.sort()) {
    const job = map.get(id)!;
    if (job.state === "QUEUED" || job.state === "RUNNING") cancelNow.push(id);
    if (job.hasExternalEffect) {
      jobsWithEffects.push(id);
      if (job.compensationId === null) blockers.push(`UNCOMPENSATED_EFFECT:${id}`);
      else compensations.push(job.compensationId);
    }
  }
  const uniqueCompensations = stableUnique(compensations, "compensationId");
  return {
    verdict: blockers.length ? "FREEZE" : "PASS",
    rootId,
    cancelNow: cancelNow.sort(),
    jobsWithMaterializedEffects: jobsWithEffects.sort(),
    requiredCompensations: uniqueCompensations,
    blockers: blockers.sort(),
  };
}
