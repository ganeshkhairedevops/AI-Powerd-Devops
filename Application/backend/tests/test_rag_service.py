from pathlib import Path

from rag.rag_service import rag_service


# =====================================================
# Test File
# =====================================================

filepath = Path(
    "uploads/test.yaml"
)


conversation_id = "test-rag-conversation"


# =====================================================
# Ingestion Test
# =====================================================

result = rag_service.ingest_file(
    filepath=str(filepath),
    conversation_id=conversation_id,
)


print()
print("=" * 60)
print("INGESTION RESULT")
print("=" * 60)

print(result)


# =====================================================
# Retrieval With Sources
# =====================================================

rag_result = (
    rag_service.retrieve_context_with_sources(
        query="Which image is used by the pod?",
        conversation_id=conversation_id,
    )
)


print()
print("=" * 60)
print("RETRIEVAL RESULT")
print("=" * 60)


print()
print("--- CONTEXT ---")

print(
    rag_result["context"]
)


print()
print("--- SOURCES ---")

for source in rag_result["sources"]:

    print(
        f"File: {source['filename']}"
    )

    print(
        f"Chunk: {source['chunk']}"
    )

    print("-" * 40)


# =====================================================
# Answer Test
# =====================================================

if rag_result["context"]:

    answer = (
        rag_service.answer_from_context(
            question="Which image is used by the pod?",
            context=rag_result["context"],
        )
    )


    print()
    print("=" * 60)
    print("ANSWER")
    print("=" * 60)

    print(answer)