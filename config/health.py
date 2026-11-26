import logging

from django.db import DatabaseError, connection
from django.http import HttpRequest, HttpResponse

logger = logging.getLogger(__name__)


def liveness(request: HttpRequest) -> HttpResponse:
    return HttpResponse("ok")


def readiness(request: HttpRequest) -> HttpResponse:
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except DatabaseError:
        logger.exception("readiness check failed")
        return HttpResponse("database unavailable", status=503)
    return HttpResponse("ok")
