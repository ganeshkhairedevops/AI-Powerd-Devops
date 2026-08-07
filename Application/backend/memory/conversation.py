"""
Conversation Manager

Maintains multiple chat sessions.
"""

from memory.chat_memory import ChatMemory


class ConversationManager:

    def __init__(self):

        self.conversations = {}

    def get_memory(self, conversation_id: str):

        if conversation_id not in self.conversations:

            self.conversations[conversation_id] = ChatMemory()

        return self.conversations[conversation_id]

    def delete(self, conversation_id: str):

        self.conversations.pop(conversation_id, None)

    def clear_all(self):

        self.conversations.clear()


conversation_manager = ConversationManager()