// EX009: real PostgreSQL + BullMQ/Redis harness, IMPORT INTO PRODUCT/scripts.
// NO mocks. The producer probe is direct BullMQ, NOT production TSA dispatcher.
// Requires fresh loopback DB nexy_ex009, Redis port 6389 AOF always. NOT_RUN here.
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { Queue, Worker } from "bullmq";
const connectionString = process.env["DATABASE_URL"] ?? "";
let u: URL;
try { u = new URL(connectionString); }
catch { throw new Error("EX009_BLOCKED: isolated DATABASE_URL missing"); }
const local = new Set(["127.0.0.1", "localhost", "[::1]"]);
if (process.env["NEXY_EX009_ISOLATED_TEST_ONLY"] !== "CONFIRMED"
  || !["postgres:", "postgresql:"].includes(u.protocol)
  || !local.has(u.hostname) || u.pathname !== "/nexy_ex009" || u.port !== "5439"
  || !local.has(process.env["REDIS_HOST"] ?? "")
  || process.env["REDIS_PORT"] !== "6389") {
  throw new Error("EX009_BLOCKED: non-isolated database/Redis endpoint");
}
const { prisma } = await import("../packages/core/db.js");
const { currentTick } = await import("../packages/core/tick.js");
const { generateUlid } = await import("../packages/core/ulid.js");
const { cancelDirectiveDispatch, claimDirectiveDispatch, completeDirectiveDispatch } =
  await import("../packages/queue/dispatch.js");
const { isFailedDispatchRetryAllowed } = await import("../packages/queue/retry-policy.js");
const { commitAuthorizedPipelineRelease, emitAuthorizedPipelineOutput } =
  await import("../packages/queue/run-state.js");
