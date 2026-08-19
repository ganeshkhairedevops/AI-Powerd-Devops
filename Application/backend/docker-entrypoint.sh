#!/bin/sh

set -e

echo "=========================================="
echo "DevOps AI Agent - Container Startup"
echo "=========================================="

# =====================================================
# Kubernetes Configuration
# =====================================================

mkdir -p /tmp/kube

if [ -f /root/.kube/config ]; then

    echo "Preparing Kubernetes configuration..."

    KUBE_API_HOST="${KUBERNETES_API_HOST:-host.docker.internal}"
    KUBE_API_PORT="${KUBERNETES_API_PORT:-65095}"

    echo "Kubernetes API Host: ${KUBE_API_HOST}"
    echo "Kubernetes API Port: ${KUBE_API_PORT}"

    # Copy kubeconfig
    cp /root/.kube/config /tmp/kube/config

    # Replace Docker Desktop localhost endpoint.
    sed -i \
        "s|https://127\.0\.0\.1:[0-9][0-9]*|https://${KUBE_API_HOST}:${KUBE_API_PORT}|g" \
        /tmp/kube/config

    # Remove certificate authority data.
    sed -i \
        '/certificate-authority-data:/d' \
        /tmp/kube/config

    # Add insecure TLS verification to cluster configuration.
    sed -i \
        '/^[[:space:]]*server:/a\    insecure-skip-tls-verify: true' \
        /tmp/kube/config

    export KUBECONFIG=/tmp/kube/config

    echo "Kubernetes configuration ready."

else

    echo "WARNING: /root/.kube/config not found."
    echo "Kubernetes Agent will not be available."

fi


# =====================================================
# Start FastAPI
# =====================================================

echo "Starting application..."

exec "$@"