from langchain_core.tools import tool
from utils.command_runner import run_command


@tool
def jenkins_version():
    """Show Jenkins CLI version."""
    return run_command(["java", "-jar", "jenkins-cli.jar", "-version"])


@tool
def jenkins_jobs():
    """List Jenkins jobs."""
    return run_command([
        "java",
        "-jar",
        "jenkins-cli.jar",
        "list-jobs",
    ])


@tool
def jenkins_nodes():
    """List Jenkins nodes."""
    return run_command([
        "java",
        "-jar",
        "jenkins-cli.jar",
        "list-nodes",
    ])