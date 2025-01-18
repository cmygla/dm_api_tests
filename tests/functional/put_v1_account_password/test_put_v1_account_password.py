def test_put_v1_account_password(mailhog_helper, account_helper, prepared_user):
    login = prepared_user.login
    password = prepared_user.password
    email = prepared_user.email
    account_helper.authorizated_user(email=email, login=login, password=password)
    account_helper.reset_account_password(
        auth_token=account_helper.auth_token, email=email, login=login, old_pass=password, new_pass=f'{password}_'
    )
