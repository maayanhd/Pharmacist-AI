import anthropic
from abc import ABC, abstractmethod
from ..models import AgentReport

MODEL = "claude-sonnet-4-6"

REPORT_TOOL = {
    "name": "report_findings",
    "description": "Report structured code quality findings for the analyzed code.",
    "input_schema": {
        "type": "object",
        "required": ["violations", "score", "summary"],
        "properties": {
            "violations": {
                "type": "array",
                "description": "List of principle violations found in the code.",
                "items": {
                    "type": "object",
                    "required": ["severity", "location", "description", "suggestion"],
                    "properties": {
                        "severity": {
                            "type": "string",
                            "enum": ["critical", "major", "minor"],
                        },
                        "location": {
                            "type": "string",
                            "description": "Class name, function name, or brief location descriptor.",
                        },
                        "description": {
                            "type": "string",
                            "description": "Clear explanation of the violation.",
                        },
                        "suggestion": {
                            "type": "string",
                            "description": "Concrete, actionable refactoring suggestion.",
                        },
                    },
                },
            },
            "score": {
                "type": "integer",
                "minimum": 0,
                "maximum": 100,
                "description": "Compliance score where 100 means perfect adherence to the principle.",
            },
            "summary": {
                "type": "string",
                "description": "One or two sentence summary of the overall compliance.",
            },
        },
    },
}


class BaseAgent(ABC):
    """Base class for all code quality agents."""

    def __init__(self, name: str, principle: str):
        self.name = name
        self.principle = principle
        self._client = anthropic.AsyncAnthropic()

    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """Specialized system prompt for this agent, will be cached."""

    async def analyze(self, code: str, filename: str) -> AgentReport:
        response = await self._client.messages.create(
            model=MODEL,
            max_tokens=4096,
            system=[
                {
                    "type": "text",
                    "text": self.system_prompt,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            tools=[REPORT_TOOL],
            tool_choice={"type": "tool", "name": "report_findings"},
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Analyze the following code from `{filename}` "
                        f"for {self.principle} violations.\n\n"
                        f"```\n{code}\n```"
                    ),
                }
            ],
        )

        for block in response.content:
            if block.type == "tool_use":
                return AgentReport.from_tool_output(self.name, self.principle, block.input)

        return AgentReport(
            agent=self.name,
            principle=self.principle,
            score=100,
            summary="No violations detected.",
            violations=[],
        )
