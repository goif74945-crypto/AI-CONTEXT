import { performance } from "node:perf_hooks";
import { NEXY_BASELINE, cloneBaseline } from "../src/baseline.mjs";
import { evaluateAll } from "../src/gates.mjs";

const iterations=20000;
const candidate=cloneBaseline();
const started=performance.now();
let keep=0;
for(let i=0;i<iterations;i++) if(evaluateAll(NEXY_BASELINE,candidate).composite.verdict==="KEEP_CANDIDATE") keep++;
const elapsedMs=performance.now()-started;
console.log(JSON.stringify({status:"OBSERVATION",suite:"cvrc20-benchmark",iterations,keep,elapsedMs,evalsPerSecond:iterations/(elapsedMs/1000),authoritative:false}));
