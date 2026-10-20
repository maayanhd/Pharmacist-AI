# Drill 02 — Bug: duplicate fills double-decrement stock (time box: 30 min)

Support report: "When the pharmacy app retries a request with the same idempotency
key, stock sometimes drops twice for one prescription."

`FillService.fill(key, medicationId, qty)` is meant to be idempotent per `key`.
Find the bug and fix it. Don't change the `Inventory` interface.

Also make sure a failed fill (e.g. out of stock) does not poison the key: a later retry
with the same key must be allowed to succeed.

Done = `npm test` is green.
