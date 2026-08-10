from pathlib import Path

from config import UPLOAD_FOLDER
from rag.loader import loader
from rag.splitter import splitter

filepath = Path(UPLOAD_FOLDER) / "test.yaml"

content = loader.load(str(filepath))

chunks = splitter.split(content)

print(f"Chunks: {len(chunks)}")
print("-" * 50)

for i, chunk in enumerate(chunks, start=1):

    print(f"\nChunk {i}\n")

    print(chunk)

    print("-" * 50)