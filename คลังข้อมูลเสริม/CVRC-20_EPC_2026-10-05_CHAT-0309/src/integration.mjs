import { evaluateAll, summarizeDeterministically } from "./gates.mjs";

export function evaluatePromotionCandidate(baseline, candidate, metadata) {
  if (!metadata || metadata.nexyCommit !== baseline.identity.commit) {
    return Object.freeze({
      kind:"CVRC20_EPC_PROPOSAL", release:"DEFER", status:"NOT_VERIFIED",
      reason:"TARGET_COMMIT_MISMATCH", authority:"NONE",
      canPromoteCanon:false, canMutateCoreState:false
    });
  }
  const report=evaluateAll(baseline,candidate);
  const summary=summarizeDeterministically(report);
  return Object.freeze({
    kind:"CVRC20_EPC_PROPOSAL",
    release:report.composite.verdict,
    status:report.composite.status,
    authority:"NONE",
    nextAuthority:"JUDGE_LAW_REVIEW_REQUIRED",
    canPromoteCanon:false,
    canMutateCoreState:false,
    canWriteVault:false,
    baselineCommit:baseline.identity.commit,
    candidateHash:report.composite.candidateHash,
    reportHash:summary.hash,
    report
  });
}
