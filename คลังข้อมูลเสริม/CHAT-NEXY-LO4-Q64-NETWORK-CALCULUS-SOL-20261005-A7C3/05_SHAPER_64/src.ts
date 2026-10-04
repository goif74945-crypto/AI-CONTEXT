import type { ArrivalContract, ServiceContract } from '../shared/contracts.js';
import { validateArrival, validateService } from '../shared/contracts.js';
import { divQFloor, minQ, mulQCeil, mulQFloor, requireNonNegative, subQ } from '../shared/q64.js';
import { fingerprint } from '../shared/canonical.js';
import { certifyFlow } from '../01_FLOWGUARD_64/src.js';

export interface ShapeTargets {readonly maxBacklogQ?:bigint; readonly maxDelayQ?:bigint;}
export type ShaperVerdict='UNCHANGED'|'SHAPED'|'BLOCKED'|'IMPOSSIBLE'|'FREEZE';
export interface ShaperResult{
  readonly system:'SHAPER-64'; readonly verdict:ShaperVerdict; readonly reason:string;
  readonly offered:ArrivalContract; readonly shaped:ArrivalContract; readonly fingerprint:string;
}
function seal(verdict:ShaperVerdict,reason:string,offered:ArrivalContract,shaped:ArrivalContract):ShaperResult{
  const base={system:'SHAPER-64' as const,verdict,reason,offered,shaped};
  return {...base,fingerprint:fingerprint(base)};
}

export function synthesizeShaper(offered:ArrivalContract,service:ServiceContract,targets:ShapeTargets):ShaperResult{
  try{
    validateArrival(offered); validateService(service);
    if(targets.maxBacklogQ===undefined&&targets.maxDelayQ===undefined) throw new Error('SHAPER_TARGET_REQUIRED');
    if(targets.maxBacklogQ!==undefined) requireNonNegative(targets.maxBacklogQ,'MAX_BACKLOG_NEGATIVE');
    if(targets.maxDelayQ!==undefined) requireNonNegative(targets.maxDelayQ,'MAX_DELAY_NEGATIVE');
    if(targets.maxDelayQ!==undefined&&targets.maxDelayQ<service.latencyQ){
      return seal('IMPOSSIBLE','DEADLINE_BELOW_INTRINSIC_SERVICE_LATENCY',offered,{burstQ:0n,rateQ:0n});
    }

    let rateQ=minQ(offered.rateQ,service.rateQ);
    if(targets.maxBacklogQ!==undefined&&service.latencyQ>0n){
      const maxRateFromBacklog=divQFloor(targets.maxBacklogQ,service.latencyQ);
      rateQ=minQ(rateQ,maxRateFromBacklog);
    }

    let burstCap=offered.burstQ;
    if(targets.maxBacklogQ!==undefined){
      const baseline=mulQCeil(rateQ,service.latencyQ);
      if(baseline>targets.maxBacklogQ){
        return seal('BLOCKED','BACKLOG_TARGET_REQUIRES_ZERO_OR_LOWER_RATE',offered,{burstQ:0n,rateQ:0n});
      }
      burstCap=minQ(burstCap,subQ(targets.maxBacklogQ,baseline));
    }
    if(targets.maxDelayQ!==undefined){
      const slack=subQ(targets.maxDelayQ,service.latencyQ);
      const maxBurstFromDelay=mulQFloor(service.rateQ,slack);
      burstCap=minQ(burstCap,maxBurstFromDelay);
    }

    const shaped={burstQ:burstCap,rateQ};
    const check=certifyFlow(shaped,service,targets);
    if(check.verdict!=='ADMIT') return seal('IMPOSSIBLE','SYNTHESIZED_SHAPE_NOT_CERTIFIABLE',offered,shaped);
    if(shaped.burstQ===offered.burstQ&&shaped.rateQ===offered.rateQ) return seal('UNCHANGED','OFFERED_FLOW_ALREADY_WITHIN_TARGETS',offered,shaped);
    if(shaped.rateQ===0n&&offered.rateQ>0n) return seal('BLOCKED','TARGETS_ALLOW_NO_POSITIVE_SUSTAINED_RATE',offered,shaped);
    return seal('SHAPED','RATE_OR_BURST_REDUCED_TO_CERTIFIED_ENVELOPE',offered,shaped);
  }catch(error){return seal('FREEZE',error instanceof Error?error.message:'UNKNOWN_ERROR',offered,{burstQ:0n,rateQ:0n});}
}
