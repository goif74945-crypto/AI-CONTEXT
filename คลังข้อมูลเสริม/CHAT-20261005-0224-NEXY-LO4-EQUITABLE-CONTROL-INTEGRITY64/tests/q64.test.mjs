import test from 'node:test';
import assert from 'node:assert/strict';
import { Q64, Q64_SCALE } from '../src/q64.mjs';

test('Q64 uses exactly 64 fractional bits', () => {
  assert.equal(Q64.parse('1').raw(), Q64_SCALE);
  assert.equal(Q64.parse('0.5').raw(), Q64_SCALE / 2n);
  assert.equal(Q64.parse('0.25').raw(), Q64_SCALE / 4n);
});

test('Q64 rejects binary Number input', () => {
  assert.throws(() => Q64.fromInt(1), TypeError);
  assert.throws(() => Q64.parse(0.1), TypeError);
});

test('Q64 arithmetic identities hold on exact quarters', () => {
  const a = Q64.parse('1.5');
  const b = Q64.parse('0.25');
  assert.equal(a.add(b).toDecimal(4), '1.7500');
  assert.equal(a.sub(b).toDecimal(4), '1.2500');
  assert.equal(a.mul(b).toDecimal(4), '0.3750');
  assert.equal(a.div(b).toDecimal(4), '6.0000');
});

test('Q64 overflow fails closed', () => {
  const max = Q64.fromRaw((1n << 127n) - 1n);
  assert.throws(() => max.add(Q64.fromRaw(1n)), RangeError);
});

test('Q64 division by zero fails closed', () => {
  assert.throws(() => Q64.one().div(Q64.zero()), RangeError);
});

test('Q64 decimal serialization is deterministic', () => {
  const x = Q64.fromRatio(1n, 3n);
  assert.equal(x.toDecimal(12), x.toDecimal(12));
  assert.match(x.toDecimal(12), /^0\.333333333333$/);
});
