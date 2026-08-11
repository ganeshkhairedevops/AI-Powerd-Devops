"""
Vector Store

Stores and retrieves document chunks using ChromaDB.

Documents are isolated by conversation_id.
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

    def add_documents(
        self,
        documents,
        conversation_id: str,
        filename: str,
    ):
        """
        Add document chunks to ChromaDB.

        Each chunk receives metadata containing:
        - conversation_id
        - filename
        - chunk_index
        """

        if not documents:
            return

        ids = []
        metadatas = []

        for index, document in enumerate(
            documents
        ):

            document_id = hashlib.sha256(
                (
                    f"{conversation_id}:"
                    f"{filename}:"
                    f"{index}:"
                    f"{document}"
                ).encode("utf-8")
            ).hexdigest()

            ids.append(document_id)

            metadatas.append(
                {
                    "conversation_id": conversation_id,
                    "filename": filename,
                    "chunk_index": index,
                }
            )

        self.db.add_texts(
            texts=documents,
            ids=ids,
            metadatas=metadatas,
        )

    def search(
        self,
        query: str,
        conversation_id: str,
        k: int = 4,
    ):
        """
        Search only documents belonging to
        the specified conversation.
        """

        return self.db.similarity_search(
            query,
            k=k,
            filter={
                "conversation_id": conversation_id
            },
        )


vector_store = VectorStore()