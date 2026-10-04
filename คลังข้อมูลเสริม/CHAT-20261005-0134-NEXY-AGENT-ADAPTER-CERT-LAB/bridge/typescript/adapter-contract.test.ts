import { simulateAdapterEvent, validateAdapterManifest } from "./adapter-contract";

function assert(condition: unknown, message: string): asserts condition {
  if (!condition) throw new Error(message);
}

const valid = {
  schema_version: "1.0",
  adapter: {
    id: "provider.example",
    provider: "ExampleAI",
    version: "1.2.0",
    supported_modes: ["fast", "strict", "audit"],
    deterministic_capable: true,
    critical: false,
    timeout_ms: 30000,
    context_capacity: 131072,
    operations: ["execute", "cancel", "healthcheck"],
  },
  authority: {
    candidate_only: true,
    direct_release: false,
    direct_vault_write: false,
    mutates_core_state: false,
    automatic_retry: false,
  },
  security: { secret_delivery: "runtime_injection", persists_secrets: false },
};

assert(validateAdapterManifest(valid).status === "PASS", "valid manifest should pass");
assert(simulateAdapterEvent(valid, "result_valid").action === "CONTINUE_TO_CROSS_VERIFY", "valid result must not release directly");
assert(simulateAdapterEvent(valid, "timeout", true).action === "EXCLUDE_AGENT_AND_CONTINUE", "noncritical timeout may exclude when quorum survives");
assert(simulateAdapterEvent(valid, "timeout", null).action === "FREEZE", "unknown quorum must freeze");

const critical = structuredClone(valid);
critical.adapter.id = "provider.critical";
critical.adapter.critical = true;
assert(simulateAdapterEvent(critical, "timeout", true).reason_code === "AGENT_TIMEOUT_CRITICAL", "critical timeout must freeze");

const invalid = structuredClone(valid);
invalid.authority.direct_release = true;
assert(validateAdapterManifest(invalid).status === "FAIL", "direct release must fail");

const badMode = structuredClone(valid) as any;
badMode.adapter.supported_modes = ["turbo"];
assert(validateAdapterManifest(badMode).status === "FAIL", "unknown mode must fail");

const badOperations = structuredClone(valid) as any;
badOperations.adapter.operations = ["execute", "cancel", "healthcheck", 7];
assert(validateAdapterManifest(badOperations).status === "FAIL", "non-string operation must fail");

const badSecret = structuredClone(valid) as any;
badSecret.security.persists_secrets = true;
assert(validateAdapterManifest(badSecret).status === "FAIL", "secret persistence must fail");

console.log("TypeScript mirror tests: PASS (9 assertions)");
