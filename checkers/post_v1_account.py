from datetime import datetime

import allure
from hamcrest import (
    equal_to,
    all_of,
    starts_with,
    assert_that,
    has_property,
    instance_of,
    has_properties,
)


class PostV1Account:

    @classmethod
    @allure.step("Проверка ответа")
    def check_response_values(cls, login, response):
        today = datetime.now().strftime("%Y-%m-%d")
        assert_that(str(response.body_as_object.resource.registration), starts_with(today))
        assert_that(
            response.body_as_object, all_of(
                has_property('resource', has_property('login', equal_to(login))),
                has_property('resource', has_property('registration', instance_of(datetime))),
                has_property(
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
