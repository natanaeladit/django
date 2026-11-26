"""Probe endpoints. Plain Django views: unversioned and outside the OpenAPI schema."""

import logging

from django.db import DatabaseError, connection
from django.http import HttpRequest, HttpResponse

logger = logging.getLogger(__name__)


def healthz(request: HttpRequest) -> HttpResponse:
    """Liveness: the process is serving requests. No I/O."""
    return HttpResponse("ok")


def readyz(request: HttpRequest) -> HttpResponse:
    """Readiness: the database is reachable."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except DatabaseError:
        logger.exception("readiness check failed")
        return HttpResponse("database unavailable", status=503)
    return HttpResponse("ok")
