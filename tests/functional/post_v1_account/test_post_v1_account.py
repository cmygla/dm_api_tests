def test_post_v1_account(account_helper, prepared_user):
    login = prepared_user.login
    password = prepared_user.password
    email = prepared_user.email
    account_helper.register_new_user(email=email, login=login, password=password, validate_response=False)
    account_helper.login_user(login=login, password=password, validate_response=False)
