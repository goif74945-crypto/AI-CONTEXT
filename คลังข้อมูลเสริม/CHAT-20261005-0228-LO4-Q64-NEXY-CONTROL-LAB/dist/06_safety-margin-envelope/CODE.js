import { Q64, complement, unit } from "../shared/q64.js";
export function safetyMargin(h) { const risk = unit(h.likelihood).mul(unit(h.impact)); const mitig = Q64.weightedMean([unit(h.containment), unit(h.reversibility)], [Q64.fromInt(3n), Q64.fromInt(2n)]); return complement(risk).mul(mitig); }
export function requireSafety(h, threshold) { const m = safetyMargin(h); if (m.compare(threshold) < 0)
    throw new Error('SAFETY_ENVELOPE_REJECTED'); return m; }
