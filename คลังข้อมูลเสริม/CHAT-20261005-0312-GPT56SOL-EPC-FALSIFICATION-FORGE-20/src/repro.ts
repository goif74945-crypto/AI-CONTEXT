import { Q64 } from "./q64";
import { ForgeError, canonicalStrings, countBig, nonEmpty } from "./core";
function canonicalRecord(record:Readonly<Record<string,string>>):string{
  return Object.keys(record).sort().map((key)=>`${encodeURIComponent(key)}=${encodeURIComponent(record[key] ?? "")}`).join("&");
}

function fnv1a64(text:string):string{
  let hash=0xcbf29ce484222325n;
  const prime=0x100000001b3n;
  const mask=0xffffffffffffffffn;
  for(let index=0;index<text.length;index+=1){
    const code=text.charCodeAt(index);
    // Canonical payload is URI-encoded ASCII before hashing, so every code unit is one byte.
    if(code>0x7f) throw new ForgeError("internal checksum input must be ASCII");
    hash^=BigInt(code);
    hash=(hash*prime)&mask;
  }
  return hash.toString(16).padStart(16,"0");
}

export interface ReproducibilityCapsule {
  readonly metadata:Readonly<Record<string,string>>;
  readonly commands:readonly string[];
  readonly environment:readonly string[];
  readonly canonicalPayload:string;
  readonly checksumAlgorithm:"FNV1A64_NON_SECURITY";
  readonly checksum:string;
}
export function reproducibilityCapsuleBuilder(
  metadata:Readonly<Record<string,string>>,commands:readonly string[],environment:readonly string[]
):ReproducibilityCapsule{
  const canonicalMetadata=Object.freeze(Object.fromEntries(Object.keys(metadata).sort().map((key)=>[nonEmpty(key,"metadata key"),nonEmpty(metadata[key] ?? "","metadata value")])));
  const canonicalCommands=Object.freeze(canonicalStrings(commands,"command"));
  const canonicalEnvironment=Object.freeze(canonicalStrings(environment,"environment descriptor"));
  const payload=`M:${encodeURIComponent(canonicalRecord(canonicalMetadata))}|C:${canonicalCommands.map(encodeURIComponent).join(",")}|E:${canonicalEnvironment.map(encodeURIComponent).join(",")}`;
  return Object.freeze({metadata:canonicalMetadata,commands:canonicalCommands,environment:canonicalEnvironment,canonicalPayload:payload,checksumAlgorithm:"FNV1A64_NON_SECURITY" as const,checksum:fnv1a64(payload)});
}

export interface ExperimentRoots { readonly id:string; readonly roots:readonly string[]; }
export interface IndependenceAudit {
  readonly independentExperiments:bigint;
  readonly totalExperiments:bigint;
  readonly ratio:Q64;
  readonly sharedRoots:readonly string[];
  readonly independentExperimentIds:readonly string[];
}
export function experimentIndependenceAuditor(experiments:readonly ExperimentRoots[]):IndependenceAudit{
  if(experiments.length===0) throw new ForgeError("at least one experiment is required");
  const normalized=experiments.map((experiment)=>({id:nonEmpty(experiment.id,"experiment id"),roots:canonicalStrings(experiment.roots,"experiment root")})).sort((a,b)=>a.id.localeCompare(b.id));
  const ids=new Set<string>();
  const rootUse=new Map<string,bigint>();
  for(const experiment of normalized){
    if(ids.has(experiment.id)) throw new ForgeError(`duplicate experiment id: ${experiment.id}`);
    ids.add(experiment.id);
    for(const root of experiment.roots) rootUse.set(root,(rootUse.get(root)??0n)+1n);
  }
  const sharedRoots=[...rootUse.entries()].filter(([,count])=>count>1n).map(([root])=>root).sort();

  // Deterministic maximal root-disjoint subset. It is intentionally conservative:
  // no two selected experiments are allowed to share a declared causal/source root.
  const usedRoots=new Set<string>();
  const independentIds:string[]=[];
  for(const experiment of normalized){
    if(experiment.roots.every((root)=>!usedRoots.has(root))){
      independentIds.push(experiment.id);
      for(const root of experiment.roots) usedRoots.add(root);
    }
  }
  const total=countBig(normalized);
  const independent=BigInt(independentIds.length);
  return Object.freeze({
    independentExperiments:independent,
    totalExperiments:total,
    ratio:Q64.ratio(independent,total),
    sharedRoots:Object.freeze(sharedRoots),
    independentExperimentIds:Object.freeze(independentIds)
  });
}

