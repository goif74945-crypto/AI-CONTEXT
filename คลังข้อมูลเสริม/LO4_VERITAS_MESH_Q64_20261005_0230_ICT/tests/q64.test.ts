import test from "node:test";
import assert from "node:assert/strict";
import { I128_MAX, I128_MIN, Q64, Q64_SCALE, UnitQ64 } from "../src/q64.ts";

test("Q64 constants and raw ABI are exact", () => {
  assert.equal(Q64.ONE.raw, 1n << 64n);
  assert.equal(Q64.ZERO.raw, 0n);
  assert.equal(Q64.MIN.raw, I128_MIN);
  assert.equal(Q64.MAX.raw, I128_MAX);
});

test("decimal parsing never uses IEEE-754 and is deterministic", () => {
  assert.equal(Q64.fromDecimal("0.5").raw, 1n << 63n);
  assert.equal(Q64.fromDecimal("1.25").raw, Q64_SCALE + (Q64_SCALE >> 2n));
  assert.equal(Q64.fromDecimal("-2.5").toDecimal(4), "-2.5000");
  assert.throws(() => Q64.fromDecimal("1e-3"), SyntaxError);
});

test("multiplication and division use exact bigint intermediates", () => {
  const a = Q64.fromFraction(3n, 4n);
  const b = Q64.fromFraction(1n, 2n);
  assert.equal(a.mul(b).raw, Q64.fromFraction(3n, 8n).raw);
  assert.equal(a.div(Q64.fromFraction(3n, 2n)).raw, Q64.fromFraction(1n, 2n).raw);
});

test("saturation is deterministic at signed i128 boundaries", () => {
  assert.equal(Q64.MAX.add(Q64.ONE).raw, I128_MAX);
  assert.equal(Q64.MIN.sub(Q64.ONE).raw, I128_MIN);
  assert.equal(Q64.saturatingFromRaw(I128_MAX + 999n).raw, I128_MAX);
  assert.equal(Q64.saturatingFromRaw(I128_MIN - 999n).raw, I128_MIN);
});

test("division by zero fails closed", () => {
  assert.throws(() => Q64.ONE.div(Q64.ZERO), /division by zero/);
  assert.throws(() => Q64.fromFraction(1n, 0n), /division by zero/);
});

test("UnitQ64 preserves [0,1] invariant", () => {
  assert.throws(() => UnitQ64.fromRaw(-1n), RangeError);
  assert.throws(() => UnitQ64.fromRaw(Q64_SCALE + 1n), RangeError);
  assert.equal(UnitQ64.fromDecimal("0.25").complement().toDecimal(4), "0.7500");
  assert.equal(UnitQ64.fromDecimal("0.5").mul(UnitQ64.fromDecimal("0.5")).toDecimal(4), "0.2500");
});

test("weighted average rejects invalid weight and is exact for binary fractions", () => {
  const score = UnitQ64.weightedAverage([
    { value: UnitQ64.ONE, weight: 1n },
    { value: UnitQ64.ZERO, weight: 1n }
  ]);
  assert.equal(score.raw, Q64_SCALE >> 1n);
  assert.throws(() => UnitQ64.weightedAverage([{ value: UnitQ64.ONE, weight: 0n }]), /weights/);
});
