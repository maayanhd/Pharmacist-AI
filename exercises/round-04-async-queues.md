# Round 4 — Async Queues

**Goal:** Move prescription filling and notifications off the request path.

## Requirements
- `POST /prescriptions/:id/fill` returns `202` with a job id; a worker fills it asynchronously.
- Notification queue emits a "prescription filled" event (logged, not sent).
- `GET /jobs/:id` reports status.
- Failed jobs retry with exponential backoff, then land in a dead-letter list.

## Constraints
- Start with an in-process queue behind an interface (BullMQ + Redis can implement it later;
  do not add Redis unless the spec needs it).
- Idempotency: submitting the same fill twice yields one fill (idempotency key / job id).
- Bounded concurrency and bounded queue size; reject with `429/503` when full.
- Graceful shutdown drains in-flight jobs.

## Acceptance
- Duplicate and concurrent submissions fill exactly once.
- Adversary cannot flood the queue into unbounded memory or poison the worker with bad payloads.
