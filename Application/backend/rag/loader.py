"""
Document Loader

Loads supported DevOps files.

Supported formats:

- TXT
- Markdown
- YAML / YML
- JSON
- Terraform
- Logs
- Shell scripts
- Dockerfile
- *.dockerfile
"""

from pathlib import Path


# =====================================================
# Supported Extensions
# =====================================================

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


# =====================================================
# Document Loader
# =====================================================

class DocumentLoader:
    """
    Loads supported DevOps documents as text.
    """

    # =================================================
    # Load
    # =================================================

    def load(
        self,
        filepath: str,
    ):

        path = Path(filepath)


        # -------------------------------------------------
        # File existence
        # -------------------------------------------------

        if not path.exists():

            raise FileNotFoundError(
                filepath
            )


        if not path.is_file():

            raise ValueError(
                f"Path is not a file: {filepath}"
            )


        # -------------------------------------------------
        # Filename
        # -------------------------------------------------

        filename = path.name.lower()


        # -------------------------------------------------
        # Normal extension
        # -------------------------------------------------

        extension = (
            path.suffix.lower()
        )


        # -------------------------------------------------
        # Dockerfile support
        #
        # Dockerfile normally has NO extension.
        #
        # Examples:
        #
        # Dockerfile
        # dockerfile
        # Dockerfile.dev
        # Dockerfile.prod
        # nginx.dockerfile
        #
        # -------------------------------------------------

        is_dockerfile = (

            filename == "dockerfile"

            or filename.startswith(
                "dockerfile."
            )

            or extension == ".dockerfile"

        )


        # -------------------------------------------------
        # Validate file type
        # -------------------------------------------------

        if (
            extension
            not in SUPPORTED_EXTENSIONS
            and not is_dockerfile
        ):

            raise ValueError(
                f"Unsupported file type: "
                f"{extension or path.name}"
            )


        # -------------------------------------------------
        # Read file
        # -------------------------------------------------

        return path.read_text(
            encoding="utf-8",
            errors="ignore",
        )


# =====================================================
# Singleton
# =====================================================

loader = DocumentLoader()