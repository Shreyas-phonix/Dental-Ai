from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

import numpy as np
from PIL import Image, ImageOps


@dataclass
class ImageValidationResult:
    valid: bool
    width: int
    height: int
    size_bytes: int
    format: str | None
    error: str | None = None


def validate_image_file(file_path: str | Path, max_size_bytes: int = 20 * 1024 * 1024) -> ImageValidationResult:
    path = Path(file_path)
    if not path.exists():
        return ImageValidationResult(False, 0, 0, 0, None, "File does not exist.")

    file_size = path.stat().st_size
    if file_size == 0:
        return ImageValidationResult(False, 0, 0, file_size, None, "File is empty.")
    if file_size > max_size_bytes:
        return ImageValidationResult(False, 0, 0, file_size, None, "File is too large.")

    try:
        with Image.open(path) as img:
            img.verify()
    except Exception:
        return ImageValidationResult(False, 0, 0, file_size, None, "The uploaded file could not be processed as an image.")

    try:
        with Image.open(path) as img:
            rgb_img = img.convert("RGB")
            return ImageValidationResult(True, rgb_img.width, rgb_img.height, file_size, rgb_img.format or path.suffix.upper().lstrip("."), None)
    except Exception as exc:
        return ImageValidationResult(False, 0, 0, file_size, None, f"Image validation failed: {exc}")


def preprocess_image(file_path: str | Path, target_size: Tuple[int, int] = (224, 224)) -> np.ndarray:
    path = Path(file_path)
    with Image.open(path) as image:
        img = image.convert("RGB")
        img = ImageOps.grayscale(img)
        img = img.resize(target_size)
        arr = np.asarray(img, dtype=np.float32)
        arr = arr / 255.0
        arr = (arr - 0.5) / 0.5
        return arr


def image_to_tensor(file_path: str | Path, target_size: Tuple[int, int] = (224, 224)) -> "torch.Tensor":
    import torch

    arr = preprocess_image(file_path, target_size)
    tensor = torch.tensor(arr, dtype=torch.float32).unsqueeze(0).unsqueeze(0)
    return tensor
