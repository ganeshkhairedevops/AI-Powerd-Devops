# AI-Powered DevOps Agent — New Machine Deployment Guide

This guide documents the manual deployment test of the AI-Powered DevOps Agent on a separate Ubuntu/Linux machine before changing the existing CI/CD workflows or production server.

## 1. Deployment goals

- Keep the existing server and deployment untouched.
- Test the code from the `feat-github-actions` branch.
- Use Docker Compose for the application, including the Ollama container if it is defined in the Compose file.
- Initially test the frontend, backend, LLM, RAG, and Docker integration.
- Test Kubernetes integration only if a valid kubeconfig and reachable cluster are available.
- Do not modify `Application/backend/Dockerfile` as part of this test.

## 2. Prepare the Ubuntu machine

Check the OS and available resources:

```bash
cat /etc/os-release
uname -m
free -h
df -h /
```

Install basic tools:

```bash
sudo apt update
sudo apt install -y git curl ca-certificates gnupg
```

## 3. Install Docker Engine and Docker Compose

For Ubuntu, add Docker's official package repository and install Docker Engine, Buildx, and the Compose plugin:

```bash
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" \
  | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
newgrp docker
```

Verify:

```bash
sudo docker version
sudo docker compose version
sudo docker run --rm hello-world
```

## 4. Clone the project

```bash
mkdir -p ~/test/AI
cd ~/test/AI
git clone --branch feat-github-actions \
  https://github.com/ganeshkhairedevops/AI-Powerd-Devops.git
cd AI-Powerd-Devops

git branch --show-current
git log -1 --oneline
git status
```

Expected branch: `feat-github-actions`.

If the repository is private, authenticate securely. Do not put a GitHub token in the clone URL or commit tokens to the repository.

## 5. Inspect the application Compose configuration

```bash
cd ~/test/AI/AI-Powerd-Devops/Application
ls -la .env*
sudo docker compose config --services
sudo docker compose config --images
```

Review the Compose file before starting services:

```bash
sed -n '1,180p' docker-compose.yml
```

Use the environment variables and service names that the checked-out configuration actually expects. Do not copy production secrets or commit `.env` files.

## 6. Understanding the `KUBE_CONFIG_PATH` error

The backend service currently has a Kubernetes mount similar to:

```yaml
- ${KUBE_CONFIG_PATH}:/tmp/kube/config:ro
```

If `KUBE_CONFIG_PATH` is unset, Compose expands the mount to an invalid value such as:

```text
:/tmp/kube/config:ro
```
`for Ex`: KUBE_CONFIG_PATH=/root/.kube

This causes an error such as:

```text
WARN: The "KUBE_CONFIG_PATH" variable is not set. Defaulting to a blank string.
invalid spec: :/tmp/kube/config:ro: empty section between colons
```

The source path must be the path to a kubeconfig **file**, because the container destination is `/tmp/kube/config`.

### If Kubernetes is configured on the test machine

Check the kubeconfig file and cluster:

```bash
ls -l /root/.kube/config
kubectl config current-context
kubectl get nodes
```

If the file is valid, set the variable in the Compose environment file used by this project, for example:

```dotenv
KUBE_CONFIG_PATH=/root/.kube/config
```

Use the actual file path on the test machine. Ensure the file is readable by Docker and do not expose its credentials.

### If Kubernetes is not being tested yet

Do not set a fake path and do not create an empty kubeconfig. Use a **test-only Compose override** that removes only the Kubernetes mount while retaining all other backend mounts, including the Docker socket, ChromaDB data, and uploads data.

Important: Compose merges volume lists. Adding another `volumes:` list in an override does not automatically remove the original Kubernetes mount. Inspect the full backend service and use a Compose-version-compatible method to replace/reset the volume list, or create a test-specific Compose file with the complete intended backend volume list. Validate the result before building:

```bash
sudo docker compose -f docker-compose.yml -f docker-compose.test.yml config --quiet
sudo docker compose -f docker-compose.yml -f docker-compose.test.yml config
```

In the resolved configuration, verify that the Kubernetes mount is absent and the required Docker socket and persistent data mounts remain. If the Compose version does not support the chosen override syntax, use a test-specific Compose file that explicitly defines the complete service configuration. Do not change the production Compose file just to test without Kubernetes.

## 7. Ollama and the LLM

If the project's Compose file already defines an Ollama container, there is no need to install Ollama directly on the host. Check the configured services and images:

```bash
sudo docker compose config --services
sudo docker compose config --images
```

Pull configured images and start the stack using the correct Compose files for the test:

```bash
sudo docker compose pull
sudo docker compose up -d
sudo docker compose ps
```

If using a test override, include it in **every** Compose command, for example:

```bash
sudo docker compose -f docker-compose.yml -f docker-compose.test.yml pull
sudo docker compose -f docker-compose.yml -f docker-compose.test.yml up -d
sudo docker compose -f docker-compose.yml -f docker-compose.test.yml ps
```

Check the configured model name in the backend configuration before downloading a model. Pull the model only if it is not already present in the Ollama container's persistent storage. An Ollama image and an LLM model are separate things: pulling the image does not guarantee the model files are present. Preserve the Ollama data volume to avoid unnecessary model downloads.

## 8. Build from source versus pulling published images

Inspect `docker-compose.yml` to see whether backend and frontend services use `build:` or only `image:`.

- `build:` allows Compose to build from the checked-out source.
- `image:` alone pulls/runs the named image; it does not build the local source code.

For a source-code test, make sure the selected Compose configuration actually builds the current checkout. Do not assume `docker compose build` builds services that have only an `image:` declaration.

If the configuration has appropriate build definitions, validate and build:

