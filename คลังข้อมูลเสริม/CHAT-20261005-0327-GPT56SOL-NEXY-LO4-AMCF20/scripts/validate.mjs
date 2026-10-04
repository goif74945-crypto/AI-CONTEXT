import { readFile,readdir,stat } from "node:fs/promises";
import { join,resolve,relative } from "node:path";
import { AMCF_SYSTEMS } from "../src/fabric.mjs";
const root=resolve(new URL("..",import.meta.url).pathname);
const required=["README.md","DESIGN.md","ARCHITECTURE.md","THREAT_MODEL.md","INTEGRATION_CONTRACT.md","TEST_PLAN.md","TEST_EVIDENCE.md","FINAL_AUDIT.md","00_EXECUTION_MEMORY.md","src/q64.mjs","src/canonical.mjs","src/fabric.mjs","tests/amcf20.test.mjs","tests/determinism-stress.mjs"];
const failures=[];
for(const f of required){try{if(!(await stat(join(root,f))).isFile())failures.push(`NOT_FILE:${f}`)}catch{failures.push(`MISSING:${f}`)}}
if(AMCF_SYSTEMS.length!==20||new Set(AMCF_SYSTEMS).size!==20)failures.push("SYSTEM_REGISTRY_NOT_20_DISTINCT");
async function walk(d){let out=[];for(const n of await readdir(d)){if(n==="node_modules")continue;const p=join(d,n),s=await stat(p);out=s.isDirectory()?out.concat(await walk(p)):out.concat(p)}return out}
for(const p of await walk(root)){if(!/\.(mjs|md|json)$/.test(p))continue;const t=await readFile(p,"utf8");for(const banned of ["TO"+"DO","FIX"+"ME","PLACE"+"HOLDER"]){if(t.toUpperCase().includes(banned))failures.push(`INCOMPLETE_MARKER:${relative(root,p)}:${banned}`)}if(/\bsk-(?:proj-)?[A-Za-z0-9]{20,}\b/.test(t))failures.push(`POSSIBLE_SECRET:${relative(root,p)}`)}
console.log(JSON.stringify({status:failures.length?"FAIL":"PASS",systems:AMCF_SYSTEMS.length,required_files:required.length,failures},null,2));if(failures.length)process.exitCode=1;
