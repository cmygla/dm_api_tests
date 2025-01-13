import pytest

from api_mailhog.apis.mailhog_api import MailhogApi
from restclient.configuration import Configuration

mailhog_configuration = Configuration(host="http://5.63.153.31:5025")


@pytest.fixture(scope="package")
def mailhog_api():
    return MailhogApi(configuration=mailhog_configuration)
