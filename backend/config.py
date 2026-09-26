from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings


ROOT_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    app_name: str = "DentalAge AI"
    # Paths resolved relative to the repository root for robust local development
    model_path: str = str(ROOT_DIR / "ml" / "weights" / "best_model.pth")
    database_url: str = f"sqlite:///{ROOT_DIR / 'backend' / 'dental_ai.db'}"
    upload_dir: str = str(ROOT_DIR / "backend" / "uploads")
    result_dir: str = str(ROOT_DIR / "backend" / "results")
    max_upload_size: int = 20 * 1024 * 1024
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
