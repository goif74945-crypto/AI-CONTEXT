import { Q64, requireUniqueIds } from "../shared/q64.ts";
export type QueueActor={id:string;credit:Q64;cost:Q64};
export function accrueCredit(a:QueueActor,quantum:Q64,cap:Q64):QueueActor{if(quantum.isNegative())throw new RangeError('negative quantum');return{...a,credit:a.credit.add(quantum).min(cap)}}
export function chooseRunnable(actors:readonly QueueActor[]):QueueActor{requireUniqueIds(actors,a=>a.id);if(actors.some(a=>a.credit.isNegative()||a.cost.isNegative()))throw new RangeError('negative queue field');const ok=actors.filter(a=>a.credit.compare(a.cost)>=0);if(!ok.length)throw new Error('NO_RUNNABLE_ACTOR');return[...ok].sort((a,b)=>b.credit.compare(a.credit)||a.id.localeCompare(b.id))[0];}
export function charge(a:QueueActor):QueueActor{if(a.credit.compare(a.cost)<0)throw new Error('INSUFFICIENT_CREDIT');return{...a,credit:a.credit.sub(a.cost)}}
