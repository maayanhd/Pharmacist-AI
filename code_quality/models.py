from dataclasses import dataclass, field
from typing import List, Literal


@dataclass
class Violation:
    severity: Literal["critical", "major", "minor"]
    location: str
    description: str
    suggestion: str


@dataclass
class AgentReport:
    agent: str
    principle: str
    score: int  # 0–100, higher = more compliant
    summary: str
    violations: List[Violation] = field(default_factory=list)

    @classmethod
    def from_tool_output(cls, agent: str, principle: str, data: dict) -> "AgentReport":
        violations = [Violation(**v) for v in data.get("violations", [])]
        return cls(
            agent=agent,
            principle=principle,
            score=data["score"],
            summary=data["summary"],
            violations=violations,
        )


@dataclass
class QualityReport:
    filename: str
    agent_reports: List[AgentReport]
    overall_score: int
    synthesis: str
    top_priorities: List[str]

    def print(self) -> None:
        width = 70
        print("\n" + "=" * width)
        print(f"  CODE QUALITY REPORT: {self.filename}")
        print("=" * width)
        print(f"\n  Overall Score: {self.overall_score}/100  {_score_badge(self.overall_score)}")
        print(f"\n  {self.synthesis}\n")

        if self.top_priorities:
            print("  TOP PRIORITIES:")
            for i, p in enumerate(self.top_priorities, 1):
                print(f"    {i}. {p}")

        print()
        for report in self.agent_reports:
            _print_agent_report(report)

        print("=" * width + "\n")


def _score_badge(score: int) -> str:
    if score >= 90:
        return "[EXCELLENT]"
    if score >= 75:
        return "[GOOD]"
    if score >= 60:
        return "[FAIR]"
    if score >= 40:
        return "[POOR]"
    return "[CRITICAL]"


def _print_agent_report(report: AgentReport) -> None:
    print(f"  {'─' * 66}")
    print(f"  {report.agent}  |  Score: {report.score}/100  {_score_badge(report.score)}")
    print(f"  {report.summary}")
    if report.violations:
        print()
        for v in sorted(report.violations, key=lambda x: {"critical": 0, "major": 1, "minor": 2}[x.severity]):
            icon = {"critical": "[!!!]", "major": "[!!]", "minor": "[!]"}[v.severity]
            print(f"    {icon} {v.location}")
            print(f"         {v.description}")
            print(f"         -> {v.suggestion}")
            print()
