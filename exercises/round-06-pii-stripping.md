# Round 6 — Aggregation and PII Stripping

**Goal:** `GET /patients/:id/summary` combines data from several services without leaking PII.

## Requirements
- Aggregate patient record, prescriptions and recent chat from separate service modules
  (simulate latency). Fetch concurrently with a concurrency cap and per-call timeout.
- If one source fails, return a partial result with a flagged gap, not a 500.
- Structured request logger.

## Constraints
- Strip or mask IPs, emails and phone numbers from every log line and every error message.
  Redaction lives in one place (DRY) and is applied at the logger, not at call sites.
- Client IP handling: do not store raw IPs; if needed for rate limiting use a salted hash.
- Respect `trust proxy` correctly so `X-Forwarded-For` cannot be spoofed.

## Acceptance
- Grepping all captured logs finds zero PII patterns, including inside error objects.
- Adversary cannot spoof client IP via headers.
