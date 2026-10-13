# 🤖 DevOps AI Agent

A **100% local AI-powered DevOps assistant** built with Python, LangChain, Ollama, FastAPI, React, ChromaDB, and RAG.

The goal is to bring everyday DevOps operations, infrastructure knowledge, and uploaded DevOps documentation into a single local AI assistant.

The application can:

- Answer general DevOps questions
- Execute DevOps tools when live system information is required
- Analyze uploaded DevOps files using RAG
- Store document embeddings locally in ChromaDB
- Keep documents isolated by conversation
- Route questions intelligently between RAG, the DevOps Agent, and the general LLM
- Provide a web-based React interface
- Run locally without requiring a cloud AI API

---

# 🚀 Project Overview

The DevOps AI Agent combines:

```text
                    ┌──────────────────────┐
                    │      React UI        │
                    │      Vite Frontend   │
                    └──────────┬───────────┘
                               │
                               │ HTTP
                               ▼
                    ┌──────────────────────┐
                    │     FastAPI API      │
                    │      Backend         │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │   Question Router    │
                    └──────────┬───────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
        ┌─────────┐       ┌─────────┐      ┌─────────┐
        │   RAG   │       │ Agent   │      │ General │
        └────┬────┘       └────┬────┘      └────┬────┘
             │                 │                 │
             ▼                 ▼                 ▼
        ChromaDB          DevOps Tools          Ollama
             │                 │
             │       ┌─────────┼─────────┐
             │       │         │         │
             │     Docker   Kubernetes  Linux
             │
             │       Git / Helm / Terraform
             │
             │       AWS / Jenkins / Ansible
             │
             │       GitHub / Monitoring
             │
             └──────────────┬──────────────────┘
                            ▼
                       Final Answer
```

---

# ✨ Features

## 🧠 Local LLM

The project uses **Ollama** for local model execution.

The LLM configuration is maintained separately in:

```text
backend/llm.py
```

This makes the model configurable without changing the rest of the application.

---

# 🛠️ DevOps Tools

The agent currently has integrations for:

- Kubernetes
- Docker
- Linux
- Git
- Helm
- Terraform
- AWS
- Jenkins
- Ansible
- GitHub
- Prometheus
- Grafana
- Node Exporter

The tools are organized under:

```text
backend/tools/
```

Examples include:

```text
tools/
├── kubernetes.py
├── docker.py
├── linux.py
├── git.py
├── helm.py
├── terraform.py
├── aws.py
├── jenkins.py
├── ansible.py
├── github.py
└── monitoring.py
```

The agent uses tools only when live infrastructure information or an actual DevOps operation is required.

---

# 📚 RAG Document Intelligence

The application supports uploading DevOps documents and asking questions about them.

Supported file types include:

```text
YAML
YML
JSON
Terraform
Markdown
TXT
LOG
Shell scripts
Dockerfile
*.dockerfile
```

Example:

```text
Dockerfile
test.yaml
deployment.yaml
main.tf
README.md
application.log
```

The document pipeline is:

```text
Upload
   ↓
Document Loader
   ↓
Text Splitter
   ↓
Ollama Embeddings
   ↓
ChromaDB
   ↓
Retriever
   ↓
Relevant Context
   ↓
LLM
   ↓
Answer
```

The embedding model currently used by the RAG pipeline is:

```text
nomic-embed-text
```

---

# 🗂️ Conversation-Isolated Documents

Documents are isolated by:

```text
conversation_id
```

This means documents uploaded in one chat are not automatically retrieved by another chat.

Example:

```text
Chat A
 ├── test.yaml
 └── deployment.yaml

Chat B
 └── Dockerfile
```

Questions in Chat A retrieve only Chat A documents.

---

# 🔀 Intelligent Question Routing

The application includes a context-aware question router.

Every question can be routed to one of three paths:

```text
                    Question
                       │
                       ▼
                Question Router
                       │
          ┌────────────┼────────────┐
          │            │            │
          ▼            ▼            ▼
         RAG         AGENT       GENERAL
          │            │            │
          ▼            ▼            ▼
      ChromaDB     DevOps Tools   Ollama
```

## RAG Example

```text
Which image is used by the pod?
```

If the uploaded YAML contains:

```yaml
containers:
  - name: nginx
    image: nginx
```

the question is routed to RAG.

---

## Agent Example

```text
Show running Docker containers
```

