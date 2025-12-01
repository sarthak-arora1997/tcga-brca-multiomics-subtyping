"""Central configuration helpers for file locations and commonly used constants."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectConfig:
    """Holds conventional project paths relative to the repository root."""

    root_dir: Path = Path(__file__).resolve().parents[1]

    @property
    def data_dir(self) -> Path:
        return self.root_dir / "data"

    @property
    def raw_data_dir(self) -> Path:
        return self.data_dir / "raw"

    @property
    def processed_data_dir(self) -> Path:
        return self.data_dir / "processed"

    @property
    def notebooks_dir(self) -> Path:
        return self.root_dir / "notebooks"
