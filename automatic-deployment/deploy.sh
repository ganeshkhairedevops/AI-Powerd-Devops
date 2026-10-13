#!/usr/bin/env bash
set -Eeuo pipefail

# Configuration is provided by /etc/devops-ai-deploy.env through systemd.
: "${GITHUB_TOKEN:?GITHUB_TOKEN must be set in /etc/devops-ai-deploy.env}"
REPO="${REPO:-ganeshkhairedevops/AI-Powerd-Devops}"
BRANCH="${BRANCH:-feat-github-actions}"
WORKFLOW="${WORKFLOW:-docker-publish.yml}"
APP_DIR="${APP_DIR:-/opt/AI-Powerd-Devops/Application}"
BACKEND_IMAGE="${BACKEND_IMAGE:-ganeshkhaire14/devops-ai-backend}"
FRONTEND_IMAGE="${FRONTEND_IMAGE:-ganeshkhaire14/devops-ai-frontend}"
STATE_DIR="${STATE_DIR:-/var/lib/devops-ai-deploy}"
STATE_FILE="$STATE_DIR/deployed_sha"
PREVIOUS_FILE="$STATE_DIR/previous_sha"

mkdir -p "$STATE_DIR"
chmod 700 "$STATE_DIR"

exec 9>/run/lock/devops-ai-deploy.lock
flock -n 9 || { echo "Another deployment check is running; exiting."; exit 0; }

for cmd in curl jq docker flock; do
    command -v "$cmd" >/dev/null 2>&1 || {
        echo "ERROR: Required command not found: $cmd" >&2
        exit 1
    }
done

if [[ ! -f "$APP_DIR/docker-compose.yml" || ! -f "$APP_DIR/docker-compose.deploy.yml" ]]; then
    echo "ERROR: Expected docker-compose.yml and docker-compose.deploy.yml in $APP_DIR" >&2
    exit 1
fi

API_URL="https://api.github.com/repos/$REPO/actions/workflows/$WORKFLOW/runs?branch=$BRANCH&per_page=1"
RUN_JSON="$(curl --retry 2 --retry-delay 2 -fsS \
    -H "Accept: application/vnd.github+json" \
    -H "Authorization: Bearer $GITHUB_TOKEN" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    "$API_URL")"

RUN_STATUS="$(jq -r '.workflow_runs[0].status // "missing"' <<< "$RUN_JSON")"
RUN_RESULT="$(jq -r '.workflow_runs[0].conclusion // "none"' <<< "$RUN_JSON")"
RUN_BRANCH="$(jq -r '.workflow_runs[0].head_branch // ""' <<< "$RUN_JSON")"
SHA="$(jq -r '.workflow_runs[0].head_sha // ""' <<< "$RUN_JSON")"

if [[ "$RUN_BRANCH" != "$BRANCH" ||
      "$RUN_STATUS" != "completed" ||
      "$RUN_RESULT" != "success" ||
      ! "$SHA" =~ ^[0-9a-f]{40}$ ]]; then
    echo "Latest publishing workflow is not successful; skipping deployment."
    exit 0
fi

CURRENT_SHA=""
if [[ -f "$STATE_FILE" ]]; then
    CURRENT_SHA="$(cat "$STATE_FILE")"
fi

if [[ "$SHA" == "$CURRENT_SHA" ]]; then
    echo "Already deployed $SHA"
    exit 0
fi

cd "$APP_DIR"
export DEPLOY_SHA="$SHA"

echo "Checking image manifests for $SHA"
docker manifest inspect "$BACKEND_IMAGE:$SHA" >/dev/null
docker manifest inspect "$FRONTEND_IMAGE:$SHA" >/dev/null

# Capture the running SHA-tagged image pair before replacing containers.
OLD_BACKEND="$(docker inspect -f '{{.Config.Image}}' devops-ai-backend 2>/dev/null || true)"
OLD_FRONTEND="$(docker inspect -f '{{.Config.Image}}' devops-ai-frontend 2>/dev/null || true)"
OLD_SHA=""

if [[ "$OLD_BACKEND" == "$BACKEND_IMAGE:"* &&
      "$OLD_FRONTEND" == "$FRONTEND_IMAGE:"* ]]; then
    OLD_BACKEND_SHA="${OLD_BACKEND#"$BACKEND_IMAGE:"}"
    OLD_FRONTEND_SHA="${OLD_FRONTEND#"$FRONTEND_IMAGE:"}"
    if [[ "$OLD_BACKEND_SHA" == "$OLD_FRONTEND_SHA" &&
          "$OLD_BACKEND_SHA" =~ ^[0-9a-f]{40}$ ]]; then
        OLD_SHA="$OLD_BACKEND_SHA"
    fi
fi

echo "Pulling backend and frontend for $SHA"
docker compose -f docker-compose.yml -f docker-compose.deploy.yml pull backend frontend

echo "Deploying $SHA"
docker compose -f docker-compose.yml -f docker-compose.deploy.yml up -d --no-build backend frontend

HEALTHY=0
for attempt in $(seq 1 18); do
    if curl -fsS http://127.0.0.1:8000/docs >/dev/null &&
       curl -fsS http://127.0.0.1:3000/ >/dev/null; then
        HEALTHY=1
        break
    fi
    sleep 5
done

if [[ "$HEALTHY" -eq 1 ]]; then
    if [[ -n "$CURRENT_SHA" ]]; then
        printf '%s\n' "$CURRENT_SHA" > "$PREVIOUS_FILE"
    elif [[ -n "$OLD_SHA" ]]; then
        printf '%s\n' "$OLD_SHA" > "$PREVIOUS_FILE"
    fi
    printf '%s\n' "$SHA" > "$STATE_FILE"
    echo "Deployment successful: $SHA"
    exit 0
fi

echo "ERROR: Health checks failed for $SHA" >&2

if [[ -n "$OLD_SHA" ]]; then
    echo "Attempting rollback to $OLD_SHA"
    export DEPLOY_SHA="$OLD_SHA"
    if docker manifest inspect "$BACKEND_IMAGE:$OLD_SHA" >/dev/null &&
       docker manifest inspect "$FRONTEND_IMAGE:$OLD_SHA" >/dev/null; then
        docker compose -f docker-compose.yml -f docker-compose.deploy.yml pull backend frontend
        docker compose -f docker-compose.yml -f docker-compose.deploy.yml up -d --no-build backend frontend
        echo "Rollback command completed for $OLD_SHA"
    else
        echo "Previous image manifests unavailable; rollback could not be completed." >&2
    fi
else
    echo "No matching previous SHA-tagged image pair was found; automatic rollback is unavailable." >&2
fi

exit 1
