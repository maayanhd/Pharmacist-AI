# Round 2 — Authentication and Authorization

**Goal:** JWT auth with refresh rotation and role-based access.

## Requirements
- `POST /auth/register`, `/auth/login`, `/auth/refresh`, `/auth/logout`.
- Passwords hashed (scrypt via `node:crypto` or bcrypt). Access token 15 min, refresh 7 days.
- Roles `pharmacist | patient | admin`. Patients only see their own prescriptions;
  only pharmacists/admins create medications.

## Constraints
- Refresh tokens rotate on every use. Reusing an old refresh token revokes the whole token family.
- Tokens never appear in URLs or logs. `JWT_SECRET` validated at startup with Zod.
- Constant-time comparison where secrets are compared.

## Acceptance
- Replay of a used refresh token fails and invalidates the family.
- Adversary cannot read another patient's data or escalate role.
