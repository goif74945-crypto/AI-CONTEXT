/**
 * Deterministic signed Q64.64 arithmetic for Lo4 experiments.
 *
 * Compatibility contract:
 * - raw value is a signed 128-bit integer represented as bigint
 * - mathematical value = raw / 2^64
 * - no IEEE-754 input path exists
 * - arithmetic uses arbitrary precision intermediates and deterministic
 *   saturation to signed i128 at operation boundaries
 */
export const Q64_SCALE = 1n << 64n;
export const I128_MIN = -(1n << 127n);
export const I128_MAX = (1n << 127n) - 1n;

function clampI128(value: bigint): bigint {
  if (value < I128_MIN) return I128_MIN;
  if (value > I128_MAX) return I128_MAX;
  return value;
}

function assertI128(value: bigint): void {
  if (value < I128_MIN || value > I128_MAX) {
    throw new RangeError("raw Q64.64 value is outside signed i128 range");
  }
}

export class Q64 {
  readonly raw: bigint;

  private constructor(raw: bigint) {
    assertI128(raw);
    this.raw = raw;
  }

  static readonly ZERO = new Q64(0n);
  static readonly ONE = new Q64(Q64_SCALE);
  static readonly MIN = new Q64(I128_MIN);
  static readonly MAX = new Q64(I128_MAX);

  static fromRaw(raw: bigint): Q64 {
    return new Q64(raw);
  }

  static saturatingFromRaw(raw: bigint): Q64 {
    return new Q64(clampI128(raw));
  }

  static fromInt(value: bigint | string): Q64 {
    const n = typeof value === "bigint" ? value : BigInt(value);
    return Q64.saturatingFromRaw(n * Q64_SCALE);
  }

  static fromFraction(numerator: bigint, denominator: bigint): Q64 {
    if (denominator === 0n) throw new RangeError("Q64.64 division by zero");
    return Q64.saturatingFromRaw((numerator * Q64_SCALE) / denominator);
  }

  static fromDecimal(text: string): Q64 {
    const match = /^([+-]?)(\d+)(?:\.(\d{1,64}))?$/.exec(text.trim());
    if (!match) throw new SyntaxError("invalid deterministic decimal literal");
    const sign = match[1] === "-" ? -1n : 1n;
    const whole = BigInt(match[2]!);
    const frac = match[3] ?? "";
    if (frac.length === 0) return Q64.fromInt(sign * whole);

    const denominator = 10n ** BigInt(frac.length);
    const numerator = whole * denominator + BigInt(frac);
    return Q64.fromFraction(sign * numerator, denominator);
  }

  add(other: Q64): Q64 {
    return Q64.saturatingFromRaw(this.raw + other.raw);
  }

  sub(other: Q64): Q64 {
    return Q64.saturatingFromRaw(this.raw - other.raw);
  }

  neg(): Q64 {
    if (this.raw === I128_MIN) return Q64.MAX;
    return Q64.fromRaw(-this.raw);
  }

  mul(other: Q64): Q64 {
    // BigInt gives an exact 256-bit-or-wider intermediate. Division truncates
    // toward zero, matching deterministic signed integer semantics.
    return Q64.saturatingFromRaw((this.raw * other.raw) / Q64_SCALE);
  }

  div(other: Q64): Q64 {
    if (other.raw === 0n) throw new RangeError("Q64.64 division by zero");
    return Q64.saturatingFromRaw((this.raw * Q64_SCALE) / other.raw);
  }

  min(other: Q64): Q64 {
    return this.raw <= other.raw ? this : other;
  }

  max(other: Q64): Q64 {
    return this.raw >= other.raw ? this : other;
  }

  compare(other: Q64): -1 | 0 | 1 {
    return this.raw < other.raw ? -1 : this.raw > other.raw ? 1 : 0;
  }

  toRawString(): string {
    return this.raw.toString(10);
  }

  toDecimal(places = 12): string {
    if (!Number.isInteger(places) || places < 0 || places > 30) {
      throw new RangeError("places must be an integer in [0, 30]");
    }
    const sign = this.raw < 0n ? "-" : "";
    const abs = this.raw < 0n ? -this.raw : this.raw;
    const whole = abs / Q64_SCALE;
    if (places === 0) return `${sign}${whole}`;
    const fractionalRaw = abs % Q64_SCALE;
    const scale10 = 10n ** BigInt(places);
    const digits = (fractionalRaw * scale10) / Q64_SCALE;
    return `${sign}${whole}.${digits.toString().padStart(places, "0")}`;
  }
}

export class UnitQ64 {
  readonly q: Q64;

  private constructor(q: Q64) {
    if (q.raw < 0n || q.raw > Q64_SCALE) {
      throw new RangeError("UnitQ64 must be in [0, 1]");
    }
    this.q = q;
  }

  static readonly ZERO = new UnitQ64(Q64.ZERO);
  static readonly ONE = new UnitQ64(Q64.ONE);
  static readonly HALF = new UnitQ64(Q64.fromFraction(1n, 2n));

  static fromRaw(raw: bigint): UnitQ64 {
    return new UnitQ64(Q64.fromRaw(raw));
  }

  static fromFraction(numerator: bigint, denominator: bigint): UnitQ64 {
    return new UnitQ64(Q64.fromFraction(numerator, denominator));
  }

  static fromDecimal(text: string): UnitQ64 {
    return new UnitQ64(Q64.fromDecimal(text));
  }

  static clamp(q: Q64): UnitQ64 {
    if (q.raw <= 0n) return UnitQ64.ZERO;
    if (q.raw >= Q64_SCALE) return UnitQ64.ONE;
    return new UnitQ64(q);
  }

  get raw(): bigint {
    return this.q.raw;
  }

  complement(): UnitQ64 {
    return UnitQ64.fromRaw(Q64_SCALE - this.raw);
  }

  mul(other: UnitQ64): UnitQ64 {
    return UnitQ64.clamp(this.q.mul(other.q));
  }

  min(other: UnitQ64): UnitQ64 {
    return this.raw <= other.raw ? this : other;
  }

  max(other: UnitQ64): UnitQ64 {
    return this.raw >= other.raw ? this : other;
  }

  static weightedAverage(terms: readonly { value: UnitQ64; weight: bigint }[]): UnitQ64 {
    if (terms.length === 0) throw new RangeError("weightedAverage requires at least one term");
    let weighted = 0n;
    let totalWeight = 0n;
    for (const { value, weight } of terms) {
      if (weight <= 0n) throw new RangeError("weights must be positive integers");
      weighted += value.raw * weight;
      totalWeight += weight;
    }
    return UnitQ64.fromRaw(weighted / totalWeight);
  }

  static product(values: readonly UnitQ64[]): UnitQ64 {
    if (values.length === 0) return UnitQ64.ONE;
    let acc = UnitQ64.ONE;
    for (const value of values) acc = acc.mul(value);
    return acc;
  }

  toRawString(): string {
    return this.raw.toString(10);
  }

  toDecimal(places = 6): string {
    return this.q.toDecimal(places);
  }
}
