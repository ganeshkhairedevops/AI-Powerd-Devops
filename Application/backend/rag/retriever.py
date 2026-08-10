"""
Retriever

Retrieves relevant document chunks
from ChromaDB.
"""

from config import TOP_K_RESULTS
from rag.vector_store import vector_store


class Retriever:

    def retrieve(
        self,
        query: str,
    ):

        results = vector_store.search(
            query=query,
            k=TOP_K_RESULTS,
        )

        return results


retriever = Retriever()