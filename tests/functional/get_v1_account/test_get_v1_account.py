def test_get_v1_account(account_helper, prepared_user):
    login = prepared_user.login
    password = prepared_user.password
    email = prepared_user.email
    account_helper.authorizated_user(email=email, login=login, password=password)
    account_helper.get_user_info()
