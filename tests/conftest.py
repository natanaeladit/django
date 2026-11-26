import pytest
from pytest_django import Settings


@pytest.fixture(autouse=True)
def _plain_http(settings: Settings) -> None:
    """The test client speaks plain HTTP; keep results independent of the host environment."""
    settings.SECURE_SSL_REDIRECT = False
