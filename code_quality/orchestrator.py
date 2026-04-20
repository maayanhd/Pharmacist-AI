import asyncio
import anthropic
from pathlib import Path
from typing import List

from .agents import SOLIDAgent, DRYAgent, KISSAgent, YAGNIAgent
from .models import AgentReport, QualityReport

MODEL = "claude-sonnet-4-6"

SUPPORTED_EXTENSIONS = {
    ".py", ".java", ".kt", ".js", ".ts", ".tsx", ".jsx",
    ".go", ".rs", ".cpp", ".c", ".cs", ".rb", ".swift",
}

SYNTHESIS_SYSTEM = """You are a senior engineering lead synthesizing code quality reports
from a team of specialized AI agents. You receive findings from four agents covering
SOLID, DRY, KISS, and YAGNI principles. Your job is to:

1. Write a 2–3 sentence executive summary of the overall code quality.
2. Identify the top 3–5 highest-priority actionable items (cross-cutting concerns first).
3. Be direct and specific — reference actual class/function names from the findings.
4. Do not repeat each agent's findings verbatim; synthesize across them."""


class CodeQualityOrchestrator:
    """Coordinates all code quality agents and synthesizes their findings."""

    def __init__(self):
        self._agents = [SOLIDAgent(), DRYAgent(), KISSAgent(), YAGNIAgent()]
        self._client = anthropic.AsyncAnthropic()

    async def analyze_file(self, filepath: Path) -> QualityReport:
        code = filepath.read_text(encoding="utf-8", errors="replace")
        filename = filepath.name

        # Run all agents in parallel
        reports: List[AgentReport] = await asyncio.gather(
            *[agent.analyze(code, filename) for agent in self._agents]
        )

        overall_score = round(sum(r.score for r in reports) / len(reports))
        synthesis, top_priorities = await self._synthesize(filename, reports, overall_score)

        return QualityReport(
            filename=filename,
            agent_reports=reports,
            overall_score=overall_score,
            synthesis=synthesis,
            top_priorities=top_priorities,
        )

    async def analyze_directory(self, dirpath: Path, recursive: bool = True) -> List[QualityReport]:
        pattern = "**/*" if recursive else "*"
        files = [
            f for f in dirpath.glob(pattern)
            if f.is_file() and f.suffix in SUPPORTED_EXTENSIONS
        ]
        if not files:
            print(f"No supported source files found in {dirpath}")
            return []

        print(f"Analyzing {len(files)} file(s) with 4-agent quality team...\n")
        return await asyncio.gather(*[self.analyze_file(f) for f in files])

    async def _synthesize(
        self, filename: str, reports: List[AgentReport], overall_score: int
    ) -> tuple[str, List[str]]:
        findings_text = "\n\n".join(
            f"=== {r.agent} (Score: {r.score}/100) ===\n"
            f"Summary: {r.summary}\n"
            + (
                "Violations:\n"
                + "\n".join(
                    f"  [{v.severity.upper()}] {v.location}: {v.description} -> {v.suggestion}"
                    for v in r.violations
                )
                if r.violations
                else "No violations."
            )
            for r in reports
        )

        response = await self._client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=[
                {
                    "type": "text",
                    "text": SYNTHESIS_SYSTEM,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            tools=[
                {
                    "name": "deliver_synthesis",
                    "description": "Deliver the synthesized engineering lead report.",
                    "input_schema": {
                        "type": "object",
                        "required": ["executive_summary", "top_priorities"],
                        "properties": {
                            "executive_summary": {
                                "type": "string",
                                "description": "2–3 sentence overall assessment.",
                            },
                            "top_priorities": {
                                "type": "array",
                                "maxItems": 5,
                                "description": "Top 3–5 highest-priority actionable items.",
                                "items": {"type": "string"},
                            },
                        },
                    },
                }
            ],
            tool_choice={"type": "tool", "name": "deliver_synthesis"},
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"File: `{filename}`  |  Overall Score: {overall_score}/100\n\n"
                        f"{findings_text}"
                    ),
                }
            ],
        )

        for block in response.content:
            if block.type == "tool_use":
                data = block.input
                return data["executive_summary"], data["top_priorities"]

        return "Analysis complete.", []
