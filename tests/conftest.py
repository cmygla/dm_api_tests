# https://intellij-support.jetbrains.com/hc/en-us/community/posts/12897247432338-PyCharm-unable-to-find-fixtures-in-conftest-py
import os
from datetime import datetime
from pathlib import Path

import pytest
from swagger_coverage_py.reporter import CoverageReporter
from vyper import v

from common.tools.base_randomizer import generate_email
from helpers.account_helper import (
    Credentials,
    AccountHelper,
)
from helpers.mailhog_helper import MailhogHelper
from packages.restclient.configuration import Configuration
from services.api_mailhog import Mailhog
from services.dm_api_account import DmApiAccount

options = (
    'service.dm_api_account', 'service.mailhog', 'user.login', 'user.password', 'telegram.chat_id', 'telegram.token')


@pytest.fixture(scope="session", autouse=True)
def setup_swagger_coverage():
    reporter = CoverageReporter(api_name="dm-api-account", host="http://5.63.153.31:5051")
    reporter.cleanup_input_files()
    reporter.setup("/swagger/Account/swagger.json")

    yield
    reporter.generate_report()


@pytest.fixture(scope="session", autouse=True)
def set_config(request):
    """
    Вычитываем значения для переменных окруженияиз файла конфига
    :param request:
    :return:
    """
    config = Path(__file__).joinpath('../../').joinpath('config')
    config_name = request.config.getoption('--env')
    v.set_config_name(config_name)
    v.add_config_path(config)
    v.read_in_config()
    for option in options:
        v.set(option, request.config.getoption(f'--{option}'))
    os.environ["TELEGRAM_BOT_CHAT_ID"] = v.get("telegram.chat_id")
    os.environ["TELEGRAM_BOT_ACCESS_TOKEN"] = v.get("telegram.token")
    request.config.stash['telegram-notifier-addfields']['enviroment'] = config_name
    request.config.stash['telegram-notifier-addfields']['report'] = "https://cmygla.github.io/dm_api_tests/"


def pytest_addoption(parser):
    """
     Создаем переменные в коружении, с которыми хотим работать
    :param parser:
    :return:
    """
    parser.addoption('--env', action='store', default='stg', help="run stg")
    for option in options:
        parser.addoption(f'--{option}', action='store', default=None)


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
    dm_api_configuration = Configuration(host=v.get("service.dm_api_account"), disable_logs=False)
    dm_api_client = DmApiAccount(configuration=dm_api_configuration)
    return dm_api_client


@pytest.fixture(scope="session")
def mailhog_client():
    mailhog_configuration = Configuration(host=v.get("service.mailhog"))
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
    dm_api_configuration = Configuration(host=v.get("service.dm_api_account"), disable_logs=False)
    dm_api_client = DmApiAccount(configuration=dm_api_configuration)
    account_helper = AccountHelper(dm_api_account_client=dm_api_client, mailhog_helper=mailhog_helper)
    account_helper.auth_client(login=prepared_user.login, password=prepared_user.password, email=prepared_user.email)
    return account_helper
