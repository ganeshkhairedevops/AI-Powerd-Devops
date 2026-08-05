"""
Tool Executor

Executes DevOps tools safely and returns
structured execution results.
"""

from __future__ import annotations

import time
import traceback
from typing import Any


class ToolExecutor:
    """Executes LangChain tools and captures their results."""

    def execute(
        self,
        tool: Any,
        command: str,
        category: str,
        tool_input: dict | None = None,
    ) -> dict:
        """
        Execute a LangChain tool.

        Args:
            tool: LangChain tool instance
            command: Display command (e.g. docker ps)
            category: Docker, Kubernetes, Linux, AWS...
            tool_input: Optional tool parameters

        Returns:
            dict:
            {
                success,
                tool,
                command,
                output,
                execution_time,
                error,
                traceback
            }
        """

        if tool_input is None:
            tool_input = {}

        start = time.perf_counter()

        try:
            result = tool.invoke(tool_input)

            execution_time = round(
                time.perf_counter() - start,
                3,
            )

            return {
                "success": True,
                "tool": category,
                "command": command,
                "output": str(result).strip(),
                "execution_time": execution_time,
                "error": None,
                "traceback": None,
            }

        except Exception as exc:

            execution_time = round(
                time.perf_counter() - start,
                3,
            )

            return {
                "success": False,
                "tool": category,
                "command": command,
                "output": "",
                "execution_time": execution_time,
                "error": str(exc),
                "traceback": traceback.format_exc(),
            }


# -------------------------------------------------------
# Singleton instance
# -------------------------------------------------------

executor = ToolExecutor()