import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DEFAULT_POLICY_PATH = path.resolve(__dirname, "../config/default-policy.json");

export function loadDefaultPolicy() {
  return JSON.parse(fs.readFileSync(DEFAULT_POLICY_PATH, "utf8"));
}

export function mergePolicy(base, override = {}) {
  return {
    ...base,
    ...override,
    preserve: { ...base.preserve, ...(override.preserve ?? {}) },
    severity: { ...base.severity, ...(override.severity ?? {}) },
    canonicalTokens: override.canonicalTokens ?? base.canonicalTokens,
    protectedLiterals: override.protectedLiterals ?? base.protectedLiterals,
    supportedLanguages: override.supportedLanguages ?? base.supportedLanguages
  };
}
