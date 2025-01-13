import pytest

from api_mailhog.data_helper.common import get_activation_token_by_login
from common.tools.base_randomizer import generate_random_string


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


@pytest.fixture(scope="function")
def created_user(account_api, test_data):
    # Регистрация пользователя
    response = account_api.post_v1_account(
        email=test_data["email"], login=test_data["login"], password=test_data["password"]
    )
    if response.status_code != 201:
        raise ValueError("Ошибка при создании пользователя")
    return test_data


@pytest.fixture(scope="function")
def activated_user(mailhog_api, account_api, created_user):
    response = mailhog_api.get_api_v2_messages()
    if response.status_code != 200:
        raise ValueError("Ошибка при получении писем")

    # Получение активационного токена
    token = get_activation_token_by_login(created_user["login"], response)
    if token is None:
        raise ValueError("Токен не был получен")

    # активация пользователя
    response = account_api.put_v1_account_token(token=token)
    if response.status_code != 200:
        raise ValueError("Пользователь не был активирован")
    return created_user


@pytest.fixture(scope="function")
def login_user(login_api, activated_user):
    response = login_api.post_v1_account_login(login=activated_user["login"], password=activated_user["password"])
    if response.status_code != 200:
        raise ValueError("Пользователь не смог авторизоваться")
    return activated_user
