"""
Kubernetes Runtime Configuration

Prepares a kubeconfig for execution from inside the
DevOps AI Agent container.

Behavior:

- Normal Kubernetes endpoints are preserved.
- localhost / 127.0.0.1 endpoints are adapted when
  running inside Docker.
- Kubernetes API port is read directly from kubeconfig.
- Docker Desktop localhost endpoints are handled
  automatically.
"""

from __future__ import annotations

import os
import re
import shutil
import socket
from pathlib import Path
from urllib.parse import urlparse, urlunparse


# =====================================================
# Paths
# =====================================================

SOURCE_CONFIG = Path("/root/.kube/config")

RUNTIME_DIR = Path("/tmp/kube")

RUNTIME_CONFIG = RUNTIME_DIR / "config"


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
        cgroup = Path("/proc/1/cgroup").read_text(
            errors="ignore"
        )

        return (
            "docker" in cgroup
            or "containerd" in cgroup
        )

    except Exception:
        return False


# =====================================================
# Docker Host Detection
# =====================================================

def host_docker_internal_available() -> bool:
    """
    Check whether host.docker.internal can be resolved.
    """

    try:
        socket.gethostbyname(
            "host.docker.internal"
        )

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
    Extract Kubernetes API server from kubeconfig.
    """

    match = re.search(
        r"(?m)^\s*server:\s*(https?://\S+)\s*$",
        config_text,
    )

    if not match:
        return None

    return match.group(1)


# =====================================================
# Rewrite Localhost Endpoint
# =====================================================

def rewrite_localhost_server(
    server: str,
) -> str:
    """
    Convert Docker Desktop localhost Kubernetes
    endpoint to host.docker.internal.

    Example:

        https://127.0.0.1:49237

    becomes:

        https://host.docker.internal:49237
    """

    parsed = urlparse(server)

    if parsed.hostname not in {
        "127.0.0.1",
        "localhost",
        "::1",
    }:

        return server

    if not host_docker_internal_available():

        print(
            "WARNING: host.docker.internal "
            "is unavailable."
        )

        return server

    hostname = "host.docker.internal"

    netloc = hostname

    if parsed.port:

        netloc = (
            f"{hostname}:{parsed.port}"
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
# Prepare Kubeconfig
# =====================================================

def prepare_kubeconfig() -> Path | None:
    """
    Prepare the runtime kubeconfig.

    The original kubeconfig is never modified.
    """

    # -------------------------------------------------
    # Check source configuration
    # -------------------------------------------------

    if not SOURCE_CONFIG.exists():

        print(
            "WARNING: Kubernetes kubeconfig not found:"
        )

        print(
            f"  {SOURCE_CONFIG}"
        )

        return None


    # -------------------------------------------------
    # Create runtime directory
    # -------------------------------------------------

    RUNTIME_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


    # -------------------------------------------------
    # Read kubeconfig
    # -------------------------------------------------

    config_text = SOURCE_CONFIG.read_text(
        encoding="utf-8"
    )


    # -------------------------------------------------
    # Find Kubernetes API server
    # -------------------------------------------------

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


    # -------------------------------------------------
    # Default
    # -------------------------------------------------

    runtime_server = server

    docker_localhost = False


    # -------------------------------------------------
    # Docker environment
    # -------------------------------------------------

    if is_running_inside_docker():

        parsed = urlparse(server)

        # ---------------------------------------------
        # Docker Desktop localhost endpoint
        # ---------------------------------------------

        if (
            parsed.hostname
            in {
                "127.0.0.1",
                "localhost",
                "::1",
            }
            and host_docker_internal_available()
        ):

            runtime_server = (
                rewrite_localhost_server(
                    server
                )
            )

            docker_localhost = True


    # =================================================
    # Rewrite Kubernetes API endpoint
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

    if docker_localhost:

        print(
            "Docker Desktop localhost endpoint detected."
        )


        # ---------------------------------------------
        # Remove certificate-authority-data
        # ---------------------------------------------

        config_text = re.sub(
            r"(?m)^\s*certificate-authority-data:.*\n",
            "",
            config_text,
        )


        # ---------------------------------------------
        # Remove existing insecure setting
        # ---------------------------------------------

        config_text = re.sub(
            r"(?m)^\s*insecure-skip-tls-verify:.*\n",
            "",
            config_text,
        )


        # ---------------------------------------------
        # Add insecure TLS verification
        # ---------------------------------------------

        config_text = re.sub(
            r"(?m)^(\s*server:\s*"
            + re.escape(runtime_server)
            + r"\s*)$",
            r"\1\n    insecure-skip-tls-verify: true",
            config_text,
            count=1,
        )


        print(
            "TLS verification disabled for "
            "Docker Desktop local endpoint."
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