The question is routed to the DevOps Agent, which can execute the Docker tool.

---

## General Example

```text
What is Kubernetes?
```

This is a general knowledge question and is handled directly by the LLM.

---

## Live Environment Example

```text
What is the Kubernetes cluster version?
```

This is treated as a live environment question and routed to the DevOps Agent.

The agent can then report the actual environment status instead of inventing a version.

---

# 🔄 RAG Fallback

If a question is routed to RAG but the uploaded documents do not contain enough information, the system can fall back to the DevOps Agent.

```text
Question
   ↓
RAG
   ↓
Enough context?
   │
   ├── YES → Answer from document
   │
   └── NO
        ↓
      Agent
        ↓
   Live DevOps tools
```

This prevents the document assistant from fabricating information.

---

# 💬 Conversation Memory

The backend maintains conversation history using the project's memory layer.

Conversation messages are associated with:

```text
conversation_id
```

This allows multiple independent chats to maintain separate context.

---

# 📄 Document Management

The frontend supports:

```text
Upload document
      ↓
Index document
      ↓
Display document
      ↓
Show chunk count
      ↓
Delete document
```

The backend provides:

```text
POST   /upload

GET    /documents/{conversation_id}

DELETE /documents/{conversation_id}/{filename}
```

---

# 🖥️ Frontend

The frontend is built using:

- React
- Vite
- JavaScript
- Tailwind CSS
- Axios
- React Icons

Main frontend components include:

```text
frontend/src/

├── components/
│   ├── ChatWindow.jsx
│   ├── FileUpload.jsx
│   ├── DocumentList.jsx
│   ├── Message.jsx
│   ├── PromptBox.jsx
│   └── ConversationHeader.jsx
│
├── context/
│   └── ChatContext.jsx
│
├── hooks/
│   └── useChat.js
│
└── services/
    └── api.js
```

---

# ⚙️ Backend

The backend is built using:

- Python
- FastAPI
- LangChain
- LangChain Ollama
- ChromaDB
- Pydantic

Main structure:

```text
backend/

├── api.py
├── agent.py
├── llm.py
├── prompts.py
├── config.py
│
├── memory/
│
├── rag/
│   ├── loader.py
│   ├── splitter.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── retriever.py
│   └── rag_service.py
│
├── services/
│   └── question_router.py
│
├── tools/
│   ├── kubernetes.py
│   ├── docker.py
│   ├── linux.py
│   ├── git.py
│   ├── helm.py
│   ├── terraform.py
│   ├── aws.py
│   ├── jenkins.py
│   ├── ansible.py
│   ├── github.py
│   └── monitoring.py
│
├── tests/
│
└── uploads/
```

---

# 📋 Prerequisites

Install the following:

### Python

Python 3.10+ recommended.

Verify:

```bash
python --version
```

### Node.js

Verify:

```bash
node --version
npm --version
```

### Ollama

Install Ollama and make sure it is running.

Verify:

```bash
ollama --version
```

---

# 🧠 Ollama Models

Pull the LLM configured by your project.

Example:

```bash
ollama pull qwen3-coder:30b
```

The exact model can be changed in:

```text
backend/llm.py
```

For RAG embeddings:

```bash
ollama pull nomic-embed-text
```

Verify:

```bash
ollama list
```

You should see the configured LLM and:

```text
nomic-embed-text
```

---

# 🔧 Backend Setup

Open a terminal:

```bash
cd Application/backend
```

Create a virtual environment:

### Windows

```powershell
python -m venv venv
```

Activate:

```powershell
.\venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# ▶️ Start Backend

From:

```text
Application/backend
```

run:

```bash
uvicorn api:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/health
```

Expected:

```json
{
  "status": "healthy",
  "agent": "online"
}
```

---

# 🌐 Frontend Setup

Open another terminal:

```bash
cd Application/frontend
```

Install dependencies:

```bash
npm install
```

Start Vite:

```bash
npm run dev
```

Vite will display the local frontend URL, normally:

```text
http://localhost:5173
```

Open that URL in your browser.

---

# 🔗 Application Configuration

The backend configuration is located in:

```text
backend/config.py
```

Example:

```python
APP_NAME = "DevOps AI Agent"

VERSION = "1.0.0"

HOST = "0.0.0.0"

PORT = 8000

