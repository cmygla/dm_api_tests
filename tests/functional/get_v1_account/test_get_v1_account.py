from datetime import datetime

from hamcrest import (
    has_properties,
    assert_that,
    has_length,
    greater_than_or_equal_to,
    has_string,
    starts_with,
)


def test_get_v1_account(auth_account_helper):
    response = auth_account_helper.get_user_info(validate_headers=False)
    print(response)
    assert_that(
        response.resource, has_properties(
            {
                "login": auth_account_helper.login,
                "roles": has_length(greater_than_or_equal_to(2)),
                "online": has_string(starts_with(str(datetime.now().date())))
            }
        )
    )
