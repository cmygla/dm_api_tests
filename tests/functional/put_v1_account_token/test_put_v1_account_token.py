import uuid

import allure

from checkers.http_checkers import check_status_code_http


@allure.suite("Тест на проверку метода PUT:v1/account/token")
class TestPutV1Account:
    @allure.sub_suite("Негативные тесты")
    @allure.title("Проверка активации пользователя с невалидным токеном")
    def test_put_v1_account_token_not_valid(self, account_helper):
        token = str(uuid.uuid4())
        with check_status_code_http(
                expected_status_code=410,
                expected_title="Activation token is invalid! Address the technical support for further assistance"
        ):
            response = account_helper.dm_api_account.account_api.put_v1_account_token(token=token)
