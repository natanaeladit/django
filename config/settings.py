from urllib.parse import unquote, urlsplit

from config.env import env

SECRET_KEY = env.secret_key
DEBUG = env.debug
ALLOWED_HOSTS = [host for host in env.allowed_hosts.split(",") if host]

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "apps.users",
    "apps.items",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
APPEND_SLASH = False
TEMPLATES = [{"BACKEND": "django.template.backends.django.DjangoTemplates"}]

_db = urlsplit(str(env.database_url))
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": _db.path.lstrip("/"),
        "USER": unquote(_db.username or ""),
        "PASSWORD": unquote(_db.password or ""),
        "HOST": _db.hostname or "",
        "PORT": _db.port or "",
        "CONN_MAX_AGE": 600,
        "CONN_HEALTH_CHECKS": True,
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

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
X_FRAME_OPTIONS = "DENY"
if not DEBUG:
    _plain_http_probe_paths = [r"^healthz$", r"^readyz$"]
    SECURE_SSL_REDIRECT = env.secure_ssl_redirect
    SECURE_REDIRECT_EXEMPT = _plain_http_probe_paths
    SECURE_HSTS_SECONDS = 31_536_000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

_csrf_middleware_missing_check = "security.W003"
SILENCED_SYSTEM_CHECKS = [_csrf_middleware_missing_check]

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
