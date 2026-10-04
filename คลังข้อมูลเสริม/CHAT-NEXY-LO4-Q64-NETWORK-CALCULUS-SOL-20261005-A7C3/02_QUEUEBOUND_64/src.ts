import type { ArrivalContract, ServiceContract } from '../shared/contracts.js';
import { backlogUpperQ, isStable } from '../shared/calculus.js';
import { validateArrival, validateService } from '../shared/contracts.js';
import { fingerprint } from '../shared/canonical.js';
import { requireNonNegative } from '../shared/q64.js';

export type BacklogVerdict = 'PASS' | 'FAIL' | 'FREEZE';
export interface BacklogCertificate {
  readonly system:'QUEUEBOUND-64'; readonly verdict:BacklogVerdict; readonly reason:string;
  readonly backlogBoundQ:bigint; readonly maxBacklogQ:bigint|null; readonly fingerprint:string;
}

function seal(verdict:BacklogVerdict, reason:string, bound:bigint, max:bigint|null):BacklogCertificate {
  const base={system:'QUEUEBOUND-64' as const,verdict,reason,backlogBoundQ:bound,maxBacklogQ:max};
  return {...base,fingerprint:fingerprint(base)};
}

export function certifyBacklog(arrival:ArrivalContract, service:ServiceContract, maxBacklogQ?:bigint):BacklogCertificate {
  try {
    validateArrival(arrival); validateService(service);
    if (maxBacklogQ !== undefined) requireNonNegative(maxBacklogQ,'MAX_BACKLOG_NEGATIVE');
    if (!isStable(arrival,service)) return seal('FREEZE','UNBOUNDED_BACKLOG_UNSTABLE_FLOW',0n,maxBacklogQ??null);
    const bound=backlogUpperQ(arrival,service);
    if (maxBacklogQ !== undefined && bound>maxBacklogQ) return seal('FAIL','BUFFER_BOUND_EXCEEDED',bound,maxBacklogQ);
    return seal('PASS','BACKLOG_BOUND_CERTIFIED',bound,maxBacklogQ??null);
  } catch(error) { return seal('FREEZE',error instanceof Error?error.message:'UNKNOWN_ERROR',0n,maxBacklogQ??null); }
}
