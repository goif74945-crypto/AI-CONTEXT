import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFile, readdir } from 'node:fs/promises';
import { join } from 'node:path';
import { Q64, auditEquitableControlPack } from './src/index.mjs';

const q = Q64.parse;
let checks = 0;
const check = (value, message) => { assert(value, message); checks += 1; };

for (let i = -128; i <= 128; i++) {
  for (let j = 1; j <= 32; j++) {
    const a = Q64.fromInt(BigInt(i));
    const b = Q64.fromRatio(BigInt(j), 8n);
    check(a.add(b).sub(b).eq(a), 'Q64 add/sub identity');
    check(a.mul(b).eq(b.mul(a)), 'Q64 mul commutativity');
  }
}

for (let i = 0; i < 20000; i++) {
  const aFreeze = BigInt(10 + (i % 5));
  const bFreeze = BigInt(11 + (i % 5));
  const aAvoid = BigInt(1 + (i % 2));
  const bAvoid = BigInt(2 + (i % 2));
  const aNear = BigInt(8 + (i % 3));
  const bNear = BigInt(10 + (i % 3));
  const pack = auditEquitableControlPack({
    cohorts: [
      { id: 'A', total: 100n, freezes: aFreeze, avoidableFreezes: aAvoid, evidenceBurdenTotal: q('100'), recoveryEligible: 10n, recovered: 9n, recoveryDurationTotal: q('18'), nearBoundary: aNear },
      { id: 'B', total: 100n, freezes: bFreeze, avoidableFreezes: bAvoid, evidenceBurdenTotal: q('110'), recoveryEligible: 10n, recovered: 9n, recoveryDurationTotal: q('19.8'), nearBoundary: bNear },
    ],
    policies: {
      freeze: { minSample: 50n, maxFreezeRateGap: q('0.05') },
      verification: { minSample: 50n, maxAverageBurdenGap: q('0.20') },
      avoidable: { minSample: 50n, maxAvoidableFreezeRateGap: q('0.03') },
      recovery: { minSample: 50n, maxRecoveryRateGap: q('0.10'), maxAverageRecoveryTimeGap: q('0.50') },
      threshold: { minSample: 50n, maxNearBoundaryRateGap: q('0.05') },
    }
  });
  check(pack.status === 'READY_FOR_HUMAN_REVIEW', 'synthetic parity scenario should pass');
  check(pack.results.length === 5, 'all five systems must execute');
}

async function collect(dir) {
  const entries = await readdir(dir, { withFileTypes: true });
  const files = [];
  for (const e of entries) {
    const p = join(dir, e.name);
    if (e.isDirectory()) files.push(...await collect(p));
    else files.push(p);
  }
  return files;
}
const root = new URL('.', import.meta.url).pathname;
const files = (await collect(root)).filter(p => !p.includes('/evidence/'));
const hashes = {};
for (const p of files.sort()) {
  hashes[p.slice(root.length)] = createHash('sha256').update(await readFile(p)).digest('hex');
}

console.log(JSON.stringify({
  status: 'PASS',
  arithmetic: 'Q64.64 signed-128 bounded BigInt host representation',
  invariantChecks: checks,
  syntheticPackCases: 20000,
  conceptCount: 5,
  authorityBoundary: 'Audit-only; no cohort inference, no Canon mutation, no release decision.',
  fileHashes: hashes,
}, null, 2));
