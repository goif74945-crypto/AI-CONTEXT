import type { ArrivalContract, ServiceContract } from '../shared/contracts.js';
import { validateArrival, validateService } from '../shared/contracts.js';
import { allBounds, isStable } from '../shared/calculus.js';
import { fingerprint } from '../shared/canonical.js';
import { requireNonNegative } from '../shared/q64.js';

export type FlowVerdict = 'ADMIT' | 'REJECT' | 'FREEZE';
export interface FlowLimits { readonly maxBacklogQ?: bigint; readonly maxDelayQ?: bigint; }
export interface FlowCertificate {
  readonly system: 'FLOWGUARD-64';
  readonly verdict: FlowVerdict;
  readonly reason: string;
  readonly backlogBoundQ: bigint;
  readonly delayBoundQ: bigint;
  readonly fingerprint: string;
}

function freeze(reason: string): FlowCertificate {
  const base = { system:'FLOWGUARD-64' as const, verdict:'FREEZE' as const, reason, backlogBoundQ:0n, delayBoundQ:0n };
  return { ...base, fingerprint:fingerprint(base) };
}

export function certifyFlow(arrival: ArrivalContract, service: ServiceContract, limits: FlowLimits = {}): FlowCertificate {
  try {
    validateArrival(arrival); validateService(service);
    if (limits.maxBacklogQ !== undefined) requireNonNegative(limits.maxBacklogQ, 'MAX_BACKLOG_NEGATIVE');
    if (limits.maxDelayQ !== undefined) requireNonNegative(limits.maxDelayQ, 'MAX_DELAY_NEGATIVE');
    if (!isStable(arrival, service)) {
      const base = { system:'FLOWGUARD-64' as const, verdict:'REJECT' as const, reason:'ARRIVAL_RATE_EXCEEDS_SERVICE_RATE', backlogBoundQ:0n, delayBoundQ:0n };
      return { ...base, fingerprint:fingerprint(base) };
    }
    const bounds = allBounds(arrival, service);
    const backlogFail = limits.maxBacklogQ !== undefined && bounds.backlogBoundQ > limits.maxBacklogQ;
    const delayFail = limits.maxDelayQ !== undefined && bounds.delayBoundQ > limits.maxDelayQ;
    const verdict: FlowVerdict = backlogFail || delayFail ? 'REJECT' : 'ADMIT';
    const reason = backlogFail && delayFail ? 'BACKLOG_AND_DELAY_LIMIT_EXCEEDED'
      : backlogFail ? 'BACKLOG_LIMIT_EXCEEDED'
      : delayFail ? 'DELAY_LIMIT_EXCEEDED'
      : 'FINITE_BOUNDS_CERTIFIED';
    const base = { system:'FLOWGUARD-64' as const, verdict, reason, ...bounds };
    return { ...base, fingerprint:fingerprint(base) };
  } catch (error) {
    return freeze(error instanceof Error ? error.message : 'UNKNOWN_ERROR');
  }
}
