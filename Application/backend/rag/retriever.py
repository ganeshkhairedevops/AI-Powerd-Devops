"""
Retriever

Retrieves relevant document chunks from ChromaDB
for a specific conversation.

Supports:

- Normal retrieval
- Retrieval with scores
- Absolute score filtering
- Relative relevance filtering
- Maximum context chunk limits
"""

from config import (
    TOP_K_RESULTS,
    RAG_SCORE_THRESHOLD,
    MAX_RAG_CONTEXT_CHUNKS,
)

from rag.vector_store import vector_store


class Retriever:

    # =================================================
    # Retrieval Configuration
    # =================================================

    # Maximum allowed distance difference from the
    # strongest retrieved result.
    #
    # Example:
    #
    # Best score = 0.65
    # Relative threshold = 0.10
    #
    # Maximum accepted score = 0.75
    #
    RELATIVE_SCORE_THRESHOLD = 0.10

    # =================================================
    # Normal Retrieval
    # =================================================

    def retrieve(
        self,
        query: str,
        conversation_id: str,
    ):
        """
        Retrieve relevant documents only from
        the specified conversation.

        Returns:
            List of LangChain Document objects.
        """

        results = self.retrieve_with_scores(
            query=query,
            conversation_id=conversation_id,
        )

        return [
            document
            for document, score in results
        ]

    # =================================================
    # Retrieve With Scores
    # =================================================

    def retrieve_with_scores(
        self,
        query: str,
        conversation_id: str,
    ):
        """
        Retrieve documents together with their
        ChromaDB distance scores.

        Two filtering stages are applied:

        1. Absolute score threshold
        2. Relative score threshold

        Lower distance generally means
        better similarity.
        """

        results = vector_store.search_with_scores(
            query=query,
            conversation_id=conversation_id,
            k=TOP_K_RESULTS,
        )

        if not results:
            return []

        # -------------------------------------------------
        # Convert and validate scores
        # -------------------------------------------------

        valid_results = []

        for document, score in results:

            try:

                score_value = float(score)

            except (
                TypeError,
                ValueError,
            ):

                continue

            valid_results.append(
                (
                    document,
                    score_value,
                )
            )

        if not valid_results:
            return []

        # -------------------------------------------------
        # Absolute score filtering
        # -------------------------------------------------

        absolute_results = [
            (
                document,
                score,
            )
            for document, score
            in valid_results
            if score <= RAG_SCORE_THRESHOLD
        ]

        if not absolute_results:
            return []

        # -------------------------------------------------
        # Find strongest result
        # -------------------------------------------------

        best_score = min(
            score
            for document, score
            in absolute_results
        )

        # -------------------------------------------------
        # Relative score filtering
        # -------------------------------------------------

        relative_results = []

        for document, score in absolute_results:

            score_difference = (
                score - best_score
            )

            if (
                score_difference
                <= self.RELATIVE_SCORE_THRESHOLD
            ):

                relative_results.append(
                    (
                        document,
                        score,
                    )
                )

        # -------------------------------------------------
        # Always keep strongest result
        #
        # This protects against floating-point
        # comparison edge cases.
        # -------------------------------------------------

        if not relative_results:

            best_result = min(
                absolute_results,
                key=lambda item: item[1],
            )

            relative_results = [
                best_result
            ]

        # -------------------------------------------------
        # Limit context size
        # -------------------------------------------------

        return relative_results[
            :MAX_RAG_CONTEXT_CHUNKS
        ]


# =====================================================
# Singleton
# =====================================================

retriever = Retriever()