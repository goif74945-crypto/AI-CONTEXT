import { Q64 } from "../shared/q64.ts";
export function limitPreferenceUpdate(previous:Q64,proposed:Q64,maxStep:Q64):Q64{
 if(maxStep.isNegative()) throw new RangeError('negative maxStep'); const delta=proposed.sub(previous); if(delta.abs().compare(maxStep)<=0)return proposed; return previous.add(delta.isNegative()?maxStep.neg():maxStep);
}
export function driftMagnitude(a:readonly Q64[],b:readonly Q64[]):Q64{ if(a.length!==b.length)throw new RangeError('shape mismatch'); return Q64.sum(a.map((v,i)=>v.sub(b[i]).abs())); }
