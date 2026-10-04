export class FreezeError extends Error {
  constructor(message, code = 'FREEZE') {
    super(message);
    this.name = 'FreezeError';
    this.code = code;
  }
}

export const Q64_SCALE = 1n << 64n;
export const Q64_ONE = Q64_SCALE;
export const Q64_ZERO = 0n;
export const Q64_MIN_RAW = -(1n << 127n);
export const Q64_MAX_RAW = (1n << 127n) - 1n;
const TEN = 10n;
const FIVE_POW_64 = 5n ** 64n;

export function assertQ64(raw, label = 'q64') {
  if (typeof raw !== 'bigint') {
    throw new FreezeError(`${label} must be Q64 raw BigInt`, 'TYPE');
  }
  if (raw < Q64_MIN_RAW || raw > Q64_MAX_RAW) {
    throw new FreezeError(`${label} overflows signed Q64.64 raw range`, 'OVERFLOW');
  }
  return raw;
}

export function checkedRaw(raw, label = 'q64') {
  return assertQ64(raw, label);
}

export function parseQ64(text) {
  if (typeof text !== 'string') {
    throw new FreezeError('Q64 decimal input must be a string', 'TYPE');
  }
  if (!/^[+-]?(?:0|[1-9]\d*)(?:\.\d+)?$/.test(text)) {
    throw new FreezeError(`invalid Q64 decimal: ${text}`, 'PARSE');
  }
  let s = text;
  let sign = 1n;
  if (s[0] === '-') { sign = -1n; s = s.slice(1); }
  else if (s[0] === '+') { s = s.slice(1); }
  const [wholeText, fracText = ''] = s.split('.');
  const whole = BigInt(wholeText);
  let raw = whole * Q64_SCALE;
  if (fracText.length) {
    const fracNum = BigInt(fracText);
    const fracDen = TEN ** BigInt(fracText.length);
    raw += (fracNum * Q64_SCALE) / fracDen;
  }
  return assertQ64(sign * raw, 'parsed Q64');
}

export function quantizeDecimal(text) {
  if (typeof text !== 'string' || !/^[+-]?(?:0|[1-9]\d*)(?:\.\d+)?$/.test(text)) {
    throw new FreezeError('invalid decimal text', 'PARSE');
  }
  let s = text;
  let sign = 1n;
  if (s[0] === '-') { sign = -1n; s = s.slice(1); }
  else if (s[0] === '+') { s = s.slice(1); }
  const [wholeText, fracText = ''] = s.split('.');
  const fracDen = fracText.length ? TEN ** BigInt(fracText.length) : 1n;
  const absoluteNumerator = BigInt(wholeText) * fracDen + (fracText.length ? BigInt(fracText) : 0n);
  const scaledNumerator = absoluteNumerator * Q64_SCALE;
  const rawAbs = scaledNumerator / fracDen;
  const remainder = scaledNumerator % fracDen;
  const raw = assertQ64(sign * rawAbs, 'quantized Q64');
  return Object.freeze({
    raw,
    exact: remainder === 0n,
    remainderNumerator: remainder,
    remainderDenominator: fracDen,
    errorUpperRaw: remainder === 0n ? 0n : 1n
  });
}

export function formatQ64(raw) {
  assertQ64(raw);
  if (raw === 0n) return '0';
  const sign = raw < 0n ? '-' : '';
  const abs = raw < 0n ? -raw : raw;
  const whole = abs / Q64_SCALE;
  const fracRaw = abs % Q64_SCALE;
  if (fracRaw === 0n) return `${sign}${whole}`;
  const fracDigits = (fracRaw * FIVE_POW_64).toString().padStart(64, '0').replace(/0+$/, '');
  return `${sign}${whole}.${fracDigits}`;
}

export function addQ(a, b) {
  assertQ64(a, 'a'); assertQ64(b, 'b');
  return assertQ64(a + b, 'sum');
}

export function subQ(a, b) {
  assertQ64(a, 'a'); assertQ64(b, 'b');
  return assertQ64(a - b, 'difference');
}

export function negQ(a) {
  assertQ64(a, 'a');
  return assertQ64(-a, 'negation');
}

export function absQ(a) {
  assertQ64(a, 'a');
  if (a === Q64_MIN_RAW) throw new FreezeError('absolute value overflow', 'OVERFLOW');
  return a < 0n ? -a : a;
}

export function mulQ(a, b) {
  assertQ64(a, 'a'); assertQ64(b, 'b');
  return assertQ64((a * b) / Q64_SCALE, 'product');
}

export function divQ(a, b) {
  assertQ64(a, 'a'); assertQ64(b, 'b');
  if (b === 0n) throw new FreezeError('division by zero', 'DIV_ZERO');
  return assertQ64((a * Q64_SCALE) / b, 'quotient');
}

export function cmpQ(a, b) {
  assertQ64(a, 'a'); assertQ64(b, 'b');
  return a < b ? -1 : a > b ? 1 : 0;
}

export function minQ(a, b) { return cmpQ(a, b) <= 0 ? a : b; }
export function maxQ(a, b) { return cmpQ(a, b) >= 0 ? a : b; }

export function midpointQ(a, b) {
  assertQ64(a, 'a'); assertQ64(b, 'b');
  return assertQ64((a + b) / 2n, 'midpoint');
}

export function sumQ(values) {
  let total = 0n;
  for (const value of values) total = addQ(total, value);
  return total;
}

export function ratioFloorRaw(numeratorRaw, denominatorRaw) {
  assertQ64(numeratorRaw, 'numerator');
  assertQ64(denominatorRaw, 'denominator');
  if (denominatorRaw <= 0n) throw new FreezeError('denominator must be positive', 'DOMAIN');
  if (numeratorRaw < 0n) throw new FreezeError('numerator must be non-negative', 'DOMAIN');
  return numeratorRaw / denominatorRaw;
}

export function isQ64(raw) {
  return typeof raw === 'bigint' && raw >= Q64_MIN_RAW && raw <= Q64_MAX_RAW;
}
