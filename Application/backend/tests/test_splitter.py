from rag.loader import loader
from rag.splitter import splitter

content = loader.load("uploads/test.yaml")

chunks = splitter.split(content)

print(f"Chunks: {len(chunks)}")
print("-" * 50)

for i, chunk in enumerate(chunks, start=1):

    print(f"\nChunk {i}\n")

    print(chunk)

    print("-" * 50)