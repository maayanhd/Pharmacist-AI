# Pharmacist-AI

Rolling Node.js/TypeScript exercise. A pharmacy API that gets harder each round.
Round specs live in `exercises/`. Work one round at a time, in order.

## Rules for every agent (lead and teammates)

- TypeScript strict mode. No `any`. Explicit types on all exports.
- Express, in-memory `Map` storage only (no database).
- Secrets only via `process.env`, validated with Zod. Never hardcode or log them.
- Never log PII (emails, IPs, phone numbers).
- Run `npm run typecheck` before marking any task complete.
- Principles: SOLID, DRY, KISS, YAGNI. Do not build for rounds that haven't started.
- Teammates own distinct files. Never edit a file another teammate owns.
- Develop on branch `claude/agentic-code-quality-team-mzkRF`. Do not open PRs unless asked.

## Quality tooling

`python run_quality_check.py src/` runs the 4-agent SOLID/DRY/KISS/YAGNI review
(needs `ANTHROPIC_API_KEY`). Any principle scoring below 70 means the round is not done.

## Running a round

Enable teams (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, set in `.claude/settings.json`), then:

> Create an agent team for Round N. Spawn teammates `architect`, `builder`,
> `quality-reviewer`, `security-auditor`, `adversary` from the matching agent
> definitions. Require plan approval from the architect first. The builder starts
> only after the plan is approved. Wait for all teammates before concluding.
