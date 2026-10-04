import { Q64, ZERO, requireUniqueIds, unit } from "../shared/q64.ts";
export type Vote={agentId:string;verdict:-1|0|1;trust:Q64;reliability:Q64};
export type Consensus={signedSupport:Q64;absoluteSupport:Q64;margin:Q64;decision:-1|0|1};
export function resolveConsensus(votes:readonly Vote[],minMargin:Q64):Consensus{
 requireUniqueIds(votes,v=>v.agentId);
 let signed=ZERO,abs=ZERO; for(const v of votes){const w=unit(v.trust).mul(unit(v.reliability));abs=abs.add(w);signed=signed.add(w.mul(Q64.fromInt(v.verdict===-1?-1n:v.verdict===1?1n:0n)));}
 if(abs.isZero())return{signedSupport:ZERO,absoluteSupport:ZERO,margin:ZERO,decision:0}; const margin=signed.abs().div(abs); const decision=margin.compare(minMargin)<0?0:signed.isNegative()?-1:1; return{signedSupport:signed,absoluteSupport:abs,margin,decision};
}
