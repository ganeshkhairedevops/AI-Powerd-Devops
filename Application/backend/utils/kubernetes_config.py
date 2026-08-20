"""
Universal Kubernetes Runtime Configuration

Prepares a kubeconfig for execution from inside the
DevOps AI Agent container.

Supported environments:

- Docker Desktop Kubernetes
- Linux + Kind
- Amazon EKS
- Other remote Kubernetes clusters
- Local Kubernetes installations

Design principles:

- Never modify the original kubeconfig.
- Always use the CURRENT kubeconfig context.
- Preserve EKS and remote Kubernetes endpoints.
- Adapt Docker Desktop localhost endpoints.
- Detect Kind dynamically through Docker.
- Do not hardcode Kind API ports.
- Generate a separate runtime kubeconfig.
"""

from __future__ import annotations

import json
import os
import re
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
    """
    Detect whether the application is running inside
    a Docker container.
    """

    if Path("/.dockerenv").exists():
        return True

    try:

        cgroup = Path(
            "/proc/1/cgroup"
        ).read_text(
            errors="ignore"
        )

        return (
            "docker" in cgroup.lower()
            or "containerd" in cgroup.lower()
        )

    except Exception:

        return False


# =====================================================
# Docker CLI Detection
# =====================================================

def docker_cli_available() -> bool:
    """
    Check whether Docker CLI is available.
    """

    return shutil.which(
        "docker"
    ) is not None


# =====================================================
# Docker Host Detection
# =====================================================

def host_docker_internal_available() -> bool:
    """
    Check whether host.docker.internal can be resolved.
    """

    try:

        socket.gethostbyname(
            DOCKER_HOSTNAME
        )

        return True

    except socket.gaierror:

        return False


# =====================================================
# Active Kubernetes Context
# =====================================================

def get_active_cluster_info(
    config_text: str,
) -> tuple[
    str | None,
    str | None,
    str | None,
]:
    """
    Get information about the CURRENT kubeconfig context.

    Returns:

        (
            current_context,
            cluster_name,
            server,
        )

    Example:

        (
            "kind-devops",
            "kind-devops",
            "https://127.0.0.1:33093",
        )

    IMPORTANT:

    This function does NOT simply take the first
    server from the kubeconfig.

    It follows:

        current-context
              ?
        matching context
              ?
        cluster
              ?
        server
    """

    try:

        config = yaml.safe_load(
            config_text
        )

    except yaml.YAMLError as exc:

        print(
            "WARNING: Failed to parse kubeconfig:"
        )

        print(
            f"  {exc}"
        )

        return (
            None,
            None,
            None,
        )

    if not isinstance(
        config,
        dict,
    ):

        return (
            None,
            None,
            None,
        )

    # -------------------------------------------------
    # Current context
    # -------------------------------------------------

    current_context = config.get(
        "current-context"
    )

    if not current_context:

        return (
            None,
            None,
            None,
        )

    # -------------------------------------------------
    # Find cluster associated with current context
    # -------------------------------------------------

    cluster_name = None

    contexts = config.get(
        "contexts",
        [],
    )

    for context in contexts:

        if not isinstance(
            context,
            dict,
        ):
            continue

        if context.get(
            "name"
        ) != current_context:

            continue

        context_data = context.get(
            "context",
            {},
        )

        if isinstance(
            context_data,
            dict,
        ):

            cluster_name = (
                context_data.get(
                    "cluster"
                )
            )

        break

    if not cluster_name:

        return (
            current_context,
            None,
            None,
        )

    # -------------------------------------------------
    # Find server for that cluster
    # -------------------------------------------------

    server = None

    clusters = config.get(
        "clusters",
        [],
    )

    for cluster in clusters:

        if not isinstance(
            cluster,
            dict,
        ):
            continue

        if cluster.get(
            "name"
        ) != cluster_name:

            continue

        cluster_data = cluster.get(
            "cluster",
            {},
        )

        if isinstance(
            cluster_data,
            dict,
        ):

            server = (
                cluster_data.get(
                    "server"
                )
            )

        break

    return (
        current_context,
        cluster_name,
        server,
    )


