# Round 5 — Real-time Updates (WebSockets)

**Goal:** Push prescription status changes to the owning patient live.

## Requirements
- WebSocket endpoint authenticated with the access token (not in the URL query string).
- Each patient joins only their own room; queue worker events fan out to that room.
- Heartbeat ping/pong; dead connections are reaped.

## Constraints
- Share the existing HTTP server (`upgrade`), no second port.
- Per-connection message size limit and rate limit. Origin check on upgrade.
- No unnecessary abstraction over the `ws` library (KISS).
- Clean up on disconnect: no leaked listeners or room entries.

## Acceptance
- Patient A never receives patient B's events.
- Adversary cannot hold unbounded idle sockets or send oversized frames.
