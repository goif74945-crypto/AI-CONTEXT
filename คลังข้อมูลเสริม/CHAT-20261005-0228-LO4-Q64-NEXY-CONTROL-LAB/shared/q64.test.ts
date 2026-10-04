import test from "node:test";
import assert from "node:assert/strict";
import { Q64 } from "./q64.ts";
test("parse and decimal",()=>{assert.equal(Q64.parse("1.5").toDecimal(1),"1.5");assert.equal(Q64.parse("-2.25").toDecimal(2),"-2.25")});
test("mul div",()=>{const a=Q64.parse("1.5"),b=Q64.parse("2");assert.equal(a.mul(b).toDecimal(1),"3.0");assert.equal(a.div(b).toDecimal(2),"0.75")});
test("overflow",()=>assert.throws(()=>Q64.fromRaw(Q64.MAX_RAW+1n),RangeError));
test("division by zero",()=>assert.throws(()=>Q64.one().div(Q64.zero()),RangeError));
test("nearest even ties",()=>{const halfRaw=Q64.SCALE/2n;assert.equal(Q64.fromRatio(1n,2n).raw,halfRaw)});
