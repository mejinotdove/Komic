# Komic

**Self-hosted comic/manga server** — FastAPI + SQLite + HTMX + WebDAV.

## Quick start

```bash
pip install -r requirements.txt
# or
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

```bash
docker build -t komic:latest .
docker compose up -d
```

## Architecture

- `app/main.py` — FastAPI entrypoint. Mounts: `/api`, `/` (web UI), `/static`, WebDAV at `DAV_PREFIX`.
- No test suite, no pyproject.toml, no setup.py.
- Pure server-rendered HTML + **HTMX** (no JS framework). No API client code.
- Frontend templates in `app/templates/`, CSS in `app/static/`.

## Config (all env vars)

| Var | Default | Note |
|-----|---------|------|
| `MANKA_PATH` | `/manka` | Comics directory, read-only in Docker |
| `DB_PATH` | `/data/komic.db` | SQLite path |
| `DAV_PREFIX` | `/dav` | WebDAV mount point |
| `EXCLUDE_DIRS` | `""` | Comma-separated dirs to skip during scan |

No `.env` loading — env vars only.

## Database

- SQLite + SQLAlchemy, WAL mode + busy timeout set at startup.
- **Alembic** manages schema. All migrations in `alembic/versions/`.
- `init_db()` (called on startup) runs `alembic upgrade head` automatically.
- `DB_PATH` is dynamic (env var), so `alembic/env.py` overrides `sqlalchemy.url` at runtime from `app.database.engine.url`.
- To add a column: edit `models.py`, then `alembic revision --autogenerate -m "msg"`, commit the .py file.

## Scanning

- `MANKA_PATH` expects subdirectories — each is treated as a comic.
- Scanner runs in a **background daemon thread** (`scan_manager.py`), status polled via `GET /api/scan/progress-bar`.
- Filename date prefix (`YYYYMMDD`) is stripped for display title.
- Supported formats: `dir`, `zip`, `7z`, `rar`. Detected by file extension + `libmagic1` in Docker.
- Cover = first image file (alphabetically) inside the archive/directory.

## WebDAV quirk

Rating is set by **MOVE** to a path like `/dav/rating/{N}/...`. This is the only write mechanism. The virtual filesystem mirrors the SQLite catalog, not the raw filesystem.

## Docker

- `python:3.12-slim` base, installs `libmagic1`.
- CI (`.github/workflows/build-image.yml`) builds on `main` push or release, saves `komic.tar.gz` (for QNAP Container Station import).
- No image registry push in CI.
