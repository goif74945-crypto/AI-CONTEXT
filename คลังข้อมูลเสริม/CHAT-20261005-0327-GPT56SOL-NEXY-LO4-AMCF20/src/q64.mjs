export const Q64_SCALE = 1n << 64n;
export const Q64_MIN_RAW = -(1n << 127n);
export const Q64_MAX_RAW = (1n << 127n) - 1n;

export class Q64Error extends Error {
  constructor(code) { super(code); this.name = "Q64Error"; this.code = code; }
}

export function checkedRaw(raw) {
  if (typeof raw !== "bigint") throw new Q64Error("Q64_TYPE");
  if (raw < Q64_MIN_RAW || raw > Q64_MAX_RAW) throw new Q64Error("Q64_OVERFLOW");
  return raw;
}

function abs(v) { return v < 0n ? -v : v; }

function roundNearestTiesAway(numerator, denominator) {
  if (denominator === 0n) throw new Q64Error("Q64_DIV_ZERO");
  if (denominator < 0n) { numerator = -numerator; denominator = -denominator; }
  if (numerator === 0n) return 0n;
  const negative = numerator < 0n;
  const a = abs(numerator);
  const q = a / denominator;
  const r = a % denominator;
  const rounded = (r * 2n >= denominator) ? q + 1n : q;
  if (rounded === 0n) throw new Q64Error("Q64_UNDERFLOW");
  return negative ? -rounded : rounded;
}

export function qFromInt(value) {
  if (typeof value !== "bigint") throw new Q64Error("Q64_INTEGER_BIGINT_REQUIRED");
  return checkedRaw(value * Q64_SCALE);
}

export function qFromRatio(numerator, denominator) {
  if (typeof numerator !== "bigint" || typeof denominator !== "bigint") throw new Q64Error("Q64_RATIO_BIGINT_REQUIRED");
  return checkedRaw(roundNearestTiesAway(numerator * Q64_SCALE, denominator));
}

export function qAdd(a,b) { return checkedRaw(checkedRaw(a) + checkedRaw(b)); }
export function qSub(a,b) { return checkedRaw(checkedRaw(a) - checkedRaw(b)); }
export function qMul(a,b) {
  checkedRaw(a); checkedRaw(b);
  return checkedRaw(roundNearestTiesAway(a * b, Q64_SCALE));
}
export function qDiv(a,b) {
  checkedRaw(a); checkedRaw(b);
  if (b === 0n) throw new Q64Error("Q64_DIV_ZERO");
  return checkedRaw(roundNearestTiesAway(a * Q64_SCALE, b));
}
export function qCmp(a,b) { checkedRaw(a); checkedRaw(b); return a < b ? -1 : a > b ? 1 : 0; }
export function qMin(a,b) { return qCmp(a,b) <= 0 ? a : b; }
export function qMax(a,b) { return qCmp(a,b) >= 0 ? a : b; }
export function qAbs(a) { checkedRaw(a); if (a === Q64_MIN_RAW) throw new Q64Error("Q64_OVERFLOW"); return a < 0n ? -a : a; }
export function qSerialize(a) { return checkedRaw(a).toString(10); }
export function qParse(text) {
  if (typeof text !== "string" || !/^-?(0|[1-9][0-9]*)$/.test(text)) throw new Q64Error("Q64_SERIALIZATION_INVALID");
  return checkedRaw(BigInt(text));
}
export function qUnitRatio(pass, total) {
  if (typeof pass !== "bigint" || typeof total !== "bigint" || total <= 0n || pass < 0n || pass > total) throw new Q64Error("Q64_UNIT_RATIO_INVALID");
  return qFromRatio(pass,total);
}
export const Q_ZERO = 0n;
export const Q_ONE = Q64_SCALE;
