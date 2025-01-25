from checkers.http_checkers import check_status_code_http


def test_put_v1_account_email(mailhog_helper, account_helper, prepared_user):
    login = prepared_user.login
    password = prepared_user.password
    email = prepared_user.email
    account_helper.auth_client(email=email, login=login, password=password)
    account_helper.update_email(email=email, login=login, password=password)
    with check_status_code_http(
            expected_status_code=403, expected_title="User is inactive. Address the technical support for more details"
    ):
        response = account_helper.login_user_raw(login=login, password=password)

    token = mailhog_helper.get_activation_token_by_login(login=login)
    account_helper.activate_user(token)
    account_helper.login_user(login=login, password=password)
