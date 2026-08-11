"""
Retriever

Retrieves relevant document chunks from ChromaDB
for a specific conversation.
"""

from config import TOP_K_RESULTS
from rag.vector_store import vector_store


class Retriever:

    def retrieve(
        self,
        query: str,
        conversation_id: str,
    ):

        results = vector_store.search(
            query=query,
            conversation_id=conversation_id,
            k=TOP_K_RESULTS,
        )

        return results


retriever = Retriever()