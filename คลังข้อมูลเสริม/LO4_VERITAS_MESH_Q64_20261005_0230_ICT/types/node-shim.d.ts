declare module "node:crypto" {
  interface Hash {
    update(data: string): Hash;
    digest(encoding: "hex"): string;
  }
  export function createHash(algorithm: "sha256" | string): Hash;
}

declare module "node:perf_hooks" {
  export const performance: { now(): number };
}

declare module "node:test" {
  interface TestContext {}
  type TestFunction = (t: TestContext) => void | Promise<void>;
  export default function test(name: string, fn: TestFunction): void;
}

declare module "node:assert/strict" {
  interface AssertStrict {
    equal(actual: unknown, expected: unknown, message?: string): void;
    deepEqual(actual: unknown, expected: unknown, message?: string): void;
    ok(value: unknown, message?: string): asserts value;
    throws(fn: () => unknown, expected?: RegExp | Function, message?: string): void;
    match(actual: string, expected: RegExp, message?: string): void;
  }
  const assert: AssertStrict;
  export default assert;
}
