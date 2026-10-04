import { canonicalize, canonicalStringify, sha256Hex, assertJsonSafe } from "./canonicalize.mjs";
import { fail } from "./errors.mjs";

const LIMITS = Object.freeze({
  manifestBytes: 1_000_000,
  enums: 256,
  enumMembersTotal: 4096,
  stateMachines: 64,
  transitionsTotal: 10_000,
  actorsPerTransition: 64,
  guardsPerTransition: 64,
  provenancePaths: 512,
});

const IDENTIFIER_RE = /^[A-Za-z][A-Za-z0-9_]{0,127}$/;
const WIRE_RE = /^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$/;
const CONTRACT_ID_RE = /^[a-z0-9][a-z0-9._:-]{0,191}$/;
const SEMVER_RE = /^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$/;
const SHA40_RE = /^[0-9a-f]{40}$/;

const TOP_KEYS = new Set(["schemaVersion", "contractId", "contractVersion", "provenance", "enums", "stateMachines"]);
const PROVENANCE_KEYS = new Set(["observedRepository", "observedRef", "observedPaths", "observedAt", "note"]);
const ENUM_KEYS = new Set(["name", "wireName", "members"]);
const MEMBER_KEYS = new Set(["name", "wire"]);
const MACHINE_KEYS = new Set(["name", "stateEnum", "eventEnum", "actorEnum", "initialState", "terminalStates", "transitions"]);
const TRANSITION_KEYS = new Set(["from", "event", "to", "actors", "guards"]);

function expectPlainObject(value, path) {
  if (value === null || typeof value !== "object" || Array.isArray(value)) {
    fail("TYPE_OBJECT_REQUIRED", "expected object", path);
  }
}

function expectArray(value, path) {
  if (!Array.isArray(value)) fail("TYPE_ARRAY_REQUIRED", "expected array", path);
}

function expectString(value, path, { min = 1, max = 256, regex = null } = {}) {
  if (typeof value !== "string") fail("TYPE_STRING_REQUIRED", "expected string", path);
  if (value.length < min || value.length > max) {
    fail("STRING_LENGTH", `length must be ${min}..${max}`, path);
  }
  if (regex && !regex.test(value)) fail("STRING_FORMAT", `invalid format: ${JSON.stringify(value)}`, path);
}

function expectAllowedKeys(object, allowed, path) {
  for (const key of Object.keys(object)) {
    if (!allowed.has(key)) fail("UNKNOWN_KEY", `unsupported key ${JSON.stringify(key)}`, `${path}.${key}`);
  }
}

function assertUnique(values, code, path, label) {
  const seen = new Set();
  for (const value of values) {
    if (seen.has(value)) fail(code, `duplicate ${label}: ${JSON.stringify(value)}`, path);
    seen.add(value);
  }
}

function normalizeProvenance(provenance) {
  if (provenance === undefined) return undefined;
  expectPlainObject(provenance, "$.provenance");
  expectAllowedKeys(provenance, PROVENANCE_KEYS, "$.provenance");
  const out = {};
  if (provenance.observedRepository !== undefined) {
    expectString(provenance.observedRepository, "$.provenance.observedRepository", { max: 256 });
    out.observedRepository = provenance.observedRepository;
  }
  if (provenance.observedRef !== undefined) {
    expectString(provenance.observedRef, "$.provenance.observedRef", { max: 256 });
    out.observedRef = provenance.observedRef;
  }
  if (provenance.observedPaths !== undefined) {
    expectArray(provenance.observedPaths, "$.provenance.observedPaths");
    if (provenance.observedPaths.length > LIMITS.provenancePaths) {
      fail("LIMIT_EXCEEDED", `observedPaths exceeds ${LIMITS.provenancePaths}`, "$.provenance.observedPaths");
    }
    for (let i = 0; i < provenance.observedPaths.length; i += 1) {
      expectString(provenance.observedPaths[i], `$.provenance.observedPaths[${i}]`, { max: 1024 });
    }
    assertUnique(provenance.observedPaths, "DUPLICATE_PROVENANCE_PATH", "$.provenance.observedPaths", "path");
    out.observedPaths = [...provenance.observedPaths].sort();
  }
  if (provenance.observedAt !== undefined) {
    expectString(provenance.observedAt, "$.provenance.observedAt", { max: 64 });
    if (Number.isNaN(Date.parse(provenance.observedAt))) {
      fail("INVALID_TIMESTAMP", "observedAt must be parseable ISO-8601 timestamp", "$.provenance.observedAt");
    }
    out.observedAt = provenance.observedAt;
  }
  if (provenance.note !== undefined) {
    expectString(provenance.note, "$.provenance.note", { max: 4096 });
    out.note = provenance.note;
  }
  return out;
}

