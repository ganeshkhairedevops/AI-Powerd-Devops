from services.question_router import (
    question_router,
    QuestionRoute,
)


questions = [

    (
        "Which image is used by the pod?",
        QuestionRoute.RAG,
    ),

    (
        "Which image is used by the pod in the uploaded YAML?",
        QuestionRoute.RAG,
    ),

    (
        "Show running Docker containers",
        QuestionRoute.AGENT,
    ),

    (
        "Show running Kubernetes pods",
        QuestionRoute.AGENT,
    ),

    (
        "What is Kubernetes?",
        QuestionRoute.GENERAL,
    ),

    (
        "Explain Docker containers",
        QuestionRoute.GENERAL,
    ),

]


for question, expected in questions:

    result = question_router.route(
        question
    )

    print(
        f"Question: {question}"
    )

    print(
        f"Expected: {expected.value}"
    )

    print(
        f"Actual:   {result.value}"
    )

    print(
        "PASS"
        if result == expected
        else "FAIL"
    )

    print("-" * 60)