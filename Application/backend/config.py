"""
Global Application Configuration

This file centralizes all configurable settings
for the DevOps AI Agent.
"""

import os


# =====================================================
# Application
# =====================================================

APP_NAME = "DevOps AI Agent"

VERSION = "1.0.0"

HOST = os.getenv(
    "HOST",
    "0.0.0.0",
)

PORT = int(
    os.getenv(
        "PORT",
        "8000",
    )
)

DEBUG = os.getenv(
    "DEBUG",
    "True",
).lower() == "true"


# =====================================================
# Ollama
# =====================================================

# Chat / Agent model
#
# Local:
#   llama3.1:8b
#
# Docker:
#   Can be overridden using OLLAMA_CHAT_MODEL

OLLAMA_CHAT_MODEL = os.getenv(
    "OLLAMA_CHAT_MODEL",
    "llama3.1:8b",
)


# Embedding model used by RAG

OLLAMA_EMBED_MODEL = os.getenv(
    "OLLAMA_EMBED_MODEL",
    "nomic-embed-text",
)


# Ollama server URL
#
# Local development:
#   http://localhost:11434
#
# Docker Compose:
#   http://ollama:11434
#
# Docker Compose overrides this using
# the OLLAMA_BASE_URL environment variable.

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434",
)


# =====================================================
# RAG
# =====================================================

CHROMA_DB_PATH = os.getenv(
    "CHROMA_DB_PATH",
    "./chroma_db",
)

UPLOAD_FOLDER = os.getenv(
    "UPLOAD_FOLDER",
    "./uploads",
)

CHUNK_SIZE = int(
    os.getenv(
        "CHUNK_SIZE",
        "1000",
    )
)

CHUNK_OVERLAP = int(
    os.getenv(
        "CHUNK_OVERLAP",
        "200",
    )
)

TOP_K_RESULTS = int(
    os.getenv(
        "TOP_K_RESULTS",
        "4",
    )
)


# =====================================================
# RAG Retrieval Quality
# =====================================================

# Maximum ChromaDB distance score accepted as
# relevant retrieval context.
#
# Lower distance generally means better similarity.

RAG_SCORE_THRESHOLD = float(
    os.getenv(
        "RAG_SCORE_THRESHOLD",
        "0.85",
    )
)


# Maximum number of relevant chunks that can be
# passed to the RAG answer generation.

MAX_RAG_CONTEXT_CHUNKS = int(
    os.getenv(
        "MAX_RAG_CONTEXT_CHUNKS",
        "3",
    )
)


# =====================================================
# Memory
# =====================================================

MAX_CHAT_HISTORY = int(
    os.getenv(
        "MAX_CHAT_HISTORY",
        "20",
    )
)

ENABLE_SUMMARIZATION = os.getenv(
    "ENABLE_SUMMARIZATION",
    "True",
).lower() == "true"


# =====================================================
# API
# =====================================================

API_PREFIX = os.getenv(
    "API_PREFIX",
    "/api",
)


# =====================================================
# Logging
# =====================================================

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO",
)

LOG_FOLDER = os.getenv(
    "LOG_FOLDER",
    "./logs",
)