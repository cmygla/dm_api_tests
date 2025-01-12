from api_mailhog.data_helper.common import get_activation_token_by_login


def test_put_v1_account_email(account_api, login_api, mailhog_api, login_user):
    # Меняем емейл
    response = account_api.put_v1_account_email(
        email=f'new_{login_user["email"]}', login=login_user["login"], password=login_user["password"]
    )
    assert response.status_code == 200, "Email не был изменен"

    # Пытаемся войти, получаем 403
    response = login_api.post_v1_account_login(login=login_user["login"], password=login_user["password"])
    assert response.status_code == 403, "Пользователь смог авторизоваться после смены email"

    # На почте находим токен по новому емейлу для подтверждения смены емейла
    response = mailhog_api.get_api_v2_messages()
    assert response.status_code == 200, "Письма не были получены после смены email"

    # Получение активационного токена
    token = get_activation_token_by_login(login=login_user["login"], response=response)
    assert token is not None, "Токен не был получен после смены email"

    # Активируем этот токен
    response = account_api.put_v1_account_token(token=token)
    assert response.status_code == 200, "Пользователь не был активирован после смены email"

    # Логинимся
    response = login_api.post_v1_account_login(login=login_user["login"], password=login_user["password"])
    assert response.status_code == 200, "Пользователь не смог авторизоваться после смены email"
