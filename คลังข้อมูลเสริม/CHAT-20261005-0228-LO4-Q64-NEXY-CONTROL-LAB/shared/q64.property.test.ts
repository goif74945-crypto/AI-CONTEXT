import test from "node:test";import assert from "node:assert/strict";import{Q64}from"./q64.ts";
function* seq(n:number){let x=0x12345678n;for(let i=0;i<n;i++){x=(1103515245n*x+12345n)&0x7fffffffn;yield x;}}
test("50000 deterministic arithmetic invariants",()=>{const vals=[...seq(50000)];for(let i=0;i<vals.length-1;i++){const a=Q64.fromRatio(vals[i]%100000n,1000n),b=Q64.fromRatio((vals[i+1]%99999n)+1n,1000n);assert.equal(a.add(b).sub(b).raw,a.raw);const m=a.mul(Q64.one());assert.equal(m.raw,a.raw);const d=a.div(Q64.one());assert.equal(d.raw,a.raw);assert.equal(a.abs().isNegative(),false);}});
