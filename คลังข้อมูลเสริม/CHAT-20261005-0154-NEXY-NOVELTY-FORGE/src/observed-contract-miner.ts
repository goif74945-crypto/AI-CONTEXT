import { canonicalId, stableLexicographic } from "./canonical.js";
import { ContractError, VerificationStatus } from "./types.js";

export interface ObservedContract {
  requirementId: string;
  behavior: string;
  evidenceClass: "E0" | "E1" | "E2" | "E3" | "E4" | "E5" | "E6" | "E7";
  sourcePath: string;
  line: number;
  authority: "OBSERVED_NON_AUTHORITY";
}

export interface ContractMiningReport {
  observations: ObservedContract[];
  duplicateConflicts: string[];
  expectedRequirementStatus: Record<string, VerificationStatus>;
  malformedMarkers: { sourcePath: string; line: number; raw: string; reason: string }[];
}

const MARKER = "@nexy-observed-contract";

interface MarkerPayload {
  requirementId?: unknown;
  behavior?: unknown;
  evidenceClass?: unknown;
}

function validateEvidenceClass(value: unknown): ObservedContract["evidenceClass"] {
  const allowed = new Set(["E0", "E1", "E2", "E3", "E4", "E5", "E6", "E7"]);
  if (typeof value !== "string" || !allowed.has(value)) {
    throw new ContractError("evidenceClass must be one of E0..E7");
  }
  return value as ObservedContract["evidenceClass"];
}

export function mineObservedContracts(
  files: Readonly<Record<string, string>>,
  expectedRequirementIds: readonly string[],
): ContractMiningReport {
  const observations: ObservedContract[] = [];
  const malformedMarkers: ContractMiningReport["malformedMarkers"] = [];

  for (const sourcePath of stableLexicographic(Object.keys(files))) {
    const lines = files[sourcePath]!.split(/\r?\n/);
    for (let index = 0; index < lines.length; index += 1) {
      const line = lines[index]!;
      const markerIndex = line.indexOf(MARKER);
      if (markerIndex < 0) continue;
      const raw = line.slice(markerIndex + MARKER.length).trim();
      try {
        const payload = JSON.parse(raw) as MarkerPayload;
        if (typeof payload.requirementId !== "string") throw new ContractError("requirementId must be a string");
        if (typeof payload.behavior !== "string" || payload.behavior.trim().length === 0) throw new ContractError("behavior must be a non-empty string");
        observations.push({
          requirementId: canonicalId(payload.requirementId, "requirementId"),
          behavior: payload.behavior.trim(),
          evidenceClass: validateEvidenceClass(payload.evidenceClass),
          sourcePath,
          line: index + 1,
          authority: "OBSERVED_NON_AUTHORITY",
        });
      } catch (error) {
        malformedMarkers.push({
          sourcePath,
          line: index + 1,
          raw,
          reason: error instanceof Error ? error.message : "unknown parse error",
        });
      }
    }
  }

  observations.sort((a, b) =>
    a.requirementId.localeCompare(b.requirementId, "en") ||
    a.sourcePath.localeCompare(b.sourcePath, "en") ||
    a.line - b.line,
  );

  const byRequirement = new Map<string, ObservedContract[]>();
  for (const observation of observations) {
    const list = byRequirement.get(observation.requirementId) ?? [];
    list.push(observation);
    byRequirement.set(observation.requirementId, list);
  }

  const duplicateConflicts: string[] = [];
  for (const [requirementId, list] of byRequirement.entries()) {
    const behaviors = new Set(list.map((item) => `${item.evidenceClass}:${item.behavior}`));
    if (behaviors.size > 1) duplicateConflicts.push(requirementId);
  }

  const expectedRequirementStatus: Record<string, VerificationStatus> = {};
  const normalizedExpected = expectedRequirementIds.map((id, index) => canonicalId(id, `expectedRequirementIds[${index}]`));
  for (const requirementId of stableLexicographic([...new Set(normalizedExpected)])) {
    if (duplicateConflicts.includes(requirementId)) {
      expectedRequirementStatus[requirementId] = "CONFLICT";
    } else if (byRequirement.has(requirementId)) {
      expectedRequirementStatus[requirementId] = "NOT_VERIFIED";
    } else {
      expectedRequirementStatus[requirementId] = "UNKNOWN";
    }
  }

  return {
    observations,
    duplicateConflicts: stableLexicographic(duplicateConflicts),
    expectedRequirementStatus,
    malformedMarkers,
  };
}
