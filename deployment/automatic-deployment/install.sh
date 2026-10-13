#!/usr/bin/env bash
set -Eeuo pipefail

# Run from a cloned repository:
# sudo bash deployment/automatic-deployment/install.sh /absolute/path/to/repo
REPO_ROOT="${1:-$(pwd)}"
SOURCE_DIR="$REPO_ROOT/deployment/automatic-deployment"
APP_DIR="$REPO_ROOT/Application"

if [[ ! -f "$SOURCE_DIR/deploy.sh" || ! -f "$APP_DIR/docker-compose.yml" ]]; then
    echo "Usage: sudo bash deployment/automatic-deployment/install.sh /absolute/path/to/repository" >&2
    echo "Could not find deployment files and Application/docker-compose.yml." >&2
    exit 1
fi

if [[ ! -f "$APP_DIR/docker-compose.deploy.yml" ]]; then
    echo "ERROR: Application/docker-compose.deploy.yml is missing. Ensure it is committed to the repository." >&2
    exit 1
fi

for cmd in docker curl jq; do
    command -v "$cmd" >/dev/null 2>&1 || {
        echo "ERROR: Required command not found: $cmd" >&2
        exit 1
    }
done

docker compose version >/dev/null

install -d -m 0755 /usr/local/lib/devops-ai-deploy
install -m 0750 "$SOURCE_DIR/deploy.sh" /usr/local/lib/devops-ai-deploy/deploy.sh
install -m 0644 "$SOURCE_DIR/devops-ai-deploy.service" /etc/systemd/system/devops-ai-deploy.service
install -m 0644 "$SOURCE_DIR/devops-ai-deploy.timer" /etc/systemd/system/devops-ai-deploy.timer

if [[ ! -f /etc/devops-ai-deploy.env ]]; then
    install -m 0600 "$SOURCE_DIR/devops-ai-deploy.env.example" /etc/devops-ai-deploy.env
    echo
    echo "Created /etc/devops-ai-deploy.env from the example."
    echo "Edit it now and replace GITHUB_TOKEN with a real token before enabling the timer:"
    echo "  sudo nano /etc/devops-ai-deploy.env"
else
    echo "Keeping existing /etc/devops-ai-deploy.env."
    chmod 0600 /etc/devops-ai-deploy.env
fi

systemctl daemon-reload

echo
echo "Installed deployment script and systemd units."
echo "IMPORTANT: Verify APP_DIR in /etc/devops-ai-deploy.env matches:"
echo "  $APP_DIR"
echo "Do not enable the timer until the environment file has a valid token and paths."
echo "Then run:"
echo "  sudo systemctl enable --now devops-ai-deploy.timer"
echo "  sudo systemctl start devops-ai-deploy.service"
echo "  sudo journalctl -u devops-ai-deploy.service -n 50 --no-pager"
