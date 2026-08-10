"""
Vector Store

Stores and retrieves document embeddings
using ChromaDB.
"""

import hashlib

from langchain_chroma import Chroma

from config import CHROMA_DB_PATH
from rag.embeddings import embedding_service


class VectorStore:

    def __init__(self):

        self.db = Chroma(
            persist_directory=CHROMA_DB_PATH,
            embedding_function=embedding_service.embeddings,
        )

    def add_documents(self, documents):

        if not documents:
            return

        ids = []

        for document in documents:

            document_id = hashlib.sha256(
                document.encode("utf-8")
            ).hexdigest()

            ids.append(document_id)

        self.db.add_texts(
            texts=documents,
            ids=ids,
        )

    def search(self, query, k=4):

        return self.db.similarity_search(
            query,
            k=k,
        )


vector_store = VectorStore()