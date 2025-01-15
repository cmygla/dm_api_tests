# https://intellij-support.jetbrains.com/hc/en-us/community/posts/12897247432338-PyCharm-unable-to-find-fixtures-in-conftest-py
import pytest

from common.tools.base_randomizer import generate_random_string
from helpers.account_helper import AccountHelper
from helpers.mailhog_helper import MailhogHelper
from restclient.configuration import Configuration
from services.api_mailhog import Mailhog
from services.dm_api_account import DmApiAccount

mailhog_configuration = Configuration(host="http://5.63.153.31:5025")
dm_api_configuration = Configuration(host="http://5.63.153.31:5051", disable_logs=False)

mailhog_helper = MailhogHelper(Mailhog(configuration=mailhog_configuration))

account_helper = AccountHelper(
    dm_api_account=DmApiAccount(configuration=dm_api_configuration), mailhog_helper=mailhog_helper
)


@pytest.fixture
def test_data():
    login = f'user_{generate_random_string(6)}'
    password = generate_random_string(12)
    email = f'{login}@mail.ru'
    return {
        "login": login,
        "password": password,
        "email": email
    }
