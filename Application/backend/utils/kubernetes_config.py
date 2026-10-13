
"""
Universal Kubernetes Runtime Configuration

Supports:

- Windows + Docker Desktop Kubernetes
- macOS + Docker Desktop Kubernetes
- Linux + Kind
- Amazon EKS
- Remote Kubernetes clusters

The original kubeconfig is NEVER modified.

A runtime kubeconfig is generated at:

    /tmp/kube/config
"""

from __future__ import annotations

import json
import os
import shutil
import socket
import subprocess
from pathlib import Path
from urllib.parse import urlparse, urlunparse

import yaml


# =====================================================
# Paths
# =====================================================

SOURCE_CONFIG = Path("/root/.kube/config")

RUNTIME_DIR = Path("/tmp/kube")

RUNTIME_CONFIG = RUNTIME_DIR / "config"


# =====================================================
# Constants
# =====================================================

LOCALHOSTS = {
    "127.0.0.1",
    "localhost",
    "::1",
}

DOCKER_HOSTNAME = "host.docker.internal"


# =====================================================
# Docker Detection
# =====================================================

def is_running_inside_docker() -> bool:

    if Path("/.dockerenv").exists():
        return True

    try:

        cgroup = Path(
            "/proc/1/cgroup"
        ).read_text(errors="ignore")

        return (
            "docker" in cgroup.lower()
            or "containerd" in cgroup.lower()
        )

    except Exception:

        return False


def docker_cli_available() -> bool:

    return shutil.which("docker") is not None


# =====================================================
# Docker Helpers
# =====================================================

def run_docker(args: list[str]) -> str | None:

    if not docker_cli_available():
        return None

    try:

        result = subprocess.run(
            ["docker", *args],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )

        if result.returncode != 0:
            return None

        return result.stdout.strip()

    except Exception:

        return None


def get_current_container_id() -> str | None:
    """
    Inside Docker, /etc/hostname normally contains
    the container ID.
    """

    try:

        container_id = Path(
            "/etc/hostname"
        ).read_text().strip()

        return container_id or None

    except Exception:

        return None


# =====================================================
# Docker Host Detection
# =====================================================

def host_docker_internal_available() -> bool:

    try:

        socket.gethostbyname(DOCKER_HOSTNAME)

        return True

    except socket.gaierror:

        return False


# =====================================================
# Active Cluster Detection
# =====================================================

def get_active_cluster_info(
    config_text: str,
) -> tuple[str | None, str | None, str | None]:

    try:

        config = yaml.safe_load(config_text)

    except yaml.YAMLError:

        return None, None, None

    if not isinstance(config, dict):

        return None, None, None

    current_context = config.get("current-context")

    if not current_context:

        return None, None, None

    cluster_name = None

    for item in config.get("contexts", []):

        if item.get("name") == current_context:

            cluster_name = (
                item.get("context", {})
                .get("cluster")
            )

            break

    if not cluster_name:

        return current_context, None, None

    server = None

    for item in config.get("clusters", []):

        if item.get("name") == cluster_name:

            server = (
                item.get("cluster", {})
                .get("server")
            )

            break

    return (
        current_context,
        cluster_name,
        server,
    )


def is_kind_context(
    current_context: str | None,
    cluster_name: str | None,
) -> bool:

    values = [
        current_context,
        cluster_name,
    ]

    for value in values:

        if value and value.lower().startswith("kind-"):
            return True

    return False


def is_eks_cluster(
    current_context: str | None,
    cluster_name: str | None,
    server: str | None,
) -> bool:

    values = [
        current_context,
        cluster_name,
        server,
    ]

    for value in values:

        if not value:
            continue

        value = value.lower()

        if "eks.amazonaws.com" in value:
            return True

        if "arn:aws:eks" in value:
            return True

    return False


# =====================================================
# URL Helpers
# =====================================================

def is_localhost_server(server: str) -> bool:

    try:

        hostname = urlparse(server).hostname

        return hostname in LOCALHOSTS

    except Exception:

        return False


def replace_server_host(
    server: str,
    hostname: str,
    port: int | None = None,
) -> str:

    parsed = urlparse(server)

    final_port = (
        port
        if port is not None
        else parsed.port
    )

    netloc = hostname

    if final_port:

        netloc = f"{hostname}:{final_port}"

    return urlunparse(
        (
            parsed.scheme,
            netloc,
            parsed.path,
            parsed.params,
            parsed.query,
            parsed.fragment,
        )
    )


# =====================================================
# Docker Desktop
# =====================================================

def rewrite_docker_desktop(server: str) -> str:

    if not host_docker_internal_available():
        return server

    parsed = urlparse(server)

    return replace_server_host(
        server,
        DOCKER_HOSTNAME,
        parsed.port,
    )


# =====================================================
# Kind Discovery
# =====================================================

def discover_kind_control_plane(
    current_context: str,
) -> tuple[str, str] | None:
    """
    Returns:

        (
            network_name,
            control_plane_ip
        )

    Example:

        ("kind", "172.18.0.2")
    """

    cluster = current_context.replace(
        "kind-",
        "",
        1,
    )

    expected_name = f"{cluster}-control-plane"

    output = run_docker(
        [
            "ps",
            "--format",
            "{{.ID}} {{.Names}}",
        ]
    )

    if not output:
        return None

    control_plane_id = None

    for line in output.splitlines():

        parts = line.split()

        if len(parts) != 2:
            continue

        cid, name = parts

        if name == expected_name:

            control_plane_id = cid
            break

    if not control_plane_id:

        return None

    inspect_output = run_docker(
        [
            "inspect",
            control_plane_id,
        ]
    )

    if not inspect_output:
        return None

    try:

        data = json.loads(inspect_output)[0]

        networks = (
            data["NetworkSettings"]["Networks"]
        )

        if "kind" in networks:

            ip = networks["kind"]["IPAddress"]

            if ip:

                return "kind", ip

        for network_name, network in networks.items():

            ip = network.get("IPAddress")

            if ip:

                return network_name, ip

    except Exception:

        return None

    return None


