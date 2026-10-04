export class Q64 {
  static readonly FRACTION_BITS = 64n;
  static readonly SCALE = 1n << Q64.FRACTION_BITS;
  static readonly MIN_RAW = -(1n << 127n);
  static readonly MAX_RAW = (1n << 127n) - 1n;
  readonly raw: bigint;

  private constructor(raw: bigint) {
    Q64.assertRange(raw);
    this.raw = raw;
  }

  private static assertRange(raw: bigint): void {
    if (raw < Q64.MIN_RAW || raw > Q64.MAX_RAW) {
      throw new RangeError(`Q64.64 overflow: ${raw}`);
    }
  }

  static fromRaw(raw: bigint): Q64 { return new Q64(raw); }
  static zero(): Q64 { return Q64.fromRaw(0n); }
  static one(): Q64 { return Q64.fromRaw(Q64.SCALE); }
  static fromInt(value: bigint): Q64 { return Q64.fromRaw(value * Q64.SCALE); }

  static fromRatio(numerator: bigint, denominator: bigint): Q64 {
    if (denominator === 0n) throw new RangeError('division by zero');
    return Q64.fromRaw(Q64.divRoundNearestEven(numerator * Q64.SCALE, denominator));
  }

  static parse(decimal: string): Q64 {
    const m = decimal.trim().match(/^([+-]?)(\d+)(?:\.(\d+))?$/);
    if (!m) throw new TypeError(`invalid Q64 decimal: ${decimal}`);
    const sign = m[1] === '-' ? -1n : 1n;
    const whole = BigInt(m[2]);
    const fracText = m[3] ?? '';
    const fracDen = fracText.length ? 10n ** BigInt(fracText.length) : 1n;
    const fracNum = fracText.length ? BigInt(fracText) : 0n;
    const totalNum = sign * (whole * fracDen + fracNum);
    return Q64.fromRatio(totalNum, fracDen);
  }

  private static divRoundNearestEven(n: bigint, d: bigint): bigint {
    if (d === 0n) throw new RangeError('division by zero');
    let nn = n;
    let dd = d;
    let sign = 1n;
    if (nn < 0n) { sign = -sign; nn = -nn; }
    if (dd < 0n) { sign = -sign; dd = -dd; }
    const q = nn / dd;
    const r = nn % dd;
    const twice = r * 2n;
    let rounded = q;
    if (twice > dd || (twice === dd && (q & 1n) === 1n)) rounded = q + 1n;
    return sign * rounded;
  }

  add(other: Q64): Q64 { return Q64.fromRaw(this.raw + other.raw); }
  sub(other: Q64): Q64 { return Q64.fromRaw(this.raw - other.raw); }
  neg(): Q64 { return Q64.fromRaw(-this.raw); }
  abs(): Q64 { return this.raw < 0n ? this.neg() : this; }
  mul(other: Q64): Q64 {
    return Q64.fromRaw(Q64.divRoundNearestEven(this.raw * other.raw, Q64.SCALE));
  }
  div(other: Q64): Q64 {
    if (other.raw === 0n) throw new RangeError('division by zero');
    return Q64.fromRaw(Q64.divRoundNearestEven(this.raw * Q64.SCALE, other.raw));
  }
  min(other: Q64): Q64 { return this.raw <= other.raw ? this : other; }
  max(other: Q64): Q64 { return this.raw >= other.raw ? this : other; }
  clamp(lo: Q64, hi: Q64): Q64 {
    if (lo.raw > hi.raw) throw new RangeError('invalid clamp bounds');
    return this.max(lo).min(hi);
  }
  compare(other: Q64): -1 | 0 | 1 { return this.raw < other.raw ? -1 : this.raw > other.raw ? 1 : 0; }
  eq(other: Q64): boolean { return this.raw === other.raw; }
  isNegative(): boolean { return this.raw < 0n; }
  isZero(): boolean { return this.raw === 0n; }

  toDecimal(places = 18): string {
    if (!Number.isInteger(places) || places < 0 || places > 30) throw new RangeError('places must be 0..30');
    const sign = this.raw < 0n ? '-' : '';
    const absRaw = this.raw < 0n ? -this.raw : this.raw;
    const whole = absRaw / Q64.SCALE;
    if (places === 0) { const rounded = Q64.divRoundNearestEven(absRaw, Q64.SCALE); return `${sign}${rounded}`; }
    const fracRaw = absRaw % Q64.SCALE;
    const scale10 = 10n ** BigInt(places);
    const frac = Q64.divRoundNearestEven(fracRaw * scale10, Q64.SCALE);
    if (frac === scale10) return `${sign}${whole + 1n}.${'0'.repeat(places)}`;
    return `${sign}${whole}.${frac.toString().padStart(places, '0')}`;
  }

  static sum(values: readonly Q64[]): Q64 {
    return values.reduce((acc, v) => acc.add(v), Q64.zero());
  }
  static weightedMean(values: readonly Q64[], weights: readonly Q64[]): Q64 {
    if (values.length === 0 || values.length !== weights.length) throw new RangeError('values/weights mismatch');
    let weighted = Q64.zero();
    let total = Q64.zero();
    for (let i = 0; i < values.length; i++) {
      if (weights[i].isNegative()) throw new RangeError('negative weight');
      weighted = weighted.add(values[i].mul(weights[i]));
      total = total.add(weights[i]);
    }
    if (total.isZero()) throw new RangeError('zero total weight');
    return weighted.div(total);
  }
}

export const ZERO = Q64.zero();
export const ONE = Q64.one();
export const HALF = Q64.fromRatio(1n, 2n);
export function q(v: string | bigint): Q64 {
  if (typeof v === 'string') return Q64.parse(v);
  return Q64.fromInt(v);
}
export function unit(v: Q64): Q64 { if (v.raw < ZERO.raw || v.raw > ONE.raw) throw new RangeError('expected unit interval [0,1]'); return v; }
export function complement(v: Q64): Q64 { return ONE.sub(unit(v)); }
export function requireUniqueIds<T>(items: readonly T[], id: (item: T) => string): void {
  const seen = new Set<string>();
  for (const item of items) { const key = id(item); if (seen.has(key)) throw new Error(`DUPLICATE_ID:${key}`); seen.add(key); }
}
export function deterministicSort<T>(items: readonly T[], score: (item: T) => Q64, id: (item: T) => string): T[] {
  return [...items].sort((a,b) => {
    const s = score(b).compare(score(a));
    if (s !== 0) return s;
    return id(a).localeCompare(id(b));
  });
}
