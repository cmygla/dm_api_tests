def test_put_v1_account_password(mailhog_helper, account_helper, prepared_user):
    login = prepared_user.login
    password = prepared_user.password
    email = prepared_user.email
    new_password = f'{password}_'
    account_helper.authorizated_user(email=email, login=login, password=password)
    account_helper.change_account_password(email=email, login=login, old_pass=password, new_pass=new_password)
    account_helper.login_user(login=login, password=new_password)
