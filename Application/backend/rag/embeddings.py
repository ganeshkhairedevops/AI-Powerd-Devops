"""
Embedding Service

Provides Ollama embeddings for RAG.
"""

from langchain_ollama import OllamaEmbeddings

from config import (
    OLLAMA_EMBED_MODEL,
    OLLAMA_BASE_URL,
)


class EmbeddingService:

    def __init__(self):

        self.embeddings = OllamaEmbeddings(
            model=OLLAMA_EMBED_MODEL,
            base_url=OLLAMA_BASE_URL,
        )

    def embed_documents(self, documents):

        return self.embeddings.embed_documents(
            documents
        )

    def embed_query(self, query):

        return self.embeddings.embed_query(
            query
        )


embedding_service = EmbeddingService()