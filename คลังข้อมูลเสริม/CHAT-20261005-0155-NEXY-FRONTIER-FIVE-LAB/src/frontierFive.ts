import { createHash } from "node:crypto";

// ===== core.ts =====

export type JsonPrimitive = null | boolean | number | string;
export type JsonValue = JsonPrimitive | JsonValue[] | { readonly [key: string]: JsonValue };

export type EvidenceClass = "E0" | "E1" | "E2" | "E3" | "E4" | "E5" | "E6" | "E7";

export const EVIDENCE_CLASSES: readonly EvidenceClass[] = [
  "E0",
  "E1",
  "E2",
  "E3",
  "E4",
  "E5",
  "E6",
  "E7",
] as const;

export function compareCodeUnits(a: string, b: string): number {
  return a < b ? -1 : a > b ? 1 : 0;
}

function assertJsonNumber(value: number): void {
  if (!Number.isFinite(value)) {
    throw new TypeError("Non-finite numbers are not canonical JSON values");
  }
}

function canonicalizeInternal(value: JsonValue): string {
  if (value === null) return "null";
  if (typeof value === "boolean") return value ? "true" : "false";
  if (typeof value === "number") {
    assertJsonNumber(value);
    return JSON.stringify(Object.is(value, -0) ? 0 : value);
  }
  if (typeof value === "string") return JSON.stringify(value);
  if (Array.isArray(value)) {
    return `[${value.map((item) => canonicalizeInternal(item)).join(",")}]`;
  }

  const entries = Object.entries(value).sort(([a], [b]) => compareCodeUnits(a, b));
  return `{${entries
    .map(([key, item]) => `${JSON.stringify(key)}:${canonicalizeInternal(item)}`)
    .join(",")}}`;
}

export function canonicalJson(value: JsonValue): string {
  return canonicalizeInternal(value);
}

export function sha256Hex(value: string | Uint8Array): string {
  return createHash("sha256").update(value).digest("hex");
}

export function stableDigest(value: JsonValue): string {
  return sha256Hex(canonicalJson(value));
}

export function assertUniqueStrings(values: readonly string[], label: string): void {
  const seen = new Set<string>();
  for (const value of values) {
    if (seen.has(value)) {
      throw new Error(`${label} contains duplicate value: ${value}`);
    }
    seen.add(value);
  }
}

export function compareLexicographically(a: readonly string[], b: readonly string[]): number {
  const length = Math.min(a.length, b.length);
  for (let i = 0; i < length; i += 1) {
    const av = a[i];
    const bv = b[i];
    if (av === undefined || bv === undefined) break;
    const cmp = compareCodeUnits(av, bv);
    if (cmp !== 0) return cmp;
  }
  return a.length - b.length;
}

// ===== provenanceCache.ts =====

export interface CacheContext {
  readonly namespace: string;
  readonly operation: string;
  readonly input: JsonValue;
  readonly authorityEpoch: string;
  readonly policyDigest: string;
  readonly dependencyVersions: Readonly<Record<string, string>>;
}

export interface CacheRecord<T extends JsonValue> {
  readonly key: string;
  readonly context: CacheContext;
  readonly value: T;
  readonly evidenceClass: EvidenceClass;
  readonly createdAtMs: number;
  readonly expiresAtMs: number;
}

export type CacheMissReason =
  | "ABSENT"
  | "STALE_TIME"
  | "DEPENDENCY_DRIFT"
  | "AUTHORITY_DRIFT"
  | "POLICY_DRIFT"
  | "EVIDENCE_CLASS_MISMATCH";

export type CacheLookup<T extends JsonValue> =
  | { readonly status: "HIT"; readonly record: CacheRecord<T> }
  | { readonly status: "MISS"; readonly reason: CacheMissReason };

function normalizedDependencies(versions: Readonly<Record<string, string>>): { readonly [key: string]: JsonValue } {
  const normalized: Record<string, JsonValue> = {};
  for (const [key, value] of Object.entries(versions).sort(([a], [b]) => compareCodeUnits(a, b))) {
    normalized[key] = value;
  }
  return normalized;
}

