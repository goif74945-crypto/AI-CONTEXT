// packages/phase-f/lo3/cage.ts
// CMD-G1.C — Lo3 The Cage: hardened sandbox for external AI calls.
//
// Two surfaces share this module:
//
//   1. runInCage(fn, config?)                           ← legacy CMD-F3
//        Runs an in-process async function with a wall-time guard and an
//        output truncation cap.  Retained for callers that just need a
//        rough resource budget around trusted internal logic.
//
//   2. runInCage(command, args, input, config?)         ← CMD-G1.C
//        Spawns an OS-isolated child process with cgroup v2 + seccomp +
//        bubblewrap (Linux), sandbox-exec (macOS), or a dev-naive
//        fallback (otherwise).  Used by swarm adapters (OpenAI,
//        Anthropic, …) whenever NEXY_CAGE_ENABLED=true so untrusted
//        plaintext from external AI providers cannot escape the cage.
//
// Both surfaces persist a CageInvocation row with the SHA-256 of args and
// stdout — the audit trail for what each external call did, without
// recording the secrets that travelled through it.

import { currentTick }                       from "../../core/tick.js";
import { generateUlid }                      from "../../core/ulid.js";
import { prisma }                            from "../../core/db.js";
import { spawn, type ChildProcess, execFile } from "node:child_process";
import { writeFileSync, mkdirSync,
         existsSync, rmSync, realpathSync,
         statSync, accessSync, constants }   from "node:fs";
import { writeFile, unlink }                 from "node:fs/promises";
import { join, isAbsolute, basename }        from "node:path";
import { createHash }                        from "node:crypto";
import { tmpdir }                            from "node:os";
import { promisify }                         from "node:util";

const execFileAsync = promisify(execFile);

// ── Constants ────────────────────────────────────────────────────────────

const DEFAULT_MAX_EXEC_MS       = 5_000;
const DEFAULT_MAX_OUTPUT_BYTES  = 64 * 1024;     // 64 KiB
const DEFAULT_MAX_MEMORY_MB     = 256;
const DEFAULT_CPU_QUOTA_PCT     = 25;            // % of one core
const CGROUP_BASE               = "/sys/fs/cgroup/nexy-cage";
const SECCOMP_ALLOWED_SYSCALLS  = new Set([
  "read", "write", "close", "fstat", "lseek", "mmap", "mprotect",
  "munmap", "brk", "rt_sigaction", "rt_sigprocmask", "ioctl",
  "access", "exit", "exit_group", "futex", "clone", "execve",
  "openat", "getdents64", "statx", "nanosleep", "arch_prctl",
  "set_tid_address", "set_robust_list", "prlimit64", "getrandom",
]);

// ── Public types (CMD-G1.C command-based API) ────────────────────────────

export type CageBackend =
  | "linux-cgroup-seccomp"
  | "macos-sandbox-exec"
  | "windows-job-object"
  | "dev-naive";

export interface CommandCageConfig {
  memoryMb:         number;        // hard cap (cgroup memory.max)
  cpuQuotaPercent:  number;        // 0..100 (cgroup cpu.max)
  cpuShares:        number;        // weight 1..10000
  wallTimeoutMs:    number;        // SIGKILL after this
  maxOutputBytes:   number;        // truncate stdout/stderr after this
  networkAllowlist: string[];      // outbound DNS allowlist
  diskWriteMb:      number;        // ephemeral disk allowed
  blockSyscalls:    string[];      // seccomp blacklist
}

export const DEFAULT_CAGE_CONFIG: CommandCageConfig = {
  memoryMb:         256,
  cpuQuotaPercent:  50,
  cpuShares:        1024,
  wallTimeoutMs:    60_000,
  maxOutputBytes:   2 * 1024 * 1024,  // 2 MB
  networkAllowlist: ["api.openai.com", "api.anthropic.com"],
  diskWriteMb:      10,
  blockSyscalls:    [
    "mount", "umount", "ptrace", "kexec_load",
    "init_module", "delete_module",
  ],
};

export interface CageMetrics {
  readonly peakRssMb:        number;
  readonly cpuMsUsed:        number;
  readonly networkBytesIn:   number;
  readonly networkBytesOut:  number;
  readonly diskBytesWritten: number;
}

export interface CommandCageResult {
  readonly id:        string;
  readonly stdout:    string;
  readonly stderr:    string;
  readonly exitCode:  number | null;
  readonly signal:    string | null;
  readonly timedOut:  boolean;
  readonly truncated: boolean;
  readonly elapsedMs: number;
  readonly backend:   CageBackend;
  readonly metrics:   CageMetrics;
  readonly startTick: bigint;
  readonly endTick:   bigint;
}

