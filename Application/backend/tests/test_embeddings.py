from rag.loader import loader
from rag.splitter import splitter
from rag.embeddings import embedding_service

content = loader.load("uploads/test.yaml")

chunks = splitter.split(content)

vectors = embedding_service.embed_documents(chunks)

print(f"Chunks: {len(chunks)}")
print(f"Vectors: {len(vectors)}")
print(f"Dimensions: {len(vectors[0])}")