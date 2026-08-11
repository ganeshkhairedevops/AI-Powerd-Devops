"""
RAG Service

Coordinates document ingestion and retrieval.

Documents are isolated by conversation_id.
"""

from pathlib import Path

from llm import llm

from rag.loader import loader
from rag.splitter import splitter
from rag.vector_store import vector_store
from rag.retriever import retriever


class RAGService:

    def ingest_file(
        self,
        filepath: str,
        conversation_id: str,
    ):

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

    def retrieve_context(
        self,
        query: str,
        conversation_id: str,
    ) -> str:

        documents = retriever.retrieve(
            query=query,
            conversation_id=conversation_id,
        )

        if not documents:
            return ""

        context_parts = []

        for index, document in enumerate(
            documents,
            start=1,
        ):

            filename = document.metadata.get(
                "filename",
                "unknown",
            )

            context_parts.append(
                f"--- {filename} | "
                f"Document Chunk {index} ---\n"
                f"{document.page_content}"
            )

        return "\n\n".join(
            context_parts
        )

    def answer_from_context(
        self,
        question: str,
        context: str,
    ) -> str:

        prompt = f"""
You are a DevOps document analysis assistant.

Answer the user's question using ONLY the
provided document context.

DOCUMENT CONTEXT
----------------
{context}
----------------

USER QUESTION
----------------
{question}
----------------

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

            answer = response.content.strip()

        else:

            answer = str(
                response
            ).strip()

        return answer


rag_service = RAGService()