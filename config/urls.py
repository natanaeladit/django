from django.urls import path

from config.api import api
from config.health import liveness, readiness

urlpatterns = [
    path("healthz", liveness),
    path("readyz", readiness),
    path("api/v1/", api.urls),
]
