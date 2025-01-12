import pytest

from api_mailhog.apis.mailhog_api import MailhogApi


@pytest.fixture(scope="package")
def mailhog_api():
    return MailhogApi()
