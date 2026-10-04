const FRACTION_BITS = 64n;
export const Q64_SCALE = 1n << FRACTION_BITS;
const RAW_MIN = -(1n << 127n);
const RAW_MAX = (1n << 127n) - 1n;

function checkRaw(raw) {
  if (typeof raw !== 'bigint') throw new TypeError('Q64 raw value must be bigint');
  if (raw < RAW_MIN || raw > RAW_MAX) throw new RangeError('Q64.64 signed 128-bit overflow');
  return raw;
}

function divTruncZero(n, d) {
  if (d === 0n) throw new RangeError('division by zero');
  const negative = (n < 0n) !== (d < 0n);
  const q = (n < 0n ? -n : n) / (d < 0n ? -d : d);
  return negative ? -q : q;
}

function pow10(n) {
  let r = 1n;
  for (let i = 0; i < n; i++) r *= 10n;
  return r;
}

export class Q64 {
  #raw;

  constructor(raw) {
    this.#raw = checkRaw(raw);
    Object.freeze(this);
  }

  static zero() { return new Q64(0n); }
  static one() { return new Q64(Q64_SCALE); }
  static fromRaw(raw) { return new Q64(raw); }

  static fromInt(value) {
    if (typeof value !== 'bigint') throw new TypeError('Q64.fromInt requires bigint');
    return new Q64(checkRaw(value * Q64_SCALE));
  }

  static fromRatio(numerator, denominator) {
    if (typeof numerator !== 'bigint' || typeof denominator !== 'bigint') {
      throw new TypeError('Q64.fromRatio requires bigint operands');
    }
    return new Q64(checkRaw(divTruncZero(numerator * Q64_SCALE, denominator)));
  }

  static parse(text) {
    if (typeof text !== 'string') throw new TypeError('Q64.parse requires a decimal string');
    const m = /^([+-]?)(\d+)(?:\.(\d+))?$/.exec(text);
    if (!m) throw new TypeError(`invalid Q64 decimal: ${text}`);
    const sign = m[1] === '-' ? -1n : 1n;
    const whole = BigInt(m[2]);
    const fracText = m[3] ?? '';
    const denominator = pow10(fracText.length);
    const frac = fracText.length === 0 ? 0n : BigInt(fracText);
    const numerator = sign * (whole * denominator + frac);
    return Q64.fromRatio(numerator, denominator);
  }

  raw() { return this.#raw; }

  add(other) { return new Q64(checkRaw(this.#raw + ensureQ64(other).#raw)); }
  sub(other) { return new Q64(checkRaw(this.#raw - ensureQ64(other).#raw)); }
  neg() { return new Q64(checkRaw(-this.#raw)); }
  abs() { return this.#raw < 0n ? this.neg() : this; }

  mul(other) {
    const rhs = ensureQ64(other).#raw;
    return new Q64(checkRaw(divTruncZero(this.#raw * rhs, Q64_SCALE)));
  }

  div(other) {
    const rhs = ensureQ64(other).#raw;
    return new Q64(checkRaw(divTruncZero(this.#raw * Q64_SCALE, rhs)));
  }

  min(other) { const rhs = ensureQ64(other); return this.#raw <= rhs.#raw ? this : rhs; }
  max(other) { const rhs = ensureQ64(other); return this.#raw >= rhs.#raw ? this : rhs; }

  cmp(other) {
    const rhs = ensureQ64(other).#raw;
    return this.#raw < rhs ? -1 : this.#raw > rhs ? 1 : 0;
  }

  eq(other) { return this.cmp(other) === 0; }
  lt(other) { return this.cmp(other) < 0; }
  lte(other) { return this.cmp(other) <= 0; }
  gt(other) { return this.cmp(other) > 0; }
  gte(other) { return this.cmp(other) >= 0; }

  clamp(minimum, maximum) {
    const lo = ensureQ64(minimum);
    const hi = ensureQ64(maximum);
    if (lo.gt(hi)) throw new RangeError('invalid clamp interval');
    if (this.lt(lo)) return lo;
    if (this.gt(hi)) return hi;
    return this;
  }

  toDecimal(places = 18) {
    if (!Number.isInteger(places) || places < 0 || places > 30) throw new RangeError('places must be integer 0..30');
    const sign = this.#raw < 0n ? '-' : '';
    const mag = this.#raw < 0n ? -this.#raw : this.#raw;
    const whole = mag / Q64_SCALE;
    if (places === 0) return `${sign}${whole}`;
    const scale10 = pow10(places);
    const frac = (mag % Q64_SCALE) * scale10 / Q64_SCALE;
    return `${sign}${whole}.${frac.toString().padStart(places, '0')}`;
  }

  toJSON() { return this.toDecimal(18); }
}

export function ensureQ64(value) {
  if (!(value instanceof Q64)) throw new TypeError('expected Q64');
  return value;
}

export function unitInterval(value, label = 'value') {
  const q = ensureQ64(value);
  if (q.lt(Q64.zero()) || q.gt(Q64.one())) throw new RangeError(`${label} must be within [0,1]`);
  return q;
}

export function sumQ64(values) {
  let total = Q64.zero();
  for (const value of values) total = total.add(ensureQ64(value));
  return total;
}
