# https://intellij-support.jetbrains.com/hc/en-us/community/posts/12897247432338-PyCharm-unable-to-find-fixtures-in-conftest-py
from datetime import datetime

import pytest

from common.tools.base_randomizer import generate_email
from helpers.account_helper import (
    AccountHelper,
    Credentials,
)
from helpers.mailhog_helper import MailhogHelper
from restclient.configuration import Configuration
from services.api_mailhog import Mailhog
from services.dm_api_account import DmApiAccount


@pytest.fixture
def prepared_user():
    now = datetime.now()
    date = now.strftime("%H_%M_%S_%f")
    login = f'ekv_{date}'
    password = '12345678'
    email = generate_email(login)
    user = Credentials(login=login, password=password, email=email)
    return user


@pytest.fixture(scope="session")
def dm_api_client():
    dm_api_configuration = Configuration(host="http://5.63.153.31:5051", disable_logs=False)
    dm_api_client = DmApiAccount(configuration=dm_api_configuration)
    return dm_api_client


@pytest.fixture(scope="session")
def mailhog_client():
    mailhog_configuration = Configuration(host="http://5.63.153.31:5025")
    mailhog_client = Mailhog(configuration=mailhog_configuration)
    return mailhog_client


@pytest.fixture(scope="session")
def mailhog_helper(mailhog_client):
    return MailhogHelper(mailhog_client=mailhog_client)


@pytest.fixture(scope="session")
def account_helper(dm_api_client, mailhog_helper):
    return AccountHelper(
        dm_api_account_client=dm_api_client, mailhog_helper=mailhog_helper
    )


@pytest.fixture()
def auth_account_helper(prepared_user, mailhog_helper):
    dm_api_configuration = Configuration(host="http://5.63.153.31:5051", disable_logs=False)
    dm_api_client = DmApiAccount(configuration=dm_api_configuration)
    account_helper = AccountHelper(dm_api_account_client=dm_api_client, mailhog_helper=mailhog_helper)
    account_helper.auth_client(login=prepared_user.login, password=prepared_user.password, email=prepared_user.email)
    return account_helper
