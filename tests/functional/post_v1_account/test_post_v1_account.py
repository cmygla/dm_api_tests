from json import loads

from api_mailhog.apis.mailhog_api import (
    MailhogApi,
)
from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi


def test_post_v1_account():
    account_api = AccountApi(
        host="http://5.63.153.31:5051"
    )
    login_api = LoginApi(
        host="http://5.63.153.31:5051"
    )
    mailhog_api = MailhogApi(
        host="http://5.63.153.31:5025"
    )

    login = 'user_ekv5'
    password = 'user_ekv_123'
    email = f'{login}@mail.ru'
    # регистрация пользователя
    response = account_api.post_v1_account(
        email=email,
        login=login,
        password=password
    )

    print(
        response.status_code
    )
    print(
        response.text
    )
    assert response.status_code == 201, "Пользователь не был создан"

    # получение письма из почтового сервера
    response = mailhog_api.get_api_v2_messages(

    )
    print(
        response.status_code
    )
    print(
        response.text
    )
    assert response.status_code == 200, "Письма не были получены"

    # получение активационного токена
    token = get_activation_token_by_login(
        login,
        response
    )
    assert token is not None, "Токен не был получен"

    # активация пользователя
    response = account_api.put_v1_account_token(
        token=token
    )
    print(
        response.status_code
    )
    print(
        response.text
    )
    assert response.status_code == 200, "Пользователь не был активирован"

    # авторизация
    response = login_api.post_v1_account_login(
        login=login,
        password=password
    )
    print(
        response.status_code
    )
    print(
        response.text
    )
    assert response.status_code == 200, "Пользователь не смог авторизоваться"


def get_activation_token_by_login(
        login,
        response
):
    token = None
    for item in response.json()["items"]:
        user_data = loads(
            item['Content']['Body']
        )
        user_login = user_data["Login"]
        if user_login == login:
            token = user_data["ConfirmationLinkUrl"].split(
                '/'
            )[-1]
    return token
