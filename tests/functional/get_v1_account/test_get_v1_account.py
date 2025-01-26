import assertpy
import hamcrest
from assertpy import soft_assertions
from hamcrest import (
    has_properties,
    has_length,
    greater_than_or_equal_to,
)

from checkers.http_checkers import check_status_code_http
from dm_api_account.models.user_details_envelope import UserRole


def test_get_v1_account_auth(auth_account_helper):
    with check_status_code_http():
        response = auth_account_helper.get_user_info()
        print(response)
        hamcrest.assert_that(
            response.body.resource, has_properties(
                {
                    "login": auth_account_helper.get_credentials().login,
                    "roles": has_length(greater_than_or_equal_to(2))}
            )
        )

        with soft_assertions():
            assertpy.assert_that(response.body.resource.login).is_equal_to(auth_account_helper.get_credentials().login)
            assertpy.assert_that(response.body.resource.roles).contains(UserRole.GUEST, UserRole.PLAYER)


def test_get_v1_account_no_auth(account_helper):
    with check_status_code_http(401, "User must be authenticated"):
        response = account_helper.get_user_info()
