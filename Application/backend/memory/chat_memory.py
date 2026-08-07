"""
Conversation Memory
"""

from collections import deque


class ChatMemory:

    def __init__(self, max_messages=20):

        self.messages = deque(maxlen=max_messages)

    def add_user_message(self, text):

        self.messages.append(
            {
                "role": "user",
                "content": text,
            }
        )

    def add_ai_message(self, text):

        self.messages.append(
            {
                "role": "assistant",
                "content": text,
            }
        )

    def history(self):

        return list(self.messages)

    def clear(self):

        self.messages.clear()


memory = ChatMemory()