import { Q64 } from "../shared/q64.js";
export class PrivacyBudgetGovernor {
    spent = Q64.zero();
    budget;
    constructor(budget) { if (budget.isNegative())
        throw new RangeError('negative budget'); this.budget = budget; }
    tryConsume(cost) { if (cost.isNegative())
        throw new RangeError('negative cost'); const next = this.spent.add(cost); if (next.compare(this.budget) > 0)
        return false; this.spent = next; return true; }
    remaining() { return this.budget.sub(this.spent); }
    used() { return this.spent; }
}
