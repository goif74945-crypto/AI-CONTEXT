import { createHash } from "node:crypto";

export type JsonPrimitive = string | number | boolean | null;
export type JsonValue = JsonPrimitive | readonly JsonValue[] | { readonly [key: string]: JsonValue };
export type DirectiveSourceClass =
  | "USER_DIRECTIVE" | "PROJECT_LAW" | "BUILD_SPEC" | "REPOSITORY_STATE"
  | "RUNTIME_EVIDENCE" | "PROJECT_CONTEXT" | "DESIGN_VISION" | "MODEL_INFERENCE" | "OTHER";
export interface DirectiveCondition { readonly key: string; readonly equals: JsonValue; }
export interface Directive {
  readonly id: string;
  readonly authorityRank: number;
  readonly localPriority?: number;
  readonly sourceClass: DirectiveSourceClass;
  readonly scope: string;
  readonly subject: string;
  readonly value: JsonValue;
  readonly conditions?: readonly DirectiveCondition[];
  readonly provenance?: string;
}
export interface CompileRequest {
  readonly target: string;
  readonly subject: string;
  readonly context?: Readonly<Record<string, JsonValue>>;
  readonly directives: readonly Directive[];
  readonly requireDecision?: boolean;
}
export type ResolutionStatus = "RESOLVED" | "FREEZE_CONFLICT" | "FREEZE_NO_DECISION" | "NO_DECISION";
export type DirectiveDisposition = "ACTIVE" | "REDUNDANT" | "SHADOWED" | "CONFLICT" | "INAPPLICABLE";
export interface DirectiveTrace {
  readonly id: string;
  readonly disposition: DirectiveDisposition;
  readonly reason: string;
  readonly precedence?: readonly [authorityRank: number, negativeSpecificity: number, negativePriority: number];
}
export interface Resolution {
  readonly status: ResolutionStatus;
  readonly target: string;
  readonly subject: string;
  readonly value?: JsonValue;
  readonly activeDirectiveIds: readonly string[];
  readonly conflictDirectiveIds: readonly string[];
  readonly trace: readonly DirectiveTrace[];
  readonly inputFingerprint: string;
  readonly fingerprint: string;
}
export interface BatchResolution { readonly resolutions: readonly Resolution[]; readonly fingerprint: string; readonly hasFreeze: boolean; }

interface ParsedScope { readonly segments: readonly string[]; readonly exactCount: number; readonly wildcardCount: number; readonly hasGlobTail: boolean; }
interface EvaluatedDirective { readonly directive: Directive; readonly precedence: readonly [number, number, number]; }

const SOURCE_CLASSES: ReadonlySet<DirectiveSourceClass> = new Set([
  "USER_DIRECTIVE", "PROJECT_LAW", "BUILD_SPEC", "REPOSITORY_STATE", "RUNTIME_EVIDENCE",
  "PROJECT_CONTEXT", "DESIGN_VISION", "MODEL_INFERENCE", "OTHER",
]);
const TOKEN = /^[A-Za-z0-9._:@-]+$/;
const SEGMENT = /^[A-Za-z0-9._:@-]+$/;