export function cacheRequestKey(context: CacheContext): string {
  return stableDigest({
    input: context.input,
    namespace: context.namespace,
    operation: context.operation,
  });
}

export function cacheKey(context: CacheContext): string {
  return stableDigest({
    authorityEpoch: context.authorityEpoch,
    dependencyVersions: normalizedDependencies(context.dependencyVersions),
    input: context.input,
    namespace: context.namespace,
    operation: context.operation,
    policyDigest: context.policyDigest,
  });
}

function sameDependencies(
  left: Readonly<Record<string, string>>,
  right: Readonly<Record<string, string>>,
): boolean {
  return canonicalJson(normalizedDependencies(left)) === canonicalJson(normalizedDependencies(right));
}

export class ProvenanceAwareCache<T extends JsonValue> {
  readonly #recordsByRequest = new Map<string, CacheRecord<T>>();

  put(record: CacheRecord<T>): void {
    if (!Number.isFinite(record.createdAtMs) || !Number.isFinite(record.expiresAtMs)) {
      throw new TypeError("Cache timestamps must be finite numbers");
    }
    if (record.expiresAtMs < record.createdAtMs) {
      throw new RangeError("expiresAtMs must be >= createdAtMs");
    }
    const expectedKey = cacheKey(record.context);
    if (record.key !== expectedKey) {
      throw new Error("Cache record key does not match its provenance context");
    }
    this.#recordsByRequest.set(cacheRequestKey(record.context), record);
  }

  lookup(
    context: CacheContext,
    requiredEvidenceClass: EvidenceClass,
    nowMs: number,
  ): CacheLookup<T> {
    if (!Number.isFinite(nowMs)) throw new TypeError("nowMs must be finite");
    const record = this.#recordsByRequest.get(cacheRequestKey(context));
    if (record === undefined) return { status: "MISS", reason: "ABSENT" };
    if (record.context.authorityEpoch !== context.authorityEpoch) {
      return { status: "MISS", reason: "AUTHORITY_DRIFT" };
    }
    if (record.context.policyDigest !== context.policyDigest) {
      return { status: "MISS", reason: "POLICY_DRIFT" };
    }
    if (!sameDependencies(record.context.dependencyVersions, context.dependencyVersions)) {
      return { status: "MISS", reason: "DEPENDENCY_DRIFT" };
    }
    if (record.evidenceClass !== requiredEvidenceClass) {
      return { status: "MISS", reason: "EVIDENCE_CLASS_MISMATCH" };
    }
    if (nowMs > record.expiresAtMs) {
      return { status: "MISS", reason: "STALE_TIME" };
    }
    return { status: "HIT", record };
  }

  size(): number {
    return this.#recordsByRequest.size;
  }
}

// ===== determinismFingerprint.ts =====

export interface DeterministicRunSnapshot {
  readonly input: JsonValue;
  readonly state: JsonValue;
  readonly policy: JsonValue;
  readonly output: JsonValue;
  readonly effects: readonly JsonValue[];
}

export interface RunFingerprint {
  readonly input: string;
  readonly state: string;
  readonly policy: string;
  readonly output: string;
  readonly effects: string;
  readonly aggregate: string;
}

export type FingerprintDimension = keyof Omit<RunFingerprint, "aggregate">;

export interface FingerprintComparison {
  readonly deterministic: boolean;
  readonly changedDimensions: readonly FingerprintDimension[];
}

export function fingerprintRun(snapshot: DeterministicRunSnapshot): RunFingerprint {
  const parts = {
    input: stableDigest(snapshot.input),
    state: stableDigest(snapshot.state),
    policy: stableDigest(snapshot.policy),
    output: stableDigest(snapshot.output),
    effects: stableDigest([...snapshot.effects]),
  } as const;

  return {
    ...parts,
    aggregate: stableDigest(parts),
  };
}

export function compareFingerprints(
  baseline: RunFingerprint,
  candidate: RunFingerprint,
): FingerprintComparison {
  const dimensions: readonly FingerprintDimension[] = ["input", "state", "policy", "output", "effects"];
  const changedDimensions = dimensions.filter((dimension) => baseline[dimension] !== candidate[dimension]);
  return {
    deterministic: changedDimensions.length === 0,
    changedDimensions,
  };
}

