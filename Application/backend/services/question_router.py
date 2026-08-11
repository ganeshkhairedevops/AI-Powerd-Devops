"""
Question Router

Determines the high-level handling strategy for a user question.

Routes:

    RAG      -> uploaded document question
    AGENT    -> live DevOps operation
    GENERAL  -> general DevOps/technical question
"""

from enum import Enum


class QuestionRoute(str, Enum):

    RAG = "rag"

    AGENT = "agent"

    GENERAL = "general"


class QuestionRouter:
    """
    Lightweight rule-based question router.

    This intentionally does not execute tools or access RAG.
    It only determines the likely handling strategy.
    """

    # =================================================
    # Live environment keywords
    # =================================================

    LIVE_KEYWORDS = (

        "show",

        "list",

        "get",

        "check",

        "current",

        "running",

        "status",

        "logs",

        "restart",

        "stop",

        "start",

        "delete",

        "create",

        "deploy",

        "deployment",

        "inspect",

        "describe",

        "version",

        "health",

        "nodes",

        "pods",

        "containers",

        "services",

        "images",

        "volumes",

        "processes",

        "disk",

        "memory",

        "cpu",

        "terraform plan",

        "terraform validate",

        "terraform state",

        "git status",

        "git branch",

        "git log",

        "helm list",

        "helm status",

        "aws",

        "jenkins",

        "ansible",

    )


    # =================================================
    # Document keywords
    # =================================================

    DOCUMENT_KEYWORDS = (

        "uploaded file",

        "uploaded document",

        "uploaded yaml",

        "uploaded json",

        "uploaded dockerfile",

        "uploaded terraform",

        "this file",

        "this document",

        "the file",

        "the document",

        "according to the file",

        "according to the document",

        "in the file",

        "in the document",

        "from the file",

        "from the document",

        "what does this yaml",

        "what does this json",

        "what does this dockerfile",

        "which image is used by the pod",

    )


    # =================================================
    # Route
    # =================================================

    def route(
        self,
        question: str,
    ) -> QuestionRoute:
        """
        Determine the appropriate route.
        """

        normalized = (
            question
            .strip()
            .lower()
        )


        if not normalized:

            return QuestionRoute.GENERAL


        # -------------------------------------------------
        # Explicit document questions
        # -------------------------------------------------

        for keyword in self.DOCUMENT_KEYWORDS:

            if keyword in normalized:

                return QuestionRoute.RAG


        # -------------------------------------------------
        # Explicit live environment questions
        # -------------------------------------------------

        for keyword in self.LIVE_KEYWORDS:

            if keyword in normalized:

                return QuestionRoute.AGENT


        # -------------------------------------------------
        # Default
        # -------------------------------------------------

        return QuestionRoute.GENERAL


# =====================================================
# Singleton
# =====================================================

question_router = QuestionRouter()