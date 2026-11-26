"""Django settings. Every deploy-specific value comes from the environment (see config/env.py)."""

from pathlib import Path
from urllib.parse import unquote, urlsplit

from config.env import env

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env.secret_key
DEBUG = env.debug
ALLOWED_HOSTS = [host for host in env.allowed_hosts.split(",") if host]

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "apps.users",
    "apps.items",
]

# API-only service: no sessions, cookies, CSRF or templates on the request path.
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
APPEND_SLASH = False  # a redirect would drop POST bodies

_db = urlsplit(str(env.database_url))
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": _db.path.lstrip("/"),
        "USER": unquote(_db.username or ""),
        "PASSWORD": unquote(_db.password or ""),
        "HOST": _db.hostname or "",
        "PORT": _db.port or "",
        # One persistent connection per worker thread: no reconnect per request.
        "CONN_MAX_AGE": 600,
        "CONN_HEALTH_CHECKS": True,
        # Fail fast instead of hanging a worker (and the readiness probe) on an unreachable DB.
        "OPTIONS": {"connect_timeout": 5},
    }
}

AUTH_USER_MODEL = "users.User"
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": f"django.contrib.auth.password_validation.{name}"}
    for name in (
        "UserAttributeSimilarityValidator",
        "MinimumLengthValidator",
        "CommonPasswordValidator",
        "NumericPasswordValidator",
    )
]

TIME_ZONE = "UTC"
USE_TZ = True
USE_I18N = False

NINJA_PAGINATION_PER_PAGE = 50
NINJA_PAGINATION_MAX_LIMIT = 100

# Trust X-Forwarded-Proto. Only correct behind a proxy/load balancer that sets or strips it.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
X_FRAME_OPTIONS = "DENY"
if not DEBUG:
    SECURE_SSL_REDIRECT = env.secure_ssl_redirect
    SECURE_REDIRECT_EXEMPT = [r"^healthz$", r"^readyz$"]  # probes arrive over plain HTTP
    SECURE_HSTS_SECONDS = 31_536_000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# No cookie-based auth exists, so there is nothing for CSRF middleware to protect.
SILENCED_SYSTEM_CHECKS = ["security.W003"]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {"()": "config.log.JsonFormatter"},
        "plain": {"format": "%(levelname)s %(name)s %(message)s"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "plain" if DEBUG else "json",
        },
    },
    "root": {"handlers": ["console"], "level": env.log_level},
}
