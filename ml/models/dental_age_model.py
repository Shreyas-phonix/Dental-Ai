from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import numpy as np
import torch
from torch import nn


class TinyDentalRegressor(nn.Module):
    def __init__(self, input_channels: int = 1, num_outputs: int = 1):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(input_channels, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d((1, 1)),
        )
        self.regressor = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, num_outputs),
        )

    def forward(self, x):
        x = self.features(x)
        return self.regressor(x).squeeze(-1)


class GradCAM:
    def __init__(self, model: nn.Module, target_layer: str = "features.5"):
        self.model = model
        self.target_layer = target_layer
        self.feature_maps = None
        self.gradients = None

        target_module = self._get_module_by_name(self.target_layer)
        target_module.register_forward_hook(self._forward_hook)
        target_module.register_full_backward_hook(self._backward_hook)

    def _get_module_by_name(self, name: str):
        module = self.model
        for part in name.split("."):
            module = getattr(module, part)
        return module

    def _forward_hook(self, module, inputs, output):
        self.feature_maps = output.detach()

    def _backward_hook(self, module, grad_input, grad_output):
        self.gradients = grad_output[0].detach()

    def generate(self, input_tensor: torch.Tensor, target_index: int | None = None) -> np.ndarray:
        self.model.zero_grad()
        logits = self.model(input_tensor)
        if target_index is None:
            target_index = 0
        logits[target_index].backward(retain_graph=True)

        weights = torch.mean(self.gradients, dim=(2, 3), keepdim=True)
        cam = (weights * self.feature_maps).sum(dim=1, keepdim=True)
        cam = torch.relu(cam)
        cam = cam.squeeze(0).squeeze(0)
        cam = cam.cpu().numpy()
        cam = (cam - cam.min()) / (cam.max() - cam.min() + 1e-8)
        return cam


def make_synthetic_training_samples(num_samples: int = 128) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(42)
    ages = rng.uniform(5, 25, size=num_samples)
    images = np.zeros((num_samples, 224, 224), dtype=np.float32)

    for idx, age in enumerate(ages):
        base = 0.5 + 0.1 * np.sin(age / 2.0)
        for y in range(224):
            for x in range(224):
                distance = ((x - 112) ** 2 + (y - 112) ** 2) ** 0.5
                value = base + 0.25 * np.exp(-distance / 120.0)
                intensity = float(value + 0.02 * rng.normal())
                images[idx, y, x] = np.clip(intensity, 0, 1)

    labels = ages.astype(np.float32)
    return images, labels


def train_development_model(model_path: Path, epochs: int = 6, batch_size: int = 16) -> None:
    model_path.parent.mkdir(parents=True, exist_ok=True)
    model = TinyDentalRegressor(input_channels=1)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = torch.nn.L1Loss()

    X, y = make_synthetic_training_samples(256)
    X = torch.tensor(X, dtype=torch.float32).unsqueeze(1)
    y = torch.tensor(y, dtype=torch.float32)

    model.train()
    for _ in range(epochs):
        indices = torch.randperm(len(X))
        for start in range(0, len(X), batch_size):
            batch_idx = indices[start:start + batch_size]
            xb = X[batch_idx]
            yb = y[batch_idx]
            optimizer.zero_grad()
            preds = model(xb)
            loss = loss_fn(preds, yb)
            loss.backward()
            optimizer.step()

    torch.save(model.state_dict(), model_path)
