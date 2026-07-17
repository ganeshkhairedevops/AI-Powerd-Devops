print("Loading agent.py")
from langchain.agents import create_agent

from llm import llm
from prompts import SYSTEM_PROMPT
from tools.kubernetes import (
    get_pods,
    get_nodes,
    get_services,
    get_deployments,
)

from tools.docker import (
    docker_ps,
    docker_images,
)

from tools.linux import (
    disk_usage,
    memory_usage,
)

# from tools.kubernetes import *
# from tools.docker import *
# from tools.linux import *

agent = create_agent(
    model=llm,
    tools=[
        get_pods,
        get_nodes,
        get_services,
        get_deployments,
        docker_ps,
        docker_images,
        disk_usage,
        memory_usage,
    ],
    system_prompt=SYSTEM_PROMPT,
)