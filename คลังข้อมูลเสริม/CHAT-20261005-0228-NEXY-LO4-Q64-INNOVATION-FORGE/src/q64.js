export const FRACTION_BITS = 64n;
export const SCALE = 1n << FRACTION_BITS;
export const MIN_RAW = -(1n << 127n);
export const MAX_RAW = (1n << 127n) - 1n;

export class Q64Error extends Error {
  constructor(code, message) {
    super(message);
    this.name = 'Q64Error';
    this.code = code;
  }
}

function assertRaw(raw) {
  if (typeof raw !== 'bigint') throw new Q64Error('TYPE', 'raw must be bigint');
  if (raw < MIN_RAW || raw > MAX_RAW) throw new Q64Error('OVERFLOW', 'Q64.64 raw value outside signed 128-bit range');
  return raw;
}

function divRoundEvenUnsigned(n, d) {
  if (d <= 0n || n < 0n) throw new Q64Error('INTERNAL', 'unsigned division invariant violated');
  const q = n / d;
  const r = n % d;
  const twice = r << 1n;
  if (twice < d) return q;
  if (twice > d) return q + 1n;
  return (q & 1n) === 0n ? q : q + 1n;
}

export function divRoundEven(n, d) {
  if (typeof n !== 'bigint' || typeof d !== 'bigint') throw new Q64Error('TYPE', 'division requires bigint');
  if (d === 0n) throw new Q64Error('DIV_ZERO', 'division by zero');
  const negative = (n < 0n) !== (d < 0n);
  const an = n < 0n ? -n : n;
  const ad = d < 0n ? -d : d;
  const q = divRoundEvenUnsigned(an, ad);
  return negative ? -q : q;
}

function pow10(n) {
  let out = 1n;
  for (let i = 0; i < n; i += 1) out *= 10n;
  return out;
}

export class Q64 {
  #raw;

  constructor(raw) {
    this.#raw = assertRaw(raw);
    Object.freeze(this);
  }

  static fromRaw(raw) { return new Q64(raw); }
  static zero() { return new Q64(0n); }
  static one() { return new Q64(SCALE); }

  static fromInt(value) {
    const v = typeof value === 'bigint' ? value : BigInt(value);
    return new Q64(assertRaw(v * SCALE));
  }

  static parse(text) {
    if (text instanceof Q64) return text;
    if (typeof text === 'bigint') return Q64.fromInt(text);
    if (typeof text !== 'string') throw new Q64Error('TYPE', 'Q64.parse accepts a decimal string, bigint, or Q64');
    const m = /^([+-]?)(\d+)(?:\.(\d+))?$/.exec(text.trim());
    if (!m) throw new Q64Error('FORMAT', 'invalid decimal string');
    const sign = m[1] === '-' ? -1n : 1n;
    const intPart = BigInt(m[2]);
    const frac = m[3] ?? '';
    const den = pow10(frac.length);
    const num = intPart * den + (frac.length ? BigInt(frac) : 0n);
    const raw = divRoundEven(sign * num * SCALE, den);
    return new Q64(assertRaw(raw));
  }

