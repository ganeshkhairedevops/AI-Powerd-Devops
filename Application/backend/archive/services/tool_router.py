"""
Tool Router

Maps a user's request to the appropriate DevOps tool function.
"""

from tools.docker import (
    docker_ps,
    docker_images,
    docker_networks,
    docker_volumes,
    docker_version,
)

from tools.kubernetes import (
    kubectl_pods,
    kubectl_nodes,
    kubectl_services,
    kubectl_deployments,
)

from tools.linux import (
    disk_usage,
    memory_usage,
    cpu_info,
    running_processes,
)

from tools.aws import (
    ec2_instances,
    eks_clusters,
    s3_buckets,
    iam_users,
    vpcs,
)

from tools.git import (
    git_status,
    git_branch,
    git_log,
)

from tools.terraform import (
    terraform_plan,
    terraform_validate,
    terraform_version,
)

from tools.jenkins import (
    jenkins_jobs,
    jenkins_version,
)


class ToolRouter:

    def __init__(self):
        self.routes = [
            # ---------------- Docker ----------------
            (
                ["docker", "container", "containers", "running container"],
                docker_ps,
                "docker ps",
                "Docker",
            ),
            (
                ["docker image", "images"],
                docker_images,
                "docker images",
                "Docker",
            ),
            (
                ["network", "docker network"],
                docker_networks,
                "docker network ls",
                "Docker",
            ),
            (
                ["volume", "docker volume"],
                docker_volumes,
                "docker volume ls",
                "Docker",
            ),
            (
                ["docker version"],
                docker_version,
                "docker version",
                "Docker",
            ),

            # ---------------- Kubernetes ----------------
            (
                ["pod", "pods"],
                kubectl_pods,
                "kubectl get pods -A",
                "Kubernetes",
            ),
            (
                ["node", "nodes"],
                kubectl_nodes,
                "kubectl get nodes",
                "Kubernetes",
            ),
            (
                ["service", "services"],
                kubectl_services,
                "kubectl get svc -A",
                "Kubernetes",
            ),
            (
                ["deployment", "deployments"],
                kubectl_deployments,
                "kubectl get deploy -A",
                "Kubernetes",
            ),

            # ---------------- Linux ----------------
            (
                ["disk", "disk usage"],
                disk_usage,
                "df -h",
                "Linux",
            ),
            (
                ["memory", "ram"],
                memory_usage,
                "free -h",
                "Linux",
            ),
            (
                ["cpu"],
                cpu_info,
                "lscpu",
                "Linux",
            ),
            (
                ["process", "processes"],
                running_processes,
                "ps aux",
                "Linux",
            ),

            # ---------------- AWS ----------------
            (
                ["ec2", "instance", "instances"],
                ec2_instances,
                "aws ec2 describe-instances",
                "AWS",
            ),
            (
                ["eks"],
                eks_clusters,
                "aws eks list-clusters",
                "AWS",
            ),
            (
                ["bucket", "s3"],
                s3_buckets,
                "aws s3 ls",
                "AWS",
            ),
            (
                ["iam"],
                iam_users,
                "aws iam list-users",
                "AWS",
            ),
            (
                ["vpc"],
                vpcs,
                "aws ec2 describe-vpcs",
                "AWS",
            ),

            # ---------------- Git ----------------
            (
                ["git status"],
                git_status,
                "git status",
                "Git",
            ),
            (
                ["branch"],
                git_branch,
                "git branch",
                "Git",
            ),
            (
                ["git log", "commit history"],
                git_log,
                "git log",
                "Git",
            ),

            # ---------------- Terraform ----------------
            (
                ["terraform plan", "plan"],
                terraform_plan,
                "terraform plan",
                "Terraform",
            ),
            (
                ["terraform validate", "validate"],
                terraform_validate,
                "terraform validate",
                "Terraform",
            ),
            (
                ["terraform version"],
                terraform_version,
                "terraform version",
                "Terraform",
            ),

            # ---------------- Jenkins ----------------
            (
                ["jenkins job", "jobs"],
                jenkins_jobs,
                "jenkins-cli list-jobs",
                "Jenkins",
            ),
            (
                ["jenkins version"],
                jenkins_version,
                "jenkins --version",
                "Jenkins",
            ),
        ]

    def route(self, question: str):
        """
        Returns:
            (tool_function, command, category)
            or None
        """

        q = question.lower()

        for keywords, tool, command, category in self.routes:
            if any(keyword in q for keyword in keywords):
                return tool, command, category

        return None