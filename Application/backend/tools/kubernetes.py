from langchain_core.tools import tool
from utils.command_runner import run_command


@tool
def get_pods():
    """List all Kubernetes Pods."""
    return run_command(["kubectl", "get", "pods", "-A"])


@tool
def get_nodes():
    """List Kubernetes Nodes."""
    return run_command(["kubectl", "get", "nodes", "-o", "wide"])


@tool
def get_services():
    """List Services."""
    return run_command(["kubectl", "get", "svc", "-A"])


@tool
def get_deployments():
    """List Deployments."""
    return run_command(["kubectl", "get", "deployments", "-A"])
##

@tool
def kubectl_version():
    """Show the kubectl client version."""
    return run_command(["kubectl", "version", "--client"])


@tool
def kubectl_cluster_info():
    """Show cluster information."""
    return run_command(["kubectl", "cluster-info"])


@tool
def kubectl_contexts():
    """List available Kubernetes contexts."""
    return run_command(["kubectl", "config", "get-contexts"])


@tool
def kubectl_current_context():
    """Show the current Kubernetes context."""
    return run_command(["kubectl", "config", "current-context"])


@tool
def kubectl_namespaces():
    """List all namespaces."""
    return run_command(["kubectl", "get", "namespaces"])


@tool
def kubectl_nodes():
    """List cluster nodes."""
    return run_command(["kubectl", "get", "nodes", "-o", "wide"])


@tool
def kubectl_pods():
    """List pods in all namespaces."""
    return run_command(["kubectl", "get", "pods", "-A", "-o", "wide"])


@tool
def kubectl_services():
    """List services in all namespaces."""
    return run_command(["kubectl", "get", "services", "-A"])


@tool
def kubectl_deployments():
    """List deployments in all namespaces."""
    return run_command(["kubectl", "get", "deployments", "-A"])


@tool
def kubectl_statefulsets():
    """List StatefulSets in all namespaces."""
    return run_command(["kubectl", "get", "statefulsets", "-A"])


@tool
def kubectl_daemonsets():
    """List DaemonSets in all namespaces."""
    return run_command(["kubectl", "get", "daemonsets", "-A"])


@tool
def kubectl_jobs():
    """List Jobs in all namespaces."""
    return run_command(["kubectl", "get", "jobs", "-A"])


@tool
def kubectl_cronjobs():
    """List CronJobs in all namespaces."""
    return run_command(["kubectl", "get", "cronjobs", "-A"])


@tool
def kubectl_ingresses():
    """List Ingress resources in all namespaces."""
    return run_command(["kubectl", "get", "ingress", "-A"])


@tool
def kubectl_events():
    """Show recent cluster events."""
    return run_command(
        ["kubectl", "get", "events", "-A", "--sort-by=.metadata.creationTimestamp"]
    )


@tool
def kubectl_describe_pod(name: str, namespace: str = "default"):
    """Describe a Kubernetes pod."""
    return run_command(["kubectl", "describe", "pod", name, "-n", namespace])


@tool
def kubectl_logs(name: str, namespace: str = "default"):
    """Get logs from a pod."""
    return run_command(["kubectl", "logs", name, "-n", namespace])


@tool
def kubectl_describe_node(name: str):
    """Describe a Kubernetes node."""
    return run_command(["kubectl", "describe", "node", name])


@tool
def kubectl_get_resource(resource: str, namespace: str = "default"):
    """Get resources of a specified type in a namespace."""
    return run_command(["kubectl", "get", resource, "-n", namespace])


@tool
def kubectl_api_resources():
    """List available Kubernetes API resources."""
    return run_command(["kubectl", "api-resources"])


@tool
def kubectl_api_versions():
    """List supported Kubernetes API versions."""
    return run_command(["kubectl", "api-versions"])