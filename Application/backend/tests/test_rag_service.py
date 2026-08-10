from pathlib import Path

from config import UPLOAD_FOLDER
from rag.rag_service import rag_service


filepath = Path(UPLOAD_FOLDER) / "test.yaml"


# ---------------------------------------
# Ingest document
# ---------------------------------------

result = rag_service.ingest_file(
    str(filepath)
)

print("=" * 60)
print("INGESTION RESULT")
print("=" * 60)

print(result)


# ---------------------------------------
# Retrieve context
# ---------------------------------------

query = "Which image is used by the pod?"

context = rag_service.retrieve_context(
    query
)


print("\n")
print("=" * 60)
print("RETRIEVED CONTEXT")
print("=" * 60)

print(context)