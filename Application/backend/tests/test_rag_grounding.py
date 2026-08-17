"""
RAG Grounding Tests
"""

from rag.rag_service import rag_service


print("=" * 60)
print("RAG GROUNDING TEST")
print("=" * 60)


# =====================================================
# Test 1 - Answer exists in context
# =====================================================

context_1 = """
--- test.yaml | Document Chunk 1 ---

apiVersion: v1
kind: Pod

spec:
  containers:
    - name: nginx
      image: nginx:1.27
"""

question_1 = (
    "Which image is used by the container?"
)

answer_1 = rag_service.answer_from_context(
    question=question_1,
    context=context_1,
)

print()
print("TEST 1")
print("Question:", question_1)
print("Answer:", answer_1)


if (
    "nginx:1.27"
    in answer_1
):

    print(
        "PASS: Answer grounded in document."
    )

else:

    print(
        "FAIL: Expected document value."
    )


# =====================================================
# Test 2 - Information not present
# =====================================================

context_2 = """
--- test.yaml | Document Chunk 1 ---

apiVersion: v1
kind: Pod

metadata:
  name: nginx
"""

question_2 = (
    "What is the Kubernetes cluster version?"
)

answer_2 = rag_service.answer_from_context(
    question=question_2,
    context=context_2,
)

print()
print("TEST 2")
print("Question:", question_2)
print("Answer:", answer_2)


if (
    answer_2
    == "NOT_ENOUGH_CONTEXT"
):

    print(
        "PASS: Missing information rejected."
    )

else:

    print(
        "FAIL: Model answered without context."
    )


# =====================================================
# Test 3 - Empty context
# =====================================================

question_3 = (
    "What port does the service expose?"
)

answer_3 = rag_service.answer_from_context(
    question=question_3,
    context="",
)

print()
print("TEST 3")
print("Question:", question_3)
print("Answer:", answer_3)


if (
    answer_3
    == "NOT_ENOUGH_CONTEXT"
):

    print(
        "PASS: Empty context handled correctly."
    )

else:

    print(
        "FAIL: Empty context should be rejected."
    )


# =====================================================
# Test 4 - Multiple facts in context
# =====================================================

context_4 = """
--- deployment.yaml | Document Chunk 1 ---

kind: Deployment

metadata:
  name: nginx

spec:
  replicas: 3

  template:
    spec:
      containers:
        - name: nginx
          image: nginx:1.27
"""

question_4 = (
    "How many replicas does the nginx deployment have?"
)

answer_4 = rag_service.answer_from_context(
    question=question_4,
    context=context_4,
)

print()
print("TEST 4")
print("Question:", question_4)
print("Answer:", answer_4)


if (
    "3"
    in answer_4
):

    print(
        "PASS: Multi-field document answer grounded."
    )

else:

    print(
        "FAIL: Expected replica count."
    )


print()
print("=" * 60)
print("GROUNDING TEST COMPLETE")
print("=" * 60)