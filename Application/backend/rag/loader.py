"""
Document Loader

Loads supported DevOps files.
"""

from pathlib import Path


SUPPORTED_EXTENSIONS = {
    ".txt",
    ".md",
    ".yaml",
    ".yml",
    ".json",
    ".tf",
    ".log",
    ".sh",
    ".dockerfile",
}


class DocumentLoader:

    def load(self, filepath: str):

        path = Path(filepath)

        if not path.exists():
            raise FileNotFoundError(filepath)

        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type: {path.suffix}"
            )

        return path.read_text(
            encoding="utf-8",
            errors="ignore",
        )


loader = DocumentLoader()