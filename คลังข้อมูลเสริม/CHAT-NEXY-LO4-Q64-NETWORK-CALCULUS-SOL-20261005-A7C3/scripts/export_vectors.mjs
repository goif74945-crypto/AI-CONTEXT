import { qInt } from '../dist/shared/q64.js';
import { certifyFlow } from '../dist/01_FLOWGUARD_64/src.js';
import { composeChain } from '../dist/04_CHAIN_64/src.js';
const rows=[];
for(let b=0n;b<10n;b++) for(let r=0n;r<5n;r++) for(let k=1n;k<=4n;k++){
  const R=r+k; const T=(b+r+k)%5n;
  const arrival={burstQ:qInt(b),rateQ:qInt(r)};
  const service={rateQ:qInt(R),latencyQ:qInt(T)};
  const flow=certifyFlow(arrival,service);
  const chain=composeChain([
    {id:'a',rateQ:qInt(R+2n),latencyQ:qInt(1n)},
    {id:'b',rateQ:qInt(R),latencyQ:qInt(T)},
    {id:'c',rateQ:qInt(R+1n),latencyQ:qInt(2n)}
  ]);
  rows.push({b:b.toString(),r:r.toString(),R:R.toString(),T:T.toString(),
    backlog:flow.backlogBoundQ.toString(),delay:flow.delayBoundQ.toString(),
    chainRate:chain.service.rateQ.toString(),chainLatency:chain.service.latencyQ.toString()});
}
process.stdout.write(JSON.stringify(rows));