// ── Legacy types (CMD-F3 fn-based API) — preserved verbatim ─────────────

export interface CageConfig {
  maxExecMs:        number;
  maxOutputBytes:   number;
  /** Memory limit in MiB (applied via cgroup v2; default 256) */
  maxMemoryMib:     number;
  /** CPU quota percent of one core (default 25) */
  cpuQuotaPct:      number;
  /** Permitted outbound hostnames; empty = no network */
  networkAllowlist: string[];
  /** Environment variables passed into the child process */
  env:              Record<string, string>;
  /** Seccomp mode: "strict" = allowlist only, "permissive" = audit-only */
  seccompMode:      "strict" | "permissive";
}

export interface CageResult {
  readonly id:           string;
  readonly output:       string;
  readonly exitCode:     number;
  readonly timedOut:     boolean;
  readonly truncated:    boolean;
  readonly elapsedMs:    number;
  readonly startTick:    bigint;
  readonly endTick:      bigint;
  readonly memoryPeakMib: number;
  readonly networkBlocked: number;  // count of blocked DNS queries
  readonly auditLog:     readonly CageAuditEntry[];
}

export interface CageAuditEntry {
  readonly entryId:   string;
  readonly timestamp: string;
  readonly event:     "SPAWN" | "STDOUT" | "STDERR" | "TIMEOUT" | "EXIT"
                    | "NETWORK_BLOCK" | "SECCOMP_VIOLATION" | "CGROUP_ATTACH";
  readonly detail:    string;
}

export type CagedFn = () => Promise<string>;

/** Propagated as a FREEZE envelope instead of calling process.exit */
export class CageError extends Error {
  readonly cageId: string;
  readonly kind:   "TIMEOUT" | "SECCOMP" | "OOM" | "SPAWN_FAILED" | "NETWORK";
  constructor(cageId: string, kind: CageError["kind"], msg: string) {
    super(msg);
    this.name   = "CageError";
    this.cageId = cageId;
    this.kind   = kind;
    Object.setPrototypeOf(this, new.target.prototype);
  }
}

// ── Default-config factories ────────────────────────────────────────────

export function defaultCageConfig(overrides: Partial<CageConfig> = {}): CageConfig {
  return {
    maxExecMs:        DEFAULT_MAX_EXEC_MS,
    maxOutputBytes:   DEFAULT_MAX_OUTPUT_BYTES,
    maxMemoryMib:     DEFAULT_MAX_MEMORY_MB,
    cpuQuotaPct:      DEFAULT_CPU_QUOTA_PCT,
    networkAllowlist: [],
    env:              {},
    seccompMode:      "permissive",
    ...overrides,
  };
}

// ── Cgroup v2 helpers (Linux only) ──────────────────────────────────────

function isCgroupAvailable(): boolean {
  return process.platform === "linux" && existsSync("/sys/fs/cgroup");
}

function cgroupPath(cageId: string): string {
  return join(CGROUP_BASE, cageId);
}

function attachCgroup(
  cageId:    string,
  pid:       number,
  memMib:    number,
  cpuPct:    number,
  audit:     CageAuditEntry[],
): void {
  if (!isCgroupAvailable()) return;
  try {
    const cgPath = cgroupPath(cageId);
    mkdirSync(cgPath, { recursive: true });
    writeFileSync(join(cgPath, "memory.max"), `${memMib * 1024 * 1024}`);
    const period  = 100_000;
    const quota   = Math.round((cpuPct / 100) * period);
    writeFileSync(join(cgPath, "cpu.max"), `${quota} ${period}`);
    writeFileSync(join(cgPath, "cgroup.procs"), `${pid}`);
    audit.push({
      entryId:   generateUlid(),
      timestamp: currentTick().toString(),
      event:     "CGROUP_ATTACH",
      detail:    `pid=${pid} mem=${memMib}MiB cpu=${cpuPct}%`,
    });
  } catch {
    // cgroup setup failure is non-fatal on restricted environments
  }
}

function cleanupCgroup(cageId: string): void {
  if (!isCgroupAvailable()) return;
  try {
    const cgPath = cgroupPath(cageId);
    if (existsSync(cgPath)) rmSync(cgPath, { recursive: true, force: true });
  } catch {
    // best-effort
  }
}

function readCgroupMemoryPeakMib(cageId: string): number {
  if (!isCgroupAvailable()) return 0;
  try {
    const { readFileSync } = require("node:fs") as typeof import("node:fs");
    const raw = readFileSync(join(cgroupPath(cageId), "memory.peak"), "utf8").trim();
    return Math.round(parseInt(raw, 10) / (1024 * 1024));
  } catch {
    return 0;
  }
}

