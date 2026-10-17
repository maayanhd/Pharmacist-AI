# Round 1 — Basic REST

**Goal:** CRUD for Users, Medications, Prescriptions on Express with in-memory Maps.

## Requirements
- `/users`, `/medications`, `/prescriptions`: list, get, create, update, delete.
- Zod schemas validate every request body and param. Responses are typed.
- Central error middleware: 400 validation, 404 missing, 500 unknown (no stack leaks).
- Prescriptions must reference an existing user and medication.

## Constraints
- IDs are UUIDs (`crypto.randomUUID`), never counters.
- No `any`. One router and one service per resource (SRP).
- Storage hidden behind a small repository interface per resource (DIP).

## Acceptance
- `npm run typecheck` clean. Invalid input never reaches a service.
- Adversary cannot cause a 500 with malformed input.
