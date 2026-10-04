import { Q64, ONE, unit } from "../shared/q64.ts";
export function freshnessDiscount(base:Q64,age:Q64,halfLife:Q64):Q64{
 if(age.isNegative()||halfLife.compare(Q64.zero())<=0)throw new RangeError('invalid time'); const factor=ONE.div(ONE.add(age.div(halfLife))); return unit(base).mul(factor);
}
