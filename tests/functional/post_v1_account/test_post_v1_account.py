import pytest

from checkers.http_checkers import check_status_code_http
from checkers.post_v1_account import PostV1Account
from common.tools.base_randomizer import (
    generate_random_string,
    generate_email,
)


def generate_random_email():
    first_part = generate_random_string(10)
    return generate_email(first_part)


def test_post_v1_account(account_helper, prepared_user):
    login = prepared_user.login
    password = prepared_user.password
    email = prepared_user.email
    account_helper.register_new_user(email=email, login=login, password=password)
    response = account_helper.login_user(login=login, password=password)
    PostV1Account.check_response_values(login, response)


@pytest.mark.parametrize(
    "login, email, password, expected_status_code, expected_title, expected_errors",
    [("valid_login", "invalid_email", "valid_password", 400, "Validation failed", {
        "Email": ["Invalid"]}),  # Невалидный e-mail
     ("1", generate_random_email(), "valid_password", 400, "Validation failed", {
         "Login": ["Short"]}),  # Короткий логин
     ("valid_login", generate_random_email(), "12345", 400, "Validation failed", {
         "Password": ["Short"]}),  # Короткий пароль
     ]
)
def test_negative_post_v1_account(
        account_helper, login, email, password, expected_status_code, expected_title, expected_errors
):
    with check_status_code_http(expected_status_code, expected_title, expected_errors):
        account_helper.register_new_user(email=email, login=login, password=password)
