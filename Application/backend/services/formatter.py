"""
Formatter Service

Uses the LLM to convert raw tool output into a
professional Markdown response.
"""

from __future__ import annotations

from llm import llm


class Formatter:
    """Formats raw DevOps command output using the LLM."""

    def format(
        self,
        question: str,
        tool: str,
        command: str,
        output: str,
    ) -> str:
        """
        Convert command output into a professional answer.

        Args:
            question: User question
            tool: Docker/Kubernetes/Linux/etc.
            command: Executed command
            output: Raw stdout

        Returns:
            Markdown formatted response
        """

        prompt = f"""
You are an expert DevOps Engineer.

The following command has already been executed.

Tool:
{tool}

Command:
{command}

User Question:
{question}

Raw Output:
{output}

Instructions:

- Never mention internal tools.
- Never mention LangChain.
- Never mention JSON.
- Never say "tool executed".
- Explain the output clearly.
- Use GitHub Markdown.
- Use tables when appropriate.
- Use bullet points.
- If there are problems, explain them.
- If everything is healthy, say so.
- End with a short summary.
"""

        response = llm.invoke(prompt)

        if hasattr(response, "content"):
            return response.content

        return str(response)


# ------------------------------------
# Singleton
# ------------------------------------

formatter = Formatter()