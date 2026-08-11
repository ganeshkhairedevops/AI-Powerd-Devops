"""
Embedding Service

Creates embeddings using Ollama's
nomic-embed-text model.
"""

from langchain_ollama import OllamaEmbeddings

from config import OLLAMA_EMBED_MODEL


class EmbeddingService:

    def __init__(self):

        self.embeddings = OllamaEmbeddings(
            model=OLLAMA_EMBED_MODEL,
        )

    def embed_documents(self, documents):
        return self.embeddings.embed_documents(documents)

    def embed_query(self, query):
        return self.embeddings.embed_query(query)


embedding_service = EmbeddingService()