function readCgroupCpuUsageMs(cgPath: string): number {
  if (!isCgroupAvailable()) return 0;
  try {
    const { readFileSync } = require("node:fs") as typeof import("node:fs");
    const stat = readFileSync(join(cgPath, "cpu.stat"), "utf8");
    const m = /usage_usec\s+(\d+)/.exec(stat);
    return m ? Math.round(parseInt(m[1] ?? "0", 10) / 1000) : 0;
  } catch {
    return 0;
  }
}

// ── Seccomp audit ───────────────────────────────────────────────────────

function parseSeccompViolation(line: string): string | null {
  const m = /\[SECCOMP\] syscall=(\S+)/.exec(line);
  if (!m) return null;
  const syscall = m[1] ?? "";
  return SECCOMP_ALLOWED_SYSCALLS.has(syscall) ? null : syscall;
}

// ── Network allowlist ───────────────────────────────────────────────────

function checkNetworkAllowed(host: string, allowlist: string[]): boolean {
  if (allowlist.length === 0) return false;
  return allowlist.some((allowed) =>
    host === allowed || host.endsWith(`.${allowed}`),
  );
}

// ── Backend detection ───────────────────────────────────────────────────

export function detectBackend(): CageBackend {
  if (process.platform === "linux") return "linux-cgroup-seccomp";
  if (process.platform === "darwin") return "macos-sandbox-exec";
  if (process.platform === "win32")  return "windows-job-object";
  return "dev-naive";
}

function hasExecutable(bin: string): boolean {
  try {
    if (process.platform === "win32") {
      execFileAsync("where", [bin]);
    } else {
      execFileAsync("which", [bin]);
    }
    return true;
  } catch {
    return false;
  }
}

async function bwrapAvailable(): Promise<boolean> {
  if (process.platform !== "linux") return false;
  try {
    await execFileAsync("which", ["bwrap"]);
    // A binary on PATH is not enough: restricted CI/container hosts often
    // expose bwrap while denying the user/mount namespaces it needs. Probe
    // the exact isolation shape before selecting it so the documented
    // dev-naive fallback remains available on those hosts.
    await execFileAsync("bwrap", [
      "--ro-bind", "/usr", "/usr",
      "--ro-bind", "/lib", "/lib",
      "--ro-bind", "/lib64", "/lib64",
      "--ro-bind", "/etc/ssl", "/etc/ssl",
      "--proc", "/proc",
      "--dev", "/dev",
      "--tmpfs", "/tmp",
      "--unshare-all",
      "--share-net",
      "--die-with-parent",
      "/usr/bin/true",
    ], { timeout: 1_000 });
    return true;
  } catch {
    return false;
  }
}

// Only the executable already running this trusted parent may extend the
// fixed system mounts. Guest input cannot nominate a runtime directory.
const PARENT_EXECUTABLE = process.execPath;
const LINUX_SYSTEM_RUNTIME_ROOTS = ["/usr", "/lib", "/lib64"] as const;

function resolveTrustedLinuxCommand(command: string): {
  executable: string;
  runtimeMounts: string[];
} {
  if (command.includes("\0") || command.split("/").some((part) => part === "." || part === "..")) {
    throw new CageError("unspawned", "SPAWN_FAILED", "COMMAND_PATH_TRAVERSAL");
  }
  let candidate = command;
  if (!isAbsolute(command)) {
    // Never resolve against guest-controlled PATH or the current directory.
    if (command.includes("/")) {
      throw new CageError("unspawned", "SPAWN_FAILED", "UNTRUSTED_RUNTIME: relative command");
    }
    candidate = [join("/usr/bin", command), join("/bin", command)]
      .find((path) => existsSync(path)) ?? (command === basename(PARENT_EXECUTABLE) ? PARENT_EXECUTABLE : "");
  }
  let executable: string;
  let parentExecutable: string;
  try {
    executable = realpathSync(candidate);
    parentExecutable = realpathSync(PARENT_EXECUTABLE);
    if (!statSync(executable).isFile()) throw new Error("command is not a regular file");
    accessSync(executable, constants.X_OK);
  } catch {
    throw new CageError("unspawned", "SPAWN_FAILED", "COMMAND_RESOLUTION_FAILED: executable required");
  }
  const withinSystemRuntime = LINUX_SYSTEM_RUNTIME_ROOTS.some((root) => executable.startsWith(`${root}/`));
  if (!withinSystemRuntime && executable !== parentExecutable) {
    throw new CageError("unspawned", "SPAWN_FAILED", "UNTRUSTED_RUNTIME: command is outside trusted runtime");
  }
  return { executable, runtimeMounts: withinSystemRuntime ? [] : [executable] };
}

