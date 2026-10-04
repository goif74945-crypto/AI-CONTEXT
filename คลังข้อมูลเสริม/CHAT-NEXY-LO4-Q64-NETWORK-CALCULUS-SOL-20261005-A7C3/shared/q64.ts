/**
 * Checked signed-128-compatible Q64.64 arithmetic.
 * Decision-relevant quantities in this lab are raw bigint Q64.64 values.
 * Intermediate bigint precision is unbounded, but every public result is checked
 * against the signed-128 raw range. Overflow is an error, never wrap/saturate.
 */
export const Q64_FRACTION_BITS = 64n;
export const Q64_ONE = 1n << Q64_FRACTION_BITS;
export const I128_MIN = -(1n << 127n);
export const I128_MAX = (1n << 127n) - 1n;

export class Q64Error extends Error {
  constructor(readonly code: string) {
    super(code);
    this.name = 'Q64Error';
  }
}

export function checkedRaw(value: bigint, code = 'Q64_OVERFLOW'): bigint {
  if (value < I128_MIN || value > I128_MAX) throw new Q64Error(code);
  return value;
}

export function requireNonNegative(value: bigint, code = 'Q64_NEGATIVE'): bigint {
  checkedRaw(value);
  if (value < 0n) throw new Q64Error(code);
  return value;
}

export function requirePositive(value: bigint, code = 'Q64_NON_POSITIVE'): bigint {
  requireNonNegative(value, code);
  if (value === 0n) throw new Q64Error(code);
  return value;
}

export function qInt(value: bigint): bigint {
  return checkedRaw(value * Q64_ONE, 'Q64_INTEGER_OVERFLOW');
}

export function qRatioFloor(numerator: bigint, denominator: bigint): bigint {
  if (denominator <= 0n) throw new Q64Error('Q64_DENOMINATOR_INVALID');
  if (numerator < 0n) throw new Q64Error('Q64_RATIO_NEGATIVE_UNSUPPORTED');
  return checkedRaw((numerator * Q64_ONE) / denominator, 'Q64_RATIO_OVERFLOW');
}

export function qRatioCeil(numerator: bigint, denominator: bigint): bigint {
  if (denominator <= 0n) throw new Q64Error('Q64_DENOMINATOR_INVALID');
  if (numerator < 0n) throw new Q64Error('Q64_RATIO_NEGATIVE_UNSUPPORTED');
  const scaled = numerator * Q64_ONE;
  return checkedRaw(ceilDivNonNegative(scaled, denominator), 'Q64_RATIO_OVERFLOW');
}

export function addQ(a: bigint, b: bigint): bigint {
  return checkedRaw(a + b, 'Q64_ADD_OVERFLOW');
}

export function subQ(a: bigint, b: bigint): bigint {
  return checkedRaw(a - b, 'Q64_SUB_OVERFLOW');
}

export function minQ(a: bigint, b: bigint): bigint { return a < b ? a : b; }
export function maxQ(a: bigint, b: bigint): bigint { return a > b ? a : b; }

export function ceilDivNonNegative(numerator: bigint, denominator: bigint): bigint {
  if (numerator < 0n) throw new Q64Error('Q64_CEIL_NUMERATOR_NEGATIVE');
  if (denominator <= 0n) throw new Q64Error('Q64_CEIL_DENOMINATOR_INVALID');
  return numerator === 0n ? 0n : 1n + ((numerator - 1n) / denominator);
}

/** floor((a*b)/ONE), for non-negative Q64 operands. */
export function mulQFloor(a: bigint, b: bigint): bigint {
  requireNonNegative(a); requireNonNegative(b);
  return checkedRaw((a * b) / Q64_ONE, 'Q64_MUL_OVERFLOW');
}

/** ceil((a*b)/ONE), conservative upper enclosure for non-negative Q64 operands. */
export function mulQCeil(a: bigint, b: bigint): bigint {
  requireNonNegative(a); requireNonNegative(b);
  return checkedRaw(ceilDivNonNegative(a * b, Q64_ONE), 'Q64_MUL_OVERFLOW');
}

/** floor((a/b)*ONE), for non-negative Q64 operands. */
export function divQFloor(a: bigint, b: bigint): bigint {
  requireNonNegative(a); requirePositive(b, 'Q64_DIVIDE_BY_ZERO');
  return checkedRaw((a * Q64_ONE) / b, 'Q64_DIV_OVERFLOW');
}

/** ceil((a/b)*ONE), conservative upper enclosure for non-negative Q64 operands. */
export function divQCeil(a: bigint, b: bigint): bigint {
  requireNonNegative(a); requirePositive(b, 'Q64_DIVIDE_BY_ZERO');
  return checkedRaw(ceilDivNonNegative(a * Q64_ONE, b), 'Q64_DIV_OVERFLOW');
}
