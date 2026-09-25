# Installation guide

## Prerequisites

- Python 3.10+
- Node.js 18+
- npm
- Docker and Docker Compose (optional)

## Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

## Environment variables

Copy `.env.example` to `.env` and adjust values as needed.
