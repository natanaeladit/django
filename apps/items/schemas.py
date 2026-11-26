from datetime import datetime

from ninja import Schema
from pydantic import Field


class ItemIn(Schema):
    name: str = Field(min_length=1, max_length=200)
    description: str = ""


class ItemPatch(Schema):
    """Partial update. Omitted or null fields are left unchanged."""

    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None


class ItemOut(Schema):
    id: int
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
