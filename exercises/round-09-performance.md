# Round 9 — Caching and Performance

**Goal:** Make read paths fast and prove it under load.

## Requirements
- Cache-aside for medication and prescription reads with a TTL; invalidate on writes.
- Cache is opt-in per route (middleware), not global.
- Load test with `autocannon`: 100 RPS for 30 s on cached reads, zero errors, p99 under 100 ms.

## Constraints
- Start with an in-process LRU behind an interface (Redis only if multi-instance is required by the spec).
- Stampede protection: concurrent misses for one key trigger a single load (request coalescing).
- Bounded memory. Never cache per-user data under a shared key (no cross-user leaks).

## Acceptance
- Load test results recorded in the PR/round notes.
- Adversary cannot cause a stampede, stale-data leak, or unbounded cache growth.
