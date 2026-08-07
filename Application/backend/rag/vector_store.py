"""
Vector Store

Stores and retrieves document embeddings
using ChromaDB.
"""

from langchain_chroma import Chroma

from rag.embeddings import embedding_service
from config import CHROMA_DB_PATH


class VectorStore:

    def __init__(self):

        self.db = Chroma(
            persist_directory=CHROMA_DB_PATH,
            embedding_function=embedding_service.embeddings,
        )

    def add_documents(self, documents):

        self.db.add_texts(documents)

    def search(self, query, k=4):

        return self.db.similarity_search(query, k=k)


vector_store = VectorStore()