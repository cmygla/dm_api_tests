import pytest

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi


@pytest.fixture(scope="package")
def account_api():
    '''test'''
    return AccountApi()


@pytest.fixture(scope="package")
def login_api():
    '''test'''
    return LoginApi()
