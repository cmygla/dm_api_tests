def test_put_v1_account_email(mailhog_helper, account_helper, prepared_user):
    login = prepared_user.login
    password = prepared_user.password
    email = prepared_user.email
    account_helper.authorizated_user(email=email, login=login, password=password)
    account_helper.update_email(email=email, login=login, password=password)

    response = account_helper.dm_api_account.login_api.post_v1_account_login(login=login, password=password)
    assert response.status_code == 403, "Пользователь смог авторизоваться после смены email"

    token = mailhog_helper.get_activation_token_by_login(login=login)
    account_helper.activate_user(token)
    account_helper.login_user(login=login, password=password)
