# Interview drills: implement a feature, fix a bug

Timed practice for the "no LeetCode, work in a real codebase with an AI assistant" format.

```bash
scripts/drill.sh list
scripts/drill.sh start 02-bug-double-fill   # copies the seed to ~/drill-workspace, starts the clock
cd ~/drill-workspace && claude              # picks up the interview-mode CLAUDE.md
scripts/drill.sh finish                     # elapsed time + test results
```

Set `DRILL_DIR` to use a different workspace. Don't peek at solutions; there are none in the repo.

## Rules of the practice

1. Keep a second Claude session on a side task (read the next file, draft test cases) so you are never watching a spinner.
2. No spec-driven workflow. Plan mode, one short plan, then code.
3. Interview-mode line lives in `drills/INTERVIEW_CLAUDE.md`. Reading slop is the time sink.
4. Doubt out loud. Say what you expect the code to do before you read it, and what looks wrong.
5. Mid reasoning tier, not the heaviest. Latency costs more than it buys here.

## After each drill

Debrief for five minutes: what did you ask Claude that you should have read yourself, which of its claims did you verify, and where did the time go? Drill 02 has a trap (the obvious fix poisons the key on failure); note whether you caught it before the tests did.
