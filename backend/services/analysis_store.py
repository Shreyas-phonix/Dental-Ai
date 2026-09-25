from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from PIL import Image

from backend.database.db import get_connection
from backend.services.file_validation import safe_filename


def save_upload(upload_file, upload_dir: str | Path) -> tuple[str, str]:
    upload_path = Path(upload_dir)
    upload_path.mkdir(parents=True, exist_ok=True)
    unique_name = safe_filename(upload_file.filename or "upload")
    destination = upload_path / unique_name
    with destination.open("wb") as f:
        f.write(upload_file.file.read())
    return str(destination), unique_name


def record_analysis(db_path: str | Path, record: dict) -> None:
    conn = get_connection(db_path)
    conn.execute(
        """
        INSERT INTO analyses (id, original_filename, generated_filename, predicted_age, uncertainty, model_version, result_path, heatmap_path, created_at, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            record["id"],
            record["original_filename"],
            record["generated_filename"],
            record["predicted_age"],
            record["uncertainty"],
            record["model_version"],
            record["result_path"],
            record["heatmap_path"],
            record["created_at"],
            record["status"],
            record["notes"],
        ),
    )
    conn.commit()
    conn.close()


def list_history(db_path: str | Path):
    conn = get_connection(db_path)
    rows = conn.execute(
        "SELECT id, predicted_age, uncertainty, model_version, created_at, status, original_filename FROM analyses ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return [
        {
            "id": row[0],
            "predicted_age": row[1],
            "uncertainty": row[2],
            "model_version": row[3],
            "created_at": row[4],
            "status": row[5],
            "original_filename": row[6],
        }
        for row in rows
    ]


def get_analysis_by_id(db_path: str | Path, analysis_id: str):
    conn = get_connection(db_path)
    row = conn.execute(
        "SELECT * FROM analyses WHERE id = ?",
        (analysis_id,),
    ).fetchone()
    conn.close()
    if row is None:
        return None
    return {
        "id": row[0],
        "original_filename": row[1],
        "generated_filename": row[2],
        "predicted_age": row[3],
        "uncertainty": row[4],
        "model_version": row[5],
        "result_path": row[6],
        "heatmap_path": row[7],
        "created_at": row[8],
        "status": row[9],
        "notes": row[10],
    }


def delete_analysis(db_path: str | Path, analysis_id: str) -> bool:
    conn = get_connection(db_path)
    cursor = conn.execute("DELETE FROM analyses WHERE id = ?", (analysis_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0
