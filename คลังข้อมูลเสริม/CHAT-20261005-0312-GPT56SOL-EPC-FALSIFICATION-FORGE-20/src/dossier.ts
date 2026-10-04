import type { AdvisoryAuthority } from "./core";
import { ForgeError, canonicalStrings, nonEmpty } from "./core";
export interface ExperimentResultInput { readonly id:string; readonly status:"PASS"|"FALSIFIED"|"NOT_VERIFIED"|"BLOCKED"; readonly evidence:readonly string[]; }
export interface PromotionExperimentDossier {
  readonly candidateId:string;
  readonly authority:AdvisoryAuthority;
  readonly autoPromote:false;
  readonly readiness:"BLOCKED_BY_FALSIFICATION"|"INSUFFICIENT_EVIDENCE"|"READY_FOR_EXTERNAL_REVIEW";
  readonly experiments:readonly {readonly id:string;readonly status:ExperimentResultInput["status"];readonly evidence:readonly string[]}[];
}
export function promotionExperimentDossierCompiler(candidateId:string,experiments:readonly ExperimentResultInput[]):PromotionExperimentDossier{
  const candidate=nonEmpty(candidateId,"candidate id");
  if(experiments.length===0) throw new ForgeError("at least one experiment result is required");
  const normalized=experiments.map((experiment)=>Object.freeze({id:nonEmpty(experiment.id,"experiment id"),status:experiment.status,evidence:Object.freeze(canonicalStrings(experiment.evidence,"experiment evidence",experiment.status!=="PASS"&&experiment.status!=="FALSIFIED"))})).sort((a,b)=>a.id.localeCompare(b.id));
  const seen=new Set<string>();
  for(const experiment of normalized){ if(seen.has(experiment.id)) throw new ForgeError(`duplicate experiment id: ${experiment.id}`); seen.add(experiment.id); }
  let falsified=false; let insufficient=false;
  for(const experiment of normalized){
    if(experiment.status==="FALSIFIED") falsified=true;
    if(experiment.status==="NOT_VERIFIED"||experiment.status==="BLOCKED"||experiment.evidence.length===0) insufficient=true;
  }
  const readiness=falsified?"BLOCKED_BY_FALSIFICATION" as const:insufficient?"INSUFFICIENT_EVIDENCE" as const:"READY_FOR_EXTERNAL_REVIEW" as const;
  return Object.freeze({candidateId:candidate,authority:"ADVISORY_ONLY" as const,autoPromote:false as const,readiness,experiments:Object.freeze(normalized)});
}

export function assertNoAuthorityEscalation(dossier: PromotionExperimentDossier): void {
  if (dossier.authority !== "ADVISORY_ONLY" || dossier.autoPromote !== false) {
    throw new ForgeError("authority escalation detected");
  }
}

