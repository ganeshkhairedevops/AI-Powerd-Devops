"""
Vector Store

Stores, searches, lists, and deletes document chunks
using ChromaDB.

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

    # =================================================
    # Add Documents
    # =================================================

    def add_documents(
        self,
        documents,
        conversation_id: str,
        filename: str,
    ):
        """
        Add document chunks to ChromaDB.

        Metadata stored for every chunk:

        - conversation_id
        - filename
        - chunk_index
        """

        if not documents:
            return

        ids = []
        metadatas = []

        for index, document in enumerate(documents):

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

    # =================================================
    # Search Documents
    # =================================================

    def search(
        self,
        query: str,
        conversation_id: str,
        k: int = 4,
    ):
        """
        Search only documents belonging to
        the specified conversation.

        Returns:
            List of LangChain Document objects.
        """

        return self.db.similarity_search(
            query,
            k=k,
            filter={
                "conversation_id": conversation_id
            },
        )

    # =================================================
    # Search Documents With Scores
    # =================================================

    def search_with_scores(
        self,
        query: str,
        conversation_id: str,
        k: int = 4,
    ):
        """
        Search documents and return similarity
        distance scores.

        The existing search() method remains
        unchanged so current RAG behavior is
        preserved.

        Returns:

            [
                (Document, score),
                ...
            ]

        The score is the distance returned by
        ChromaDB. Lower values generally indicate
        a more similar result.
        """

        return self.db.similarity_search_with_score(
            query,
            k=k,
            filter={
                "conversation_id": conversation_id
            },
        )

    # =================================================
    # List Documents
    # =================================================

    def list_documents(
        self,
        conversation_id: str,
    ):
        """
        Return all uploaded documents belonging
        to a specific conversation.
        """

        results = self.db.get(
            where={
                "conversation_id": conversation_id
            }
        )

        documents = {}

        metadatas = results.get(
            "metadatas",
            [],
        )

        for metadata in metadatas:

            if not metadata:
                continue

            filename = metadata.get(
                "filename",
                "unknown",
            )

            documents.setdefault(
                filename,
                0,
            )

            documents[filename] += 1

        return [
            {
                "filename": filename,
                "chunks": chunks,
            }
            for filename, chunks
            in documents.items()
        ]

    # =================================================
    # Delete Document
    # =================================================

    def delete_document(
        self,
        conversation_id: str,
        filename: str,
    ):
        """
        Delete all chunks belonging to a file
        inside a specific conversation.
        """

        results = self.db.get(
            where={
                "$and": [
                    {
                        "conversation_id": conversation_id
                    },
                    {
                        "filename": filename
                    },
                ]
            }
        )

        ids = results.get(
            "ids",
            [],
        )

        if not ids:
            return False

        self.db.delete(
            ids=ids
        )

        return True


# =====================================================
# Singleton
# =====================================================

vector_store = VectorStore()