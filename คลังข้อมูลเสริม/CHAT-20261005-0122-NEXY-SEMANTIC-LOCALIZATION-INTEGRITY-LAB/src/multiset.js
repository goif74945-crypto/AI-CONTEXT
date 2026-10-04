export function toMultiset(values) {
  const map = new Map();
  for (const value of values) {
    map.set(value, (map.get(value) ?? 0) + 1);
  }
  return map;
}

export function diffMultiset(expectedValues, actualValues) {
  const expected = toMultiset(expectedValues);
  const actual = toMultiset(actualValues);
  const missing = [];
  const extra = [];

  const keys = [...new Set([...expected.keys(), ...actual.keys()])].sort();
  for (const key of keys) {
    const expectedCount = expected.get(key) ?? 0;
    const actualCount = actual.get(key) ?? 0;
    for (let i = actualCount; i < expectedCount; i += 1) missing.push(key);
    for (let i = expectedCount; i < actualCount; i += 1) extra.push(key);
  }

  return { equal: missing.length === 0 && extra.length === 0, missing, extra };
}
