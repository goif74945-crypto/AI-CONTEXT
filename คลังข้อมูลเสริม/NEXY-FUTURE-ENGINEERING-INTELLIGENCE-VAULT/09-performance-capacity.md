# Performance & Capacity
Decompose latency across client, edge, API, application, database/cache, external dependencies, queue/worker. Track p50/p95/p99.
Capacity: peak RPS, concurrency, payload, queries/request, cache ratio, external calls, CPU/memory, queue rates, storage growth, retention.
Profiles: steady, peak, spike, soak, dependency slowdown, cold cache, post-deploy warmup, queue recovery.
Optimization must not weaken authorization, validation, durability, consistency, or evidence integrity.
Every buffer/queue needs bounded capacity or explicit overload behavior.