# =====================================================
# Active Cluster Detection
# =====================================================

def is_active_kind_context(
    current_context: str | None,
    cluster_name: str | None,
) -> bool:
    """
    Determine whether the ACTIVE context is a Kind cluster.
    """

    values = [
        current_context,
        cluster_name,
    ]

    for value in values:

        if not value:
            continue

        if value.lower().startswith(
            "kind-"
        ):

            return True

    return False


def is_active_eks_cluster(
    server: str | None,
    cluster_name: str | None,
    current_context: str | None,
) -> bool:
    """
    Determine whether the ACTIVE cluster is EKS.
    """

    values = [
        server,
        cluster_name,
        current_context,
    ]

    for value in values:

        if not value:
            continue

        if (
            "eks.amazonaws.com"
            in value.lower()
        ):

            return True

        if (
            "arn:aws:eks"
            in value.lower()
        ):

            return True

    return False


# =====================================================
# Docker Command Helper
# =====================================================

def run_docker(
    args: list[str],
) -> str | None:
    """
    Execute Docker CLI command.

    Returns stdout when successful.
    """

    if not docker_cli_available():

        return None

    try:

        result = subprocess.run(
            [
                "docker",
                *args,
            ],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )

        if result.returncode != 0:

            return None

        return result.stdout.strip()

    except Exception:

        return None


# =====================================================
# Kind Control Plane Discovery
# =====================================================

def discover_kind_control_plane() -> (
    tuple[str, int] | None
):
    """
    Discover the Kind control-plane container.

    Returns:

        (
            container_ip,
            api_port
        )

    Example:

        (
            "172.18.0.2",
            6443
        )

    Docker socket access is required.
    """

    output = run_docker(
        [
            "ps",
            "--filter",
            "name=control-plane",
            "--format",
            "{{.ID}}",
        ]
    )

    if not output:

        return None

    container_ids = [
        line.strip()
        for line in output.splitlines()
        if line.strip()
    ]

    for container_id in container_ids:

        inspect_output = run_docker(
            [
                "inspect",
                container_id,
            ]
        )

        if not inspect_output:

            continue

        try:

            data = json.loads(
                inspect_output
            )

            if not data:

                continue

            container = data[0]

            networks = (
                container
                .get(
                    "NetworkSettings",
                    {},
                )
                .get(
                    "Networks",
                    {},
                )
            )

            if not networks:

                continue

            # -------------------------------------------------
            # Prefer the Kind network
            # -------------------------------------------------

            preferred_network = (
                networks.get("kind")
            )

            if preferred_network:

                container_ip = (
                    preferred_network.get(
                        "IPAddress"
                    )
                )

                if container_ip:

                    return (
                        container_ip,
                        6443,
                    )

            # -------------------------------------------------
            # Fallback: first available network
            # -------------------------------------------------

            for network in (
                networks.values()
            ):

                container_ip = (
                    network.get(
                        "IPAddress"
                    )
                )

                if container_ip:

                    return (
                        container_ip,
                        6443,
                    )

        except (
            json.JSONDecodeError,
            KeyError,
            TypeError,
        ):

            continue

    return None


# =====================================================
# URL Helpers
# =====================================================

def is_localhost_server(
    server: str,
) -> bool:
    """
    Determine whether a Kubernetes server points
    to localhost.
    """

    try:

        hostname = urlparse(
            server
        ).hostname

        return hostname in LOCALHOSTS

    except Exception:

        return False


def replace_server_host(
    server: str,
    hostname: str,
    port: int | None = None,
) -> str:
    """
    Replace hostname and optionally port while preserving
    the remaining URL components.
    """

    parsed = urlparse(
        server
    )

    final_port = (
        port
        if port is not None
        else parsed.port
    )

    netloc = hostname

    if final_port:

        netloc = (
            f"{hostname}:{final_port}"
        )

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
# Docker Desktop Endpoint
# =====================================================