function normalizeEnum(input, index) {
  const path = `$.enums[${index}]`;
  expectPlainObject(input, path);
  expectAllowedKeys(input, ENUM_KEYS, path);
  expectString(input.name, `${path}.name`, { regex: IDENTIFIER_RE, max: 128 });
  expectString(input.wireName, `${path}.wireName`, { regex: WIRE_RE, max: 128 });
  expectArray(input.members, `${path}.members`);
  if (input.members.length === 0) fail("EMPTY_ENUM", "enum must contain at least one member", `${path}.members`);
  const members = input.members.map((member, memberIndex) => {
    const memberPath = `${path}.members[${memberIndex}]`;
    expectPlainObject(member, memberPath);
    expectAllowedKeys(member, MEMBER_KEYS, memberPath);
    expectString(member.name, `${memberPath}.name`, { regex: IDENTIFIER_RE, max: 128 });
    expectString(member.wire, `${memberPath}.wire`, { regex: WIRE_RE, max: 128 });
    return { name: member.name, wire: member.wire };
  });
  assertUnique(members.map((x) => x.name), "DUPLICATE_ENUM_MEMBER_NAME", `${path}.members`, "member name");
  assertUnique(members.map((x) => x.wire), "DUPLICATE_ENUM_WIRE", `${path}.members`, "wire value");
  members.sort((a, b) => a.wire.localeCompare(b.wire) || a.name.localeCompare(b.name));
  return { name: input.name, wireName: input.wireName, members };
}

function enumWireSet(enumeration) {
  return new Set(enumeration.members.map((member) => member.wire));
}

