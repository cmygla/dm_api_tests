def test_post_v1_account_login_not_activated_user(account_helper, prepared_user):
    login = prepared_user.login
    password = prepared_user.password
    email = prepared_user.email
    account_helper.create_user(email=email, login=login, password=password)
    # авторизация
    response = account_helper.dm_api_account.login_api.post_v1_account_login(login=login, password=password)
    assert response.status_code == 403, "Неактивированный пользователь авторизовался"
