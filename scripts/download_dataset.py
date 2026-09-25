from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ml.inference.inference import DentalAgePredictor, ensure_model_exists


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/run_inference.py path/to/image.jpg")
        raise SystemExit(1)

    image_path = Path(sys.argv[1])
    model_path = ROOT / "ml/weights/best_model.pth"
    ensure_model_exists(model_path)
    predictor = DentalAgePredictor(model_path)
    print(predictor.predict(image_path))
