#!/usr/bin/env bash
# Hook gate: exit 2 sends stderr back to the agent and blocks the action.
cd "$(dirname "$0")/.." || exit 0
[ -d node_modules ] || exit 0
if ! out=$(npm run --silent typecheck 2>&1); then
  echo "Type check failed. Fix before completing:" >&2
  echo "$out" | head -30 >&2
  exit 2
fi
