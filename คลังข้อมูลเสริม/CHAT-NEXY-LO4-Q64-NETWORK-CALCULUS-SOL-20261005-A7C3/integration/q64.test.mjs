import test from 'node:test';
import assert from 'node:assert/strict';
import {
  I128_MAX, Q64_ONE, addQ, divQCeil, mulQCeil, qInt, qRatioCeil, qRatioFloor
} from '../dist/shared/q64.js';

test('Q64.64 directed rounding encloses non-representable thirds', () => {
  const lo=qRatioFloor(1n,3n);
  const hi=qRatioCeil(1n,3n);
  assert.equal(lo < hi,true);
  assert.equal(mulQCeil(hi,qInt(3n)) >= Q64_ONE,true);
  assert.equal(divQCeil(qInt(1n),qInt(3n)),hi);
});

test('signed-128 raw overflow fails closed', () => {
  assert.throws(()=>qInt(1n<<63n),/Q64_INTEGER_OVERFLOW/);
  assert.throws(()=>addQ(I128_MAX,1n),/Q64_ADD_OVERFLOW/);
});
