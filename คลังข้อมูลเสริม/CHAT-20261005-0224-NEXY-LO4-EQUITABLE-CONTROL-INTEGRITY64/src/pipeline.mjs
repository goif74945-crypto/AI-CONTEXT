import { auditFreezeBurden } from './freezeburden.mjs';
import { auditVerificationBurden } from './verifytax.mjs';
import { auditAvoidableFreeze } from './avoidablefreeze.mjs';
import { auditRecoveryEquity } from './recoveryequity.mjs';
import { auditThresholdFragility } from './thresholdfragility.mjs';

export function auditEquitableControlPack(input) {
  const results = [
    auditFreezeBurden({ cohorts: input.cohorts, policy: input.policies.freeze }),
    auditVerificationBurden({ cohorts: input.cohorts, policy: input.policies.verification }),
    auditAvoidableFreeze({ cohorts: input.cohorts, policy: input.policies.avoidable }),
    auditRecoveryEquity({ cohorts: input.cohorts, policy: input.policies.recovery }),
    auditThresholdFragility({ cohorts: input.cohorts, policy: input.policies.threshold }),
  ];
  const frozen = results.filter(r => r.status === 'FREEZE_FAIRNESS_REVIEW').map(r => r.system).sort();
  return {
    suite: 'EQUITABLE_CONTROL_INTEGRITY64',
    status: frozen.length === 0 ? 'READY_FOR_HUMAN_REVIEW' : 'FREEZE_FAIRNESS_REVIEW',
    frozenSystems: frozen,
    results,
    authorityNotice: 'Audit results are advisory Lo4 evidence only; they do not infer cohort membership, alter Canon, or make release decisions.',
  };
}