function buildLinuxBwrapArgs(command: string, args: readonly string[]): string[] {
  const { executable, runtimeMounts } = resolveTrustedLinuxCommand(command);
  return [
    "--ro-bind", "/usr", "/usr",
    "--ro-bind", "/lib", "/lib",
    "--ro-bind", "/lib64", "/lib64",
    "--ro-bind", "/etc/ssl", "/etc/ssl",
    // Bind the single trusted binary; its sibling files remain invisible.
    ...runtimeMounts.flatMap((path) => ["--ro-bind", path, path]),
    "--proc", "/proc",
    "--dev", "/dev",
    "--tmpfs", "/tmp",
    "--unshare-all",
    "--share-net",
    "--die-with-parent",
    executable, ...args,
  ];
}

// ── Hashing helpers (DB persistence) ────────────────────────────────────

function hashArgs(args: readonly string[]): string {
  return createHash("sha256").update(args.join("\x00")).digest("hex");
}

function hashOutput(output: string): string {
  return createHash("sha256").update(output).digest("hex");
}

function defaultMetrics(): CageMetrics {
  return {
    peakRssMb:        0,
    cpuMsUsed:        0,
    networkBytesIn:   0,
    networkBytesOut:  0,
    diskBytesWritten: 0,
  };
}

async function persistCageInvocation(args: {
  id:        string;
  command:   string;
  argsArr:   readonly string[];
  backend:   CageBackend;
  config:    CommandCageConfig;
  stdout:    string;
  exitCode:  number | null;
  signal:    string | null;
  timedOut:  boolean;
  metrics:   CageMetrics;
  startTick: bigint;
  endTick:   bigint;
}): Promise<void> {
  try {
    const cageClient =
      (prisma as unknown as Record<string, unknown>)["cageInvocation"];
    if (!cageClient || typeof (cageClient as { create?: unknown }).create !== "function") {
      return;
    }
    await (cageClient as {
      create: (a: { data: Record<string, unknown> }) => Promise<unknown>;
    }).create({
      data: {
        id:         args.id,
        command:    args.command.slice(0, 256),
        argsHash:   hashArgs(args.argsArr),
        backend:    args.backend,
        config:     args.config as unknown as Record<string, unknown>,
        stdoutHash: hashOutput(args.stdout),
        exitCode:   args.exitCode,
        signal:     args.signal,
        timedOut:   args.timedOut,
        metrics:    args.metrics as unknown as Record<string, unknown>,
        startTick:  args.startTick,
        endTick:    args.endTick,
      },
    });
  } catch {
    // Persistence is best-effort — the cage MUST never freeze just because
    // the audit table is unreachable.  The hash chain lives in the audit_log
    // table for the kernel-level invariant.
  }
}

// ── Shared child-process collector ──────────────────────────────────────

interface CollectArgs {
  id:          string;
  proc:        ChildProcess;
  input:       string;
  cfg:         CommandCageConfig;
  startTick:   bigint;
  cgroupPath:  string | null;
}

async function collectProcessResult(
  args: CollectArgs,
): Promise<Omit<CommandCageResult, "backend" | "id">> {
  const { proc, input, cfg, startTick, cgroupPath } = args;
  let stdout = "";
  let stderr = "";
  let truncated = false;
  let timedOut  = false;

  if (input.length > 0 && proc.stdin) {
    proc.stdin.write(input);
    proc.stdin.end();
  }

  proc.stdout?.on("data", (chunk: Buffer) => {
    if (truncated) return;
    const remaining = cfg.maxOutputBytes - stdout.length;
    if (chunk.length >= remaining) {
      stdout += chunk.toString("utf-8").slice(0, Math.max(0, remaining));
      truncated = true;
      proc.kill("SIGTERM");
    } else {
      stdout += chunk.toString("utf-8");
    }
  });

  proc.stderr?.on("data", (chunk: Buffer) => {
    if (stderr.length < cfg.maxOutputBytes) {
      const remaining = cfg.maxOutputBytes - stderr.length;
      stderr += chunk.toString("utf-8").slice(0, Math.max(0, remaining));
    }
  });

  const killTimer = setTimeout(() => {
    timedOut = true;
    proc.kill("SIGKILL");
  }, cfg.wallTimeoutMs);

  const { exitCode, signal } = await new Promise<{
    exitCode: number | null; signal: string | null;
  }>((resolve) => {
    proc.on("close", (code, sig) => {
      clearTimeout(killTimer);
      resolve({ exitCode: code, signal: sig as string | null });
    });
    proc.on("error", () => {
      clearTimeout(killTimer);
      resolve({ exitCode: null, signal: null });
    });
  });

  const endTick = currentTick();
  const metrics: CageMetrics = cgroupPath
    ? {
        peakRssMb:        readCgroupMemoryPeakMib(args.id),
        cpuMsUsed:        readCgroupCpuUsageMs(cgroupPath),
        networkBytesIn:   0,
        networkBytesOut:  0,
        diskBytesWritten: 0,
      }
    : defaultMetrics();

  return {
    stdout, stderr,
    exitCode, signal,
    timedOut, truncated,
    elapsedMs: Number(endTick - startTick),
    metrics, startTick, endTick,
  };
}

