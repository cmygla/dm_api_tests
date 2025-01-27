from datetime import datetime

import hamcrest
from assertpy import (
    assertpy,
    soft_assertions,
)
from hamcrest import (
    has_properties,
    has_length,
    greater_than_or_equal_to,
)

from dm_api_account.models.user_details_envelope import UserRole


class GetV1Account:

    @classmethod
    def check_response_values(cls, login, response):
        hamcrest.assert_that(
            response.body.resource, has_properties(
                {
                    "login": login,
                    "roles": has_length(greater_than_or_equal_to(2))}
            )
        )
        with soft_assertions():
            today = datetime.now().strftime("%Y-%m-%d")
            assertpy.assert_that(str(response.body.resource.registration)).starts_with(today)
            assertpy.assert_that(response.body.resource.roles).contains(UserRole.GUEST, UserRole.PLAYER)
