import { ContractError, assertNonEmpty, assertSafeInt, checkedAdd, checkedMul, stableUnique } from "../../../src/canonical.js";

export interface RetryNode {
  readonly id: string;
  readonly maxAttempts: number;
  readonly fanOut: number;
  readonly localEffectsPerAttempt: number;
  readonly retryExplicitlySafe: boolean;
  readonly children: readonly string[];
}

export interface RetryAnalysis {
  readonly verdict: "PASS" | "FREEZE";
  readonly rootId: string;
  readonly worstCaseEffectAttempts: string;
  readonly budget: string;
  readonly unsafeRetryNodes: readonly string[];
  readonly reasonCodes: readonly string[];
}

export function analyzeRetryAmplification(
  rootId: string,
  nodes: readonly RetryNode[],
  effectAttemptBudget: bigint,
  analysisCap: bigint = 10_000_000_000n,
): RetryAnalysis {
  assertNonEmpty(rootId, "rootId");
  if (effectAttemptBudget < 0n || analysisCap < 1n || effectAttemptBudget > analysisCap) {
    throw new ContractError("invalid retry analysis budget/cap");
  }
  const map = new Map<string, RetryNode>();
  for (const node of nodes) {
    assertNonEmpty(node.id, "node.id");
    if (map.has(node.id)) throw new ContractError(`duplicate retry node ${node.id}`);
    assertSafeInt(node.maxAttempts, `${node.id}.maxAttempts`, 1);
    assertSafeInt(node.fanOut, `${node.id}.fanOut`, 1);
    assertSafeInt(node.localEffectsPerAttempt, `${node.id}.localEffectsPerAttempt`, 0);
    stableUnique(node.children, `${node.id}.children`);
    map.set(node.id, node);
  }
  if (!map.has(rootId)) throw new ContractError("root retry node does not exist");
  for (const node of map.values()) {
    for (const child of node.children) if (!map.has(child)) throw new ContractError(`unknown retry child ${child}`);
  }
  const visiting = new Set<string>();
  const memo = new Map<string, bigint>();
  const unsafe = new Set<string>();
  function visit(id: string): bigint {
    const cached = memo.get(id); if (cached !== undefined) return cached;
    if (visiting.has(id)) throw new ContractError(`retry graph cycle at ${id}`);
    visiting.add(id);
    const node = map.get(id)!;
    if (node.maxAttempts > 1 && !node.retryExplicitlySafe) unsafe.add(id);
    let perAttempt = BigInt(node.localEffectsPerAttempt);
    for (const childId of node.children) {
      const child = visit(childId);
      const fanoutChild = checkedMul(BigInt(node.fanOut), child, analysisCap, `${id} fanout`);
      perAttempt = checkedAdd(perAttempt, fanoutChild, analysisCap, `${id} per-attempt effects`);
    }
    const total = checkedMul(BigInt(node.maxAttempts), perAttempt, analysisCap, `${id} attempts`);
    visiting.delete(id); memo.set(id, total); return total;
  }
  const total = visit(rootId);
  const reasons: string[] = [];
  if (unsafe.size) reasons.push("RETRY_NOT_EXPLICITLY_SAFE");
  if (total > effectAttemptBudget) reasons.push("EFFECT_ATTEMPT_BUDGET_EXCEEDED");
  return {
    verdict: reasons.length ? "FREEZE" : "PASS",
    rootId,
    worstCaseEffectAttempts: total.toString(),
    budget: effectAttemptBudget.toString(),
    unsafeRetryNodes: [...unsafe].sort(),
    reasonCodes: reasons,
  };
}
