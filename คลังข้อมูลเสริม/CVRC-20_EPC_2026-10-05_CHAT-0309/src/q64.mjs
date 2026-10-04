export const Q64_SHIFT = 64n;
export const Q64_ONE = 1n << Q64_SHIFT;
export const Q64_ZERO = 0n;
export const I128_MIN = -(1n << 127n);
export const I128_MAX = (1n << 127n) - 1n;

export class Q64RangeError extends RangeError {
  constructor(operation, value) {
    super(`Q64.64 i128 range violation in ${operation}: ${value}`);
    this.name = "Q64RangeError";
    this.operation = operation;
    this.value = value;
  }
}
export class Q64DivisionByZeroError extends RangeError {
  constructor() {
    super("Q64.64 division by zero");
    this.name = "Q64DivisionByZeroError";
  }
}
export function q64Check(value, operation = "check") {
  if (typeof value !== "bigint") throw new TypeError("Q64.64 value must be bigint");
  if (value < I128_MIN || value > I128_MAX) throw new Q64RangeError(operation, value);
  return value;
}
export function q64FromInt(value) {
  if (typeof value !== "bigint") throw new TypeError("integer must be bigint");
  return q64Check(value << Q64_SHIFT, "fromInt");
}
export function q64FromRatio(numerator, denominator) {
  if (typeof numerator !== "bigint" || typeof denominator !== "bigint") throw new TypeError("ratio operands must be bigint");
  if (denominator === 0n) throw new Q64DivisionByZeroError();
  const neg = (numerator < 0n) !== (denominator < 0n);
  const n = numerator < 0n ? -numerator : numerator;
  const d = denominator < 0n ? -denominator : denominator;
  const mag = (n << Q64_SHIFT) / d;
  return q64Check(neg ? -mag : mag, "fromRatio");
}
export function q64Add(a, b) {
  return q64Check(q64Check(a, "add:a") + q64Check(b, "add:b"), "add");
}
export function q64Sub(a, b) {
  return q64Check(q64Check(a, "sub:a") - q64Check(b, "sub:b"), "sub");
}
export function q64Mul(a, b) {
  q64Check(a, "mul:a"); q64Check(b, "mul:b");
  const neg = (a < 0n) !== (b < 0n);
  const aa = a < 0n ? -a : a;
  const bb = b < 0n ? -b : b;
  const mag = (aa * bb) >> Q64_SHIFT;
  return q64Check(neg ? -mag : mag, "mul");
}
export function q64Div(a, b) {
  q64Check(a, "div:a"); q64Check(b, "div:b");
  if (b === 0n) throw new Q64DivisionByZeroError();
  const neg = (a < 0n) !== (b < 0n);
  const aa = a < 0n ? -a : a;
  const bb = b < 0n ? -b : b;
  const mag = (aa << Q64_SHIFT) / bb;
  return q64Check(neg ? -mag : mag, "div");
}
export function q64Unit(value) {
  q64Check(value, "unit");
  if (value < 0n || value > Q64_ONE) throw new Q64RangeError("unit", value);
  return value;
}
export function q64ComplementUnit(value) {
  return q64Sub(Q64_ONE, q64Unit(value));
}
export function q64RatioOfCounts(numerator, denominator) {
  if (!Number.isSafeInteger(numerator) || !Number.isSafeInteger(denominator)) throw new TypeError("count ratio requires safe integers");
  if (numerator < 0 || denominator <= 0 || numerator > denominator) throw new RangeError("invalid count ratio");
  return q64FromRatio(BigInt(numerator), BigInt(denominator));
}
export function q64ToExactString(raw) {
  q64Check(raw, "toExactString");
  const neg = raw < 0n;
  const mag = neg ? -raw : raw;
  const whole = mag >> Q64_SHIFT;
  const frac = mag & (Q64_ONE - 1n);
  return `${neg ? "-" : ""}${whole}+${frac}/2^64`;
}
