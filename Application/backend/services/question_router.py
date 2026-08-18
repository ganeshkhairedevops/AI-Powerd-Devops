"""
Question Router

Determines whether a question should be handled by:

- RAG
- DevOps Agent
- General LLM

Routing priority:

1. Explicit live-environment / DevOps operation
2. Explicit document question
3. Document/configuration question when documents exist
4. General knowledge
5. General
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

    1. Live DevOps operation
    2. Explicit document question
    3. Configuration/resource question when documents exist
    4. General knowledge
    5. General
    """

    # =================================================
    # LIVE DEVOPS PHRASES
    # =================================================

    LIVE_PHRASES = (

        # -------------------------------------------------
        # Kubernetes
        # -------------------------------------------------

        "show kubernetes nodes",
        "list kubernetes nodes",
        "get kubernetes nodes",

        "show nodes",
        "list nodes",
        "get nodes",

        "show kubernetes pods",
        "list kubernetes pods",
        "get kubernetes pods",

        "show running kubernetes pods",
        "show running pods",
        "list running pods",
        "get running pods",

        "show pods",
        "list pods",
        "get pods",

        "show kubernetes services",
        "list kubernetes services",
        "get kubernetes services",

        "show services",
        "list services",
        "get services",

        "show kubernetes deployments",
        "list kubernetes deployments",
        "get kubernetes deployments",

        "show deployments",
        "list deployments",
        "get deployments",

        "show kubernetes statefulsets",
        "list kubernetes statefulsets",
        "get kubernetes statefulsets",

        "show statefulsets",
        "list statefulsets",
        "get statefulsets",

        "show kubernetes daemonsets",
        "list kubernetes daemonsets",
        "get kubernetes daemonsets",

        "show daemonsets",
        "list daemonsets",
        "get daemonsets",

        "show kubernetes jobs",
        "list kubernetes jobs",
        "get kubernetes jobs",

        "show kubernetes cronjobs",
        "list kubernetes cronjobs",
        "get kubernetes cronjobs",

        "show kubernetes ingresses",
        "list kubernetes ingresses",
        "get kubernetes ingresses",

        "show kubernetes events",
        "list kubernetes events",
        "get kubernetes events",

        "current kubernetes context",
        "current context",

        "kubernetes context",
        "kubernetes cluster version",
        "cluster version",
        "kubernetes cluster info",
        "cluster info",
        "cluster status",

        "show namespaces",
        "list namespaces",
        "get namespaces",
        "show kubernetes namespaces",
        "list kubernetes namespaces",
        "get kubernetes namespaces",

        "kubectl",

        # -------------------------------------------------
        # Docker
        # -------------------------------------------------

        "show docker containers",
        "list docker containers",
        "get docker containers",

        "show running docker containers",
        "show running containers",
        "list running containers",
        "get running containers",

        "show docker images",
        "list docker images",
        "get docker images",

        "show docker networks",
        "list docker networks",
        "get docker networks",

        "show docker volumes",
        "list docker volumes",
        "get docker volumes",

        "show docker logs",
        "show container logs",

        "inspect docker container",
        "inspect container",

        "docker version",
        "docker info",
        "docker ps",
        "docker images",
        "docker networks",
        "docker volumes",

        # -------------------------------------------------
        # Linux
        # -------------------------------------------------

        "show disk usage",
        "check disk usage",
        "disk usage",

        "show memory usage",
        "check memory usage",
        "memory usage",

        "show cpu usage",
        "check cpu usage",
        "cpu usage",

        "show running processes",
        "list running processes",
        "running processes",

        # -------------------------------------------------
        # Git
        # -------------------------------------------------

        "git status",
        "git branch",
        "git log",
        "git remote",
        "git diff",
        "git tags",
        "git stash",
        "git commit",

        # -------------------------------------------------
        # Helm
        # -------------------------------------------------

        "helm list",
        "helm status",
        "helm history",
        "helm values",

        # -------------------------------------------------
        # Terraform
        # -------------------------------------------------

        "terraform version",
        "terraform validate",
        "terraform fmt",
        "terraform plan",
        "terraform show",
        "terraform workspace",
        "terraform state",
        "terraform providers",

        # -------------------------------------------------
        # AWS
        # -------------------------------------------------

        "aws identity",
        "aws account",
        "aws regions",
        "show ec2 instances",
        "list ec2 instances",
        "show eks clusters",
        "list eks clusters",
        "show s3 buckets",
        "list s3 buckets",
        "show iam users",
        "list iam users",
        "show vpcs",
        "list vpcs",

        # -------------------------------------------------
        # Jenkins
        # -------------------------------------------------

        "jenkins version",
        "jenkins jobs",
        "jenkins nodes",

        # -------------------------------------------------
        # Ansible
        # -------------------------------------------------

        "ansible version",
        "ansible inventory",
        "ansible galaxy roles",

        # -------------------------------------------------
        # GitHub CLI
        # -------------------------------------------------

        "gh version",
        "github repo status",
        "github pull requests",
        "github issues",

        # -------------------------------------------------
        # Monitoring
        # -------------------------------------------------

        "prometheus version",
        "grafana version",
        "node exporter version",
    )

    # =================================================
    # LIVE DEVOPS KEYWORDS
    #
    # These catch natural variations such as:
    #
    # "Can you show me the Kubernetes nodes?"
    #
    # =================================================

    LIVE_KEYWORDS = (

        # Kubernetes
        "kubernetes nodes",
        "kubernetes pods",
        "kubernetes services",
        "kubernetes deployments",
        "kubernetes statefulsets",
        "kubernetes daemonsets",
        "kubernetes jobs",
        "kubernetes cronjobs",
        "kubernetes ingresses",
        "kubernetes events",
        "kubernetes namespaces",
        "kubernetes context",
        "kubernetes cluster",

        # Docker
        "docker containers",
        "docker images",
        "docker networks",
        "docker volumes",
        "docker logs",

        # CLI commands
        "kubectl ",
        "docker ps",
        "docker images",
        "terraform plan",
        "terraform state",
        "git status",
        "git branch",
        "git log",
        "helm list",
        "helm status",
        "aws identity",
        "jenkins jobs",
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
    # Document / Configuration Keywords
    # =================================================

    DOCUMENT_KEYWORDS = (

        # Kubernetes configuration
        "apiversion",
        "api version",
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

        # HPA
        "hpa",
        "horizontal pod autoscaler",
        "minreplicas",
        "maxreplicas",
        "averageutilization",
        "utilization",

        # Docker configuration
        "dockerfile",
        "docker image",
        "container port",
        "restart policy",
        "restart_policy",

        # Terraform configuration
        "terraform resource",
        "terraform variable",
        "terraform output",
        "terraform provider",
        "aws region",
        "instance type",
        "instance_type",

        # Monitoring configuration
        "prometheus",
        "grafana",
        "alerting",
        "monitoring",

        # Jenkins configuration
        "jenkins pipeline",
        "pipeline",
        "deploy environment",
        "deploy_environment",

        # Ansible configuration
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
    # Helper: Live DevOps Detection
    # =================================================

    def _is_live_question(
        self,
        normalized: str,
    ) -> bool:
        """
        Detect questions that require live DevOps tools.

        This check intentionally happens before RAG so that
        uploaded documents cannot hijack live infrastructure
        questions.
        """

        # -------------------------------------------------
        # Exact / phrase matching
        # -------------------------------------------------

        for phrase in self.LIVE_PHRASES:

            if phrase.lower() in normalized:

                return True

        # -------------------------------------------------
        # Keyword matching
        # -------------------------------------------------

        for keyword in self.LIVE_KEYWORDS:

            if keyword.lower() in normalized:

                return True

        return False

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

        1. Live DevOps operation
        2. Explicit document question
        3. Configuration/resource question when documents exist
        4. General knowledge
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
        # LIVE DEVOPS
        #
        # IMPORTANT:
        #
        # This runs BEFORE checking documents.
        #
        # Therefore:
        #
        # "Show Kubernetes nodes"
        #
        # goes to AGENT even when:
        #
        # has_documents=True
        # =================================================

        if self._is_live_question(normalized):

            return QuestionRoute.AGENT

        # =================================================
        # Priority 2:
        # Explicit document question
        # =================================================

        if has_documents:

            for phrase in self.DOCUMENT_PHRASES:

                if phrase.lower() in normalized:

                    return QuestionRoute.RAG

            # =================================================
            # Priority 3:
            # Configuration / resource question
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