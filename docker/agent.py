# LLM
import subprocess
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
# Modern LangChain core structural imports
from langchain_core.messages import SystemMessage, HumanMessage

# LLM Configuration 
llm = ChatOllama(
    model="qwen3-coder:30b", # best for coding free locally
    temperature=0,
    num_ctx=8192,
)

# TOOLS
@tool
def get_pods():
    """
    Lists the pods of a running kubernetes cluster
    """
    result = subprocess.run(["kubectl", "get", "pods" ,"-A"], capture_output=True, text=True)
    return result.stdout or result.stderr

@tool
def get_docker_containers():
    """
    Lists the running docker containers
    """
    result = subprocess.run(["docker", "ps"], capture_output=True, text=True)
    return result.stdout or result.stderr

# Bind tools directly to the model 
tools = [get_pods, get_docker_containers]
llm_with_tools = llm.bind_tools(tools)

# SYSTEM PROMPT
system_prompt = (
    "You are a DevOps assistant that inspects live Kubernetes clusters and Docker environments using tools.\n"
    "Tools:\n"
    "- get_pods: lists all pods in all namespaces (kubectl get pods -A).\n"
    "- get_docker_containers: lists running containers (docker ps).\n"
    "Rules:\n"
    "- When a question needs live state, ALWAYS call the relevant tool. Never invent pod or container names.\n"
    "- Answer only from tool output. If a tool returns nothing or an error, say so.\n"
    "- Call out problem states (CrashLoopBackOff, Error, high restarts, Exited) and keep the rest concise."
)

# USER INPUT
question = input("Ask your Kubernetes Agent a Question: > ")

# Construct Messages Array
messages = [
    SystemMessage(content=system_prompt),
    HumanMessage(content=question)
]

print("\n[Agent is thinking and processing tools...]")

# First inference pass
response = llm_with_tools.invoke(messages)

# Check if the LLM decided it needs to run a tool
if response.tool_calls:
    for tool_call in response.tool_calls:
        tool_name = tool_call["name"]
        print(f"[Executing Tool: {tool_name}]")
        
        # Route to the correct tool manually
        if tool_name == "get_pods":
            tool_output = get_pods.invoke(tool_call["args"])
        elif tool_name == "get_docker_containers":
            tool_output = get_docker_containers.invoke(tool_call["args"])
        else:
            tool_output = "Unknown tool requested."
            
        # Append the tool execution history back to the conversation
        messages.append(response)
        from langchain_core.messages import ToolMessage
        messages.append(ToolMessage(content=tool_output, tool_call_id=tool_call["id"]))
        
    # Second inference pass with tool output data injected
    final_response = llm_with_tools.invoke(messages)
    print("\n--- FINAL ANSWER ---")
    print(final_response.content)
else:
    # No tool execution was required
    print("\n--- FINAL ANSWER ---")
    print(response.content)
