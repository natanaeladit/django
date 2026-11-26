from django.conf import settings
from ninja import NinjaAPI

from apps.items.api import router as items_router

api = NinjaAPI(
    title="API",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    openapi_url="/openapi.json" if settings.DEBUG else None,
)
api.add_router("/items", items_router)
