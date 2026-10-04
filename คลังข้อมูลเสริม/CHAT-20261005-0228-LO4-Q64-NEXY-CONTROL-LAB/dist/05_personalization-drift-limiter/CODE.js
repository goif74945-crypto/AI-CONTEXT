import { Q64 } from "../shared/q64.js";
export function limitPreferenceUpdate(previous, proposed, maxStep) {
    if (maxStep.isNegative())
        throw new RangeError('negative maxStep');
    const delta = proposed.sub(previous);
    if (delta.abs().compare(maxStep) <= 0)
        return proposed;
    return previous.add(delta.isNegative() ? maxStep.neg() : maxStep);
}
export function driftMagnitude(a, b) { if (a.length !== b.length)
    throw new RangeError('shape mismatch'); return Q64.sum(a.map((v, i) => v.sub(b[i]).abs())); }