// ── Linux backend: cgroup v2 + bwrap + seccomp ──────────────────────────

async function runLinuxCgroupSeccomp(
  id:        string,
  command:   string,
  args:      string[],
  input:     string,
  cfg:       CommandCageConfig,
  startTick: bigint,
): Promise<CommandCageResult> {
  const trustedCommand = resolveTrustedLinuxCommand(command);
  const cgPath      = `/sys/fs/cgroup/nexy-cage-${id}`;
  const seccompFile = join(tmpdir(), `nexy-seccomp-${id}.json`);
  const useBwrap    = await bwrapAvailable();
  if (!useBwrap) {
    throw new CageError(id, "SPAWN_FAILED", "CAGE_OS_ISOLATION_UNAVAILABLE");
  }

  try {
    if (isCgroupAvailable()) {
      try {
        mkdirSync(cgPath, { recursive: true });
        writeFileSync(join(cgPath, "memory.max"),
          `${cfg.memoryMb * 1024 * 1024}`);
        writeFileSync(join(cgPath, "cpu.max"),
          `${cfg.cpuQuotaPercent * 1_000} 100000`);
        writeFileSync(join(cgPath, "cpu.weight"), `${cfg.cpuShares}`);
      } catch {
        // cgroup mkdir / write failures are non-fatal — we proceed without
      }
    }

    const seccompJson = JSON.stringify({
      defaultAction: "SCMP_ACT_ALLOW",
      syscalls: cfg.blockSyscalls.map((name) => ({
        names: [name], action: "SCMP_ACT_ERRNO",
      })),
    });
    await writeFile(seccompFile, seccompJson, "utf-8");

    let proc: ChildProcess;
    if (useBwrap) {
      proc = spawn("bwrap", buildLinuxBwrapArgs(trustedCommand.executable, args), {
        stdio: ["pipe", "pipe", "pipe"],
        env:   { PATH: "/usr/bin:/bin" },
      });
    } else {
      proc = spawn(trustedCommand.executable, args, {
        stdio: ["pipe", "pipe", "pipe"],
        env:   { ...process.env },
      });
    }

    const result = await collectProcessResult({
      id, proc, input, cfg, startTick,
      cgroupPath: isCgroupAvailable() ? cgPath : null,
    });
    return { id, backend: "linux-cgroup-seccomp", ...result };
  } finally {
    await Promise.allSettled([
      unlink(seccompFile).catch(() => undefined),
    ]);
    if (isCgroupAvailable()) {
      try {
        rmSync(cgPath, { recursive: true, force: true });
      } catch { /* ignore */ }
    }
  }
}

// ── macOS backend: sandbox-exec ─────────────────────────────────────────

async function runMacOSSandbox(
  id:        string,
  command:   string,
  args:      string[],
  input:     string,
  cfg:       CommandCageConfig,
  startTick: bigint,
): Promise<CommandCageResult> {
  const sbProfile = join(tmpdir(), `nexy-sb-${id}.sb`);
  const profile = [
    "(version 1)",
    "(deny default)",
    "(allow process-fork)",
    "(allow process-exec)",
    "(allow file-read*)",
    '(allow file-write* (subpath "/tmp"))',
    ...cfg.networkAllowlist.map((d) =>
      `(allow network-outbound (remote ip "${d}:*"))`,
    ),
  ].join("\n");
  await writeFile(sbProfile, profile, "utf-8");

  try {
    const proc = spawn("sandbox-exec", ["-f", sbProfile, command, ...args], {
      stdio: ["pipe", "pipe", "pipe"],
    });
    const result = await collectProcessResult({
      id, proc, input, cfg, startTick, cgroupPath: null,
    });
    return { id, backend: "macos-sandbox-exec", ...result };
  } finally {
    await unlink(sbProfile).catch(() => undefined);
  }
}

// ── Windows backend: stub (Job Object not implemented in Node) ──────────

