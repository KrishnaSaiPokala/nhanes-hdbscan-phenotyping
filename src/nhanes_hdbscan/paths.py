"""Path helpers for reproducible local project execution."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable


def project_root(start: str | Path | None = None) -> Path:
    """Return the nearest ancestor containing ``pyproject.toml`` or ``.git``."""
    current = Path(start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (candidate / "pyproject.toml").exists() or (candidate / ".git").exists():
            return candidate
    return current


def resolve_project_path(path: str | Path, root: str | Path | None = None) -> Path:
    """Resolve a path relative to the project root unless it is already absolute."""
    path = Path(path)
    if path.is_absolute():
        return path
    return project_root(root) / path


def ensure_dirs(paths: Iterable[str | Path]) -> list[Path]:
    """Create directories and return them as ``Path`` objects."""
    created: list[Path] = []
    for path in paths:
        directory = Path(path)
        directory.mkdir(parents=True, exist_ok=True)
        created.append(directory)
    return created
