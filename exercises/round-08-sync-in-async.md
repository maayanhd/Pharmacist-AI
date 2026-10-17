# Round 8 — Slow Synchronous Dependencies

**Goal:** Integrate a flaky, slow "Drug Interaction" HTTP API without letting it hurt the service.

## Requirements
- Include a local mock service that randomly returns 500s and adds multi-second delays.
- `POST /prescriptions/check-interactions` calls it with a timeout, retries with backoff and jitter,
  and trips a circuit breaker after repeated failures (open, half-open, closed).
- When open, return a clear degraded response instead of waiting.

## Constraints
- Timeout via `AbortController`. Retries only for idempotent/safe failures.
- Open/Closed: adding a second external provider must not modify existing provider code.
- Implement the breaker yourself or with a small library; justify the choice.
- Bulkhead: limit concurrent outbound calls.

## Acceptance
- With the mock failing, the endpoint still answers fast (target p99 under 200 ms when open).
- Adversary cannot cause request pile-up or retry storms.