const connection = { host:"127.0.0.1", port:6389 };
const queue = new Queue("pipeline", {connection});
let worker: Worker | undefined;
const claims = new Map<string, string[]>();
const providers = new Map<string, number>();
const sha = (v:string) => createHash("sha256").update(v).digest("hex");
const createdAt = new Date("2026-10-08T00:00:00Z"); // test metadata, not TSA
let seq = 0;
function report(id:string, verdict:string, evidence:unknown) {
  console.log(JSON.stringify({id,verdict,evidence}));
}
async function seed(tag:string, runState="RUNNING") {
  const runId=generateUlid(), directiveId=generateUlid();
  const key="ex009-"+tag+"-"+(++seq);
  const tick=currentTick();
  await prisma.pipelineRun.create({data:{
    id:runId,createdTick:tick,wireVersion:2,agentId:1,
    fsmStateBefore:15,fsmStateAfter:15,commandResult:"Accepted",
    payloadHash:sha(runId),requestId:key,traceId:key,runState,
  }});
  await prisma.directiveRecord.create({data:{
    id:directiveId,createdTick:tick,createdAt,projectId:"ex009-isolated",
    input:"fixture",inputType:"TEXT",mode:"strict",priority:"NORMAL",
    maxTokens:512,allowExternal:false,deterministicRequired:true,
    operatorId:"EX009",requestedByRole:"OWNER",schemaVersion:"1.0.0",
    idempotencyKey:key,pipelineRunId:runId,
  }});
  await prisma.directiveDispatch.create({data:{
    id:generateUlid(),directiveId,pipelineRunId:runId,
    idempotencyKey:key,status:"PENDING",attempts:0,
    createdTick:tick,updatedTick:tick,
  }});
  return {runId,directiveId,key};
}
type Seed = Awaited<ReturnType<typeof seed>>;
async function row(id:string) {
  const v=await prisma.directiveDispatch.findUnique({where:{pipelineRunId:id}});
  assert.ok(v,"dispatch row missing");
  return v;
}
function directTestJob(s:Seed) {
  return queue.add("pipeline",{
    directiveId:s.directiveId,pipelineRunId:s.runId,input:"fixture",
    mode:"strict",priority:"NORMAL",idempotencyKey:s.key,
  },{jobId:s.key,removeOnComplete:false,removeOnFail:false});
}
async function poll(key:string) {
  for(let i=0;i<100;i++){
    const j=await queue.getJob(key);
    if(j && (await j.getState())==="completed")return;
    await new Promise(r=>setTimeout(r,120)); // test timeout only, never core time
  }
  throw new Error("EX009_TIMEOUT: "+key);
}
try {
  const client=await queue.client;
  assert.equal(await client.ping(),"PONG");
  const aof=await client.config("GET","appendonly") as unknown as string[];
  const fsync=await client.config("GET","appendfsync") as unknown as string[];
  assert.equal(aof[1],"yes","Redis AOF must be enabled");
  assert.equal(fsync[1],"always","Redis appendfsync must be always");
  assert.equal(await prisma.directiveDispatch.count(),0,"requires empty dedicated DB");
  await prisma.$queryRawUnsafe("SELECT 1");
  report("T00","PASS_REAL_SERVICE_PRECHECK",{database:"nexy_ex009",redis:"127.0.0.1:6389",aof:aof[1],fsync:fsync[1]});
  const pre=await seed("pre");
  await cancelDirectiveDispatch(pre.runId);
  assert.equal((await row(pre.runId)).status,"CANCELLED");
  assert.equal(await queue.getJob(pre.key),undefined);
  assert.equal(await claimDirectiveDispatch(pre.runId),"CANCELLED");
  report("T01","PASS",{db:"CANCELLED",redis:"NO_JOB",providerCalls:0});
  const after=await seed("published","CONSENSUS");
  await directTestJob(after);
  assert.ok(await queue.getJob(after.key),"must publish to Redis before cancel");
  const observed=await row(after.runId);
  await cancelDirectiveDispatch(after.runId);
  const cas=await prisma.directiveDispatch.updateMany({
    where:{id:observed.id,status:observed.status,attempts:observed.attempts},
    data:{status:"ENQUEUED",attempts:{increment:1},updatedTick:currentTick()},
  });
  assert.equal(cas.count,0);
  assert.equal((await row(after.runId)).status,"CANCELLED");
  worker=new Worker("pipeline",async job=>{
    const runId=String(job.data.pipelineRunId);
    const claim=await claimDirectiveDispatch(runId); // real product function
    claims.set(runId,[...(claims.get(runId)??[]),claim]);
    if(claim!=="CLAIMED")return {claim,provider:"NOT_CALLED"};
    providers.set(runId,(providers.get(runId)??0)+1);
    if((await row(runId)).status==="CANCELLED")return {claim,provider:"ABORTED"};
    await completeDirectiveDispatch(runId);
    return {claim,provider:"FIXTURE_ONLY"};
  },{connection,concurrency:1});
  await worker.waitUntilReady();
  await poll(after.key);
  assert.deepEqual(claims.get(after.runId),["CANCELLED"]);
  assert.equal(providers.get(after.runId)??0,0);
  assert.equal((await row(after.runId)).attempts,0);
  report("T04","PASS_REAL_BULLMQ_DB_CAS",{jobState:"completed",db:"CANCELLED",claim:"CANCELLED",providerCalls:0});
  const dupe=await seed("dupe");
  const [a,b]=await Promise.all([directTestJob(dupe),directTestJob(dupe)]);
  assert.equal(a.id,b.id);
  await poll(dupe.key);
  assert.equal(claims.get(dupe.runId)?.length,1);
  assert.equal(providers.get(dupe.runId),1);
  report("T06","PASS_REAL_BULLMQ_DEDUP",{jobId:a.id,claims:1});
  const policy={enabled:true,maxAttempts:3,safeErrorCodes:["QUEUE_UNAVAILABLE"]};
  assert.equal(isFailedDispatchRetryAllowed({status:"FAILED",attempts:1,lastError:"QUEUE_UNAVAILABLE"},policy),true);
  assert.equal(isFailedDispatchRetryAllowed({status:"FAILED",attempts:3,lastError:"QUEUE_UNAVAILABLE"},policy),false);
  assert.equal(isFailedDispatchRetryAllowed({status:"FAILED",attempts:1,lastError:"SCHEMA_VIOLATION"},policy),false);
  report("T07","PASS_SOURCE_POLICY_ONLY",{bullmqFailedRetry:"NOT_RUN"});
  const output="ex009 release rejected", hash=sha(output);
  const metrics={confidence:1,deterministicMatchScore:1,quorumCount:5,
    evidenceCount:5,candidateHash:hash,agentIds:["a","b","c","d","e"]};
  await assert.rejects(
    commitAuthorizedPipelineRelease(after.runId,metrics,output,hash,sha("consensus")),
    /DISPATCH_CANCELLED/,
  );
  await assert.rejects(
    emitAuthorizedPipelineOutput(after.runId,"OWNER",after.key,after.key),
    /UNVERIFIED_OUTPUT/,
  );
  const run=await prisma.pipelineRun.findUniqueOrThrow({where:{id:after.runId}});
  assert.notEqual(run.runState,"STABLE");
  assert.notEqual(run.accepted,true);
  assert.equal(run.outputText,null);
  const receipts=await prisma.auditLog.count({where:{
    resourceId:after.runId,action:"RELEASE_POLICY_PASSED",
  }});
  assert.equal(receipts,0);
  report("T11","PASS_REAL_RELEASE_TX_FENCE",{runState:run.runState,output:null,lawPassReceipts:0});
  report("T02,T03,T05,T08,T09,T10,T12,T13,T14","NOT_RUN",
    "Requires controlled service faults, production worker, or validated TSA boundary.");
} finally {
  await worker?.close();
  await queue.close();
  await prisma.$disconnect();
}
