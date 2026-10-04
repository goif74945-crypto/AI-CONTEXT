const test = require('node:test');
const assert = require('node:assert/strict');
const { Q64, Q64Error } = require('../dist/index.js');

test('Q64 parses exact decimals and performs checked arithmetic', () => {
  const a = Q64.parse('1.5');
  const b = Q64.parse('2.25');
  assert.equal(a.add(b).toString(), '3.75');
  assert.equal(a.mul(b).toString(), '3.375');
  assert.equal(b.div(a).toString(), '1.5');
  assert.equal(Q64.ratio(1n, 4n).toString(), '0.25');
});

test('Q64 fails closed on invalid arithmetic', () => {
  assert.throws(() => Q64.MAX.add(Q64.fromRaw(1n)), Q64Error);
  assert.throws(() => Q64.ONE.div(Q64.ZERO), Q64Error);
  assert.throws(() => Q64.parse('NaN'), Q64Error);
  assert.throws(() => Q64.parse('1e3'), Q64Error);
});

test('Q64 ratio truncates toward zero for NEXY fixed-point compatibility', () => {
  const scale=1n<<64n;
  assert.equal(Q64.ratio(1n,3n).raw, scale/3n);
  assert.equal(Q64.ratio(-1n,3n).raw, -(scale/3n));
  assert.equal(Q64.parse('0.1').raw, scale/10n);
});
