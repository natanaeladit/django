# Django API

Typed Django REST API: Django 6.1, Django Ninja, PostgreSQL, gunicorn, Docker. Python 3.14.

## Prerequisites

- [uv](https://docs.astral.sh/uv/) (`winget install --id=astral-sh.uv -e`)
- Docker Desktop

## Local development (PowerShell)

```powershell
Copy-Item .env.example .env          # then set SECRET_KEY (command is in the file)
uv sync                              # creates .venv with all dependencies
docker compose up -d --wait db       # PostgreSQL on 127.0.0.1:5432
uv run python manage.py migrate
uv run python manage.py runserver    # http://127.0.0.1:8000/api/v1/docs (DEBUG only)
```

gunicorn does not run on Windows; it is used only inside the container.

## Checks

```powershell
uv run pytest                        # needs the db container; coverage gate 90%
uv run ruff check .
uv run ruff format .
uv run mypy .
uv run python manage.py makemigrations --check --dry-run
```

CI (`.github/workflows/ci.yml`) runs the same commands plus `check --deploy` and a Docker build.

## Run the production image locally

```powershell
docker compose up --build -d --wait  # db, one-shot migrate, then web on :8000
curl.exe http://localhost:8000/readyz
docker compose down                  # add -v to also delete the database volume
```

## Endpoints

| Path | Purpose |
|---|---|
| `GET /healthz` | Liveness. No I/O. |
| `GET /readyz` | Readiness. 503 when the database is unreachable. |
| `/api/v1/items` | Example resource: list (limit/offset), create, get, patch, delete. |
| `/api/v1/docs` | Swagger UI, only when `DEBUG=true`. |

## Configuration

All configuration is environment variables, validated at startup by `config/env.py`.

| Variable | Required | Default | Notes |
|---|---|---|---|
| `SECRET_KEY` | yes | | 50+ random characters |
| `DATABASE_URL` | yes | | `postgresql://user:pass@host:5432/name` |
| `ALLOWED_HOSTS` | in production | empty | comma-separated |
| `DEBUG` | no | `false` | |
| `SECURE_SSL_REDIRECT` | no | `true` | keep on behind a TLS-terminating proxy |
| `LOG_LEVEL` | no | `INFO` | JSON logs on stdout when not DEBUG |
| `WEB_CONCURRENCY` | no | `2` | gunicorn worker processes |
| `GUNICORN_THREADS` | no | `4` | threads per worker |

Each worker thread holds one database connection: `WEB_CONCURRENCY x GUNICORN_THREADS`
connections per container. Keep the total across replicas under PostgreSQL's `max_connections`.

## Deploying

- Run `python manage.py migrate` as a separate one-off job before rolling out new replicas
  (see the `migrate` service in `compose.yaml`). The web container never migrates on start.
- The service trusts `X-Forwarded-Proto`. Deploy it only behind a proxy or load balancer that
  sets that header itself.
- Probes must send a `Host` header listed in `ALLOWED_HOSTS`, otherwise Django answers 400.
  The image's built-in `HEALTHCHECK` uses `localhost`. Kubernetes probes use the pod IP by
  default: set `httpHeaders` with a `Host` value on the probe.

## Adding an app

Copy `apps/items`, add it to `INSTALLED_APPS` in `config/settings.py`, mount its router in
`config/api.py`, then `uv run python manage.py makemigrations <name>`.

Authentication is not included yet. It plugs in at one place: `NinjaAPI(auth=...)` in
`config/api.py`.
