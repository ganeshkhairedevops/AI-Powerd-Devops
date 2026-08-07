"""
Persistent Storage

(Currently in-memory)

Later:
SQLite
PostgreSQL
Redis
MongoDB
"""

import json
from pathlib import Path


MEMORY_FILE = Path("memory_store.json")


def save(data):

    MEMORY_FILE.write_text(
        json.dumps(data, indent=4)
    )


def load():

    if not MEMORY_FILE.exists():

        return {}

    return json.loads(
        MEMORY_FILE.read_text()
    )