import pytest

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from restclient.configuration import Configuration

dm_api_configuration = Configuration(host="http://5.63.153.31:5051", disable_logs=False)


@pytest.fixture(scope="package")
def account_api():
    '''test'''
    return AccountApi(configuration=dm_api_configuration)


@pytest.fixture(scope="package")
def login_api():
    '''test'''
    return LoginApi(configuration=dm_api_configuration)
