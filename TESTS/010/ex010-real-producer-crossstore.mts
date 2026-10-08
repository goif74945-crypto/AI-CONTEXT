// EX010: real PostgreSQL + BullMQ/Redis harness, IMPORT INTO PRODUCT/scripts.
// REAL dispatchDirective -> enqueueDirective -> BullMQ -> Prisma CAS via test-only transport ACK barriers.
// No mocks of producer or DB operations. TSA clock injection is TEST-ONLY and UNSIGNED.
// Requires fresh loopback DB nexy_ex010, Redis port 6390 AOF always. NOT_RUN here.
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { Queue, Worker } from "bullmq";
const connectionString = process.env["DATABASE_URL"] ?? "";
let u: URL;
try { u = new URL(connectionString); }
catch { throw new Error("EX010_BLOCKED: isolated DATABASE_URL missing"); }
const local = new Set(["127.0.0.1", "localhost", "[::1]"]);
if (process.env["NEXY_EX010_ISOLATED_TEST_ONLY"] !== "CONFIRMED"
  || !["postgres:", "postgresql:"].includes(u.protocol)
  || !local.has(u.hostname) || u.pathname !== "/nexy_ex010" || u.port !== "5440"
  || !local.has(process.env["REDIS_HOST"] ?? "")
  || process.env["REDIS_PORT"] !== "6390") {
  throw new Error("EX010_BLOCKED: non-isolated database/Redis endpoint");
}
const { prisma } = await import("../packages/core/db.js");
const { currentTick, injectTsaBatchTime, currentTsaBatchTimeMs } = await import("../packages/core/tick.js");
const { generateUlid } = await import("../packages/core/ulid.js");
const { dispatchDirective, cancelDirectiveDispatch, claimDirectiveDispatch, completeDirectiveDispatch } =
  await import("../packages/queue/dispatch.js");
const { isFailedDispatchRetryAllowed } = await import("../packages/queue/retry-policy.js");
const { commitAuthorizedPipelineRelease, emitAuthorizedPipelineOutput } =
  await import("../packages/queue/run-state.js");
