# LabFlow (Developer README)

A minimal runnable prototype for the LabFlow MVP: FastAPI backend + React (Vite) frontend.

Run locally with Docker Compose:

```bash
# build and run
docker-compose up --build

# Backend: http://localhost:8000
# Frontend: http://localhost:5173
```

Frontend dev notes:
- New UI uses Chakra UI and React Markdown. After pulling changes run `npm install` in `frontend/` (or let Docker build do it).
- Use `http://localhost:5173` to access the app.

Testing & demo data

- Seed the DB with a demo project & experiment:

```bash
python backend/scripts/seed.py
```

- Run backend tests:

```bash
pytest backend/tests -q
```

Security & privacy

- Optional server-side video encryption: set `ENCRYPT_VIDEOS=1` and `ENCRYPTION_KEY` (Fernet key) in the environment before running the backend. Uploaded videos will be encrypted at rest and decrypted on download.
- Consent: pass a `consent` form field on upload (true/false) to record opt-in for using video for model training.
