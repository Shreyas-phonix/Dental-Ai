from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ml.training.train import train_model


if __name__ == "__main__":
    print("Training model from the project training pipeline...")
    result = train_model(ROOT / "ml/weights/best_model.pth")
    print(result)
