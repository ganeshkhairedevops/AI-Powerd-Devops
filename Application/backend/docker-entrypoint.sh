#!/bin/sh

set -e

mkdir -p /tmp/kube

if [ -f /root/.kube/config ]; then

    # Change Docker Desktop Kubernetes API endpoint
    # from localhost to the Docker host.
    sed \
        's#https://127.0.0.1:65095#https://host.docker.internal:65095#g' \
        /root/.kube/config \
        > /tmp/kube/config

    # Remove certificate authority data because
    # we are using insecure-skip-tls-verify for this
    # local Docker Desktop development environment.
    sed -i '/^[[:space:]]*certificate-authority-data:/d' /tmp/kube/config

    # Enable insecure TLS verification.
    sed -i '/server: https:\/\/host.docker.internal:65095/a\    insecure-skip-tls-verify: true' /tmp/kube/config

    export KUBECONFIG=/tmp/kube/config
fi

exec "$@"