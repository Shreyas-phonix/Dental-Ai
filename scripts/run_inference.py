from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ml.inference.inference import ensure_model_exists


if __name__ == "__main__":
    model_path = ROOT / "ml/weights/best_model.pth"
    ensure_model_exists(model_path)
    print(f"Model ready at {model_path}")
