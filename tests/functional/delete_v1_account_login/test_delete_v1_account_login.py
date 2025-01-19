def test_delete_v1_account_login(account_helper, prepared_user):
    login = prepared_user.login
    password = prepared_user.password
    email = prepared_user.email
    account_helper.authorizated_user(email=email, login=login, password=password)
    account_helper.delete_account_login()
