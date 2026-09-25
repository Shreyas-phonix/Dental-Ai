# Docker deployment guide

## Build and run

```bash
docker compose up --build
```

## Notes

This repository is designed so it can eventually migrate to PostgreSQL, but the default development database is SQLite. The Docker configuration includes a Postgres service for future expansion and future-proofing.
