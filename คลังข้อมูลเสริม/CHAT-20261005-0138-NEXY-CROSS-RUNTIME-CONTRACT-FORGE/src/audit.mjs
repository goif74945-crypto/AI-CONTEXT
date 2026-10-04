import { canonicalize, canonicalStringify } from "./canonicalize.mjs";
import { normalizeAndValidateManifest } from "./validate-manifest.mjs";

export function buildExpectedRuntimeSnapshot(inputManifest) {
  const { normalized, semanticFingerprint } = normalizeAndValidateManifest(inputManifest);
  const enums = Object.create(null);
  for (const enumeration of normalized.enums) {
    enums[enumeration.wireName] = enumeration.members.map((member) => member.wire);
  }
  const stateMachines = Object.create(null);
  for (const machine of normalized.stateMachines) {
    stateMachines[machine.name] = {
      stateEnum: normalized.enums.find((x) => x.name === machine.stateEnum).wireName,
      eventEnum: normalized.enums.find((x) => x.name === machine.eventEnum).wireName,
      actorEnum: normalized.enums.find((x) => x.name === machine.actorEnum).wireName,
      initialState: machine.initialState,
      terminalStates: machine.terminalStates,
      transitions: machine.transitions,
    };
  }
  return canonicalize({
    snapshotSchemaVersion: 1,
    contractId: normalized.contractId,
    contractVersion: normalized.contractVersion,
    semanticFingerprint,
    enums,
    stateMachines,
  });
}

function typeOf(value) {
  if (value === null) return "null";
  if (Array.isArray(value)) return "array";
  return typeof value;
}

export function diffJson(expected, observed, path = "$") {
  const diffs = [];
  const expectedType = typeOf(expected);
  const observedType = typeOf(observed);
  if (expectedType !== observedType) {
    return [{ path, kind: "TYPE_MISMATCH", expected: expectedType, observed: observedType }];
  }
  if (expectedType === "array") {
    const max = Math.max(expected.length, observed.length);
    for (let i = 0; i < max; i += 1) {
      const childPath = `${path}[${i}]`;
      if (i >= expected.length) diffs.push({ path: childPath, kind: "UNEXPECTED_VALUE", observed: observed[i] });
      else if (i >= observed.length) diffs.push({ path: childPath, kind: "MISSING_VALUE", expected: expected[i] });
      else diffs.push(...diffJson(expected[i], observed[i], childPath));
    }
    return diffs;
  }
  if (expectedType === "object") {
    const keys = [...new Set([...Object.keys(expected), ...Object.keys(observed)])].sort();
    for (const key of keys) {
      const childPath = `${path}.${key}`;
      if (!Object.prototype.hasOwnProperty.call(expected, key)) diffs.push({ path: childPath, kind: "UNEXPECTED_KEY", observed: observed[key] });
      else if (!Object.prototype.hasOwnProperty.call(observed, key)) diffs.push({ path: childPath, kind: "MISSING_KEY", expected: expected[key] });
      else diffs.push(...diffJson(expected[key], observed[key], childPath));
    }
    return diffs;
  }
  if (!Object.is(expected, observed)) {
    diffs.push({ path, kind: "VALUE_MISMATCH", expected, observed });
  }
  return diffs;
}

export function auditRuntimeSnapshot(inputManifest, observedSnapshot) {
  const expected = buildExpectedRuntimeSnapshot(inputManifest);
  const observed = canonicalize(observedSnapshot);
  const diffs = diffJson(expected, observed);
  return {
    pass: diffs.length === 0,
    status: diffs.length === 0 ? "PASS" : "FAIL",
    expectedFingerprint: expected.semanticFingerprint,
    observedFingerprint: typeof observed.semanticFingerprint === "string" ? observed.semanticFingerprint : null,
    diffs,
    expectedCanonical: canonicalStringify(expected),
    observedCanonical: canonicalStringify(observed),
  };
}
