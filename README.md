# DentalAge AI

Explainable dental X-ray age-estimation research prototype.

## Current status

The repository contains a React/Vite frontend, FastAPI backend, PyTorch regression inference pipeline, Grad-CAM visualization, SQLite history, Docker scaffolding, documentation, and tests.

The bundled model path is explicitly a **development fallback** generated from synthetic data when real weights are absent. It must not be treated as clinically validated or used for medical, legal, forensic, or identity decisions.

## Run locally

From the repository root:

```powershell
python -m pip install -r .\backend\requirements.txt
python -m uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

In a second PowerShell window:

```powershell
cd .\frontend
npm install
npm run dev
```

Open `http://localhost:5173`. The API health endpoint is `http://localhost:8000/api/v1/health`.

## API

- `GET /api/v1/health`
- `POST /api/v1/predict` with multipart field `file`
- `GET /api/v1/history`
- `GET /api/v1/history/{id}`
- `GET /api/v1/result/{id}`
- `DELETE /api/v1/history/{id}`

## Training and inference

```powershell
python scripts\train_model.py
python scripts\run_inference.py path\to\image.jpg
```

No clinical dataset is bundled. Add only a properly licensed, de-identified dataset and document subject-level train/validation/test splits before training a real model. The evaluation module provides MAE, RMSE, R², and median absolute error helpers; metrics must come from actual dataset evaluation.

## Tests and Docker

```powershell
pytest -q
docker compose up --build
```

## Responsible use

This application provides an AI-estimated dental age for research and educational purposes. It is not a definitive determination of chronological age and should not be used as the sole basis for medical, legal, forensic, or identity-related decisions.
