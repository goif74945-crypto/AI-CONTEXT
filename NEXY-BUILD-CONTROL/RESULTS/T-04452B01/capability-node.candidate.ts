import { compareCanonicalText } from "../../core/canonical-order.js";
import { createHash } from "node:crypto";

export type CapabilityResourceValue = string | number | boolean | undefined;
export interface CapabilityResourceProfile {
  readonly cpu_millicores?: number;
  readonly memory_mib?: number;
  readonly [key: string]: CapabilityResourceValue;
}

/** Immutable, source-aligned metadata for a CapabilityNode. */
export interface CapabilityNodeDefinition {
  readonly id?: string;
  readonly version: string;
  readonly dependencies: readonly string[];
  readonly forbidden_with: readonly string[];
  readonly resource_profile: CapabilityResourceProfile;
  readonly permission_scope: readonly string[];
  readonly max_depth: number;
  readonly deterministic_class: string;
}

export interface CapabilityNode extends CapabilityNodeDefinition {
  readonly id?: string;
  readonly capId: string;
  readonly name: string;
  readonly scope: string;
  readonly description: string;
  readonly deprecated: boolean;
}

export const CAPABILITY_NODE_STATIC_REASON_CODES = {
  R001: "R001_DEPENDENCY_CYCLE",
  R002: "R002_PERMISSION_ESCALATION",
  R003: "R003_RESOURCE_CAP_VIOLATION",
  R004: "R004_DETERMINISM_CLASS_VIOLATION",
  R005: "R005_UNDECLARED_NETWORK_SCOPE",
  R006: "R006_DYNAMIC_CODE_LOADING",
  R007: "R007_NONDET_SYSCALL",
  R008: "R008_SCHEMA_NONCANONICAL",
  R009: "R009_CONTAINER_DIGEST_MISMATCH",
  R010: "R010_SPEC_HASH_DRIFT",
} as const;

export type CapabilityNodeStaticReasonCode =
  (typeof CAPABILITY_NODE_STATIC_REASON_CODES)[keyof typeof CAPABILITY_NODE_STATIC_REASON_CODES];

export type CapabilityNodeValidationCode =
  | CapabilityNodeStaticReasonCode
  | "INTERNAL_FORBIDDEN_COMBINATION"
  | "INTERNAL_SYSCALL_SCOPE_MISMATCH"
  | "INTERNAL_UNKNOWN_DEPENDENCY";

