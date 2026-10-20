# Drill 01 — Feature: paginate and search medications (time box: 45 min)

`GET /medications` currently returns every medication as a bare array.

Make it return:

```json
{ "items": [...], "total": 45, "page": 1, "limit": 20 }
```

- `?page` (default 1) and `?limit` (default 20, max 100, values above 100 are clamped).
- `?q` filters by name, case-insensitive substring. `total` counts filtered results.
- Invalid `page`/`limit` (non-integer, less than 1) → `400` with `{ "error": "..." }`.
- A page past the end → `200` with empty `items`.

Done = `npm test` is green.
