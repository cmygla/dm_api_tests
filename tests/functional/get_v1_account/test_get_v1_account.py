from hamcrest import (
    has_properties,
    assert_that,
    has_length,
    greater_than_or_equal_to,
)

from checkers.http_checkers import check_status_code_http


def test_get_v1_account_auth(auth_account_helper):
    with check_status_code_http():
        response = auth_account_helper.get_user_info()
        print(response)
        assert_that(
            response.body.resource, has_properties(
                {
                    "login": auth_account_helper.get_credentials().login,
                    "roles": has_length(greater_than_or_equal_to(2))}
            )
        )


def test_get_v1_account_no_auth(account_helper):
    with check_status_code_http(401, "User must be authenticated"):
        response = account_helper.get_user_info()
