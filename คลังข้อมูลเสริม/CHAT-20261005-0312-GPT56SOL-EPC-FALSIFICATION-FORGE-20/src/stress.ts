import { Q64 } from "./q64";
import { ForgeError, canonicalStrings, nonEmpty, sixDigit } from "./core";
export interface EnvironmentObservation { readonly environment: string; readonly metrics: Readonly<Record<string,Q64>>; }
export interface Sensitivity { readonly minimum: Q64; readonly maximum: Q64; readonly span: Q64; }

export function environmentalSensitivityMatrix(observations: readonly EnvironmentObservation[]): Readonly<Record<string,Sensitivity>> {
  if (observations.length < 2) throw new ForgeError("at least two environments are required");
  const normalized = [...observations].sort((a,b)=>nonEmpty(a.environment,"environment").localeCompare(nonEmpty(b.environment,"environment")));
  const first = normalized[0];
  if (first === undefined) throw new ForgeError("missing first environment");
  const keys = Object.keys(first.metrics).sort();
  if (keys.length === 0) throw new ForgeError("metrics must be non-empty");
  const out: Record<string,Sensitivity> = {};
  for (const key of keys) {
    let min: Q64 | undefined;
    let max: Q64 | undefined;
    for (const observation of normalized) {
      const value = observation.metrics[key];
      if (value === undefined) throw new ForgeError(`metric ${key} missing in environment ${observation.environment}`);
      min = min === undefined ? value : min.min(value);
      max = max === undefined ? value : max.max(value);
    }
    if (min === undefined || max === undefined) throw new ForgeError("metric aggregation failed");
    out[key] = Object.freeze({minimum:min,maximum:max,span:max.sub(min)});
  }
  for (const observation of normalized) {
    const otherKeys = Object.keys(observation.metrics).sort();
    if (otherKeys.join("\u0000") !== keys.join("\u0000")) throw new ForgeError("environment metric sets differ");
  }
  return Object.freeze(out);
}

export interface DeterminismProbe { readonly id: string; readonly inputId: string; readonly expected: "BYTE_IDENTICAL_REPLAY"; }
export function determinismProbeGenerator(inputId: string, repetitions: bigint): readonly DeterminismProbe[] {
  const id = nonEmpty(inputId, "input id");
  if (repetitions <= 0n || repetitions > 999999n) throw new ForgeError("repetitions must be in [1,999999]");
  const probes: DeterminismProbe[] = [];
  let ordinal = 1n;
  while (ordinal <= repetitions) {
    probes.push(Object.freeze({id:`DET-${id}-${sixDigit(ordinal)}`,inputId:id,expected:"BYTE_IDENTICAL_REPLAY" as const}));
    ordinal += 1n;
  }
  return Object.freeze(probes);
}

export interface ResourceProbe { readonly id:string; readonly resource:string; readonly position:"BELOW_MIN"|"AT_MIN"|"AT_MAX"|"ABOVE_MAX"; readonly value:Q64; }
export function resourceEnvelopeProbe(resource:string,minimum:Q64,maximum:Q64):readonly ResourceProbe[]{
  const name=nonEmpty(resource,"resource");
  if(minimum.raw<0n) throw new ForgeError("resource minimum must be non-negative");
  if(minimum.compare(maximum)>0) throw new ForgeError("resource minimum exceeds maximum");
  if(minimum.raw===Q64.MIN_RAW || maximum.raw===Q64.MAX_RAW) throw new ForgeError("resource boundary cannot be probed outside signed-128 range");
  const rows:readonly [ResourceProbe["position"],bigint][]=[
    ["BELOW_MIN",minimum.raw-1n],["AT_MIN",minimum.raw],["AT_MAX",maximum.raw],["ABOVE_MAX",maximum.raw+1n]
  ];
  return Object.freeze(rows.map(([position,raw],index)=>Object.freeze({id:`REP-${name}-${String(index+1).padStart(2,"0")}`,resource:name,position,value:Q64.fromRaw(raw)})));
}

export interface VersionDifference { readonly key:string; readonly before:string|undefined; readonly after:string|undefined; }
export function crossVersionDifferentialExperiment(
  before:Readonly<Record<string,string>>,after:Readonly<Record<string,string>>
):readonly VersionDifference[]{
  const keys=[...new Set([...Object.keys(before),...Object.keys(after)])].sort();
  const differences:VersionDifference[]=[];
  for(const key of keys){
    const left=before[key]; const right=after[key];
    if(left!==right) differences.push(Object.freeze({key,before:left,after:right}));
  }
  return Object.freeze(differences);
}

export interface ObservabilityContract { readonly falsifier:string; readonly signal:string; readonly obligation:"MUST_BE_OBSERVABLE"; }
export function observabilityProbeContractCompiler(
  falsifiers:readonly string[],signalByFalsifier:Readonly<Record<string,string>>
):readonly ObservabilityContract[]{
  const normalized=canonicalStrings(falsifiers,"falsifier");
  return Object.freeze(normalized.map((falsifier)=>{
    const signal=signalByFalsifier[falsifier];
    if(signal===undefined) throw new ForgeError(`missing observable signal for falsifier: ${falsifier}`);
    return Object.freeze({falsifier,signal:nonEmpty(signal,"observable signal"),obligation:"MUST_BE_OBSERVABLE" as const});
  }));
}

