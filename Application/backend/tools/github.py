from langchain_core.tools import tool
from utils.command_runner import run_command


@tool
def gh_version():
    """Show GitHub CLI version."""
    return run_command(["gh", "--version"])


@tool
def gh_repo_status():
    """Show repository status."""
    return run_command(["gh", "repo", "view"])


@tool
def gh_pr_list():
    """List pull requests."""
    return run_command(["gh", "pr", "list"])


@tool
def gh_issue_list():
    """List GitHub issues."""
    return run_command(["gh", "issue", "list"])