def rewrite_docker_desktop_endpoint(
    server: str,
) -> str:
    """
    Convert Docker Desktop localhost endpoint:

        https://127.0.0.1:49237

    into:

        https://host.docker.internal:49237
    """

    if not is_localhost_server(
        server
    ):

        return server

    if not host_docker_internal_available():

        print(
            "WARNING: host.docker.internal "
            "is unavailable."
        )

        return server

    parsed = urlparse(
        server
    )

    return replace_server_host(
        server,
        DOCKER_HOSTNAME,
        parsed.port,
    )


# =====================================================
# Kind Endpoint
# =====================================================

def rewrite_kind_endpoint(
    server: str,
) -> str | None:
    """
    Convert a localhost Kind API endpoint into
    the internal Kind control-plane endpoint.

    Example:

        https://127.0.0.1:33093

    becomes:

        https://172.18.0.2:6443
    """

    if not is_localhost_server(
        server
    ):

        return None

    control_plane = (
        discover_kind_control_plane()
    )

    if not control_plane:

        print(
            "WARNING: Kind control-plane "
            "container could not be discovered."
        )

        return None

    container_ip, api_port = (
        control_plane
    )

    return replace_server_host(
        server,
        container_ip,
        api_port,
    )


# =====================================================
# Docker Desktop TLS
# =====================================================

def add_insecure_tls(
    config_text: str,
    runtime_server: str,
) -> str:
    """
    Disable TLS verification for Docker Desktop's
    local Kubernetes endpoint.

    Kind keeps its CA data.
    EKS keeps its CA data.
    """

    # -------------------------------------------------
    # Remove CA data
    # -------------------------------------------------

    config_text = re.sub(
        r"(?m)^\s*certificate-authority-data:.*\n",
        "",
        config_text,
    )

    # -------------------------------------------------
    # Remove existing insecure setting
    # -------------------------------------------------

    config_text = re.sub(
        r"(?m)^\s*insecure-skip-tls-verify:.*\n",
        "",
        config_text,
    )

    # -------------------------------------------------
    # Add insecure TLS
    # -------------------------------------------------

    pattern = (
        r"(?m)^(\s*server:\s*"
        + re.escape(runtime_server)
        + r"\s*)$"
    )

    config_text = re.sub(
        pattern,
        r"\1\n    insecure-skip-tls-verify: true",
        config_text,
        count=1,
    )

    return config_text


# =====================================================
# Prepare Kubeconfig
# =====================================================

