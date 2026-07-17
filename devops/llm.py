# Ollama LLM configuration

from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="qwen3-coder:30b",
    temperature=0,
    num_ctx=8192,
)