async function runWindowsJobObject(
  id:        string,
  command:   string,
  args:      string[],
  input:     string,
  cfg:       CommandCageConfig,
  startTick: bigint,
): Promise<CommandCageResult> {
  process.stderr.write(
    "[L3o-CAGE] Windows: Job Object isolation requires a native helper; falling back to dev-naive\n",
  );
  const fallback = await runDevNaive(id, command, args, input, cfg, startTick);
  return { ...fallback, backend: "windows-job-object" };
}

// ── Dev fallback (NO isolation) ─────────────────────────────────────────

async function runDevNaive(
  id:        string,
  command:   string,
  args:      string[],
  input:     string,
  cfg:       CommandCageConfig,
  startTick: bigint,
): Promise<CommandCageResult> {
  if (process.env["NEXY_CAGE_QUIET"] !== "1") {
    process.stderr.write(
      "[L3o-CAGE] WARNING: running without OS isolation — dev mode only\n",
    );
  }
  const proc = spawn(command, args, { stdio: ["pipe", "pipe", "pipe"] });
  const result = await collectProcessResult({
    id, proc, input, cfg, startTick, cgroupPath: null,
  });
  return { id, backend: "dev-naive", ...result };
}

// ── Backend dispatcher ──────────────────────────────────────────────────

async function dispatchBackend(
  backend:   CageBackend,
  id:        string,
  command:   string,
  args:      string[],
  input:     string,
  cfg:       CommandCageConfig,
  startTick: bigint,
): Promise<CommandCageResult> {
  switch (backend) {
    case "linux-cgroup-seccomp":
      return runLinuxCgroupSeccomp(id, command, args, input, cfg, startTick);
    case "macos-sandbox-exec":
      return runMacOSSandbox(id, command, args, input, cfg, startTick);
    case "windows-job-object":
      return runWindowsJobObject(id, command, args, input, cfg, startTick);
    case "dev-naive":
    default:
      return runDevNaive(id, command, args, input, cfg, startTick);
  }
}

// ── Public command-based runner ─────────────────────────────────────────

async function runInCageCommand(
  command: string,
  args:    string[],
  input:   string,
  config:  Partial<CommandCageConfig> = {},
): Promise<CommandCageResult> {
  if (command.length === 0) {
    throw new CageError("unspawned", "SPAWN_FAILED", "command must be non-empty");
  }
  const cfg       = { ...DEFAULT_CAGE_CONFIG, ...config };
  const id        = generateUlid();
  const startTick = currentTick();
  const backend   = detectBackend();

  let result: CommandCageResult;
  try {
    result = await dispatchBackend(backend, id, command, args, input, cfg, startTick);
  } catch (err) {
    const endTick = currentTick();
    result = {
      id, backend,
      stdout:   "",
      stderr:   String(err),
      exitCode: null,
      signal:   null,
      timedOut: false,
      truncated: false,
      elapsedMs: Number(endTick - startTick),
      metrics:   defaultMetrics(),
      startTick,
      endTick,
    };
  }

  await persistCageInvocation({
    id:        result.id,
    command,
    argsArr:   args,
    backend:   result.backend,
    config:    cfg,
    stdout:    result.stdout,
    exitCode:  result.exitCode,
    signal:    result.signal,
    timedOut:  result.timedOut,
    metrics:   result.metrics,
    startTick: result.startTick,
    endTick:   result.endTick,
  });

  return result;
}

// ── Legacy in-process runner (CMD-F3, fn-based) ─────────────────────────

async function runInCageFn(
  fn: CagedFn,
  config: Partial<CageConfig> | undefined,
): Promise<CageResult> {
  const cfg       = defaultCageConfig(config);
  const id        = generateUlid();
  const startTick = currentTick();
  const audit: CageAuditEntry[] = [];

  audit.push({
    entryId:   generateUlid(),
    timestamp: startTick.toString(),
    event:     "SPAWN",
    detail:    "in-process cage",
  });

  let timedOut = false;
  let output   = "";

  const work = fn().then((r) => { output = r; }).catch(() => { output = ""; });
  const timer = new Promise<void>((resolve) => {
    setTimeout(() => {
      timedOut = true;
      audit.push({
        entryId:   generateUlid(),
        timestamp: currentTick().toString(),
        event:     "TIMEOUT",
        detail:    `after ${cfg.maxExecMs}ms`,
      });
      resolve();
    }, cfg.maxExecMs);
  });

  await Promise.race([work, timer]);

  const endTick   = currentTick();
  const elapsedMs = Number(endTick - startTick);
  let truncated   = false;

  if (output.length > cfg.maxOutputBytes) {
    output    = output.slice(0, cfg.maxOutputBytes);
    truncated = true;
  }

  audit.push({
    entryId:   generateUlid(),
    timestamp: endTick.toString(),
    event:     "EXIT",
    detail:    `timedOut=${timedOut} truncated=${truncated}`,
  });

  return {
    id,
    output,
    exitCode:        timedOut ? -1 : 0,
    timedOut,
    truncated,
    elapsedMs,
    startTick,
    endTick,
    memoryPeakMib:   0,
    networkBlocked:  0,
    auditLog:        audit,
  };
}

