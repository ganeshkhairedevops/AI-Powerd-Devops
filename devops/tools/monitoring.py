from langchain_core.tools import tool
from utils.command_runner import run_command


@tool
def prometheus_version():
    """Show Prometheus version."""
    return run_command(["prometheus", "--version"])


@tool
def grafana_version():
    """Show Grafana version."""
    return run_command(["grafana-server", "-v"])


@tool
def node_exporter_version():
    """Show Node Exporter version."""
    return run_command(["node_exporter", "--version"])