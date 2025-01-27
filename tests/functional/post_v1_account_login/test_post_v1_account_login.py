from checkers.http_checkers import check_status_code_http


def test_post_v1_account_login_not_activated_user(account_helper, prepared_user):
    login = prepared_user.login
    password = prepared_user.password
    email = prepared_user.email
    account_helper.create_user(email=email, login=login, password=password)
    with check_status_code_http(
            expected_status_code=404, expected_title="User is inactive. Address the technical support for more details"
    ):
        response = account_helper.login_user_raw(login=login, password=password)