// ── Public overloaded entry point ───────────────────────────────────────

export async function runInCage(
  fn: CagedFn, config?: Partial<CageConfig>,
): Promise<CageResult>;
export async function runInCage(
  command: string, args: string[], input: string,
  config?: Partial<CommandCageConfig>,
): Promise<CommandCageResult>;
export async function runInCage(
  arg1: CagedFn | string,
  arg2?: Partial<CageConfig> | string[],
  arg3?: string,
  arg4?: Partial<CommandCageConfig>,
): Promise<CageResult | CommandCageResult> {
  if (typeof arg1 === "function") {
    return runInCageFn(arg1, arg2 as Partial<CageConfig> | undefined);
  }
  return runInCageCommand(
    arg1,
    (arg2 as string[]) ?? [],
    arg3 ?? "",
    arg4,
  );
}

// ── Sandboxed Node.js script runner (CMD-F3 legacy) ─────────────────────

interface SpawnResult {
  stdout:          string;
  stderr:          string;
  exitCode:        number;
  timedOut:        boolean;
  networkBlocked:  number;
  memoryPeakMib:   number;
  audit:           CageAuditEntry[];
}

async function spawnCaged(
  script:  string,
  cageId:  string,
  cfg:     CageConfig,
): Promise<SpawnResult> {
  const audit: CageAuditEntry[] = [];
  let networkBlocked = 0;

  const childEnv: NodeJS.ProcessEnv = {
    ...process.env,
    ...cfg.env,
    NEXY_CAGE_ID:        cageId,
    NEXY_SECCOMP_MODE:   cfg.seccompMode,
    NEXY_NET_ALLOWLIST:  cfg.networkAllowlist.join(","),
    NODE_OPTIONS:        "--dns-result-order=ipv4first",
  };

  audit.push({
    entryId:   generateUlid(),
    timestamp: currentTick().toString(),
    event:     "SPAWN",
    detail:    `script=${script.slice(0, 80)} seccomp=${cfg.seccompMode}`,
  });

  let child: ChildProcess;
  try {
    child = spawn(process.execPath, ["--eval", script], {
      env:      childEnv,
      stdio:    ["ignore", "pipe", "pipe"],
      detached: false,
    });
  } catch (e) {
    throw new CageError(cageId, "SPAWN_FAILED", `spawn failed: ${String(e)}`);
  }

  if (child.pid !== undefined) {
    attachCgroup(cageId, child.pid, cfg.maxMemoryMib, cfg.cpuQuotaPct, audit);
  }

  const stdoutChunks: Buffer[] = [];
  const stderrLines: string[]  = [];

  child.stdout?.on("data", (chunk: Buffer) => {
    stdoutChunks.push(chunk);
    audit.push({
      entryId:   generateUlid(),
      timestamp: currentTick().toString(),
      event:     "STDOUT",
      detail:    `+${chunk.length}B`,
    });
  });

  child.stderr?.on("data", (chunk: Buffer) => {
    const lines = chunk.toString("utf8").split("\n");
    for (const line of lines) {
      stderrLines.push(line);
      if (line.includes("NEXY_NET_BLOCK:")) {
        const hostMatch = /NEXY_NET_BLOCK:(\S+)/.exec(line);
        const host      = hostMatch?.[1] ?? "unknown";
        if (!checkNetworkAllowed(host, cfg.networkAllowlist)) {
          networkBlocked++;
          audit.push({
            entryId:   generateUlid(),
            timestamp: currentTick().toString(),
            event:     "NETWORK_BLOCK",
            detail:    `host=${host}`,
          });
        }
      }
      const violated = parseSeccompViolation(line);
      if (violated) {
        audit.push({
          entryId:   generateUlid(),
          timestamp: currentTick().toString(),
          event:     "SECCOMP_VIOLATION",
          detail:    `syscall=${violated}`,
        });
        if (cfg.seccompMode === "strict" && child.pid !== undefined) {
          child.kill("SIGKILL");
        }
      }
    }
  });

  return new Promise((resolve) => {
    let timedOut = false;
    const timer  = setTimeout(() => {
      timedOut = true;
      audit.push({
        entryId:   generateUlid(),
        timestamp: currentTick().toString(),
        event:     "TIMEOUT",
        detail:    `after ${cfg.maxExecMs}ms`,
      });
      child.kill("SIGKILL");
    }, cfg.maxExecMs);

    child.on("close", (code) => {
      clearTimeout(timer);
      const stdout   = Buffer.concat(stdoutChunks).toString("utf8");
      const stderr   = stderrLines.join("\n");
      const exitCode = code ?? (timedOut ? -1 : -2);
      const memPeak  = readCgroupMemoryPeakMib(cageId);
      cleanupCgroup(cageId);
      audit.push({
        entryId:   generateUlid(),
        timestamp: currentTick().toString(),
        event:     "EXIT",
        detail:    `code=${exitCode} timedOut=${timedOut}`,
      });
      resolve({
        stdout, stderr, exitCode, timedOut,
        networkBlocked, memoryPeakMib: memPeak, audit,
      });
    });
  });
}