// ===== failureMinimizer.ts =====
export interface MinimizeOptions {
  readonly maxEvaluations?: number;
}

export interface MinimizeResult<T> {
  readonly minimal: readonly T[];
  readonly evaluations: number;
  readonly oneMinimal: boolean;
}

interface RangeChunk<T> {
  readonly start: number;
  readonly end: number;
  readonly items: readonly T[];
}

function splitIntoChunks<T>(items: readonly T[], chunks: number): readonly RangeChunk<T>[] {
  const result: RangeChunk<T>[] = [];
  let cursor = 0;
  for (let i = 0; i < chunks; i += 1) {
    const remainingItems = items.length - cursor;
    const remainingChunks = chunks - i;
    const size = Math.ceil(remainingItems / remainingChunks);
    const start = cursor;
    const end = cursor + size;
    result.push({ start, end, items: items.slice(start, end) });
    cursor = end;
  }
  return result.filter((chunk) => chunk.items.length > 0);
}

function complementOfRange<T>(source: readonly T[], chunk: RangeChunk<T>): readonly T[] {
  return [...source.slice(0, chunk.start), ...source.slice(chunk.end)];
}

export function minimizeFailure<T>(
  items: readonly T[],
  fails: (candidate: readonly T[]) => boolean,
  options: MinimizeOptions = {},
): MinimizeResult<T> {
  const maxEvaluations = options.maxEvaluations ?? 10_000;
  if (!Number.isSafeInteger(maxEvaluations) || maxEvaluations < 1) {
    throw new RangeError("maxEvaluations must be a positive safe integer");
  }

  let evaluations = 0;
  const evaluate = (candidate: readonly T[]): boolean => {
    evaluations += 1;
    if (evaluations > maxEvaluations) {
      throw new Error(`Failure minimization exceeded maxEvaluations=${maxEvaluations}`);
    }
    return fails(candidate);
  };

  if (!evaluate(items)) {
    throw new Error("Initial candidate does not reproduce the failure");
  }

  let current = [...items];
  let granularity = 2;

  while (current.length >= 2) {
    const chunks = splitIntoChunks(current, Math.min(granularity, current.length));
    let reduced = false;

    for (const chunk of chunks) {
      if (evaluate(chunk.items)) {
        current = [...chunk.items];
        granularity = 2;
        reduced = true;
        break;
      }
    }
    if (reduced) continue;

    for (const chunk of chunks) {
      const complement = complementOfRange(current, chunk);
      if (evaluate(complement)) {
        current = [...complement];
        granularity = Math.max(2, granularity - 1);
        reduced = true;
        break;
      }
    }
    if (reduced) continue;

    if (granularity >= current.length) break;
    granularity = Math.min(current.length, granularity * 2);
  }

  let oneMinimal = true;
  for (let i = 0; i < current.length; i += 1) {
    const candidate = [...current.slice(0, i), ...current.slice(i + 1)];
    if (evaluate(candidate)) {
      oneMinimal = false;
      break;
    }
  }

  return { minimal: current, evaluations, oneMinimal };
}

// ===== invariantMiner.ts =====

export type InvariantKind = "REQUIRED_PATH" | "STABLE_TYPE" | "CONSTANT" | "NUMERIC_RANGE";

export interface InvariantProposal {
  readonly status: "PROPOSAL";
  readonly kind: InvariantKind;
  readonly path: string;
  readonly sampleCount: number;
  readonly support: number;
  readonly details: JsonValue;
}

export interface InvariantMiningOptions {
  readonly minSamples?: number;
}

function valueType(value: JsonValue): string {
  if (value === null) return "null";
  if (Array.isArray(value)) return "array";
  return typeof value;
}

function flatten(value: JsonValue, prefix = "$"): Map<string, JsonValue> {
  const result = new Map<string, JsonValue>();
  result.set(prefix, value);
  if (value !== null && typeof value === "object" && !Array.isArray(value)) {
    for (const [key, child] of Object.entries(value).sort(([a], [b]) => compareCodeUnits(a, b))) {
      const escaped = key.replaceAll("~", "~0").replaceAll("/", "~1");
      const childPath = prefix === "$" ? `$/` + escaped : `${prefix}/${escaped}`;
      for (const [path, nested] of flatten(child, childPath)) result.set(path, nested);
    }
  }
  return result;
}

