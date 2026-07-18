# AI-Powered DevOps Agent

An intelligent, LLM-driven automation system designed to optimize, monitor, and manage DevOps workflows. By leveraging an extensible LLM architecture, custom tooling pipelines, and context-aware prompts, this project functions as an autonomous AI agent capable of handling operations tasks, parsing logs, and managing infrastructure configurations.

##  Key Features

* **LLM Integration Layer**: Flexible Large Language Model orchestration abstraction (`llm.py`) tailored for operational accuracy.
* **Autonomous Agent Engine**: Core agent logic (`agent.py`) capable of reasoning, scheduling tasks, and evaluating environments.
* **Custom Tooling Infrastructure**: Modular ecosystem (`tools/`, `utils/`) allowing the agent to interface with local scripts, cloud APIs, and CI/CD pipelines.
* **Optimized Prompts**: Context-rich templates (`prompts.py`) pre-tuned for typical engineering workflows, incident analysis, and error correction.

---

## Repository Structure

```text
devops/
+-- tools/                 # Executable operational utilities for the agent
+-- utils/                 # General helper functions and logging abstractions
+-- agent.py               # Main agent execution loop and reasoning framework
+-- llm.py                 # Core Large Language Model interface configuration
+-- main.py                # System entry point
+-- prompts.py             # Tailored prompt templates for system behaviors
+-- requirements.txt       # Project dependencies
```

---

##  Getting Started

### Prerequisites

* Python 3.10 or higher

* **Ollama**: Download and install [Ollama](https://ollama.com).
* **LLM Model**: Pull the required model (or any compatible model of your choice) or which is menction in llm.py:
   ```bash
   ollama pull llama3.1:8b
   ```

### Installation

1. Clone the repository and navigate into the `devops` subdirectory:
   ```bash
   git clone 
   cd AI-Powerd-Devops/devops
   ```

2. Create and activate a isolated python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux
   venv\Scripts\activate    # On Windows 
   ```

3. Install all required code dependencies:
   ```bash
   pip install -r requirements.txt
   ```


### Running the Agent

Start the main entry program to spin up the agent initialization terminal:

```bash
python main.py
```

---

##  Project Roadmap (Coming Soon)

We are actively expanding this agent to become a full-suite DevOps platform. Over the next few days, we plan to implement:

* **CI/CD Integrations**: Native connectors for **GitHub Actions**, **Jenkins**, and **GitLab CI** to automate code deployments.
* **Infrastructure as Code (IaC) Assistants**: Deep tool hooks for **Terraform** and **Ansible** to generate and validate cloud configurations automatically.
* **Container Orchestration Support**: Dedicated plugins for **Docker** and **Kubernetes** to audit cluster health, spin up pods, and troubleshoot container crashes.

---

##  Extensibility: Adding Custom Tools

To extend the capabilities of your AI DevOps Agent (e.g., adding an AWS CLI tool or Kubernetes health check script):

1. Drop your functional logic or script inside the `tools/` folder.
2. Provide descriptive system execution contexts inside `prompts.py` so the agent understands **when** and **why** to call it.

---

## Contributing

Contributions are welcome! Please feel free to open a Pull Request, report a bug, or suggest new toolkits to integrate into the framework.


