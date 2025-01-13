from api_mailhog.data_helper.common import get_activation_token_by_login


def test_post_v1_account(account_api, login_api, mailhog_api, test_data):
    # регистрация пользователя
    response = account_api.post_v1_account(
        email=test_data["email"], login=test_data["login"], password=test_data["password"]
    )
    assert response.status_code == 201, "Пользователь не был создан"

    # получение письма из почтового сервера
    response = mailhog_api.get_api_v2_messages()
    assert response.status_code == 200, "Письма не были получены"

    # получение активационного токена
    token = get_activation_token_by_login(login=test_data["login"], response=response)
    assert token is not None, "Токен не был получен"

    # активация пользователя
    response = account_api.put_v1_account_token(token=token)
    assert response.status_code == 200, "Пользователь не был активирован"

    # авторизация
    response = login_api.post_v1_account_login(login=test_data["login"], password=test_data["password"])
    assert response.status_code == 200, "Пользователь не смог авторизоваться"
