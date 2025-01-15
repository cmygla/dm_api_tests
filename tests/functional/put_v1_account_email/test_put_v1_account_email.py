from conftest import (
    account_helper,
    mailhog_helper,
)


def test_put_v1_account_email(test_data):
    account_helper.register_new_user(email=test_data["email"], login=test_data["login"], password=test_data["password"])
    account_helper.login_user(login=test_data["login"], password=test_data["password"])

    # Меняем емейл
    response = account_helper.dm_api_account.account_api.put_v1_account_email(
        email=f'new_{test_data["email"]}', login=test_data["login"], password=test_data["password"]
    )
    assert response.status_code == 200, "Email не был изменен"

    # Пытаемся войти, получаем 403
    response = account_helper.dm_api_account.login_api.post_v1_account_login(
        login=test_data["login"], password=test_data["password"]
    )
    assert response.status_code == 403, "Пользователь смог авторизоваться после смены email"

    token = mailhog_helper.get_activation_token_by_login(login=test_data["login"])
    account_helper.activate_user(token)
    account_helper.login_user(login=test_data["login"], password=test_data["password"])
