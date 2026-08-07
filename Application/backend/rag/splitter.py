"""
Document Splitter

Splits documents into chunks for embeddings.
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter


class DocumentSplitter:

    def __init__(self):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=[
                "\n\n",
                "\n",
                " ",
                ""
            ],
        )

    def split(self, text: str):

        return self.splitter.split_text(text)


splitter = DocumentSplitter()