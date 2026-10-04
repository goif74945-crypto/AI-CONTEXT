/** Checked signed i128-domain Q64.64 arithmetic for SCARM advisory metrics. */
export type Q64 = bigint;
export const Q64_SHIFT = 64n;
export const Q64_ONE: Q64 = 1n << Q64_SHIFT;
export const Q64_ZERO: Q64 = 0n;
export const I128_MIN = -(1n << 127n);
export const I128_MAX = (1n << 127n) - 1n;

function checked(value: bigint): Q64 {
  if (value < I128_MIN || value > I128_MAX) {
    throw new RangeError("SCARM_Q64_OVERFLOW");
  }
  return value;
}

export function q64FromInt(value: bigint): Q64 {
  return checked(value << Q64_SHIFT);
}

export function q64FromRatio(numerator: bigint, denominator: bigint): Q64 {
  if (denominator === 0n) throw new RangeError("SCARM_Q64_DIVIDE_BY_ZERO");
  return checked((numerator << Q64_SHIFT) / denominator);
}

export function q64Add(a: Q64, b: Q64): Q64 { return checked(a + b); }
export function q64Sub(a: Q64, b: Q64): Q64 { return checked(a - b); }
export function q64Mul(a: Q64, b: Q64): Q64 { return checked((a * b) >> Q64_SHIFT); }
export function q64Div(a: Q64, b: Q64): Q64 {
  if (b === 0n) throw new RangeError("SCARM_Q64_DIVIDE_BY_ZERO");
  return checked((a << Q64_SHIFT) / b);
}

export function q64Metric(value: Q64): Q64 {
  if (value < Q64_ZERO || value > Q64_ONE) throw new RangeError("SCARM_Q64_METRIC_RANGE");
  return value;
}

export function q64Min(a: Q64, b: Q64): Q64 { return a <= b ? a : b; }
export function q64Max(a: Q64, b: Q64): Q64 { return a >= b ? a : b; }

export function q64Square(a: Q64): Q64 {
  return q64Mul(a, a);
}

export function q64ToDecimalString(value: Q64, digits = 8): string {
  if (!Number.isSafeInteger(digits) || digits < 0 || digits > 32) throw new RangeError("DIGITS_RANGE");
  const negative = value < 0n;
  const magnitude = negative ? -value : value;
  const integer = magnitude >> Q64_SHIFT;
  let fraction = magnitude & (Q64_ONE - 1n);
  let out = "";
  for (let i = 0; i < digits; i += 1) {
    fraction *= 10n;
    out += (fraction >> Q64_SHIFT).toString();
    fraction &= Q64_ONE - 1n;
  }
  return `${negative ? "-" : ""}${integer.toString()}${digits === 0 ? "" : "." + out}`;
}
