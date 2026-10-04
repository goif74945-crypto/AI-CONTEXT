export class ForgeError extends Error {
  public constructor(message: string) {
    super(message);
    this.name = "ForgeError";
  }
}

export const MECHANISM_IDS = Object.freeze([
  "RHC", "FG", "MFP", "CNEP", "BCPP", "FIEP", "AKEP", "DES", "OTP", "EIYE",
  "SES", "CDM", "ESM", "DPG", "REP", "CVDE", "OPCC", "RCB", "EIA", "PEDC"
] as const);

export type MechanismId = (typeof MECHANISM_IDS)[number];
export type AdvisoryAuthority = "ADVISORY_ONLY";

export function nonEmpty(value: string, label: string): string {
  const trimmed = value.trim();
  if (trimmed.length === 0) throw new ForgeError(`${label} must be non-empty`);
  return trimmed;
}

export function canonicalStrings(values: readonly string[], label: string, allowEmpty = false): string[] {
  const set = new Set<string>();
  for (const value of values) set.add(nonEmpty(value, label));
  const result = [...set].sort();
  if (!allowEmpty && result.length === 0) throw new ForgeError(`${label} must contain at least one value`);
  return result;
}

export function countBig<T>(items: readonly T[]): bigint {
  let count = 0n;
  for (const _item of items) count += 1n;
  return count;
}

export function sixDigit(value: bigint): string {
  if (value <= 0n || value > 999999n) throw new ForgeError("probe ordinal out of range");
  return value.toString().padStart(6, "0");
}