export function mineInvariants(
  traces: readonly JsonValue[],
  options: InvariantMiningOptions = {},
): readonly InvariantProposal[] {
  const minSamples = options.minSamples ?? 3;
  if (!Number.isSafeInteger(minSamples) || minSamples < 2) {
    throw new RangeError("minSamples must be an integer >= 2");
  }
  if (traces.length < minSamples) return [];

  const flattened = traces.map((trace) => flatten(trace));
  const allPaths = new Set<string>();
  for (const item of flattened) for (const path of item.keys()) allPaths.add(path);

  const proposals: InvariantProposal[] = [];
  for (const path of [...allPaths].sort()) {
    const values = flattened.map((trace) => trace.get(path)).filter((value): value is JsonValue => value !== undefined);
    const support = values.length / traces.length;
    if (support === 1) {
      proposals.push({
        status: "PROPOSAL",
        kind: "REQUIRED_PATH",
        path,
        sampleCount: traces.length,
        support,
        details: { observed: traces.length },
      });
    }

    if (values.length < minSamples) continue;
    const types = [...new Set(values.map(valueType))].sort();
    if (types.length === 1) {
      proposals.push({
        status: "PROPOSAL",
        kind: "STABLE_TYPE",
        path,
        sampleCount: traces.length,
        support,
        details: { type: types[0] ?? "unknown" },
      });
    }

    const canonicalValues = [...new Set(values.map((value) => canonicalJson(value)))];
    if (canonicalValues.length === 1) {
      proposals.push({
        status: "PROPOSAL",
        kind: "CONSTANT",
        path,
        sampleCount: traces.length,
        support,
        details: { value: values[0] ?? null },
      });
    }

    if (values.every((value) => typeof value === "number" && Number.isFinite(value))) {
      const numeric = values as number[];
      proposals.push({
        status: "PROPOSAL",
        kind: "NUMERIC_RANGE",
        path,
        sampleCount: traces.length,
        support,
        details: { min: Math.min(...numeric), max: Math.max(...numeric) },
      });
    }
  }

  return proposals;
}

// ===== evidenceSelector.ts =====

export interface EvidenceObligation {
  readonly id: string;
  readonly requiredClass: EvidenceClass;
}

export interface EvidenceCandidate {
  readonly id: string;
  readonly cost: number;
  readonly proves: readonly {
    readonly obligationId: string;
    readonly evidenceClass: EvidenceClass;
  }[];
  readonly mandatory?: boolean;
}

export interface EvidenceSelection {
  readonly selectedIds: readonly string[];
  readonly totalCost: number;
  readonly coveredObligations: readonly string[];
}

function candidateCovers(
  candidate: EvidenceCandidate,
  obligation: EvidenceObligation,
): boolean {
  return candidate.proves.some(
    (proof) => proof.obligationId === obligation.id && proof.evidenceClass === obligation.requiredClass,
  );
}