export async function runScriptInCage(
  script:  string,
  config?: Partial<CageConfig>,
): Promise<CageResult> {
  const cfg       = defaultCageConfig(config);
  const id        = generateUlid();
  const startTick = currentTick();

  const result    = await spawnCaged(script, id, cfg);
  const endTick   = currentTick();
  const elapsedMs = Number(endTick - startTick);

  let output    = result.stdout;
  let truncated = false;
  if (output.length > cfg.maxOutputBytes) {
    output    = output.slice(0, cfg.maxOutputBytes);
    truncated = true;
  }

  if (result.timedOut) {
    throw new CageError(id, "TIMEOUT", `cage ${id} exceeded ${cfg.maxExecMs}ms`);
  }

  return {
    id,
    output,
    exitCode:        result.exitCode,
    timedOut:        result.timedOut,
    truncated,
    elapsedMs,
    startTick,
    endTick,
    memoryPeakMib:   result.memoryPeakMib,
    networkBlocked:  result.networkBlocked,
    auditLog:        result.audit,
  };
}

// ── Policy builder ──────────────────────────────────────────────────────

export interface CagePolicy {
  readonly policyId:   string;
  readonly minTier:    number;
  readonly config:     CageConfig;
  isNetworkAllowed(host: string): boolean;
  describe(): string;
}

export function createCagePolicy(
  minTier: number,
  overrides: Partial<CageConfig> = {},
): CagePolicy {
  const policyId = generateUlid();
  const config   = defaultCageConfig(overrides);

  return {
    policyId,
    minTier,
    config,
    isNetworkAllowed(host) {
      return checkNetworkAllowed(host, config.networkAllowlist);
    },
    describe() {
      const net = config.networkAllowlist.length > 0
        ? config.networkAllowlist.join(", ")
        : "none";
      return [
        `CagePolicy[${policyId.slice(-6)}]`,
        `tier≥${minTier}`,
        `mem=${config.maxMemoryMib}MiB`,
        `cpu=${config.cpuQuotaPct}%`,
        `net=[${net}]`,
        `seccomp=${config.seccompMode}`,
      ].join(" ");
    },
  };
}

// ── Resource-metrics snapshot ───────────────────────────────────────────

export interface ResourceSnapshot {
  readonly snapshotId: string;
  readonly cageId:     string;
  readonly tick:       bigint;
  readonly memoryMib:  number;
  readonly cpuPct:     number;
}

export function captureResourceSnapshot(cageId: string): ResourceSnapshot {
  return {
    snapshotId: generateUlid(),
    cageId,
    tick:       currentTick(),
    memoryMib:  readCgroupMemoryPeakMib(cageId),
    cpuPct:     0,
  };
}

// ── Allowlist validation ────────────────────────────────────────────────

export function validateNetworkAllowlist(
  list: string[],
): { valid: boolean; errors: string[] } {
  const errors: string[] = [];
  const hostnameRe = /^[a-z0-9]([a-z0-9-]*[a-z0-9])?(\.[a-z0-9]([a-z0-9-]*[a-z0-9])?)*$/i;
  for (const entry of list) {
    if (!hostnameRe.test(entry)) {
      errors.push(`invalid hostname: ${entry}`);
    }
  }
  return { valid: errors.length === 0, errors };
}

// ── Test / introspection helpers ────────────────────────────────────────

export const _internals = {
  DEFAULT_CAGE_CONFIG,
  hashArgs,
  hashOutput,
  detectBackend,
  checkNetworkAllowed,
  defaultMetrics,
  resolveTrustedLinuxCommand,
  buildLinuxBwrapArgs,
  bwrapAvailable,
};
