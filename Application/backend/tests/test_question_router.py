from services.question_router import (
    question_router,
    QuestionRoute,
)


tests = [

    # =================================================
    # RAG
    # =================================================

    (
        "Which image is used by the pod?",
        True,
        QuestionRoute.RAG,
    ),

    (
        "What apiVersion is used in the pod?",
        True,
        QuestionRoute.RAG,
    ),

    (
        "Which image is defined in the uploaded YAML?",
        True,
        QuestionRoute.RAG,
    ),

    (
        "What container is defined in the file?",
        True,
        QuestionRoute.RAG,
    ),


    # =================================================
    # AGENT
    # =================================================

    (
        "Show running Docker containers",
        True,
        QuestionRoute.AGENT,
    ),

    (
        "Show running Kubernetes pods",
        True,
        QuestionRoute.AGENT,
    ),

    (
        "What is the Kubernetes cluster version?",
        True,
        QuestionRoute.AGENT,
    ),

    (
        "Show Docker images",
        True,
        QuestionRoute.AGENT,
    ),

    (
        "What is the current Kubernetes context?",
        True,
        QuestionRoute.AGENT,
    ),


    # =================================================
    # GENERAL
    # =================================================

    (
        "What is Kubernetes?",
        True,
        QuestionRoute.GENERAL,
    ),

    (
        "Explain Docker containers",
        True,
        QuestionRoute.GENERAL,
    ),

    (
        "What is Terraform?",
        True,
        QuestionRoute.GENERAL,
    ),


    # =================================================
    # No documents
    # =================================================

    (
        "Which image is used by the pod?",
        False,
        QuestionRoute.GENERAL,
    ),

    (
        "What is Kubernetes?",
        False,
        QuestionRoute.GENERAL,
    ),

]


# =====================================================
# Run Tests
# =====================================================

passed = 0
failed = 0


for question, has_documents, expected in tests:

    actual = question_router.route(
        question=question,
        has_documents=has_documents,
    )


    status = (
        "PASS"
        if actual == expected
        else "FAIL"
    )


    print(
        f"[{status}] "
        f"{question}"
    )

    print(
        f"  Documents: {has_documents}"
    )

    print(
        f"  Expected:  {expected.value}"
    )

    print(
        f"  Actual:    {actual.value}"
    )

    print("-" * 60)


    if actual == expected:

        passed += 1

    else:

        failed += 1


print()
print("=" * 60)

print(
    f"Passed: {passed}"
)

print(
    f"Failed: {failed}"
)

print("=" * 60)


if failed > 0:

    raise SystemExit(1)