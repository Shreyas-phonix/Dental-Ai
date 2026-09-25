from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel, Field


class HistoryItem(BaseModel):
    id: str
    predicted_age: float | None
    uncertainty: str | None = None
    model_version: str = "1.0.0-dev"
    created_at: str
    status: str = "completed"
    original_filename: str | None = None


class PredictionResponse(BaseModel):
    id: str
    predicted_age: float
    uncertainty: str | None = None
    model_version: str = "1.0.0-dev"
    explanation_available: bool = True
    heatmap_url: str | None = None
    created_at: str
    status: str = "completed"