function stableTextCompare(a: string, b: string): number { return a < b ? -1 : a > b ? 1 : 0; }
function normalizeNumber(value: number): number {
  if (!Number.isFinite(value)) throw new TypeError("JSON-compatible values cannot contain NaN or Infinity");
  return Object.is(value, -0) ? 0 : value;
}
export function canonicalize(value: JsonValue): JsonValue {
  if (value === null || typeof value === "string" || typeof value === "boolean") return value;
  if (typeof value === "number") return normalizeNumber(value);
  if (Array.isArray(value)) return value.map(canonicalize);
  const prototype = Object.getPrototypeOf(value);
  if (prototype !== Object.prototype && prototype !== null) throw new TypeError("Only plain JSON objects are supported");
  const objectValue = value as { readonly [key: string]: JsonValue };
  const result: Record<string, JsonValue> = {};
  for (const key of Object.keys(objectValue).sort()) {
    const item = objectValue[key];
    if (item === undefined) throw new TypeError("Undefined is not JSON-compatible");
    result[key] = canonicalize(item);
  }
  return result;
}
export function canonicalJson(value: JsonValue): string { return JSON.stringify(canonicalize(value)); }
export function fingerprint(value: JsonValue): string { return createHash("sha256").update(canonicalJson(value), "utf8").digest("hex"); }
function jsonEqual(a: JsonValue, b: JsonValue): boolean { return canonicalJson(a) === canonicalJson(b); }
function validateToken(value: string, label: string): void {
  if (!TOKEN.test(value)) throw new TypeError(`${label} must use canonical ASCII token characters`);
}
function splitPath(path: string, label: string): string[] {
  if (path.length === 0 || path.startsWith("/") || path.endsWith("/") || path.includes("//"))
    throw new TypeError(`${label} must be a non-empty normalized slash-delimited path`);
  return path.split("/");
}
function parseScope(scope: string): ParsedScope {
  const segments = splitPath(scope, "scope");
  let exactCount = 0, wildcardCount = 0, hasGlobTail = false;
  segments.forEach((segment, index) => {
    if (segment === "*") { wildcardCount += 1; return; }
    if (segment === "**") {
      if (index !== segments.length - 1) throw new TypeError("`**` is allowed only as the final scope segment");
      wildcardCount += 1; hasGlobTail = true; return;
    }
    if (!SEGMENT.test(segment)) throw new TypeError(`Invalid scope segment: ${segment}`);
    exactCount += 1;
  });
  return { segments, exactCount, wildcardCount, hasGlobTail };
}
function validateTarget(target: string): readonly string[] {
  const segments = splitPath(target, "target");
  for (const segment of segments) if (!SEGMENT.test(segment)) throw new TypeError(`Invalid target segment: ${segment}`);
  return segments;
}
function matchesScope(parsed: ParsedScope, target: readonly string[]): boolean {
  const minimumLength = parsed.hasGlobTail ? parsed.segments.length - 1 : parsed.segments.length;
  if (target.length < minimumLength || (!parsed.hasGlobTail && target.length !== parsed.segments.length)) return false;
  for (let i = 0; i < minimumLength; i += 1) {
    const expected = parsed.segments[i], actual = target[i];
    if (expected === undefined || actual === undefined || (expected !== "*" && expected !== actual)) return false;
  }
  return true;
}
function specificity(parsed: ParsedScope): number {
  return parsed.exactCount * 1000 + parsed.segments.length * 10 - parsed.wildcardCount - (parsed.hasGlobTail ? 100 : 0);
}
function validateDirective(directive: Directive): void {
  validateToken(directive.id, "Directive id");
  if (!Number.isSafeInteger(directive.authorityRank) || directive.authorityRank < 0)
    throw new TypeError(`Directive ${directive.id}: authorityRank must be a non-negative safe integer`);
  if (directive.localPriority !== undefined && !Number.isSafeInteger(directive.localPriority))
    throw new TypeError(`Directive ${directive.id}: localPriority must be a safe integer`);
  if (!SOURCE_CLASSES.has(directive.sourceClass)) throw new TypeError(`Directive ${directive.id}: unsupported sourceClass`);
  validateToken(directive.subject, `Directive ${directive.id}: subject`);
  parseScope(directive.scope); canonicalJson(directive.value);
  const keys = new Set<string>();
  for (const condition of directive.conditions ?? []) {
    validateToken(condition.key, `Directive ${directive.id}: condition key`);
    if (keys.has(condition.key)) throw new TypeError(`Directive ${directive.id}: duplicate condition key ${condition.key}`);
    keys.add(condition.key); canonicalJson(condition.equals);
  }
}
function conditionsMatch(d: Directive, context: Readonly<Record<string, JsonValue>>): boolean {
  for (const c of d.conditions ?? []) {
    const actual = context[c.key];
    if (actual === undefined || !jsonEqual(actual, c.equals)) return false;
  }
  return true;
}
function sameTier(a: EvaluatedDirective, b: EvaluatedDirective): boolean {
  return a.precedence[0] === b.precedence[0] && a.precedence[1] === b.precedence[1] && a.precedence[2] === b.precedence[2];
}
function comparePrecedence(a: EvaluatedDirective, b: EvaluatedDirective): number {
  if (a.precedence[0] !== b.precedence[0]) return a.precedence[0] - b.precedence[0];
  if (a.precedence[1] !== b.precedence[1]) return a.precedence[1] - b.precedence[1];
  if (a.precedence[2] !== b.precedence[2]) return a.precedence[2] - b.precedence[2];
  return stableTextCompare(a.directive.id, b.directive.id);
}
function normalizedInputFingerprint(request: CompileRequest): string {
  const directives = [...request.directives].map((d) => ({
    id: d.id, authorityRank: d.authorityRank, localPriority: d.localPriority ?? 0, sourceClass: d.sourceClass,
    scope: d.scope, subject: d.subject, value: canonicalize(d.value),
    conditions: [...(d.conditions ?? [])].map((c) => ({ key: c.key, equals: canonicalize(c.equals) }))
      .sort((a, b) => stableTextCompare(`${a.key}:${canonicalJson(a.equals)}`, `${b.key}:${canonicalJson(b.equals)}`)),
    provenance: d.provenance ?? null,
  })).sort((a, b) => stableTextCompare(a.id, b.id));
  return fingerprint({
    target: request.target, subject: request.subject, requireDecision: request.requireDecision === true,
    context: canonicalize(request.context ?? {}), directives,
  } as unknown as JsonValue);
}

