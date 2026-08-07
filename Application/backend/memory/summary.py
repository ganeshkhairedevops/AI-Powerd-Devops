"""
Conversation Summarizer
"""

from llm import llm


class ConversationSummary:

    def summarize(self, messages):

        prompt = f"""
Summarize this DevOps conversation.

Keep:

- Important commands
- Problems discussed
- Solutions
- Current context

Conversation:

{messages}
"""

        response = llm.invoke(prompt)

        return response.content


summary = ConversationSummary()