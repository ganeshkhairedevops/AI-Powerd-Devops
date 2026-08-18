"""
Ollama LLM Configuration

The Ollama endpoint is configurable so the same
application works both locally and inside Docker.
"""

from langchain_ollama import ChatOllama

from config import (
    OLLAMA_CHAT_MODEL,
    OLLAMA_BASE_URL,
)


llm = ChatOllama(
    model=OLLAMA_CHAT_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0,
)

# Ollama LLM configuration this is manual we cang change module

# from langchain_ollama import ChatOllama

# llm = ChatOllama(
#     model="qwen3-coder:30b",
#     temperature=0,
#     num_ctx=8192,
# )
# used for low config systems, like my laptop, and for testing
# llm = ChatOllama(
#     model="qwen2.5-coder:7b",
#     temperature=0,
#     num_ctx=2048,
# )

# llm = ChatOllama(
#     model="llama3.1:8b",
#     temperature=0,
# )