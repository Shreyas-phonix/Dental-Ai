from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "DentalAge AI"
    model_path: str = "ml/weights/best_model.pth"
    database_url: str = "sqlite:///./backend/dental_ai.db"
    upload_dir: str = "backend/uploads"
    result_dir: str = "backend/results"
    max_upload_size: int = 20 * 1024 * 1024
    cors_origins: str = "http://localhost:5173"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
