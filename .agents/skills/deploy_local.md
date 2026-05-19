# Skill — Deploy locally

Goal: make the application runnable on a developer machine.

Required:
1. `docker-compose.yml`.
2. `.env.example`.
3. Backend Dockerfile.
4. Frontend Dockerfile.
5. Database initialization.
6. README instructions.

Commands expected:

```bash
docker compose up --build
```

Expected URLs:

```text
Frontend: http://localhost:5173
Backend: http://localhost:8000
API Docs: http://localhost:8000/docs
```

Rules:
- Do not deploy to cloud unless explicitly requested.
- Do not require paid external services.
- Do not require real credentials for MVP.
