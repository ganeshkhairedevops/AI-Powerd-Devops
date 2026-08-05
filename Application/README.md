#  AI-Powered DevOps Agent

An intelligent AI-powered DevOps Assistant that enables engineers to manage infrastructure using natural language.

Built with **Python**, **LangChain**, **Ollama**, and a modern **Frontend + Backend** architecture, the application can interact with DevOps tools like Docker, Kubernetes, Git, Helm, Terraform, Ansible, Jenkins, and Prometheus—all from a single interface.

---

#  Features

- Local LLM powered by Ollama
- Intelligent LangChain Agent
- Natural Language DevOps Assistant
- Linux Administration
- Docker Management
- Kubernetes Operations
- Git Integration
- Helm Support
- Terraform Commands
- Ansible Automation
- Jenkins Integration
- Prometheus & Grafana Support
- Modular Tool Architecture
- Modern Frontend & Backend Application

---

# Architecture

```
                +----------------------+
                |      Frontend        |
                |   React + Vite UI    |
                +----------+-----------+
                           |
                           |
                    REST API / HTTP
                           |
                +----------v-----------+
                |       Backend        |
                |  FastAPI / Python    |
                +----------+-----------+
                           |
                    LangChain Agent
                           |
                     Ollama (Local LLM)
                           |
        -----------------------------------------
        |      |       |      |      |          |
      Docker  K8s    Git   Helm  Linux   DevOps Tools
        |      |       |      |      |
   Terraform  Jenkins  Ansible  Monitoring
```

---

#  Project Structure

```text
AI-Powerd-Devops/

+-- Application/
¦   +-- frontend/          # React + Vite User Interface
¦   +-- backend/           # FastAPI Backend
¦   +-- README.md
```

---

#  Technology Stack

### AI

- Ollama
- LangChain
- Local LLM

### Backend

- Python
- FastAPI

### Frontend

- React
- Vite
- Axios

### DevOps

- Docker
- Kubernetes
- Git
- Helm
- Terraform
- Ansible
- Jenkins
- Prometheus
- Grafana
- Linux

---

#  Getting Started

## 1. Clone Repository

```bash
git clone https://github.com/ganeshkhairedevops/AI-Powerd-Devops.git

cd AI-Powerd-Devops
```

---

## 2. Install Ollama

Install Ollama and pull your preferred model.

Example:

```bash
ollama pull llama3.1:8b
```

---

## 3. Backend Setup

```bash
cd Application/backend

python -m venv venv

pip install -r requirements.txt

source venv/bin/activate  # Linux

venv\Scripts\activate    # On Windows 

python main.py
```

---

## 4. Frontend Setup

```bash
cd Application/frontend

npm install

npm run dev
```

---

#  Example Prompts

```
Show all running Docker containers

List all Kubernetes Pods

Check disk usage

Show Git branches

List Helm releases

Run Terraform plan

Execute Ansible playbook

Show Jenkins jobs

Check Prometheus targets

Display Grafana dashboards
```

---

### Next Phase

- Chat History
- Session Memory
- RAG Knowledge Base
- Multi-Agent Architecture
- CI/CD Automation

---

#  Contributing

Contributions, issues, and feature requests are welcome.

If you'd like to contribute:

- Fork the repository
- Create a feature branch
- Commit your changes
- Open a Pull Request

---

##  Connect

GitHub:
https://github.com/ganeshkhairedevops

Project:
https://github.com/ganeshkhairedevops/AI-Powerd-Devops
