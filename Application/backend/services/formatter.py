"""
Formatter Service

Creates professional Markdown responses from parsed DevOps data.
"""

from __future__ import annotations

import json

from llm import llm


class Formatter:

    def _markdown_table(self, data):

        if not isinstance(data, list):
            return None

        if len(data) == 0:
            return None

        headers = list(data[0].keys())

        table = []

        table.append("| " + " | ".join(headers) + " |")
        table.append("|" + "|".join(["---"] * len(headers)) + "|")

        for row in data:
            table.append(
                "| "
                + " | ".join(str(row.get(h, "")) for h in headers)
                + " |"
            )

        return "\n".join(table)

    def format(
        self,
        question: str,
        tool: str,
        command: str,
        output,
    ):

        markdown_table = self._markdown_table(output)

        structured_output = json.dumps(
            output,
            indent=2,
        )

        prompt = f"""
You are a Senior DevOps Engineer.

The command has ALREADY been executed.

User Question:
{question}

Tool:
{tool}

Command:
{command}

Structured Data:

{structured_output}

Instructions:

Return ONLY valid GitHub Markdown.

DO NOT explain obvious column names.

DO NOT output:

- text
- Copy
- json
- Tool Call

Write your answer in this format:

# Result

Brief summary.

# Analysis

Health checks

Problems

Warnings

# Recommendations

Actionable next steps.

Keep the answer concise.
"""

        response = llm.invoke(prompt)

        analysis = (
            response.content
            if hasattr(response, "content")
            else str(response)
        )

        if markdown_table:

            return f"""
# {tool}

## Data

{markdown_table}

{analysis}
"""

        return analysis


formatter = Formatter()