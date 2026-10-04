#!/usr/bin/env node
import { readFile } from 'node:fs/promises';
import { analyzeImpact } from './impact_graph.mjs';

const [graphPath, ...changedIds] = process.argv.slice(2);

if (!graphPath || changedIds.length === 0) {
  process.stderr.write('usage: node src/cli.mjs <graph.json> <changed-node-id> [more-ids...]\n');
  process.exitCode = 64;
} else {
  try {
    const graph = JSON.parse(await readFile(graphPath, 'utf8'));
    const result = analyzeImpact(graph, changedIds);
    process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
    if (result.status !== 'PASS') process.exitCode = 2;
  } catch (error) {
    process.stdout.write(`${JSON.stringify({
      status: 'FREEZE',
      reason_code: 'INPUT_READ_FAILURE',
      details: { message: error instanceof Error ? error.message : String(error) }
    }, null, 2)}\n`);
    process.exitCode = 2;
  }
}
