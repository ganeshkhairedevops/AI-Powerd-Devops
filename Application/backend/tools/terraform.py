from langchain_core.tools import tool
from utils.command_runner import run_command


@tool
def terraform_version():
    """Show the installed Terraform version."""
    return run_command(["terraform", "version"])


@tool
def terraform_validate():
    """Validate the current Terraform configuration."""
    return run_command(["terraform", "validate"])


@tool
def terraform_fmt():
    """Format Terraform configuration files."""
    return run_command(["terraform", "fmt"])


@tool
def terraform_plan():
    """Generate and show an execution plan."""
    return run_command(["terraform", "plan"])


@tool
def terraform_show():
    """Show the current Terraform state or plan."""
    return run_command(["terraform", "show"])


@tool
def terraform_workspace():
    """List available Terraform workspaces."""
    return run_command(["terraform", "workspace", "list"])


@tool
def terraform_state_list():
    """List resources in the Terraform state."""
    return run_command(["terraform", "state", "list"])


@tool
def terraform_providers():
    """Show the providers required by the current configuration."""
    return run_command(["terraform", "providers"])