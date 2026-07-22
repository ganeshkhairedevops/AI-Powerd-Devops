# Creates the LangChain agent
from langchain.agents import create_agent

from llm import llm
from prompts import SYSTEM_PROMPT

from tools.kubernetes import *
from tools.docker import *
from tools.linux import *
from tools.git import *
from tools.helm import *
from tools.terraform import *
from tools.aws import *
from tools.jenkins import *
from tools.ansible import *
from tools.github import *
from tools.monitoring import *


TOOLS = [
    get_pods,
    get_nodes,
    get_services,
    get_deployments,

    kubectl_version,
    kubectl_cluster_info,
    kubectl_contexts,
    kubectl_current_context,
    kubectl_namespaces,
    kubectl_nodes,
    kubectl_pods,
    kubectl_services,
    kubectl_deployments,
    kubectl_statefulsets,
    kubectl_daemonsets,
    kubectl_jobs,
    kubectl_cronjobs,
    kubectl_ingresses,
    kubectl_events,
    kubectl_describe_pod,
    kubectl_logs,
    kubectl_describe_node,
    kubectl_get_resource,
    kubectl_api_resources,
    kubectl_api_versions,

    docker_ps,
    docker_images,
    docker_networks,
    docker_volumes,
    docker_version,
    docker_ps_all,
    docker_logs,
    docker_inspect,
    docker_image_inspect,
    docker_exec,

    disk_usage,
    memory_usage,
    cpu_info,
    running_processes,

    git_status,
    git_branch,
    git_log,
    git_remote,
    git_diff,
    git_show,
    git_tags,
    git_stash_list,
    git_current_commit,
    git_last_commit,

    helm_list,
    helm_status,
    helm_history,
    helm_get_values,

    terraform_version,
    terraform_validate,
    terraform_fmt,
    terraform_plan,
    terraform_show,
    terraform_workspace,
    terraform_state_list,
    terraform_providers,
    # AWS
    aws_identity,
    aws_regions,
    ec2_instances,
    eks_clusters,
    s3_buckets,
    iam_users,
    vpcs,
    # Jenkins
    jenkins_version,
    jenkins_jobs,
    jenkins_nodes,

    # Ansible
    ansible_version,
    ansible_inventory,
    ansible_galaxy_roles,

    # GitHub
    gh_version,
    gh_repo_status,
    gh_pr_list,
    gh_issue_list,

    # Monitoring
    prometheus_version,
    grafana_version,
    node_exporter_version,
]


agent = create_agent(
    model=llm,
    tools=TOOLS,
    system_prompt=SYSTEM_PROMPT,
)
