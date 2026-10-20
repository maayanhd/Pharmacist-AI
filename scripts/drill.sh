#!/usr/bin/env bash
# Timed interview drills. Usage: drill.sh list | start <drill> | finish
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DIR="${DRILL_DIR:-$HOME/drill-workspace}"

case "${1:-}" in
  list)
    for d in "$ROOT"/drills/*/; do basename "$d"; done
    ;;
  start)
    name="${2:?usage: drill.sh start <drill>}"
    src="$ROOT/drills/$name"
    [ -d "$src" ] || { echo "No such drill: $name (try: drill.sh list)" >&2; exit 1; }
    if [ -e "$DIR" ] && [ ! -f "$DIR/.started" ]; then
      echo "Refusing to overwrite $DIR (not a drill workspace)." >&2
      exit 1
    fi
    [ -d "$ROOT/node_modules" ] || (cd "$ROOT" && npm install --silent)
    rm -rf "$DIR"
    mkdir -p "$DIR"
    cp -r "$src/src" "$src/test" "$src/README.md" "$DIR/"
    cp "$ROOT/drills/INTERVIEW_CLAUDE.md" "$DIR/CLAUDE.md"
    ln -s "$ROOT/node_modules" "$DIR/node_modules"
    printf '{"private":true,"scripts":{"test":"node --import tsx --test test/*.test.ts"}}\n' > "$DIR/package.json"
    date +%s > "$DIR/.started"
    cat "$DIR/README.md"
    echo
    echo "Workspace: $DIR"
    echo "Timer started. Run: cd $DIR && claude"
    ;;
  finish)
    [ -f "$DIR/.started" ] || { echo "No active drill in $DIR" >&2; exit 1; }
    elapsed=$(( $(date +%s) - $(cat "$DIR/.started") ))
    printf 'Elapsed: %dm%02ds\n\n' $((elapsed / 60)) $((elapsed % 60))
    cd "$DIR" && npm test
    ;;
  *)
    echo "usage: drill.sh list | start <drill> | finish" >&2
    exit 1
    ;;
esac
