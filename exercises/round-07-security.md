# Round 7 — Security Hardening

**Goal:** Close the OWASP Top 10 gaps across the whole app.

## Requirements
- `helmet` with a strict CSP; CORS allowlist from env (never `*` with credentials).
- Rate limits: global per-IP, tighter on `/auth/*` and `/chat/*`, with `Retry-After`.
- Body size limits, content-type enforcement, strict Zod validation everywhere (reject unknown keys).
- Login throttling and uniform error messages (no user enumeration).
- Dependency audit (`npm audit`) reviewed; no known high/critical issues.

## Constraints
- Security config centralized in one module. Fail closed on missing/invalid config.
- Prototype pollution, ReDoS and path traversal inputs must be handled.
- Nothing sensitive in error responses.

## Acceptance
- Security auditor signs off on each Top 10 category with file references.
- Adversary fails to: enumerate users, bypass limits, inject via headers/body, or crash the server.
