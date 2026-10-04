export class Q64Error extends Error {
  public constructor(message: string) {
    super(message);
    this.name = "Q64Error";
  }
}

const SCALE = 1n << 64n;
const MIN_RAW = -(1n << 127n);
const MAX_RAW = (1n << 127n) - 1n;
const TEN = 10n;

function checkedRaw(raw: bigint): bigint {
  if (raw < MIN_RAW || raw > MAX_RAW) {
    throw new Q64Error("Q64.64 signed-128 overflow");
  }
  return raw;
}

function pow10(exp: bigint): bigint {
  if (exp < 0n) throw new Q64Error("negative decimal exponent forbidden");
  let result = 1n;
  let i = 0n;
  while (i < exp) {
    result *= TEN;
    i += 1n;
  }
  return result;
}

function divRoundHalfAway(numerator: bigint, denominator: bigint): bigint {
  if (denominator <= 0n) throw new Q64Error("invalid denominator");
  const negative = numerator < 0n;
  const magnitude = negative ? -numerator : numerator;
  const quotient = magnitude / denominator;
  const remainder = magnitude % denominator;
  const rounded = remainder * 2n >= denominator ? quotient + 1n : quotient;
  return negative ? -rounded : rounded;
}

export class Q64 {
  public static readonly SCALE = SCALE;
  public static readonly MIN_RAW = MIN_RAW;
  public static readonly MAX_RAW = MAX_RAW;
  public static readonly ZERO = new Q64(0n);
  public static readonly ONE = new Q64(SCALE);
  public static readonly MIN = new Q64(MIN_RAW);
  public static readonly MAX = new Q64(MAX_RAW);

  public readonly raw: bigint;

  private constructor(raw: bigint) {
    this.raw = checkedRaw(raw);
    Object.freeze(this);
  }

  public static fromRaw(raw: bigint): Q64 {
    return new Q64(raw);
  }

  public static fromInt(value: bigint): Q64 {
    return new Q64(checkedRaw(value * SCALE));
  }

  public static ratio(numerator: bigint, denominator: bigint): Q64 {
    if (denominator === 0n) throw new Q64Error("division by zero");
    const signNegative = (numerator < 0n) !== (denominator < 0n);
    const n = numerator < 0n ? -numerator : numerator;
    const d = denominator < 0n ? -denominator : denominator;
    // NEXY compatibility: integer fixed-point ratio truncates toward zero.
    const rawMagnitude = (n * SCALE) / d;
    return new Q64(signNegative ? -rawMagnitude : rawMagnitude);
  }

  public static parse(text: string): Q64 {
    if (!/^-?(?:0|[1-9]\d*)(?:\.\d+)?$/.test(text)) {
      throw new Q64Error("invalid canonical decimal");
    }
    const negative = text.startsWith("-");
    const unsigned = negative ? text.slice(1) : text;
    const parts = unsigned.split(".");
    const integerPart = parts[0];
    if (integerPart === undefined) throw new Q64Error("invalid decimal");
    const fractionPart = parts[1] ?? "";
    const denominator = pow10(BigInt(fractionPart.length));
    const integer = BigInt(integerPart);
    const fraction = fractionPart.length === 0 ? 0n : BigInt(fractionPart);
    const numerator = integer * denominator + fraction;
    // Canonical decimal ingestion follows the same truncation direction as
    // authoritative NEXY Q64 ratio construction.
    const rawMagnitude = (numerator * SCALE) / denominator;
    return new Q64(negative ? -rawMagnitude : rawMagnitude);
  }

  public add(other: Q64): Q64 {
    return new Q64(checkedRaw(this.raw + other.raw));
  }

  public sub(other: Q64): Q64 {
    return new Q64(checkedRaw(this.raw - other.raw));
  }

  public neg(): Q64 {
    if (this.raw === MIN_RAW) throw new Q64Error("negation overflow");
    return new Q64(-this.raw);
  }

  public abs(): Q64 {
    return this.raw < 0n ? this.neg() : this;
  }

  public mul(other: Q64): Q64 {
    const product = this.raw * other.raw;
    const raw = product / SCALE;
    return new Q64(checkedRaw(raw));
  }

  public div(other: Q64): Q64 {
    if (other.raw === 0n) throw new Q64Error("division by zero");
    const raw = (this.raw * SCALE) / other.raw;
    return new Q64(checkedRaw(raw));
  }

  public compare(other: Q64): -1 | 0 | 1 {
    if (this.raw < other.raw) return -1;
    if (this.raw > other.raw) return 1;
    return 0;
  }

  public min(other: Q64): Q64 {
    return this.raw <= other.raw ? this : other;
  }

  public max(other: Q64): Q64 {
    return this.raw >= other.raw ? this : other;
  }

  public isBetweenInclusive(minimum: Q64, maximum: Q64): boolean {
    return this.raw >= minimum.raw && this.raw <= maximum.raw;
  }

  public toString(): string {
    if (this.raw === 0n) return "0";
    const negative = this.raw < 0n;
    const magnitude = negative ? -this.raw : this.raw;
    const integer = magnitude / SCALE;
    const remainder = magnitude % SCALE;
    if (remainder === 0n) return `${negative ? "-" : ""}${integer.toString()}`;

    // Render to 18 decimal places using deterministic half-away rounding.
    const decimalScale = pow10(18n);
    let fractional = divRoundHalfAway(remainder * decimalScale, SCALE);
    let carry = 0n;
    if (fractional >= decimalScale) {
      fractional -= decimalScale;
      carry = 1n;
    }
    const whole = integer + carry;
    let fractionText = fractional.toString().padStart(18, "0");
    fractionText = fractionText.replace(/0+$/, "");
    if (fractionText.length === 0) return `${negative ? "-" : ""}${whole.toString()}`;
    return `${negative ? "-" : ""}${whole.toString()}.${fractionText}`;
  }
}

export function q64Unit(value: Q64, label: string): Q64 {
  if (!value.isBetweenInclusive(Q64.ZERO, Q64.ONE)) {
    throw new Q64Error(`${label} must be in [0,1]`);
  }
  return value;
}
