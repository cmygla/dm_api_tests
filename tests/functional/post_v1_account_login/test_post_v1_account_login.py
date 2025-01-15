from conftest import account_helper


def test_post_v1_account_login_not_activated_user(account_helper, test_data):
    account_helper.create_user(email=test_data["email"], login=test_data["login"], password=test_data["password"])
    # авторизация
    response = account_helper.dm_api_account.login_api.post_v1_account_login(
        login=test_data["login"], password=test_data["password"]
    )
    assert response.status_code == 403, "Неактивированный пользователь авторизовался"
