# NEXY.AI Integration Proposal

**Classification:** AI-PROPOSED / NON-CANONICAL / NOT INTEGRATED

## Read-only implementation observations
At the exact read-only implementation revision observed during this mission, NEXY contains a BullMQ `pipeline` queue, an explicit runtime concurrency cap, queue states, stale-job handling, durable cancellation paths, and a worker that resolves durable runtime configuration before consumption. These observations make a queue-capacity sidecar a plausible future adapter target; they do not authorize code changes or establish that current runtime traffic satisfies a token-bucket model.

## Proposed adapter boundary
A future adapter could receive only explicit, versioned contracts:

```text
QueueFlowContract {
  burstQ64,
  arrivalRateQ64,
  serviceRateQ64,
  serviceLatencyQ64,
  optionalMaxBacklogQ64,
  optionalMaxDelayQ64,
  authorityId,
  contractRevision
}
```

The adapter would return one advisory certificate and never enqueue/dequeue jobs itself. NEXY LAW/ECL would decide whether the certificate is relevant and authorized.

## Candidate uses
- pre-admission check for bounded pipeline load;
- explicit memory/backlog budget proof before raising queue concurrency;
- deadline feasibility check across multiple declared stages;
- offline configuration review comparing a proposed arrival envelope to declared service capacity;
- generation of a stricter producer-side shaping proposal without changing service-side law.

## Required proof before adoption
1. identify the authoritative unit and time base for every contract field;
2. prove how actual BullMQ/workload behavior maps to the token-bucket and rate-latency assumptions;
3. prove scheduler/queue discipline compatibility and account for packet/job granularity;
4. bind contracts to current runtime-config revision and exact implementation revision;
5. add NEXY-native Q64.64 adapter tests and FREEZE propagation tests;
6. run realistic queue load tests and measure whether certified bounds are conservative;
7. security/DoS review for adversarial contract sizes and configuration churn;
8. formal promotion decision before any Canon or release-gate role.

Until those exist, this project is a tested standalone prototype only.
