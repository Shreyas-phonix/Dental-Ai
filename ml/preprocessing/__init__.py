from __future__ import annotations

import os
from pathlib import Path

import numpy as np
from PIL import Image


def load_image(path: str | Path):
    with Image.open(path) as img:
        return np.array(img)


if __name__ == "__main__":
    print("ML preprocessing module loaded.")
