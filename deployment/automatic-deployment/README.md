# Automatic Deployment with GitHub Actions and systemd

This folder contains the server-side polling deployment setup for the DevOps AI Agent.

## How it works

1. A developer pushes to the configured Git branch.
2. GitHub Actions runs the `docker-publish.yml` workflow.
3. The workflow publishes backend and frontend images tagged with the commit SHA.
4. A Linux systemd timer checks the latest publishing workflow every five minutes.
5. When the latest workflow is successful and the SHA has not already been deployed, the server pulls both images and updates the containers.
6. The script checks `http://127.0.0.1:8000/docs` and `http://127.0.0.1:3000/`.
7. If the HTTP checks fail, it attempts rollback only when it can identify a matching previous SHA-tagged image pair.

The deployment uses `Application/docker-compose.yml` and `Application/docker-compose.deploy.yml`. The override file must be tracked in Git.

## Requirements

- Linux server with systemd.
- Docker Engine and Docker Compose v2 installed and working.
- `curl`, `jq`, and `flock` available.
- Network access to GitHub API and Docker Hub.
- The backend and frontend images published to Docker Hub with commit-SHA tags.
- A GitHub fine-grained personal access token with access to this repository and **Actions: Read-only** permission. Do not use or commit an organization/server's personal secret.
- Ports 3000 and 8000 reachable locally on the server for the configured HTTP checks.

For a public repository, the workflow API endpoint may allow unauthenticated access, but this configuration uses a token for consistent access. Keep the token private.

## Repository configuration

Review `Application/docker-compose.deploy.yml`. It should refer to the SHA variable:

```yaml
services:
  backend:
    image: ganeshkhaire14/devops-ai-backend:${DEPLOY_SHA}

  frontend:
    image: ganeshkhaire14/devops-ai-frontend:${DEPLOY_SHA}
```

If your Docker Hub namespaces, workflow filename, branch, container names, ports, or endpoints differ, update the environment settings and script before enabling the timer.

## Install on a new Linux server

### 1. Clone the project

```bash
git clone --branch feat-github-actions https://github.com/ganeshkhairedevops/AI-Powerd-Devops.git
cd AI-Powerd-Devops
```

Use the intended branch for your deployment.

### 2. Install the systemd files

Run the installer with the absolute path to the repository:

```bash
sudo bash deployment/automatic-deployment/install.sh "$PWD"
```

The installer copies:
- `deploy.sh` to `/usr/local/lib/devops-ai-deploy/deploy.sh`
- the service to `/etc/systemd/system/devops-ai-deploy.service`
- the timer to `/etc/systemd/system/devops-ai-deploy.timer`
- the example environment file to `/etc/devops-ai-deploy.env` only if that file does not already exist

It does not overwrite an existing `/etc/devops-ai-deploy.env`.

### 3. Configure the environment securely

```bash
sudo nano /etc/devops-ai-deploy.env
```

Set these values for the server:

```bash
GITHUB_TOKEN=YOUR_REAL_TOKEN
REPO=ganeshkhairedevops/AI-Powerd-Devops
BRANCH=feat-github-actions
WORKFLOW=docker-publish.yml
APP_DIR=/absolute/path/to/AI-Powerd-Devops/Application
BACKEND_IMAGE=ganeshkhaire14/devops-ai-backend
FRONTEND_IMAGE=ganeshkhaire14/devops-ai-frontend
STATE_DIR=/var/lib/devops-ai-deploy
```

`APP_DIR` must point to the directory containing both Compose files. Do not add the actual token to Git, README files, shell history, screenshots, or support messages.

Restrict access:

```bash
sudo chown root:root /etc/devops-ai-deploy.env
sudo chmod 600 /etc/devops-ai-deploy.env
```

### 4. Verify the files before enabling the timer

```bash
sudo systemctl cat devops-ai-deploy.service
sudo systemctl cat devops-ai-deploy.timer
sudo test -x /usr/local/lib/devops-ai-deploy/deploy.sh && echo "Deploy script installed"
sudo test -f /etc/devops-ai-deploy.env && echo "Environment file exists"
```

Confirm `APP_DIR`, repository, branch, workflow name, image names, and the image names used by `docker-compose.yml` match your setup.

### 5. Enable the timer and run an initial check

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now devops-ai-deploy.timer
sudo systemctl start devops-ai-deploy.service
```

Check the result:

```bash
systemctl is-enabled devops-ai-deploy.timer
systemctl is-active devops-ai-deploy.timer
systemctl list-timers --all devops-ai-deploy.timer
sudo journalctl -u devops-ai-deploy.service -n 100 --no-pager
```

The first run may deploy the latest successful workflow SHA, or report `Already deployed` if that SHA is already recorded in `/var/lib/devops-ai-deploy/deployed_sha`.

## Verify an automatic deployment

1. Push a change to the configured branch that triggers the Docker publishing workflow.
2. Wait until `docker-publish.yml` completes successfully.
3. Do **not** manually start the service during the test.
4. Watch the log:

```bash
sudo journalctl -u devops-ai-deploy.service -f
```

5. Confirm the running image tags:

```bash
docker inspect -f '{{.Config.Image}}' devops-ai-backend
docker inspect -f '{{.Config.Image}}' devops-ai-frontend
```

Both tags should match the new 40-character commit SHA.

## Operations and troubleshooting

```bash
# Timer state and next execution
systemctl is-active devops-ai-deploy.timer
systemctl list-timers --all devops-ai-deploy.timer

# Recent deployment logs
sudo journalctl -u devops-ai-deploy.service -n 100 --no-pager

# Run a manual diagnostic check (this is not an automatic deployment test)
sudo systemctl start devops-ai-deploy.service

# Stop automatic checks
sudo systemctl disable --now devops-ai-deploy.timer
```

Common messages:
- `Latest publishing workflow is not successful; skipping deployment.` — the latest workflow run returned for the configured branch has not completed successfully; inspect the GitHub Actions run, branch, and workflow name.
- `Already deployed <SHA>` — no action is required; that SHA is already recorded as deployed.
- `curl: (22) ... 401` — replace the invalid/expired GitHub token and verify token permissions.
- `No matching previous SHA-tagged image pair...` — first deployment or previous containers were not using matching SHA-tagged image names; automatic rollback is unavailable in that case.

## Important operational notes

- This mechanism polls GitHub Actions; it is not a webhook and deployment may take up to roughly five minutes after a successful workflow, plus image pull and startup time.
- The script deploys only when the latest workflow run for the configured branch has `status=completed` and `conclusion=success`.
- The health checks confirm HTTP availability only, not full application correctness.
- Rollback is best-effort and requires a matching previous pair of SHA-tagged images.
- The deployment script runs as root because it controls Docker and systemd-managed deployment. Review scripts before running them.
- Keep the server's environment file out of Git. The committed `.env.example` contains only a placeholder.
- The script does not delete application data volumes. Keep a backup strategy for ChromaDB, uploads, and Ollama data.
- Kind/EKS configuration is outside the scope of this deployment folder.