const connection = { host:"127.0.0.1", port:6390 };
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
  const key="ex010-"+tag+"-"+(++seq);
  const tick=currentTick();
  await prisma.pipelineRun.create({data:{
    id:runId,createdTick:tick,wireVersion:2,agentId:1,
    fsmStateBefore:15,fsmStateAfter:15,commandResult:"Accepted",
    payloadHash:sha(runId),requestId:key,traceId:key,runState,
  }});
  await prisma.directiveRecord.create({data:{
    id:directiveId,createdTick:tick,createdAt,projectId:"ex010-isolated",
    input:"fixture",inputType:"TEXT",mode:"strict",priority:"NORMAL",
    maxTokens:512,allowExternal:false,deterministicRequired:true,
    operatorId:"EX010",requestedByRole:"OWNER",schemaVersion:"1.0.0",
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
  if (v === null) throw new Error("EX010_DISPATCH_ROW_MISSING");
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
  throw new Error("EX010_TIMEOUT: "+key);
}
try {
  const client=(await queue.client) as unknown as {
    ping: () => Promise<string>;
    config: (...args: string[]) => Promise<string[]>;
  };
  assert.equal(await client.ping(),"PONG");
  const aof=await client.config("GET","appendonly") as unknown as string[];
  const fsync=await client.config("GET","appendfsync") as unknown as string[];
  assert.equal(aof[1],"yes","Redis AOF must be enabled");
  assert.equal(fsync[1],"always","Redis appendfsync must be always");
  assert.equal(await prisma.directiveDispatch.count(),0,"requires empty dedicated DB");
  await prisma.$queryRawUnsafe("SELECT 1");
  report("T00","PASS_REAL_SERVICE_PRECHECK",{database:"nexy_ex010",redis:"127.0.0.1:6390",aof:aof[1],fsync:fsync[1]});
  // SOURCE-LINKED real producer test suite. This deterministic clock fixture is
  // TEST_ONLY_TIME_INJECTION, *not* a TSA signature, witness or trusted runtime time.
  injectTsaBatchTime(1_800_000_000_000n);
  assert.equal(currentTsaBatchTimeMs(), 1_800_000_000_000n);
  report("TSA_FIXTURE", "TEST_ONLY_TIME_INJECTION_NOT_SIGNED",
    {fixedBatch: "1800000000000", productionTsaSignature: "NOT_VERIFIED"});

  // Instrument ONLY the transport ACK barrier after REAL BullMQ Queue.add() has
  // persisted the job to Redis; no production state transition is rewritten.
  // The actual dispatchDirective() and enqueueDirective() code executes.
  const realAdd = Queue.prototype.add;
  let afterPublish: ((job: unknown) => Promise<void>) | undefined;
  Object.defineProperty(Queue.prototype, "add", {
    configurable: true, writable: true,
    value: async function (this: Queue, ...args: unknown[]) {
      const job = await (realAdd as (...a: unknown[]) => Promise<unknown>).apply(this, args);
      if (afterPublish) await afterPublish(job);
      return job;
    },
  });
  function barrier() {
    let reached!: () => void, release!: () => void;
    const entered = new Promise<void>((resolve) => { reached = resolve; });
    const proceed = new Promise<void>((resolve) => { release = resolve; });
    return { reached, release, entered, proceed };
  }
  async function bounded<T>(p: Promise<T>, label: string): Promise<T> {
    return Promise.race([
      p,
      new Promise<never>((_, reject) => setTimeout(
        () => reject(new Error("EX010_TEST_BARRIER_TIMEOUT: " + label)), 10000,
      )),
    ]);
  }

  // G3-P1: real product producer queue.add published to Redis, then owner
  // cancels before producer durable CAS. Worker must ignore that real job.
  const crossCancel = await seed("producer-cancel");
  const gatePublishA = barrier();
  afterPublish = async () => { gatePublishA.reached(); await gatePublishA.proceed; };
  const sending = dispatchDirective(crossCancel.runId);
  try {
    await bounded(gatePublishA.entered, "producer published");
    assert.ok(await queue.getJob(crossCancel.key), "real Redis job published");
    await cancelDirectiveDispatch(crossCancel.runId);
    gatePublishA.release();
    const result = await bounded(sending, "producer post-cancel CAS");
    assert.equal(result.status, "CANCELLED");
    assert.equal(result.delivered, false);
    const v = await row(crossCancel.runId);
    assert.equal(v.status, "CANCELLED");
    assert.equal(v.attempts, 0);
    assert.equal(v.lastError, "OWNER_CANCEL");
    report("G3-P1", "PASS_PRODUCER_DB_REDIS_BOUNDARY",
      {producer: result.status, redis: "PUBLISHED", status: v.status, attempts: v.attempts});
  } finally { gatePublishA.release(); afterPublish = undefined; }

  // G3-P2: Redis side-effect happened, but ACK is lost/throws after publication.
  // Owner cancellation must remain durable despite the catch path.
  const crossAckLost = await seed("producer-ack-lost");
  const gatePublishB = barrier();
  afterPublish = async () => {
    gatePublishB.reached(); await gatePublishB.proceed;
    throw Object.assign(new Error("EX010_TEST_ACK_LOST_AFTER_REAL_PUBLISH"),
      {code: "QUEUE_UNAVAILABLE"});
  };
  const ackSending = dispatchDirective(crossAckLost.runId);
  try {
    await bounded(gatePublishB.entered, "redis ACK loss after publish");
    assert.ok(await queue.getJob(crossAckLost.key), "ambiguous Redis side effect exists");
    await cancelDirectiveDispatch(crossAckLost.runId);
    gatePublishB.release();
    const result = await bounded(ackSending, "failure-path CAS");
    assert.equal(result.status, "CANCELLED");
    const v = await row(crossAckLost.runId);
    assert.equal(v.status, "CANCELLED");
    assert.equal(v.lastError, "OWNER_CANCEL");
    assert.equal(v.attempts, 0);
    report("G3-P2", "PASS_INSTRUMENTED_ACK_LOSS_AFTER_REAL_REDIS_PUBLISH",
      {redis: "JOB_EXISTS", durable: v.status, inferredNotPublished: false});
  } finally { gatePublishB.release(); afterPublish = undefined; }

  // G3-P3: worker's actual DB claim wins while producer waits on Redis ACK.
  // Producer CAS may not move PROCESSING back to ENQUEUED.
  const claimed = await seed("producer-early-claim");
  const gatePublishC = barrier();
  afterPublish = async () => { gatePublishC.reached(); await gatePublishC.proceed; };
  const claimSending = dispatchDirective(claimed.runId);
  try {
    await bounded(gatePublishC.entered, "worker early claim");
    assert.ok(await queue.getJob(claimed.key));
    assert.equal(await claimDirectiveDispatch(claimed.runId), "CLAIMED");
    gatePublishC.release();
    const result = await bounded(claimSending, "producer loses to worker claim");
    assert.equal(result.status, "PROCESSING");
    const v = await row(claimed.runId);
    assert.equal(v.status, "PROCESSING");
    assert.equal(v.attempts, 0);
    await cancelDirectiveDispatch(claimed.runId);
    assert.equal((await row(claimed.runId)).status, "CANCELLED");
    report("G3-P3", "PASS_REAL_DB_WORKER_CLAIM_BEFORE_PRODUCER_CAS",
      {producer: result.status, durableAfterCancel: "CANCELLED", attempts: v.attempts});
  } finally { gatePublishC.release(); afterPublish = undefined; }

  // G3-P4: two concurrent ACTUAL producers share one BullMQ jobId.
  const dupProducer = await seed("producer-duplicate");
  const [p1, p2] = await Promise.all([
    dispatchDirective(dupProducer.runId),
    dispatchDirective(dupProducer.runId),
  ]);
  assert.ok(await queue.getJob(dupProducer.key));
  const dv = await row(dupProducer.runId);
  assert.equal(dv.status, "ENQUEUED");
  assert.equal(dv.attempts, 1, "only one CAS may advance attempts");
  assert.ok([p1.status, p2.status].every(v => v === "ENQUEUED"));
  report("G3-P4", "PASS_REAL_DISPATCH_DUPLICATE_IDEMPOTENCY",
    {attempts: dv.attempts, jobId: dupProducer.key, statuses: [p1.status,p2.status]});

  // G3-P5: probe worker is started later, after all cancellations.
  // It must never execute provider for either real published CANCELLED row.
  // This does not prove the packages/queue/workers.ts production Worker.
  const deniedProducerRuns = [crossCancel.runId,crossAckLost.runId,claimed.runId];

  const pre=await seed("pre");
  await cancelDirectiveDispatch(pre.runId);
  assert.equal((await row(pre.runId)).status,"CANCELLED");
  assert.equal((await queue.getJob(pre.key)) ?? null, null);
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
  for (const id of deniedProducerRuns) {
    const pending = await row(id);
    const job = await queue.getJob(pending.idempotencyKey);
    assert.ok(job, "real producer job missing after cancellation");
    await poll(pending.idempotencyKey);
    assert.equal(providers.get(id) ?? 0, 0, "cancelled run executed test provider");
    assert.deepEqual(claims.get(id), ["CANCELLED"]);
  }
  report("G3-P5", "PASS_PROBE_WORKER_NO_PROVIDER_AFTER_CANCEL",
    {cancelledPublishedJobCount: deniedProducerRuns.length, providerCalls: 0,
     fullProductionWorker: "NOT_RUN"});

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
  const output="ex010 release rejected", hash=sha(output);
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
  // Transport instrumentation was test-only; do not retain it in other processes.
  // Queue.prototype is process-local and the script exits after closing connections.
  await queue.close();
  await prisma.$disconnect();
}
