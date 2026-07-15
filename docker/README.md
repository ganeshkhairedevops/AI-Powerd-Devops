# DevOps AI Agent (Kubernetes & Docker Inspector)

A lightweight, local AI agent built with **LangChain** and **Ollama** that uses function calling (tool use) to inspect the live state of your local Kubernetes clusters and Docker environments. 

## Features
* **Local First**: Runs entirely on your machine using Ollama (default: `qwen3-coder:30b`).
* **Tool Bindings**: Dynamically executes `kubectl` and `docker` CLI commands based on your natural language questions.
* **Smart Analysis**: Automatically highlights problem states like `CrashLoopBackOff`, `Error`, or high restart counts.

## Prerequisites

Before running the agent, ensure you have the following installed and configured:

1. Python 3.10+
2. **Ollama**: Download and install [Ollama](https://ollama.com).
3. **LLM Model**: Pull the required model (or any compatible model of your choice):
   ```bash
   ollama pull qwen3-coder:30b
   ```
4. **CLIs**: Ensure `kubectl` and `docker` are installed and authenticated to a running cluster/daemon.

## Installation

1. Clone this repository or copy the script.
2. Create a virtual env
    ```bash
    python3 -m venv venv
    ```
4. Avtivate env
    ```bash
    source venv/bin/activate
    ```    
4. Install the required dependencies using requirements file:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the agent script using Python:

```bash
python agent.py
```

### Example Prompts to Try:
*  *"how many containers are running"*
* *"Are there any failing pods in my cluster right now?"*
* *"List all my running docker containers."*
* *"Is my database pod healthy?"*

## Architecture & Workflow

1. **System Prompt**: Enforces rules making the LLM rely strictly on live tool outputs rather than hallucinating environment states.
2. **First Pass**: The LLM evaluates your question and determines if it needs to trigger a tool call (`get_pods` or `get_docker_containers`).
3. **Execution**: The script catches the tool request, safely runs the underlying shell subsystem command (`kubectl` or `docker`), and captures the text output.
4. **Second Pass**: The tool results are appended back into the LangChain chat history context, allowing the LLM to generate a concise, human-readable health summary.
