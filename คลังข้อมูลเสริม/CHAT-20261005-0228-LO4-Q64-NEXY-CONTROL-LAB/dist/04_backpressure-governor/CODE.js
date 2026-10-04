import { Q64, complement, unit } from "../shared/q64.js";
export function evaluateBackpressure(p) {
    const pressure = Q64.weightedMean([unit(p.queue), unit(p.errors), unit(p.latency)], [Q64.fromInt(4n), Q64.fromInt(5n), Q64.fromInt(3n)]);
    const level = pressure.compare(Q64.parse('0.90')) >= 0 ? 'FREEZE' : pressure.compare(Q64.parse('0.70')) >= 0 ? 'DEGRADED' : pressure.compare(Q64.parse('0.45')) >= 0 ? 'GUARDED' : 'NORMAL';
    return { pressure, admission: level === 'FREEZE' ? Q64.zero() : complement(pressure), level };
}
