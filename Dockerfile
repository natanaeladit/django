# syntax=docker/dockerfile:1

FROM python:3.14-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:0.13.10 /uv /bin/uv
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never
WORKDIR /app
# Dependencies only: this layer is rebuilt only when the lockfile changes.
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-dev

FROM python:3.14-slim
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH"
RUN useradd --system --uid 10001 --no-create-home app
WORKDIR /app
COPY --from=builder /app/.venv .venv
COPY manage.py gunicorn.conf.py ./
COPY config config
COPY apps apps
# Precompile: the filesystem is read-only at runtime, so bytecode must exist already.
RUN python -m compileall -q config apps
USER app
EXPOSE 8000
HEALTHCHECK --interval=10s --timeout=3s --start-period=10s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/healthz', timeout=2)"]
CMD ["gunicorn", "config.wsgi", "-c", "gunicorn.conf.py"]
