from pathlib import Path

from config import UPLOAD_FOLDER
from rag.loader import loader
from rag.splitter import splitter
from rag.embeddings import embedding_service

filepath = Path(UPLOAD_FOLDER) / "test.yaml"

content = loader.load(str(filepath))

chunks = splitter.split(content)

vectors = embedding_service.embed_documents(chunks)

print(f"Chunks: {len(chunks)}")
print(f"Vectors: {len(vectors)}")
print(f"Dimensions: {len(vectors[0])}")