import { Q64, Q64Error } from "./q64";
import type { AdvisoryAuthority } from "./core";
import { ForgeError, canonicalStrings, countBig, nonEmpty } from "./core";
export interface RequirementInput {
  readonly id: string;
  readonly statement: string;
  readonly invariants: readonly string[];
  readonly evidenceRequired: readonly string[];
}

export interface HypothesisContract {
  readonly id: string;
  readonly requirementId: string;
  readonly claim: string;
  readonly falsifiers: readonly string[];
  readonly requiredEvidence: readonly string[];
  readonly authority: AdvisoryAuthority;
}

export function requirementToHypothesis(requirement: RequirementInput): HypothesisContract {
  const id = nonEmpty(requirement.id, "requirement id");
  const statement = nonEmpty(requirement.statement, "requirement statement");
  const invariants = canonicalStrings(requirement.invariants, "invariant");
  const evidence = canonicalStrings(requirement.evidenceRequired, "required evidence");
  return Object.freeze({
    id: `HYP-${id}`,
    requirementId: id,
    claim: statement,
    falsifiers: Object.freeze(invariants.map((x) => `violate:${x}`)),
    requiredEvidence: Object.freeze(evidence),
    authority: "ADVISORY_ONLY" as const
  });
}

export interface FalsifiabilityInput {
  readonly id: string;
  readonly claim: string;
  readonly falsifiers: readonly string[];
  readonly observables: readonly string[];
}

export interface FalsifiabilityResult {
  readonly hypothesisId: string;
  readonly status: "PASS";
  readonly falsifierCount: bigint;
  readonly observableCount: bigint;
}

export function falsifiabilityGate(input: FalsifiabilityInput): FalsifiabilityResult {
  const id = nonEmpty(input.id, "hypothesis id");
  nonEmpty(input.claim, "hypothesis claim");
  const falsifiers = canonicalStrings(input.falsifiers, "falsifier");
  const observables = canonicalStrings(input.observables, "observable");
  return Object.freeze({
    hypothesisId: id,
    status: "PASS" as const,
    falsifierCount: countBig(falsifiers),
    observableCount: countBig(observables)
  });
}

export interface FalsifierCandidate {
  readonly id: string;
  readonly cost: Q64;
  readonly falsifies: readonly string[];
}

export interface MinimalFalsifierResult {
  readonly selected: readonly FalsifierCandidate[];
  readonly covered: readonly string[];
  readonly uncovered: readonly string[];
}

export function minimalFalsifierPlan(
  candidates: readonly FalsifierCandidate[],
  hypotheses: readonly string[]
): MinimalFalsifierResult {
  if (candidates.length === 0) throw new ForgeError("at least one falsifier candidate is required");
  const required = canonicalStrings(hypotheses, "hypothesis");
  if (required.length > 128) throw new ForgeError("exact minimal planner supports at most 128 hypotheses");
  if (candidates.length > 128) throw new ForgeError("exact minimal planner supports at most 128 candidates");

  const hypothesisIndex = new Map<string, bigint>();
  let bit = 1n;
  for (const hypothesis of required) {
    hypothesisIndex.set(hypothesis, bit);
    bit <<= 1n;
  }
  const fullMask = bit - 1n;

  const normalized = candidates.map((candidate) => {
    const id = nonEmpty(candidate.id, "candidate id");
    if (candidate.cost.raw < 0n) throw new ForgeError("candidate cost must be non-negative");
    const falsifies = canonicalStrings(candidate.falsifies, "falsified hypothesis");
    let mask = 0n;
    for (const hypothesis of falsifies) mask |= hypothesisIndex.get(hypothesis) ?? 0n;
    return { id, cost: candidate.cost, falsifies, mask };
  }).filter((candidate) => candidate.mask !== 0n).sort((a, b) => a.id.localeCompare(b.id));
  if (normalized.length === 0) throw new ForgeError("no candidate can falsify any required hypothesis");

  interface State { readonly cost: Q64; readonly ids: readonly string[]; }
  const states = new Map<bigint, State>();
  states.set(0n, {cost: Q64.ZERO, ids: Object.freeze([])});
  const better = (candidate: State, current: State | undefined): boolean => {
    if (current === undefined) return true;
    const costCmp = candidate.cost.compare(current.cost);
    if (costCmp !== 0) return costCmp < 0;
    if (candidate.ids.length !== current.ids.length) return candidate.ids.length < current.ids.length;
    return candidate.ids.join("\u0000").localeCompare(current.ids.join("\u0000")) < 0;
  };

  for (const candidate of normalized) {
    const snapshot = [...states.entries()];
    for (const [mask, state] of snapshot) {
      const nextMask = mask | candidate.mask;
      if (nextMask === mask) continue;
      let nextCost: Q64;
      try { nextCost = state.cost.add(candidate.cost); }
      catch (error) {
        if (error instanceof Q64Error) throw new ForgeError("falsifier plan cost overflow");
        throw error;
      }
      const proposal: State = {cost: nextCost, ids: Object.freeze([...state.ids, candidate.id])};
      if (better(proposal, states.get(nextMask))) states.set(nextMask, proposal);
    }
  }

  const optimum = states.get(fullMask);
  if (optimum === undefined) throw new ForgeError("required hypotheses are not fully falsifiable by candidate set");
  const byId = new Map(normalized.map((candidate) => [candidate.id, candidate]));
  const selected = optimum.ids.map((id) => {
    const candidate = byId.get(id);
    if (candidate === undefined) throw new ForgeError("internal candidate lookup failure");
    return Object.freeze({id:candidate.id,cost:candidate.cost,falsifies:Object.freeze(candidate.falsifies)});
  });
  return Object.freeze({
    selected: Object.freeze(selected),
    covered: Object.freeze(required),
    uncovered: Object.freeze([])
  });
}

