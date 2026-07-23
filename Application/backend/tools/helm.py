from langchain_core.tools import tool
from utils.command_runner import run_command


@tool
def helm_list():
    """List all Helm releases across all namespaces."""
    return run_command(["helm", "list", "-A"])


@tool
def helm_history(release: str):
    """Show the revision history for a Helm release."""
    return run_command(["helm", "history", release])


@tool
def helm_repos():
    """List configured Helm repositories."""
    return run_command(["helm", "repo", "list"])


@tool
def helm_search():
    """Search all configured Helm repositories."""
    return run_command(["helm", "search", "repo"])


@tool
def helm_version():
    """Show the installed Helm version."""
    return run_command(["helm", "version"])


@tool
def helm_status(release: str):
    """Show the status of a Helm release."""
    return run_command(["helm", "status", release])


@tool
def helm_get_values(release: str):
    """Get the values for a Helm release."""
    return run_command(["helm", "get", "values", release])