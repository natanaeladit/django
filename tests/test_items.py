import pytest
from django.test import Client

from apps.items.models import Item

pytestmark = pytest.mark.django_db

URL = "/api/v1/items"


def test_create_returns_201_and_persists(client: Client) -> None:
    response = client.post(URL, {"name": "widget"}, content_type="application/json")

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "widget"
    assert body["description"] == ""
    assert Item.objects.get(id=body["id"]).name == "widget"


@pytest.mark.parametrize("payload", [{}, {"name": ""}, {"name": "x" * 201}])
def test_create_rejects_invalid_payload(client: Client, payload: dict[str, str]) -> None:
    response = client.post(URL, payload, content_type="application/json")

    assert response.status_code == 422
    assert not Item.objects.exists()


def test_list_is_paginated_and_ordered(client: Client) -> None:
    Item.objects.bulk_create(Item(name=f"item-{n}") for n in range(3))

    response = client.get(URL, {"limit": 2, "offset": 1})

    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 3
    assert [item["name"] for item in body["items"]] == ["item-1", "item-2"]


def test_list_rejects_limit_above_maximum(client: Client) -> None:
    response = client.get(URL, {"limit": 101})

    assert response.status_code == 422


def test_get_returns_item(client: Client) -> None:
    item = Item.objects.create(name="widget")

    response = client.get(f"{URL}/{item.id}")

    assert response.status_code == 200
    assert response.json()["id"] == item.id


def test_patch_changes_only_sent_fields(client: Client) -> None:
    item = Item.objects.create(name="widget", description="old")

    response = client.patch(
        f"{URL}/{item.id}",
        {"description": "new", "name": None},
        content_type="application/json",
    )

    assert response.status_code == 200
    item.refresh_from_db()
    assert (item.name, item.description) == ("widget", "new")


def test_delete_removes_item(client: Client) -> None:
    item = Item.objects.create(name="widget")

    response = client.delete(f"{URL}/{item.id}")

    assert response.status_code == 204
    assert not Item.objects.exists()


@pytest.mark.parametrize("method", ["get", "patch", "delete"])
def test_missing_item_returns_404(client: Client, method: str) -> None:
    response = getattr(client, method)(f"{URL}/999", {}, content_type="application/json")

    assert response.status_code == 404