function normalizeMachine(input, index, enumByName) {
  const path = `$.stateMachines[${index}]`;
  expectPlainObject(input, path);
  expectAllowedKeys(input, MACHINE_KEYS, path);
  expectString(input.name, `${path}.name`, { regex: IDENTIFIER_RE, max: 128 });
  for (const field of ["stateEnum", "eventEnum", "actorEnum"]) {
    expectString(input[field], `${path}.${field}`, { regex: IDENTIFIER_RE, max: 128 });
    if (!enumByName.has(input[field])) fail("UNKNOWN_ENUM_REFERENCE", `${field} references unknown enum ${JSON.stringify(input[field])}`, `${path}.${field}`);
  }
  const stateEnum = enumByName.get(input.stateEnum);
  const eventEnum = enumByName.get(input.eventEnum);
  const actorEnum = enumByName.get(input.actorEnum);
  const states = enumWireSet(stateEnum);
  const events = enumWireSet(eventEnum);
  const actors = enumWireSet(actorEnum);

  expectString(input.initialState, `${path}.initialState`, { regex: WIRE_RE, max: 128 });
  if (!states.has(input.initialState)) fail("UNKNOWN_STATE", `initialState ${JSON.stringify(input.initialState)} not in ${input.stateEnum}`, `${path}.initialState`);
  expectArray(input.terminalStates, `${path}.terminalStates`);
  for (let i = 0; i < input.terminalStates.length; i += 1) {
    const state = input.terminalStates[i];
    expectString(state, `${path}.terminalStates[${i}]`, { regex: WIRE_RE, max: 128 });
    if (!states.has(state)) fail("UNKNOWN_STATE", `terminal state ${JSON.stringify(state)} not in ${input.stateEnum}`, `${path}.terminalStates[${i}]`);
  }
  assertUnique(input.terminalStates, "DUPLICATE_TERMINAL_STATE", `${path}.terminalStates`, "terminal state");
  if (input.terminalStates.includes(input.initialState)) {
    fail("INITIAL_STATE_TERMINAL", "initial state cannot also be terminal", `${path}.initialState`);
  }

  expectArray(input.transitions, `${path}.transitions`);
  const semanticKeys = new Map();
  const transitions = input.transitions.map((transition, transitionIndex) => {
    const transitionPath = `${path}.transitions[${transitionIndex}]`;
    expectPlainObject(transition, transitionPath);
    expectAllowedKeys(transition, TRANSITION_KEYS, transitionPath);
    for (const field of ["from", "event", "to"]) {
      expectString(transition[field], `${transitionPath}.${field}`, { regex: WIRE_RE, max: 128 });
    }
    if (!states.has(transition.from)) fail("UNKNOWN_STATE", `unknown from state ${JSON.stringify(transition.from)}`, `${transitionPath}.from`);
    if (!states.has(transition.to)) fail("UNKNOWN_STATE", `unknown to state ${JSON.stringify(transition.to)}`, `${transitionPath}.to`);
    if (!events.has(transition.event)) fail("UNKNOWN_EVENT", `unknown event ${JSON.stringify(transition.event)}`, `${transitionPath}.event`);
    if (input.terminalStates.includes(transition.from)) {
      fail("TERMINAL_OUTBOUND_TRANSITION", `terminal state ${transition.from} cannot have outbound transitions`, `${transitionPath}.from`);
    }
    expectArray(transition.actors, `${transitionPath}.actors`);
    if (transition.actors.length === 0) fail("EMPTY_ACTORS", "transition must authorize at least one actor", `${transitionPath}.actors`);
    if (transition.actors.length > LIMITS.actorsPerTransition) fail("LIMIT_EXCEEDED", `actors exceeds ${LIMITS.actorsPerTransition}`, `${transitionPath}.actors`);
    for (let actorIndex = 0; actorIndex < transition.actors.length; actorIndex += 1) {
      const actor = transition.actors[actorIndex];
      expectString(actor, `${transitionPath}.actors[${actorIndex}]`, { regex: WIRE_RE, max: 128 });
      if (!actors.has(actor)) fail("UNKNOWN_ACTOR", `unknown actor ${JSON.stringify(actor)}`, `${transitionPath}.actors[${actorIndex}]`);
    }
    assertUnique(transition.actors, "DUPLICATE_ACTOR", `${transitionPath}.actors`, "actor");
    const guards = transition.guards ?? [];
    expectArray(guards, `${transitionPath}.guards`);
    if (guards.length > LIMITS.guardsPerTransition) fail("LIMIT_EXCEEDED", `guards exceeds ${LIMITS.guardsPerTransition}`, `${transitionPath}.guards`);
    for (let guardIndex = 0; guardIndex < guards.length; guardIndex += 1) {
      expectString(guards[guardIndex], `${transitionPath}.guards[${guardIndex}]`, { regex: WIRE_RE, max: 128 });
    }
    assertUnique(guards, "DUPLICATE_GUARD", `${transitionPath}.guards`, "guard");
    const normalizedActors = [...transition.actors].sort();
    const normalizedGuards = [...guards].sort();
    for (const actor of normalizedActors) {
      const key = `${transition.from}\u0000${transition.event}\u0000${actor}`;
      const semantics = `${transition.to}\u0000${normalizedGuards.join("\u0001")}`;
      if (semanticKeys.has(key)) {
        const previous = semanticKeys.get(key);
        fail(
          previous === semantics ? "DUPLICATE_TRANSITION" : "NON_DETERMINISTIC_TRANSITION",
          `duplicate decision key from=${transition.from} event=${transition.event} actor=${actor}`,
          transitionPath,
        );
      }
      semanticKeys.set(key, semantics);
    }
    return {
      from: transition.from,
      event: transition.event,
      to: transition.to,
      actors: normalizedActors,
      guards: normalizedGuards,
    };
  });
  transitions.sort((a, b) => {
    const ka = canonicalStringify(a);
    const kb = canonicalStringify(b);
    return ka.localeCompare(kb);
  });
  return {
    name: input.name,
    stateEnum: input.stateEnum,
    eventEnum: input.eventEnum,
    actorEnum: input.actorEnum,
    initialState: input.initialState,
    terminalStates: [...input.terminalStates].sort(),
    transitions,
  };
}

