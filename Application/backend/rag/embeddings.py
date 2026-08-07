"""
Embedding Service

Creates embeddings using Ollama's
nomic-embed-text model.
"""

from langchain_ollama import OllamaEmbeddings


class EmbeddingService:

    def __init__(self):

        self.embeddings = OllamaEmbeddings(
            model="nomic-embed-text",
        )

    def embed_documents(
        self,
        documents,
    ):
        return self.embeddings.embed_documents(documents)

    def embed_query(
        self,
        query,
    ):
        return self.embeddings.embed_query(query)


embedding_service = EmbeddingService()