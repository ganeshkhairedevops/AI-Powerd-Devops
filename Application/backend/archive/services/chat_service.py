"""
Chat Service

Main orchestration layer for the DevOps AI Agent.
"""

from __future__ import annotations

from services.tool_router import ToolRouter
from services.tool_executor import executor
from services.formatter import formatter
from services.response import ChatResponse


class ChatService:
    """Coordinates routing, execution, and formatting."""

    def __init__(self):
        self.router = ToolRouter()

    def ask(self, question: str) -> ChatResponse:
        """
        Process a user question.

        Flow:
        User Question
              ?
        Tool Router
              ?
        Tool Executor
              ?
        Formatter
              ?
        ChatResponse
        """

        route = self.router.route(question)

        if route is None:
            return ChatResponse(
                success=False,
                answer=(
                    "? Sorry, I couldn't determine which DevOps tool "
                    "should handle this request."
                ),
            )

        tool, command, category = route

        result = executor.execute(
            tool=tool,
            command=command,
            category=category,
        )

        if not result["success"]:
            return ChatResponse(
                success=False,
                answer=f"### Execution Failed\n\n{result['error']}",
                tool=category,
                command=command,
                raw_output=result["traceback"],
                execution_time=result["execution_time"],
            )

        answer = formatter.format(
            question=question,
            tool=category,
            command=command,
            output=result["output"],
        )

        return ChatResponse(
            success=True,
            answer=answer,
            tool=category,
            command=command,
            raw_output=result["output"],
            execution_time=result["execution_time"],
        )


# ---------------------------------------
# Singleton instance
# ---------------------------------------

chat_service = ChatService()