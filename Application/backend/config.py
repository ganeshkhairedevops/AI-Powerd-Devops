"""
Global Application Configuration

This file centralizes all configurable settings
for the DevOps AI Agent.
"""

# =====================================================
# Application
# =====================================================

APP_NAME = "DevOps AI Agent"

VERSION = "1.0.0"

HOST = "0.0.0.0"

PORT = 8000

DEBUG = True


# =====================================================
# Ollama
# =====================================================

# Development Model
OLLAMA_CHAT_MODEL = "llama3.1:8b"

# Production Model
# OLLAMA_CHAT_MODEL = "qwen3-coder:30b"

OLLAMA_EMBED_MODEL = "nomic-embed-text"


# =====================================================
# RAG
# =====================================================

CHROMA_DB_PATH = "./chroma_db"

UPLOAD_FOLDER = "./uploads"

CHUNK_SIZE = 1000

CHUNK_OVERLAP = 200

TOP_K_RESULTS = 4


# =====================================================
# Memory
# =====================================================

MAX_CHAT_HISTORY = 20

ENABLE_SUMMARIZATION = True


# =====================================================
# API
# =====================================================

API_PREFIX = "/api"


# =====================================================
# Logging
# =====================================================

LOG_LEVEL = "INFO"

LOG_FOLDER = "./logs"