export function compileAuthorityCollision(request: CompileRequest): Resolution {
  validateToken(request.subject, "Request subject");
  const target = validateTarget(request.target), context = request.context ?? {};
  const seen = new Set<string>();
  for (const d of request.directives) {
    validateDirective(d);
    if (seen.has(d.id)) throw new TypeError(`Duplicate directive id: ${d.id}`);
    seen.add(d.id);
  }
  canonicalJson(context as unknown as JsonValue);
  const inputFingerprint = normalizedInputFingerprint(request);
  const applicable: EvaluatedDirective[] = [], trace: DirectiveTrace[] = [];
  for (const d of request.directives) {
    if (d.subject !== request.subject) { trace.push({ id: d.id, disposition: "INAPPLICABLE", reason: "subject-mismatch" }); continue; }
    const parsed = parseScope(d.scope);
    if (!matchesScope(parsed, target)) { trace.push({ id: d.id, disposition: "INAPPLICABLE", reason: "scope-mismatch" }); continue; }
    if (!conditionsMatch(d, context)) { trace.push({ id: d.id, disposition: "INAPPLICABLE", reason: "condition-mismatch" }); continue; }
    const spec = specificity(parsed), priority = d.localPriority ?? 0;
    applicable.push({ directive: d, precedence: [d.authorityRank, -spec, -priority] });
  }
  applicable.sort(comparePrecedence);
  const traceSort = (a: DirectiveTrace, b: DirectiveTrace) => stableTextCompare(a.id, b.id);
  if (applicable.length === 0) {
    const status: ResolutionStatus = request.requireDecision === true ? "FREEZE_NO_DECISION" : "NO_DECISION";
    const base = { status, target: request.target, subject: request.subject, activeDirectiveIds: [] as string[], conflictDirectiveIds: [] as string[], trace: trace.sort(traceSort), inputFingerprint };
    return { ...base, fingerprint: fingerprint(base as unknown as JsonValue) };
  }
  const strongest = applicable[0];
  if (strongest === undefined) throw new Error("Invariant violation");
  const topTier = applicable.filter((x) => sameTier(x, strongest));
  const values = new Set(topTier.map((x) => canonicalJson(x.directive.value)));
  if (values.size > 1) {
    const conflictDirectiveIds = topTier.map((x) => x.directive.id).sort(stableTextCompare);
    for (const item of applicable) {
      const conflict = topTier.includes(item);
      trace.push({ id: item.directive.id, disposition: conflict ? "CONFLICT" : "SHADOWED", reason: conflict ? "equal-precedence-contradiction" : "weaker-than-conflicting-top-tier", precedence: item.precedence });
    }
    const base = { status: "FREEZE_CONFLICT" as const, target: request.target, subject: request.subject, activeDirectiveIds: [] as string[], conflictDirectiveIds, trace: trace.sort(traceSort), inputFingerprint };
    return { ...base, fingerprint: fingerprint(base as unknown as JsonValue) };
  }
  const activeValue = canonicalize(strongest.directive.value), activeDirectiveIds: string[] = [];
  for (const item of applicable) {
    if (sameTier(item, strongest)) {
      activeDirectiveIds.push(item.directive.id);
      trace.push({ id: item.directive.id, disposition: item.directive.id === strongest.directive.id ? "ACTIVE" : "REDUNDANT", reason: item.directive.id === strongest.directive.id ? "strongest-applicable-directive" : "same-precedence-same-value", precedence: item.precedence });
    } else {
      const consistent = jsonEqual(item.directive.value, activeValue);
      trace.push({ id: item.directive.id, disposition: consistent ? "REDUNDANT" : "SHADOWED", reason: consistent ? "weaker-consistent-directive" : "weaker-contradictory-directive", precedence: item.precedence });
    }
  }
  activeDirectiveIds.sort(stableTextCompare);
  const base = { status: "RESOLVED" as const, target: request.target, subject: request.subject, value: activeValue, activeDirectiveIds, conflictDirectiveIds: [] as string[], trace: trace.sort(traceSort), inputFingerprint };
  return { ...base, fingerprint: fingerprint(base as unknown as JsonValue) };
}

export function compileBatch(requests: readonly CompileRequest[]): BatchResolution {
  const resolutions = requests.map(compileAuthorityCollision).sort((a, b) => stableTextCompare(a.target, b.target) || stableTextCompare(a.subject, b.subject));
  const base = { resolutions, hasFreeze: resolutions.some((r) => r.status.startsWith("FREEZE_")) };
  return { ...base, fingerprint: fingerprint(base as unknown as JsonValue) };
}
