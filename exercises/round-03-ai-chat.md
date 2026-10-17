# Round 3 — AI Chat with SSE Streaming

**Goal:** Authenticated pharmacist-assistant chat that streams over Server-Sent Events.

## Requirements
- `POST /chat/stream` returns `text/event-stream`, forwarding Anthropic SDK stream deltas.
- Per-session conversation history in memory, keyed by user + session id.
- System prompt: pharmacy assistant that gives general information and defers to a pharmacist.

## Constraints
- Hard history budget: truncate oldest turns to stay within a token estimate. Never throw on long history.
- Client disconnect must abort the upstream request and free resources.
- One reusable SSE helper (DRY). API key from env only. Model id in config, not scattered.
- Mockable client behind an interface so tests need no network.

## Acceptance
- Streams incrementally, ends with a terminal event, survives mid-stream disconnect.
- Adversary cannot read another user's session or exhaust memory with huge messages.
