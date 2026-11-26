from django.urls import path

from config.api import api
from config.health import healthz, readyz

urlpatterns = [
    path("healthz", healthz),
    path("readyz", readyz),
    path("api/v1/", api.urls),
]