DEBUG = True
```

LLM configuration is maintained separately in:

```text
backend/llm.py
```

---

# 🧪 Running Tests

Tests are located under:

```text
backend/tests/
```

Run the loader test:

```bash
python -m tests.test_loader
```

Run the splitter test:

```bash
python -m tests.test_splitter
```

Run the embedding test:

```bash
python -m tests.test_embeddings
```

Run the RAG service test:

```bash
python -m tests.test_rag_service
```

Run the question router tests:

```bash
python -m tests.test_question_router
```

The question router currently validates:

```text
RAG
Agent
General
Document-aware routing
Live environment routing
```

---

# 🧪 Example RAG Test

Upload:

```yaml
apiVersion: v1
kind: Pod

metadata:
  name: nginx

spec:
  containers:
    - name: nginx
      image: nginx
```

Ask:

```text
Which image is used by the pod?
```

Expected:

```text
The image used by the pod is "nginx".
```

---

# 🐳 Example Docker Test

Ask:

```text
Show running Docker containers
```

The question should be routed to:

```text
Agent → Docker → docker_ps
```

---

# ☸️ Example Kubernetes Test

Ask:

```text
Show running Kubernetes pods
```

The agent will attempt to use the Kubernetes tools available on the machine.

If Kubernetes is not installed or configured, the agent should report the actual error instead of fabricating output.

---

# 🧹 ChromaDB

ChromaDB stores the document vectors locally.

The configured path is controlled by:

```text
backend/config.py
```

If the local ChromaDB data is removed, uploaded documents need to be indexed again.

---

# 🔐 Security Notes

This project is currently designed for local development and learning.

Before production deployment:

- Restrict CORS origins
- Add authentication
- Add authorization
- Validate uploaded files
- Add upload size limits
- Sanitize filenames
- Add structured logging
- Add tool permission controls
- Add command execution safeguards
- Disable development mode
- Protect API endpoints


---

# 🚀 GitHub Actions CI/CD and Automatic Deployment

The project now includes a GitHub Actions-based Docker publishing workflow and server-side automatic deployment polling.

## Deployment workflow

```text
Developer pushes to feat-github-actions
                ↓
       GitHub Actions CI / build
                ↓
   Build and publish Docker images
                ↓
  Publish images tagged with commit SHA
                ↓
 Linux server checks GitHub Actions
       using a systemd timer
       (every five minutes)
                ↓
 Confirm the latest publishing run succeeded
                ↓
 Pull backend and frontend images for that SHA
                ↓
 Update application containers with Docker Compose
                ↓
 Check frontend and backend HTTP endpoints
                ↓
 Record the deployed commit SHA
