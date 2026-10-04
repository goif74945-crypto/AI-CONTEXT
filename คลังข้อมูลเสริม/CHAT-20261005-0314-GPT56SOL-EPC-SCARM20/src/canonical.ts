/** Locale-independent exact UTF-16 code-unit ordering. No normalization is performed. */
export function compareCanonicalText(left: string, right: string): number {
  if (left === right) return 0;
  return left < right ? -1 : 1;
}

export function sortedUnique(values: readonly string[]): readonly string[] {
  return Object.freeze([...new Set(values)].sort(compareCanonicalText));
}

export function sameStringSet(left: readonly string[], right: readonly string[]): boolean {
  const a = sortedUnique(left);
  const b = sortedUnique(right);
  return a.length === b.length && a.every((value, index) => value === b[index]);
}

export function setDifference(left: readonly string[], right: readonly string[]): readonly string[] {
  const rightSet = new Set(right);
  return sortedUnique(left.filter((value) => !rightSet.has(value)));
}

export function canonicalJoin(values: readonly string[]): string {
  return sortedUnique(values).map((value) => `${value.length}:${value}`).join("|");
}
