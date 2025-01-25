def test_put_v1_account_email(mailhog_helper, account_helper, prepared_user):
    login = prepared_user.login
    password = prepared_user.password
    email = prepared_user.email
    account_helper.auth_client(email=email, login=login, password=password, validate_response=False)
    account_helper.update_email(email=email, login=login, password=password, validate_response=False)

    response = account_helper.login_user_raw(login=login, password=password, validate_response=False)
    assert response.status_code == 403, "Пользователь смог авторизоваться после смены email"

    token = mailhog_helper.get_activation_token_by_login(login=login)
    account_helper.activate_user(token, validate_response=False)
    account_helper.login_user(login=login, password=password, validate_response=False)
