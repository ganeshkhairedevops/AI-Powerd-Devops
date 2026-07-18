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

@tool
def docker_version():
    """Show the Docker version."""
    return run_command(["docker", "version"])

@tool
def docker_ps_all():
    """List all Docker containers."""
    return run_command(["docker", "ps", "-a"])

@tool
def docker_logs(container: str):
    """Show logs for a Docker container."""
    return run_command(["docker", "logs", container])

@tool
def docker_inspect(container: str):
    """Inspect a Docker container."""
    return run_command(["docker", "inspect", container])

@tool
def docker_image_inspect(image: str):
    """Inspect a Docker image."""
    return run_command(["docker", "image", "inspect", image])

@tool
def docker_exec(container: str, command: str):
    """Run a command inside a running container."""
    return run_command(["docker", "exec", container, "sh", "-c", command])