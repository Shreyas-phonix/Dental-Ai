from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import torch

from ml.models.dental_age_model import TinyDentalRegressor, make_synthetic_training_samples


def train_model(model_path: str | Path = "ml/weights/best_model.pth", epochs: int = 8, batch_size: int = 16):
    model = TinyDentalRegressor(input_channels=1)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    criterion = torch.nn.L1Loss()

    X, y = make_synthetic_training_samples(num_samples=256)
    X = torch.tensor(X, dtype=torch.float32).unsqueeze(1)
    y = torch.tensor(y, dtype=torch.float32)

    for _ in range(epochs):
        order = torch.randperm(len(X))
        for start in range(0, len(X), batch_size):
            idx = order[start:start + batch_size]
            xb = X[idx]
            yb = y[idx]
            optimizer.zero_grad()
            preds = model(xb)
            loss = criterion(preds, yb)
            loss.backward()
            optimizer.step()

    path = Path(model_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), path)
    return {"model_path": str(path), "epochs": epochs}


if __name__ == "__main__":
    print(json.dumps(train_model(), indent=2))
