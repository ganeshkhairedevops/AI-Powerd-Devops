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