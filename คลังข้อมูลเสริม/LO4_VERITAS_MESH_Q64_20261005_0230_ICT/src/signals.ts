import { UnitQ64 } from "./q64.ts";

export interface SignalFrame {
  requirementClarity: UnitQ64;
  evidenceCoverage: UnitQ64;
  evidenceFreshness: UnitQ64;
  sourceDiversity: UnitQ64;
  contradictionPressure: UnitQ64;
  scopeDistance: UnitQ64;
  canonAlignment: UnitQ64;
  interfaceCompatibility: UnitQ64;
  regressionRisk: UnitQ64;
  failureObservability: UnitQ64;
  reversibility: UnitQ64;
  userValue: UnitQ64;
  safetyMargin: UnitQ64;
  deterministicReproducibility: UnitQ64;
  testCoverage: UnitQ64;
  uncertainty: UnitQ64;
  changeSurface: UnitQ64;
  agentDisagreement: UnitQ64;
  resourcePressure: UnitQ64;
  novelty: UnitQ64;
  rollbackReadiness: UnitQ64;
  dependencyStability: UnitQ64;
  provenanceCompleteness: UnitQ64;
  assumptionRatio: UnitQ64;
}

export type SignalName = keyof SignalFrame;

export function mapFrame(frame: SignalFrame, fn: (value: UnitQ64, key: SignalName) => UnitQ64): SignalFrame {
  const out = {} as SignalFrame;
  for (const key of Object.keys(frame) as SignalName[]) out[key] = fn(frame[key], key);
  return out;
}

export function frameFromRaw(raw: Record<SignalName, string>): SignalFrame {
  const out = {} as SignalFrame;
  for (const key of Object.keys(raw) as SignalName[]) out[key] = UnitQ64.fromRaw(BigInt(raw[key]));
  return out;
}

export function frameToRaw(frame: SignalFrame): Record<SignalName, string> {
  const out = {} as Record<SignalName, string>;
  for (const key of Object.keys(frame) as SignalName[]) out[key] = frame[key].toRawString();
  return out;
}
