#!/usr/bin/env python3
"""
Code Quality Team — enforces SOLID, DRY, KISS, and YAGNI principles.

Usage:
    python run_quality_check.py <file_or_directory> [--no-recurse]

Examples:
    python run_quality_check.py src/main.py
    python run_quality_check.py src/
    python run_quality_check.py src/ --no-recurse

Requires:
    ANTHROPIC_API_KEY environment variable set.
"""

import asyncio
import sys
from pathlib import Path

from code_quality import CodeQualityOrchestrator


async def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}

    if not args:
        print(__doc__)
        return 1

    target = Path(args[0])
    if not target.exists():
        print(f"Error: path does not exist: {target}")
        return 1

    orchestrator = CodeQualityOrchestrator()

    if target.is_file():
        report = await orchestrator.analyze_file(target)
        report.print()
    else:
        recursive = "--no-recurse" not in flags
        reports = await orchestrator.analyze_directory(target, recursive=recursive)
        for report in reports:
            report.print()

    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
