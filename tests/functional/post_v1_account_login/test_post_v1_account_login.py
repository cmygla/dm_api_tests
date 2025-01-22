def test_post_v1_account_login_not_activated_user(account_helper, prepared_user):
    login = prepared_user.login
    password = prepared_user.password
    email = prepared_user.email
    account_helper.create_user(email=email, login=login, password=password)

    response = account_helper.login_user_raw(login=login, password=password, validate_response=False)
    assert response.status_code == 403, "Неактивированный пользователь авторизовался"
