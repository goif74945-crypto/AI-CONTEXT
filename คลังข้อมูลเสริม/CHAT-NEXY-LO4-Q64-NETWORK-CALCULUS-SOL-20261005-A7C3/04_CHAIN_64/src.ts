import type { ArrivalContract, NamedServiceContract, ServiceContract } from '../shared/contracts.js';
import { validateArrival, validateNamedService } from '../shared/contracts.js';
import { addQ, requireNonNegative } from '../shared/q64.js';
import { fingerprint } from '../shared/canonical.js';
import { certifyFlow } from '../01_FLOWGUARD_64/src.js';

export type ChainVerdict='PASS'|'FAIL'|'FREEZE';
export interface ChainComposition {
  readonly system:'CHAIN-64'; readonly verdict:'PASS'|'FREEZE'; readonly reason:string;
  readonly stages:readonly NamedServiceContract[]; readonly service:ServiceContract; readonly fingerprint:string;
}
export interface ChainLimits {readonly maxBacklogQ?:bigint; readonly maxDelayQ?:bigint;}
export interface ChainCertificate {
  readonly system:'CHAIN-64'; readonly verdict:ChainVerdict; readonly reason:string;
  readonly composedService:ServiceContract; readonly backlogBoundQ:bigint; readonly delayBoundQ:bigint; readonly fingerprint:string;
}

function freezeComposition(reason:string,stages:readonly NamedServiceContract[]):ChainComposition{
  const base={system:'CHAIN-64' as const,verdict:'FREEZE' as const,reason,stages:[...stages],service:{rateQ:0n,latencyQ:0n}};
  return {...base,fingerprint:fingerprint(base)};
}

export function composeChain(stages:readonly NamedServiceContract[]):ChainComposition{
  try{
    if(stages.length===0) return freezeComposition('CHAIN_EMPTY',stages);
    const seen=new Set<string>();
    let minRate:bigint|null=null;
    let latency=0n;
    for(const stage of stages){
      validateNamedService(stage);
      if(seen.has(stage.id)) throw new Error('CHAIN_DUPLICATE_STAGE_ID');
      seen.add(stage.id);
      minRate=minRate===null||stage.rateQ<minRate?stage.rateQ:minRate;
      latency=addQ(latency,stage.latencyQ);
    }
    if(minRate===null) return freezeComposition('CHAIN_EMPTY',stages);
    const service={rateQ:minRate,latencyQ:latency};
    const base={system:'CHAIN-64' as const,verdict:'PASS' as const,reason:'RATE_LATENCY_CHAIN_COMPOSED',stages:[...stages],service};
    return {...base,fingerprint:fingerprint(base)};
  }catch(error){return freezeComposition(error instanceof Error?error.message:'UNKNOWN_ERROR',stages);}
}

export function certifyChain(arrival:ArrivalContract,stages:readonly NamedServiceContract[],limits:ChainLimits={}):ChainCertificate{
  try{
    validateArrival(arrival);
    if(limits.maxBacklogQ!==undefined) requireNonNegative(limits.maxBacklogQ,'MAX_BACKLOG_NEGATIVE');
    if(limits.maxDelayQ!==undefined) requireNonNegative(limits.maxDelayQ,'MAX_DELAY_NEGATIVE');
    const composed=composeChain(stages);
    if(composed.verdict==='FREEZE'){
      const base={system:'CHAIN-64' as const,verdict:'FREEZE' as const,reason:composed.reason,composedService:composed.service,backlogBoundQ:0n,delayBoundQ:0n};
      return {...base,fingerprint:fingerprint(base)};
    }
    const flow=certifyFlow(arrival,composed.service,limits);
    const verdict:ChainVerdict=flow.verdict==='ADMIT'?'PASS':flow.verdict==='REJECT'?'FAIL':'FREEZE';
    const base={system:'CHAIN-64' as const,verdict,reason:flow.reason,composedService:composed.service,backlogBoundQ:flow.backlogBoundQ,delayBoundQ:flow.delayBoundQ};
    return {...base,fingerprint:fingerprint(base)};
  }catch(error){
    const base={system:'CHAIN-64' as const,verdict:'FREEZE' as const,reason:error instanceof Error?error.message:'UNKNOWN_ERROR',composedService:{rateQ:0n,latencyQ:0n},backlogBoundQ:0n,delayBoundQ:0n};
    return {...base,fingerprint:fingerprint(base)};
  }
}
