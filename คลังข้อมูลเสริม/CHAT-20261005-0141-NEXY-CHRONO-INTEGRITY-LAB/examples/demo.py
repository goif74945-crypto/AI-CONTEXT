from nexy_chrono_integrity import ChronoIntegrityKernel, FakeDualClock

NS = 1_000_000_000
clock = FakeDualClock(wall_ns=1_800_000_000 * NS, monotonic_ns=10 * NS)
kernel = ChronoIntegrityKernel()
envelope = kernel.issue(
    envelope_id="demo-otac-window",
    sample=clock.sample(),
    timeout_ns=300 * NS,
    max_wall_monotonic_skew_ns=2 * NS,
    policy_version="proposal-v1",
    purpose="example OTAC-style TTL",
)
clock.advance(60 * NS)
print(kernel.evaluate(envelope, clock.sample()))
