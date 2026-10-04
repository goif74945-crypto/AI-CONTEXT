import { ContractError } from "./types.js";

export function canonicalToken(value: string, field: string): string {
  const normalized = value.trim().toLocaleLowerCase("en-US").replace(/\s+/g, " ");
  if (!normalized) {
    throw new ContractError(`${field} must not be empty`);
  }
  return normalized;
}

export function canonicalId(value: string, field: string): string {
  const normalized = value.trim();
  if (!/^[A-Za-z0-9._:-]+$/.test(normalized)) {
    throw new ContractError(`${field} contains unsupported characters: ${value}`);
  }
  return normalized;
}

export function stableLexicographic(values: readonly string[]): string[] {
  return [...values].sort((a, b) => a.localeCompare(b, "en"));
}

export function assertFiniteNumber(value: number, field: string): void {
  if (!Number.isFinite(value)) {
    throw new ContractError(`${field} must be finite`);
  }
}

export function assertUnitInterval(value: number, field: string): void {
  assertFiniteNumber(value, field);
  if (value < 0 || value > 1) {
    throw new ContractError(`${field} must be between 0 and 1 inclusive`);
  }
}

export function round12(value: number): number {
  return Number(value.toFixed(12));
}
