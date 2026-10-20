# Drill 03 — Bug: users stay blocked forever (time box: 20 min)

Support report: "Once a user hits the rate limit they are blocked permanently, even
after the window has passed."

`RateLimiter` is a fixed-window limiter: at most `limit` calls per `windowMs` per key.
Find the bug and fix it with the smallest sensible change.

Done = `npm test` is green.
