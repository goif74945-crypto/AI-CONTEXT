import { describe, expect, it } from "vitest";
import { readFileSync } from "node:fs";

const run = readFileSync("packages/queue/run-state.ts", "utf8");
const dispatch = readFileSync("packages/queue/dispatch.ts", "utf8");
function segment(source: string, start: string, end?: string) {
  const a = source.indexOf(start);
  if (a < 0) throw new Error("SOURCE_ANCHOR_MISSING:" + start);
  const b = end ? source.indexOf(end, a + start.length) : source.length;
  if (b < 0) throw new Error("END_ANCHOR_MISSING:" + end);
  return source.slice(a, b);
}
describe("EX010 canonical OWNER cancellation transaction source contract (not DB runtime proof)", () => {
  it("canonical cancel goes through recordPipelineRunFailure with cancelDispatch true", () => {
    const cancel = segment(run, "export async function cancelPipelineRun(");
    expect(cancel).toContain("const incidentId = await recordPipelineRunFailure(");
    expect(cancel).toContain("cancelDispatch: true");
  });
  it("canonical failure transaction locks PipelineRun and writes FREEZE plus dispatch CANCELLED", () => {
    const failure = segment(run, "export async function recordPipelineRunFailure(", "export async function emitAuthorizedPipelineOutput(");
    const transaction = failure.indexOf("await prisma.$transaction(");
    const lock = failure.indexOf("await lockPipelineRun(tx, failure.pipelineRunId)");
    const durableFreeze = failure.indexOf("await tx.pipelineRun.update(");
    const durableCancel = failure.indexOf("await tx.directiveDispatch.updateMany(");
    expect(transaction).toBeGreaterThanOrEqual(0);
    expect(lock).toBeGreaterThan(transaction);
    expect(durableFreeze).toBeGreaterThan(lock);
    expect(durableCancel).toBeGreaterThan(durableFreeze);
    expect(failure).toContain("status: DISPATCH_STATUS.CANCELLED");
  });
  it("LAW release takes the same transaction-level advisory lock before checking cancellation", () => {
    const release = segment(run, "export async function commitAuthorizedPipelineRelease(", "export interface RunFailure");
    expect(release.indexOf("await lockPipelineRun(tx, pipelineRunId)")).toBeGreaterThanOrEqual(0);
    expect(release.indexOf("await assertDispatchNotCancelled(tx, pipelineRunId)")).toBeGreaterThan(0);
    expect(release.indexOf("await lockPipelineRun(tx, pipelineRunId)")).toBeLessThan(
      release.indexOf("await assertDispatchNotCancelled(tx, pipelineRunId)"));
  });
  it("standalone dispatch helper uses status updateMany without acquiring PipelineRun advisory lock", () => {
    const direct = segment(dispatch, "export async function cancelDirectiveDispatch(");
    expect(direct).toContain("await prisma.directiveDispatch.updateMany(");
    expect(direct).not.toContain("pg_advisory_xact_lock");
    expect(direct).not.toContain("lockPipelineRun(");
  });
  it("output emission requires STABLE and releaseable, but no independent dispatch cancel lookup", () => {
    const emit = segment(run, "export async function emitAuthorizedPipelineOutput(", "export interface RevokeStableReleaseOptions");
    expect(emit).toContain("await lockPipelineRun(tx, pipelineRunId)");
    expect(emit).toContain("current.runState !== RUN_STATE.STABLE");
    expect(emit).toContain("current.releaseable !== true");
    expect(emit).not.toContain("await assertDispatchNotCancelled(tx, pipelineRunId)");
  });
});
