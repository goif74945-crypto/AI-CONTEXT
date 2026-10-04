import { Q64, ONE, unit } from "../shared/q64.js";
export function freshnessDiscount(base, age, halfLife) {
    if (age.isNegative() || halfLife.compare(Q64.zero()) <= 0)
        throw new RangeError('invalid time');
    const factor = ONE.div(ONE.add(age.div(halfLife)));
    return unit(base).mul(factor);
}
