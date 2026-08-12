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
        """
        Retrieve relevant documents only from
        the specified conversation.
        """

        results = vector_store.search(
            query=query,
            conversation_id=conversation_id,
            k=TOP_K_RESULTS,
        )

        return results

    # =================================================
    # Retrieve With Scores
    # =================================================

    def retrieve_with_scores(
        self,
        query: str,
        conversation_id: str,
    ):
        """
        Retrieve relevant documents together
        with their similarity scores.
        """

        results = vector_store.search_with_scores(
            query=query,
            conversation_id=conversation_id,
            k=TOP_K_RESULTS,
        )

        return results


# =====================================================
# Singleton
# =====================================================

retriever = Retriever()