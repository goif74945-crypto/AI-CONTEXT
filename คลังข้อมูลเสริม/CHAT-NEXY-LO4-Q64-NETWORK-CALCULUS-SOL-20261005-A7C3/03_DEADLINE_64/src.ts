import type { ArrivalContract, ServiceContract } from '../shared/contracts.js';
import { delayUpperQ, isStable } from '../shared/calculus.js';
import { validateArrival, validateService } from '../shared/contracts.js';
import { fingerprint } from '../shared/canonical.js';
import { requireNonNegative } from '../shared/q64.js';

export type DeadlineVerdict='PASS'|'FAIL'|'FREEZE';
export interface DeadlineCertificate {
  readonly system:'DEADLINE-64'; readonly verdict:DeadlineVerdict; readonly reason:string;
  readonly delayBoundQ:bigint; readonly maxDelayQ:bigint|null; readonly fingerprint:string;
}
function seal(verdict:DeadlineVerdict,reason:string,bound:bigint,max:bigint|null):DeadlineCertificate {
  const base={system:'DEADLINE-64' as const,verdict,reason,delayBoundQ:bound,maxDelayQ:max};
  return {...base,fingerprint:fingerprint(base)};
}
export function certifyDeadline(arrival:ArrivalContract,service:ServiceContract,maxDelayQ?:bigint):DeadlineCertificate {
  try {
    validateArrival(arrival); validateService(service);
    if(maxDelayQ!==undefined) requireNonNegative(maxDelayQ,'MAX_DELAY_NEGATIVE');
    if(!isStable(arrival,service)) return seal('FREEZE','UNBOUNDED_DELAY_UNSTABLE_FLOW',0n,maxDelayQ??null);
    const bound=delayUpperQ(arrival,service);
    if(maxDelayQ!==undefined&&bound>maxDelayQ) return seal('FAIL','DEADLINE_BOUND_EXCEEDED',bound,maxDelayQ);
    return seal('PASS','DELAY_BOUND_CERTIFIED',bound,maxDelayQ??null);
  } catch(error){return seal('FREEZE',error instanceof Error?error.message:'UNKNOWN_ERROR',0n,maxDelayQ??null);}
}
