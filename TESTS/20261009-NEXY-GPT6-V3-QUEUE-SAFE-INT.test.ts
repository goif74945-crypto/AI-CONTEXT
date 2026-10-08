import { describe, it, expect } from "vitest";
import { isFailedDispatchRetryPolicy, isFailedDispatchRetryAllowed, FAILED_RETRY_DISABLED } from "../../packages/queue/retry-policy.js";
const policy = (maxAttempts: number) => ({ enabled: true, maxAttempts, safeErrorCodes: ["QUEUE_UNAVAILABLE"] });
const row = (attempts: number, lastError = "QUEUE_UNAVAILABLE") => ({ status: "FAILED", attempts, lastError });
describe("FAILED retry safe integer boundary (EX-V3)", () => {
  it("rejects policy caps larger than MAX_SAFE_INTEGER", () => {
    expect(isFailedDispatchRetryPolicy(policy(Number.MAX_SAFE_INTEGER + 1))).toBe(false);
  });
  it("rejects unsafe persisted attempt counters", () => {
    expect(isFailedDispatchRetryAllowed(row(Number.MAX_SAFE_INTEGER + 1), policy(Number.MAX_SAFE_INTEGER))).toBe(false);
  });
  it("accepts bounded caps and refuses after cap", () => {
    expect(isFailedDispatchRetryPolicy(policy(2))).toBe(true);
    expect(isFailedDispatchRetryAllowed(row(1), policy(2))).toBe(true);
    expect(isFailedDispatchRetryAllowed(row(2), policy(2))).toBe(false);
  });
  it("refuses schema/security failures and stays disabled by default", () => {
    expect(isFailedDispatchRetryAllowed(row(0, "SCHEMA_VIOLATION"), policy(2))).toBe(false);
    expect(isFailedDispatchRetryAllowed(row(0, "SECURITY_BREACH_DETECTED"), policy(2))).toBe(false);
    expect(isFailedDispatchRetryAllowed(row(0), FAILED_RETRY_DISABLED)).toBe(false);
  });
});
