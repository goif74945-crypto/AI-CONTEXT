import { describe, expect, it } from "vitest";
import {
  CAPABILITY_NODE_STATIC_REASON_CODES,
  CapabilityNodeRegistry,
  validateCapabilityNode,
  type CapabilityNode,
} from "../../packages/phase-f/universe/capability-node.js";

function node(overrides: Partial<CapabilityNode> = {}): CapabilityNode {
  return {
    capId: overrides.capId ?? "cap-" + (overrides.name ?? "base"),
    name: overrides.name ?? "base",
    scope: overrides.scope ?? "APP",
    description: overrides.description ?? "deterministic capability",
    version: overrides.version ?? "1.0.0",
    deprecated: false,
    dependencies: overrides.dependencies ?? [],
    forbidden_with: overrides.forbidden_with ?? [],
    resource_profile: overrides.resource_profile ?? { cpu_millicores: 100, memory_mib: 128 },
    permission_scope: overrides.permission_scope ?? ["app"],
    max_depth: overrides.max_depth ?? 5,
    deterministic_class: overrides.deterministic_class ?? "SANDBOXED",
  };
}

describe("CapabilityNode contract", () => {
  it("pins authoritative G22 static reason-code identity", () => {
    expect(CAPABILITY_NODE_STATIC_REASON_CODES).toEqual({
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
    });
  });

  it("deduplicates rejection identities and returns them in lexical order", () => {
    const failures = validateCapabilityNode(node({
      name: "multi-reject",
      scope: "APP",
      description: "eval(https://example.invalid)",
      permission_scope: ["KERNEL:override", "UNIVERSE:write"],
      resource_profile: { cpu_millicores: 1001, memory_mib: 128 },
    }), []);

    expect(failures).toEqual([
      "R002_PERMISSION_ESCALATION",
      "R003_RESOURCE_CAP_VIOLATION",
      "R005_UNDECLARED_NETWORK_SCOPE",
      "R006_DYNAMIC_CODE_LOADING",
    ]);
  });
  it("registers immutable DAG nodes and computes an order-independent envelope hash", () => {
    const registry = new CapabilityNodeRegistry();
    registry.register(node({ name: "base", version: "1.0.0" }));
    registry.register(node({ name: "child", version: "1.0.0", dependencies: ["base"] }));
    const hashBefore = registry.envelopeHash();
    expect(registry.get("child", "1.0.0")?.dependencies).toEqual(["base"]);
    registry.seal();
    expect(registry.isSealed()).toBe(true);
    expect(registry.envelopeHash()).toBe(hashBefore);
    expect(() => registry.register(node({ name: "late" }))).toThrow(/sealed/);
  });

  it("does not repurpose canonical R009 for duplicate-node rejection", () => {
    const registry = new CapabilityNodeRegistry();
    registry.register(node({ name: "duplicate", version: "1.0.0" }));
    expect(() => registry.register(node({ name: "duplicate", version: "1.0.0" })))
      .toThrow(/INTERNAL_DUPLICATE_NODE/);
  });

  it("rejects cycles, resource over-cap, and hidden network capability", () => {
    const known = [node({ name: "base" })];
    expect(validateCapabilityNode(node({ name: "cycle", dependencies: ["cycle"] }), known)).toContain("R001_DEPENDENCY_CYCLE");
    expect(validateCapabilityNode(node({ name: "too-big", resource_profile: { cpu_millicores: 1001 } }), known)).toContain("R003_RESOURCE_CAP_VIOLATION");
    expect(validateCapabilityNode(node({ name: "sneaky", description: "calls https://example.invalid" }), known)).toContain("R005_UNDECLARED_NETWORK_SCOPE");
  });

  it("rejects upward permission scope independently of syscall mismatch", () => {
    const failures = validateCapabilityNode(node({
      name: "scope-escalation",
      scope: "APP",
      permission_scope: ["UNIVERSE:write"],
    }), []);

    expect(failures).toContain("R002_PERMISSION_ESCALATION");
    expect(failures).not.toContain("INTERNAL_SYSCALL_SCOPE_MISMATCH");
  });

  it("rejects Kernel override permission markers even without a ranked scope", () => {
    const failures = validateCapabilityNode(node({
      name: "kernel-override",
      scope: "APP",
      permission_scope: ["KERNEL:override"],
    }), []);

    expect(failures).toContain("R002_PERMISSION_ESCALATION");
    expect(failures).not.toContain("INTERNAL_SYSCALL_SCOPE_MISMATCH");
  });

  it("rejects dependency paths that carry Kernel authority", () => {
    const kernelAuthority = node({
      name: "kernel-authority",
      scope: "KERNEL",
      permission_scope: ["KERNEL:authority"],
      max_depth: 0,
    });
    const failures = validateCapabilityNode(node({
      name: "kernel-dependent",
      scope: "APP",
      dependencies: ["kernel-authority"],
      permission_scope: ["APP:read"],
      max_depth: 1,
    }), [kernelAuthority]);

    expect(failures).toContain("R002_PERMISSION_ESCALATION");
  });

  it("keeps CapabilityNodeRegistry as staging/static verification, not runtime authority", () => {
    const registry = new CapabilityNodeRegistry();
    const staged = registry.register(node({
      name: "bounded",
      version: "1.0.0",
      resource_profile: { cpu_millicores: 50, memory_mib: 64 },
      max_depth: 0,
      deterministic_class: "SANDBOXED",
    }));
    expect(staged.dependencies).toEqual([]);
    expect(registry.validate(staged)).toEqual([]);
    registry.seal();
    expect(() => registry.register(node({ name: "late" }))).toThrow(/sealed/);
    expect("grant" in (registry as object)).toBe(false);
    expect("activate" in (registry as object)).toBe(false);
  });
});
