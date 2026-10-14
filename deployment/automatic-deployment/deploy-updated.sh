
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

# Prevent overlapping deployment checks.
exec 9>/run/lock/devops-ai-deploy.lock
flock -n 9 || {
    echo "Another deployment check is running; exiting."
    exit 0
}

# Verify required commands.
for cmd in curl jq docker flock; do
    command -v "$cmd" >/dev/null 2>&1 || {
        echo "ERROR: Required command not found: $cmd" >&2
        exit 1
    }
done

# Verify application Compose files.
if [[ ! -f "$APP_DIR/docker-compose.yml" ||
      ! -f "$APP_DIR/docker-compose.deploy.yml" ]]; then
    echo "ERROR: Expected Compose files not found in $APP_DIR" >&2
    exit 1
fi

cd "$APP_DIR"

# Query the latest publishing workflow run for the target branch.
API_URL="https://api.github.com/repos/$REPO/actions/workflows/$WORKFLOW/runs?branch=$BRANCH&per_page=1"

RUN_JSON="$(curl --connect-timeout 10 --max-time 30 \
    --retry 2 --retry-delay 2 -fsS \
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

# Read the last successfully deployed SHA.
CURRENT_SHA=""
if [[ -f "$STATE_FILE" ]]; then
    CURRENT_SHA="$(cat "$STATE_FILE")"
fi

if [[ "$SHA" == "$CURRENT_SHA" ]]; then
    echo "Already deployed $SHA"
    exit 0
fi

export DEPLOY_SHA="$SHA"

# Verify both commit-specific images before deployment.
echo "Checking image manifests for $SHA"

if ! docker manifest inspect "$BACKEND_IMAGE:$SHA" >/dev/null 2>&1 ||
   ! docker manifest inspect "$FRONTEND_IMAGE:$SHA" >/dev/null 2>&1; then
    echo "ERROR: One or both image manifests are unavailable for $SHA" >&2
    exit 1
fi

# Detect the running SHA-tagged backend/frontend image pair.
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

# Health-check backend and frontend with bounded HTTP requests.
wait_for_health() {
    local attempt

    for attempt in $(seq 1 18); do
        if curl --connect-timeout 3 --max-time 10 -fsS \
             http://127.0.0.1:8000/docs >/dev/null &&
           curl --connect-timeout 3 --max-time 10 -fsS \
             http://127.0.0.1:3000/ >/dev/null; then
            echo "Health checks passed."
            return 0
        fi

        echo "Health check attempt $attempt/18 failed; retrying in 5 seconds."
        sleep 5
    done

    echo "Health checks failed after all attempts." >&2
    return 1
}

# Pull images before replacing the running containers.
echo "Pulling backend and frontend for $SHA"

if ! docker compose \
     -f docker-compose.yml \
     -f docker-compose.deploy.yml \
     pull backend frontend; then
    echo "ERROR: Image pull failed; deployment was not started." >&2
    exit 1
fi

# Deploy and verify the new version.
echo "Deploying $SHA"

if docker compose \
     -f docker-compose.yml \
     -f docker-compose.deploy.yml \
     up -d --no-build backend frontend &&
   wait_for_health; then

    # Record the previous SHA only after the new version is healthy.
    if [[ -n "$OLD_SHA" ]]; then
        printf '%s\n' "$OLD_SHA" > "$PREVIOUS_FILE"
    fi

    # Record the new SHA only after successful health checks.
    printf '%s\n' "$SHA" > "$STATE_FILE"

    echo "Deployment successful: $SHA"
    exit 0
fi

echo "ERROR: Deployment or health checks failed for $SHA" >&2

# Attempt rollback to the previously running image pair.
if [[ -n "$OLD_SHA" ]]; then
    echo "Attempting rollback to $OLD_SHA"
    export DEPLOY_SHA="$OLD_SHA"

    if docker manifest inspect "$BACKEND_IMAGE:$OLD_SHA" >/dev/null 2>&1 &&
       docker manifest inspect "$FRONTEND_IMAGE:$OLD_SHA" >/dev/null 2>&1 &&
       docker compose \
         -f docker-compose.yml \
         -f docker-compose.deploy.yml \
         pull backend frontend &&
       docker compose \
         -f docker-compose.yml \
         -f docker-compose.deploy.yml \
         up -d --no-build backend frontend; then

        if wait_for_health; then
            echo "Rollback successful; health checks passed: $OLD_SHA"

            # Keep state consistent with the version restored.
            printf '%s\n' "$OLD_SHA" > "$STATE_FILE"
        else
            echo "CRITICAL: Rollback was attempted, but health checks failed for $OLD_SHA." >&2
        fi
    else
        echo "CRITICAL: Automatic rollback failed for $OLD_SHA." >&2
    fi
else
    echo "CRITICAL: No matching previous SHA-tagged image pair was found." >&2
    echo "Automatic rollback is unavailable." >&2
fi

exit 1
