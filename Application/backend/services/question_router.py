"""
Question Router

Determines whether a question should be handled by:

- RAG
- DevOps Agent
- General LLM

The router can use conversation context to determine
whether uploaded documents should be considered.
"""

from enum import Enum


# =====================================================
# Routes
# =====================================================

class QuestionRoute(str, Enum):

    RAG = "rag"

    AGENT = "agent"

    GENERAL = "general"


# =====================================================
# Question Router
# =====================================================

class QuestionRouter:
    """
    Context-aware question router.

    Routing priority:

    1. Explicit live-environment question
    2. Explicit document question
    3. Configuration/resource question when documents exist
    4. General knowledge question
    5. General
    """

    # =================================================
    # Explicit live-environment indicators
    # =================================================

    LIVE_PHRASES = (

        # -------------------------------------------------
        # Kubernetes live operations
        # -------------------------------------------------

        "show running kubernetes pods",
        "show kubernetes pods",
        "list kubernetes pods",
        "get kubernetes pods",

        "show running pods",
        "show pods",
        "list pods",
        "get pods",

        "show nodes",
        "list nodes",
        "get nodes",

        "show kubernetes services",
        "list kubernetes services",
        "get kubernetes services",

        "show kubernetes deployments",
        "list kubernetes deployments",
        "get kubernetes deployments",

        "show kubernetes events",
        "list kubernetes events",

        "current kubernetes context",
        "current context",

        "cluster version",
        "cluster status",
        "cluster info",

        "live cluster",
        "live environment",

        "kubectl",

        # -------------------------------------------------
        # Docker live operations
        # -------------------------------------------------

        "show running docker containers",
        "show docker containers",
        "list docker containers",
        "get docker containers",

        "show running containers",
        "list running containers",

        "show docker images",
        "list docker images",
        "get docker images",

        "show docker networks",
        "list docker networks",

        "show docker volumes",
        "list docker volumes",

        "show container logs",
        "show docker logs",

        "inspect container",
        "inspect docker container",

        "docker version",
        "docker info",

        "docker ps",
        "docker images",
        "docker networks",
        "docker volumes",

        # -------------------------------------------------
        # Terraform live operations
        # -------------------------------------------------

        "terraform plan",
        "terraform validate",
        "terraform state",

        # -------------------------------------------------
        # Git live operations
        # -------------------------------------------------

        "git status",
        "git branch",
        "git log",

        # -------------------------------------------------
        # Helm live operations
        # -------------------------------------------------

        "helm list",
        "helm status",

        # -------------------------------------------------
        # AWS live operations
        # -------------------------------------------------

        "aws account",
        "aws identity",

        # -------------------------------------------------
        # Jenkins live operations
        # -------------------------------------------------

        "jenkins jobs",

        # -------------------------------------------------
        # Ansible live operations
        # -------------------------------------------------

        "ansible inventory",
    )

    # =================================================
    # Explicit document indicators
    # =================================================

    DOCUMENT_PHRASES = (

        "uploaded file",
        "uploaded document",
        "uploaded yaml",
        "uploaded yml",
        "uploaded json",
        "uploaded dockerfile",
        "uploaded terraform",

        "this file",
        "this document",

        "the file",
        "the document",

        "in the file",
        "in the document",

        "from the file",
        "from the document",

        "according to the file",
        "according to the document",

        "according to the yaml",
        "according to the dockerfile",

        "in test.yaml",
        "in test.yml",

        "in the yaml",
        "in the dockerfile",

        "what image is used",
        "which image is used",

        "what image is defined",
        "which image is defined",

        "what api version",
        "which api version",

        "what apiversion",
        "which apiversion",

        "how many replicas",

        "what container",
        "which container",
    )

    # =================================================
    # Document/configuration indicators
    # =================================================

    DOCUMENT_KEYWORDS = (

        # Kubernetes
        "apiversion",
        "kind",
        "metadata",
        "spec",
        "image",
        "replicas",
        "namespace",
        "port",
        "ports",
        "volume",
        "volumes",
        "service",
        "deployment",
        "configmap",
        "secret",
        "ingress",
        "probe",
        "readiness",
        "liveness",

        # Kubernetes HPA
        "hpa",
        "horizontal pod autoscaler",
        "minreplicas",
        "maxreplicas",
        "averageutilization",
        "utilization",

        # Docker
        "dockerfile",
        "docker image",
        "container port",
        "restart policy",
        "restart_policy",

        # Terraform
        "terraform resource",
        "terraform variable",
        "terraform output",
        "terraform provider",
        "aws region",
        "instance type",
        "instance_type",

        # Monitoring
        "prometheus",
        "grafana",
        "alerting",
        "monitoring",

        # Jenkins
        "jenkins pipeline",
        "pipeline",
        "deploy environment",
        "deploy_environment",

        # Ansible
        "ansible",
        "playbook",
        "inventory",
    )

    # =================================================
    # General knowledge indicators
    # =================================================

    GENERAL_PHRASES = (

        "what is",
        "what are",

        "explain",

        "define",

        "difference between",

        "why use",

        "how does",

        "what does",
    )

    # =================================================
    # Route
    # =================================================

    def route(
        self,
        question: str,
        has_documents: bool = False,
    ) -> QuestionRoute:
        """
        Determine the appropriate route.

        Priority:

        1. Explicit live-environment question
        2. Explicit document question
        3. Configuration/resource question when documents exist
        4. General knowledge question
        5. General
        """

        normalized = (
            question
            .strip()
            .lower()
        )

        # =================================================
        # Empty question
        # =================================================

        if not normalized:

            return QuestionRoute.GENERAL

        # =================================================
        # Priority 1:
        # Explicit live environment
        # =================================================

        for phrase in self.LIVE_PHRASES:

            if phrase.lower() in normalized:

                return QuestionRoute.AGENT

        # =================================================
        # Priority 2:
        # Explicit document question
        #
        # This MUST happen before GENERAL_PHRASES.
        #
        # Example:
        #
        # "What is the namespace of the deployment?"
        #
        # contains "what is" AND "namespace".
        #
        # Since documents exist, RAG must win.
        # =================================================

        if has_documents:

            for phrase in self.DOCUMENT_PHRASES:

                if phrase.lower() in normalized:

                    return QuestionRoute.RAG

            # =================================================
            # Priority 3:
            # Configuration/resource question
            # =================================================

            for keyword in self.DOCUMENT_KEYWORDS:

                if keyword.lower() in normalized:

                    return QuestionRoute.RAG

        # =================================================
        # Priority 4:
        # General knowledge
        # =================================================

        for phrase in self.GENERAL_PHRASES:

            if phrase.lower() in normalized:

                return QuestionRoute.GENERAL

        # =================================================
        # Priority 5:
        # Default
        # =================================================

        return QuestionRoute.GENERAL


# =====================================================
# Singleton
# =====================================================

question_router = QuestionRouter()