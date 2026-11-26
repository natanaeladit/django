import pytest
from pytest_django import Settings


@pytest.fixture(autouse=True)
def _disable_ssl_redirect_for_plain_http_test_client(settings: Settings) -> None:
    settings.SECURE_SSL_REDIRECT = False
