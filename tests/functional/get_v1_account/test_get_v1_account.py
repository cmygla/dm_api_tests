import allure

from checkers.get_v1_account import GetV1Account
from checkers.http_checkers import check_status_code_http


@allure.suite("Тест на проверку метода GET:v1/account")
class TestGetV1Account:

    @allure.sub_suite("Позитивные тесты")
    @allure.title("Проверка получения текущего пользователя")
    def test_get_v1_account_auth(self, auth_account_helper):
        with check_status_code_http():
            response = auth_account_helper.get_user_info()
            login = auth_account_helper.get_credentials().login
            GetV1Account.check_response_values(login, response)

    @allure.sub_suite("Негативные тесты")
    @allure.title("Проверка получения неактивного пользователя")
    def test_get_v1_account_no_auth(self, account_helper):
        with check_status_code_http(401, "User must be authenticated"):
            response = account_helper.get_user_info()
