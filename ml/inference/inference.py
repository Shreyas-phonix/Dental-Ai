from __future__ import annotations

from pathlib import Path

import numpy as np
import torch

from ml.models.dental_age_model import TinyDentalRegressor, GradCAM
from ml.preprocessing.preprocess import image_to_tensor


class DentalAgePredictor:
    def __init__(self, model_path: str | Path, device: str = "cpu"):
        self.device = torch.device(device)
        self.model_path = Path(model_path)
        self.model = TinyDentalRegressor(input_channels=1)
        self.model.load_state_dict(torch.load(self.model_path, map_location=self.device))
        self.model.to(self.device)
        self.model.eval()

    @torch.no_grad()
    def predict(self, image_path: str | Path) -> float:
        tensor = image_to_tensor(image_path, target_size=(224, 224)).to(self.device)
        output = self.model(tensor)
        return float(output.item())

    def gradcam_heatmap(self, image_path: str | Path) -> np.ndarray:
        tensor = image_to_tensor(image_path, target_size=(224, 224)).to(self.device)
        cam = GradCAM(self.model)
        heatmap = cam.generate(tensor)
        return heatmap


def ensure_model_exists(model_path: str | Path) -> Path:
    model_path = Path(model_path)
    if model_path.exists():
        return model_path

    model_path.parent.mkdir(parents=True, exist_ok=True)
    from ml.models.dental_age_model import train_development_model

    train_development_model(model_path)
    return model_path
