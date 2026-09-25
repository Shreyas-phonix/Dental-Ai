from __future__ import annotations

import os
import sqlite3
from pathlib import Path


def initialize_db(db_path: str | Path) -> Path:
    db_file = Path(db_path)
    db_file.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_file)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS analyses (
            id TEXT PRIMARY KEY,
            original_filename TEXT,
            generated_filename TEXT,
            predicted_age REAL,
            uncertainty TEXT,
            model_version TEXT,
            result_path TEXT,
            heatmap_path TEXT,
            created_at TEXT,
            status TEXT,
            notes TEXT
        )
        """
    )
    conn.commit()
    conn.close()
    return db_file


def get_connection(db_path: str | Path):
    return sqlite3.connect(db_path)
