# https://intellij-support.jetbrains.com/hc/en-us/community/posts/12897247432338-PyCharm-unable-to-find-fixtures-in-conftest-py
import pytest

from api_mailhog.apis.mailhog_api import MailhogApi
from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from restclient.configuration import Configuration

mailhog_configuration = Configuration(host="http://5.63.153.31:5025")
dm_api_configuration = Configuration(host="http://5.63.153.31:5051", disable_logs=False)


@pytest.fixture(scope="package")
def mailhog_api():
    return MailhogApi(configuration=mailhog_configuration)


@pytest.fixture(scope="package")
def account_api():
    return AccountApi(configuration=dm_api_configuration)


@pytest.fixture(scope="package")
def login_api():
    return LoginApi(configuration=dm_api_configuration)
