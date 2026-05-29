"""NHANES public-data URL and download helpers.

Raw NHANES files are intentionally not redistributed in this repository.
These helpers make data acquisition explicit and auditable for users who run
full analyses locally.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.request import urlretrieve
import json

NHANES_BASE_URL = "https://wwwn.cdc.gov/Nchs/Nhanes"


@dataclass(frozen=True)
class NHANESFile:
    """Metadata for one public NHANES XPT file."""

    cycle: str
    component: str
    stem: str

    @property
    def filename(self) -> str:
        """Return the expected XPT filename."""
        return f"{self.stem}.XPT"

    @property
    def url(self) -> str:
        """Return the public NHANES download URL."""
        return f"{NHANES_BASE_URL}/{self.cycle}/{self.component}/{self.filename}"


def download_file(url: str, destination: str | Path, overwrite: bool = False) -> Path:
    """Download a file if needed and return the destination path."""
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and not overwrite:
        return destination
    urlretrieve(url, destination)  # nosec B310 - URL is user-supplied public data source.
    return destination


def download_nhanes_file(spec: NHANESFile, output_dir: str | Path, overwrite: bool = False) -> Path:
    """Download one NHANES file described by ``spec``."""
    output_dir = Path(output_dir)
    return download_file(spec.url, output_dir / spec.filename, overwrite=overwrite)


def write_manifest(files: list[NHANESFile], path: str | Path) -> Path:
    """Write a JSON manifest of expected NHANES source files."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = [asdict(file) | {"filename": file.filename, "url": file.url} for file in files]
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path
