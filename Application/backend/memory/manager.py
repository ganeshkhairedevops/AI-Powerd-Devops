"""
Conversation Memory Manager
"""

from collections import defaultdict
from memory.models import Message


class MemoryManager:

    def __init__(self):
        self._memory = defaultdict(list)

    def add_message(self, conversation_id: str, role: str, content: str):

        self._memory[conversation_id].append(
            Message(
                role=role,
                content=content,
            )
        )

    def get_messages(self, conversation_id: str):

        return self._memory.get(conversation_id, [])

    def clear(self, conversation_id: str):

        self._memory.pop(conversation_id, None)


memory = MemoryManager()