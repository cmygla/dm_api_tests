def test_post_v1_account_login_not_activated_user(login_api, created_user):
    # авторизация
    response = login_api.post_v1_account_login(login=created_user["login"], password=created_user["password"])
    assert response.status_code == 403, "Неактивированный пользователь авторизовался"
