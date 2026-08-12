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

        This method is kept compatible with the
        existing application and returns only the
        context string.
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
        both the context and source information.

        Returns:

        {
            "context": str,
            "sources": [
                {
                    "filename": str,
                    "chunk": int
                }
            ]
        }
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
            #
            # vector_store stores chunk_index starting
            # from 0, so convert it to a human-readable
            # chunk number starting from 1.
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
            #
            # Avoid duplicate source entries if multiple
            # retrieved results point to the same chunk.
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
    # Answer From Context
    # =================================================

    def answer_from_context(
        self,
        question: str,
        context: str,
    ) -> str:
        """
        Answer the question using only
        retrieved document context.
        """

        prompt = f"""
You are a DevOps document analysis assistant.

Answer the user's question using ONLY the
provided document context.

## DOCUMENT CONTEXT

{context}

## USER QUESTION

{question}

Rules:

1. Use only information present in the document context.

2. Do not use external knowledge.

3. Do not execute or suggest DevOps tool calls.

4. Do not output JSON.

5. Do not output function calls.

6. If the document contains the answer, answer clearly
   and directly.

7. If the document does not contain enough information,
   respond with exactly:

NOT_ENOUGH_CONTEXT

8. Keep the answer concise.

Answer:
"""

        response = llm.invoke(
            prompt
        )

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