# DentalAge AI

DentalAge AI is a production-quality prototype for explainable dental X-ray age estimation. The project combines a FastAPI backend, a PyTorch regression model, a SQLite-backed analysis history, and a polished React frontend for upload, inference, explanation, and review.

## Features

- Upload and validate panoramic dental radiographs
- Image preprocessing and model inference
- Explainability via Grad-CAM-style overlay
- SQLite-based analysis history
- Full-stack dashboard with upload, results, history, and about pages
- Development fallback training path when a research dataset is not available
- Docker, environment configuration, and test scaffolding

## Architecture

- Frontend: React + Vite + TypeScript + Tailwind
- Backend: FastAPI + Pydantic + SQLite
- ML: PyTorch + OpenCV + Pillow + NumPy + scikit-learn
- Explainability: Grad-CAM overlay pipeline

## Quick start

1. Copy `.env.example` to `.env`.
2. Install backend dependencies from `backend/requirements.txt`.
3. Install frontend dependencies from `frontend/package.json`.
4. Start the backend:
   ```bash
   cd backend
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```
5. Start the frontend:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
6. Open the app and upload a dental X-ray.

## Dataset setup

The repository includes a dataset documentation file and a setup roadmap. No medical dataset is bundled by default. For a real clinical-grade deployment, use a licensed public dental radiograph dataset and replace the development fallback weights.

## Model training

```bash
python scripts/train_model.py
```

## Inference

```bash
python scripts/run_inference.py path/to/image.jpg
```

## Tests

```bash
pytest
```

## Responsible use

This application provides an AI-estimated dental age for research and educational purposes. It is not a definitive determination of chronological age and should not be used as the sole basis for medical, legal, forensic, or identity-related decisions.

## License

This project is intended for research and educational use. Review dataset licenses before using a public dental radiography dataset in a production environment.
