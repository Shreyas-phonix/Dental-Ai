from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
from PIL import Image


def ensure_dirs(*paths: str | Path) -> None:
    for path in paths:
        Path(path).mkdir(parents=True, exist_ok=True)


def is_supported_image_extension(filename: str) -> bool:
    supported = {".jpg", ".jpeg", ".png", ".bmp"}
    return Path(filename).suffix.lower() in supported


def is_valid_image(file_path: str | Path) -> bool:
    try:
        with Image.open(file_path) as img:
            img.verify()
        return True
    except Exception:
        return False


def safe_filename(filename: str) -> str:
    stem = Path(filename).stem[:80]
    suffix = Path(filename).suffix.lower()
    return f"{stem}_{abs(hash(filename))}{suffix}"
