# System architecture

## Overview

The application is organized into three major layers:

1. Frontend: a React dashboard for upload, results, and history.
2. Backend: a FastAPI service that validates input, stores metadata, and returns predictions.
3. ML stack: preprocessing, regression model, training, evaluation, and explainability modules.

## Data flow

- User uploads an OPG or panoramic X-ray.
- Backend validates extension, MIME type, file size, and image readability.
- Image is prepared in the preprocessing module.
- The model estimates dental age.
- Grad-CAM is generated to highlight influential regions.
- Predictions and metadata are stored in SQLite.
- Results are displayed in the UI with disclaimers.

## Deployment model

- Local development: FastAPI + Vite dev servers
- Containerized deployment: Docker Compose
- Production-ready migration path: SQLAlchemy, PostgreSQL, object storage, and persistent model artifacts
