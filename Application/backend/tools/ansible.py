from langchain_core.tools import tool
from utils.command_runner import run_command


@tool
def ansible_version():
    """Show Ansible version."""
    return run_command(["ansible", "--version"])


@tool
def ansible_inventory():
    """List inventory hosts."""
    return run_command([
        "ansible-inventory",
        "--list",
    ])


@tool
def ansible_galaxy_roles():
    """List installed Galaxy roles."""
    return run_command([
        "ansible-galaxy",
        "role",
        "list",
    ])