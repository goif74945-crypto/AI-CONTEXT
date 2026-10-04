import { Q64 as Q } from "./shared/q64.js";
import { evaluateBackpressure } from "./04_backpressure-governor/CODE.js";
import { severity } from "./17_incident-severity-aggregator/CODE.js";
import { allocateDuty } from "./19_swarm-duty-allocator/CODE.js";
export function runProbe() {
    const out = [];
    for (let i = 0n; i < 1000n; i++) {
        const x = Q.fromRatio((i * 37n) % 1000n, 1000n);
        const y = Q.fromRatio((i * 91n + 7n) % 1000n, 1000n);
        const b = evaluateBackpressure({ queue: x, errors: y, latency: x.add(y).div(Q.fromInt(2n)).clamp(Q.zero(), Q.one()) });
        const s = severity({ impact: x, reach: y, exploitability: x, irreversibility: y, spread: x });
        const d = allocateDuty([{ id: "a", capacity: Q.one(), fitness: Q.one(), trust: Q.one(), load: x, reserve: Q.one() }, { id: "b", capacity: Q.one(), fitness: Q.parse("0.9"), trust: Q.parse("0.95"), load: y, reserve: Q.parse("0.9") }]);
        out.push(`${b.pressure.raw}:${b.admission.raw}:${s.score.raw}:${d[0].share.raw}:${d[1].share.raw}`);
    }
    return out.join("|");
}
