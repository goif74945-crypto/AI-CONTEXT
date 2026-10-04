import { requireUniqueIds } from "../shared/q64.js";
export function accrueCredit(a, quantum, cap) { if (quantum.isNegative())
    throw new RangeError('negative quantum'); return { ...a, credit: a.credit.add(quantum).min(cap) }; }
export function chooseRunnable(actors) { requireUniqueIds(actors, a => a.id); if (actors.some(a => a.credit.isNegative() || a.cost.isNegative()))
    throw new RangeError('negative queue field'); const ok = actors.filter(a => a.credit.compare(a.cost) >= 0); if (!ok.length)
    throw new Error('NO_RUNNABLE_ACTOR'); return [...ok].sort((a, b) => b.credit.compare(a.credit) || a.id.localeCompare(b.id))[0]; }
export function charge(a) { if (a.credit.compare(a.cost) < 0)
    throw new Error('INSUFFICIENT_CREDIT'); return { ...a, credit: a.credit.sub(a.cost) }; }
