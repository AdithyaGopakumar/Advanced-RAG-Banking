"""
File discovery for the knowledge ingestion pipeline.
"""
from pathlib import Path


def discover_knowledge_files(root_dir: Path) -> list[Path]:
    """
    Recursively discover supported knowledge files (Markdown) in the given directory.

    Args:
        root_dir: The root directory of the knowledge base.

    Returns:
        A deterministically sorted list of Path objects for all .md files.
        
    Raises:
        FileNotFoundError: If the root_dir does not exist.
        NotADirectoryError: If the root_dir is not a directory.
    """
    if not root_dir.exists():
        raise FileNotFoundError(f"Knowledge root directory not found: {root_dir}")
    if not root_dir.is_dir():
        raise NotADirectoryError(f"Knowledge root is not a directory: {root_dir}")

    md_files = []
    for path in root_dir.rglob("*.md"):
        # Ignore files in hidden directories (like .git, .pytest_cache)
        if any(part.startswith(".") for part in path.parts):
            continue
        md_files.append(path)

    # Deterministic sorting
    return sorted(md_files)