def prepare_kubeconfig() -> Path | None:
    """
    Prepare runtime kubeconfig.

    The original kubeconfig is NEVER modified.
    """

    # =================================================
    # Check source configuration
    # =================================================

    if not SOURCE_CONFIG.exists():

        print(
            "WARNING: Kubernetes kubeconfig not found:"
        )

        print(
            f"  {SOURCE_CONFIG}"
        )

        return None

    # =================================================
    # Create runtime directory
    # =================================================

    RUNTIME_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # =================================================
    # Read kubeconfig
    # =================================================

    config_text = (
        SOURCE_CONFIG.read_text(
            encoding="utf-8"
        )
    )

    # =================================================
    # Get ACTIVE cluster information
    # =================================================

    (
        current_context,
        cluster_name,
        server,
    ) = get_active_cluster_info(
        config_text
    )

    print(
        f"Current Kubernetes context: "
        f"{current_context}"
    )

    print(
        f"Active Kubernetes cluster: "
        f"{cluster_name}"
    )

    if not server:

        print(
            "WARNING: Kubernetes API server "
            "could not be found for the "
            "current context."
        )

        shutil.copy2(
            SOURCE_CONFIG,
            RUNTIME_CONFIG,
        )

        return RUNTIME_CONFIG

    print(
        f"Active Kubernetes API Server: "
        f"{server}"
    )

    # =================================================
    # Environment detection
    # =================================================

    inside_docker = (
        is_running_inside_docker()
    )

    kind_cluster = (
        is_active_kind_context(
            current_context,
            cluster_name,
        )
    )

    eks_cluster = (
        is_active_eks_cluster(
            server,
            cluster_name,
            current_context,
        )
    )

    print(
        f"Running inside Docker: "
        f"{inside_docker}"
    )

    print(
        f"Kind cluster detected: "
        f"{kind_cluster}"
    )

    print(
        f"EKS cluster detected: "
        f"{eks_cluster}"
    )

    # =================================================
    # Defaults
    # =================================================

    runtime_server = server

    docker_desktop_localhost = False

    kind_localhost = False

    # =================================================
    # Docker-specific handling
    # =================================================

    if inside_docker:

        # =============================================
        # Kind
        # =============================================

        if (
            kind_cluster
            and is_localhost_server(
                server
            )
        ):

            kind_server = (
                rewrite_kind_endpoint(
                    server
                )
            )

            if kind_server:

                runtime_server = (
                    kind_server
                )

                kind_localhost = True

                print(
                    "Kind cluster detected."
                )

                print(
                    "Kind control-plane endpoint: "
                    f"{runtime_server}"
                )

        # =============================================
        # Docker Desktop Kubernetes
        # =============================================

        elif (
            not eks_cluster
            and is_localhost_server(
                server
            )
            and host_docker_internal_available()
        ):

            runtime_server = (
                rewrite_docker_desktop_endpoint(
                    server
                )
            )

            docker_desktop_localhost = True

            print(
                "Docker Desktop localhost "
                "Kubernetes endpoint detected."
            )

        # =============================================
        # EKS
        # =============================================

        elif eks_cluster:

            print(
                "Amazon EKS endpoint detected."
            )

            print(
                "Preserving EKS endpoint."
            )

        # =============================================
        # Normal remote Kubernetes
        # =============================================

        else:

            print(
                "Remote Kubernetes endpoint "
                "detected."
            )

            print(
                "Preserving Kubernetes endpoint."
            )

    # =================================================
    # Rewrite active server
    # =================================================

    if runtime_server != server:

        print(
            "Container Kubernetes API Server: "
            f"{runtime_server}"
        )

        config_text = config_text.replace(
            server,
            runtime_server,
            1,
        )

    else:

        print(
            "Using Kubernetes API Server: "
            f"{runtime_server}"
        )

    # =================================================
    # Docker Desktop TLS
    # =================================================

    if docker_desktop_localhost:

        print(
            "Applying Docker Desktop local TLS "
            "configuration."
        )

        config_text = add_insecure_tls(
            config_text,
            runtime_server,
        )

        print(
            "TLS verification disabled for "
            "Docker Desktop local endpoint."
        )

    # =================================================
    # Kind TLS
    # =================================================

    if kind_localhost:

        print(
            "Preserving Kind certificate "
            "authority data."
        )

    # =================================================
    # EKS TLS
    # =================================================

    if eks_cluster:

        print(
            "Preserving EKS certificate "
            "authority data."
        )

    # =================================================
    # Write runtime configuration
    # =================================================

    RUNTIME_CONFIG.write_text(
        config_text,
        encoding="utf-8",
    )

    print(
        "Runtime kubeconfig created: "
        f"{RUNTIME_CONFIG}"
    )

    return RUNTIME_CONFIG


# =====================================================
# Main
# =====================================================

def main() -> None:
    """
    Prepare kubeconfig and configure KUBECONFIG.
    """

    config = prepare_kubeconfig()

    if config:

        os.environ[
            "KUBECONFIG"
        ] = str(config)

        print(
            f"KUBECONFIG={config}"
        )


# =====================================================
# Entry Point
# =====================================================

if __name__ == "__main__":

    main()