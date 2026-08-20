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
- Any Kubernetes endpoint already reachable from the container

Design principles:

- Never modify the original kubeconfig.
- Preserve remote Kubernetes endpoints.
- Adapt Docker Desktop localhost endpoints.
- Detect Kind dynamically through Docker.
- Do not hardcode Kind ports.
- Do not require platform-specific docker-compose files.
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

KIND_CONTROL_PLANE_NAMES = {
    "control-plane",
}


# =====================================================
# Docker Detection
# =====================================================

def is_running_inside_docker() -> bool:
    """
    Detect whether the application is running inside Docker.
    """

    if Path("/.dockerenv").exists():
        return True

    try:
        cgroup = Path("/proc/1/cgroup").read_text(
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

    return shutil.which("docker") is not None


# =====================================================
# Docker Host Detection
# =====================================================

def host_docker_internal_available() -> bool:
    """
    Check whether host.docker.internal can be resolved.
    """

    try:
        socket.gethostbyname(DOCKER_HOSTNAME)

        return True

    except socket.gaierror:

        return False


# =====================================================
# Kubernetes Server Detection
# =====================================================

def extract_server(
    config_text: str,
) -> str | None:
    """
    Extract the first Kubernetes API server from kubeconfig.

    The current kubeconfig is expected to contain the
    active cluster server near the beginning of the file.
    """

    match = re.search(
        r"(?m)^\s*server:\s*(https?://\S+)\s*$",
        config_text,
    )

    if not match:
        return None

    return match.group(1)


# =====================================================
# Cluster Detection
# =====================================================

def is_kind_cluster(
    config_text: str,
) -> bool:
    """
    Detect whether the kubeconfig contains a Kind cluster.

    This does not depend on a specific Kind version or
    specific API port.
    """

    patterns = (
        r"\bkind-[A-Za-z0-9._-]+",
        r"\bkind-devops\b",
        r"\bkind\b",
    )

    for pattern in patterns:

        if re.search(
            pattern,
            config_text,
            flags=re.IGNORECASE,
        ):

            return True

    return False


def is_eks_cluster(
    config_text: str,
) -> bool:
    """
    Detect Amazon EKS from the kubeconfig.

    EKS endpoints normally contain:
        eks.amazonaws.com
    """

    return (
        "eks.amazonaws.com"
        in config_text.lower()
    )


# =====================================================
# Docker Command Helper
# =====================================================

def run_docker(
    args: list[str],
) -> str | None:
    """
    Execute a Docker CLI command.

    Returns stdout when successful.
    """

    if not docker_cli_available():
        return None

    try:

        result = subprocess.run(
            ["docker", *args],
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

def discover_kind_control_plane() -> tuple[str, int] | None:
    """
    Discover the Kind control-plane container.

    Returns:

        (container_ip, api_port)

    Example:

        ("172.18.0.2", 6443)

    This dynamically discovers the container instead
    of assuming a host port such as 33093.
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
                .get("NetworkSettings", {})
                .get("Networks", {})
            )

            container_ip = None

            for network in networks.values():

                ip = network.get(
                    "IPAddress"
                )

                if ip:
                    container_ip = ip
                    break

            if not container_ip:
                continue

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
# Localhost Endpoint Detection
# =====================================================

def is_localhost_server(
    server: str,
) -> bool:
    """
    Determine whether a Kubernetes server is localhost.
    """

    try:

        hostname = urlparse(
            server
        ).hostname

        return hostname in LOCALHOSTS

    except Exception:

        return False


# =====================================================
# Rewrite Server Hostname
# =====================================================

def replace_server_host(
    server: str,
    hostname: str,
    port: int | None = None,
) -> str:
    """
    Replace hostname and optionally port while preserving
    scheme, path, query and fragment.
    """

    parsed = urlparse(server)

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
    Convert Docker Desktop localhost endpoint to:

        https://host.docker.internal:<port>

    Only used when host.docker.internal is available.
    """

    if not is_localhost_server(server):
        return server

    if not host_docker_internal_available():
        return server

    parsed = urlparse(server)

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
    Rewrite a localhost Kind API endpoint to the
    internal Kind control-plane container.

    Example:

        https://127.0.0.1:33093

    becomes:

        https://172.18.0.2:6443
    """

    if not is_localhost_server(server):
        return None

    control_plane = (
        discover_kind_control_plane()
    )

    if not control_plane:
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
# TLS Configuration
# =====================================================

def add_insecure_tls(
    config_text: str,
    runtime_server: str,
) -> str:
    """
    Disable TLS verification for endpoints where the
    hostname differs from the certificate.

    This is mainly intended for Docker Desktop local
    development.

    Kind normally retains its CA data.
    """

    config_text = re.sub(
        r"(?m)^\s*certificate-authority-data:.*\n",
        "",
        config_text,
    )

    config_text = re.sub(
        r"(?m)^\s*insecure-skip-tls-verify:.*\n",
        "",
        config_text,
    )

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
    Prepare a runtime kubeconfig.

    Original kubeconfig is NEVER modified.
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

    config_text = SOURCE_CONFIG.read_text(
        encoding="utf-8"
    )

    # =================================================
    # Find API server
    # =================================================

    server = extract_server(
        config_text
    )

    if not server:

        print(
            "WARNING: Kubernetes API server "
            "could not be found in kubeconfig."
        )

        shutil.copy2(
            SOURCE_CONFIG,
            RUNTIME_CONFIG,
        )

        return RUNTIME_CONFIG

    print(
        f"Original Kubernetes API Server: {server}"
    )

    runtime_server = server

    docker_desktop_localhost = False

    kind_localhost = False

    # =================================================
    # Environment Detection
    # =================================================

    inside_docker = (
        is_running_inside_docker()
    )

    kind_cluster = is_kind_cluster(
        config_text
    )

    eks_cluster = is_eks_cluster(
        config_text
    )

    print(
        f"Running inside Docker: {inside_docker}"
    )

    print(
        f"Kind cluster detected: {kind_cluster}"
    )

    print(
        f"EKS cluster detected: {eks_cluster}"
    )

    # =================================================
    # Only adapt endpoints inside Docker
    # =================================================

    if inside_docker:

        # =============================================
        # Case 1:
        # Kind on Linux
        # =============================================

        if (
            kind_cluster
            and is_localhost_server(server)
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
        # Case 2:
        # Docker Desktop Kubernetes
        # =============================================

        elif (
            is_localhost_server(server)
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
        # Case 3:
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
        # Case 4:
        # Any other remote Kubernetes
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
    # Rewrite server in runtime config
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
    # Docker Desktop TLS Handling
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

    # =================================================
    # Kind TLS Handling
    # =================================================

    if kind_localhost:

        print(
            "Preserving Kind certificate "
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