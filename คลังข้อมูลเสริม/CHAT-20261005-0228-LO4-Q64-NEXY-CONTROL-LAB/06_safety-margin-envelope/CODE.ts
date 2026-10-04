import { Q64, complement, unit } from "../shared/q64.ts";
export type Hazard={likelihood:Q64;impact:Q64;containment:Q64;reversibility:Q64};
export function safetyMargin(h:Hazard):Q64{ const risk=unit(h.likelihood).mul(unit(h.impact)); const mitig=Q64.weightedMean([unit(h.containment),unit(h.reversibility)],[Q64.fromInt(3n),Q64.fromInt(2n)]); return complement(risk).mul(mitig); }
export function requireSafety(h:Hazard,threshold:Q64):Q64{ const m=safetyMargin(h); if(m.compare(threshold)<0)throw new Error('SAFETY_ENVELOPE_REJECTED'); return m; }
