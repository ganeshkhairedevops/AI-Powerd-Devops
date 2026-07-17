from langchain_core.tools import tool
from utils.command_runner import run_command


@tool
def docker_ps():
    """List running Docker containers."""
    return run_command(["docker", "ps"])


@tool
def docker_images():
    """List Docker images."""
    return run_command(["docker", "images"])


@tool
def docker_networks():
    """List Docker networks."""
    return run_command(["docker", "network", "ls"])


@tool
def docker_volumes():
    """List Docker volumes."""
    return run_command(["docker", "volume", "ls"])