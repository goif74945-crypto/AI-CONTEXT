import type { ErasurePlan, ErasureReceipt, ReceiptVerification } from './types.ts';

const HEX64 = /^[0-9a-f]{64}$/;

export function verifyErasureReceipts(plan: ErasurePlan, receipts: ErasureReceipt[]): ReceiptVerification {
  if (plan.status === 'FREEZE') {
    return {
      status: 'FAIL',
      missingActionIds: plan.actions.map(a => a.actionId).sort(),
      invalidReceiptActionIds: receipts.map(r => r.actionId).sort(),
    };
  }

  const actionById = new Map(plan.actions.map(action => [action.actionId, action]));
  const receiptByActionId = new Map<string, ErasureReceipt[]>();
  for (const receipt of receipts) {
    const bucket = receiptByActionId.get(receipt.actionId) ?? [];
    bucket.push(receipt);
    receiptByActionId.set(receipt.actionId, bucket);
  }

  const missingActionIds: string[] = [];
  const invalid = new Set<string>();

  for (const action of plan.actions) {
    const matches = receiptByActionId.get(action.actionId) ?? [];
    if (matches.length === 0) {
      missingActionIds.push(action.actionId);
      continue;
    }
    if (matches.length !== 1) {
      invalid.add(action.actionId);
      continue;
    }
    const receipt = matches[0]!;
    const outcomeValid = action.kind === 'RETAIN_UNDER_HOLD'
      ? receipt.outcome === 'RETAINED' || receipt.outcome === 'APPLIED'
      : receipt.outcome === 'APPLIED' || receipt.outcome === 'NOOP';

    if (
      receipt.planHash !== plan.planHash
      || receipt.nodeId !== action.nodeId
      || !HEX64.test(receipt.evidenceHash)
      || !outcomeValid
    ) {
      invalid.add(action.actionId);
    }
  }

  for (const receipt of receipts) {
    if (!actionById.has(receipt.actionId)) invalid.add(receipt.actionId);
  }

  const invalidReceiptActionIds = [...invalid].sort();
  missingActionIds.sort();
  return {
    status: invalidReceiptActionIds.length > 0
      ? 'FAIL'
      : missingActionIds.length > 0
        ? 'NOT_VERIFIED'
        : 'PASS',
    missingActionIds,
    invalidReceiptActionIds,
  };
}
