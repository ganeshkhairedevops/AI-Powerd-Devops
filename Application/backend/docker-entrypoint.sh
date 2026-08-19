#!/bin/sh

set -e

echo "=========================================="
echo "DevOps AI Agent - Container Startup"
echo "=========================================="

# =====================================================
# Kubernetes Configuration
# =====================================================

echo "Preparing Kubernetes configuration..."

python -m utils.kubernetes_config

export KUBECONFIG=/tmp/kube/config

echo "KUBECONFIG=${KUBECONFIG}"


# =====================================================
# Start FastAPI
# =====================================================

echo "Starting application..."

exec "$@"