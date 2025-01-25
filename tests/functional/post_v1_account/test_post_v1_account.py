from datetime import datetime

from hamcrest import (
    assert_that,
    has_property,
    all_of,
    equal_to,
    instance_of,
    has_properties,
)


def test_post_v1_account(account_helper, prepared_user):
    login = prepared_user.login
    password = prepared_user.password
    email = prepared_user.email
    account_helper.register_new_user(email=email, login=login, password=password, validate_response=False)
    response = account_helper.login_user(login=login, password=password, validate_headers=False)
    assert_that(
        response, all_of(
            has_property('resource', has_property('login', equal_to(login))),
            has_property('resource', has_property('registration', instance_of(datetime))), has_property(
                'resource', has_property(
                    'rating', has_properties(
                        {
                            'enabled': equal_to(True),
                            'quality': equal_to(0),
                            'quantity': equal_to(0)

                        }
                    )
                )
            )
        )
    )
