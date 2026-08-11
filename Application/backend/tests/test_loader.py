from pathlib import Path

from config import UPLOAD_FOLDER
from rag.loader import loader

filepath = Path(UPLOAD_FOLDER) / "test.yaml"

content = loader.load(str(filepath))

print(content)