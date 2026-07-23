from langchain_core.tools import tool
from utils.command_runner import run_command


@tool
def git_status():
    """Show git repository status."""
    return run_command(["git", "status"])


@tool
def git_branch():
    """List local and remote git branches."""
    return run_command(["git", "branch", "-a"])


@tool
def git_log():
    """Show recent git commit history."""
    return run_command(["git", "log", "--oneline", "--graph", "--decorate", "-20"])


@tool
def git_remote():
    """List configured git remotes."""
    return run_command(["git", "remote", "-v"])


@tool
def git_diff():
    """Show working tree changes."""
    return run_command(["git", "diff"])


@tool
def git_show():
    """Show details of the latest commit."""
    return run_command(["git", "show", "--stat", "HEAD"])


@tool
def git_tags():
    """List git tags."""
    return run_command(["git", "tag"])


@tool
def git_stash_list():
    """List git stashes."""
    return run_command(["git", "stash", "list"])


@tool
def git_current_commit():
    """Show the current commit hash (HEAD)."""
    return run_command(["git", "rev-parse", "HEAD"])


@tool
def git_last_commit():
    """Show the last commit."""
    return run_command(["git", "log", "-1"])