# =====================================================
# Attach Backend to Kind Network
# =====================================================

def ensure_network_connected(
    network_name: str,
) -> bool:
    """
    Connect the CURRENT backend container to
    the Kind Docker network if needed.

    This is executed only for an active Kind context.
    """

    container_id = get_current_container_id()

    if not container_id:

        print("Unable to determine current container ID.")

        return False

    inspect_output = run_docker(
        [
            "inspect",
            container_id,
        ]
    )

    if not inspect_output:

        return False

    try:

        data = json.loads(inspect_output)[0]

        networks = (
            data["NetworkSettings"]["Networks"]
        )

        if network_name in networks:

            print(
                f"Backend already connected to Docker network: {network_name}"
            )

            return True

    except Exception:

        return False

    print(
        f"Connecting backend to Docker network: {network_name}"
    )

    result = run_docker(
        [
            "network",
            "connect",
            network_name,
            container_id,
        ]
    )

    if result is None:

        print(
            f"Failed to connect backend to network: {network_name}"
        )

        return False

    print(
        f"Backend successfully connected to network: {network_name}"
    )

    return True


# =====================================================
# TLS Helper
# =====================================================

def apply_docker_desktop_tls(
    config: dict,
    cluster_name: str,
):

    clusters = config.get("clusters", [])

    for item in clusters:

        if item.get("name") != cluster_name:
            continue

        cluster = item.get("cluster", {})

        cluster.pop(
            "certificate-authority-data",
            None,
        )

        cluster.pop(
            "certificate-authority",
            None,
        )

        cluster["insecure-skip-tls-verify"] = True


# =====================================================
# Prepare Runtime Config
# =====================================================

def prepare_kubeconfig() -> Path | None:

    if not SOURCE_CONFIG.exists():

        print("WARNING: Kubernetes kubeconfig not found.")

        print(SOURCE_CONFIG)

        return None

    RUNTIME_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    config_text = SOURCE_CONFIG.read_text()

    try:

        config = yaml.safe_load(config_text)

    except yaml.YAMLError as exc:

        print(f"Invalid kubeconfig: {exc}")

        return None

    (
        current_context,
        cluster_name,
        server,
    ) = get_active_cluster_info(config_text)

    print(f"Current Kubernetes context: {current_context}")
    print(f"Active Kubernetes cluster: {cluster_name}")
    print(f"Active Kubernetes API Server: {server}")

    if not all(
        [
            current_context,
            cluster_name,
            server,
        ]
    ):

        shutil.copy2(
            SOURCE_CONFIG,
            RUNTIME_CONFIG,
        )

        return RUNTIME_CONFIG

    inside_docker = is_running_inside_docker()

    kind_cluster = is_kind_context(
        current_context,
        cluster_name,
    )

    eks_cluster = is_eks_cluster(
        current_context,
        cluster_name,
        server,
    )

    print(f"Running inside Docker: {inside_docker}")
    print(f"Kind cluster detected: {kind_cluster}")
    print(f"EKS cluster detected: {eks_cluster}")

    runtime_server = server

    # =================================================
    # Linux + Kind
    # =================================================

    if (
        inside_docker
        and kind_cluster
        and is_localhost_server(server)
    ):

        discovered = discover_kind_control_plane(
            current_context
        )

        if discovered:

            network_name, control_plane_ip = discovered

            if ensure_network_connected(network_name):

                runtime_server = replace_server_host(
                    server,
                    control_plane_ip,
                    6443,
                )

                print(
                    f"Kind control-plane endpoint: {runtime_server}"
                )

            else:

                print(
                    "WARNING: Could not attach backend to Kind network."
                )

    # =================================================
    # Docker Desktop
    # =================================================

    elif (
        inside_docker
        and not eks_cluster
        and is_localhost_server(server)
        and host_docker_internal_available()
    ):

        runtime_server = rewrite_docker_desktop(server)

        print(
            f"Docker Desktop endpoint: {runtime_server}"
        )

        apply_docker_desktop_tls(
            config,
            cluster_name,
        )

    # =================================================
    # EKS / Remote
    # =================================================

    else:

        print("Preserving Kubernetes endpoint.")

    # =================================================
    # Update ONLY active cluster
    # =================================================

    for item in config.get("clusters", []):

        if item.get("name") == cluster_name:

            item["cluster"]["server"] = runtime_server

            break

    # =================================================
    # Write runtime kubeconfig
    # =================================================

    RUNTIME_CONFIG.write_text(
        yaml.safe_dump(
            config,
            sort_keys=False,
        )
    )

    print(
        f"Runtime kubeconfig created: {RUNTIME_CONFIG}"
    )

    return RUNTIME_CONFIG


# =====================================================
# Main
# =====================================================

def main():

    config = prepare_kubeconfig()

    if config:

        os.environ["KUBECONFIG"] = str(config)

        print(f"KUBECONFIG={config}")


if __name__ == "__main__":

    main()