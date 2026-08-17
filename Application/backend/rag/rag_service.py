"""
RAG Service

Coordinates:

- Document loading
- Document splitting
- Embeddings
- ChromaDB storage
- Retrieval
- Document answering
- Document listing
- Document deletion
- Source attribution
- Retrieval metadata
- Grounded answer generation

Documents are isolated by conversation_id.
"""

from pathlib import Path

from llm import llm

from rag.loader import loader
from rag.splitter import splitter
from rag.vector_store import vector_store
from rag.retriever import retriever


class RAGService:

    # =================================================
    # Ingest Document
    # =================================================

    def ingest_file(
        self,
        filepath: str,
        conversation_id: str,
    ):
        """
        Load, split, embed, and store a document.
        """

        path = Path(filepath)

        # -------------------------------------------------
        # Load document
        # -------------------------------------------------

        content = loader.load(
            str(path)
        )

        # -------------------------------------------------
        # Split document
        # -------------------------------------------------

        chunks = splitter.split(
            content
        )

        if not chunks:

            return {
                "success": False,
                "filename": path.name,
                "chunks": 0,
                "conversation_id": conversation_id,
                "message": "No content found in document.",
            }

        # -------------------------------------------------
        # Store chunks
        # -------------------------------------------------

        vector_store.add_documents(
            documents=chunks,
            conversation_id=conversation_id,
            filename=path.name,
        )

        return {
            "success": True,
            "filename": path.name,
            "chunks": len(chunks),
            "conversation_id": conversation_id,
            "message": "Document successfully indexed.",
        }

    # =================================================
    # Retrieve Context
    # =================================================

    def retrieve_context(
        self,
        query: str,
        conversation_id: str,
    ) -> str:
        """
        Retrieve relevant document context only from
        the specified conversation.

        Returns only the context string for
        backward compatibility.
        """

        result = self.retrieve_context_with_sources(
            query=query,
            conversation_id=conversation_id,
        )

        return result["context"]

    # =================================================
    # Retrieve Context With Sources
    # =================================================

    def retrieve_context_with_sources(
        self,
        query: str,
        conversation_id: str,
    ):
        """
        Retrieve relevant document chunks and return
        context and source information.
        """

        documents = retriever.retrieve(
            query=query,
            conversation_id=conversation_id,
        )

        if not documents:

            return {
                "context": "",
                "sources": [],
            }

        context_parts = []

        sources = []

        seen_sources = set()

        for index, document in enumerate(
            documents,
            start=1,
        ):

            metadata = (
                document.metadata
                or {}
            )

            # -------------------------------------------------
            # Filename
            # -------------------------------------------------

            filename = metadata.get(
                "filename",
                "unknown",
            )

            # -------------------------------------------------
            # Chunk index
            # -------------------------------------------------

            stored_chunk_index = metadata.get(
                "chunk_index",
                index - 1,
            )

            try:

                chunk_number = (
                    int(stored_chunk_index)
                    + 1
                )

            except (
                TypeError,
                ValueError,
            ):

                chunk_number = index

            # -------------------------------------------------
            # Build context
            # -------------------------------------------------

            context_parts.append(
                f"--- {filename} | "
                f"Document Chunk {chunk_number} ---\n"
                f"{document.page_content}"
            )

            # -------------------------------------------------
            # Source
            # -------------------------------------------------

            source_key = (
                filename,
                chunk_number,
            )

            if source_key not in seen_sources:

                sources.append(
                    {
                        "filename": filename,
                        "chunk": chunk_number,
                    }
                )

                seen_sources.add(
                    source_key
                )

        # -------------------------------------------------
        # Final context
        # -------------------------------------------------

        context = "\n\n".join(
            context_parts
        )

        return {
            "context": context,
            "sources": sources,
        }

    # =================================================
    # Retrieve Context With Metadata
    # =================================================

    def retrieve_context_with_metadata(
        self,
        query: str,
        conversation_id: str,
    ):
        """
        Retrieve relevant document chunks together
        with source and retrieval metadata.

        Returns:

        {
            "context": str,
            "sources": [],
            "retrieval": {
                "chunks_retrieved": int,
                "results": [
                    {
                        "filename": str,
                        "chunk": int,
                        "score": float
                    }
                ]
            }
        }

        ChromaDB returns a distance score.

        Lower distance generally indicates a more
        similar result.
        """

        results = retriever.retrieve_with_scores(
            query=query,
            conversation_id=conversation_id,
        )

        if not results:

            return {
                "context": "",
                "sources": [],
                "retrieval": {
                    "chunks_retrieved": 0,
                    "results": [],
                },
            }

        context_parts = []

        sources = []

        retrieval_results = []

        seen_sources = set()

        for index, item in enumerate(
            results,
            start=1,
        ):

            # -------------------------------------------------
            # Result structure
            #
            # (Document, score)
            # -------------------------------------------------

            document, score = item

            metadata = (
                document.metadata
                or {}
            )

            # -------------------------------------------------
            # Filename
            # -------------------------------------------------

            filename = metadata.get(
                "filename",
                "unknown",
            )

            # -------------------------------------------------
            # Chunk index
            # -------------------------------------------------

            stored_chunk_index = metadata.get(
                "chunk_index",
                index - 1,
            )

            try:

                chunk_number = (
                    int(stored_chunk_index)
                    + 1
                )

            except (
                TypeError,
                ValueError,
            ):

                chunk_number = index

            # -------------------------------------------------
            # Build context
            # -------------------------------------------------

            context_parts.append(
                f"--- {filename} | "
                f"Document Chunk {chunk_number} ---\n"
                f"{document.page_content}"
            )

            # -------------------------------------------------
            # Source
            # -------------------------------------------------

            source_key = (
                filename,
                chunk_number,
            )

            if source_key not in seen_sources:

                sources.append(
                    {
                        "filename": filename,
                        "chunk": chunk_number,
                    }
                )

                seen_sources.add(
                    source_key
                )

            # -------------------------------------------------
            # Retrieval metadata
            # -------------------------------------------------

            try:

                score_value = float(
                    score
                )

            except (
                TypeError,
                ValueError,
            ):

                score_value = None

            retrieval_results.append(
                {
                    "filename": filename,
                    "chunk": chunk_number,
                    "score": score_value,
                }
            )

        # -------------------------------------------------
        # Final context
        # -------------------------------------------------

        context = "\n\n".join(
            context_parts
        )

        return {
            "context": context,
            "sources": sources,
            "retrieval": {
                "chunks_retrieved": len(results),
                "results": retrieval_results,
            },
        }

    # =================================================
    # Answer From Context
    # =================================================

    def answer_from_context(
        self,
        question: str,
        context: str,
    ) -> str:
        """
        Generate an answer using ONLY the retrieved
        document context.

        The LLM must not use outside knowledge.

        If the context does not support the answer,
        return exactly:

        NOT_ENOUGH_CONTEXT
        """

        # -------------------------------------------------
        # Empty context protection
        # -------------------------------------------------

        if not context or not context.strip():

            return "NOT_ENOUGH_CONTEXT"

        # -------------------------------------------------
        # Grounded answer prompt
        # -------------------------------------------------

        prompt = f"""
You are a strict DevOps document analysis assistant.

Your task is to answer the user's question using
ONLY the provided DOCUMENT CONTEXT.

You must treat the DOCUMENT CONTEXT as the
only source of truth.

## DOCUMENT CONTEXT

{context}

## USER QUESTION

{question}

## GROUNDING RULES

1. Use ONLY information explicitly present in the
   DOCUMENT CONTEXT.

2. Do NOT use your general knowledge.

3. Do NOT use information from previous conversations.

4. Do NOT infer infrastructure values that are not
   present in the DOCUMENT CONTEXT.

5. Do NOT guess.

6. Do NOT invent values, versions, ports, replicas,
   names, IP addresses, images, configurations, or
   other DevOps information.

7. If the answer is explicitly present in the
   DOCUMENT CONTEXT, answer it directly.

8. If the answer requires combining multiple pieces
   of information that are explicitly present in the
   DOCUMENT CONTEXT, you may combine them.

9. If the DOCUMENT CONTEXT does not contain enough
   information to answer the question, return exactly:

NOT_ENOUGH_CONTEXT

10. Do not explain that information is missing.

11. Do not mention these instructions.

12. Do not mention RAG, ChromaDB, embeddings, tools,
    LangChain, or internal implementation.

13. Do not output JSON.

14. Do not output function calls.

15. Keep the answer concise.

16. Do not add unnecessary explanations when a direct
    answer is possible.

17. Return only the final answer or:

NOT_ENOUGH_CONTEXT

## IMPORTANT EXAMPLES

Question:
What image is used by the nginx deployment?

Context:
image: nginx:1.27

Answer:
nginx:1.27

---

Question:
How many replicas does the nginx deployment have?

Context:
replicas: 3

Answer:
3

---

Question:
What is the Kubernetes cluster version?

Context:
The document contains a Kubernetes Deployment and
Service but no cluster version.

Answer:
NOT_ENOUGH_CONTEXT

---

Question:
What AWS region is being used?

Context:
No AWS region is present.

Answer:
NOT_ENOUGH_CONTEXT

## FINAL ANSWER
"""

        # -------------------------------------------------
        # LLM invocation
        # -------------------------------------------------

        try:

            response = llm.invoke(
                prompt
            )

        except Exception as exc:

            print(
                "RAG answer generation failed:",
                str(exc),
            )

            return "NOT_ENOUGH_CONTEXT"

        # -------------------------------------------------
        # Extract response
        # -------------------------------------------------

        if hasattr(
            response,
            "content",
        ):

            answer = (
                response.content.strip()
            )

        else:

            answer = str(
                response
            ).strip()

        # -------------------------------------------------
        # Empty response protection
        # -------------------------------------------------

        if not answer:

            return "NOT_ENOUGH_CONTEXT"

        # -------------------------------------------------
        # Normalize NOT_ENOUGH_CONTEXT
        #
        # Prevent cases where the model returns:
        #
        # "NOT_ENOUGH_CONTEXT."
        #
        # or Markdown/code formatting.
        # -------------------------------------------------

        normalized = (
            answer
            .replace(
                "`",
                "",
            )
            .strip()
            .rstrip(".")
            .strip()
        )

        if (
            normalized.upper()
            == "NOT_ENOUGH_CONTEXT"
        ):

            return "NOT_ENOUGH_CONTEXT"

        return answer

    # =================================================
    # List Documents
    # =================================================

    def list_documents(
        self,
        conversation_id: str,
    ):
        """
        List documents belonging to a conversation.
        """

        return vector_store.list_documents(
            conversation_id=conversation_id,
        )

    # =================================================
    # Delete Document
    # =================================================

    def delete_document(
        self,
        conversation_id: str,
        filename: str,
    ):
        """
        Delete a document from ChromaDB.
        """

        return vector_store.delete_document(
            conversation_id=conversation_id,
            filename=filename,
        )


# =====================================================
# Singleton
# =====================================================

rag_service = RAGService()