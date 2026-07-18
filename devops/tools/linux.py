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

@tool
def linux_uname():
    """Show system information."""
    return run_command(["uname", "-a"])

@tool
def linux_hostname():
    """Show the system hostname."""
    return run_command(["hostname"])

@tool
def linux_uptime():
    """Show system uptime and load average."""
    return run_command(["uptime"])


@tool
def linux_whoami():
    """Show the current user."""
    return run_command(["whoami"])

@tool
def linux_pwd():
    """Show the current working directory."""
    return run_command(["pwd"])


@tool
def linux_ls(path: str = "."):
    """List files in a directory."""
    return run_command(["ls", "-lah", path])

def linux_cpu():
    """Show CPU information."""
    return run_command(["lscpu"])


@tool
def linux_mounts():
    """Show mounted filesystems."""
    return run_command(["mount"])


@tool
def linux_processes():
    """List running processes."""
    return run_command(["ps", "-ef"])


@tool
def linux_top():
    """Show current CPU and memory usage."""
    return run_command(["top", "-b", "-n", "1"])

@tool
def linux_env():
    """Show environment variables."""
    return run_command(["env"])


@tool
def linux_ip():
    """Show IP address information."""
    return run_command(["ip", "addr"])


@tool
def linux_routes():
    """Show routing table."""
    return run_command(["ip", "route"])


@tool
def linux_ports():
    """Show listening network ports."""
    return run_command(["ss", "-tuln"])

@tool
def linux_connections():
    """Show active network connections."""
    return run_command(["ss", "-tunap"])


@tool
def linux_ping(host: str):
    """Ping a host."""
    return run_command(["ping", "-c", "4", host])


@tool
def linux_dns_lookup(host: str):
    """Lookup DNS records."""
    return run_command(["nslookup", host])


@tool
def linux_cat(file: str):
    """Display a file."""
    return run_command(["cat", file])

@tool
def linux_tail(file: str):
    """Show the last 100 lines of a file."""
    return run_command(["tail", "-100", file])


@tool
def linux_head(file: str):
    """Show the first 100 lines of a file."""
    return run_command(["head", "-100", file])


@tool
def linux_find(path: str, pattern: str):
    """Find files matching a pattern."""
    return run_command(["find", path, "-name", pattern])


@tool
def linux_systemctl():
    """List systemd services."""
    return run_command(["systemctl", "list-units", "--type=service"])

@tool
def linux_journal():
    """Show the last 100 system journal entries."""
    return run_command(["journalctl", "-n", "100", "--no-pager"])


@tool
def linux_date():
    """Show the current system date and time."""
    return run_command(["date"])