export function selectMinimalEvidence(
  obligations: readonly EvidenceObligation[],
  candidates: readonly EvidenceCandidate[],
): EvidenceSelection {
  assertUniqueStrings(obligations.map((item) => item.id), "obligations");
  assertUniqueStrings(candidates.map((item) => item.id), "candidates");
  if (candidates.length > 64) {
    throw new RangeError("Exact selector is intentionally bounded to 64 candidates");
  }
  for (const candidate of candidates) {
    if (!Number.isFinite(candidate.cost) || candidate.cost < 0) {
      throw new RangeError(`Candidate ${candidate.id} has invalid cost`);
    }
  }

  const obligationById = new Map(obligations.map((item) => [item.id, item] as const));
  for (const candidate of candidates) {
    for (const proof of candidate.proves) {
      if (!obligationById.has(proof.obligationId)) {
        throw new Error(`Candidate ${candidate.id} references unknown obligation ${proof.obligationId}`);
      }
    }
  }

  const impossible = obligations
    .filter((obligation) => !candidates.some((candidate) => candidateCovers(candidate, obligation)))
    .map((obligation) => `${obligation.id}:${obligation.requiredClass}`);
  if (impossible.length > 0) {
    throw new Error(`No evidence plan covers all obligations; impossible=${impossible.join(",")}`);
  }

  const mandatory = candidates.filter((candidate) => candidate.mandatory === true);
  const selectedMandatoryIds = new Set(mandatory.map((candidate) => candidate.id));
  const optional = candidates
    .filter((candidate) => candidate.mandatory !== true)
    .filter((candidate) => obligations.some((obligation) => candidateCovers(candidate, obligation)))
    .sort((a, b) => compareCodeUnits(a.id, b.id));

  const mandatoryCovered = new Set(
    obligations
      .filter((obligation) => mandatory.some((candidate) => candidateCovers(candidate, obligation)))
      .map((obligation) => obligation.id),
  );
  const mandatoryCost = mandatory.reduce((sum, candidate) => sum + candidate.cost, 0);

  let bestIds: readonly string[] | undefined;
  let bestCost = Number.POSITIVE_INFINITY;

  const search = (selected: readonly EvidenceCandidate[], covered: ReadonlySet<string>, cost: number): void => {
    if (cost > bestCost) return;
    if (covered.size === obligations.length) {
      const ids = [...mandatory.map((candidate) => candidate.id), ...selected.map((candidate) => candidate.id)].sort(compareCodeUnits);
      if (cost < bestCost || (cost === bestCost && bestIds !== undefined && compareLexicographically(ids, bestIds) < 0) || bestIds === undefined) {
        bestCost = cost;
        bestIds = ids;
      }
      return;
    }

    const uncovered = obligations.find((obligation) => !covered.has(obligation.id));
    if (uncovered === undefined) return;

    const choices = optional.filter(
      (candidate) => !selected.includes(candidate) && candidateCovers(candidate, uncovered),
    );
    for (const candidate of choices) {
      const nextCovered = new Set(covered);
      for (const obligation of obligations) {
        if (candidateCovers(candidate, obligation)) nextCovered.add(obligation.id);
      }
      search([...selected, candidate], nextCovered, cost + candidate.cost);
    }
  };

  search([], mandatoryCovered, mandatoryCost);
  if (bestIds === undefined) {
    throw new Error("No evidence plan covers all obligations");
  }

  for (const id of selectedMandatoryIds) {
    if (!bestIds.includes(id)) throw new Error(`Internal invariant failed: missing mandatory candidate ${id}`);
  }

  return {
    selectedIds: bestIds,
    totalCost: bestCost,
    coveredObligations: obligations.map((item) => item.id).sort(compareCodeUnits),
  };
}

// ===== integration.ts =====

export interface FrontierFiveInput {
  readonly cacheContext: CacheContext;
  readonly run: DeterministicRunSnapshot;
  readonly traces: readonly JsonValue[];
  readonly obligations: readonly EvidenceObligation[];
  readonly candidates: readonly EvidenceCandidate[];
  readonly failingSteps: readonly string[];
  readonly reproducesFailure: (steps: readonly string[]) => boolean;
}

export interface FrontierFiveReport {
  readonly advisoryOnly: true;
  readonly cacheKey: string;
  readonly fingerprint: ReturnType<typeof fingerprintRun>;
  readonly invariantProposals: ReturnType<typeof mineInvariants>;
  readonly evidencePlan: ReturnType<typeof selectMinimalEvidence>;
  readonly minimizedFailure: ReturnType<typeof minimizeFailure<string>>;
}

export function analyzeFrontierFive(input: FrontierFiveInput): FrontierFiveReport {
  return {
    advisoryOnly: true,
    cacheKey: cacheKey(input.cacheContext),
    fingerprint: fingerprintRun(input.run),
    invariantProposals: mineInvariants(input.traces),
    evidencePlan: selectMinimalEvidence(input.obligations, input.candidates),
    minimizedFailure: minimizeFailure(input.failingSteps, input.reproducesFailure),
  };
}
