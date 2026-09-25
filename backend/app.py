from __future__ import annotations

import uuid
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

from backend.config import settings
from backend.database.db import initialize_db
from backend.schemas.models import PredictionResponse
from backend.services.analysis_store import delete_analysis, get_analysis_by_id, list_history, record_analysis, save_upload
from backend.services.file_validation import is_supported_image_extension, is_valid_image
from ml.inference.inference import ensure_model_exists, DentalAgePredictor


app = FastAPI(title="DentalAge AI API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

initialize_db(settings.database_url.replace("sqlite:///", "") if settings.database_url.startswith("sqlite:///") else settings.database_url)

UPLOAD_DIR = Path(settings.upload_dir)
RESULT_DIR = Path(settings.result_dir)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
RESULT_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = Path(settings.model_path)
MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
ensure_model_exists(MODEL_PATH)


def create_heatmap_file(source_path: Path, heatmap_array) -> Path:
    import numpy as np
    from PIL import Image

    heatmap = (heatmap_array - heatmap_array.min()) / (heatmap_array.max() - heatmap_array.min() + 1e-8)
    color = np.zeros((heatmap.shape[0], heatmap.shape[1], 3), dtype=np.uint8)
    color[:, :, 0] = np.clip(heatmap * 255, 0, 255)
    color[:, :, 1] = np.clip((1 - heatmap) * 255, 0, 255)
    color[:, :, 2] = np.clip((1 - heatmap) * 80, 0, 255)
    target = RESULT_DIR / f"heatmap_{source_path.stem}_{uuid.uuid4().hex[:8]}.png"
    Image.fromarray(color, mode="RGB").save(target)
    return target


@app.get("/api/v1/health")
def health_check():
    return {
        "status": "ok",
        "app": settings.app_name,
        "model_available": MODEL_PATH.exists(),
        "database": settings.database_url,
    }


@app.post("/api/v1/predict")
async def predict(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file was uploaded.")
    if not is_supported_image_extension(file.filename):
        raise HTTPException(status_code=400, detail="Please upload a JPG, JPEG, or PNG dental X-ray.")

    if file.size and file.size > settings.max_upload_size:
        raise HTTPException(status_code=413, detail="The uploaded file is too large.")

    stored_path, generated_name = save_upload(file, UPLOAD_DIR)
    source_path = Path(stored_path)

    if not is_valid_image(source_path):
        raise HTTPException(status_code=400, detail="The uploaded file could not be processed as an image.")

    try:
        predictor = DentalAgePredictor(MODEL_PATH)
        age = predictor.predict(source_path)
        heatmap = predictor.gradcam_heatmap(source_path)
        heatmap_path = create_heatmap_file(source_path, heatmap)
    except Exception as exc:
        raise HTTPException(status_code=503, detail="The AI model is currently unavailable.") from exc

    analysis_id = str(uuid.uuid4())
    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    record = {
        "id": analysis_id,
        "original_filename": file.filename,
        "generated_filename": generated_name,
        "predicted_age": round(float(age), 2),
        "uncertainty": None,
        "model_version": "1.0.0-dev",
        "result_path": str(source_path),
        "heatmap_path": str(heatmap_path),
        "created_at": created_at,
        "status": "completed",
        "notes": "AI-estimated dental age for research and educational use only.",
    }
    record_analysis(settings.database_url.replace("sqlite:///", "") if settings.database_url.startswith("sqlite:///") else settings.database_url, record)

    response = {
        "id": analysis_id,
        "predicted_age": round(float(age), 2),
        "uncertainty": None,
        "model_version": "1.0.0-dev",
        "explanation_available": True,
        "heatmap_url": f"/results/{heatmap_path.name}",
        "created_at": created_at,
        "status": "completed",
    }
    return response


@app.get("/api/v1/history")
def list_analysis_history():
    db_path = settings.database_url.replace("sqlite:///", "") if settings.database_url.startswith("sqlite:///") else settings.database_url
    return list_history(db_path)


@app.get("/api/v1/history/{analysis_id}")
def get_history_item(analysis_id: str):
    db_path = settings.database_url.replace("sqlite:///", "") if settings.database_url.startswith("sqlite:///") else settings.database_url
    item = get_analysis_by_id(db_path, analysis_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Analysis not found.")
    return item


@app.get("/api/v1/result/{analysis_id}")
def get_result(analysis_id: str):
    db_path = settings.database_url.replace("sqlite:///", "") if settings.database_url.startswith("sqlite:///") else settings.database_url
    item = get_analysis_by_id(db_path, analysis_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Analysis not found.")
    source = Path(item["result_path"])
    if source.exists():
        return FileResponse(source)
    raise HTTPException(status_code=404, detail="Result file not found.")


@app.delete("/api/v1/history/{analysis_id}")
def delete_history_item(analysis_id: str):
    db_path = settings.database_url.replace("sqlite:///", "") if settings.database_url.startswith("sqlite:///") else settings.database_url
    deleted = delete_analysis(db_path, analysis_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Analysis not found.")
    return {"status": "deleted", "id": analysis_id}


@app.get("/results/{image_name}")
def get_result_image(image_name: str):
    file_path = RESULT_DIR / image_name
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Heatmap not found.")
    return FileResponse(file_path)