```bash
sudo docker compose config --quiet
sudo docker compose build
sudo docker compose up -d
```

If a test override is required, include `-f docker-compose.test.yml` as shown above.

## 9. Inspect services and logs

```bash
sudo docker compose ps
sudo docker compose logs --tail=100
```

For live logs:

```bash
sudo docker compose logs -f
```

Press `Ctrl+C` to stop following logs; this does not stop the containers.

Use the actual service names returned by `docker compose config --services` when requesting individual logs.

## 10. Functional test checklist

### Backend

If port 8000 is published by the Compose configuration:

```bash
curl -i http://localhost:8000/docs
```

The FastAPI Swagger page should respond. Test a health endpoint only if the application actually defines one.

### Frontend

If port 3000 is published:

```bash
curl -I http://localhost:3000
```

Open `http://<NEW_MACHINE_IP>:3000` in a browser, replacing the placeholder with the test machine's IP.

### LLM

Send a basic prompt through the frontend and confirm that the backend can reach the configured Ollama service and return a response.

### RAG / ChromaDB

Use the application's supported document-ingestion or knowledge-base feature. Ingest a test document, ask a question about it, and verify retrieval. Confirm that ChromaDB and upload data are stored in persistent volumes.

### Docker agent

Confirm Docker works on the host:

```bash
sudo docker ps
sudo docker images
```

Then test a supported agent prompt such as `Show Docker images`. The backend generally needs access to `/var/run/docker.sock`; this grants significant control over the Docker host, so use it only on a trusted test machine.

### Kubernetes agent (optional)

Kubernetes tests require a valid kubeconfig and reachable cluster. If Kubernetes is not configured, skip this part initially. When configured, test `kubectl config current-context` and `kubectl get nodes` on the host first, then test a supported Kubernetes prompt through the application.


## Kind on the new machine (optional Kubernetes testing)

Kind is **not required** to start the frontend, backend, Ollama, RAG/ChromaDB, or Docker-agent features. Install Kind on the new machine only if you want to test the Kubernetes-agent features against a local Kubernetes cluster. Having Kind installed on the current machine does not make its cluster available to the new machine.

### If you are not testing Kubernetes initially

- Skip Kind and `kubectl` setup for now.
- Use a test-only Compose configuration that removes only the Kubernetes kubeconfig mount while preserving the Docker socket and ChromaDB/uploads volumes.
- Do not set `KUBE_CONFIG_PATH` to a fake path or create an empty kubeconfig.
- Validate the merged configuration and confirm the Kubernetes mount is absent before building or starting the stack.

### If you want to test Kubernetes on the new machine

Install Docker first, then install `kubectl` and Kind by following their official Linux instructions:

- `kubectl`: https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/
- Kind: https://kind.sigs.k8s.io/docs/user/quick-start/

Create a separate test cluster and verify it:

```bash
kind create cluster --name devops-ai-test
kubectl config current-context
kubectl get nodes
kubectl get pods -A
```

Then set `KUBE_CONFIG_PATH` to the actual kubeconfig **file** path on the new machine, for example `/root/.kube/config` when running as root and that file exists. The Compose mount maps this file to `/tmp/kube/config` inside the backend container. Check that the backend is configured to read that same container path and that the cluster endpoint in the kubeconfig is reachable from inside the backend container. A kubeconfig that works on the host may refer to a loopback address or a Kind control-plane container name that is not reachable from the backend container; verify connectivity rather than assuming the mount alone is sufficient.

Do not copy production kubeconfig credentials onto the test machine unless necessary and authorized. Use a dedicated test cluster and least-privilege access where possible.

## 11. Restart and persistence test

After the functional checks pass:

```bash
sudo docker compose restart
sudo docker compose ps
sudo docker compose logs --tail=100
```

Repeat the frontend, backend, and LLM tests. If you use a Compose override, include the same `-f` arguments in these commands.

## 12. Troubleshooting

- **`KUBE_CONFIG_PATH` blank / invalid mount:** set it to a valid kubeconfig file path, or remove the Kubernetes mount using a test-only Compose override that correctly replaces the service's volume list.
- **Backend cannot reach Ollama:** check the Compose service name, network, endpoint configured in the backend, and Ollama logs.
- **Model not found:** list models inside the Ollama container and pull the exact model configured by the application if missing.
- **Frontend cannot reach backend:** check published ports, frontend API configuration, and Nginx logs.
- **Port already in use:** inspect `sudo ss -lntp` for the relevant port and adjust the test deployment configuration.
- **Container exits:** inspect `sudo docker compose logs --tail=200 <service-name>`.
- **Private image pull fails:** authenticate to Docker Hub securely if the configured images are private.

## 13. Keep the test deployment separate

- Do not change the current production server during this test.
- Do not install or enable a second automatic deployment timer yet.
- Do not copy production secrets or production Kubernetes credentials unless required and approved.
- Do not commit `.env`, tokens, kubeconfig files, or local backup files.
- Only after the manual deployment passes should automatic deployment, health checks, and rollback behavior be tested on the new machine.

## Deployment status

Use this checklist to track progress:

- [ ] Docker Engine and Compose installed
- [ ] Repository cloned from `feat-github-actions`
- [ ] Compose configuration validates
- [ ] `KUBE_CONFIG_PATH` handled appropriately for the test
- [ ] Ollama container starts and required model is available
- [ ] Backend responds on its configured port
- [ ] Frontend loads from a browser
- [ ] LLM prompt succeeds
- [ ] RAG retrieval succeeds
- [ ] Docker agent succeeds
- [ ] Kubernetes agent succeeds (optional; only if Kind or another cluster is configured on the new machine)
- [ ] Restart and persistence tests pass
- [ ] Automatic deployment tested separately after manual checks pass
