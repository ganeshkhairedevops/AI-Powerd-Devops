from langchain_core.tools import tool
from utils.command_runner import run_command


@tool
def disk_usage():
    """Show disk usage."""
    return run_command(["df", "-h"])


@tool
def memory_usage():
    """Show memory usage."""
    return run_command(["free", "-h"])


@tool
def cpu_info():
    """Show CPU information."""
    return run_command(["lscpu"])


@tool
def running_processes():
    """Show running processes."""
    return run_command(["ps", "-ef"])