export function normalizeAndValidateManifest(input) {
  assertJsonSafe(input);
  const rawSize = Buffer.byteLength(JSON.stringify(input), "utf8");
  if (rawSize > LIMITS.manifestBytes) fail("LIMIT_EXCEEDED", `manifest exceeds ${LIMITS.manifestBytes} bytes`, "$");
  expectPlainObject(input, "$");
  expectAllowedKeys(input, TOP_KEYS, "$");
  if (input.schemaVersion !== 1) fail("UNSUPPORTED_SCHEMA_VERSION", "schemaVersion must equal 1", "$.schemaVersion");
  expectString(input.contractId, "$.contractId", { regex: CONTRACT_ID_RE, max: 192 });
  expectString(input.contractVersion, "$.contractVersion", { regex: SEMVER_RE, max: 128 });
  expectArray(input.enums, "$.enums");
  expectArray(input.stateMachines, "$.stateMachines");
  if (input.enums.length === 0) fail("EMPTY_ENUM_COLLECTION", "at least one enum is required", "$.enums");
  if (input.enums.length > LIMITS.enums) fail("LIMIT_EXCEEDED", `enums exceeds ${LIMITS.enums}`, "$.enums");
  if (input.stateMachines.length > LIMITS.stateMachines) fail("LIMIT_EXCEEDED", `stateMachines exceeds ${LIMITS.stateMachines}`, "$.stateMachines");

  const enums = input.enums.map(normalizeEnum);
  assertUnique(enums.map((x) => x.name), "DUPLICATE_ENUM_NAME", "$.enums", "enum name");
  assertUnique(enums.map((x) => x.wireName), "DUPLICATE_ENUM_WIRE_NAME", "$.enums", "enum wireName");
  const memberTotal = enums.reduce((sum, enumeration) => sum + enumeration.members.length, 0);
  if (memberTotal > LIMITS.enumMembersTotal) fail("LIMIT_EXCEEDED", `enum members exceeds ${LIMITS.enumMembersTotal}`, "$.enums");
  enums.sort((a, b) => a.name.localeCompare(b.name));
  const enumByName = new Map(enums.map((enumeration) => [enumeration.name, enumeration]));

  let transitionTotal = 0;
  const stateMachines = input.stateMachines.map((machine, index) => {
    const normalized = normalizeMachine(machine, index, enumByName);
    transitionTotal += normalized.transitions.length;
    if (transitionTotal > LIMITS.transitionsTotal) fail("LIMIT_EXCEEDED", `transitions exceeds ${LIMITS.transitionsTotal}`, "$.stateMachines");
    return normalized;
  });
  assertUnique(stateMachines.map((x) => x.name), "DUPLICATE_MACHINE_NAME", "$.stateMachines", "state machine name");
  stateMachines.sort((a, b) => a.name.localeCompare(b.name));

  const provenance = normalizeProvenance(input.provenance);
  const normalized = {
    schemaVersion: 1,
    contractId: input.contractId,
    contractVersion: input.contractVersion,
    ...(provenance !== undefined ? { provenance } : {}),
    enums,
    stateMachines,
  };
  const semantic = {
    schemaVersion: normalized.schemaVersion,
    contractId: normalized.contractId,
    contractVersion: normalized.contractVersion,
    enums: normalized.enums,
    stateMachines: normalized.stateMachines,
  };
  return {
    normalized: canonicalize(normalized),
    semantic: canonicalize(semantic),
    semanticFingerprint: sha256Hex(semantic),
    manifestFingerprint: sha256Hex(normalized),
    limits: LIMITS,
  };
}

export function assertObservedCommitRefIfSha(manifest) {
  const ref = manifest?.provenance?.observedRef;
  if (ref !== undefined && /^[0-9a-f]+$/.test(ref) && !SHA40_RE.test(ref)) {
    fail("INVALID_GIT_SHA", "hex observedRef must be a full 40-character lowercase commit SHA", "$.provenance.observedRef");
  }
}