const MAX_DEPTH = 5;
const CPU_LIMIT = 1000;
const MEMORY_LIMIT = 4096;
const SCOPE_RANK: Record<string, number> = {
  APP: 1,
  CHANNEL: 2,
  STORAGE: 3,
  COMPUTE: 4,
  NETWORK: 5,
  UNIVERSE: 6,
};
const DYNAMIC_CODE = /(?:eval\s*\(|new\s+Function|vm\.|dlopen|code[_ -]?load|require\s*\(|import\s*\()/i;
const NETWORK_MARKER = /(?:\bhttps?:\/\/|\bsocket\b|\bdns\b|\btcp\b|\budp\b|\begress\b|\bnetwork\b)/i;
const AUTHORITY_ESCALATION_MARKER = /(?:\bkernel\b|\bauthority\b|\boverride\b)/i;

function unique(values: readonly string[]): string[] {
  return Array.from(new Set(values.map((value) => value.trim()).filter(Boolean)));
}

function nodeIdentity(node: CapabilityNode): string {
  return (node.id ?? node.capId ?? node.name ?? "").trim();
}

export function capabilityNodeKey(node: CapabilityNode): string {
  return nodeIdentity(node) + "@" + node.version;
}

function nodeText(node: CapabilityNode): string {
  return [node.id, node.name, node.description, ...node.permission_scope, JSON.stringify(node.resource_profile)].join(" ");
}

function byReference(nodes: readonly CapabilityNode[], reference: string): CapabilityNode | undefined {
  return nodes.find((node) => node.id === reference || node.name === reference || node.capId === reference || capabilityNodeKey(node) === reference);
}

/** Pure static verifier; no registry state is mutated on rejection. */
export function validateCapabilityNode(
  candidate: CapabilityNode,
  knownNodes: readonly CapabilityNode[] = [],
): readonly CapabilityNodeValidationCode[] {
  const failures: CapabilityNodeValidationCode[] = [];
  const dependencies = unique(candidate.dependencies);
  const forbidden = unique(candidate.forbidden_with);
  const identity = nodeText(candidate);
  const ids = [candidate.id, candidate.capId, candidate.name].filter(Boolean) as string[];

  if (!(candidate.id ?? candidate.capId ?? candidate.name ?? "").trim() || !candidate.version.trim() || !candidate.deterministic_class.trim()) {
    failures.push("R008_SCHEMA_NONCANONICAL");
  }
  if (!Number.isInteger(candidate.max_depth) || candidate.max_depth < 0 || candidate.max_depth > MAX_DEPTH) {
    failures.push("R008_SCHEMA_NONCANONICAL");
  }
  if (dependencies.length !== candidate.dependencies.length) failures.push("R008_SCHEMA_NONCANONICAL");
  if (forbidden.length !== candidate.forbidden_with.length) failures.push("INTERNAL_FORBIDDEN_COMBINATION");
  if (dependencies.some((dependency) => ids.includes(dependency))) {
    failures.push("R001_DEPENDENCY_CYCLE");
  }
  if (dependencies.some((dependency) => forbidden.includes(dependency))) {
    failures.push("INTERNAL_FORBIDDEN_COMBINATION");
  }
  if (DYNAMIC_CODE.test(identity)) failures.push("R006_DYNAMIC_CODE_LOADING");
  if (candidate.scope !== "NETWORK" && NETWORK_MARKER.test(identity)) {
    failures.push("R005_UNDECLARED_NETWORK_SCOPE");
  }
  const candidateScopeRank = typeof candidate.scope === "string" ? SCOPE_RANK[candidate.scope.toUpperCase()] : undefined;
  if (AUTHORITY_ESCALATION_MARKER.test(candidate.scope)) {
    failures.push("R002_PERMISSION_ESCALATION");
  }
  for (const permission of candidate.permission_scope) {
    if (AUTHORITY_ESCALATION_MARKER.test(permission)) {
      failures.push("R002_PERMISSION_ESCALATION");
      continue;
    }
    const permissionScope = permission.split(":")[0]?.trim().toUpperCase();
    const permissionRank = permissionScope ? SCOPE_RANK[permissionScope] : undefined;
    if (permissionRank !== undefined && candidateScopeRank !== undefined && permissionRank > candidateScopeRank) {
      failures.push("R002_PERMISSION_ESCALATION");
    }
  }
  if (candidate.permission_scope.some((scope) => /^syscall:/i.test(scope) && scope.toLowerCase() !== "syscall:" + candidate.scope.toLowerCase())) {
    failures.push("INTERNAL_SYSCALL_SCOPE_MISMATCH");
  }
  for (const [key, value] of Object.entries(candidate.resource_profile)) {
    const normalized = key.toLowerCase();
    if (normalized.includes("cpu") || normalized.includes("millicore")) {
      if (typeof value !== "number" || Number.isFinite(value) === false || value < 0 || value > CPU_LIMIT) {
        failures.push("R003_RESOURCE_CAP_VIOLATION");
      }
    }
    if (normalized.includes("memory") || normalized.includes("mib")) {
      if (typeof value !== "number" || Number.isFinite(value) === false || value < 0 || value > MEMORY_LIMIT) {
        failures.push("R003_RESOURCE_CAP_VIOLATION");
      }
    }
  }

  const resolve = (reference: string): CapabilityNode | undefined => byReference(knownNodes, reference);
  const visiting = new Set<string>();
  const visited = new Set<string>();
  const depthOf = (node: CapabilityNode): number => {
    const key = capabilityNodeKey(node);
    if (visiting.has(key)) {
      failures.push("R001_DEPENDENCY_CYCLE");
      return MAX_DEPTH + 1;
    }
    if (visited.has(key)) return 0;
    visiting.add(key);
    let depth = 0;
    for (const reference of node.dependencies) {
      const dependency = node === candidate && ids.includes(reference) ? candidate : resolve(reference);
      if (!dependency) {
        failures.push("INTERNAL_UNKNOWN_DEPENDENCY");
        continue;
      }
      const dependencyScopeRank = SCOPE_RANK[dependency.scope.toUpperCase()];
      if (
        AUTHORITY_ESCALATION_MARKER.test(dependency.scope) ||
        dependency.permission_scope.some((scope) => AUTHORITY_ESCALATION_MARKER.test(scope)) ||
        (dependencyScopeRank !== undefined && candidateScopeRank !== undefined && dependencyScopeRank > candidateScopeRank)
      ) {
        failures.push("R002_PERMISSION_ESCALATION");
      }
      depth = Math.max(depth, 1 + depthOf(dependency));
    }
    visiting.delete(key);
    visited.add(key);
    return depth;
  };
  const dependencyDepth = depthOf(candidate);
  if (dependencyDepth > MAX_DEPTH || dependencyDepth > candidate.max_depth) failures.push("R008_SCHEMA_NONCANONICAL");

  for (const reference of forbidden) {
    const forbiddenNode = resolve(reference);
    if (forbiddenNode && (forbiddenNode.forbidden_with.includes(candidate.name) || forbiddenNode.dependencies.includes(candidate.name))) {
      failures.push("INTERNAL_FORBIDDEN_COMBINATION");
    }
  }
  return Array.from(new Set(failures)).sort(compareCanonicalText);
}

export function capabilityNodeHash(node: CapabilityNode): string {
  const canonical = JSON.stringify({
    id: nodeIdentity(node),
    name: node.name,
    version: node.version,
    scope: node.scope,
    dependencies: Array.from(node.dependencies).sort(compareCanonicalText),
    forbidden_with: Array.from(node.forbidden_with).sort(compareCanonicalText),
    resource_profile: Object.fromEntries(Object.entries(node.resource_profile).sort(([a], [b]) => compareCanonicalText(a, b))),
    permission_scope: Array.from(node.permission_scope).sort(compareCanonicalText),
    max_depth: node.max_depth,
    deterministic_class: node.deterministic_class,
  });
  return createHash("sha256").update(canonical).digest("hex");
}

export class CapabilityNodeRegistry {
  private readonly nodesByKey = new Map<string, CapabilityNode>();
  private sealed = false;

  register(node: CapabilityNode): CapabilityNode {
    if (this.sealed) throw new Error("Capability node registry is sealed");
    const key = capabilityNodeKey(node);
    if (this.nodesByKey.has(key)) throw new Error("R009_DUPLICATE_NODE:" + key);
    const failures = validateCapabilityNode(node, Array.from(this.nodesByKey.values()));
    if (failures.length > 0) throw new Error("CapabilityNode rejected:" + failures.join(","));
    const frozen: CapabilityNode = Object.freeze({
      ...node,
      id: node.id ?? node.capId ?? node.name,
      dependencies: Object.freeze(Array.from(node.dependencies)),
      forbidden_with: Object.freeze(Array.from(node.forbidden_with)),
      permission_scope: Object.freeze(Array.from(node.permission_scope)),
      resource_profile: Object.freeze({ ...node.resource_profile }),
    });
    this.nodesByKey.set(key, frozen);
    return frozen;
  }

  validate(node: CapabilityNode): readonly string[] {
    return validateCapabilityNode(node, Array.from(this.nodesByKey.values()));
  }

  seal(): void { this.sealed = true; }
  isSealed(): boolean { return this.sealed; }
  get(name: string, version?: string): CapabilityNode | undefined {
    return version
        ? Array.from(this.nodesByKey.values()).find((node) => node.version === version && (node.id === name || node.capId === name || node.name === name || capabilityNodeKey(node) === name + "@" + version))
        : Array.from(this.nodesByKey.values()).find((node) => node.id === name || node.capId === name || node.name === name);
  }
  list(): readonly CapabilityNode[] { return Array.from(this.nodesByKey.values()); }
  envelopeHash(): string {
    const hashes = this.list().map(capabilityNodeHash).sort(compareCanonicalText).join("|");
    return createHash("sha256").update(hashes || "empty").digest("hex");
  }
}
