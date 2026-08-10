"""
RAG Service

Coordinates document ingestion and retrieval.
"""

from pathlib import Path

from rag.loader import loader
from rag.splitter import splitter
from rag.vector_store import vector_store
from rag.retriever import retriever


class RAGService:

    def ingest_file(self, filepath: str):

        path = Path(filepath)

        # Load document
        content = loader.load(str(path))

        # Split document
        chunks = splitter.split(content)

        if not chunks:
            return {
                "success": False,
                "filename": path.name,
                "chunks": 0,
                "message": "No content found in document.",
            }

        # Store document chunks
        vector_store.add_documents(chunks)

        return {
            "success": True,
            "filename": path.name,
            "chunks": len(chunks),
            "message": "Document successfully indexed.",
        }

    def retrieve_context(self, query: str) -> str:

        documents = retriever.retrieve(query)

        if not documents:
            return ""

        context_parts = []

        for index, document in enumerate(
            documents,
            start=1,
        ):

            context_parts.append(
                f"--- Document Chunk {index} ---\n"
                f"{document.page_content}"
            )

        return "\n\n".join(context_parts)


rag_service = RAGService()