```

## Container images

The publishing workflow uses these Docker Hub repositories:

- Backend: `ganeshkhaire14/devops-ai-backend`
- Frontend: `ganeshkhaire14/devops-ai-frontend`

Images are published with both a `latest` tag and a commit-SHA tag. The automated deployment uses the commit-SHA tags so the backend and frontend can be deployed from the same Git commit.

## Version-controlled deployment files

The reusable server deployment templates are maintained in:

```text
deployment/automatic-deployment/
├── deploy.sh
├── devops-ai-deploy.service
├── devops-ai-deploy.timer
├── devops-ai-deploy.env.example
├── install.sh
└── README.md
```

These files let another project user install the server-side polling setup without manually recreating files under `/usr/local/lib` and `/etc/systemd/system`. The actual secret file `/etc/devops-ai-deploy.env` is created/configured on each server and must never be committed.

### Install on another Linux server

After cloning the repository and ensuring Docker Compose plus the SHA-based `Application/docker-compose.deploy.yml` are present:

```bash
git clone --branch feat-github-actions https://github.com/ganeshkhairedevops/AI-Powerd-Devops.git
cd AI-Powerd-Devops
sudo bash deployment/automatic-deployment/install.sh "$PWD"
sudo nano /etc/devops-ai-deploy.env
```

Set a valid GitHub token and update `APP_DIR` to the absolute path of that clone's `Application` directory. Then secure the file and enable the timer:

```bash
sudo chown root:root /etc/devops-ai-deploy.env
sudo chmod 600 /etc/devops-ai-deploy.env
sudo systemctl enable --now devops-ai-deploy.timer
sudo systemctl start devops-ai-deploy.service
sudo journalctl -u devops-ai-deploy.service -n 100 --no-pager
```

Read `deployment/automatic-deployment/README.md` before installation for requirements, configuration, verification, troubleshooting, and rollback limitations.

## Server deployment configuration

The deployment setup uses:

- `Application/docker-compose.yml` for the main application Compose configuration.
- `Application/docker-compose.deploy.yml` as a Compose override for SHA-tagged backend and frontend images.
- `/usr/local/lib/devops-ai-deploy/deploy.sh` to query GitHub Actions, pull images, deploy, and check HTTP availability.
- `/etc/systemd/system/devops-ai-deploy.service` as the one-shot deployment service.
- `/etc/systemd/system/devops-ai-deploy.timer` to trigger periodic checks.
- `/etc/devops-ai-deploy.env` for the GitHub token used by the server. This file must remain private and must never be committed to Git.

The systemd timer is configured with `OnBootSec=2min` and `OnUnitActiveSec=5min`. The timer is enabled and active on the deployment server. A check skips deployment when the latest publishing workflow has not completed successfully or when its commit SHA is already deployed.

## Useful deployment verification commands

Check the timer and its next activation:

```bash
systemctl is-enabled devops-ai-deploy.timer
systemctl is-active devops-ai-deploy.timer
systemctl list-timers --all devops-ai-deploy.timer
```

Follow deployment logs:

```bash
sudo journalctl -u devops-ai-deploy.service -f
```

Check the image tags used by the running containers:

```bash
docker inspect -f '{{.Config.Image}}' devops-ai-backend
docker inspect -f '{{.Config.Image}}' devops-ai-frontend
```

Check the application endpoints from the server:

```bash
curl -I http://127.0.0.1:3000/
curl -I http://127.0.0.1:8000/docs
```

The HTTP checks verify endpoint availability; they are not a complete end-to-end application test.

## Verified deployment progress

- [x] GitHub Actions publishing workflow completed successfully for commit `d20e40d4a3514a77f9934d7a657e4d889a65b69d`.
- [x] Backend and frontend images for that commit were published to Docker Hub.
- [x] Server-side deployment pulled and started both SHA-tagged images.
- [x] Deployment log reported `Deployment successful` for that commit.
- [x] A subsequent scheduled check detected the same commit and skipped a redundant deployment.
- [x] The systemd deployment timer was verified as enabled and active.

The next end-to-end verification is to push another change that triggers the publishing workflow and confirm the timer deploys that new SHA without manually starting the deployment service.

> **Security note:** Do not commit GitHub tokens, environment files, credentials, or production secrets. Keep the server's deployment environment file restricted to root access.

---

# 🗺️ Current Development Status

## Completed

- [x] Local LLM integration
- [x] LangChain DevOps Agent
- [x] Docker tools
- [x] Kubernetes tools
- [x] Linux tools
- [x] Git tools
- [x] Helm tools
- [x] Terraform tools
- [x] AWS tools
- [x] Jenkins tools
- [x] Ansible tools
- [x] GitHub tools
- [x] Monitoring tools
- [x] FastAPI backend
- [x] React/Vite frontend
- [x] Conversation memory
- [x] File upload
- [x] Document loader
- [x] Document splitter
- [x] Ollama embeddings
- [x] ChromaDB vector store
- [x] RAG retrieval
- [x] RAG document answering
- [x] Conversation-isolated documents
- [x] Document listing
- [x] Document deletion
- [x] Dockerfile support
- [x] Intelligent question routing
- [x] RAG / Agent / General routing
- [x] RAG fallback to Agent
- [x] Question router tests
- [x] GitHub Actions Docker image publishing workflow
- [x] SHA-tagged backend and frontend images
- [x] Docker Compose deployment using commit-SHA image tags
- [x] Server-side automatic deployment checks with a systemd timer
- [x] HTTP availability checks after deployment

---

# 🎯 Project Goal

The long-term goal is to build a **fully local DevOps AI platform** that combines:

```text
AI
+
DevOps Tools
+
RAG
+
Infrastructure Knowledge
+
Conversation Memory
+
Web UI
+
Automation
```

without depending on cloud AI APIs for the core assistant workflow.

---

# 👨‍💻 Author

**Ganesh Khaire**

DevOps Engineer | Cloud | Kubernetes | Automation | AI

GitHub:

```text
https://github.com/ganeshkhairedevops
```

---

# ⭐ Project Status

🚧 **Actively under development**

The project is being built incrementally with real DevOps tools, local AI, RAG, and practical infrastructure workflows.
