from unittest.mock import patch

import pytest
from django.db import OperationalError, connection
from django.test import Client


def test_healthz_needs_no_database(client: Client) -> None:
    response = client.get("/healthz")

    assert response.status_code == 200


@pytest.mark.django_db
def test_readyz_ok_when_database_reachable(client: Client) -> None:
    response = client.get("/readyz")

    assert response.status_code == 200


def test_readyz_503_when_database_down(client: Client) -> None:
    with patch.object(connection, "cursor", side_effect=OperationalError("down")):
        response = client.get("/readyz")

    assert response.status_code == 503
