declare module "node:crypto" {
  interface Hash {
    update(data: string | Uint8Array): Hash;
    digest(encoding: "hex"): string;
  }
  export function createHash(algorithm: string): Hash;
}

declare module "node:test" {
  type TestFunction = (name: string, fn: () => void) => void;
  const test: TestFunction;
  export default test;
}

declare module "node:assert/strict" {
  interface AssertStrict {
    equal(actual: unknown, expected: unknown, message?: string): void;
    deepEqual(actual: unknown, expected: unknown, message?: string): void;
    throws(fn: () => unknown, expected?: RegExp, message?: string): void;
    ok(value: unknown, message?: string): asserts value;
  }
  const assert: AssertStrict;
  export default assert;
}
