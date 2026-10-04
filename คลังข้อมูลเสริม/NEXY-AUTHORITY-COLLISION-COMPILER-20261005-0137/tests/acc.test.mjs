import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";
import { canonicalJson, compileAuthorityCollision, compileBatch, fingerprint } from "../dist/acc.js";

const d = (id, value, extra = {}) => ({ id, value, authorityRank: 2, sourceClass: "BUILD_SPEC", scope: "project/NEXY", subject: "x", ...extra });

test("authority dominates specificity", () => {
  const r = compileAuthorityCollision({ target:"project/NEXY/module/auth", subject:"x", directives:[d("user",false,{authorityRank:0,sourceClass:"USER_DIRECTIVE",scope:"project/NEXY/**"}),d("build",true,{scope:"project/NEXY/module/auth"})] });
  assert.equal(r.value,false); assert.equal(r.trace.find(x=>x.id==="build")?.disposition,"SHADOWED");
});
test("equal strongest contradiction freezes without lexical tie-break", () => {
  const r=compileAuthorityCollision({target:"project/NEXY",subject:"x",directives:[d("a",true,{authorityRank:1}),d("b",false,{authorityRank:1})]});
  assert.equal(r.status,"FREEZE_CONFLICT"); assert.deepEqual(r.conflictDirectiveIds,["a","b"]);
});
test("same value at equal precedence is redundancy", () => {
  const r=compileAuthorityCollision({target:"project/NEXY",subject:"x",directives:[d("z",{b:2,a:1},{authorityRank:1}),d("a",{a:1,b:2},{authorityRank:1})]});
  assert.equal(r.status,"RESOLVED"); assert.deepEqual(r.activeDirectiveIds,["a","z"]); assert.equal(r.trace.find(x=>x.id==="z")?.disposition,"REDUNDANT");
});
test("scope specificity resolves after authority", () => {
  const r=compileAuthorityCollision({target:"project/NEXY/module/auth",subject:"x",directives:[d("broad",true,{authorityRank:1,scope:"project/NEXY/**"}),d("exact",false,{authorityRank:1,scope:"project/NEXY/module/auth"})]});
  assert.equal(r.value,false);
});
test("local priority resolves only after equal authority and specificity", () => {
  const r=compileAuthorityCollision({target:"project/NEXY",subject:"x",directives:[d("low",true,{authorityRank:1,localPriority:1}),d("high",false,{authorityRank:1,localPriority:2})]});
  assert.equal(r.value,false);
});
test("conditions gate applicability", () => {
  const r=compileAuthorityCollision({target:"project/NEXY",subject:"x",context:{env:"prod"},directives:[d("dev",true,{conditions:[{key:"env",equals:"dev"}]}),d("prod",false,{conditions:[{key:"env",equals:"prod"}]})]});
  assert.equal(r.value,false); assert.equal(r.trace.find(x=>x.id==="dev")?.disposition,"INAPPLICABLE");
});
test("missing required decision freezes",()=>assert.equal(compileAuthorityCollision({target:"project/NEXY",subject:"x",directives:[],requireDecision:true}).status,"FREEZE_NO_DECISION"));
test("missing optional decision is explicit",()=>assert.equal(compileAuthorityCollision({target:"project/NEXY",subject:"x",directives:[]}).status,"NO_DECISION"));
test("duplicate IDs reject",()=>assert.throws(()=>compileAuthorityCollision({target:"project/NEXY",subject:"x",directives:[d("dup",1),d("dup",1)]}),/Duplicate directive id/));
test("invalid glob rejects",()=>assert.throws(()=>compileAuthorityCollision({target:"project/NEXY/a",subject:"x",directives:[d("bad",1,{scope:"project/**/a"})]}),/final scope segment/));
test("duplicate condition keys reject",()=>assert.throws(()=>compileAuthorityCollision({target:"project/NEXY",subject:"x",context:{env:"prod"},directives:[d("c",1,{conditions:[{key:"env",equals:"prod"},{key:"env",equals:"dev"}]})]}),/duplicate condition key/));
test("NaN rejects",()=>assert.throws(()=>compileAuthorityCollision({target:"project/NEXY",subject:"x",directives:[d("nan",Number.NaN)]}),/NaN or Infinity/));
test("caller mutation cannot change compiled value snapshot",()=>{const value={nested:{allowed:false}};const r=compileAuthorityCollision({target:"project/NEXY",subject:"x",directives:[d("s",value)]});value.nested.allowed=true;assert.deepEqual(r.value,{nested:{allowed:false}});});
test("canonical object key order and -0 are stable",()=>{assert.equal(canonicalJson({b:2,a:1}),canonicalJson({a:1,b:2}));assert.equal(fingerprint(-0),fingerprint(0));});
function shuffle(items,seed){const out=[...items];let s=seed>>>0;const n=()=>{s=(Math.imul(s,1664525)+1013904223)>>>0;return s/0x1_0000_0000;};for(let i=out.length-1;i>0;i--){const j=Math.floor(n()*(i+1));[out[i],out[j]]=[out[j],out[i]];}return out;}
test("500 seeded permutations preserve full result and both fingerprints",()=>{const directives=[d("u",false,{authorityRank:0,sourceClass:"USER_DIRECTIVE",scope:"project/NEXY/**"}),d("p",false,{authorityRank:1,sourceClass:"PROJECT_LAW",scope:"project/NEXY/module/*"}),d("b",true,{scope:"project/NEXY/module/auth"}),d("m",true,{authorityRank:8,sourceClass:"MODEL_INFERENCE",scope:"project/NEXY/module/auth"})];const base=compileAuthorityCollision({target:"project/NEXY/module/auth",subject:"x",directives});for(let seed=1;seed<=500;seed++){const r=compileAuthorityCollision({target:"project/NEXY/module/auth",subject:"x",directives:shuffle(directives,seed)});assert.deepEqual(r,base,`seed=${seed}`);}});
test("batch order and freeze aggregation are deterministic",()=>{const b=compileBatch([{target:"z/t",subject:"x",directives:[],requireDecision:true},{target:"a/t",subject:"x",directives:[d("ok",7,{scope:"a/t"})]}]);assert.equal(b.resolutions[0]?.target,"a/t");assert.equal(b.hasFreeze,true);});
test("protected NEXY.AI fixture resolves false and shadows model suggestion",async()=>{const req=JSON.parse(await readFile(new URL("../fixtures/example-request.json",import.meta.url),"utf8"));const r=compileAuthorityCollision(req);assert.equal(r.status,"RESOLVED");assert.equal(r.value,false);assert.deepEqual(r.activeDirectiveIds,["user-protect-nexy"]);assert.equal(r.trace.find(x=>x.id==="model-convenience")?.disposition,"SHADOWED");});
