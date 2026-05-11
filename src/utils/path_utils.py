"""
Local path utilities — replaces external worksheet-core PathManager dependency.
"""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def resolve(relative_path: str) -> Path:
    """Resolve a relative path against the project root."""
    return PROJECT_ROOT / relative_path
