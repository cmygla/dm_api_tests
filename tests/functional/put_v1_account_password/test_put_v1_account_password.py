def test_put_v1_account_password(mailhog_helper, account_helper, prepared_user):
    login = prepared_user.login
    password = prepared_user.password
    email = prepared_user.email
    new_password = f'{password}_'
    account_helper.auth_client(email=email, login=login, password=password, validate_response=False)
    account_helper.change_account_password(email=email, login=login, old_pass=password, new_pass=new_password)
    account_helper.login_user_raw(login=login, password=new_password)