  get raw() { return this.#raw; }
  isZero() { return this.#raw === 0n; }
  isNegative() { return this.#raw < 0n; }
  eq(other) { return this.#raw === Q64.parse(other).raw; }
  lt(other) { return this.#raw < Q64.parse(other).raw; }
  lte(other) { return this.#raw <= Q64.parse(other).raw; }
  gt(other) { return this.#raw > Q64.parse(other).raw; }
  gte(other) { return this.#raw >= Q64.parse(other).raw; }

  add(other) { return new Q64(assertRaw(this.#raw + Q64.parse(other).raw)); }
  sub(other) { return new Q64(assertRaw(this.#raw - Q64.parse(other).raw)); }

  neg() {
    if (this.#raw === MIN_RAW) throw new Q64Error('OVERFLOW', 'cannot negate minimum Q64.64 value');
    return new Q64(-this.#raw);
  }

  abs() { return this.#raw < 0n ? this.neg() : this; }

  mul(other) {
    const rhs = Q64.parse(other).raw;
    return new Q64(assertRaw(divRoundEven(this.#raw * rhs, SCALE)));
  }

  div(other) {
    const rhs = Q64.parse(other).raw;
    if (rhs === 0n) throw new Q64Error('DIV_ZERO', 'division by zero');
    return new Q64(assertRaw(divRoundEven(this.#raw * SCALE, rhs)));
  }

  clamp(min, max) {
    const lo = Q64.parse(min);
    const hi = Q64.parse(max);
    if (lo.gt(hi)) throw new Q64Error('RANGE', 'min > max');
    if (this.lt(lo)) return lo;
    if (this.gt(hi)) return hi;
    return this;
  }

  min(other) { const rhs = Q64.parse(other); return this.lte(rhs) ? this : rhs; }
  max(other) { const rhs = Q64.parse(other); return this.gte(rhs) ? this : rhs; }

  floorInt() {
    if (this.#raw >= 0n) return this.#raw / SCALE;
    const q = this.#raw / SCALE;
    return this.#raw % SCALE === 0n ? q : q - 1n;
  }

  toFixed(digits = 18) {
    if (!Number.isInteger(digits) || digits < 0 || digits > 30) throw new Q64Error('FORMAT', 'digits must be integer 0..30');
    const negative = this.#raw < 0n;
    const a = negative ? -this.#raw : this.#raw;
    const intPart = a / SCALE;
    if (digits === 0) return `${negative ? '-' : ''}${intPart}`;
    const fracRaw = a % SCALE;
    const scale10 = pow10(digits);
    let frac = divRoundEvenUnsigned(fracRaw * scale10, SCALE);
    let carry = 0n;
    if (frac === scale10) { carry = 1n; frac = 0n; }
    const body = `${intPart + carry}.${frac.toString().padStart(digits, '0')}`;
    return `${negative ? '-' : ''}${body}`;
  }

  toJSON() { return { q64_64_raw: this.#raw.toString(), decimal: this.toFixed(18) }; }
  toString() { return this.toFixed(18); }
}

export const QZERO = Q64.zero();
export const QONE = Q64.one();

export function q(value) { return Q64.parse(value); }
export function qInt(value) { return Q64.fromInt(typeof value === 'bigint' ? value : BigInt(value)); }

export function qRatio(numerator, denominator) {
  const n = typeof numerator === 'bigint' ? numerator : BigInt(numerator);
  const d = typeof denominator === 'bigint' ? denominator : BigInt(denominator);
  if (d === 0n) throw new Q64Error('DIV_ZERO', 'ratio denominator is zero');
  return Q64.fromRaw(assertRaw(divRoundEven(n * SCALE, d)));
}

export function requireUnitInterval(value, name = 'value') {
  const v = q(value);
  if (v.lt(QZERO) || v.gt(QONE)) throw new Q64Error('RANGE', `${name} must be within [0,1]`);
  return v;
}

export function sumQ(values) {
  let total = QZERO;
  for (const v of values) total = total.add(v);
  return total;
}

export function meanQ(values) {
  if (!Array.isArray(values) || values.length === 0) throw new Q64Error('EMPTY', 'mean requires at least one value');
  return sumQ(values).div(qInt(BigInt(values.length)));
}

export function weightedMean(pairs) {
  if (!Array.isArray(pairs) || pairs.length === 0) throw new Q64Error('EMPTY', 'weighted mean requires values');
  let numerator = QZERO;
  let weightSum = QZERO;
  for (const { value, weight } of pairs) {
    const v = q(value);
    const w = q(weight);
    if (w.lt(QZERO)) throw new Q64Error('RANGE', 'weight must be non-negative');
    numerator = numerator.add(v.mul(w));
    weightSum = weightSum.add(w);
  }
  if (weightSum.isZero()) throw new Q64Error('DIV_ZERO', 'weight sum is zero');
  return numerator.div(weightSum);
}
