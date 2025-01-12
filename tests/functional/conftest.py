import pytest

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
