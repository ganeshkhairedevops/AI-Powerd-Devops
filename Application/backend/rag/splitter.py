"""
Document Splitter

Splits documents into chunks for embeddings.
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import CHUNK_SIZE
from config import CHUNK_OVERLAP


class DocumentSplitter:

    def __init__(self):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=[
                "\n\n",
                "\n",
                " ",
                "",
            ],
        )

    def split(self, text: str):

        return self.splitter.split_text(text)


splitter = DocumentSplitter()