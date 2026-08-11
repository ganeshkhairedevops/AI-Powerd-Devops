from pathlib import Path

from config import UPLOAD_FOLDER
from rag.loader import loader
from rag.splitter import splitter
from rag.vector_store import vector_store
from rag.retriever import retriever

filepath = Path(UPLOAD_FOLDER) / "test.yaml"

content = loader.load(str(filepath))

chunks = splitter.split(content)

vector_store.add_documents(chunks)

query = "Which image is used by the pod?"

results = retriever.retrieve(query)

print(f"Results: {len(results)}")

print("-" * 60)

for i, doc in enumerate(results, start=1):

    print(f"Document {i}\n")

    print(doc.page_content)

    print("-" * 60)