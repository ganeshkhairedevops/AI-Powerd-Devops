# Ollama LLM configuration

from langchain_ollama import ChatOllama

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

llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0,
)