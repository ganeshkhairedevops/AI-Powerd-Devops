from rag.retriever import retriever


conversation_id = "test-rag-conversation"


results = retriever.retrieve(
    query="Which image is used by the pod?",
    conversation_id=conversation_id,
)


print()
print("=" * 60)
print("RETRIEVAL METADATA TEST")
print("=" * 60)

print(
    "Chunks retrieved:",
    len(results),
)


for index, document in enumerate(
    results,
    start=1,
):

    print()
    print(
        f"Chunk {index}"
    )

    print(
        "Filename:",
        document.metadata.get(
            "filename",
            "unknown",
        ),
    )

    print(
        "Chunk Index:",
        document.metadata.get(
            "chunk_index",
            "unknown",
        ),
    )

    print(
        "Content:",
        document.page_content[:200],
    )


print()
print("=" * 60)

if results:
    print("PASS: Documents retrieved successfully.")
else:
    print("FAIL: No documents retrieved.")