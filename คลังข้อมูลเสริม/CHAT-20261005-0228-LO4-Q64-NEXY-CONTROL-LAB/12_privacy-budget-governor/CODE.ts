import { Q64 } from "../shared/q64.ts";
export class PrivacyBudgetGovernor{
  private spent:Q64=Q64.zero();
  readonly budget:Q64;
  constructor(budget:Q64){if(budget.isNegative())throw new RangeError('negative budget');this.budget=budget;}
  tryConsume(cost:Q64):boolean{if(cost.isNegative())throw new RangeError('negative cost');const next=this.spent.add(cost);if(next.compare(this.budget)>0)return false;this.spent=next;return true;}
  remaining():Q64{return this.budget.sub(this.spent);}
  used():Q64{return this.spent;}
}
