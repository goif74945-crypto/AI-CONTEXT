import { Q64, ZERO, requireUniqueIds } from "../shared/q64.ts";
export type Demand={id:string;weight:Q64;floor:Q64};
export type Allocation={id:string;amount:Q64};
export function allocateBudget(total:Q64,demands:readonly Demand[]):Allocation[]{
  if(total.isNegative())throw new RangeError('negative total');
  if(!demands.length)return[];
  requireUniqueIds(demands,d=>d.id);
  const ds=[...demands].sort((a,b)=>a.id.localeCompare(b.id));
  if(ds.some(d=>d.weight.isNegative()||d.floor.isNegative()))throw new RangeError('negative demand field');
  const floorSum=Q64.sum(ds.map(d=>d.floor));
  if(floorSum.compare(total)>0)throw new Error('INSUFFICIENT_BUDGET_FOR_FLOORS');
  const remainder=total.sub(floorSum);const weightSum=Q64.sum(ds.map(d=>d.weight));
  if(weightSum.isZero()&&!remainder.isZero())throw new Error('ZERO_WEIGHT_WITH_REMAINDER');
  let distributed=ZERO;const out:Allocation[]=[];
  for(let i=0;i<ds.length;i++){const d=ds[i];const extra=i===ds.length-1?remainder.sub(distributed):(weightSum.isZero()?ZERO:remainder.mul(d.weight).div(weightSum));distributed=distributed.add(extra);out.push({id:d.id,amount:d.floor.add(extra)});}
  return out;
}
