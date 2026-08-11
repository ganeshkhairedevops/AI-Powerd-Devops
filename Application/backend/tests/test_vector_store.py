from pathlib import Path

from config import UPLOAD_FOLDER
from rag.loader import loader
from rag.splitter import splitter
from rag.vector_store import vector_store

filepath = Path(UPLOAD_FOLDER) / "test.yaml"

content = loader.load(str(filepath))

chunks = splitter.split(content)

vector_store.add_documents(chunks)

results = vector_store.search("nginx")

print(f"Results: {len(results)}")

for doc in results:

    print("-" * 50)

    print(doc.page_content)