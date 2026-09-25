from __future__ import annotations

import os
from pathlib import Path

import numpy as np

from ml.models.dental_age_model import TinyDentalRegressor, train_development_model


def mae(y_true, y_pred):
    return float(np.mean(np.abs(np.asarray(y_true) - np.asarray(y_pred))))


def rmse(y_true, y_pred):
    errors = np.asarray(y_true) - np.asarray(y_pred)
    return float(np.sqrt(np.mean(errors ** 2)))


def r2_score(y_true, y_pred):
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    if ss_tot == 0:
        return 0.0
    return float(1 - (ss_res / ss_tot))


def median_absolute_error(y_true, y_pred):
    return float(np.median(np.abs(np.asarray(y_true) - np.asarray(y_pred))))


def evaluate_predictions(y_true, y_pred):
    return {
        "mae": mae(y_true, y_pred),
        "rmse": rmse(y_true, y_pred),
        "r2": r2_score(y_true, y_pred),
        "median_absolute_error": median_absolute_error(y_true, y_pred),
    }


def ensure_default_model(model_path: str | Path) -> Path:
    model_path = Path(model_path)
    if not model_path.exists():
        train_development_model(model_path)
    return model_path
