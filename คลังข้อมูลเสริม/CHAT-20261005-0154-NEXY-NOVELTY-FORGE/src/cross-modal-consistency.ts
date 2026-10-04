import { canonicalId, canonicalToken, stableLexicographic } from "./canonical.js";
import { ContractError, Decision, Diagnostic } from "./types.js";

export type Modality = "text" | "code" | "ui" | "api" | "test" | "config" | "runtime";

export interface ArtifactAssertion {
  artifactId: string;
  modality: Modality;
  subject: string;
  predicate: string;
  object: string;
  polarity?: "affirm" | "deny";
  critical?: boolean;
}

export interface CrossModalPolicy {
  freezeOnCriticalConflict: boolean;
  minimumModalitiesForCrossCheck: number;
}

export interface AssertionConflict {
  key: string;
  critical: boolean;
  artifactIds: string[];
  modalities: Modality[];
  variants: string[];
}

export interface CrossModalReport {
  decision: Decision;
  comparedKeys: number;
  crossCheckedKeys: number;
  conflicts: AssertionConflict[];
  diagnostics: Diagnostic[];
}

interface NormalizedAssertion {
  artifactId: string;
  modality: Modality;
  key: string;
  variant: string;
  critical: boolean;
}

export function evaluateCrossModalConsistency(
  assertions: readonly ArtifactAssertion[],
  policy: CrossModalPolicy,
): CrossModalReport {
  if (!Number.isInteger(policy.minimumModalitiesForCrossCheck) || policy.minimumModalitiesForCrossCheck < 2) {
    throw new ContractError("minimumModalitiesForCrossCheck must be an integer >= 2");
  }

  const normalized: NormalizedAssertion[] = assertions.map((item, index) => {
    const subject = canonicalToken(item.subject, `assertions[${index}].subject`);
    const predicate = canonicalToken(item.predicate, `assertions[${index}].predicate`);
    const object = canonicalToken(item.object, `assertions[${index}].object`);
    const polarity = item.polarity ?? "affirm";
    return {
      artifactId: canonicalId(item.artifactId, `assertions[${index}].artifactId`),
      modality: item.modality,
      key: `${subject}::${predicate}`,
      variant: `${polarity}:${object}`,
      critical: item.critical ?? false,
    };
  });

  const groups = new Map<string, NormalizedAssertion[]>();
  for (const assertion of normalized) {
    const group = groups.get(assertion.key) ?? [];
    group.push(assertion);
    groups.set(assertion.key, group);
  }

  const conflicts: AssertionConflict[] = [];
  let crossCheckedKeys = 0;

  for (const key of stableLexicographic([...groups.keys()])) {
    const group = groups.get(key)!;
    const modalities = stableLexicographic([...new Set(group.map((item) => item.modality))]) as Modality[];
    if (modalities.length >= policy.minimumModalitiesForCrossCheck) {
      crossCheckedKeys += 1;
    }

    const variants = stableLexicographic([...new Set(group.map((item) => item.variant))]);
    if (variants.length > 1) {
      conflicts.push({
        key,
        critical: group.some((item) => item.critical),
        artifactIds: stableLexicographic([...new Set(group.map((item) => item.artifactId))]),
        modalities,
        variants,
      });
    }
  }

  const criticalConflict = conflicts.some((conflict) => conflict.critical);
  const decision: Decision = conflicts.length === 0
    ? "PASS"
    : criticalConflict && policy.freezeOnCriticalConflict
      ? "FREEZE"
      : "REVIEW";

  const diagnostics: Diagnostic[] = [];
  if (crossCheckedKeys === 0 && assertions.length > 0) {
    diagnostics.push({
      code: "NO_CROSS_MODAL_COVERAGE",
      message: "Assertions exist, but no semantic key is represented by enough modalities to count as a cross-check.",
    });
  }

  return {
    decision,
    comparedKeys: groups.size,
    crossCheckedKeys,
    conflicts,
    diagnostics,
  };
}
