const fs = require("fs");
const path = require("path");
const { validateAdapterManifest, simulateAdapterEvent } = require("./.build/adapter-contract.js");
const ROOT = path.resolve(__dirname, "../..");
const load = (name) => JSON.parse(fs.readFileSync(path.join(ROOT, "fixtures", name), "utf8"));
const cases = {
  valid_noncritical: validateAdapterManifest(load("valid-noncritical.json")).status,
  valid_critical: validateAdapterManifest(load("valid-critical.json")).status,
  invalid_critical_timeout: validateAdapterManifest(load("invalid-critical-timeout.json")).status,
  invalid_authority_escalation: validateAdapterManifest(load("invalid-authority-escalation.json")).status,
  valid_result: simulateAdapterEvent(load("valid-noncritical.json"), "result_valid").action,
  schema_invalid: simulateAdapterEvent(load("valid-noncritical.json"), "result_schema_invalid").action,
  noncritical_timeout_quorum: simulateAdapterEvent(load("valid-noncritical.json"), "timeout", true).action,
  noncritical_timeout_no_quorum: simulateAdapterEvent(load("valid-noncritical.json"), "timeout", false).action,
  noncritical_timeout_unknown: simulateAdapterEvent(load("valid-noncritical.json"), "timeout", null).action,
  critical_timeout: simulateAdapterEvent(load("valid-critical.json"), "timeout", true).action,
};
process.stdout.write(JSON.stringify(cases, Object.keys(cases).sort()) + "\n");
