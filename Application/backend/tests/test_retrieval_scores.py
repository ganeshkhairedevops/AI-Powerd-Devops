from rag.vector_store import vector_store


conversation_id = "test-rag-conversation"


results = vector_store.search_with_scores(
    query="Which image is used by the pod?",
    conversation_id=conversation_id,
    k=4,
)


print()
print("=" * 60)
print("RETRIEVAL SCORE TEST")
print("=" * 60)

print(
    "Results:",
    len(results),
)


for index, item in enumerate(
    results,
    start=1,
):

    document, score = item

    print()
    print(
        f"Result {index}"
    )

    print(
        "Filename:",
        document.metadata.get(
            "filename",
            "unknown",
        ),
    )

    print(
        "Chunk:",
        int(
            document.metadata.get(
                "chunk_index",
                index - 1,
            )
        ) + 1,
    )

    print(
        "Score:",
        score,
    )

    print(
        "Content:",
        document.page_content[:200],
    )


print()
print("=" * 60)


if results:

    print(
        "PASS: Retrieval scores returned successfully."
    )

else:

    print(
        "FAIL: No retrieval results returned."
    )